import json
import os
from datetime import datetime, timedelta
from utils import format_currency
from translations import translate_text
from ai_fallback import FallbackFinancialAdvisor
from ai_realtime import RealTimeFinancialAI
from gemini_ai import get_financial_advice, analyze_budget, get_investment_guidance, get_government_scheme_advice
from dotenv import load_dotenv

class FinancialChatbot:
    def __init__(self):
        self.fallback_advisor = FallbackFinancialAdvisor()
        self.realtime_ai = RealTimeFinancialAI()
        self.use_ai = False
        
        # Try to initialize Gemini AI
        try:
            load_dotenv()
            gemini_key = os.getenv("GEMINI_API_KEY")
            if gemini_key:
                self.use_ai = True
                print("✅ Google Gemini AI connected successfully")
            else:
                print("⚠️ GEMINI_API_KEY not found, using fallback responses")
        except Exception as e:
            print(f"❌ Gemini AI initialization failed: {e}")
            print("🔄 Using enhanced intelligent fallback responses")

    def get_financial_advice(self, query, user_data, transactions, language='english'):
        """Get personalized financial advice"""
        if self.use_ai and language == 'english':
            try:
                # Prepare context for Gemini AI
                expense_transactions = [t for t in transactions if t['type'] == 'expense'] if transactions else []
                income_transactions = [t for t in transactions if t['type'] == 'income'] if transactions else []
                
                total_expenses = sum([t['amount'] for t in expense_transactions])
                total_income = sum([t['amount'] for t in income_transactions])
                
                user_context = f"""
                User Profile:
                - Name: {user_data['name']}
                - Age: {user_data['age']}
                - Monthly Income: ₹{user_data['monthly_income']}
                - Recent Total Expenses: ₹{total_expenses}
                - Recent Total Income: ₹{total_income}
                """
                
                transaction_summary = f"Recent transactions: {len(expense_transactions)} expenses totaling ₹{total_expenses}, {len(income_transactions)} income entries totaling ₹{total_income}"
                
                prompt = f"""
                You are SheFin, an AI financial advisor for women in India. Provide specific, actionable advice.
                
                {user_context}
                {transaction_summary}
                
                User Question: {query}
                
                Please provide personalized financial advice that is:
                1. Specific to her situation
                2. Culturally appropriate for Indian women
                3. Action-oriented with clear next steps
                4. Encouraging and supportive
                """
                
                ai_response = get_financial_advice(prompt)
                if ai_response and len(ai_response.strip()) > 20:
                    return ai_response
                    
            except Exception as e:
                print(f"Gemini AI error: {e}")
        
        # Fallback to intelligent responses
        if language == 'english':
            return self.realtime_ai.analyze_query(query, user_data, transactions)
        else:
            return self.fallback_advisor.get_response(query, user_data, language)

    def get_budget_insights(self, transactions, user_data, language='english'):
        """Generate budget insights"""
        if not transactions:
            return translate_text("Add some transactions to get personalized budget insights!", language)
        
        # Quick analysis
        expense_transactions = [t for t in transactions if t['type'] == 'expense']
        total_expenses = sum([t['amount'] for t in expense_transactions])
        
        # Category analysis
        category_spending = {}
        for transaction in expense_transactions:
            category = transaction['category']
            category_spending[category] = category_spending.get(category, 0) + transaction['amount']
        
        if category_spending:
            top_category = max(category_spending.keys(), key=lambda k: category_spending[k])
        else:
            top_category = "Food"
        
        if self.use_ai and language == 'english':
            try:
                transactions_data = f"Total expenses: ₹{total_expenses}, Top spending category: {top_category}, Category breakdown: {category_spending}"
                user_context = f"Monthly income: ₹{user_data['monthly_income']}, Age: {user_data['age']}, Name: {user_data['name']}"
                
                ai_response = analyze_budget(transactions_data, user_context)
                if ai_response and len(ai_response.strip()) > 20:
                    return ai_response
                    
            except Exception as e:
                print(f"Gemini AI budget analysis error: {e}")
        
        # Fallback insights
        if total_expenses > user_data['monthly_income'] * 0.8:
            return translate_text("Your expenses are quite high. Consider the 50-30-20 rule: 50% needs, 30% wants, 20% savings.", language)
        else:
            return translate_text(f"Good job managing expenses! Your top spending category is {top_category}. Try to increase your savings rate for better financial health.", language)

    def get_budgeting_tips(self, language='english'):
        """Get general budgeting tips"""
        return self.fallback_advisor.get_budget_tips(language)

    def get_investment_basics(self, language='english'):
        """Get investment basics"""
        return self.fallback_advisor.get_investment_basics(language)

    def get_government_schemes_info(self, language='english'):
        """Get government schemes information"""
        return self.fallback_advisor.get_government_schemes_info(language)

    def get_investment_education(self, topic, language='english'):
        """Get educational content for specific investment topics"""
        education_content = {
            'sip': translate_text("SIP (Systematic Investment Plan) allows you to invest a fixed amount regularly in mutual funds. Benefits: Rupee cost averaging, Power of compounding, Disciplined investing, Low minimum investment.", language),
            'mutual_funds': translate_text("Mutual funds pool money from multiple investors to invest in stocks, bonds, or other securities. Types: Equity funds (high risk/return), Debt funds (low risk/return), Hybrid funds (balanced).", language),
            'stocks': translate_text("Stocks represent ownership in companies. Key concepts: Dividends (profit sharing), Capital appreciation (price increase), Market volatility, Long-term wealth creation potential.", language),
            'ppf': translate_text("Public Provident Fund (PPF) is a 15-year investment scheme with tax benefits. Features: Tax-free returns, Currently ~7.1% interest, Lock-in period of 15 years, Maximum investment ₹1.5 lakh per year.", language),
            'gold': translate_text("Gold investments in India: Physical gold, Gold ETFs, Gold mutual funds, Digital gold. Benefits: Inflation hedge, Portfolio diversification, Cultural significance in India.", language)
        }
        
        return education_content.get(topic.lower(), translate_text("Learn about different investment options to build wealth systematically. Start with understanding your risk tolerance and investment goals.", language))

    def get_investment_recommendations(self, user_data, risk_tolerance, investment_horizon, amount, language='english'):
        """Get personalized investment recommendations"""
        if self.use_ai and language == 'english':
            try:
                user_profile = f"Age: {user_data['age']}, Income: ₹{user_data['monthly_income']}, Risk tolerance: {risk_tolerance}, Investment horizon: {investment_horizon}, Amount: ₹{amount}"
                ai_response = get_investment_guidance(user_profile, f"Investment of ₹{amount} for {investment_horizon}")
                if ai_response and len(ai_response.strip()) > 20:
                    return ai_response
            except Exception as e:
                print(f"Gemini AI investment recommendation error: {e}")
        
        # Fallback recommendations
        recommendations = []
        if risk_tolerance == "Conservative":
            recommendations.extend([
                "PPF (Public Provident Fund) - 15-year lock-in, tax-free returns",
                "NSC (National Savings Certificate) - 5-year term, fixed returns",
                "Fixed Deposits - Safe, predictable returns"
            ])
        elif risk_tolerance == "Moderate":
            recommendations.extend([
                "Balanced Mutual Funds - Mix of equity and debt",
                "SIP in Diversified Equity Funds - Long-term wealth creation",
                "Gold ETFs - Inflation hedge"
            ])
        else:  # Aggressive
            recommendations.extend([
                "Equity Mutual Funds - High growth potential",
                "Direct Stock Investment - Individual company stocks",
                "ELSS Funds - Tax saving with equity exposure"
            ])
            
        return translate_text(f"Investment recommendations for {risk_tolerance.lower()} risk profile:\n" + "\n".join([f"• {rec}" for rec in recommendations]), language)

    def get_scheme_information(self, query, user_data, language='english'):
        """Get information about government schemes"""
        if self.use_ai and language == 'english':
            try:
                user_context = f"Age: {user_data['age']}, Income: ₹{user_data['monthly_income']}, Location: India"
                ai_response = get_government_scheme_advice(user_context)
                if ai_response and len(ai_response.strip()) > 20:
                    return ai_response
            except Exception as e:
                print(f"Gemini AI scheme information error: {e}")
        
        return self.fallback_advisor.get_government_schemes_info(language)

