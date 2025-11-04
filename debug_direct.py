#!/usr/bin/env python3
"""
Direct debug of document bot database connection
"""

import psycopg
from datetime import date

def debug_direct():
    print("🔍 Direct Database Debug...")
    print("=" * 40)
    
    # Test connection
    try:
        print("Testing connection to: postgresql://postgres:root@localhost:5433/telegram_bot_db")
        conn = psycopg.connect("postgresql://postgres:root@localhost:5433/telegram_bot_db")
        print("✅ Connection successful!")
        
        with conn.cursor() as cur:
            # Check upload_sessions table
            print("\n📋 Checking upload_sessions table...")
            cur.execute("SELECT COUNT(*) FROM upload_sessions")
            count = cur.fetchone()[0]
            print(f"Total records: {count}")
            
            if count > 0:
                # Check unique users
                cur.execute("SELECT COUNT(DISTINCT user_id) FROM upload_sessions")
                unique_users = cur.fetchone()[0]
                print(f"Unique users: {unique_users}")
                
                # Show sample data
                cur.execute("SELECT id, user_id, status FROM upload_sessions LIMIT 5")
                samples = cur.fetchall()
                print("Sample records:")
                for sample in samples:
                    print(f"  ID: {sample[0]}, User: {sample[1]}, Status: {sample[2]}")
                
                # Test the exact query our monitoring bot uses
                print("\n🧪 Testing monitoring bot query...")
                cur.execute("SELECT COUNT(DISTINCT user_id) FROM upload_sessions")
                result = cur.fetchone()
                total_users = result[0] if result else 0
                print(f"Query result: {total_users} unique users")
                
            else:
                print("❌ No records found in upload_sessions table")
        
        conn.close()
        print("\n✅ Debug completed successfully!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_direct()
