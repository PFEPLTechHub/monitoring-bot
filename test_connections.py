#!/usr/bin/env python3
"""
Test script to verify database connections and data collection
"""
import sys
from pathlib import Path
from datetime import date

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_data_collection():
    """Test data collection from both bots"""
    print("Testing data collection...")
    
    try:
        from data_collector import DataCollector
        
        collector = DataCollector()
        
        # Test individual bot stats
        print("\nDOCKFIY Bot Statistics:")
        dockify_stats = collector.get_dockify_stats()
        print(f"  Today: {dockify_stats['today']} users")
        print(f"  This Week: {dockify_stats['week']} users")
        print(f"  This Month: {dockify_stats['month']} users")
        
        print("\nTel-Bot Statistics:")
        tel_bot_stats = collector.get_tel_bot_stats()
        print(f"  Today: {tel_bot_stats['today']} users")
        print(f"  This Week: {tel_bot_stats['week']} users")
        print(f"  This Month: {tel_bot_stats['month']} users")
        
        print("\nInvoice System Statistics:")
        invoice_stats = collector.get_invoice_stats()
        print(f"  Today: {invoice_stats['today']} users")
        print(f"  This Week: {invoice_stats['week']} users")
        print(f"  This Month: {invoice_stats['month']} users")
        
        print("\nTravel System Statistics:")
        travel_stats = collector.get_travel_stats()
        print(f"  Today: {travel_stats['today']} users")
        print(f"  This Week: {travel_stats['week']} users")
        print(f"  This Month: {travel_stats['month']} users")
        
        print("\nDocument Bot Statistics:")
        document_stats = collector.get_document_stats()
        print(f"  Today: {document_stats['today']} users")
        print(f"  This Week: {document_stats['week']} users")
        print(f"  This Month: {document_stats['month']} users")
        
        print("\nCombined Statistics:")
        combined_stats = collector.get_combined_stats()
        print(f"  Total Today: {combined_stats['total']['today']} users")
        print(f"  Total This Week: {combined_stats['total']['week']} users")
        print(f"  Total This Month: {combined_stats['total']['month']} users")
        
        # Test trends
        print("\nTesting daily trends...")
        trends = collector.get_daily_trends(7)  # Last 7 days
        print(f"  DOCKFIY trend points: {len(trends['dockify'])}")
        print(f"  Tel-Bot trend points: {len(trends['tel_bot'])}")
        print(f"  Invoice trend points: {len(trends['invoice'])}")
        print(f"  Travel trend points: {len(trends['travel'])}")
        print(f"  Document trend points: {len(trends['document'])}")
        
        return True
        
    except Exception as e:
        print(f"Error testing data collection: {e}")
        return False

def test_report_generation():
    """Test report generation"""
    print("\nTesting report generation...")
    
    try:
        from report_generator import generate_consolidated_report
        
        # Generate test report
        report_path = generate_consolidated_report("test")
        
        if Path(report_path).exists():
            print(f"Test report generated: {report_path}")
            print(f"  File size: {Path(report_path).stat().st_size} bytes")
            
            # Clean up test file
            Path(report_path).unlink()
            print("Test file cleaned up")
            return True
        else:
            print("Report file was not created")
            return False
            
    except Exception as e:
        print(f"Error testing report generation: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    
    try:
        from config import BOT_TOKEN, ADMIN_CHAT_ID, SYSTEM_NAMES
        
        print(f"  Bot Token: {'Set' if BOT_TOKEN != 'YOUR_MONITORING_BOT_TOKEN' else 'Not configured'}")
        print(f"  Admin Chat ID: {'Set' if ADMIN_CHAT_ID != 'YOUR_ADMIN_CHAT_ID' else 'Not configured'}")
        print(f"  DOCKFIY Bot Name: {SYSTEM_NAMES['dockify']}")
        print(f"  Tel-Bot Name: {SYSTEM_NAMES['tel_bot']}")
        print(f"  Invoice System Name: {SYSTEM_NAMES['invoice']}")
        print(f"  Travel System Name: {SYSTEM_NAMES['travel']}")
        print(f"  Document Bot Name: {SYSTEM_NAMES['document']}")
        
        return True
        
    except Exception as e:
        print(f"Error testing configuration: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Monitoring Report Bot Setup...")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Data Collection", test_data_collection),
        ("Report Generation", test_report_generation)
    ]
    
    success_count = 0
    for test_name, test_func in tests:
        print(f"\n{test_name} Test")
        print("-" * 30)
        if test_func():
            success_count += 1
        else:
            print(f"FAILED: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {success_count}/{len(tests)} tests passed")
    
    if success_count == len(tests):
        print("All tests passed! Bot is ready to run.")
    else:
        print("Some tests failed. Please check your configuration.")
    
    return success_count == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
