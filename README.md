## AI Website Summarizer

An AI-powered web application that extracts readable content from webpages and generates concise, easy-to-understand summaries using the Groq API.

Built with Python, Gradio, Requests, BeautifulSoup, and the OpenAI Python SDK.

## Overview

Reading long webpages can be time-consung. The AI Website Summarizer simplifies this process by fetching webpage content, extracting readable text, and using a large language model (LLM) to generate a concise summary.

Users can enter a website URL through a simple web interface and view the generated summary in Markdown format.

## Features

- **Web-based interface:** Accepts website URLs through a Gradio interface.
- **URL validation:** Supports HTTP and HTTPS URLs and can automatically add HTTPS when the scheme is omitted.
- **Web scraping:** Fetches webpage content using Python Requests.
- **HTML parsing:** Uses BeautifulSoup to extract readable text and remove common non-content elements.
- **AI-powered summarization:** Uses the Groq API with an OpenAI-compatible Python SDK.
- **Request timeout:** Configures a timeout to prevent requests from waiting indefinitely.
- **Custom exceptions:** Uses application-specific exceptions to distinguish website-fetching failures from other errors.
- **Environment-based configuration:** Loads API credentials from environment variables.
- **Modular codebase:** Separates the user interface, scraping logic, summarization logic, and exception definitions.

## Technology Stack

| Technology        | Purpose                          |
| ----------------- | -------------------------------- |
| Python            | Application logic                |
| Gradio            | Web interface                    |
| requests          | HTTP requests                    |
| beautifulsoup4    | HTML parsing and text extraction |
| Groq API          | AI-generated summaries           |
| OpenAI Python SDK | API client                       |
| dotenv            | Environment variable loading     |


## Project Structure

```text
AI-Website-Summarizer/
├── src/
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── scraper.py
│   ├── url_security.py
│   └── website_summarizer.py
│
├── app.py
├── .env
├── .gitignore
├── app.log
├── README.md
└── requirements.txt
```

### Module Responsibilities

- **`app.py`** — Creates and launches the Gradio interface, handles user requests, and displays summaries or user-friendly error messages.
- **`src/url_security.py`** — Validates URL structure, checks allowed schemes and ports, and rejects URLs that resolve to non-public IP.
- **`src/scraper.py`** — Fetches webpage content using HTTP requests, parses HTML, and extracts readable text.
- **`src/website_summarizer.py`** — Coordinates webpage fetching and AI-powered summarization using the Groq API.
- **`src/exceptions.py`** — Defines custom exceptions for URL validation and website-fetching errors.
- **`src/logging_config.py`** — Configures application-wide logging, including log levels, output file, and log message format.
- **`requirements.txt`** — Lists the Python dependencies required to run the application.
- **`.env.example`** — Documents the required environment variables using placeholder values without exposing credentials.

## Prerequisites

- Python 3.10 or later, subject to dependency compatibility.
- pip.
- A Groq API key.
- An internet connection.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShwetaChavhan/ai-website-summarizer.git
cd ai-website-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get an API key from the [Groq Console](https://console.groq.com/).

Never commit your actual `.env` file or expose your API key in source code.

### 5. Run the application

```bash
python app.py
```

Open the local URL printed by Gradio in your browser.

## How It Works

1. The user enters a webpage URL.
2. The application validates the URL and normalizes URLs without a scheme.
3. The scraper sends an HTTP GET request with configured headers and a timeout.
4. BeautifulSoup parses the HTML and removes common irrelevant elements.
5. The extracted text is limited to a configured character count.
6. The application sends the webpage content to the Groq API.
7. The language model generates a concise summary.
8. Gradio displays the result to the user.

## Error Handling

The application uses validation and exception handling to manage expected failures.

Examples include:

- Empty or invalid URLs.
- Unsupported URL schemes.
- Missing hostnames or embedded credentials.
- Network errors and HTTP failures.
- Request timeouts.
- AI API authentication, connectivity, or rate-limit failures.

The application distinguishes between fetching errors and AI-service errors so that an error message is never treated as webpage content.

## Security Considerations

The application fetches URLs supplied by users, so URL validation alone is not sufficient for public deployment.

Recommended safeguards include:

- Keeping API keys in environment variables.
- Limiting downloaded response sizes and extracted text.
- Restricting requests to permitted network destinations.
- Blocking loopback, private, link-local, and other prohibited IP addresses.
- Validating redirect destinations and accounting for DNS resolution.
- Restricting supported content types.
- Returning safe error messages without exposing sensitive diagnostic information.

**Important:** Do not expose the application publicly until appropriate Server-Side Request Forgery (SSRF) protections and resource limits have been implemented and tested.

## Limitations

- JavaScript-rendered websites may not expose their full content to the scraper.
- Some websites may block automated requests or require authentication.
- API availability and usage limits depend on the provider and account.

## Future Improvements

- Strengthen SSRF protection and redirect validation.
- Add maximum response-size and content-type checks.
- Improve main-article extraction.
- Add automated tests using pytest.

## Author

**Shweta Chavhan**

Built as a learning project exploring Python web scraping, API integration, AI-powered text summarization.

GitHub: [Shweta Chavhan](https://github.com/ShwetaChavhan)
