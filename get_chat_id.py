#!/usr/bin/env python3
"""
Simple script to get your Telegram Chat ID
"""
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def get_chat_id():
    """Get chat ID from bot updates"""
    from config import BOT_TOKEN
    
    if BOT_TOKEN == "YOUR_MONITORING_BOT_TOKEN" or BOT_TOKEN == "YOUR_MONITORING_BOT_TOKEN":
        print("❌ Bot token not configured!")
        print("Please set MONITORING_BOT_TOKEN in your .env file")
        return
    
    import requests
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['ok'] and data['result']:
                print("📱 Recent messages to your bot:")
                print("=" * 50)
                
                for update in data['result'][-5:]:  # Show last 5 messages
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        username = message['from'].get('username', 'No username')
                        first_name = message['from'].get('first_name', 'No name')
                        text = message.get('text', 'No text')
                        
                        print(f"Chat ID: {chat_id}")
                        print(f"From: {first_name} (@{username})")
                        print(f"Message: {text}")
                        print("-" * 30)
                
                print("\n✅ Copy one of the Chat IDs above and add it to your .env file:")
                print("ADMIN_CHAT_ID=your_chat_id_here")
                
            else:
                print("❌ No messages found!")
                print("Please send a message to your bot first, then run this script again.")
        else:
            print(f"❌ Error getting updates: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🔍 Getting your Telegram Chat ID...")
    print("=" * 50)
    get_chat_id()

if __name__ == "__main__":
    main()
