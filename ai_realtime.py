"""
Real-time AI response system with streaming and context awareness
Provides more intelligent responses than static fallbacks
"""

import re
import random
from datetime import datetime
from translations import translate_text

class RealTimeFinancialAI:
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        
    def analyze_query(self, query, user_data=None, transactions=None):
        """Analyze user query and generate contextual response"""
        query_lower = query.lower()
        
        # Update user context
        if user_data:
            self.user_context.update(user_data)
        
        # Calculate financial metrics if transactions available
        financial_summary = self._calculate_financial_summary(transactions) if transactions else {}
        
        # Determine query intent and generate response
        intent = self._classify_intent(query_lower)
        response = self._generate_contextual_response(query, intent, financial_summary)
        
        # Store conversation
        self.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now()
        })
        
        return response
    
    def _classify_intent(self, query):
        """Classify user intent from query"""
        intents = {
            'budget_analysis': ['budget', 'spending', 'expense', 'money management', 'track'],
            'investment_advice': ['invest', 'investment', 'mutual fund', 'sip', 'shares', 'returns'],
            'savings_help': ['save', 'saving', 'emergency fund', 'deposit'],
            'government_schemes': ['government', 'scheme', 'yojana', 'loan', 'subsidy'],
            'goal_planning': ['goal', 'target', 'plan', 'achieve', 'future'],
            'debt_management': ['debt', 'loan', 'emi', 'credit card', 'repay'],
            'tax_planning': ['tax', 'saving', '80c', 'deduction', 'rebate'],
            'insurance': ['insurance', 'policy', 'cover', 'protection'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good evening']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in query for keyword in keywords):
                return intent
        
        return 'general_advice'
    
    def _calculate_financial_summary(self, transactions):
        """Calculate financial metrics from transactions"""
        if not transactions:
            return {}
        
        income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        # Category analysis
        expense_categories = {}
        for t in transactions:
            if t['type'] == 'expense':
                category = t['category']
                expense_categories[category] = expense_categories.get(category, 0) + t['amount']
        
        top_category = max(expense_categories, key=expense_categories.get) if expense_categories else 'None'
        
        return {
            'total_income': income,
            'total_expenses': expenses,
            'net_savings': savings,
            'savings_rate': savings_rate,
            'top_expense_category': top_category,
            'transaction_count': len(transactions)
        }
    
    def _generate_contextual_response(self, query, intent, financial_summary):
        """Generate intelligent response based on context"""
        user_name = self.user_context.get('name', 'there')
        monthly_income = self.user_context.get('monthly_income', 0)
        
        if intent == 'greeting':
            return f"Hello {user_name}! I'm your personal financial advisor. How can I help you manage your finances better today?"
        
        elif intent == 'budget_analysis':
            if financial_summary:
                savings_rate = financial_summary['savings_rate']
                top_category = financial_summary['top_expense_category']
                
                if savings_rate > 20:
                    response = f"Excellent work, {user_name}! You're saving {savings_rate:.1f}% of your income, which is above the recommended 20%. "
                elif savings_rate > 10:
                    response = f"Good job, {user_name}! You're saving {savings_rate:.1f}% of your income. "
                else:
                    response = f"Let's work on improving your savings, {user_name}. You're currently saving {savings_rate:.1f}% of your income. "
                
                response += f"Your highest spending is in {top_category}. Here are personalized tips:\n\n"
                response += self._get_category_specific_advice(top_category)
            else:
                response = f"Hi {user_name}! To give you personalized budgeting advice, start by adding your income and expenses. Here are some general budgeting principles:\n\n"
                response += "1. Follow the 50/30/20 rule\n2. Track every expense\n3. Automate your savings\n4. Review monthly and adjust"
            
            return response
        
        elif intent == 'investment_advice':
            age = self.user_context.get('age', 30)
            risk_advice = self._get_age_appropriate_investment_advice(age, monthly_income)
            
            return f"Based on your profile, {user_name}, here's my investment recommendation:\n\n{risk_advice}\n\nRemember: Start small, stay consistent, and never invest money you can't afford to lose."
        
        elif intent == 'savings_help':
            if monthly_income:
                emergency_fund = monthly_income * 6
                monthly_save = max(monthly_income * 0.2, 1000)
                
                return f"Great question, {user_name}! Based on your income of ₹{monthly_income:,.0f}:\n\n1. Emergency Fund Goal: ₹{emergency_fund:,.0f} (6 months expenses)\n2. Start saving ₹{monthly_save:,.0f} monthly\n3. Use automatic transfers\n4. Keep emergency funds in high-yield savings\n5. Consider short-term FDs for better returns"
            else:
                return self._get_general_savings_advice()
        
        elif intent == 'government_schemes':
            return self._get_personalized_scheme_advice()
        
        elif intent == 'goal_planning':
            return f"Excellent, {user_name}! Goal-based planning is key to financial success. Here's how to approach it:\n\n1. Define SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)\n2. Calculate required monthly savings\n3. Choose appropriate investment vehicles\n4. Automate contributions\n5. Review progress quarterly\n\nWhat specific goal are you planning for? Home, education, retirement, or something else?"
        
        else:
            return self._get_personalized_general_advice()
    
    def _get_category_specific_advice(self, category):
        """Get advice specific to spending category"""
        advice_map = {
            'Food': "1. Plan weekly meals and make grocery lists\n2. Cook at home more often\n3. Buy in bulk for non-perishables\n4. Use grocery apps for discounts",
            'Transportation': "1. Consider carpooling or public transport\n2. Maintain your vehicle regularly\n3. Compare fuel prices\n4. Walk or cycle for short distances",
            'Shopping': "1. Make a list before shopping\n2. Wait 24 hours before big purchases\n3. Look for sales and discounts\n4. Avoid impulse buying",
            'Entertainment': "1. Look for free events and activities\n2. Use streaming services instead of cinema\n3. Host potluck dinners\n4. Take advantage of happy hours"
        }
        
        return advice_map.get(category, "1. Track this category carefully\n2. Set a monthly limit\n3. Look for alternatives\n4. Review necessity vs wants")
    
    def _get_age_appropriate_investment_advice(self, age, income):
        """Get investment advice based on age and income"""
        if age < 30:
            return "At your age, you can take higher risks for better returns:\n1. Start SIP in diversified equity funds\n2. 70% equity, 30% debt allocation\n3. Consider small-cap funds for growth\n4. Use ELSS for tax savings\n5. Start with ₹1000/month and increase annually"
        elif age < 45:
            return "Balanced approach for your age group:\n1. 60% equity, 40% debt allocation\n2. Mix of large-cap and mid-cap funds\n3. Consider hybrid funds\n4. Increase PPF contributions\n5. Review portfolio annually"
        else:
            return "Conservative approach for stability:\n1. 40% equity, 60% debt allocation\n2. Focus on large-cap and debt funds\n3. Increase FD and bond investments\n4. Consider Senior Citizen Savings Scheme\n5. Prioritize capital preservation"
    
    def _get_general_savings_advice(self):
        """General savings advice when no specific data available"""
        return "Here are proven savings strategies:\n\n1. Pay yourself first - save before spending\n2. Automate savings transfers\n3. Use the 52-week savings challenge\n4. Open high-yield savings accounts\n5. Reduce unnecessary subscriptions\n6. Cook at home more often\n7. Compare prices before purchases"
    
    def _get_personalized_scheme_advice(self):
        """Get personalized government scheme advice"""
        age = self.user_context.get('age', 30)
        schemes = []
        
        if age <= 45:
            schemes.append("• Sukanya Samriddhi Yojana - For daughters' education (7.6% returns)")
        
        schemes.extend([
            "• Pradhan Mantri Jan Dhan Yojana - Zero balance banking",
            "• Atal Pension Yojana - Guaranteed pension after 60",
            "• Mudra Yojana - Business loans up to ₹10 lakh",
            "• Stand Up India - Loans for women entrepreneurs"
        ])
        
        return f"Based on your profile, these government schemes can benefit you:\n\n" + "\n".join(schemes) + "\n\nVisit your nearest bank for applications and detailed eligibility criteria."
    
    def _get_personalized_general_advice(self):
        """Personalized general financial advice"""
        name = self.user_context.get('name', 'there')
        
        return f"Here's my general financial guidance for you, {name}:\n\n1. Emergency Fund: Build 6 months of expenses\n2. Insurance: Get adequate health and term life coverage\n3. Investments: Start SIP in mutual funds\n4. Debt: Pay off high-interest debt first\n5. Tax Planning: Use 80C deductions effectively\n6. Regular Review: Monitor and adjust quarterly\n\nWhat specific area would you like to focus on first?"

def stream_response(text, delay=0.05):
    """Simulate streaming response for real-time feel"""
    import time
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # New line at the end