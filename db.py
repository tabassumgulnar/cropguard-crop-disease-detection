"""
CropGuard Database Module (SQLite)
Provides persistent storage, querying, analytics, and demo data insertion
for crop disease reports and agriculture officer verifications.
"""

import os
import sqlite3
from datetime import datetime, timedelta
import random

try:
    import pandas as pd
except ImportError:
    pd = None

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cropguard.db")


def get_db_connection(db_path: str = DB_PATH):
    """Establishes SQLite connection with row factory."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Initializes the database schema if not already created."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            crop TEXT NOT NULL,
            predicted_disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_name TEXT,
            language TEXT DEFAULT 'en',
            is_uncertain INTEGER DEFAULT 0,
            expert_status TEXT DEFAULT 'Pending',
            expert_label TEXT,
            expert_notes TEXT,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            weather_risk TEXT,
            image_name TEXT
        )
        """
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_crop ON reports(crop)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_disease ON reports(predicted_disease)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_timestamp ON reports(timestamp)"
    )
    conn.commit()
    conn.close()


def save_report(
    crop: str,
    predicted_disease: str,
    confidence: float,
    latitude: float,
    longitude: float,
    location_name: str = "",
    language: str = "en",
    is_uncertain: bool = False,
    temperature: float = None,
    humidity: float = None,
    rainfall: float = None,
    weather_risk: str = "Unknown",
    image_name: str = "",
    db_path: str = DB_PATH,
) -> int:
    """Saves a new diagnosis report to the database."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO reports (
            timestamp, crop, predicted_disease, confidence,
            latitude, longitude, location_name, language,
            is_uncertain, expert_status, expert_label, expert_notes,
            temperature, humidity, rainfall, weather_risk, image_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            crop.lower(),
            predicted_disease,
            round(confidence, 4),
            round(latitude, 4),
            round(longitude, 4),
            location_name or "Custom GPS",
            language,
            1 if is_uncertain else 0,
            "Pending",
            None,
            "",
            round(temperature, 1) if temperature is not None else None,
            round(humidity, 1) if humidity is not None else None,
            round(rainfall, 2) if rainfall is not None else None,
            weather_risk,
            image_name,
        ),
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id


def get_all_reports(db_path: str = DB_PATH):
    """Retrieves all reports sorted by timestamp descending as a Pandas DataFrame (or list of dicts if pandas unavailable)."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    query = "SELECT * FROM reports ORDER BY timestamp DESC"
    if pd is not None:
        df = pd.read_sql_query(query, conn)
    else:
        cursor = conn.cursor()
        cursor.execute(query)
        df = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return df


