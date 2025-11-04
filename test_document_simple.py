#!/usr/bin/env python3
"""
Simple test for document bot using only upload_sessions table
"""

import sys
sys.path.append('.')

from data_collector import DataCollector

def test_document_simple():
    print("🔧 Testing Document Bot (upload_sessions only)...")
    print("=" * 50)
    
    try:
        collector = DataCollector()
        
        # Test document bot stats
        print("Testing Document Bot Statistics...")
        stats = collector.get_document_stats()
        print(f"✅ Today: {stats['today']} users")
        print(f"✅ Week: {stats['week']} users") 
        print(f"✅ Month: {stats['month']} users")
        
        # Test combined stats
        print("\nTesting Combined Statistics...")
        combined = collector.get_combined_stats()
        print(f"✅ Document Bot: {combined['document']['today']} users today")
        print(f"✅ Total: {combined['total']['today']} users today")
        
        print("\n🎉 Document Bot Test Completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_document_simple()
