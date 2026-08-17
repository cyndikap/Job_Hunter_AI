from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class UserMemory:
    def __init__(self, storage_path: str | None = None):
        default_path = Path(__file__).resolve().parents[3] / ".jobhunter" / "user_memory.json"
        candidate = Path(storage_path) if storage_path else default_path

        try:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            with candidate.open("a", encoding="utf-8"):
                pass
            self.storage_path = candidate
        except OSError:
            fallback = default_path
            fallback.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path = fallback

        self._profile = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.storage_path.exists():
            return {
                "preferences": {},
                "interaction_history": [],
                "favorite_companies": [],
                "target_locations": [],
                "salary_targets": [],
                "target_technologies": [],
            }
        try:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return {
                "preferences": {},
                "interaction_history": [],
                "favorite_companies": [],
                "target_locations": [],
                "salary_targets": [],
                "target_technologies": [],
            }

    def _save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as handle:
            json.dump(self._profile, handle, ensure_ascii=False, indent=2)

    def save_preferences(self, preferences: dict[str, Any]) -> dict[str, Any]:
        self._profile["preferences"].update(preferences)
        self._save()
        return self._profile["preferences"]

    def record_interaction(self, message: str) -> None:
        self._profile.setdefault("interaction_history", []).append(message)
        self._save()

    def get_profile(self) -> dict[str, Any]:
        return self._profile


user_memory = UserMemory()
