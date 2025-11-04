#!/usr/bin/env python3
"""
Package Monitoring Report Bot for Hostinger VPS Deployment
This script creates a deployment package with all necessary files
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for Hostinger VPS"""
    
    print("📦 Creating Monitoring Report Bot Deployment Package...")
    print("=" * 60)
    
    # Create deployment directory
    deploy_dir = "monitoring-report-bot-deployment"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Files to include in deployment
    essential_files = [
        "bot_simple.py",
        "start_bot.py", 
        "data_collector.py",
        "report_generator.py",
        "config.py",
        "requirements.txt",
        "test_connections.py",
        "test_document_simple.py",
        "env.example",
        "deploy.sh",
        "supervisor.conf",
        "nginx.conf",
        "systemd.service",
        "DEPLOYMENT_HOSTINGER_VPS.md"
    ]
    
    # Copy essential files
    print("📋 Copying essential files...")
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (not found)")
    
    # Create reports directory
    reports_dir = os.path.join(deploy_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create static directory (for future web interface)
    static_dir = os.path.join(deploy_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    # Create logs directory
    logs_dir = os.path.join(deploy_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create a simple README for deployment
    readme_content = f"""# Monitoring Report Bot - Deployment Package

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Quick Start

1. Upload this package to your VPS
2. Extract to /var/www/monitoring-report-bot
3. Run: chmod +x deploy.sh && ./deploy.sh
4. Configure .env file with your database credentials
5. Start the bot: sudo supervisorctl start monitoring-report-bot

## Files Included

- bot_simple.py - Main bot application
- data_collector.py - Data collection from all systems
- report_generator.py - PDF report generation
- config.py - Configuration management
- deploy.sh - Automated deployment script
- supervisor.conf - Process management config
- nginx.conf - Web server config (optional)
- DEPLOYMENT_HOSTINGER_VPS.md - Detailed deployment guide

## Next Steps

1. Configure your .env file with database credentials
2. Test connections: python test_connections.py
3. Start the bot and check logs
4. Test bot commands in Telegram

For detailed instructions, see DEPLOYMENT_HOSTINGER_VPS.md
"""
    
    with open(os.path.join(deploy_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    # Create zip package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"monitoring-report-bot-deployment-{timestamp}.zip"
    
    print(f"\n📦 Creating zip package: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
                print(f"  ✅ {arcname}")
    
    # Clean up deployment directory
    shutil.rmtree(deploy_dir)
    
    print(f"\n🎉 Deployment package created: {zip_filename}")
    print(f"📁 Package size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    print("\n📋 Next steps:")
    print("1. Upload the zip file to your Hostinger VPS")
    print("2. Extract: unzip monitoring-report-bot-deployment-*.zip")
    print("3. Run: chmod +x deploy.sh && ./deploy.sh")
    print("4. Configure your .env file")
    print("5. Start the bot!")
    
    return zip_filename

if __name__ == "__main__":
    create_deployment_package()
