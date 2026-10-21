import logging
import gradio as gr
from src.website_summarizer import summarize
from src.exceptions import InvalidURLError, WebsiteFetchError
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

def summarize_website(url):
    """Return a status message and the website summary."""

    logger.info("Summarization request received.")

    try:
        summary = summarize(url)
        logger.info("Summary generated and returned to the UI.")        
        return "✅ Website summarized successfully.", summary

    except InvalidURLError as e:               
        return f"⚠️ {e}", ""

    except WebsiteFetchError as e:           
        return f"⚠️ {e}", ""    
    
    except Exception:
        logger.exception("Unexpected error while summarizing website")
        return "❌ Something went wrong. Please try again later.", ""


# Create a web interface for the AI summarization function.
app=gr.Interface(
    fn=summarize_website,
    inputs=gr.Textbox(label="Website URL", placeholder="https://example.com", lines=1),
    outputs=[
        gr.Markdown(label="Status"),
        gr.Markdown(label="Summary"),
    ],
    title="AI Website Summarizer"    
)

# Launch the app
app.launch(share=True)  