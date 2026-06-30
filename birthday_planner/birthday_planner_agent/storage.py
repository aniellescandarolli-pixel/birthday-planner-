"""Local JSON persistence helpers for the Birthday Planner agent."""

import json
import os
from typing import Any

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PEOPLE_FILE = os.path.join(_DATA_DIR, "people.json")
PLANS_FILE = os.path.join(_DATA_DIR, "plans.json")


def _ensure_data_dir() -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)


def _load(path: str, default: Any) -> Any:
    _ensure_data_dir()
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return default
        return json.loads(content)


def _save(path: str, data: Any) -> None:
    _ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_people() -> list[dict]:
    return _load(PEOPLE_FILE, [])


def save_people(people: list[dict]) -> None:
    _save(PEOPLE_FILE, people)


def load_plans() -> dict:
    return _load(PLANS_FILE, {})


def save_plans(plans: dict) -> None:
    _save(PLANS_FILE, plans)
