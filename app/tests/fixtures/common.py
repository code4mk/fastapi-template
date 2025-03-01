from unittest.mock import MagicMock
from fastapi import UploadFile
from io import BytesIO
import pytest

@pytest.fixture
def mock_file_image():
    """
    Creates a mock UploadFile that simulates an image upload.
    Returns a MagicMock object that mimics UploadFile behavior with image-specific attributes.
    """
    # Create a small 1x1 black pixel in PNG format
    image_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00'
        b'\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc'
        b'\x00\x00\x00\x02\x00\x01\xe5\x27\xde\xfc\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.png"
    mock_file.content_type = "image/png"
    mock_file.file = BytesIO(image_data)
    return mock_file

@pytest.fixture
def mock_file_video():
    """
    Creates a mock UploadFile that simulates a video upload.
    Returns a MagicMock object that mimics UploadFile behavior with video-specific attributes.
    """
    # Create a minimal valid video file bytes
    video_data = b'FaKeViDeOdAtA'  # This is just a placeholder, not actual video data
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_video.mp4"
    mock_file.content_type = "video/mp4"
    mock_file.file = BytesIO(video_data)
    return mock_file

@pytest.fixture
def mock_file_pdf():
    """
    Creates a mock UploadFile that simulates a PDF upload.
    Returns a MagicMock object that mimics UploadFile behavior with PDF-specific attributes.
    """
    # Create a minimal valid PDF file bytes
    pdf_data = b'%PDF-1.4\n%EOF'  # Minimal PDF file structure
    
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_document.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.file = BytesIO(pdf_data)
    return mock_file
