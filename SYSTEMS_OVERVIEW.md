# 📊 Monitoring Report Bot - Complete Systems Overview

## 🎯 System Coverage

The monitoring bot now tracks **5 COMPLETE SYSTEMS** across your infrastructure:

| # | System Name | Type | Database | Port | User Tracking |
|---|-------------|------|----------|------|---------------|
| 1 | **@DOCKFIY-PART 3** | Telegram Bot | PostgreSQL | 5433 | `telegram_id` in `user_activity` |
| 2 | **@tel-bot-main** | Telegram Bot | MySQL | 3306 | `telegram_id` in `user_activity` |
| 3 | **Invoice System (Managers/Admins)** | Web App | MySQL | 3306 | `manager_info_id` in `history_log` |
| 4 | **Travel System (Vehicle Forms)** | Web App | MySQL | 3305 | `emp_uid` in `journeys` |
| 5 | **Document Bot (File Uploads)** | Telegram Bot | PostgreSQL | 5432 | `user_id` in `history` |

---

## 📈 What's Being Tracked

### 1. @DOCKFIY-PART 3
- **Purpose**: Document management and file handling bot
- **Activity**: Bot interactions and commands
- **Database**: `telegram-document-bot` (PostgreSQL)
- **Metric**: Unique Telegram users interacting with the bot

### 2. @tel-bot-main
- **Purpose**: Task management and team collaboration bot
- **Activity**: Task creation, assignments, and updates
- **Database**: `task_manager` (MySQL)
- **Metric**: Unique Telegram users using task features

### 3. Invoice System (Managers/Admins)
- **Purpose**: Invoice generation and management system
- **Activity**: Manager and admin activities (not employee downloads)
- **Database**: `invoice_system_testing` (MySQL)
- **Metric**: Unique managers/admins using the system

### 4. Travel System (Vehicle Forms)
- **Purpose**: Vehicle journey tracking and form submissions
- **Activity**: Daily vehicle form submissions (start/end journey)
- **Database**: `u221987201_travel` (MySQL)
- **Metric**: Unique employees submitting vehicle forms

### 5. Document Bot (File Uploads)
- **Purpose**: Secure document upload and file management
- **Activity**: File uploads and document submissions
- **Database**: `telegram_bot_db` (PostgreSQL)
- **Metric**: Unique users uploading files

---

## 📋 Report Contents

### Daily Reports (All 5 Systems)
- **Today's Users**: Unique users per system + total
- **This Week's Users**: Unique users per system + total
- **This Month's Users**: Unique users per system + total

### Trend Analysis (30-Day Graphs)
- **DOCKFIY Bot**: Daily active users (Blue)
- **Tel-Bot**: Daily active users (Red)
- **Invoice System**: Daily active users (Orange)
- **Travel System**: Daily active users (Green)
- **Document Bot**: Daily active users (Purple)

---

## 🔧 Configuration

### Environment Variables Required

```ini
# DOCKFIY Bot Database (PostgreSQL)
DOCKFIY_DB_HOST=localhost
DOCKFIY_DB_PORT=5433
DOCKFIY_DB_NAME=telegram-document-bot
DOCKFIY_DB_USER=postgres
DOCKFIY_DB_PASSWORD=root

# Tel-Bot Database (MySQL)
TEL_BOT_DB_HOST=localhost
TEL_BOT_DB_PORT=3306
TEL_BOT_DB_NAME=task_manager
TEL_BOT_DB_USER=root
TEL_BOT_DB_PASSWORD=root

# Invoice System Database (MySQL)
INVOICE_DB_HOST=localhost
INVOICE_DB_PORT=3306
INVOICE_DB_NAME=invoice_system_testing
INVOICE_DB_USER=root
INVOICE_DB_PASSWORD=root

# Travel System Database (MySQL)
TRAVEL_DB_HOST=localhost
TRAVEL_DB_PORT=3305
TRAVEL_DB_NAME=u221987201_travel
TRAVEL_DB_USER=root
TRAVEL_DB_PASSWORD=

# Document Bot Database (PostgreSQL)
DOCUMENT_DB_HOST=localhost
DOCUMENT_DB_PORT=5432
DOCUMENT_DB_NAME=telegram_bot_db
DOCUMENT_DB_USER=postgres
DOCUMENT_DB_PASSWORD=root

# System Display Names
DOCKFIY_BOT_NAME=@DOCKFIY-PART 3
TEL_BOT_NAME=@tel-bot-main
INVOICE_SYSTEM_NAME=Invoice System (Managers/Admins)
TRAVEL_SYSTEM_NAME=Travel System (Vehicle Forms)
DOCUMENT_BOT_NAME=Document Bot (File Uploads)
```

