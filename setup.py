#!/usr/bin/env python3
"""
Setup script for Monitoring Report Bot
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_environment():
    """Setup environment file"""
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    # Copy env.example to .env
    try:
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from env.example")
        print("⚠️  Please edit .env file with your configuration")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def create_reports_directory():
    """Create reports directory"""
    reports_dir = Path("reports")
    try:
        reports_dir.mkdir(exist_ok=True)
        print("✅ Reports directory created")
        return True
    except Exception as e:
        print(f"❌ Error creating reports directory: {e}")
        return False

def check_database_connections():
    """Check database connections"""
    print("🔄 Checking database connections...")
    
    try:
        from data_collector import DataCollector
        collector = DataCollector()
        
        # Test DOCKFIY connection
        dockify_conn = collector.get_dockify_connection()
        if dockify_conn:
            print("✅ DOCKFIY database connection successful")
            dockify_conn.close()
        else:
            print("⚠️  DOCKFIY database connection failed")
        
        # Test tel-bot connection
        tel_bot_conn = collector.get_tel_bot_connection()
        if tel_bot_conn:
            print("✅ Tel-Bot database connection successful")
            tel_bot_conn.close()
        else:
            print("⚠️  Tel-Bot database connection failed")
        
        return True
    except Exception as e:
        print(f"❌ Error checking database connections: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Monitoring Report Bot...")
    print("=" * 50)
    
    steps = [
        ("Environment Setup", setup_environment),
        ("Dependencies Installation", install_dependencies),
        ("Directory Creation", create_reports_directory),
        ("Database Connection Check", check_database_connections)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * 30)
        if step_func():
            success_count += 1
        else:
            print(f"⚠️  {step_name} had issues")
    
    print("\n" + "=" * 50)
    print(f"Setup completed: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your bot token and database credentials")
        print("2. Run: python start_bot.py")
    else:
        print("⚠️  Setup completed with some issues")
        print("Please resolve the issues above before running the bot")
    
    return success_count == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
