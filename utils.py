def format_currency(amount):
    """Format currency in Indian format"""
    if amount >= 10000000:  # 1 crore
        return f"{amount/10000000:.1f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"{amount/100000:.1f}L"
    elif amount >= 1000:  # 1 thousand
        return f"{amount/1000:.1f}K"
    else:
        return f"{amount:,.0f}"

def get_user_language():
    """Get user's preferred language"""
    # This would typically come from user preferences
    return 'english'

def translate_text(text, language):
    """Simple translation function"""
    from translations import TRANSLATIONS
    
    if language == 'english':
        return text
    
    # Look up translation
    if text in TRANSLATIONS and language in TRANSLATIONS[text]:
        return TRANSLATIONS[text][language]
    
    return text  # Return original if translation not found

def validate_email(email):
    """Validate email address"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_age_from_dob(date_of_birth):
    """Calculate age from date of birth"""
    from datetime import datetime
    today = datetime.now().date()
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_financial_year_dates():
    """Get current financial year start and end dates"""
    from datetime import datetime, date
    
    current_date = datetime.now().date()
    
    if current_date.month >= 4:  # April to March
        fy_start = date(current_date.year, 4, 1)
        fy_end = date(current_date.year + 1, 3, 31)
    else:
        fy_start = date(current_date.year - 1, 4, 1)
        fy_end = date(current_date.year, 3, 31)
    
    return fy_start, fy_end

def calculate_savings_rate(income, expenses):
    """Calculate savings rate percentage"""
    if income <= 0:
        return 0
    return ((income - expenses) / income) * 100

def get_expense_category_icon(category):
    """Get emoji icon for expense category"""
    icons = {
        'Food': '🍽️',
        'Transportation': '🚗',
        'Healthcare': '🏥',
        'Education': '📚',
        'Shopping': '🛍️',
        'Utilities': '⚡',
        'Entertainment': '🎬',
        'Other': '📦',
        'Salary': '💰',
        'Business': '💼',
        'Investment Returns': '📈',
        'Government Benefits': '🏛️'
    }
    return icons.get(category, '📦')

def format_indian_currency(amount):
    """Format currency in Indian numbering system"""
    if amount >= 0:
        return f"₹{amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    else:
        return f"-₹{abs(amount):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def get_month_name(month_number, language='english'):
    """Get month name in specified language"""
    months = {
        'english': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        'hindi': [
            'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
            'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'
        ],
        'tamil': [
            'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
            'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
        ]
    }
    
    if language in months and 1 <= month_number <= 12:
        return months[language][month_number - 1]
    return months['english'][month_number - 1] if 1 <= month_number <= 12 else 'Unknown'

def is_working_day():
    """Check if today is a working day (Monday to Friday)"""
    from datetime import datetime
    return datetime.now().weekday() < 5

def get_next_working_day():
    """Get the next working day"""
    from datetime import datetime, timedelta
    
    current_date = datetime.now().date()
    days_ahead = 1
    
    while (current_date + timedelta(days=days_ahead)).weekday() >= 5:  # Saturday = 5, Sunday = 6
        days_ahead += 1
    
    return current_date + timedelta(days=days_ahead)

def calculate_inflation_adjusted_amount(amount, years, inflation_rate=6):
    """Calculate inflation adjusted amount"""
    return amount * (1 + inflation_rate / 100) ** years

def get_risk_level_description(risk_level, language='english'):
    """Get risk level description"""
    descriptions = {
        'english': {
            'Conservative': 'Low risk, stable returns. Suitable for capital preservation.',
            'Moderate': 'Balanced risk and return. Good for medium-term goals.',
            'Aggressive': 'High risk, high potential returns. For long-term wealth creation.'
        },
        'hindi': {
            'Conservative': 'कम जोखिम, स्थिर रिटर्न। पूंजी संरक्षण के लिए उपयुक्त।',
            'Moderate': 'संतुलित जोखिम और रिटर्न। मध्यम अवधि के लक्ष्यों के लिए अच्छा।',
            'Aggressive': 'उच्च जोखिम, उच्च संभावित रिटर्न। दीर्घकालिक संपत्ति निर्माण के लिए।'
        },
        'tamil': {
            'Conservative': 'குறைந்த ஆபத்து, நிலையான வருமானம். மூலதன பாதுகாப்பிற்கு ஏற்றது.',
            'Moderate': 'சமநிலையான ஆபத்து மற்றும் வருமானம். நடுத்தர கால இலக்குகளுக்கு நல்லது.',
            'Aggressive': 'அதிக ஆபத்து, அதிக சாத்தியமான வருமானம். நீண்ட கால செல்வ உருவாக்கத்திற்கு.'
        }
    }
    
    return descriptions.get(language, descriptions['english']).get(risk_level, '')
