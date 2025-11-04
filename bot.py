"""
Monitoring Report Bot - Main bot application
"""
import logging
import asyncio
import schedule
import time
from datetime import datetime, date
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN, ADMIN_CHAT_ID, SCHEDULE_CONFIG
from report_generator import generate_consolidated_report
from data_collector import DataCollector

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MonitoringReportBot:
    def __init__(self):
        self.data_collector = DataCollector()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied. This bot is for administrators only.")
            return
        
        welcome_text = """
🤖 *Monitoring Report Bot*

This bot generates consolidated reports for your Telegram bots.

*Available Commands:*
/start - Show this help message
/weekly - Generate weekly report
/monthly - Generate monthly report
/stats - Show current statistics
/schedule - Show scheduled reports info

*Scheduled Reports:*
• Weekly reports: Every Monday at 9:00 AM
• Monthly reports: 1st of every month at 9:00 AM

Reports are automatically sent to administrators.
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def weekly_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /weekly command"""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied. This bot is for administrators only.")
            return
        
        await update.message.reply_text("📊 Generating weekly report...")
        
        try:
            # Generate report
            report_path = generate_consolidated_report("weekly")
            
            # Send PDF to admin
            await self._send_report(update, context, report_path, "Weekly")
            
        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            await update.message.reply_text(f"❌ Error generating report: {str(e)}")
    
    async def monthly_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /monthly command"""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied. This bot is for administrators only.")
            return
        
        await update.message.reply_text("📊 Generating monthly report...")
        
        try:
            # Generate report
            report_path = generate_consolidated_report("monthly")
            
            # Send PDF to admin
            await self._send_report(update, context, report_path, "Monthly")
            
        except Exception as e:
            logger.error(f"Error generating monthly report: {e}")
            await update.message.reply_text(f"❌ Error generating report: {str(e)}")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied. This bot is for administrators only.")
            return
        
        await update.message.reply_text("📈 Fetching current statistics...")
        
        try:
            # Get current stats
            stats = self.data_collector.get_combined_stats()
            
            stats_text = f"""
📊 *Current Statistics*

*Today:*
• {BOT_NAMES['dockify']}: {stats['dockify']['today']} users
• {BOT_NAMES['tel_bot']}: {stats['tel_bot']['today']} users
• **Total**: {stats['total']['today']} users

*This Week:*
• {BOT_NAMES['dockify']}: {stats['dockify']['week']} users
• {BOT_NAMES['tel_bot']}: {stats['tel_bot']['week']} users
• **Total**: {stats['total']['week']} users

*This Month:*
• {BOT_NAMES['dockify']}: {stats['dockify']['month']} users
• {BOT_NAMES['tel_bot']}: {stats['tel_bot']['month']} users
• **Total**: {stats['total']['month']} users
            """
            
            await update.message.reply_text(stats_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error fetching stats: {e}")
            await update.message.reply_text(f"❌ Error fetching statistics: {str(e)}")
    
    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /schedule command"""
        if not self._is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied. This bot is for administrators only.")
            return
        
        schedule_text = f"""
📅 *Scheduled Reports*

*Weekly Reports:*
• Day: Monday (Day {SCHEDULE_CONFIG['weekly_day']})
• Time: {SCHEDULE_CONFIG['weekly_time']}

*Monthly Reports:*
• Day: {SCHEDULE_CONFIG['monthly_day']}st of every month
• Time: {SCHEDULE_CONFIG['monthly_time']}

Reports are automatically generated and sent to administrators.
You can also generate reports manually using /weekly or /monthly commands.
        """
        
        await update.message.reply_text(schedule_text, parse_mode='Markdown')
    
    async def _send_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE, report_path: str, report_type: str):
        """Send generated report to admin"""
        try:
            with open(report_path, 'rb') as pdf_file:
                caption = f"📊 {report_type} Monitoring Report\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=pdf_file,
                    filename=f"{report_type.lower()}_monitoring_report.pdf",
                    caption=caption
                )
            
            await update.message.reply_text(f"✅ {report_type} report generated and sent successfully!")
            
            # Clean up the file
            Path(report_path).unlink(missing_ok=True)
            
        except Exception as e:
            logger.error(f"Error sending report: {e}")
            await update.message.reply_text(f"❌ Error sending report: {str(e)}")
    
    def _is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        admin_ids = [int(id.strip()) for id in ADMIN_CHAT_ID.split(',') if id.strip()]
        return user_id in admin_ids
    
    def send_scheduled_report(self, report_type: str):
        """Send scheduled report to all admins"""
        try:
            # Generate report
            report_path = generate_consolidated_report(report_type)
            
            # Send to all admins
            admin_ids = [int(id.strip()) for id in ADMIN_CHAT_ID.split(',') if id.strip()]
            
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                for admin_id in admin_ids:
                    try:
                        with open(report_path, 'rb') as pdf_file:
                            caption = f"📊 Scheduled {report_type.title()} Monitoring Report\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            loop.run_until_complete(self.application.bot.send_document(
                                chat_id=admin_id,
                                document=pdf_file,
                                filename=f"scheduled_{report_type.lower()}_report.pdf",
                                caption=caption
                            ))
                        logger.info(f"Scheduled {report_type} report sent to admin {admin_id}")
                    except Exception as e:
                        logger.error(f"Error sending scheduled report to admin {admin_id}: {e}")
            finally:
                loop.close()
            
            # Clean up the file
            Path(report_path).unlink(missing_ok=True)
            
        except Exception as e:
            logger.error(f"Error generating scheduled {report_type} report: {e}")
    
    def setup_scheduler(self):
        """Setup scheduled report generation"""
        # Weekly reports (Mondays at 9:00 AM)
        schedule.every().monday.at(SCHEDULE_CONFIG['weekly_time']).do(
            lambda: self.send_scheduled_report("weekly")
        )
        
        # Monthly reports (1st of month at 9:00 AM)
        def monthly_job():
            if date.today().day == SCHEDULE_CONFIG['monthly_day']:
                self.send_scheduled_report("monthly")
        
        schedule.every().day.at(SCHEDULE_CONFIG['monthly_time']).do(monthly_job)
        
        logger.info("Scheduler setup completed")
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    async def run(self):
        """Run the bot"""
        # Create application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("weekly", self.weekly_report_command))
        self.application.add_handler(CommandHandler("monthly", self.monthly_report_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("schedule", self.schedule_command))
        
        # Setup scheduler
        self.setup_scheduler()
        
        # Start scheduler in background
        import threading
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Monitoring Report Bot started")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        # Keep the bot running
        try:
            await self.application.updater.idle()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.application.stop()
            await self.application.shutdown()


def main():
    """Main function"""
    bot = MonitoringReportBot()
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
