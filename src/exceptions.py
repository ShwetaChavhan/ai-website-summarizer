class WebsiteFetchError(Exception):
    """Raised when a webpage cannot be fetched or parsed."""

class InvalidURLError(ValueError):
    """Raised when the submitted URL is invalid or uses an unsupported scheme."""    