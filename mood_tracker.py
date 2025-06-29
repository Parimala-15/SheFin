"""
Money Mood Emoji Tracker
Track emotional relationship with money and spending patterns
"""

import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd
from translations import translate_text

class MoneyMoodTracker:
    def __init__(self, db_path="shefin_local.db"):
        self.db_path = db_path
        self.use_postgresql = False  # Always use SQLite for better performance
        self.init_mood_tables()
        
        # Mood categories with emojis
        self.mood_categories = {
            "excited": {
                "emoji": "🤩",
                "name": "Excited",
                "description": "Feeling great about money decisions!"
            },
            "confident": {
                "emoji": "😊",
                "name": "Confident", 
                "description": "Feeling secure and in control"
            },
            "neutral": {
                "emoji": "😐",
                "name": "Neutral",
                "description": "Just okay with money today"
            },
            "worried": {
                "emoji": "😰",
                "name": "Worried",
                "description": "Anxious about finances"
            },
            "stressed": {
                "emoji": "😫",
                "name": "Stressed",
                "description": "Money stress is overwhelming"
            },
            "guilty": {
                "emoji": "😔",
                "name": "Guilty",
                "description": "Regret about spending decisions"
            },
            "happy": {
                "emoji": "😄",
                "name": "Happy",
                "description": "Money decisions bring joy"
            },
            "frustrated": {
                "emoji": "😤",
                "name": "Frustrated",
                "description": "Annoyed with financial situation"
            }
        }
        
        # Spending triggers and emotions
        self.spending_triggers = {
            "impulse": "Impulse buying",
            "emotional": "Emotional spending",
            "social": "Social pressure",
            "necessity": "Essential purchase",
            "celebration": "Celebrating something",
            "stress": "Stress relief",
            "boredom": "Boredom shopping",
            "planned": "Planned purchase"
        }

    def init_mood_tables(self):
        """Initialize mood tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Mood entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                mood_type TEXT NOT NULL,
                mood_intensity INTEGER CHECK(mood_intensity >= 1 AND mood_intensity <= 5),
                spending_trigger TEXT,
                notes TEXT,
                amount_spent REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Mood goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_type TEXT NOT NULL,
                target_mood TEXT NOT NULL,
                target_frequency INTEGER DEFAULT 5,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()

    def log_mood(self, user_id, mood_type, mood_intensity, spending_trigger=None, notes="", amount_spent=0):
        """Log a mood entry"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute("""
                INSERT INTO mood_entries 
                (user_id, date, mood_type, mood_intensity, spending_trigger, notes, amount_spent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, today, mood_type, mood_intensity, spending_trigger, notes, amount_spent))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error logging mood: {e}")
            return False

    def get_mood_history(self, user_id, days=30):
        """Get mood history for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            thirty_days_ago = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            query = """
                SELECT date, mood_type, mood_intensity, spending_trigger, notes, amount_spent
                FROM mood_entries
                WHERE user_id = ? AND date >= ?
                ORDER BY date DESC
            """
            
            df = pd.read_sql_query(query, conn, params=[user_id, thirty_days_ago])
            conn.close()
            
            return df.to_dict('records') if not df.empty else []
            
        except Exception as e:
            print(f"Error getting mood history: {e}")
            return []

    def get_mood_insights(self, user_id, language='english'):
        """Generate mood insights and patterns"""
        history = self.get_mood_history(user_id, days=30)
        
        if not history:
            return {
                "summary": translate_text("Start tracking your money mood to see insights!", language),
                "patterns": [],
                "recommendations": []
            }
        
        # Analyze patterns
        mood_counts = {}
        trigger_counts = {}
        total_emotional_spending = 0
        
        for entry in history:
            mood = entry['mood_type']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            if entry['spending_trigger']:
                trigger = entry['spending_trigger']
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
                
                if trigger in ['emotional', 'stress', 'impulse']:
                    total_emotional_spending += entry.get('amount_spent', 0)
        
        # Most common mood
        most_common_mood = max(mood_counts, key=mood_counts.get) if mood_counts else 'neutral'
        mood_emoji = self.mood_categories.get(most_common_mood, {}).get('emoji', '😐')
        
        # Generate insights
        insights = {
            "summary": f"{mood_emoji} Most common mood: {most_common_mood.title()}",
            "total_entries": len(history),
            "emotional_spending": total_emotional_spending,
            "patterns": self._analyze_patterns(history, language),
            "recommendations": self._get_mood_recommendations(most_common_mood, trigger_counts, language)
        }
        
        return insights

    def _analyze_patterns(self, history, language):
        """Analyze mood and spending patterns"""
        patterns = []
        
        # Weekend vs weekday mood
        weekend_moods = []
        weekday_moods = []
        
        for entry in history:
            date_obj = datetime.strptime(entry['date'], '%Y-%m-%d')
            if date_obj.weekday() >= 5:  # Weekend
                weekend_moods.append(entry['mood_type'])
            else:
                weekday_moods.append(entry['mood_type'])
        
        if weekend_moods and weekday_moods:
            weekend_avg = self._calculate_mood_score(weekend_moods)
            weekday_avg = self._calculate_mood_score(weekday_moods)
            
            if weekend_avg > weekday_avg:
                patterns.append(translate_text("You feel better about money on weekends", language))
            else:
                patterns.append(translate_text("You feel better about money on weekdays", language))
        
        # Spending trigger patterns
        trigger_counts = {}
        for entry in history:
            if entry['spending_trigger']:
                trigger = entry['spending_trigger']
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
        
        if trigger_counts:
            top_trigger = max(trigger_counts, key=trigger_counts.get)
            patterns.append(f"{translate_text('Main spending trigger', language)}: {self.spending_triggers.get(top_trigger, top_trigger)}")
        
        return patterns

    def _calculate_mood_score(self, moods):
        """Calculate average mood score"""
        mood_scores = {
            'excited': 5, 'happy': 4, 'confident': 4,
            'neutral': 3, 'worried': 2, 'frustrated': 2,
            'stressed': 1, 'guilty': 1
        }
        
        if not moods:
            return 3
            
        total_score = sum([mood_scores.get(mood, 3) for mood in moods])
        return total_score / len(moods)

    def _get_mood_recommendations(self, most_common_mood, trigger_counts, language):
        """Get personalized recommendations based on mood patterns"""
        recommendations = []
        
        if most_common_mood in ['stressed', 'worried', 'guilty']:
            recommendations.extend([
                translate_text("Try the 24-hour rule before making purchases", language),
                translate_text("Practice daily money affirmations", language),
                translate_text("Create a calming money routine", language)
            ])
        
        elif most_common_mood in ['excited', 'happy']:
            recommendations.extend([
                translate_text("Channel positive energy into saving goals", language),
                translate_text("Consider automatic investing when you feel good", language)
            ])
        
        # Trigger-based recommendations
        if trigger_counts:
            top_trigger = max(trigger_counts, key=trigger_counts.get)
            
            if top_trigger == 'emotional':
                recommendations.append(translate_text("Try emotion journaling before spending", language))
            elif top_trigger == 'impulse':
                recommendations.append(translate_text("Use a shopping list to avoid impulse buys", language))
            elif top_trigger == 'social':
                recommendations.append(translate_text("Set social spending limits in advance", language))
        
        return recommendations[:3]  # Return top 3 recommendations

    def get_mood_streaks(self, user_id):
        """Calculate mood streaks"""
        history = self.get_mood_history(user_id, days=90)
        
        if not history:
            return {"current_positive_streak": 0, "best_positive_streak": 0}
        
        # Define positive moods
        positive_moods = ['excited', 'happy', 'confident']
        
        current_streak = 0
        best_streak = 0
        temp_streak = 0
        
        # Sort by date ascending
        sorted_history = sorted(history, key=lambda x: x['date'])
        
        for entry in sorted_history:
            if entry['mood_type'] in positive_moods:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 0
        
        # Calculate current streak (from most recent entries)
        for entry in reversed(sorted_history):
            if entry['mood_type'] in positive_moods:
                current_streak += 1
            else:
                break
        
        return {
            "current_positive_streak": current_streak,
            "best_positive_streak": best_streak
        }

    def set_mood_goal(self, user_id, goal_type, target_mood, target_frequency=5):
        """Set a mood improvement goal"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO mood_goals 
                (user_id, goal_type, target_mood, target_frequency)
                VALUES (?, ?, ?, ?)
            """, (user_id, goal_type, target_mood, target_frequency))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error setting mood goal: {e}")
            return False

    def get_mood_calendar_data(self, user_id, month=None, year=None):
        """Get mood data for calendar view"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"
            
            cursor.execute("""
                SELECT date, mood_type, mood_intensity
                FROM mood_entries
                WHERE user_id = ? AND date >= ? AND date < ?
                ORDER BY date
            """, (user_id, start_date, end_date))
            
            results = cursor.fetchall()
            conn.close()
            
            # Format for calendar
            calendar_data = {}
            for date, mood_type, intensity in results:
                day = int(date.split('-')[2])
                emoji = self.mood_categories.get(mood_type, {}).get('emoji', '😐')
                calendar_data[day] = {
                    'emoji': emoji,
                    'mood': mood_type,
                    'intensity': intensity
                }
            
            return calendar_data
            
        except Exception as e:
            print(f"Error getting calendar data: {e}")
            return {}