#!/usr/bin/env python3
"""
Simple test to check document bot database connection and data
"""

import psycopg
from datetime import date, timedelta

def test_document_db():
    """Test document bot database"""
    print("🔍 Testing Document Bot Database Connection...")
    
    # Try different database configurations
    configs = [
        ("telegram_bot_db", "Document bot's configured database"),
        ("telegram-document-bot", "DOCKFIY's database (might be shared)")
    ]
    
    for db_name, description in configs:
        print(f"\n📡 Testing {db_name} ({description})...")
        try:
            conn = psycopg.connect(f"postgresql://postgres:root@localhost:5433/{db_name}")
            print(f"✅ Connected to {db_name}")
            
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
                    # Count records
                    cur.execute("SELECT COUNT(*) FROM history")
                    count = cur.fetchone()[0]
                    print(f"📊 Total history records: {count}")
                    
                    if count > 0:
                        # Check today's records
                        today = date.today()
                        cur.execute("""
                            SELECT COUNT(DISTINCT user_id) 
                            FROM history 
                            WHERE DATE(created_at) = %s
                        """, (today,))
                        today_users = cur.fetchone()[0]
                        print(f"👥 Today's unique users: {today_users}")
                        
                        # Get most recent record
                        cur.execute("""
                            SELECT user_id, created_at, file_id 
                            FROM history 
                            ORDER BY created_at DESC 
                            LIMIT 1
                        """)
                        latest = cur.fetchone()
                        print(f"🕒 Most recent: User {latest[0]} at {latest[1]}")
                        
                        return True  # Found data, this is the right database
                
                # Check upload_sessions table
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'upload_sessions'
                    )
                """)
                sessions_exists = cur.fetchone()[0]
                print(f"📋 Upload_sessions table exists: {sessions_exists}")
                
                if sessions_exists:
                    cur.execute("SELECT COUNT(*) FROM upload_sessions")
                    session_count = cur.fetchone()[0]
                    print(f"📊 Total session records: {session_count}")
                    
                    if session_count > 0:
                        # Check today's sessions
                        today = date.today()
                        cur.execute("""
                            SELECT COUNT(DISTINCT user_id) 
                            FROM upload_sessions 
                            WHERE DATE(created_at) = %s
                        """, (today,))
                        today_sessions = cur.fetchone()[0]
                        print(f"👥 Today's unique users (sessions): {today_sessions}")
                        
                        if today_sessions > 0:
                            return True  # Found data in sessions table
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Failed to connect to {db_name}: {e}")
    
    return False

if __name__ == "__main__":
    success = test_document_db()
    if success:
        print("\n✅ Found document bot data!")
    else:
        print("\n❌ No document bot data found in any database")
