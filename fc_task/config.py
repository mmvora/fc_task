import os
from dotenv import dotenv_values

dotenv_config = dotenv_values(".env")


def load_redis_url() -> str:
    redis_url = os.getenv("REDIS_URL", dotenv_config.get("REDIS_URL"))
    if redis_url is None:
        raise Exception("REDIS_URL environment variable not set")
    os.environ["REDIS_URL"] = redis_url
    return redis_url


def load_db_url() -> str:
    db_url = os.getenv("DATABASE_URL", dotenv_config.get("DATABASE_URL"))
    if db_url is None:
        raise Exception("DATABASE_URL environment variable not set")
    os.environ["DATABASE_URL"] = db_url
    return db_url


def load_openai_creds() -> dict:
    api_key = os.getenv("OPENAI_API_KEY", dotenv_config.get("OPENAI_API_KEY"))
    if api_key is None:
        raise Exception("OPENAI_API_KEY environment variable not set")

    org_id = os.getenv("OPENAI_ORG_ID", dotenv_config.get("OPENAI_ORG_ID"))
    base_url = os.getenv("OPENAI_BASE_URL", dotenv_config.get("OPENAI_BASE_URL"))

    if org_id is None and base_url is None:
        raise Exception("Please provide either OPENAI_ORG_ID or OPENAI_BASE_URL")

    return {"api_key": api_key, "org_id": org_id, "base_url": base_url}


def get_openai_model() -> str:
    environment_model = os.getenv("OPENAI_MODEL", dotenv_config.get("OPENAI_MODEL"))
    if environment_model is None:
        raise Exception("OPENAI_MODEL environment variable is not set")
    return environment_model

def get_neo4j_url() -> str:
    neo4j_url = os.getenv("NEO4J_URL", dotenv_config.get("NEO4J_URL"))
    if neo4j_url is None:
        raise Exception("NEO4J_URL environment variable not set")
    return neo4j_url

def get_neo4j_user() -> str:
    neo4j_user = os.getenv("NEO4J_USER", dotenv_config.get("NEO4J_USER"))
    if neo4j_user is None:
        raise Exception("NEO4J_USER environment variable not set")
    return neo4j_user

def get_neo4j_password() -> str:
    neo4j_password = os.getenv("NEO4J_PASSWORD", dotenv_config.get("NEO4J_PASSWORD"))
    if neo4j_password is None:
        raise Exception("NEO4J_PASSWORD environment variable not set")
    return neo4j_password

def get_neo4j_creds() -> dict:
    return {
        "url": get_neo4j_url(),
        "user": get_neo4j_user(),
        "password": get_neo4j_password(),
    }