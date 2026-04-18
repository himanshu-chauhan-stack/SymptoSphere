from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from .model_trainer import (
    MODEL_BUNDLE_PATH,
    build_bundle_from_legacy_model,
    train_and_save_models,
)


class SymptoPredictor:
    """Inference wrapper around the trained multi-model bundle."""

    def __init__(self, retrain: bool = False) -> None:
        self.bundle = self._load_bundle(retrain=retrain)
        self.best_model = self.bundle["best_model"]
        self.best_model_name = str(self.bundle["best_model_name"])
        self.encoder = self.bundle["encoder"]
        self.feature_names = list(self.bundle["feature_names"])
        self.model_scores = list(self.bundle["model_scores"])
        self.selection_reason = str(self.bundle["selection_reason"])
        self.metadata = dict(self.bundle.get("metadata", {}))
        self._index_map = {name: idx for idx, name in enumerate(self.feature_names)}

    def _load_bundle(self, retrain: bool) -> dict[str, Any]:
        if MODEL_BUNDLE_PATH.exists() and not retrain:
            return joblib.load(MODEL_BUNDLE_PATH)

        try:
            return train_and_save_models()
        except Exception:
            if MODEL_BUNDLE_PATH.exists():
                return joblib.load(MODEL_BUNDLE_PATH)
            return build_bundle_from_legacy_model()

    def get_all_symptoms(self) -> list[str]:
        return self.feature_names

    def get_model_comparison(self) -> list[dict[str, str | float]]:
        rows: list[dict[str, str | float]] = []
        for row in self.model_scores:
            rows.append(
                {
                    "model": str(row["model"]),
                    "cv_accuracy": float(row["cv_accuracy"]),
                    "cv_std": float(row["cv_std"]),
                    "test_accuracy": float(row["test_accuracy"]),
                }
            )
        return rows

    def predict_top3(self, selected_symptoms: list[str]) -> list[dict[str, str | float]]:
        input_vector = np.zeros(len(self.feature_names), dtype=int)

        for symptom in selected_symptoms:
            idx = self._index_map.get(symptom)
            if idx is not None:
                input_vector[idx] = 1

        sample = pd.DataFrame([input_vector], columns=self.feature_names)
        probabilities = self.best_model.predict_proba(sample)[0]
        class_names = self.encoder.inverse_transform(np.arange(len(probabilities)))

        top_indices = probabilities.argsort()[-3:][::-1]
        return [
            {
                "disease": str(class_names[idx]),
                "confidence": float(probabilities[idx] * 100),
            }
            for idx in top_indices
        ]

    @property
    def symptom_count(self) -> int:
        return int(self.metadata.get("symptom_count", len(self.feature_names)))

    @property
    def disease_count(self) -> int:
        return int(self.metadata.get("disease_count", len(self.encoder.classes_)))

    @property
    def top_accuracy_percent(self) -> float:
        if not self.model_scores:
            return 0.0
        return float(self.model_scores[0]["cv_accuracy"] * 100)
