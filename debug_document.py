#!/usr/bin/env python3
"""
Debug script for Document Bot connection issues
"""

import sys
import os
sys.path.append('.')

import psycopg
from datetime import date, timedelta

def test_document_connection():
    """Test document bot database connection and data"""
    print("🔍 Debugging Document Bot Connection...")
    print("=" * 50)
    
    # Test different database configurations
    configs = [
        {
            "name": "Config 1 (Port 5433, telegram_bot_db)",
            "host": "localhost",
            "port": 5433,
            "database": "telegram_bot_db",
            "user": "postgres",
            "password": "root"
        },
        {
            "name": "Config 2 (Port 5432, telegram_bot_db)",
            "host": "localhost", 
            "port": 5432,
            "database": "telegram_bot_db",
            "user": "postgres",
            "password": "root"
        }
    ]
    
    for config in configs:
        print(f"\n📡 Testing {config['name']}...")
        try:
            conn_str = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            conn = psycopg.connect(conn_str)
            print(f"✅ Connection successful!")
            
            with conn.cursor() as cur:
                # Check if history table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'history'
                    )
                """)
                history_exists = cur.fetchone()[0]
                print(f"📋 History table exists: {history_exists}")
                
                if history_exists:
                    # Count total records
                    cur.execute("SELECT COUNT(*) FROM history")
                    total_records = cur.fetchone()[0]
                    print(f"📊 Total history records: {total_records}")
                    
                    if total_records > 0:
                        # Check recent records
                        cur.execute("""
                            SELECT user_id, created_at 
                            FROM history 
                            ORDER BY created_at DESC 
                            LIMIT 5
                        """)
                        recent_records = cur.fetchall()
                        print("🕒 Recent records:")
                        for record in recent_records:
                            print(f"   User ID: {record[0]}, Date: {record[1]}")
                        
                        # Check today's records
                        today = date.today()
                        cur.execute("""
                            SELECT COUNT(DISTINCT user_id) 
                            FROM history 
                            WHERE DATE(created_at) = %s
                        """, (today,))
                        today_users = cur.fetchone()[0]
                        print(f"👥 Today's unique users: {today_users}")
                        
                        # Check this week's records
                        week_start = today - timedelta(days=today.weekday())
                        cur.execute("""
                            SELECT COUNT(DISTINCT user_id) 
                            FROM history 
                            WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                        """, (week_start, today))
                        week_users = cur.fetchone()[0]
                        print(f"📅 This week's unique users: {week_users}")
                        
                        # Check this month's records
                        month_start = today.replace(day=1)
                        cur.execute("""
                            SELECT COUNT(DISTINCT user_id) 
                            FROM history 
                            WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                        """, (month_start, today))
                        month_users = cur.fetchone()[0]
                        print(f"📆 This month's unique users: {month_users}")
                
                # Check users table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    )
                """)
                users_exists = cur.fetchone()[0]
                print(f"👤 Users table exists: {users_exists}")
                
                if users_exists:
                    cur.execute("SELECT COUNT(*) FROM users")
                    user_count = cur.fetchone()[0]
                    print(f"👥 Total users: {user_count}")
                    
                    if user_count > 0:
                        cur.execute("SELECT telegram_id, first_name FROM users LIMIT 5")
                        users = cur.fetchall()
                        print("👤 Sample users:")
                        for user in users:
                            print(f"   Telegram ID: {user[0]}, Name: {user[1]}")
            
            conn.close()
            print(f"✅ {config['name']} - SUCCESS!")
            
        except Exception as e:
            print(f"❌ {config['name']} - FAILED: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Debug complete!")

if __name__ == "__main__":
    test_document_connection()
