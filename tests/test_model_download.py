import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.model_download import download_file


def test_download_file_skips_when_exists(tmp_path):
    target = tmp_path / "model.pkl"
    target.write_text("cached")
    result = download_file("https://example.com/model.pkl", target, skip_if_exists=True)
    assert result == target
    assert target.read_text() == "cached"


def test_download_file_overwrites_when_not_exists(tmp_path):
    target = tmp_path / "model.pkl"
    fake_content = b"model-data"
    mock_response = MagicMock()
    mock_response.read.return_value = fake_content
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("app.model_download.urllib.request.urlopen", return_value=mock_response):
        result = download_file("https://example.com/model.pkl", target, skip_if_exists=False)

    assert result == target
    assert target.read_bytes() == fake_content


def test_download_file_retries_on_failure(tmp_path):
    target = tmp_path / "model.pkl"
    call_count = 0

    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise OSError("Connection refused")
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"data"
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    with patch("app.model_download.urllib.request.urlopen", side_effect=side_effect):
        result = download_file("https://example.com/model.pkl", target, retries=3, delay=0)

    assert result == target
    assert call_count == 3
