"""Download files from URL with retry logic and local caching."""
import logging
import time
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)


def download_file(
    url: str,
    target: Path,
    *,
    skip_if_exists: bool = True,
    retries: int = 3,
    delay: float = 5.0,
) -> Path:
    """Download a file from *url* to *target* path.

    Args:
        url: Direct download URL.
        target: Local path to save the file.
        skip_if_exists: If True and target exists, skip download.
        retries: Number of retry attempts on failure.
        delay: Seconds to wait between retries.

    Returns:
        The target Path.

    Raises:
        RuntimeError: If all retries fail.
    """
    if skip_if_exists and target.exists():
        logger.info("Model file already exists at %s, skipping download.", target)
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            logger.info("Downloading %s (attempt %d/%d)...", url, attempt, retries)
            with urllib.request.urlopen(url) as response:
                data = response.read()
            target.write_bytes(data)
            logger.info("Download complete: %s (%d bytes)", target, target.stat().st_size)
            return target
        except Exception as e:
            last_error = e
            logger.warning("Attempt %d failed: %s", attempt, e)
            if attempt < retries:
                logger.info("Retrying in %.0f seconds...", delay)
                time.sleep(delay)

    raise RuntimeError(
        f"Failed to download {url} after {retries} attempts. Last error: {last_error}"
    )
