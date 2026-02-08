"""Unit tests for ChatParser module."""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from whatsapp_analyzer.parser import ChatParser


class TestChatParser:
    """Test cases for ChatParser class."""
    
    def test_parser_initialization(self):
        """Test parser initialization."""
        parser = ChatParser()
        assert parser.file_path is None
        assert parser.messages == []
        assert parser.df is None
    
    def test_parser_with_file_path(self):
        """Test parser initialization with file path."""
        parser = ChatParser("test.txt")
        assert parser.file_path == "test.txt"
    
    def test_match_android_pattern(self):
        """Test matching Android message pattern."""
        parser = ChatParser()
        line = "12/25/2023, 10:30 AM - Alice: Hey! Merry Christmas!"
        match = parser._match_message(line)
        
        assert match is not None
        assert len(match) == 3
        assert match[1] == "Alice"
        assert match[2] == "Hey! Merry Christmas!"
    
    def test_match_ios_pattern(self):
        """Test matching iOS message pattern."""
        parser = ChatParser()
        line = "[12/25/2023, 10:30:00 AM] Alice: Hey! Merry Christmas!"
        match = parser._match_message(line)
        
        assert match is not None
        assert len(match) == 3
        assert match[1] == "Alice"
        assert match[2] == "Hey! Merry Christmas!"
    
    def test_is_media_message(self):
        """Test media message detection."""
        parser = ChatParser()
        
        assert parser._is_media_message("<Media omitted>")
        assert parser._is_media_message("Check out this image omitted")
        assert parser._is_media_message("file.jpg attached")
        assert not parser._is_media_message("Just a normal message")
    
    def test_is_system_message(self):
        """Test system message detection."""
        parser = ChatParser()
        
        assert parser._is_system_message("System", "Alice changed the subject to Test")
        assert parser._is_system_message("System", "Bob added Charlie")
        assert parser._is_system_message("System", "Alice left")
        assert not parser._is_system_message("Alice", "Hey there!")
    
    def test_load_sample_chat(self):
        """Test loading sample chat file."""
        sample_path = Path(__file__).parent.parent / 'data' / 'sample' / 'sample_chat.txt'
        
        if sample_path.exists():
            parser = ChatParser(str(sample_path))
            df = parser.load_chat()
            
            assert df is not None
            assert len(df) > 0
            assert 'datetime' in df.columns
            assert 'author' in df.columns
            assert 'message' in df.columns
            assert 'is_media' in df.columns
            assert 'is_system' in df.columns
    
    def test_get_chat_info(self):
        """Test chat info extraction."""
        sample_path = Path(__file__).parent.parent / 'data' / 'sample' / 'sample_chat.txt'
        
        if sample_path.exists():
            parser = ChatParser(str(sample_path))
            parser.load_chat()
            info = parser.get_chat_info()
            
            assert 'total_messages' in info
            assert 'participants' in info
            assert 'participant_names' in info
            assert 'date_range' in info
            assert info['total_messages'] > 0
            assert info['participants'] >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
