"""
Database connection and initialization module for Urwat il Wusqa Travels DMS.
Supports MySQL (PyMySQL) with automatic database creation and SQLite fallback.
Single-Role Architecture: Admin Only (adminuser / ZAFAR@786).
"""
import os
import ssl
import pymysql
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

DB_HOST = Config.MYSQL_HOST
DB_PORT = Config.MYSQL_PORT
DB_USER = Config.MYSQL_USER
DB_PASS = Config.MYSQL_PASSWORD
DB_NAME = Config.MYSQL_DB

USE_MYSQL = True
ACTIVE_ENGINE = 'mysql'

def get_ssl_context():
    """Returns an SSL configuration required for TiDB Cloud Serverless and remote TLS MySQL connections."""
    ca_path = getattr(Config, 'MYSQL_SSL_CA', None)
    if 'tidbcloud.com' in DB_HOST or DB_PORT == 4000 or getattr(Config, 'MYSQL_SSL', False):
        try:
            if ca_path and os.path.exists(ca_path):
                # Official ISRG Root X1 CA Certificate for TiDB Cloud
                return {'ca': ca_path}
            else:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                return ctx
        except Exception:
            return None
    return None

def get_connection():
    global USE_MYSQL, ACTIVE_ENGINE
    if USE_MYSQL and DB_PASS != '<PASSWORD>':
        ssl_ctx = get_ssl_context()
        conn_params = {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER,
            'password': DB_PASS,
            'database': DB_NAME,
            'cursorclass': pymysql.cursors.DictCursor,
            'autocommit': True,
            'connect_timeout': 8
        }
        if ssl_ctx:
            conn_params['ssl'] = ssl_ctx

        try:
            conn = pymysql.connect(**conn_params)
            ACTIVE_ENGINE = 'mysql'
            return conn, 'mysql'
        except Exception:
            try:
                temp_params = {
                    'host': DB_HOST,
                    'port': DB_PORT,
                    'user': DB_USER,
                    'password': DB_PASS,
                    'autocommit': True,
                    'connect_timeout': 8
                }
                if ssl_ctx:
                    temp_params['ssl'] = ssl_ctx
                temp_conn = pymysql.connect(**temp_params)
                with temp_conn.cursor() as cur:
                    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                temp_conn.close()

                conn = pymysql.connect(**conn_params)
                ACTIVE_ENGINE = 'mysql'
                return conn, 'mysql'
            except Exception:
                USE_MYSQL = False
    elif DB_PASS == '<PASSWORD>':
        # TiDB configured but password placeholder has not been replaced yet
        pass

    # Fallback to local SQLite if MySQL server is not currently reachable
    ACTIVE_ENGINE = 'sqlite'
    sqlite_path = os.path.join(os.path.dirname(__file__), 'utw_dms.db')
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'
    return conn, 'sqlite'

def get_active_engine():
    global ACTIVE_ENGINE
    return ACTIVE_ENGINE

def query_all(query, params=()):
    conn, engine = get_connection()
    try:
        if engine == 'mysql':
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        else:
            cur = conn.cursor()
            sqlite_q = query.replace('%s', '?')
            cur.execute(sqlite_q, params)
            rows = cur.fetchall()
            return [dict(ix) for ix in rows]
    finally:
        conn.close()

def query_one(query, params=()):
    conn, engine = get_connection()
    try:
        if engine == 'mysql':
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()
        else:
            cur = conn.cursor()
            sqlite_q = query.replace('%s', '?')
            cur.execute(sqlite_q, params)
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()

def execute_stmt(query, params=()):
    conn, engine = get_connection()
    try:
        if engine == 'mysql':
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.lastrowid
        else:
            cur = conn.cursor()
            sqlite_q = query.replace('%s', '?')
            cur.execute(sqlite_q, params)
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()

