from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .disease_data import (
    DOCTOR_SEED_DATA,
    SPECIALIZATION_TO_DOCTOR_ID,
    get_disease_seed_data,
    get_disease_specialization_map,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(__file__).resolve().parent / "sympthosphere.db"


def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_database(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with _connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS disease_info (
                disease_name TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                medicines TEXT NOT NULL,
                home_remedies TEXT NOT NULL,
                precautions TEXT NOT NULL,
                urgency_level TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                experience TEXT NOT NULL,
                rating REAL NOT NULL,
                avatar_type TEXT NOT NULL,
                bio TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS disease_doctor_map (
                disease_name TEXT PRIMARY KEY,
                primary_doctor_id INTEGER NOT NULL,
                backup_doctor_id INTEGER NOT NULL,
                FOREIGN KEY(primary_doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(backup_doctor_id) REFERENCES doctors(id)
            )
            """
        )

        _seed_disease_info(cursor)
        _seed_doctors(cursor)
        _seed_disease_doctor_mapping(cursor)

        conn.commit()


def _seed_disease_info(cursor: sqlite3.Cursor) -> None:
    entries = get_disease_seed_data()
    for row in entries:
        cursor.execute(
            """
            INSERT OR REPLACE INTO disease_info (
                disease_name, description, medicines, home_remedies, precautions, urgency_level
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["disease_name"],
                row["description"],
                json.dumps(row["medicines"]),
                json.dumps(row["home_remedies"]),
                json.dumps(row["precautions"]),
                row["urgency_level"],
            ),
        )


def _seed_doctors(cursor: sqlite3.Cursor) -> None:
    for doctor in DOCTOR_SEED_DATA:
        cursor.execute(
            """
            INSERT OR REPLACE INTO doctors (
                id, name, specialization, experience, rating, avatar_type, bio
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doctor["id"],
                doctor["name"],
                doctor["specialization"],
                doctor["experience"],
                doctor["rating"],
                doctor["avatar_type"],
                doctor["bio"],
            ),
        )


def _seed_disease_doctor_mapping(cursor: sqlite3.Cursor) -> None:
    specialization_map = get_disease_specialization_map()
    fallback_id = SPECIALIZATION_TO_DOCTOR_ID["General Physician"]

    for disease_name, specialization in specialization_map.items():
        primary_id = SPECIALIZATION_TO_DOCTOR_ID.get(specialization, fallback_id)
        cursor.execute(
            """
            INSERT OR REPLACE INTO disease_doctor_map (
                disease_name, primary_doctor_id, backup_doctor_id
            ) VALUES (?, ?, ?)
            """,
            (disease_name, primary_id, fallback_id),
        )


def _loads_list(raw_json: str) -> list[str]:
    try:
        data = json.loads(raw_json)
        if isinstance(data, list):
            return [str(item) for item in data]
        return []
    except json.JSONDecodeError:
        return []


def fetch_disease_info(disease_name: str, db_path: Path = DB_PATH) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT disease_name, description, medicines, home_remedies, precautions, urgency_level
            FROM disease_info
            WHERE TRIM(LOWER(disease_name)) = TRIM(LOWER(?))
            """,
            (disease_name,),
        ).fetchone()

    if row is None:
        return None

    return {
        "disease_name": row["disease_name"],
        "description": row["description"],
        "medicines": _loads_list(row["medicines"]),
        "home_remedies": _loads_list(row["home_remedies"]),
        "precautions": _loads_list(row["precautions"]),
        "urgency_level": row["urgency_level"],
    }


def fetch_recommended_doctors(disease_name: str, db_path: Path = DB_PATH) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT d.id, d.name, d.specialization, d.experience, d.rating, d.avatar_type, d.bio
            FROM disease_doctor_map m
            JOIN doctors d ON d.id IN (m.primary_doctor_id, m.backup_doctor_id)
            WHERE TRIM(LOWER(m.disease_name)) = TRIM(LOWER(?))
            ORDER BY CASE WHEN d.id = m.primary_doctor_id THEN 0 ELSE 1 END
            """,
            (disease_name,),
        ).fetchall()

        if not rows:
            rows = conn.execute(
                """
                SELECT id, name, specialization, experience, rating, avatar_type, bio
                FROM doctors
                WHERE specialization = 'General Physician'
                LIMIT 1
                """
            ).fetchall()

    doctors: list[dict[str, Any]] = []
    for row in rows:
        doctors.append(
            {
                "id": row["id"],
                "name": row["name"],
                "specialization": row["specialization"],
                "experience": row["experience"],
                "rating": row["rating"],
                "avatar_type": row["avatar_type"],
                "bio": row["bio"],
            }
        )

    # Ensure two recommendations are always available.
    if len(doctors) == 1:
        doctors.append(doctors[0])

    return doctors[:2]
