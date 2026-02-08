"""WhatsApp Chat Parser - Parse chat exports from iOS and Android formats."""

import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd
from pathlib import Path


class ChatParser:
    """Parse WhatsApp chat export files."""
    
    # Regex patterns for different export formats
    ANDROID_PATTERN = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APap][Mm])\s-\s([^:]+):\s(.+)'
    IOS_PATTERN = r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s?[APap][Mm])\]\s([^:]+):\s(.+)'
    ALTERNATIVE_PATTERN = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s([^:]+):\s(.+)'
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize the parser with an optional file path."""
        self.file_path = file_path
        self.messages: List[Dict] = []
        self.df: Optional[pd.DataFrame] = None
        
    def load_chat(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Load and parse a WhatsApp chat export file.
        
        Args:
            file_path: Path to the chat export file. If None, uses self.file_path
            
        Returns:
            DataFrame containing parsed messages
        """
        path = file_path or self.file_path
        if not path:
            raise ValueError("No file path provided")
            
        file_path_obj = Path(path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Chat file not found: {path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.messages = self._parse_content(content)
        self.df = pd.DataFrame(self.messages)
        
        if not self.df.empty:
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
            self.df = self.df.sort_values('datetime').reset_index(drop=True)
            
        return self.df
    
    def _parse_content(self, content: str) -> List[Dict]:
        """Parse chat content and extract messages.
        
        Args:
            content: Raw chat file content
            
        Returns:
            List of message dictionaries
        """
        lines = content.split('\n')
        messages = []
        current_message = None
        
        for line in lines:
            if not line.strip():
                continue
                
            # Try to match different patterns
            match = self._match_message(line)
            
            if match:
                # Save previous message if exists
                if current_message:
                    messages.append(current_message)
                    
                timestamp, author, message = match
                current_message = {
                    'datetime': self._parse_datetime(timestamp),
                    'author': author.strip(),
                    'message': message.strip(),
                    'is_media': self._is_media_message(message),
                    'is_system': self._is_system_message(author, message)
                }
            else:
                # Continuation of previous message (multiline)
                if current_message:
                    current_message['message'] += '\n' + line.strip()
                    
        # Add last message
        if current_message:
            messages.append(current_message)
            
        return messages
    
    def _match_message(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Try to match a line with known message patterns.
        
        Args:
            line: Single line from chat file
            
        Returns:
            Tuple of (timestamp, author, message) or None if no match
        """
        patterns = [
            self.ANDROID_PATTERN,
            self.IOS_PATTERN,
            self.ALTERNATIVE_PATTERN
        ]
        
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                return match.groups()
                
        return None
    
    def _parse_datetime(self, timestamp: str) -> datetime:
        """Parse datetime from various formats.
        
        Args:
            timestamp: Timestamp string from chat
            
        Returns:
            Parsed datetime object
        """
        # Common datetime formats
        formats = [
            '%d/%m/%Y, %I:%M %p',
            '%d/%m/%y, %I:%M %p',
            '%m/%d/%Y, %I:%M %p',
            '%m/%d/%y, %I:%M %p',
            '%d/%m/%Y, %H:%M',
            '%d/%m/%y, %H:%M',
            '%m/%d/%Y, %H:%M',
            '%m/%d/%y, %H:%M',
            '%d/%m/%Y, %I:%M:%S %p',
            '%d/%m/%y, %I:%M:%S %p',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp.strip(), fmt)
            except ValueError:
                continue
                
        raise ValueError(f"Could not parse datetime: {timestamp}")
    
    def _is_media_message(self, message: str) -> bool:
        """Check if message is a media attachment.
        
        Args:
            message: Message text
            
        Returns:
            True if message contains media
        """
        media_indicators = [
            '<Media omitted>',
            'image omitted',
            'video omitted',
            'audio omitted',
            'document omitted',
            'sticker omitted',
            'GIF omitted',
            '.jpg',
            '.png',
            '.mp4',
            '.pdf'
        ]
        
        return any(indicator.lower() in message.lower() for indicator in media_indicators)
    
    def _is_system_message(self, author: str, message: str) -> bool:
        """Check if message is a system notification.
        
        Args:
            author: Message author
            message: Message text
            
        Returns:
            True if message is a system notification
        """
        system_indicators = [
            'changed the subject',
            'changed this group',
            'created group',
            'added',
            'removed',
            'left',
            'joined using this group',
            'security code changed',
            'Messages and calls are end-to-end encrypted',
            'You deleted this message',
            'This message was deleted'
        ]
        
        return any(indicator.lower() in message.lower() for indicator in system_indicators)
    
    def get_chat_info(self) -> Dict:
        """Get basic information about the parsed chat.
        
        Returns:
            Dictionary with chat statistics
        """
        if self.df is None or self.df.empty:
            return {}
            
        return {
            'total_messages': len(self.df),
            'participants': self.df['author'].nunique(),
            'participant_names': self.df['author'].unique().tolist(),
            'date_range': {
                'start': self.df['datetime'].min(),
                'end': self.df['datetime'].max()
            },
            'media_messages': self.df['is_media'].sum(),
            'system_messages': self.df['is_system'].sum(),
            'text_messages': (~self.df['is_media'] & ~self.df['is_system']).sum()
        }