---

## 🚀 Features

### Bot Commands
- `/start` - Welcome message and bot introduction
- `/stats` - View current statistics for all 5 systems
- `/weekly` - Generate and send weekly report
- `/monthly` - Generate and send monthly report

### Automated Reports
- **Weekly**: Every Monday at 9:00 AM
- **Monthly**: 1st of each month at 9:00 AM

### Report Format
- **PDF Format**: Professional, branded reports
- **Page 1**: Three tables (Today, Week, Month) with all 5 systems
- **Page 2**: Five trend graphs showing 30-day activity patterns

---

## 📊 Data Architecture

### PostgreSQL Systems (2)
1. **DOCKFIY Bot** - Port 5433
2. **Document Bot** - Port 5432

### MySQL Systems (3)
1. **Tel-Bot** - Port 3306
2. **Invoice System** - Port 3306
3. **Travel System** - Port 3305

### Data Collection Method
- **Real-time**: Direct database queries
- **Aggregation**: Daily, Weekly, Monthly unique user counts
- **Trends**: 30-day rolling window for activity patterns

---

## 💡 Use Cases

### Business Intelligence
- Track user engagement across all platforms
- Identify usage patterns and trends
- Monitor system adoption and activity levels

### Performance Monitoring
- Daily active users per system
- Weekly engagement metrics
- Monthly growth tracking

### Reporting
- Automated weekly summaries for management
- Monthly comprehensive reports
- On-demand statistics via bot commands

---

## 🎨 Report Design

### Color Scheme
- **DOCKFIY Bot**: Blue (`#3B82F6`)
- **Tel-Bot**: Red (`#EF4444`)
- **Invoice System**: Orange (`#F59E0B`)
- **Travel System**: Green (`#10B981`)
- **Document Bot**: Purple (`#8B5CF6`)

### Layout
- Professional PDF format
- Branded header with company logo
- Clear tables with alternating row colors
- Line graphs with distinct colors
- Page numbering and timestamps

---

## 📦 Files Modified

### Core Configuration
- `config.py` - Added Document Bot database config
- `env.example` - Added Document Bot environment variables

### Data Collection
- `data_collector.py` - Added Document Bot connection and stats methods

### Report Generation
- `report_generator.py` - Added Document Bot to tables and graphs

### Bot Interface
- `bot_simple.py` - Updated `/stats` command for 5 systems

### Testing
- `test_connections.py` - Added Document Bot tests

---

## ✅ Verification Checklist

Before running the bot, ensure:

- [ ] All 5 databases are accessible
- [ ] Database credentials are correct in `.env`
- [ ] All systems have the required tables
- [ ] Bot token is configured
- [ ] Admin chat ID is set
- [ ] Python dependencies are installed

---

## 🔍 Troubleshooting

### Connection Issues
- Verify database ports are correct
- Check firewall settings
- Ensure database services are running

### Missing Data
- Verify table names match the configuration
- Check if user activity tables have data
- Ensure date/time columns are populated

### Report Generation
- Check write permissions for reports directory
- Verify reportlab library is installed
- Ensure sufficient disk space

---

## 📞 Support

For issues or questions:
1. Check logs in the monitoring bot
2. Run `python test_connections.py` to verify setup
3. Review individual system statistics
4. Check database connectivity

---

**Last Updated**: October 7, 2025
**Version**: 5.0 (Five Systems)
**Status**: ✅ Production Ready

