import sqlite3
import os

DB_PATH = os.path.join("database", "vbcua.db")


# -------------------------------------------------
# CREATE DATABASE
# -------------------------------------------------

def create_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_name TEXT,

        topic TEXT,

        transcript TEXT,

        similarity REAL,

        level TEXT,

        duration REAL,

        rms REAL,

        fillers INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


# -------------------------------------------------
# INSERT REPORT
# -------------------------------------------------

def insert_report(
    student_name,
    topic,
    transcript,
    similarity,
    level,
    duration,
    rms,
    fillers
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports(

            student_name,

            topic,

            transcript,

            similarity,

            level,

            duration,

            rms,

            fillers

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            student_name,

            topic,

            transcript,

            similarity,

            level,

            duration,

            rms,

            fillers
        )

    )

    conn.commit()

    conn.close()

# -------------------------------------------------
# GET ALL REPORTS
# -------------------------------------------------

def get_reports():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            student_name,
            topic,
            transcript,
            similarity,
            level,
            duration,
            rms,
            fillers,
            created_at
        FROM reports
        ORDER BY id DESC
    """)

    reports = cursor.fetchall()

    conn.close()

    return reports


# -------------------------------------------------
# DASHBOARD STATISTICS
# -------------------------------------------------

def get_dashboard_stats():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            AVG(similarity),
            MAX(similarity),
            AVG(duration)
        FROM reports
    """)

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return (0, 0, 0, 0)

    total = result[0] or 0
    average = result[1] or 0
    best = result[2] or 0
    duration = result[3] or 0

    return {
        "total_reports": total,
        "average_similarity": average,
        "best_similarity": best,
        "average_duration": duration
    }


# -------------------------------------------------
# SIMILARITY HISTORY
# -------------------------------------------------

def get_similarity_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            similarity
        FROM reports
        ORDER BY id
    """)

    history = cursor.fetchall()

    conn.close()

    return history

# -------------------------------------------------
# DELETE ALL REPORTS
# -------------------------------------------------

def delete_all_reports():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM reports")

    conn.commit()

    conn.close()


# -------------------------------------------------
# TOP PERFORMING STUDENTS
# -------------------------------------------------

def get_top_students():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_name,
            MAX(similarity)
        FROM reports
        GROUP BY student_name
        ORDER BY MAX(similarity) DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# -------------------------------------------------
# TOPIC PERFORMANCE
# -------------------------------------------------

def get_topic_performance():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            topic,
            AVG(similarity)
        FROM reports
        GROUP BY topic
        ORDER BY AVG(similarity) DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data    