import ipaddress
import socket
import logging
from urllib.parse import urlparse
from src.exceptions import InvalidURLError, WebsiteFetchError

logger = logging.getLogger(__name__)    

ALLOWED_SCHEMES = {"http", "https"}
ALLOWED_PORTS = {80, 443}

def validate_url(url):
    """Validate URL syntax and reject non-public destinations."""           
    logger.info("URL validation started.")
    url = url.strip()

    # Reject malformed URLs and unsupported schemes.
    parsed_url = urlparse(url)     

    # If the scheme is empty, assume HTTPS.
    if not parsed_url.scheme:  
        url = "https://" + url
        logger.info("URL scheme was missing; HTTPS was added")
        parsed_url = urlparse(url)

    if parsed_url.scheme.lower() not in ALLOWED_SCHEMES:
        logger.warning("URL rejected: unsupported scheme.")
        raise InvalidURLError("Unsupported URL scheme. Please use HTTP or HTTPS.")        

    # Reject URLs without a hostname or containing credentials.    
    if (
        not parsed_url.hostname 
        or parsed_url.username is not None
        or parsed_url.password is not None
    ):
        logger.warning("URL rejected: missing hostname or URL contains embedded credentials.")
        raise InvalidURLError("URL rejected: missing hostname or URL contains embedded credentials")

    # Accessing port can raise ValueError for malformed ports.
    try:
        port = parsed_url.port       
    except ValueError as e:
        logger.warning("URL rejected: The URL contains an invalid port.")
        raise InvalidURLError("The URL contains an invalid port.") from e

    effective_port = port or (443 if parsed_url.scheme.lower() == "https" else 80)

    if effective_port not in ALLOWED_PORTS:
        logger.warning("URL rejected: invalid port.")        
        raise InvalidURLError("URL rejected: invalid port.")             

    # Reject IP literals and DNS names that resolve to non-public addresses.
    try:
        try:
            addresses = [ipaddress.ip_address(parsed_url.hostname)]
        except ValueError:
              results = socket.getaddrinfo(            
                  parsed_url.hostname,
                  effective_port,
                  type=socket.SOCK_STREAM,
              )
              addresses = [
                  ipaddress.ip_address(result[4][0].split("%")[0])
                  for result in results
              ]

        if not addresses:
            logger.warning("URL rejected: hostname resolution failed.")
            raise WebsiteFetchError("The website hostname could not be resolved.")

        if any(not address.is_global for address in addresses):
            logger.warning("URL rejected: destination resolves to a restricted IP address.")
            raise InvalidURLError("This URL resolves to a non-public IP address.")

    except (InvalidURLError, WebsiteFetchError):
        raise
    except (OSError, ValueError) as exc:
        logger.warning("Hostname resolution failed or returned an invalid address; error_type=%s.",type(exc).__name__)
        raise WebsiteFetchError("Could not safely resolve the website hostname.") from exc

    logger.info("URL validation successful.")
    # Return a normalized URL, including the default HTTPS scheme if omitted.
    return url
