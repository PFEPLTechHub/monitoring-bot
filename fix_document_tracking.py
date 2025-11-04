#!/usr/bin/env python3
"""
Comprehensive fix for document bot tracking
This script will check all possible data sources and provide a working solution
"""

import psycopg
from datetime import date, timedelta

def fix_document_tracking():
    print("🔧 Comprehensive Document Bot Tracking Fix")
    print("=" * 50)
    
    try:
        conn = psycopg.connect("postgresql://postgres:root@localhost:5433/telegram_bot_db")
        print("✅ Connected to document bot database")
        
        with conn.cursor() as cur:
            # Check all tables
            print("\n📊 Database Analysis:")
            
            # 1. Upload sessions
            cur.execute("SELECT COUNT(*) FROM upload_sessions")
            sessions_count = cur.fetchone()[0]
            print(f"📋 upload_sessions: {sessions_count} records")
            
            # 2. History
            cur.execute("SELECT COUNT(*) FROM history")
            history_count = cur.fetchone()[0]
            print(f"📋 history: {history_count} records")
            
            # 3. Files
            cur.execute("SELECT COUNT(*) FROM files")
            files_count = cur.fetchone()[0]
            print(f"📋 files: {files_count} records")
            
            # 4. Users
            cur.execute("SELECT COUNT(*) FROM users")
            users_count = cur.fetchone()[0]
            print(f"📋 users: {users_count} records")
            
            # Check which table has the most recent data
            print("\n🕒 Checking recent activity:")
            
            # Check upload_sessions for recent activity (without date filter)
            if sessions_count > 0:
                cur.execute("SELECT COUNT(DISTINCT user_id) FROM upload_sessions")
                unique_sessions_users = cur.fetchone()[0]
                print(f"👥 Unique users in upload_sessions: {unique_sessions_users}")
                
                # Show recent sessions
                cur.execute("SELECT id, user_id, status FROM upload_sessions ORDER BY id DESC LIMIT 3")
                recent_sessions = cur.fetchall()
                print("Recent upload_sessions:")
                for session in recent_sessions:
                    print(f"  ID: {session[0]}, User: {session[1]}, Status: {session[2]}")
            
            # Check history for recent activity
            if history_count > 0:
                cur.execute("SELECT COUNT(DISTINCT user_id) FROM history")
                unique_history_users = cur.fetchone()[0]
                print(f"👥 Unique users in history: {unique_history_users}")
                
                # Show recent history
                cur.execute("SELECT user_id, created_at FROM history ORDER BY created_at DESC LIMIT 3")
                recent_history = cur.fetchall()
                print("Recent history:")
                for record in recent_history:
                    print(f"  User: {record[0]}, Date: {record[1]}")
            
            # Check files for recent activity
            if files_count > 0:
                cur.execute("SELECT COUNT(DISTINCT session_id) FROM files")
                unique_file_sessions = cur.fetchone()[0]
                print(f"📁 Unique sessions in files: {unique_file_sessions}")
                
                # Show recent files
                cur.execute("SELECT session_id, original_name, created_at FROM files ORDER BY created_at DESC LIMIT 3")
                recent_files = cur.fetchall()
                print("Recent files:")
                for file_record in recent_files:
                    print(f"  Session: {file_record[0]}, Name: {file_record[1]}, Date: {file_record[2]}")
            
            # Determine the best tracking method
            print("\n🎯 Recommended Tracking Method:")
            
            if history_count > 0:
                print("✅ Use HISTORY table (has proper timestamps)")
                # Test today's query
                today = date.today()
                cur.execute("""
                    SELECT COUNT(DISTINCT user_id) 
                    FROM history 
                    WHERE DATE(created_at) = %s
                """, (today,))
                today_result = cur.fetchone()[0]
                print(f"📅 Today's unique users (history): {today_result}")
                
            elif sessions_count > 0:
                print("⚠️  HISTORY table is empty, but upload_sessions has data")
                print("💡 Solution: Use upload_sessions without date filtering")
                print("📝 Note: This will show total unique users, not daily/weekly/monthly")
                
            elif files_count > 0:
                print("⚠️  HISTORY and upload_sessions are empty, but files has data")
                print("💡 Solution: Use files table to track activity")
                
            else:
                print("❌ No data found in any table")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_document_tracking()