def update_report_expert_label(
    report_id: int,
    expert_label: str,
    status: str = "Confirmed",
    notes: str = "",
    db_path: str = DB_PATH,
) -> bool:
    """Updates the expert verification label and status for a specific report."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE reports
        SET expert_label = ?, expert_status = ?, expert_notes = ?
        WHERE id = ?
        """,
        (expert_label, status, notes, report_id),
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_all_reports(db_path: str = DB_PATH) -> bool:
    """Clears all records in reports table."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports")
    conn.commit()
    conn.close()
    return True


def load_demo_data(db_path: str = DB_PATH) -> int:
    """
    Inserts ~30 realistic sample crop disease reports across agricultural
    regions of Maharashtra (Pune, Nashik, Jalgaon, Ahmednagar, Solapur,
    Nagpur, Kolhapur, Chhatrapati Sambhaji Nagar, Satara, etc.).
    """
    init_db(db_path)

    # 30+ Maharashtra agricultural hotspot centers with jitter
    maharashtra_locations = [
        ("Pune (Baramati)", 18.1519, 74.5775),
        ("Pune (Haveli)", 18.5204, 73.8567),
        ("Pune (Junnar)", 19.2064, 73.8763),
        ("Nashik (Niphad - Onion Hub)", 20.0768, 74.1089),
        ("Nashik (Yeola)", 20.0422, 74.4897),
        ("Nashik (Dindori)", 20.1989, 73.8322),
        ("Ahmednagar (Rahuri - MPKV)", 19.3942, 74.6514),
        ("Ahmednagar (Sangamner)", 19.5772, 74.2144),
        ("Ahmednagar (Kopargaon)", 19.8911, 74.4816),
        ("Jalgaon (Raver - Banana/Cotton)", 21.2464, 75.9272),
        ("Jalgaon (Bhusawal)", 21.0455, 75.7885),
        ("Jalgaon (Jamner)", 20.8142, 75.7801),
        ("Solapur (Pandharpur)", 17.6775, 75.3214),
        ("Solapur (Mohol)", 17.7011, 75.6481),
        ("Solapur (Barshi)", 18.2335, 76.0428),
        ("Chhatrapati Sambhaji Nagar (Paithan)", 19.4819, 75.3853),
        ("Chhatrapati Sambhaji Nagar (Gangapur)", 19.7001, 75.0069),
        ("Nagpur (Katol - Cotton)", 21.2654, 78.5878),
        ("Nagpur (Umred)", 20.8522, 79.3275),
        ("Amravati (Achalpur)", 21.2588, 77.5113),
        ("Wardha (Hinganghat - Cotton)", 20.5601, 78.8378),
        ("Yavatmal (Wani - Cotton Belt)", 20.0611, 78.9511),
        ("Kolhapur (Shirol)", 16.7381, 74.5936),
        ("Kolhapur (Karveer)", 16.6956, 74.2317),
        ("Satara (Karad)", 17.2885, 74.1844),
        ("Satara (Phaltan)", 17.9858, 74.4336),
        ("Sangli (Tasgaon)", 17.0344, 74.6019),
        ("Beed (Ambejogai)", 18.7303, 76.3861),
        ("Latur (Ausa)", 18.2519, 76.5056),
        ("Nanded (Loha)", 18.9489, 77.1172),
        ("Dhule (Shirpur)", 21.3533, 74.8814),
        ("Buldhana (Khamgaon)", 20.6869, 76.5683),
    ]

    sample_scenarios = [
        # (crop, disease, confidence_range, risk, base_temp, base_hum)
        ("tomato", "tomato_early_blight", (0.75, 0.94), "High", 26.5, 84.0),
        ("tomato", "tomato_late_blight", (0.80, 0.96), "High", 21.0, 92.0),
        ("tomato", "tomato_leaf_curl_virus", (0.72, 0.91), "Medium", 30.5, 62.0),
        ("tomato", "tomato_leaf_mold", (0.68, 0.88), "Medium", 24.0, 78.0),
        ("tomato", "tomato_healthy", (0.85, 0.98), "Low", 28.0, 55.0),
        ("cotton", "cotton_bacterial_blight", (0.78, 0.95), "High", 29.0, 81.0),
        ("cotton", "cotton_leaf_curl", (0.70, 0.92), "Medium", 33.0, 58.0),
        ("cotton", "cotton_bollworm", (0.81, 0.96), "Medium", 29.5, 66.0),
        ("onion", "onion_purple_blotch", (0.76, 0.94), "High", 25.0, 86.0),
        ("onion", "onion_downy_mildew", (0.82, 0.97), "High", 19.5, 91.0),
        ("onion", "onion_stemphylium_blight", (0.71, 0.89), "Medium", 27.0, 74.0),
        # Uncertain cases (< 0.60)
        ("tomato", "tomato_early_blight", (0.42, 0.58), "Medium", 25.0, 70.0),
        ("cotton", "cotton_bacterial_blight", (0.45, 0.59), "Low", 31.0, 50.0),
        ("onion", "onion_purple_blotch", (0.40, 0.57), "High", 23.5, 85.0),
    ]

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    inserted_count = 0
    now = datetime.now()

    random.seed(42)  # Deterministic realistic demo set

    for i, loc in enumerate(maharashtra_locations):
        loc_name, base_lat, base_lon = loc
        # slight jitter
        lat = base_lat + random.uniform(-0.02, 0.02)
        lon = base_lon + random.uniform(-0.02, 0.02)

        scenario = sample_scenarios[i % len(sample_scenarios)]
        crop, disease, conf_range, weather_risk, base_temp, base_hum = scenario

        conf = random.uniform(conf_range[0], conf_range[1])
        is_uncertain = conf < 0.60
        temp = base_temp + random.uniform(-2.5, 2.5)
        hum = base_hum + random.uniform(-5.0, 5.0)
        rain = round(random.choice([0.0, 0.0, 1.2, 5.4, 14.8, 22.0]), 1) if weather_risk == "High" else 0.0

        # Random timestamp over last 14 days
        hours_ago = random.randint(1, 14 * 24)
        ts = (now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M:%S")

        lang = random.choice(["mr", "mr", "en", "hi"])

        # Verification distribution
        r_val = random.random()
        if r_val < 0.45:
            expert_status = "Confirmed"
            expert_label = disease
            expert_notes = "Verified by Taluka Agriculture Officer; symptoms typical."
        elif r_val < 0.60:
            expert_status = "Corrected"
            # Switch to another related label
            if crop == "tomato":
                expert_label = "tomato_early_blight" if disease != "tomato_early_blight" else "tomato_leaf_mold"
            elif crop == "cotton":
                expert_label = "cotton_bacterial_blight" if disease != "cotton_bacterial_blight" else "cotton_leaf_curl"
            else:
                expert_label = "onion_purple_blotch" if disease != "onion_purple_blotch" else "onion_stemphylium_blight"
            expert_notes = "Field inspection showed characteristic target lesions."
        else:
            expert_status = "Pending"
            expert_label = None
            expert_notes = ""

        cursor.execute(
            """
            INSERT INTO reports (
                timestamp, crop, predicted_disease, confidence,
                latitude, longitude, location_name, language,
                is_uncertain, expert_status, expert_label, expert_notes,
                temperature, humidity, rainfall, weather_risk, image_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ts,
                crop,
                disease,
                round(conf, 4),
                round(lat, 4),
                round(lon, 4),
                loc_name,
                lang,
                1 if is_uncertain else 0,
                expert_status,
                expert_label,
                expert_notes,
                round(temp, 1),
                round(hum, 1),
                round(rain, 1),
                weather_risk,
                f"sample_{crop}_{i+1}.jpg",
            ),
        )
        inserted_count += 1

    conn.commit()
    conn.close()
    return inserted_count


def get_summary_stats(db_path: str = DB_PATH) -> dict:
    """Returns analytics summary dictionary for quick metrics widgets."""
    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    pending = cursor.execute("SELECT COUNT(*) FROM reports WHERE expert_status = 'Pending'").fetchone()[0]
    confirmed = cursor.execute("SELECT COUNT(*) FROM reports WHERE expert_status = 'Confirmed'").fetchone()[0]
    corrected = cursor.execute("SELECT COUNT(*) FROM reports WHERE expert_status = 'Corrected'").fetchone()[0]
    uncertain = cursor.execute("SELECT COUNT(*) FROM reports WHERE is_uncertain = 1").fetchone()[0]

    conn.close()
    return {
        "total_reports": total,
        "pending_verification": pending,
        "confirmed": confirmed,
        "corrected": corrected,
        "uncertain": uncertain,
    }


if __name__ == "__main__":
    init_db()
    count = load_demo_data()
    print(f"Database initialized and {count} demo records inserted.")
