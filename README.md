# Monitoring Report Bot

A Telegram bot that generates consolidated monitoring reports for multiple bots by collecting user activity data and creating comprehensive PDF reports.

## Features

- **Consolidated Reports**: Combines data from multiple bots into single reports
- **Multiple Time Periods**: Daily, weekly, and monthly statistics
- **Scheduled Reports**: Automatic weekly (Mondays) and monthly (1st of month) reports
- **Visual Charts**: Line graphs showing usage trends over time
- **Admin Controls**: Secure access with admin-only commands
- **Multi-System Support**: Supports DOCKFIY bot, tel-bot, and invoice website

## Supported Systems

1. **@DOCKFIY-PART 3** - PostgreSQL database
2. **@tel-bot-main** - MySQL database  
3. **Invoice Website** - MySQL database

## Report Contents

### Page 1: Usage Statistics Tables
- **Today (Unique Users)**: Current day statistics
- **This Week (Unique Users)**: Monday to current day statistics  
- **This Month (Unique Users)**: Current month statistics
- Each section shows individual bot counts and totals

### Page 2: Usage Trends
- **DOCKFIY Bot Trends**: Daily active users over last 30 days
- **Tel-Bot Trends**: Daily active users over last 30 days
- **Invoice Website Trends**: Daily active users over last 30 days

## Setup Instructions

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the bot token

### 2. Get Admin Chat ID

1. Start a conversation with your new bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response

### 3. Environment Configuration

1. Copy `env.example` to `.env`
2. Fill in your configuration:

```env
# Bot Token (Get from @BotFather)
MONITORING_BOT_TOKEN=your_bot_token_here

# Admin Chat ID (Your Telegram Chat ID)
ADMIN_CHAT_ID=your_chat_id_here

# DOCKFIY Bot Database Configuration
DOCKFIY_DB_HOST=localhost
DOCKFIY_DB_PORT=5433
DOCKFIY_DB_NAME=telegram-document-bot
DOCKFIY_DB_USER=postgres
DOCKFIY_DB_PASSWORD=root

# Tel-Bot Database Configuration
TEL_BOT_DB_HOST=localhost
TEL_BOT_DB_PORT=3306
TEL_BOT_DB_NAME=task_manager
TEL_BOT_DB_USER=root
TEL_BOT_DB_PASSWORD=root

# Bot Names (for display in reports)
DOCKFIY_BOT_NAME=@DOCKFIY-PART 3
TEL_BOT_NAME=@tel-bot-main

# Logging Level
LOG_LEVEL=INFO
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Requirements

Ensure both bots have the `user_activity` table created:

- **DOCKFIY Bot**: Uses PostgreSQL with the migration in `DOCKFIY-PART 3/migrations/create_user_activity_table.sql`
- **Tel-Bot**: Uses MySQL with the migration in `tel-bot-main/migrations/create_user_activity_table.sql`

### 6. Run the Bot

```bash
python bot.py
```

## Usage

### Bot Commands

- `/start` - Show help message and available commands
- `/weekly` - Generate and send weekly report immediately
- `/monthly` - Generate and send monthly report immediately  
- `/stats` - Show current statistics (today, week, month)
- `/schedule` - Show scheduled report information

### Scheduled Reports

- **Weekly Reports**: Every Monday at 9:00 AM
- **Monthly Reports**: 1st of every month at 9:00 AM

Reports are automatically generated and sent to all configured administrators.

## Report Format

The generated PDF reports contain:

1. **Cover Page**: Title and report type
2. **Usage Statistics**: Tables showing unique user counts for:
   - Today
   - This week (Monday to today)
   - This month
3. **Trend Charts**: Line graphs showing daily usage patterns over the last 30 days

## Security

- Only administrators (configured in `ADMIN_CHAT_ID`) can access bot commands
- Database connections use configured credentials
- Reports are temporarily generated and automatically cleaned up after sending

## Troubleshooting

### Common Issues

1. **"Access denied" message**
   - Check that your chat ID is correctly configured in `ADMIN_CHAT_ID`

2. **Database connection errors**
   - Verify database credentials and connectivity
   - Ensure both bots are running and accessible

3. **No data in reports**
   - Check that the `user_activity` tables exist in both databases
   - Verify that the bots are actively tracking user activity

4. **Scheduled reports not working**
   - Check system time and timezone settings
   - Verify the bot is running continuously

### Logs

The bot logs important events including:
- Report generation
- Database connections
- Scheduled report execution
- Error messages

Check the console output for detailed logging information.

## Adding New Bots

To add support for additional bots:

1. Update `config.py` with new database configuration
2. Modify `data_collector.py` to include new bot data collection methods
3. Update `report_generator.py` to include new bot in reports
4. Add bot name to `BOT_NAMES` in config

## Development

The bot is structured with separate modules:

- `config.py` - Configuration management
- `data_collector.py` - Database connections and data collection
- `report_generator.py` - PDF report generation
- `bot.py` - Telegram bot logic and scheduling

## License

This project is part of the monitoring system for your Telegram bots.
# monitoring-bot