def init_db():
    conn, engine = get_connection()
    try:
        if engine == 'mysql':
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'admin',
                phone VARCHAR(30),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pilgrim_groups (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) UNIQUE NOT NULL,
                group_name VARCHAR(100) NOT NULL,
                leader_name VARCHAR(100),
                leader_phone VARCHAR(30),
                total_pax INT DEFAULT 0,
                arrival_date DATE,
                departure_date DATE,
                status VARCHAR(30) DEFAULT 'Active'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # Riaz Ul Jannah Permits (Exact schema requested by user)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS riaz_permits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) NOT NULL DEFAULT 'GENERAL',
                passport_number VARCHAR(50) NOT NULL,
                visa_number VARCHAR(50) NOT NULL,
                pilgrim_whatsapp VARCHAR(30),
                permit_date DATE NOT NULL,
                slot_time VARCHAR(50) NOT NULL,
                status ENUM('Upcoming', 'Completed', 'Missed') NOT NULL DEFAULT 'Upcoming',
                permit_type ENUM('Own Permit', 'Managed on Wheel Chair', 'Managed by Cash') NOT NULL DEFAULT 'Own Permit',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX (group_code),
                INDEX (passport_number),
                INDEX (permit_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS zyarat_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) NOT NULL,
                city ENUM('Makkah', 'Madinah') NOT NULL,
                zyarat_date DATE NOT NULL,
                departure_time VARCHAR(20),
                destination VARCHAR(150) NOT NULL,
                bus_number VARCHAR(50),
                driver_name VARCHAR(100),
                driver_phone VARCHAR(30),
                guide_murshid VARCHAR(100) NOT NULL,
                booked_pax INT NOT NULL,
                actual_pax INT NOT NULL,
                status ENUM('Scheduled', 'Boarding', 'In Transit', 'Completed') NOT NULL DEFAULT 'Scheduled',
                notes TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS flight_tracker (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) NOT NULL,
                flight_number VARCHAR(30) NOT NULL,
                airline VARCHAR(50),
                route_type VARCHAR(50) NOT NULL DEFAULT 'Outbound',
                airport VARCHAR(50) NOT NULL,
                origin_city VARCHAR(100) DEFAULT 'Pakistan',
                departure_time VARCHAR(30),
                destination_city VARCHAR(100) DEFAULT 'Saudi Arabia',
                arrival_time VARCHAR(30),
                flight_date DATE,
                flight_time VARCHAR(30),
                pax_count INT NOT NULL,
                transport_assigned VARCHAR(100),
                status VARCHAR(50) DEFAULT 'On Time',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # Ensure all flight columns exist if table was created previously
            try:
                cursor.execute("SHOW COLUMNS FROM flight_tracker")
                mysql_flight_cols = [c.get('Field') if isinstance(c, dict) else c[0] for c in cursor.fetchall()]
                missing_flight_cols = [
                    ('origin_city', 'VARCHAR(100) DEFAULT NULL'),
                    ('departure_time', 'VARCHAR(30) DEFAULT NULL'),
                    ('destination_city', 'VARCHAR(100) DEFAULT NULL'),
                    ('arrival_time', 'VARCHAR(30) DEFAULT NULL'),
                    ('flight_date', 'DATE DEFAULT NULL'),
                    ('airline', 'VARCHAR(50) DEFAULT NULL')
                ]
                for col_name, col_type in missing_flight_cols:
                    if col_name not in mysql_flight_cols:
                        cursor.execute(f"ALTER TABLE flight_tracker ADD COLUMN {col_name} {col_type};")
            except Exception as e:
                print(f"[DB Warning] Could not check or alter MySQL flight_tracker columns: {e}")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hotel_transfers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) NOT NULL,
                city ENUM('Makkah', 'Madinah') NOT NULL,
                hotel_name VARCHAR(100) NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                rooms_allocated INT NOT NULL,
                voucher_status ENUM('Confirmed', 'Pending') DEFAULT 'Confirmed',
                assigned_coordinator VARCHAR(100)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS operational_incidents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50),
                severity ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
                category VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                reported_by VARCHAR(100) NOT NULL,
                status ENUM('Open', 'In Progress', 'Resolved') DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pilgrims (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_code VARCHAR(50) NOT NULL,
                name VARCHAR(150) NOT NULL,
                reference_by VARCHAR(150),
                passport_number VARCHAR(50),
                contact VARCHAR(50),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX (group_code),
                INDEX (passport_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            cursor.close()

        else:
            # SQLite setup
            cursor = conn.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'admin',
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS pilgrim_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT UNIQUE NOT NULL,
                group_name TEXT NOT NULL,
                leader_name TEXT,
                leader_phone TEXT,
                total_pax INTEGER DEFAULT 0,
                arrival_date DATE,
                departure_date DATE,
                status TEXT DEFAULT 'Active'
            );

            CREATE TABLE IF NOT EXISTS riaz_permits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT NOT NULL DEFAULT 'GENERAL',
                passport_number TEXT NOT NULL,
                visa_number TEXT NOT NULL,
                pilgrim_whatsapp TEXT,
                permit_date DATE NOT NULL,
                slot_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Upcoming',
                permit_type TEXT NOT NULL DEFAULT 'Own Permit',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS zyarat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT NOT NULL,
                city TEXT NOT NULL,
                zyarat_date DATE NOT NULL,
                departure_time TEXT,
                destination TEXT NOT NULL,
                bus_number TEXT,
                driver_name TEXT,
                driver_phone TEXT,
                guide_murshid TEXT NOT NULL,
                booked_pax INTEGER NOT NULL,
                actual_pax INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS flight_tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                airline TEXT,
                route_type TEXT NOT NULL DEFAULT 'Outbound',
                airport TEXT NOT NULL,
                origin_city TEXT DEFAULT 'Pakistan',
                departure_time TEXT,
                destination_city TEXT DEFAULT 'Saudi Arabia',
                arrival_time TEXT,
                flight_date DATE,
                flight_time TEXT,
                pax_count INTEGER NOT NULL,
                transport_assigned TEXT,
                status TEXT DEFAULT 'On Time',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS hotel_transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT NOT NULL,
                city TEXT NOT NULL,
                hotel_name TEXT NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                rooms_allocated INTEGER NOT NULL,
                voucher_status TEXT DEFAULT 'Confirmed',
                assigned_coordinator TEXT
            );

            CREATE TABLE IF NOT EXISTS operational_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                reported_by TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS pilgrims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_code TEXT NOT NULL,
                name TEXT NOT NULL,
                reference_by TEXT,
                passport_number TEXT,
                contact TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

        # Ensure Single Admin User Always Exists: adminuser / ZAFAR@786
        admin_check = query_one("SELECT * FROM users WHERE username = %s", ('adminuser',))
        if not admin_check:
            admin_pass_hash = generate_password_hash('ZAFAR@786')
            execute_stmt(
                "INSERT INTO users (username, password_hash, full_name, role, phone) VALUES (%s, %s, %s, %s, %s)",
                ('adminuser', admin_pass_hash, 'Zafar Iqbal (Admin)', 'admin', '+92 300 1234567')
            )

    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Database schema verified (Single-Admin Architecture + Updated Permit Schema).")
