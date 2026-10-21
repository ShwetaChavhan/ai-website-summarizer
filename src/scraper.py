# Dependencies:
import requests
import logging
from bs4 import BeautifulSoup
from src.exceptions import WebsiteFetchError
from src.url_security import validate_url

logger = logging.getLogger(__name__)

# Reuse these headers for website requests to identify the client and
# specify the preferred response formats and language.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Define a function that fetches and extracts readable content from a website.
def fetch_website_contents(url):
    """Fetch a webpage and extract its readable text.

        Args:
        url: The HTTP or HTTPS URL of the webpage to fetch.

    Returns:
        A string containing the webpage title and extracted text,
        or an error message if the request fails.
    """    
    logger.info("Website fetch started.")

    url=validate_url(url)
    try:
        # Send an HTTP GET request   
        # Pass the headers and stop waiting if the request takes more than 15 seconds.
        response = requests.get(url, headers=HEADERS, timeout=15)
        logger.info("Website responded with HTTP status %s.", response.status_code)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.warning("Webpage request timed out.")
        raise WebsiteFetchError(f"Could not fetch the website. Error: {e}")

    logger.info("HTML parsing started.")
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "No title found"

    # Remove elements that usually do not contribute to the main readable content.  
    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()

    # Extract the remaining text from the HTML.
    text = soup.get_text(separator="\n", strip=True)
    logger.info("Website fetched successfully")
    return f"Title: {title}\n\nPage contents:\n{text}"

