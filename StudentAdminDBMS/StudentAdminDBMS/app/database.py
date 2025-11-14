import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                'postgresql://postgres:admin123@localhost:5432/lost_found_db',
                cursor_factory=RealDictCursor
            )
            self.conn.autocommit = False
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    def get_cursor(self):
        if self.conn.closed:
            self.connect()
        return self.conn.cursor()
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
    
    # User operations
    def get_user_by_username(self, username):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_user_by_id(self, user_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def create_user(self, username, email, password_hash, full_name, role, phone):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING user_id
            """, (username, email, password_hash, full_name, role, phone))
            user_id = cursor.fetchone()['user_id']
            self.commit()
            cursor.close()
            return user_id
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
    
    def update_last_login(self, user_id):
        cursor = self.get_cursor()
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s", (user_id,))
        self.commit()
        cursor.close()
    
    def get_all_users(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT user_id, username, email, full_name, role, phone, created_at, last_login FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        return users
    
    # Lost items operations
    def create_lost_item(self, user_id, item_name, category, description, location_lost, date_lost):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO lost_items (user_id, item_name, category, description, location_lost, date_lost)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING lost_id
            """, (user_id, item_name, category, description, location_lost, date_lost))
            lost_id = cursor.fetchone()['lost_id']
            self.commit()
            cursor.close()
            return lost_id
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
    
    def get_lost_items_by_user(self, user_id):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT * FROM lost_items 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def get_all_lost_items(self):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT l.*, u.username, u.full_name, u.email, u.phone
            FROM lost_items l
            JOIN users u ON l.user_id = u.user_id
            ORDER BY l.created_at DESC
        """)
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def update_lost_item_status(self, lost_id, status):
        cursor = self.get_cursor()
        cursor.execute("UPDATE lost_items SET status = %s WHERE lost_id = %s", (status, lost_id))
        self.commit()
        cursor.close()
    
    # Found items operations
    def create_found_item(self, user_id, item_name, category, description, location_found, date_found):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO found_items (user_id, item_name, category, description, location_found, date_found)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING found_id
            """, (user_id, item_name, category, description, location_found, date_found))
            found_id = cursor.fetchone()['found_id']
            self.commit()
            cursor.close()
            return found_id
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
    
    def get_found_items_by_user(self, user_id):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT * FROM found_items 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def get_found_item_by_id(self, found_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM found_items WHERE found_id = %s", (found_id,))
        item = cursor.fetchone()
        cursor.close()
        return item
    
    def get_all_found_items(self):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT f.*, u.username, u.full_name, u.email, u.phone
            FROM found_items f
            JOIN users u ON f.user_id = u.user_id
            ORDER BY f.created_at DESC
        """)
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def update_found_item_status(self, found_id, status):
        cursor = self.get_cursor()
        cursor.execute("UPDATE found_items SET status = %s WHERE found_id = %s", (status, found_id))
        self.commit()
        cursor.close()
    
    # Matching operations
    def create_match(self, lost_id, found_id, match_score):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO match_table (lost_id, found_id, match_score)
                VALUES (%s, %s, %s)
                ON CONFLICT (lost_id, found_id) DO UPDATE SET match_score = EXCLUDED.match_score
                RETURNING match_id
            """, (lost_id, found_id, match_score))
            match_id = cursor.fetchone()['match_id']
            self.commit()
            cursor.close()
            return match_id
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
    
    def get_matches_for_lost_item(self, lost_id):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT m.*, f.*, u.username, u.full_name, u.phone, u.email
            FROM match_table m
            JOIN found_items f ON m.found_id = f.found_id
            JOIN users u ON f.user_id = u.user_id
            WHERE m.lost_id = %s
            ORDER BY m.match_score DESC, m.match_date DESC
        """, (lost_id,))
        matches = cursor.fetchall()
        cursor.close()
        return matches
    
    def get_matches_for_found_item(self, found_id):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT m.*, l.*, u.username, u.full_name, u.phone, u.email
            FROM match_table m
            JOIN lost_items l ON m.lost_id = l.lost_id
            JOIN users u ON l.user_id = u.user_id
            WHERE m.found_id = %s
            ORDER BY m.match_score DESC, m.match_date DESC
        """, (found_id,))
        matches = cursor.fetchall()
        cursor.close()
        return matches
    
    def verify_match(self, match_id):
        cursor = self.get_cursor()
        cursor.execute("UPDATE match_table SET verified = TRUE WHERE match_id = %s", (match_id,))
        self.commit()
        cursor.close()
    
    # Notification operations
    def create_notification(self, user_id, match_id, message):
        cursor = self.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO notifications (user_id, match_id, message)
                VALUES (%s, %s, %s)
                RETURNING notification_id
            """, (user_id, match_id, message))
            notification_id = cursor.fetchone()['notification_id']
            self.commit()
            cursor.close()
            return notification_id
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
    
    def get_user_notifications(self, user_id, unread_only=False):
        cursor = self.get_cursor()
        if unread_only:
            cursor.execute("""
                SELECT * FROM notifications 
                WHERE user_id = %s AND is_read = FALSE
                ORDER BY created_at DESC
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT * FROM notifications 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
        notifications = cursor.fetchall()
        cursor.close()
        return notifications
    
    def mark_notification_read(self, notification_id):
        cursor = self.get_cursor()
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE notification_id = %s", (notification_id,))
        self.commit()
        cursor.close()
    
    def mark_all_notifications_read(self, user_id):
        cursor = self.get_cursor()
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (user_id,))
        self.commit()
        cursor.close()
    
    # Statistics
    def get_statistics(self):
        cursor = self.get_cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as total FROM lost_items")
        stats['total_lost'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM lost_items WHERE status = 'unfound'")
        stats['unfound_lost'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM found_items")
        stats['total_found'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM found_items WHERE status = 'unclaimed'")
        stats['unclaimed_found'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM match_table WHERE verified = TRUE")
        stats['verified_matches'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'student'")
        stats['total_students'] = cursor.fetchone()['total']
        
        cursor.close()
        return stats
