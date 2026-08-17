import re
from typing import Iterable

DEFAULT_SKILLS = [
    "Azure",
    "Databricks",
    "Python",
    "PySpark",
    "Spark",
    "GenAI",
    "Machine Learning",
    "Data Engineering",
    "SQL",
    "DevOps",
    "Power BI",
    "Azure Data Factory",
    "ETL",
    "Data Warehouse",
    "Airflow",
    "Kafka",
]


def normalize_skill(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def extract_skills(text: str, skills: Iterable[str] = DEFAULT_SKILLS) -> list[str]:
    if not text:
        return []

    haystack = text.lower()
    matched: list[str] = []
    for skill in skills:
        normalized_skill = normalize_skill(skill)
        if normalized_skill in haystack:
            matched.append(skill)
    return sorted(set(matched), key=lambda x: x.lower())
