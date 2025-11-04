#!/usr/bin/env python3
"""
Test the document bot fix
"""

import sys
sys.path.append('.')

from data_collector import DataCollector

def test_document_fix():
    print("🔧 Testing Document Bot Fix...")
    print("=" * 40)
    
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
        
        # Test trends
        print("\nTesting Daily Trends...")
        trends = collector.get_daily_trends(7)
        print(f"✅ Document trend points: {len(trends['document'])}")
        
        print("\n🎉 Document Bot Fix Test Completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_document_fix()