class CreditScorer:
    def calculate_score(self, user_data, transactions):
        """Calculate simulated credit score"""
        base_score = 650
        
        # Age factor (stability)
        if user_data['age'] >= 25:
            base_score += 30
        elif user_data['age'] >= 21:
            base_score += 15
            
        # Income factor
        monthly_income = user_data['monthly_income']
        if monthly_income >= 50000:
            base_score += 50
        elif monthly_income >= 25000:
            base_score += 30
        elif monthly_income >= 15000:
            base_score += 20
            
        # Transaction behavior
        spending_ratio = 0.7  # Default spending ratio
        if transactions:
            expense_transactions = [t for t in transactions if t['type'] == 'expense']
            total_expenses = sum([t['amount'] for t in expense_transactions])
            
            # Spending ratio
            spending_ratio = total_expenses / monthly_income if monthly_income > 0 else 1
            if spending_ratio < 0.6:
                base_score += 40
            elif spending_ratio < 0.8:
                base_score += 20
            else:
                base_score -= 20
                
        # Cap at 850
        final_score = min(850, max(300, base_score))
        
        # Determine grade and range
        if final_score >= 750:
            grade = "Excellent"
            score_range = "750-850"
        elif final_score >= 700:
            grade = "Good"
            score_range = "700-749"
        elif final_score >= 650:
            grade = "Fair"
            score_range = "650-699"
        else:
            grade = "Poor"
            score_range = "300-649"
            
        # Calculate factors breakdown
        factors = {
            "Payment History": min(100, (final_score - 300) // 5),
            "Income Stability": min(100, monthly_income // 1000),
            "Spending Behavior": max(0, 100 - int(spending_ratio * 100)),
            "Age Factor": min(100, user_data['age'] * 2)
        }
        
        return {
            'score': final_score,
            'grade': grade,
            'range': score_range,
            'factors': factors
        }

    def get_improvement_tips(self, credit_score, language='english'):
        """Get tips to improve credit score"""
        # Handle both old format (number) and new format (dict)
        score = credit_score['score'] if isinstance(credit_score, dict) else credit_score
        
        tips = []
        if score >= 750:
            tips = [
                translate_text("Excellent credit score! Maintain your good financial habits.", language),
                translate_text("You qualify for the best interest rates on loans and credit cards.", language),
                translate_text("Continue monitoring your credit report regularly.", language)
            ]
        elif score >= 700:
            tips = [
                translate_text("Good credit score! Keep credit utilization below 30%.", language),
                translate_text("Pay all bills on time to maintain your score.", language),
                translate_text("Maintain older credit accounts for better credit history.", language)
            ]
        elif score >= 650:
            tips = [
                translate_text("Fair credit score. Pay down existing debt.", language),
                translate_text("Never miss payment due dates.", language),
                translate_text("Don't apply for too many loans/cards at once.", language)
            ]
        else:
            tips = [
                translate_text("Focus on paying all bills on time.", language),
                translate_text("Reduce your debt-to-income ratio.", language),
                translate_text("Build a longer credit history.", language),
                translate_text("Avoid loan defaults and late payments.", language)
            ]
        return tips

class GoalPlanner:
    def __init__(self):
        self.fallback_advisor = FallbackFinancialAdvisor()
        # Check if Gemini AI is available
        self.use_ai = bool(os.getenv("GEMINI_API_KEY"))

    def create_action_plan(self, goal_name, target_amount, target_date, user_data, transactions, language='english'):
        """Create action plan for financial goals"""
        today = datetime.now()
        target_datetime = datetime.combine(target_date, datetime.min.time())
        months_to_goal = max(1, (target_datetime - today).days // 30)
        
        monthly_savings_required = target_amount / months_to_goal
        current_income = user_data['monthly_income']
        
        # Calculate current expenses
        if transactions:
            expense_transactions = [t for t in transactions if t['type'] == 'expense']
            current_expenses = sum([t['amount'] for t in expense_transactions])
        else:
            current_expenses = current_income * 0.7  # Assume 70% expenses
            
        available_for_savings = current_income - current_expenses
        
        if monthly_savings_required <= available_for_savings:
            difficulty = "achievable"
        elif monthly_savings_required <= available_for_savings * 1.5:
            difficulty = "challenging"
        else:
            difficulty = "very challenging"
            
        plan = f"""
        **Goal: {goal_name}**
        **Target: ₹{format_currency(target_amount)} by {target_date}**
        
        **Action Plan:**
        • Monthly savings needed: ₹{format_currency(monthly_savings_required)}
        • Goal difficulty: {difficulty}
        • Timeline: {months_to_goal} months
        
        **Recommendations:**
        """
        
        if difficulty == "achievable":
            plan += f"""
        ✅ Great! This goal is achievable with your current income.
        • Set up automatic transfer of ₹{format_currency(monthly_savings_required)} monthly
        • Consider SIP in mutual funds for better returns
        • Track progress monthly
        """
        elif difficulty == "challenging":
            plan += f"""
        ⚠️ This goal requires some effort but is doable.
        • Reduce expenses by ₹{format_currency(monthly_savings_required - available_for_savings)}
        • Look for additional income sources
        • Consider extending timeline by 6 months
        """
        else:
            plan += f"""
        🔴 This goal needs significant changes to achieve.
        • Consider extending timeline to {months_to_goal + 12} months
        • Explore side income opportunities
        • Review and reduce major expenses
        • Start with smaller, achievable milestones
        """
        
        return translate_text(plan, language)

    def get_goal_recommendations(self, goal, language='english'):
        """Get recommendations for achieving a goal"""
        goal_type = goal.get('category', 'General')
        target_amount = goal.get('target_amount', 0)
        
        recommendations = {
            'Emergency Fund': f"Build your emergency fund gradually. Aim for 6 months of expenses (₹{format_currency(target_amount)}). Keep it in liquid funds or savings account for easy access.",
            'Child Education': f"Education costs are rising at 10-12% annually. Consider starting early with equity mutual funds through SIP. Sukanya Samriddhi Yojana is excellent for girl child education.",
            'House Purchase': f"Home buying requires 20% down payment plus registration costs. Start with diversified equity funds for long-term wealth creation. Consider home loan pre-approval.",
            'Retirement': f"Retirement planning needs 25-30 times your annual expenses. Start early, use EPF, PPF, and equity mutual funds. The power of compounding works best over 20+ years.",
            'Marriage': f"Wedding expenses can be significant. Plan 12-18 months ahead. Use debt funds for short-term goals, equity funds for longer timelines.",
            'Business': f"Business goals need careful planning. Keep some money liquid, research your market, and consider taking a business loan for remaining capital.",
            'Healthcare': f"Health expenses are unpredictable. Maintain health insurance plus a separate medical emergency fund. Consider investing in liquid or ultra-short-term funds."
        }
        
        default_rec = f"Set up automatic monthly transfers towards your goal of ₹{format_currency(target_amount)}. Review and adjust monthly based on your progress."
        
        return translate_text(recommendations.get(goal_type, default_rec), language)