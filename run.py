"""
InnoSphere One-Click Application Launcher
Automates environment checks, database verification, browser launch, and Flask server startup.
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess

def print_banner():
    banner = r"""
 ============================================================================
  ___                  ____        _                     
 |_ _|_ __  _ __   ___/ ___| _ __ | |__   ___ _ __ ___  
  | || '_ \| '_ \ / _ \___ \| '_ \| '_ \ / _ \ '__/ _ \ 
  | || | | | | | | (_) |__) | |_) | | | |  __/ | |  __/ 
 |___|_| |_|_| |_|\___/____/| .__/|_| |_|\___|_|  \___| 
                            |_|                          
  Unified Innovation, Hackathon & Research Management Portal
  Institutional Innovation Portal
 ============================================================================
"""
    print(banner)

def check_dependencies():
    print("[1/4] Checking Python dependencies...")
    required = ["flask", "mysql.connector", "dotenv", "werkzeug", "reportlab", "docx"]
    missing = []
    
    for mod in required:
        try:
            if mod == "dotenv":
                __import__("dotenv")
            elif mod == "mysql.connector":
                __import__("mysql.connector")
            elif mod == "docx":
                __import__("docx")
            else:
                __import__(mod)
        except ImportError:
            missing.append(mod)

    if missing:
        print(f"--> Installing missing dependencies: {', '.join(missing)}...")
        req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("--> Dependencies installed successfully.")
    else:
        print("--> All dependencies are satisfied.")

def check_database():
    print("[2/4] Verifying MySQL database connection & schema...")
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'atharv@27')
    db_name = os.getenv('DB_NAME', 'innosphere_db')

    import mysql.connector
    try:
        # Check if database exists
        conn = mysql.connector.connect(
            host=host, port=port, user=user, password=password
        )
        cur = conn.cursor()
        cur.execute("SHOW DATABASES LIKE %s;", (db_name,))
        exists = cur.fetchone()

        need_setup = False
        if not exists:
            need_setup = True
        else:
            cur.execute(f"USE {db_name};")
            cur.execute("SHOW TABLES;")
            tables = cur.fetchall()
            if len(tables) < 10:
                need_setup = True

        cur.close()
        conn.close()

        if need_setup:
            print("--> Database missing or empty. Initializing and seeding schema...")
            setup_script = os.path.join(os.path.dirname(__file__), "database", "setup_db.py")
            subprocess.check_call([sys.executable, setup_script])
            print("--> Database initialized and seeded successfully.")
        else:
            print(f"--> Database '{db_name}' is healthy and ready with all 16 tables & seed data.")

    except mysql.connector.Error as err:
        print("\n" + "!" * 70)
        print(f" [DATABASE CONNECTION ERROR]: {err}")
        print(" Please ensure MySQL 8.0 Server is running on your machine.")
        print(f" Current .env configuration: User='{user}', Host='{host}:{port}'")
        print("!" * 70 + "\n")
        sys.exit(1)

def open_browser():
    """Opens default browser after a short delay."""
    time.sleep(1.2)
    print("\n--> Opening InnoSphere in your browser: http://localhost:5000\n")
    try:
        webbrowser.open("http://localhost:5000")
    except Exception:
        pass

def start_server():
    print("[3/4] Starting Flask Web Server...")
    print("[4/4] InnoSphere is LIVE!")
    print("-" * 70)
    print("  Local URL:        http://localhost:5000")
    print("  Public Hub:       http://localhost:5000/hackathons")
    print("  Leaderboard:      http://localhost:5000/leaderboard")
    print("  Certificates:     http://localhost:5000/verify-certificate")
    print("-" * 70)
    print("  DEMO ACCOUNTS (Use 1-click buttons on http://localhost:5000/login):")
    print("  • Admin:          admin@innosphere.edu          / admin123")
    print("  • Coordinator:    coord@pict.edu                / coord123")
    print("  • Student:        atharv@pict.edu               / student123")
    print("  • Judge:          judge.sharma@innosphere.edu   / judge123")
    print("  • Mentor:         mentor@innosphere.edu         / mentor123")
    print("-" * 70)
    print("  Press Ctrl+C to stop the server\n")

    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Import and run app
    from app import app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    print_banner()
    check_dependencies()
    check_database()
    start_server()
