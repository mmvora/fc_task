from newspaper import Article

def get_text_nlp(url: str) -> dict:
    article = Article(url)
    article.download()
    article.parse()
    article_text = article.text
    article.nlp()
    article_summary = article.summary

    return {
        "text": article_text,
        "summary": article_summary
    }


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Dividend"
    print(get_text_nlp(url))