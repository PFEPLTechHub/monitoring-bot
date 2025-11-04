# 🚀 Monitoring Report Bot - Hostinger VPS Deployment Guide

## 📋 Prerequisites

- Hostinger VPS access (SSH)
- Domain name (optional)
- All system databases accessible from VPS

## 🔧 VPS Setup

### 1. Connect to Your VPS
```bash
ssh root@your-vps-ip
# or
ssh username@your-vps-ip
```

### 2. Update System
```bash
apt update && apt upgrade -y
```

### 3. Install Required Software
```bash
# Install Python 3.11
apt install python3.11 python3.11-pip python3.11-venv -y

# Install PostgreSQL client
apt install postgresql-client -y

# Install MySQL client
apt install mysql-client -y

# Install system dependencies for PDF generation
apt install python3-dev libpq-dev build-essential -y

# Install git
apt install git -y

# Install nginx (for web interface)
apt install nginx -y

# Install supervisor (for process management)
apt install supervisor -y
```

## 📁 Project Setup

### 1. Create Project Directory
```bash
mkdir -p /var/www/monitoring-report-bot
cd /var/www/monitoring-report-bot
```

### 2. Clone/Upload Your Project
```bash
# If using git
git clone your-repo-url .

# Or upload your files via SCP/SFTP
```

### 3. Set Up Python Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🔐 Environment Configuration

### 1. Create Environment File
```bash
nano .env
```

### 2. Environment Variables
```env
# Monitoring Report Bot Configuration
MONITORING_BOT_TOKEN=your_actual_bot_token_here
ADMIN_CHAT_ID=your_telegram_chat_id_here

# DOCKFIY Bot Database Configuration
DOCKFIY_DB_HOST=your_dockify_db_host
DOCKFIY_DB_PORT=5433
DOCKFIY_DB_NAME=telegram-document-bot
DOCKFIY_DB_USER=your_db_user
DOCKFIY_DB_PASSWORD=your_db_password

# Tel-Bot Database Configuration
TEL_BOT_DB_HOST=your_telbot_db_host
TEL_BOT_DB_PORT=3306
TEL_BOT_DB_NAME=task_manager
TEL_BOT_DB_USER=your_db_user
TEL_BOT_DB_PASSWORD=your_db_password

# Invoice System Database Configuration
INVOICE_DB_HOST=your_invoice_db_host
INVOICE_DB_PORT=3306
INVOICE_DB_NAME=invoice_system_testing
INVOICE_DB_USER=your_db_user
INVOICE_DB_PASSWORD=your_db_password

# Travel System Database Configuration
TRAVEL_DB_HOST=your_travel_db_host
TRAVEL_DB_PORT=3305
TRAVEL_DB_NAME=u221987201_travel
TRAVEL_DB_USER=your_db_user
TRAVEL_DB_PASSWORD=your_db_password

# Document Bot Database Configuration
DOCUMENT_DB_HOST=your_document_db_host
DOCUMENT_DB_PORT=5433
DOCUMENT_DB_NAME=telegram_bot_db
DOCUMENT_DB_USER=your_db_user
DOCUMENT_DB_PASSWORD=your_db_password

# System Names (for display in reports)
DOCKFIY_BOT_NAME=@DOCKFIY-PART 3
TEL_BOT_NAME=@tel-bot-main
INVOICE_SYSTEM_NAME=Invoice System (Managers/Admins)
TRAVEL_SYSTEM_NAME=Travel System (Vehicle Forms)
DOCUMENT_BOT_NAME=Document Bot (File Uploads)

# Logging Level
LOG_LEVEL=INFO
```

### 3. Set File Permissions
```bash
chmod 600 .env
chown -R www-data:www-data /var/www/monitoring-report-bot
```

## 🔄 Process Management with Supervisor

### 1. Create Supervisor Configuration
```bash
nano /etc/supervisor/conf.d/monitoring-report-bot.conf
```

### 2. Supervisor Config Content
```ini
[program:monitoring-report-bot]
command=/var/www/monitoring-report-bot/venv/bin/python /var/www/monitoring-report-bot/start_bot.py
directory=/var/www/monitoring-report-bot
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/monitoring-report-bot.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
environment=PATH="/var/www/monitoring-report-bot/venv/bin"
```

### 3. Reload Supervisor
```bash
supervisorctl reread
supervisorctl update
supervisorctl start monitoring-report-bot
supervisorctl status monitoring-report-bot
```

## 🌐 Nginx Configuration (Optional - for Web Interface)

### 1. Create Nginx Config
```bash
nano /etc/nginx/sites-available/monitoring-report-bot
```

### 2. Nginx Config Content
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/monitoring-report-bot/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. Enable Site
```bash
ln -s /etc/nginx/sites-available/monitoring-report-bot /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## 🔒 SSL Certificate (Optional)

### 1. Install Certbot
```bash
apt install certbot python3-certbot-nginx -y
```

### 2. Get SSL Certificate
```bash
certbot --nginx -d your-domain.com
```

## 🧪 Testing Deployment

### 1. Test Database Connections
```bash
cd /var/www/monitoring-report-bot
source venv/bin/activate
python test_connections.py
```

### 2. Test Bot Functionality
```bash
python test_document_simple.py
```

### 3. Check Bot Status
```bash
supervisorctl status monitoring-report-bot
tail -f /var/log/monitoring-report-bot.log
```

## 📊 Monitoring & Maintenance

### 1. View Logs
```bash
# Bot logs
tail -f /var/log/monitoring-report-bot.log

# Supervisor logs
supervisorctl tail monitoring-report-bot

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. Restart Bot
```bash
supervisorctl restart monitoring-report-bot
```

### 3. Update Bot
```bash
cd /var/www/monitoring-report-bot
git pull  # If using git
supervisorctl restart monitoring-report-bot
```

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Failed**
   - Check firewall settings
   - Verify database credentials
   - Test connection manually

2. **Bot Not Starting**
   - Check logs: `tail -f /var/log/monitoring-report-bot.log`
   - Verify environment variables
   - Check Python dependencies

3. **Permission Denied**
   - Check file permissions: `ls -la /var/www/monitoring-report-bot`
   - Fix ownership: `chown -R www-data:www-data /var/www/monitoring-report-bot`

4. **Port Already in Use**
   - Check running processes: `netstat -tlnp | grep :8000`
   - Kill conflicting processes

## 📈 Performance Optimization

### 1. Enable Log Rotation
```bash
nano /etc/logrotate.d/monitoring-report-bot
```

Add:
```
/var/log/monitoring-report-bot.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
}
```

### 2. Set Up Monitoring
```bash
# Install monitoring tools
apt install htop iotop -y
```

## 🚀 Deployment Checklist

- [ ] VPS access configured
- [ ] Required software installed
- [ ] Project files uploaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Supervisor configuration created
- [ ] Bot started successfully
- [ ] Database connections tested
- [ ] Bot commands working
- [ ] Reports generating
- [ ] Nginx configured (if needed)
- [ ] SSL certificate installed (if needed)
- [ ] Monitoring set up

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Verify all environment variables
3. Test database connections
4. Ensure all dependencies are installed
5. Check file permissions

---

**Deployment completed successfully!** 🎉
