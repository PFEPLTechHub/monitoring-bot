"""
Data Collector - Collects user activity data from both bots
"""
import logging
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import psycopg
import pymysql

from config import DOCKFIY_DB_CONFIG, TEL_BOT_DB_CONFIG, INVOICE_DB_CONFIG, TRAVEL_DB_CONFIG, DOCUMENT_DB_CONFIG

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.dockify_config = DOCKFIY_DB_CONFIG
        self.tel_bot_config = TEL_BOT_DB_CONFIG
        self.invoice_config = INVOICE_DB_CONFIG
        self.travel_config = TRAVEL_DB_CONFIG
        self.document_config = DOCUMENT_DB_CONFIG
    
    def get_dockify_connection(self):
        """Get PostgreSQL connection for DOCKFIY bot"""
        try:
            conn_str = f"postgresql://{self.dockify_config['user']}:{self.dockify_config['password']}@{self.dockify_config['host']}:{self.dockify_config['port']}/{self.dockify_config['database']}"
            return psycopg.connect(conn_str)
        except Exception as e:
            logger.error(f"Failed to connect to DOCKFIY database: {e}")
            return None
    
    def get_tel_bot_connection(self):
        """Get MySQL connection for tel-bot"""
        try:
            return pymysql.connect(
                host=self.tel_bot_config['host'],
                port=int(self.tel_bot_config['port']),
                user=self.tel_bot_config['user'],
                password=self.tel_bot_config['password'],
                database=self.tel_bot_config['database'],
                charset='utf8mb4'
            )
        except Exception as e:
            logger.error(f"Failed to connect to tel-bot database: {e}")
            return None
    
    def get_invoice_connection(self):
        """Get MySQL connection for invoice system"""
        try:
            return pymysql.connect(
                host=self.invoice_config['host'],
                port=int(self.invoice_config['port']),
                user=self.invoice_config['user'],
                password=self.invoice_config['password'],
                database=self.invoice_config['database'],
                charset='utf8mb4'
            )
        except Exception as e:
            logger.error(f"Failed to connect to invoice database: {e}")
            return None
    
    def get_travel_connection(self):
        """Get MySQL connection for travel system"""
        try:
            return pymysql.connect(
                host=self.travel_config['host'],
                port=int(self.travel_config['port']),
                user=self.travel_config['user'],
                password=self.travel_config['password'],
                database=self.travel_config['database'],
                charset='utf8mb4'
            )
        except Exception as e:
            logger.error(f"Failed to connect to travel database: {e}")
            return None
    
    def get_document_connection(self):
        """Get PostgreSQL connection for document bot"""
        try:
            conn_str = f"postgresql://{self.document_config['user']}:{self.document_config['password']}@{self.document_config['host']}:{self.document_config['port']}/{self.document_config['database']}"
            logger.info(f"Connecting to document bot database: {self.document_config['host']}:{self.document_config['port']}/{self.document_config['database']}")
            conn = psycopg.connect(conn_str)
            logger.info("Document bot database connection successful")
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to document database: {e}")
            return None
    
    def get_dockify_stats(self, target_date: date = None) -> Dict:
        """Get user statistics from DOCKFIY bot"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_dockify_connection()
        if not conn:
            return {"today": 0, "week": 0, "month": 0}
        
        try:
            with conn.cursor() as cur:
                # Today's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id)
                    FROM user_activity
                    WHERE activity_date = %s
                """, (target_date,))
                result = cur.fetchone()
                today = result[0] if result else 0
                
                # Week's unique users (Monday to today)
                week_start = target_date - timedelta(days=target_date.weekday())
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id)
                    FROM user_activity
                    WHERE activity_date >= %s AND activity_date <= %s
                """, (week_start, target_date))
                result = cur.fetchone()
                week = result[0] if result else 0
                
                # Month's unique users
                month_start = date(target_date.year, target_date.month, 1)
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id)
                    FROM user_activity
                    WHERE activity_date >= %s AND activity_date <= %s
                """, (month_start, target_date))
                result = cur.fetchone()
                month = result[0] if result else 0
                
                return {"today": today, "week": week, "month": month}
        
        except Exception as e:
            logger.error(f"Error getting DOCKFIY stats: {e}")
            return {"today": 0, "week": 0, "month": 0}
        finally:
            conn.close()
    
    def get_tel_bot_stats(self, target_date: date = None) -> Dict:
        """Get user statistics from tel-bot"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_tel_bot_connection()
        if not conn:
            return {"today": 0, "week": 0, "month": 0}
        
        try:
            with conn.cursor() as cur:
                # Today's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id) as count
                    FROM user_activity
                    WHERE activity_date = %s
                """, (target_date.strftime('%Y-%m-%d'),))
                result = cur.fetchone()
                today = result[0] if result else 0
                
                # Week's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id) as count
                    FROM user_activity
                    WHERE activity_date >= DATE_SUB(%s, INTERVAL WEEKDAY(%s) DAY)
                      AND activity_date <= %s
                """, (target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d')))
                result = cur.fetchone()
                week = result[0] if result else 0
                
                # Month's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT telegram_id) as count
                    FROM user_activity
                    WHERE YEAR(activity_date) = %s
                      AND MONTH(activity_date) = %s
                """, (target_date.year, target_date.month))
                result = cur.fetchone()
                month = result[0] if result else 0
                
                return {"today": today, "week": week, "month": month}
        
        except Exception as e:
            logger.error(f"Error getting tel-bot stats: {e}")
            return {"today": 0, "week": 0, "month": 0}
        finally:
            conn.close()
    
    def get_invoice_stats(self, target_date: date = None) -> Dict:
        """Get user statistics from invoice system"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_invoice_connection()
        if not conn:
            return {"today": 0, "week": 0, "month": 0}
        
        try:
            with conn.cursor() as cur:
                # Today's unique users (managers and admins who used the system)
                cur.execute("""
                    SELECT COUNT(DISTINCT manager_info_id) as count
                    FROM history_log
                    WHERE DATE(date) = %s
                      AND manager_info_id IS NOT NULL
                """, (target_date.strftime('%Y-%m-%d'),))
                result = cur.fetchone()
                today = result[0] if result else 0
                
                # Week's unique users (managers and admins who used the system)
                cur.execute("""
                    SELECT COUNT(DISTINCT manager_info_id) as count
                    FROM history_log
                    WHERE DATE(date) >= DATE_SUB(%s, INTERVAL WEEKDAY(%s) DAY)
                      AND DATE(date) <= %s
                      AND manager_info_id IS NOT NULL
                """, (target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d')))
                result = cur.fetchone()
                week = result[0] if result else 0
                
                # Month's unique users (managers and admins who used the system)
                cur.execute("""
                    SELECT COUNT(DISTINCT manager_info_id) as count
                    FROM history_log
                    WHERE YEAR(DATE(date)) = %s
                      AND MONTH(DATE(date)) = %s
                      AND manager_info_id IS NOT NULL
                """, (target_date.year, target_date.month))
                result = cur.fetchone()
                month = result[0] if result else 0
                
                return {"today": today, "week": week, "month": month}
        
        except Exception as e:
            logger.error(f"Error getting invoice stats: {e}")
            return {"today": 0, "week": 0, "month": 0}
        finally:
            conn.close()
    
    def get_travel_stats(self, target_date: date = None) -> Dict:
        """Get user statistics from travel system"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_travel_connection()
        if not conn:
            return {"today": 0, "week": 0, "month": 0}
        
        try:
            with conn.cursor() as cur:
                # Today's unique users (employees who submitted vehicle forms)
                cur.execute("""
                    SELECT COUNT(DISTINCT emp_uid) as count
                    FROM journeys
                    WHERE DATE(start_time) = %s
                      AND emp_uid IS NOT NULL
                """, (target_date.strftime('%Y-%m-%d'),))
                result = cur.fetchone()
                today = result[0] if result else 0
                
                # Week's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT emp_uid) as count
                    FROM journeys
                    WHERE DATE(start_time) >= DATE_SUB(%s, INTERVAL WEEKDAY(%s) DAY)
                      AND DATE(start_time) <= %s
                      AND emp_uid IS NOT NULL
                """, (target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d'), target_date.strftime('%Y-%m-%d')))
                result = cur.fetchone()
                week = result[0] if result else 0
                
                # Month's unique users
                cur.execute("""
                    SELECT COUNT(DISTINCT emp_uid) as count
                    FROM journeys
                    WHERE YEAR(DATE(start_time)) = %s
                      AND MONTH(DATE(start_time)) = %s
                      AND emp_uid IS NOT NULL
                """, (target_date.year, target_date.month))
                result = cur.fetchone()
                month = result[0] if result else 0
                
                return {"today": today, "week": week, "month": month}
        
        except Exception as e:
            logger.error(f"Error getting travel stats: {e}")
            return {"today": 0, "week": 0, "month": 0}
        finally:
            conn.close()
    
    def get_document_stats(self, target_date: date = None) -> Dict:
        """Get user statistics from document bot"""
        if target_date is None:
            target_date = date.today()
        
        conn = self.get_document_connection()
        if not conn:
            return {"today": 0, "week": 0, "month": 0}
        
        try:
            with conn.cursor() as cur:
                # Check if upload_sessions has created_at column
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'upload_sessions' AND column_name = 'created_at'
                """)
                has_created_at = cur.fetchone() is not None
                
                if has_created_at:
                    logger.info("Using upload_sessions table with created_at column")
                    # Today's unique users (users who started upload sessions)
                    cur.execute("""
                        SELECT COUNT(DISTINCT user_id) as count
                        FROM upload_sessions
                        WHERE DATE(created_at) = %s
                    """, (target_date,))
                    result = cur.fetchone()
                    today = result[0] if result else 0
                    
                    # Week's unique users
                    week_start = target_date - timedelta(days=target_date.weekday())
                    cur.execute("""
                        SELECT COUNT(DISTINCT user_id) as count
                        FROM upload_sessions
                        WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                    """, (week_start, target_date))
                    result = cur.fetchone()
                    week = result[0] if result else 0
                    
                    # Month's unique users
                    month_start = target_date.replace(day=1)
                    cur.execute("""
                        SELECT COUNT(DISTINCT user_id) as count
                        FROM upload_sessions
                        WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                    """, (month_start, target_date))
                    result = cur.fetchone()
                    month = result[0] if result else 0
                    
                    logger.info(f"Document bot stats from upload_sessions: today={today}, week={week}, month={month}")
                    return {"today": today, "week": week, "month": month}
                
                else:
                    logger.info("upload_sessions missing created_at, using total count from upload_sessions")
                    # upload_sessions table doesn't have created_at, so use total unique users
                    cur.execute("SELECT COUNT(DISTINCT user_id) FROM upload_sessions")
                    result = cur.fetchone()
                    total_users = result[0] if result else 0
                    logger.info(f"Document bot upload_sessions query result: {total_users}")
                    
                    # Since we can't filter by date, return the total for all periods
                    logger.info(f"Document bot stats from upload_sessions (total): {total_users}")
                    return {"today": total_users, "week": total_users, "month": total_users}
        
        except Exception as e:
            logger.error(f"Error getting document stats: {e}")
            return {"today": 0, "week": 0, "month": 0}
        finally:
            conn.close()
    
    def get_combined_stats(self, target_date: date = None) -> Dict:
        """Get combined statistics from both bots"""
        if target_date is None:
            target_date = date.today()
        
        dockify_stats = self.get_dockify_stats(target_date)
        tel_bot_stats = self.get_tel_bot_stats(target_date)
        invoice_stats = self.get_invoice_stats(target_date)
        travel_stats = self.get_travel_stats(target_date)
        document_stats = self.get_document_stats(target_date)
        
        return {
            "dockify": dockify_stats,
            "tel_bot": tel_bot_stats,
            "invoice": invoice_stats,
            "travel": travel_stats,
            "document": document_stats,
            "total": {
                "today": dockify_stats["today"] + tel_bot_stats["today"] + invoice_stats["today"] + travel_stats["today"] + document_stats["today"],
                "week": dockify_stats["week"] + tel_bot_stats["week"] + invoice_stats["week"] + travel_stats["week"] + document_stats["week"],
                "month": dockify_stats["month"] + tel_bot_stats["month"] + invoice_stats["month"] + travel_stats["month"] + document_stats["month"]
            }
        }
    
    def get_daily_trends(self, days: int = 30) -> Dict:
        """Get daily trends for both bots"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get DOCKFIY trends
        dockify_trends = self._get_dockify_daily_trends(start_date, end_date)
        
        # Get tel-bot trends
        tel_bot_trends = self._get_tel_bot_daily_trends(start_date, end_date)
        
        # Get invoice trends
        invoice_trends = self._get_invoice_daily_trends(start_date, end_date)
        
        travel_trends = self._get_travel_daily_trends(start_date, end_date)
        
        # Get document trends
        document_trends = self._get_document_daily_trends(start_date, end_date)
        
        return {
            "dockify": dockify_trends,
            "tel_bot": tel_bot_trends,
            "invoice": invoice_trends,
            "travel": travel_trends,
            "document": document_trends
        }
    
    def _get_dockify_daily_trends(self, start_date: date, end_date: date) -> List[Dict]:
        """Get daily trends from DOCKFIY bot"""
        conn = self.get_dockify_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        activity_date,
                        COUNT(DISTINCT telegram_id) as unique_users
                    FROM user_activity
                    WHERE activity_date >= %s AND activity_date <= %s
                    GROUP BY activity_date
                    ORDER BY activity_date ASC
                """, (start_date, end_date))
                
                results = cur.fetchall()
                return [
                    {
                        'date': row[0].isoformat(),
                        'unique_users': row[1]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error getting DOCKFIY daily trends: {e}")
            return []
        finally:
            conn.close()
    
    def _get_tel_bot_daily_trends(self, start_date: date, end_date: date) -> List[Dict]:
        """Get daily trends from tel-bot"""
        conn = self.get_tel_bot_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        activity_date,
                        COUNT(DISTINCT telegram_id) as unique_users
                    FROM user_activity
                    WHERE activity_date >= %s AND activity_date <= %s
                    GROUP BY activity_date
                    ORDER BY activity_date ASC
                """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                results = cur.fetchall()
                return [
                    {
                        'date': row[0].strftime('%Y-%m-%d'),
                        'unique_users': row[1]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error getting tel-bot daily trends: {e}")
            return []
        finally:
            conn.close()
    
    def _get_invoice_daily_trends(self, start_date: date, end_date: date) -> List[Dict]:
        """Get daily trends from invoice system"""
        conn = self.get_invoice_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        DATE(date) as activity_date,
                        COUNT(DISTINCT manager_info_id) as unique_users
                    FROM history_log
                    WHERE DATE(date) >= %s AND DATE(date) <= %s
                      AND manager_info_id IS NOT NULL
                    GROUP BY DATE(date)
                    ORDER BY DATE(date) ASC
                """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                results = cur.fetchall()
                return [
                    {
                        'date': row[0].strftime('%Y-%m-%d'),
                        'unique_users': row[1]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error getting invoice daily trends: {e}")
            return []
        finally:
            conn.close()
    
    def _get_travel_daily_trends(self, start_date: date, end_date: date) -> List[Dict]:
        """Get daily trends from travel system"""
        conn = self.get_travel_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        DATE(start_time) as activity_date,
                        COUNT(DISTINCT emp_uid) as unique_users
                    FROM journeys
                    WHERE DATE(start_time) >= %s AND DATE(start_time) <= %s
                      AND emp_uid IS NOT NULL
                    GROUP BY DATE(start_time)
                    ORDER BY DATE(start_time) ASC
                """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                results = cur.fetchall()
                return [
                    {
                        'date': row[0].strftime('%Y-%m-%d'),
                        'unique_users': row[1]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error getting travel daily trends: {e}")
            return []
        finally:
            conn.close()
    
    def _get_document_daily_trends(self, start_date: date, end_date: date) -> List[Dict]:
        """Get daily trends from document bot"""
        conn = self.get_document_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cur:
                # Check if upload_sessions has created_at column
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'upload_sessions' AND column_name = 'created_at'
                """)
                has_created_at = cur.fetchone() is not None
                
                if has_created_at:
                    # Use upload_sessions table with timestamps
                    cur.execute("""
                        SELECT 
                            DATE(created_at) as activity_date,
                            COUNT(DISTINCT user_id) as unique_users
                        FROM upload_sessions
                        WHERE DATE(created_at) >= %s AND DATE(created_at) <= %s
                        GROUP BY DATE(created_at)
                        ORDER BY DATE(created_at) ASC
                    """, (start_date, end_date))
                else:
                    # upload_sessions doesn't have created_at column, can't generate trends
                    logger.info("upload_sessions missing created_at, cannot generate daily trends")
                    return []
                
                results = cur.fetchall()
                return [
                    {
                        'date': row[0].strftime('%Y-%m-%d'),
                        'unique_users': row[1]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error getting document daily trends: {e}")
            return []
        finally:
            conn.close()
