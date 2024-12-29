import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fc_task.config import load_db_url

from fc_task.article_model import Article, Base
from fc_task.runner.tasks import extract_url

DATA_SOURCE_DIR = os.getenv("DATA_SOURCE_DIR", "data_source")


def main() -> None:
    engine = create_engine(load_db_url())
    Base.metadata.create_all(engine)

    # loop through CSV files in the directory
    for file in os.listdir(DATA_SOURCE_DIR):
        if file.endswith(".csv"):
            # read the file
            with open(os.path.join(DATA_SOURCE_DIR, file), "r") as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)
                for row in reader:
                    url = row[1]
                    with Session(engine) as session:
                        if session.query(Article).filter(Article.url == url).first():
                            print(f"Skipping {url}")
                            continue
                        else:
                            print(f"Extracting {url}")
                            extract_url.delay(url)


if __name__ == "__main__":
    main()
