from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = Path(__file__).resolve().parent / "models"
MODEL_BUNDLE_PATH = MODELS_DIR / "model_bundle.joblib"
MODEL_REPORT_PATH = MODELS_DIR / "model_report.json"
LEGACY_MODEL_PATH = BASE_DIR / "ML_models" / "best_model.joblib"


def _read_dataset(csv_path: Path) -> pd.DataFrame:
    """Load dataset and drop unnamed helper columns from malformed CSV exports."""
    frame = pd.read_csv(csv_path)
    frame = frame.loc[:, ~frame.columns.str.contains(r"^Unnamed")]
    if "prognosis" not in frame.columns:
        raise ValueError(f"Missing prognosis column in {csv_path}")
    return frame


def _prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, LabelEncoder]:
    train_df = _read_dataset(DATASET_DIR / "training_data.csv")
    test_df = _read_dataset(DATASET_DIR / "test_data.csv")

    x_train = train_df.drop(columns=["prognosis"])
    y_train_raw = train_df["prognosis"]

    x_test = test_df.drop(columns=["prognosis"])
    y_test_raw = test_df["prognosis"]

    # Keep exact feature contract used by the original project.
    x_test = x_test.reindex(columns=x_train.columns, fill_value=0)

    encoder = LabelEncoder()
    y_train = pd.Series(encoder.fit_transform(y_train_raw), index=y_train_raw.index)
    y_test = pd.Series(encoder.transform(y_test_raw), index=y_test_raw.index)

    return x_train, x_test, y_train, y_test, encoder


def _build_models(random_state: int) -> dict[str, Any]:
    models: dict[str, Any] = {
        "SVM": SVC(probability=True, C=3.0, gamma="scale", kernel="rbf"),
        "Random Forest": RandomForestClassifier(
            n_estimators=350,
            random_state=random_state,
            n_jobs=-1,
        ),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state),
        "Naive Bayes": GaussianNB(),
    }

    # Optional advanced models are loaded only during training runs.
    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            use_label_encoder=False,
            eval_metric="mlogloss",
            n_estimators=250,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=random_state,
            n_jobs=1,
        )
    except Exception:
        pass

    try:
        from lightgbm import LGBMClassifier

        models["LightGBM"] = LGBMClassifier(
            n_estimators=250,
            learning_rate=0.05,
            random_state=random_state,
            verbose=-1,
        )
    except Exception:
        pass

    return models


def train_and_save_models(random_state: int = 42) -> dict[str, Any]:
    """Train all models, select the best via cross-validation, and persist the bundle."""
    x_train, x_test, y_train, y_test, encoder = _prepare_data()

    models = _build_models(random_state=random_state)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    model_scores: list[dict[str, float | str]] = []

    for model_name, model in models.items():
        cv_scores = cross_val_score(model, x_train, y_train, cv=cv, scoring="accuracy", n_jobs=1)
        model.fit(x_train, y_train)
        test_predictions = model.predict(x_test)
        test_accuracy = accuracy_score(y_test, test_predictions)

        model_scores.append(
            {
                "model": model_name,
                "cv_accuracy": float(cv_scores.mean()),
                "cv_std": float(cv_scores.std()),
                "test_accuracy": float(test_accuracy),
            }
        )

    ranked_scores = sorted(
        model_scores,
        key=lambda row: (float(row["cv_accuracy"]), float(row["test_accuracy"])),
        reverse=True,
    )
    best_model_name = str(ranked_scores[0]["model"])
    best_model = models[best_model_name]

    selection_reason = (
        f"{best_model_name} selected - highest 5-fold cross-validation accuracy: "
        f"{ranked_scores[0]['cv_accuracy'] * 100:.2f}%"
    )

    bundle = {
        "best_model": best_model,
        "best_model_name": best_model_name,
        "model_scores": ranked_scores,
        "models_available": [row["model"] for row in ranked_scores],
        "encoder": encoder,
        "feature_names": list(x_train.columns),
        "selection_reason": selection_reason,
        "metadata": {
            "symptom_count": int(x_train.shape[1]),
            "disease_count": int(len(encoder.classes_)),
        },
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_BUNDLE_PATH)
    MODEL_REPORT_PATH.write_text(json.dumps(ranked_scores, indent=2), encoding="utf-8")

    return bundle


def build_bundle_from_legacy_model() -> dict[str, Any]:
    """Fallback for environments where full training fails but legacy model exists."""
    if not LEGACY_MODEL_PATH.exists():
        raise FileNotFoundError("Legacy model not found")

    best_model, encoder = joblib.load(LEGACY_MODEL_PATH)
    train_df = _read_dataset(DATASET_DIR / "training_data.csv")
    feature_names = list(train_df.drop(columns=["prognosis"]).columns)

    bundle = {
        "best_model": best_model,
        "best_model_name": "Legacy Best Model",
        "model_scores": [
            {
                "model": "Legacy Best Model",
                "cv_accuracy": 0.0,
                "cv_std": 0.0,
                "test_accuracy": 0.0,
            }
        ],
        "models_available": ["Legacy Best Model"],
        "encoder": encoder,
        "feature_names": feature_names,
        "selection_reason": "Legacy model loaded because full retraining was unavailable.",
        "metadata": {
            "symptom_count": len(feature_names),
            "disease_count": int(len(encoder.classes_)),
        },
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_BUNDLE_PATH)
    return bundle
