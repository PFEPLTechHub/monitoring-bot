#!/usr/bin/env python3
"""
Comprehensive debug script for Document Bot
"""

import sys
import os
sys.path.append('.')

import psycopg
from datetime import date, timedelta

def debug_document_bot():
    """Comprehensive debug of document bot database"""
    print("🔍 Comprehensive Document Bot Debug...")
    print("=" * 60)
    
    # Try the corrected configuration
    try:
        conn_str = "postgresql://postgres:root@localhost:5433/telegram_bot_db"
        conn = psycopg.connect(conn_str)
        print("✅ Connected to document bot database")
        
        with conn.cursor() as cur:
            # List all tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cur.fetchall()
            print(f"\n📋 Available tables: {[t[0] for t in tables]}")
            
            # Check each table
            for table_name in ['users', 'upload_sessions', 'files', 'history']:
                print(f"\n🔍 Checking table: {table_name}")
                
                cur.execute(f"""
                    SELECT COUNT(*) FROM {table_name}
                """)
                count = cur.fetchone()[0]
                print(f"   Total records: {count}")
                
                if count > 0:
                    # Get recent records
                    if table_name == 'users':
                        cur.execute(f"""
                            SELECT telegram_id, first_name, created_at 
                            FROM {table_name} 
                            ORDER BY created_at DESC 
                            LIMIT 3
                        """)
                    elif table_name == 'upload_sessions':
                        cur.execute(f"""
                            SELECT session_id, user_id, status, created_at 
                            FROM {table_name} 
                            ORDER BY created_at DESC 
                            LIMIT 3
                        """)
                    elif table_name == 'files':
                        cur.execute(f"""
                            SELECT id, session_id, original_name, created_at 
                            FROM {table_name} 
                            ORDER BY created_at DESC 
                            LIMIT 3
                        """)
                    elif table_name == 'history':
                        cur.execute(f"""
                            SELECT user_id, file_id, session_id, created_at 
                            FROM {table_name} 
                            ORDER BY created_at DESC 
                            LIMIT 3
                        """)
                    
                    recent_records = cur.fetchall()
                    print("   Recent records:")
                    for record in recent_records:
                        print(f"     {record}")
            
            # Test our monitoring query logic
            print(f"\n🧪 Testing monitoring query logic...")
            today = date.today()
            
            # Test 1: History table with today's users
            cur.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM history
                WHERE DATE(created_at) = %s
            """, (today,))
            result = cur.fetchone()
            today_history = result[0] if result else 0
            print(f"   Today's unique users (history table): {today_history}")
            
            # Test 2: Upload sessions with today's users
            cur.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM upload_sessions
                WHERE DATE(created_at) = %s
            """, (today,))
            result = cur.fetchone()
            today_sessions = result[0] if result else 0
            print(f"   Today's unique users (upload_sessions): {today_sessions}")
            
            # Test 3: Files table with today's activity
            cur.execute("""
                SELECT COUNT(DISTINCT session_id) as count
                FROM files
                WHERE DATE(created_at) = %s
            """, (today,))
            result = cur.fetchone()
            today_files = result[0] if result else 0
            print(f"   Today's unique sessions (files table): {today_files}")
            
            # Test 4: Check last 7 days
            week_start = today - timedelta(days=7)
            cur.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM history
                WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
            """, (week_start, today))
            result = cur.fetchone()
            week_history = result[0] if result else 0
            print(f"   Last 7 days unique users (history): {week_history}")
            
            # Test 5: Check if there are any records at all
            cur.execute("SELECT COUNT(*) FROM history WHERE created_at >= NOW() - INTERVAL '30 days'")
            recent_count = cur.fetchone()[0]
            print(f"   Records in last 30 days: {recent_count}")
            
            if recent_count > 0:
                # Get the most recent record
                cur.execute("""
                    SELECT user_id, created_at, file_id, session_id
                    FROM history
                    ORDER BY created_at DESC
                    LIMIT 1
                """)
                latest = cur.fetchone()
                print(f"   Most recent record: User {latest[0]} at {latest[1]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_document_bot()
