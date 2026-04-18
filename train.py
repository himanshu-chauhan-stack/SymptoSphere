from __future__ import annotations

import json

from ml.model_trainer import MODEL_REPORT_PATH, train_and_save_models


def main() -> None:
    print("Training models and generating a fresh model bundle...")
    bundle = train_and_save_models()
    print(f"Best model: {bundle['best_model_name']}")
    print(f"Selection reason: {bundle['selection_reason']}")

    if MODEL_REPORT_PATH.exists():
        report = json.loads(MODEL_REPORT_PATH.read_text(encoding="utf-8"))
        print("Model ranking:")
        for row in report:
            print(
                f" - {row['model']}: CV={row['cv_accuracy'] * 100:.2f}% "
                f"Test={row['test_accuracy'] * 100:.2f}%"
            )


if __name__ == "__main__":
    main()