import sqlite3
import os
from typing import List, Dict, Optional
from config import config_manager

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        """初始化数据库管理器"""
        db_config = config_manager.get_database_config()
        self.enabled = db_config.get("enabled", False)
        self.db_path = db_config.get("db_path", "chat_history.db")
        
        if self.enabled:
            self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        try:
            # 确保数据库目录存在
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # 检查数据库文件是否存在
            db_exists = os.path.exists(self.db_path)
            
            # 连接数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建表格
            if not db_exists:
                # 创建角色信息表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS character_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        greeting TEXT,
                        tone TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建聊天历史表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 插入默认角色
                cursor.execute('''
                    INSERT INTO character_info (name, description, greeting, tone)
                    VALUES (?, ?, ?, ?)
                ''', (
                    "AI Vtuber",
                    "一个友好的AI虚拟主播",
                    "你好！我是你的AI虚拟主播，很高兴认识你！",
                    "活泼、友好、幽默"
                ))
            
            # 提交并关闭连接
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"初始化数据库失败: {e}")
    
    def save_chat_message(self, role: str, content: str) -> bool:
        """保存聊天消息"""
        if not self.enabled:
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (role, content)
                VALUES (?, ?)
            ''', (role, content))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"保存聊天消息失败: {e}")
            return False
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, str]]:
        """获取聊天历史"""
        if not self.enabled:
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, content, timestamp
                FROM chat_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            # 反转顺序，使最早的消息在前
            history = []
            for role, content, timestamp in reversed(results):
                history.append({
                    "role": role,
                    "content": content,
                    "timestamp": timestamp
                })
            
            return history
        except Exception as e:
            print(f"获取聊天历史失败: {e}")
            return []
    
    def clear_chat_history(self) -> bool:
        """清空聊天历史"""
        if not self.enabled:
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM chat_history
            ''')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"清空聊天历史失败: {e}")
            return False
    
    def get_character_info(self) -> Optional[Dict[str, str]]:
        """获取角色信息"""
        if not self.enabled:
            return None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT name, description, greeting, tone
                FROM character_info
                ORDER BY id LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "name": result[0],
                    "description": result[1],
                    "greeting": result[2],
                    "tone": result[3]
                }
            else:
                return None
        except Exception as e:
            print(f"获取角色信息失败: {e}")
            return None
    
    def update_character_info(self, name: str, description: str, greeting: str, tone: str) -> bool:
        """更新角色信息"""
        if not self.enabled:
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查是否存在角色信息
            cursor.execute('''
                SELECT id FROM character_info
                ORDER BY id LIMIT 1
            ''')
            
            result = cursor.fetchone()
            
            if result:
                # 更新现有角色
                cursor.execute('''
                    UPDATE character_info
                    SET name = ?, description = ?, greeting = ?, tone = ?
                    WHERE id = ?
                ''', (name, description, greeting, tone, result[0]))
            else:
                # 插入新角色
                cursor.execute('''
                    INSERT INTO character_info (name, description, greeting, tone)
                    VALUES (?, ?, ?, ?)
                ''', (name, description, greeting, tone))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新角色信息失败: {e}")
            return False

# 创建全局数据库管理器实例
database_manager = DatabaseManager()
