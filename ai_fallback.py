"""
Fallback AI responses when OpenAI API is unavailable
Provides pre-written financial advice responses for common queries
"""

import random
from translations import translate_text

class FallbackFinancialAdvisor:
    def __init__(self):
        self.responses = {
            'budgeting': {
                'english': [
                    "Here are 5 practical budgeting tips for you:\n\n1. Follow the 50/30/20 rule - 50% for needs, 30% for wants, 20% for savings\n2. Track every expense for at least a month to understand your spending patterns\n3. Create separate savings accounts for different goals\n4. Use cash envelopes for discretionary spending categories\n5. Review and adjust your budget monthly based on actual spending",
                    
                    "Smart budgeting strategies:\n\n1. Pay yourself first - save before spending\n2. Use the zero-based budgeting method\n3. Automate your savings and bill payments\n4. Cut unnecessary subscriptions and memberships\n5. Cook at home more often to reduce food expenses\n6. Compare prices before making purchases"
                ],
                'hindi': [
                    "आपके लिए 5 व्यावहारिक बजटिंग टिप्स:\n\n1. 50/30/20 नियम का पालन करें - 50% जरूरतों के लिए, 30% इच्छाओं के लिए, 20% बचत के लिए\n2. अपने खर्च के पैटर्न को समझने के लिए कम से कम एक महीने तक हर खर्च को ट्रैक करें\n3. विभिन्न लक्ष्यों के लिए अलग बचत खाते बनाएं\n4. विवेकाधीन खर्च श्रेणियों के लिए कैश लिफाफे का उपयोग करें\n5. वास्तविक खर्च के आधार पर मासिक रूप से अपने बजट की समीक्षा और समायोजन करें"
                ],
                'tamil': [
                    "உங்களுக்கான 5 நடைமுறை பட்ஜெட் குறிப்புகள்:\n\n1. 50/30/20 விதியைப் பின்பற்றுங்கள் - 50% தேவைகளுக்கு, 30% விருப்பங்களுக்கு, 20% சேமிப்புக்கு\n2. உங்கள் செலவு முறைகளைப் புரிந்துகொள்ள குறைந்தது ஒரு மாதம் ஒவ்வொரு செலவையும் கண்காணியுங்கள்\n3. வெவ்வேறு இலக்குகளுக்கு தனி சேமிப்பு கணக்குகளை உருவாக்குங்கள்\n4. விருப்பப்படி செலவு வகைகளுக்கு பண உறைகளைப் பயன்படுத்துங்கள்\n5. உண்மையான செலவுகளின் அடிப்படையில் மாதந்தோறும் உங்கள் பட்ஜெட்டை மதிப்பாய்வு செய்து சரிசெய்யுங்கள்"
                ]
            },
            
            'investment': {
                'english': [
                    "Investment basics for beginners:\n\n1. Start with SIP (Systematic Investment Plan) in diversified mutual funds\n2. Begin with just ₹500-1000 per month\n3. Focus on large-cap equity funds for stability\n4. Consider ELSS funds for tax savings under Section 80C\n5. Don't try to time the market - invest regularly\n6. Review your portfolio annually, not daily",
                    
                    "Safe investment options for women:\n\n1. Sukanya Samriddhi Yojana for daughters (7.6% returns)\n2. PPF (Public Provident Fund) - 15-year lock-in, tax-free\n3. Fixed Deposits for emergency funds\n4. Gold ETFs for inflation protection\n5. Balanced mutual funds for moderate risk\n6. National Savings Certificate (NSC) for tax benefits"
                ],
                'hindi': [
                    "शुरुआती लोगों के लिए निवेश की मूल बातें:\n\n1. विविधीकृत म्यूचुअल फंड में एसआईपी (व्यवस्थित निवेश योजना) से शुरुआत करें\n2. महीने में सिर्फ ₹500-1000 से शुरू करें\n3. स्थिरता के लिए लार्ज-कैप इक्विटी फंड पर ध्यान दें\n4. धारा 80सी के तहत कर बचत के लिए ईएलएसएस फंड पर विचार करें\n5. बाजार का समय निकालने की कोशिश न करें - नियमित रूप से निवेश करें\n6. अपने पोर्टफोलियो की सालाना समीक्षा करें, रोजाना नहीं"
                ],
                'tamil': [
                    "ஆரம்பநிலைக்கான முதலீட்டு அடிப்படைகள்:\n\n1. பல்வகைப்படுத்தப்பட்ட மியூச்சுவல் ஃபண்டுகளில் SIP (முறையான முதலீட்டுத் திட்டம்) ஆரம்பியுங்கள்\n2. மாதத்திற்கு வெறும் ₹500-1000 இல் தொடங்குங்கள்\n3. நிலைத்தன்மைக்காக பெரிய-கேப் ஈக்விட்டி ஃபண்டுகளில் கவனம் செலுத்துங்கள்\n4. பிரிவு 80சி கீழ் வரி சேமிப்பிற்காக ELSS ஃபண்டுகளைக் கருத்தில் கொள்ளுங்கள்\n5. சந்தையின் நேரத்தைக் கணிக்க முயற்சிக்காதீர்கள் - தொடர்ந்து முதலீடு செய்யுங்கள்\n6. உங்கள் போர்ட்ஃபோலியோவை ஆண்டுதோறும் மதிப்பாய்வு செய்யுங்கள், தினமும் அல்ல"
                ]
            },
            
            'savings': {
                'english': [
                    "Smart saving strategies:\n\n1. Open a high-yield savings account\n2. Use automatic transfers to savings\n3. Save all windfalls (bonuses, gifts) immediately\n4. Reduce unnecessary subscriptions and memberships\n5. Try the 52-week savings challenge\n6. Save before you spend, not after",
                    
                    "Emergency fund tips:\n\n1. Aim for 6-12 months of expenses\n2. Keep it in a separate high-yield account\n3. Don't invest emergency funds in risky assets\n4. Build it gradually - even ₹100/month helps\n5. Use it only for true emergencies\n6. Replenish immediately after use"
                ],
                'hindi': [
                    "स्मार्ट बचत रणनीतियां:\n\n1. एक हाई-यील्ड सेविंग्स अकाउंट खोलें\n2. बचत के लिए ऑटोमैटिक ट्रांसफर का उपयोग करें\n3. सभी अप्रत्याशित आय (बोनस, उपहार) तुरंत बचाएं\n4. अनावश्यक सब्सक्रिप्शन और सदस्यता कम करें\n5. 52-सप्ताह की बचत चुनौती आजमाएं\n6. खर्च करने के बाद नहीं, पहले बचत करें"
                ],
                'tamil': [
                    "புத்திசாலித்தனமான சேமிப்பு உத்திகள்:\n\n1. அதிக வருமானம் தரும் சேமிப்பு கணக்கு திறக்கவும்\n2. சேமிப்புக்கு தானியங்கி பரிமாற்றங்களைப் பயன்படுத்துங்கள்\n3. எல்லா எதிர்பாராத வருமானத்தையும் (போனஸ், பரிசுகள்) உடனே சேமிக்கவும்\n4. தேவையற்ற சந்தாக்கள் மற்றும் உறுப்பினர்களைக் குறைக்கவும்\n5. 52-வார சேமிப்பு சவாலை முயற்சிக்கவும்\n6. செலவு செய்த பிறகு அல்ல, முதலில் சேமிக்கவும்"
                ]
            },
            
            'government_schemes': {
                'english': [
                    "Important government schemes for women:\n\n1. Sukanya Samriddhi Yojana - 7.6% for girl child education\n2. Pradhan Mantri Jan Dhan Yojana - Zero balance banking\n3. Atal Pension Yojana - Guaranteed pension after 60\n4. Mudra Yojana - Business loans up to ₹10 lakh\n5. Stand Up India - Loans for women entrepreneurs\n6. Mahila Shakti Kendra - Skill development programs",
                    
                    "How to apply for schemes:\n\n1. Visit your nearest bank branch\n2. Carry required documents (Aadhaar, PAN, photos)\n3. Fill application forms carefully\n4. Submit with initial deposit if required\n5. Follow up on application status\n6. Contact bank officials for help"
                ],
                'hindi': [
                    "महिलाओं के लिए महत्वपूर्ण सरकारी योजनाएं:\n\n1. सुकन्या समृद्धि योजना - बालिका शिक्षा के लिए 7.6%\n2. प्रधानमंत्री जन धन योजना - जीरो बैलेंस बैंकिंग\n3. अटल पेंशन योजना - 60 के बाद गारंटीड पेंशन\n4. मुद्रा योजना - ₹10 लाख तक बिजनेस लोन\n5. स्टैंड अप इंडिया - महिला उद्यमियों के लिए लोन\n6. महिला शक्ति केंद्र - कौशल विकास कार्यक्रम"
                ],
                'tamil': [
                    "பெண்களுக்கான முக்கியமான அரசாங்க திட்டங்கள்:\n\n1. சுகன்யா சம்ரித்தி யோஜனா - பெண் குழந்தை கல்விக்கு 7.6%\n2. பிரதான் மந்திரி ஜன் தன் யோஜனா - பூஜ்ஜிய இருப்பு வங்கி\n3. அடல் ஓய்வூதிய யோஜனா - 60க்கு பிறகு உத்தரவாத ஓய்வூதியம்\n4. முத்ரா யோஜனா - ₹10 லட்சம் வரை வணிக கடன்\n5. ஸ்டாண்ட் அப் இந்தியா - பெண் தொழில்முனைவோருக்கான கடன்\n6. மகிளா சக்தி கேந்திரா - திறன் மேம்பாட்டு திட்டங்கள்"
                ]
            }
        }
    
    def get_response(self, query, user_data=None, language='english'):
        """Get fallback response based on query keywords"""
        query_lower = query.lower()
        
        # Detect query type based on keywords
        if any(word in query_lower for word in ['budget', 'budgeting', 'expense', 'spending', 'money management']):
            category = 'budgeting'
        elif any(word in query_lower for word in ['invest', 'investment', 'mutual fund', 'sip', 'share', 'stock']):
            category = 'investment'
        elif any(word in query_lower for word in ['save', 'saving', 'emergency fund', 'bank account']):
            category = 'savings'
        elif any(word in query_lower for word in ['government', 'scheme', 'yojana', 'loan', 'subsidy']):
            category = 'government_schemes'
        else:
            # Default general advice
            category = 'budgeting'
        
        # Get appropriate response
        if category in self.responses and language in self.responses[category]:
            responses = self.responses[category][language]
            response = random.choice(responses)
            
            # Add personalized touch if user data available
            if user_data:
                name = user_data.get('name', 'there')
                response = f"Hello {name}! {response}"
            
            return response
        
        # Fallback response if no match
        return self.get_general_advice(language)
    
    def get_general_advice(self, language='english'):
        """General financial advice when query doesn't match categories"""
        advice = {
            'english': "Here's some general financial advice:\n\n1. Track your income and expenses monthly\n2. Build an emergency fund covering 6 months of expenses\n3. Start investing early, even with small amounts\n4. Avoid high-interest debt like credit cards\n5. Learn about government schemes for women\n6. Consider insurance for financial protection\n\nFeel free to ask more specific questions about budgeting, investments, or savings!",
            
            'hindi': "यहाँ कुछ सामान्य वित्तीय सलाह है:\n\n1. अपनी आय और व्यय को मासिक रूप से ट्रैक करें\n2. 6 महीने के खर्च को कवर करने वाला इमरजेंसी फंड बनाएं\n3. जल्दी निवेश शुरू करें, छोटी राशि से भी\n4. क्रेडिट कार्ड जैसे उच्च-ब्याज ऋण से बचें\n5. महिलाओं के लिए सरकारी योजनाओं के बारे में जानें\n6. वित्तीय सुरक्षा के लिए बीमा पर विचार करें\n\nबजटिंग, निवेश या बचत के बारे में और विशिष्ट प्रश्न पूछने में संकोच न करें!",
            
            'tamil': "இதோ சில பொதுவான நிதி ஆலோசனைகள்:\n\n1. உங்கள் வருமானம் மற்றும் செலவுகளை மாதந்தோறும் கண்காணியுங்கள்\n2. 6 மாத செலவுகளை உள்ளடக்கிய அவசரகால நிதியை உருவாக்குங்கள்\n3. சிறிய தொகையிலும் சீக்கிரம் முதலீடு செய்யத் தொடங்குங்கள்\n4. கிரெடிட் கார்டு போன்ற அதிக வட்டி கடன்களை தவிர்க்கவும்\n5. பெண்களுக்கான அரசாங்க திட்டங்களைப் பற்றி அறியுங்கள்\n6. நிதி பாதுகாப்பிற்கான காப்பீட்டைக் கருத்தில் கொள்ளுங்கள்\n\nபட்ஜெட், முதலீடு அல்லது சேமிப்பு பற்றிய குறிப்பிட்ட கேள்விகளைக் கேட்க தயங்காதீர்கள்!"
        }
        
        return advice.get(language, advice['english'])
    
    def get_budget_tips(self, language='english'):
        """Get specific budget tips"""
        if 'budgeting' in self.responses and language in self.responses['budgeting']:
            return random.choice(self.responses['budgeting'][language])
        return self.get_general_advice(language)
    
    def get_investment_basics(self, language='english'):
        """Get investment basics"""
        if 'investment' in self.responses and language in self.responses['investment']:
            return random.choice(self.responses['investment'][language])
        return self.get_general_advice(language)
    
    def get_government_schemes_info(self, language='english'):
        """Get government schemes information"""
        if 'government_schemes' in self.responses and language in self.responses['government_schemes']:
            return random.choice(self.responses['government_schemes'][language])
        return self.get_general_advice(language)