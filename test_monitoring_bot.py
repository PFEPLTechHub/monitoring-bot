#!/usr/bin/env python3
"""
Test the monitoring bot's data collector directly
"""

import sys
sys.path.append('.')

from data_collector import DataCollector
import logging

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)

def test_monitoring_bot():
    print("🤖 Testing Monitoring Bot Data Collector...")
    print("=" * 50)
    
    try:
        collector = DataCollector()
        
        print("1. Testing document bot connection...")
        conn = collector.get_document_connection()
        if conn:
            print("✅ Document bot connection successful")
            conn.close()
        else:
            print("❌ Document bot connection failed")
            return
        
        print("\n2. Testing document bot stats...")
        stats = collector.get_document_stats()
        print(f"✅ Document bot stats: {stats}")
        
        print("\n3. Testing combined stats...")
        combined = collector.get_combined_stats()
        print(f"✅ Document bot in combined: {combined['document']}")
        print(f"✅ Total: {combined['total']}")
        
        print("\n🎉 Monitoring bot test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_monitoring_bot()
