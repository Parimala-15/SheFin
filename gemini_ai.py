import os
import logging
from dotenv import load_dotenv
import os


def get_financial_advice(prompt: str) -> str:
    """Get financial advice from Gemini AI"""
    try:
        # Import here to avoid issues if package not available
        import google.generativeai as genai
        load_dotenv()  # Loads variables from .env
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "AI service temporarily unavailable. Please check your API configuration."
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return response.text or "I'm here to help with your financial questions!"
    except ImportError:
        logging.error("Google Generative AI package not available")
        return "AI service temporarily unavailable. Using fallback responses."
    except Exception as e:
        logging.error(f"Gemini AI error: {e}")
        return "I'm currently having trouble connecting to provide personalized advice. Please try again."


def analyze_budget(transactions_data: str, user_context: str) -> str:
    """Analyze budget and provide insights"""
    prompt = f"""
    You are SheFin, an AI financial advisor for women in India. Analyze this financial data and provide specific, actionable advice.
    
    User Context: {user_context}
    Transaction Data: {transactions_data}
    
    Please provide:
    1. Budget analysis with key insights
    2. 3 specific recommendations for improvement
    3. Government schemes that might be relevant
    4. Investment suggestions appropriate for Indian women
    
    Keep the response encouraging and practical.
    """
    
    return get_financial_advice(prompt)


def get_investment_guidance(user_profile: str, goal: str) -> str:
    """Get investment guidance for specific goals"""
    prompt = f"""
    You are SheFin, an AI financial advisor specializing in helping Indian women achieve their financial goals.
    
    User Profile: {user_profile}
    Financial Goal: {goal}
    
    Provide specific investment advice including:
    1. Suitable investment options (SIP, PPF, mutual funds, etc.)
    2. Risk assessment and recommendations
    3. Timeline and amount suggestions
    4. Government schemes and tax benefits
    5. Step-by-step action plan
    
    Focus on options available in India and be encouraging about women's financial independence.
    """
    
    return get_financial_advice(prompt)


def get_government_scheme_advice(user_data: str) -> str:
    """Get personalized government scheme recommendations"""
    prompt = f"""
    You are SheFin, an AI advisor helping Indian women access government financial schemes.
    
    User Information: {user_data}
    
    Recommend relevant government schemes such as:
    - Sukanya Samriddhi Yojana
    - Pradhan Mantri Jan Dhan Yojana  
    - Atal Pension Yojana
    - Pradhan Mantri Mudra Yojana
    - Mahila Shakti Kendra programs
    
    For each relevant scheme, provide:
    1. Eligibility criteria
    2. Benefits and returns
    3. How to apply
    4. Required documents
    
    Be specific about which schemes best match this user's profile.
    """
    
    return get_financial_advice(prompt)