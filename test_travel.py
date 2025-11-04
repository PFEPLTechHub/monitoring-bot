#!/usr/bin/env python3
"""
Simple test script for Travel system integration
"""

import sys
import os
sys.path.append('.')

from data_collector import DataCollector
from config import SYSTEM_NAMES

def test_travel_system():
    """Test Travel system integration"""
    print("Testing Travel System Integration...")
    print("=" * 40)
    
    try:
        collector = DataCollector()
        
        # Test Travel system stats
        print("\nTravel System Statistics:")
        travel_stats = collector.get_travel_stats()
        print(f"  Today: {travel_stats['today']} users")
        print(f"  This Week: {travel_stats['week']} users")
        print(f"  This Month: {travel_stats['month']} users")
        
        # Test combined stats
        print("\nCombined Statistics (All 4 Systems):")
        combined_stats = collector.get_combined_stats()
        print(f"  Total Today: {combined_stats['total']['today']} users")
        print(f"  Total This Week: {combined_stats['total']['week']} users")
        print(f"  Total This Month: {combined_stats['total']['month']} users")
        
        # Test trends
        print("\nTesting Travel System Trends:")
        trends = collector.get_daily_trends(7)
        print(f"  Travel trend points: {len(trends['travel'])}")
        
        print("\nSystem Names:")
        print(f"  Travel: {SYSTEM_NAMES['travel']}")
        
        print("\nTravel System Integration: SUCCESS!")
        return True
        
    except Exception as e:
        print(f"\nError testing Travel system: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_travel_system()
