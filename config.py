"""
Configuration for the Monitoring Report Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("MONITORING_BOT_TOKEN", "7728001472:AAEaIDON0CPfO7x_D2BwZyBYlFkFlW89ZBQ")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "YOUR_ADMIN_CHAT_ID")

# Database Configurations for all three systems
DOCKFIY_DB_CONFIG = {
    "host": os.getenv("DOCKFIY_DB_HOST", "localhost"),
    "port": os.getenv("DOCKFIY_DB_PORT", "5433"),
    "database": os.getenv("DOCKFIY_DB_NAME", "telegram-document-bot"),
    "user": os.getenv("DOCKFIY_DB_USER", "postgres"),
    "password": os.getenv("DOCKFIY_DB_PASSWORD", "root"),
    "db_type": "postgresql"
}

TEL_BOT_DB_CONFIG = {
    "host": os.getenv("TEL_BOT_DB_HOST", "localhost"),
    "port": os.getenv("TEL_BOT_DB_PORT", "3306"),
    "database": os.getenv("TEL_BOT_DB_NAME", "task_manager"),
    "user": os.getenv("TEL_BOT_DB_USER", "root"),
    "password": os.getenv("TEL_BOT_DB_PASSWORD", "root"),
    "db_type": "mysql"
}

INVOICE_DB_CONFIG = {
    "host": os.getenv("INVOICE_DB_HOST", "localhost"),
    "port": os.getenv("INVOICE_DB_PORT", "3306"),
    "database": os.getenv("INVOICE_DB_NAME", "invoice_system_testing"),
    "user": os.getenv("INVOICE_DB_USER", "root"),
    "password": os.getenv("INVOICE_DB_PASSWORD", "root"),
    "db_type": "mysql"
}

TRAVEL_DB_CONFIG = {
    "host": os.getenv("TRAVEL_DB_HOST", "localhost"),
    "port": os.getenv("TRAVEL_DB_PORT", "3305"),
    "database": os.getenv("TRAVEL_DB_NAME", "u221987201_travel"),
    "user": os.getenv("TRAVEL_DB_USER", "root"),
    "password": os.getenv("TRAVEL_DB_PASSWORD", ""),
    "db_type": "mysql"
}

DOCUMENT_DB_CONFIG = {
    "host": os.getenv("DOCUMENT_DB_HOST", "localhost"),
    "port": os.getenv("DOCUMENT_DB_PORT", "5433"),
    "database": os.getenv("DOCUMENT_DB_NAME", "telegram_bot_db"),
    "user": os.getenv("DOCUMENT_DB_USER", "postgres"),
    "password": os.getenv("DOCUMENT_DB_PASSWORD", "root"),
    "db_type": "postgresql"
}

# System Names for Reports
SYSTEM_NAMES = {
    "dockify": os.getenv("DOCKFIY_BOT_NAME", "@DOCKFIY-PART 3"),
    "tel_bot": os.getenv("TEL_BOT_NAME", "@tel-bot-main"),
    "invoice": os.getenv("INVOICE_SYSTEM_NAME", "Invoice System (Managers/Admins)"),
    "travel": os.getenv("TRAVEL_SYSTEM_NAME", "Travel System (Vehicle Forms)"),
    "document": os.getenv("DOCUMENT_BOT_NAME", "Document Bot (File Uploads)")
}

# Report Configuration
REPORTS_DIR = "reports"
SCHEDULE_CONFIG = {
    "weekly_day": 0,  # Monday (0=Monday, 1=Tuesday, etc.)
    "weekly_time": "09:00",  # 9 AM
    "monthly_day": 1,  # 1st of the month
    "monthly_time": "09:00"  # 9 AM
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
