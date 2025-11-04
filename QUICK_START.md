# Quick Start Guide - Monitoring Report Bot

This guide will help you set up the Monitoring Report Bot in just a few minutes.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Both existing bots** (@DOCKFIY-PART 3 and @tel-bot-main) running with user activity tracking
3. **Database access** to both bots' databases

## Step 1: Create Your Monitoring Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name like "My Monitoring Bot"
4. Choose a username like "my_monitoring_bot"
5. **Save the bot token** - you'll need it in the next step

## Step 2: Get Your Chat ID

1. Start a conversation with your new monitoring bot
2. Send any message (like "hello")
3. Open this URL in your browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find the `"chat":{"id":123456789}` in the response
5. **Save this chat ID** - this is your admin ID

## Step 3: Setup the Bot

### Option A: Windows (Double-click setup)
1. Double-click `setup.bat`
2. Follow the prompts

### Option B: Command Line
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy env.example .env  # Windows
# or
cp env.example .env    # Linux/Mac
```

## Step 4: Configure Your Bot

Edit the `.env` file with your information:

```env
# Replace with your bot token from Step 1
MONITORING_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Replace with your chat ID from Step 2
ADMIN_CHAT_ID=123456789

# Database settings (adjust if different)
DOCKFIY_DB_HOST=localhost
DOCKFIY_DB_PORT=5433
DOCKFIY_DB_NAME=telegram-document-bot
DOCKFIY_DB_USER=postgres
DOCKFIY_DB_PASSWORD=root

TEL_BOT_DB_HOST=localhost
TEL_BOT_DB_PORT=3306
TEL_BOT_DB_NAME=task_manager
TEL_BOT_USER=root
TEL_BOT_PASSWORD=root
```

## Step 5: Test Your Setup

```bash
# Test connections and data collection
python test_connections.py
```

You should see:
- ✅ Configuration test passed
- ✅ Database connections successful
- ✅ Report generation test passed

## Step 6: Start the Bot

### Option A: Windows (Double-click)
Double-click `start_bot.bat`

### Option B: Command Line
```bash
python start_bot.py
```

You should see:
```
🤖 Starting Monitoring Report Bot...
✅ Environment configuration looks good!
✅ Bot configuration loaded successfully
🚀 Starting bot...
INFO - Monitoring Report Bot started
```

## Step 7: Test the Bot

1. Open Telegram and start your monitoring bot
2. Send `/start` - you should see the help message
3. Send `/stats` - you should see current statistics
4. Send `/weekly` - you should receive a PDF report

## Scheduled Reports

The bot will automatically send reports:
- **Weekly**: Every Monday at 9:00 AM
- **Monthly**: 1st of every month at 9:00 AM

## Troubleshooting

### "Access denied" message
- Check that your chat ID is correct in `.env`
- Make sure you're messaging the right bot

### Database connection errors
- Verify both bots are running
- Check database credentials in `.env`
- Ensure `user_activity` tables exist in both databases

### No data in reports
- Check that both bots have user activity tracking enabled
- Verify users are actively using both bots
- Run `python test_connections.py` to diagnose

### Bot not starting
- Check Python version: `python --version` (should be 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check `.env` file exists and is properly configured

## What's Next?

Once your bot is running:

1. **Weekly Reports**: Every Monday at 9 AM, you'll get a consolidated report
2. **Monthly Reports**: On the 1st of each month at 9 AM, you'll get a monthly summary
3. **Manual Reports**: Use `/weekly` or `/monthly` commands anytime
4. **Current Stats**: Use `/stats` to see real-time statistics

## Report Contents

Your reports will show:
- **Daily Usage**: How many unique users today
- **Weekly Usage**: How many unique users this week (Monday to today)
- **Monthly Usage**: How many unique users this month
- **Trends**: Line graphs showing usage patterns over time
- **Bot Breakdown**: Separate statistics for each bot

The reports look exactly like the example in your image, but with your actual bot names and real data!

## Support

If you encounter issues:
1. Check the console output for error messages
2. Run `python test_connections.py` to diagnose problems
3. Verify your database connections and credentials
4. Make sure both source bots are running and tracking user activity

Happy monitoring! 📊🤖
