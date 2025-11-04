#!/usr/bin/env python3
"""
Startup script for Monitoring Report Bot
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_environment():
    """Check if environment is properly configured"""
    env_file = current_dir / ".env"
    
    if not env_file.exists():
        print("❌ Environment file not found!")
        print("Please copy 'env.example' to '.env' and configure your settings.")
        return False
    
    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "MONITORING_BOT_TOKEN",
        "ADMIN_CHAT_ID"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please configure these in your .env file.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def main():
    """Main startup function"""
    print("🤖 Starting Monitoring Report Bot...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Import and run bot
    try:
        from bot_simple import main as run_bot
        print("✅ Bot configuration loaded successfully")
        print("🚀 Starting bot...")
        run_bot()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
