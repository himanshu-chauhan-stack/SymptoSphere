from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

from database import fetch_disease_info, fetch_recommended_doctors, init_database
from ml import SymptoPredictor

BASE_DIR = Path(__file__).resolve().parent
TRANSLATION_DIR = BASE_DIR / "translations"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "symptosphere-dev-secret")

    init_database()

    try:
        predictor = SymptoPredictor()
        app.config["PREDICTOR"] = predictor
        app.config["MODEL_READY"] = True
        app.config["MODEL_ERROR"] = ""
    except Exception as exc:
        app.logger.exception("Model initialization failed")
        app.config["PREDICTOR"] = None
        app.config["MODEL_READY"] = False
        app.config["MODEL_ERROR"] = str(exc)

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        return {
            "medical_disclaimer": (
                "SymptoSphere is an educational AI tool. "
                "It does not replace professional medical advice."
            )
        }

    @app.route("/")
    def index() -> str:
        predictor_instance: SymptoPredictor | None = app.config.get("PREDICTOR")
        stats = {
            "symptom_count": predictor_instance.symptom_count if predictor_instance else 132,
            "disease_count": predictor_instance.disease_count if predictor_instance else 41,
            "top_accuracy": round(predictor_instance.top_accuracy_percent, 2)
            if predictor_instance
            else 97.0,
        }
        return render_template("index.html", stats=stats)

    @app.route("/predict")
    def predict() -> str:
        predictor_instance: SymptoPredictor | None = app.config.get("PREDICTOR")
        if predictor_instance is None:
            return render_template(
                "error.html",
                error_title="Model Unavailable",
                error_message=(
                    "The machine learning engine could not be initialized. "
                    "Please verify dependencies and try again."
                ),
                error_details=app.config.get("MODEL_ERROR", ""),
            )

        symptoms = predictor_instance.get_all_symptoms()
        return render_template("predict.html", symptoms=symptoms)

    @app.route("/results", methods=["POST"])
    def results() -> str:
        predictor_instance: SymptoPredictor | None = app.config.get("PREDICTOR")
        if predictor_instance is None:
            return render_template(
                "error.html",
                error_title="Prediction Engine Offline",
                error_message="The prediction service is not available right now.",
                error_details=app.config.get("MODEL_ERROR", ""),
            )

        selected_symptoms = request.form.getlist("symptoms")
        if not selected_symptoms:
            flash("Please select at least one symptom.", "warning")
            return redirect(url_for("predict"))

        try:
            predictions = predictor_instance.predict_top3(selected_symptoms)
            model_comparison = predictor_instance.get_model_comparison()
            top_disease = str(predictions[0]["disease"])

            disease_info = fetch_disease_info(top_disease) or _build_fallback_disease_info(top_disease)
            doctors = fetch_recommended_doctors(top_disease)
            doctor_cards = _attach_doctor_messages(doctors=doctors, disease_name=top_disease)

            return render_template(
                "results.html",
                predictions=predictions,
                selected_model=predictor_instance.best_model_name,
                selection_reason=predictor_instance.selection_reason,
                model_comparison=model_comparison,
                selected_symptoms=selected_symptoms,
                disease_info=disease_info,
                doctors=doctor_cards,
            )
        except Exception as exc:
            app.logger.exception("Prediction failed")
            return render_template(
                "error.html",
                error_title="Prediction Error",
                error_message=(
                    "We could not process your request right now. "
                    "Please try again after selecting symptoms once more."
                ),
                error_details=str(exc),
            )

    @app.route("/about")
    def about() -> str:
        return render_template("about.html")

    @app.route("/api/translations/<lang_code>")
    def translation_bundle(lang_code: str) -> Any:
        allowed = {"en", "hi"}
        if lang_code not in allowed:
            abort(404)

        path = TRANSLATION_DIR / f"{lang_code}.json"
        if not path.exists():
            abort(404)

        with path.open("r", encoding="utf-8-sig") as stream:
            payload = json.load(stream)
        return jsonify(payload)

    @app.errorhandler(404)
    def not_found(_: Any) -> tuple[str, int]:
        return (
            render_template(
                "error.html",
                error_title="Page Not Found",
                error_message="The page you requested does not exist.",
                error_details="",
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(_: Any) -> tuple[str, int]:
        return (
            render_template(
                "error.html",
                error_title="Server Error",
                error_message="An unexpected error occurred. Please try again.",
                error_details="",
            ),
            500,
        )

    return app


def _build_fallback_disease_info(disease_name: str) -> dict[str, Any]:
    return {
        "disease_name": disease_name,
        "description": (
            "A specific treatment profile was not found in our local database for this disease label."
        ),
        "medicines": [
            "Symptom-control medicine (as prescribed by doctor)",
            "Hydration support (as prescribed by doctor)",
            "Follow-up treatment after physician evaluation (as prescribed by doctor)",
        ],
        "home_remedies": [
            "Rest and maintain fluid intake.",
            "Consume balanced, easy-to-digest meals.",
            "Track changes in symptoms and seek help if worsening.",
        ],
        "precautions": [
            "Avoid self-medication beyond basic first aid.",
            "Consult a licensed doctor for confirmation.",
            "Visit emergency care for severe or rapidly worsening symptoms.",
        ],
        "urgency_level": "Moderate",
    }


def _attach_doctor_messages(doctors: list[dict[str, Any]], disease_name: str) -> list[dict[str, Any]]:
    response: list[dict[str, Any]] = []
    for doctor in doctors:
        role_hint = "primary specialist" if not response else "backup general support"
        message = (
            f"Hello! Based on your symptoms, you may be showing signs of {disease_name}. "
            f"Please do not panic - this can often be managed with timely care. "
            f"As your {role_hint}, I recommend an in-person medical evaluation soon, "
            f"staying hydrated, and avoiding self-medication."
        )

        payload = dict(doctor)
        payload["message"] = message
        response.append(payload)
    return response


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
