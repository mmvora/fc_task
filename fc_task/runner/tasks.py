from .celery import app
from urllib.parse import unquote
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fc_task.config import load_db_url
from fc_task.extractor.text_llm_summary import get_text_summary
from fc_task.extractor.text_nlp import get_text_nlp
from fc_task.article_model import Article


@app.task
def extract_url(url: str) -> None:
    engine = create_engine(load_db_url())
    print(f"Processing {url}")
    # the title is the last term in the slash-separated URL before any .
    title = unquote(url.split("/")[-1].split(".")[0])
    print(f"Processing {title}")
    try:
        text_nlp = get_text_nlp(url)
        text_summary = get_text_summary(text_nlp["text"])
        article = Article(
            url=url,
            title=title,
            full_content=text_nlp["text"],
            nlp_summary=text_nlp["summary"],
            ai_summary=text_summary,
        )
        with Session(engine) as session:
            session.add(article)
            session.commit()
    except Exception as e:
        print(f"Error processing {url}: {e}")
