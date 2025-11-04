#!/usr/bin/env python3
"""
Diagnose document bot database to find why it's showing 0 users
"""

import psycopg
from datetime import date, timedelta

def diagnose_document_db():
    print("🔍 Diagnosing Document Bot Database...")
    print("=" * 50)
    
    try:
        conn = psycopg.connect("postgresql://postgres:root@localhost:5433/telegram_bot_db")
        print("✅ Connected to document bot database")
        
        with conn.cursor() as cur:
            # Check upload_sessions table
            print("\n📋 Checking upload_sessions table...")
            cur.execute("SELECT COUNT(*) FROM upload_sessions")
            sessions_count = cur.fetchone()[0]
            print(f"Total upload_sessions records: {sessions_count}")
            
            if sessions_count > 0:
                # Check if created_at column exists
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'upload_sessions' AND column_name = 'created_at'
                """)
                has_created_at = cur.fetchone() is not None
                print(f"Has created_at column: {has_created_at}")
                
                # Show recent records
                cur.execute("SELECT id, user_id, status FROM upload_sessions ORDER BY id DESC LIMIT 5")
                recent_sessions = cur.fetchall()
                print("Recent upload_sessions:")
                for session in recent_sessions:
                    print(f"  ID: {session[0]}, User: {session[1]}, Status: {session[2]}")
            
            # Check history table
            print("\n📋 Checking history table...")
            cur.execute("SELECT COUNT(*) FROM history")
            history_count = cur.fetchone()[0]
            print(f"Total history records: {history_count}")
            
            if history_count > 0:
                # Show recent records with dates
                cur.execute("""
                    SELECT user_id, created_at, file_id, session_id 
                    FROM history 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """)
                recent_history = cur.fetchall()
                print("Recent history records:")
                for record in recent_history:
                    print(f"  User: {record[0]}, Date: {record[1]}, File: {record[2]}, Session: {record[3]}")
                
                # Check today's records
                today = date.today()
                cur.execute("""
                    SELECT COUNT(DISTINCT user_id) 
                    FROM history 
                    WHERE DATE(created_at) = %s
                """, (today,))
                today_users = cur.fetchone()[0]
                print(f"\nToday's unique users (history): {today_users}")
                
                # Check this week's records
                week_start = today - timedelta(days=today.weekday())
                cur.execute("""
                    SELECT COUNT(DISTINCT user_id) 
                    FROM history 
                    WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                """, (week_start, today))
                week_users = cur.fetchone()[0]
                print(f"This week's unique users (history): {week_users}")
                
                # Check this month's records
                month_start = today.replace(day=1)
                cur.execute("""
                    SELECT COUNT(DISTINCT user_id) 
                    FROM history 
                    WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                """, (month_start, today))
                month_users = cur.fetchone()[0]
                print(f"This month's unique users (history): {month_users}")
                
                # Check date range of all records
                cur.execute("""
                    SELECT MIN(created_at) as earliest, MAX(created_at) as latest
                    FROM history
                """)
                date_range = cur.fetchone()
                print(f"History date range: {date_range[0]} to {date_range[1]}")
            
            # Check files table
            print("\n📋 Checking files table...")
            cur.execute("SELECT COUNT(*) FROM files")
            files_count = cur.fetchone()[0]
            print(f"Total files records: {files_count}")
            
            if files_count > 0:
                cur.execute("""
                    SELECT id, session_id, original_name, created_at 
                    FROM files 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """)
                recent_files = cur.fetchall()
                print("Recent files:")
                for file_record in recent_files:
                    print(f"  ID: {file_record[0]}, Session: {file_record[1]}, Name: {file_record[2]}, Date: {file_record[3]}")
            
            # Check users table
            print("\n📋 Checking users table...")
            cur.execute("SELECT COUNT(*) FROM users")
            users_count = cur.fetchone()[0]
            print(f"Total users: {users_count}")
            
            if users_count > 0:
                cur.execute("SELECT telegram_id, first_name FROM users LIMIT 5")
                sample_users = cur.fetchall()
                print("Sample users:")
                for user in sample_users:
                    print(f"  Telegram ID: {user[0]}, Name: {user[1]}")
        
        conn.close()
        print("\n🏁 Diagnosis complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_document_db()
