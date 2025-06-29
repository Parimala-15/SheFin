def get_schemes_for_user(user_data):
    """Get government schemes relevant to user profile"""
    
    schemes = []
    age = user_data['age']
    monthly_income = user_data['monthly_income']
    
    # Sukanya Samriddhi Yojana
    if age <= 45:  # Can open account for girl child up to 10 years
        schemes.append({
            'name': 'Sukanya Samriddhi Yojana',
            'description': 'A savings scheme for the girl child offering attractive interest rates and tax benefits.',
            'benefits': 'Current interest rate: 7.6% p.a., Tax deduction under 80C, Tax-free maturity',
            'eligibility': 'For girl child below 10 years of age',
            'how_to_apply': 'Visit any authorized bank or post office with required documents'
        })
    
    # Pradhan Mantri Jan Dhan Yojana
    schemes.append({
        'name': 'Pradhan Mantri Jan Dhan Yojana (PMJDY)',
        'description': 'Financial inclusion program providing basic banking services.',
        'benefits': 'Zero balance account, RuPay debit card, Accident insurance of ₹2 lakh',
        'eligibility': 'All Indian citizens',
        'how_to_apply': 'Visit any participating bank branch with Aadhaar card'
    })
    
    # Atal Pension Yojana
    if 18 <= age <= 40:
        schemes.append({
            'name': 'Atal Pension Yojana (APY)',
            'description': 'Pension scheme providing guaranteed monthly pension after 60 years.',
            'benefits': 'Guaranteed pension of ₹1,000 to ₹5,000 per month, Government co-contribution',
            'eligibility': 'Age 18-40 years with bank account',
            'how_to_apply': 'Apply through your bank or online'
        })
    
    # Pradhan Mantri Mudra Yojana
    if monthly_income <= 100000:  # For micro-entrepreneurs
        schemes.append({
            'name': 'Pradhan Mantri Mudra Yojana',
            'description': 'Micro-credit scheme for small businesses and entrepreneurs.',
            'benefits': 'Loans up to ₹10 lakh without collateral, Special focus on women entrepreneurs',
            'eligibility': 'Non-corporate, non-farm small/micro enterprises',
            'how_to_apply': 'Apply at banks, NBFCs, or MFIs'
        })
    
    # Mahila Shakti Kendra
    schemes.append({
        'name': 'Mahila Shakti Kendra',
        'description': 'Community participation and decision-making for women empowerment.',
        'benefits': 'Skill development, Employment support, Digital literacy',
        'eligibility': 'All women, especially in rural areas',
        'how_to_apply': 'Contact local Anganwadi centers or district administration'
    })
    
    # Stand Up India
    if 18 <= age <= 65:
        schemes.append({
            'name': 'Stand Up India',
            'description': 'Facilitating bank loans for SC/ST and women entrepreneurs.',
            'benefits': 'Loans between ₹10 lakh to ₹1 crore, Lower interest rates',
            'eligibility': 'Women entrepreneurs for greenfield enterprises',
            'how_to_apply': 'Apply through scheduled commercial banks'
        })
    
    # Deen Dayal Upadhyaya Grameen Kaushalya Yojana
    if age <= 35 and monthly_income <= 30000:
        schemes.append({
            'name': 'Deen Dayal Upadhyaya Grameen Kaushalya Yojana',
            'description': 'Skill development program for rural youth.',
            'benefits': 'Free skill training, Placement assistance, Special focus on women',
            'eligibility': 'Poor rural households, Age 15-35 years',
            'how_to_apply': 'Register through official portal or contact implementing agencies'
        })
    
    # Beti Bachao Beti Padhao
    if age <= 50:  # Can benefit from awareness and education components
        schemes.append({
            'name': 'Beti Bachao Beti Padhao',
            'description': 'Campaign for girl child protection and education.',
            'benefits': 'Educational scholarships, Healthcare support, Awareness programs',
            'eligibility': 'Girl children and their families',
            'how_to_apply': 'Contact district administration or education department'
        })
    
    # Maternity Benefit Programme
    if 18 <= age <= 45:
        schemes.append({
            'name': 'Pradhan Mantri Matru Vandana Yojana',
            'description': 'Maternity benefit programme for pregnant and lactating mothers.',
            'benefits': 'Cash incentive of ₹5,000 for first live birth',
            'eligibility': 'Pregnant and lactating mothers (excluding government employees)',
            'how_to_apply': 'Register at Anganwadi centers or health facilities'
        })
    
    # National Pension System
    if 18 <= age <= 65:
        schemes.append({
            'name': 'National Pension System (NPS)',
            'description': 'Voluntary pension system with tax benefits.',
            'benefits': 'Tax deduction up to ₹2 lakh, Market-linked returns, Flexible withdrawal',
            'eligibility': 'All Indian citizens aged 18-65 years',
            'how_to_apply': 'Open account through banks, online platforms, or POP-SP'
        })
    
    return schemes

def get_scheme_details(scheme_name):
    """Get detailed information about a specific scheme"""
    
    scheme_details = {
        'Sukanya Samriddhi Yojana': {
            'full_description': 'Sukanya Samriddhi Yojana is a government savings scheme designed to meet the education and marriage expenses of a girl child. It offers one of the highest interest rates among government schemes.',
            'interest_rate': '7.6% per annum (as of 2024)',
            'minimum_deposit': '₹250 per year',
            'maximum_deposit': '₹1.5 lakh per year',
            'maturity_period': '21 years from account opening',
            'tax_benefits': 'Deposit, interest, and maturity amount are all tax-free (EEE status)',
            'documents_required': [
                'Birth certificate of girl child',
                'Identity proof of parent/guardian',
                'Address proof',
                'Passport size photographs'
            ],
            'partial_withdrawal': 'Allowed after girl attains 18 years for education purposes (up to 50% of balance)'
        },
        
        'Pradhan Mantri Jan Dhan Yojana (PMJDY)': {
            'full_description': 'PMJDY is a financial inclusion program that aims to provide affordable access to financial services like banking, savings, credit, insurance, and pension.',
            'account_features': [
                'Zero minimum balance',
                'RuPay debit card',
                'Mobile banking facility',
                'Overdraft facility up to ₹10,000'
            ],
            'insurance_benefits': [
                'Accidental death coverage: ₹2 lakh',
                'Life insurance: ₹30,000'
            ],
            'documents_required': [
                'Aadhaar card',
                'PAN card (if available)',
                'Passport size photograph'
            ]
        },
        
        'Atal Pension Yojana (APY)': {
            'full_description': 'APY is a pension scheme that provides guaranteed monthly pension ranging from ₹1,000 to ₹5,000 at the age of 60 years.',
            'contribution_matrix': {
                '₹1,000 pension': 'Monthly contribution: ₹42-₹291 (depending on entry age)',
                '₹2,000 pension': 'Monthly contribution: ₹84-₹582',
                '₹3,000 pension': 'Monthly contribution: ₹126-₹873',
                '₹4,000 pension': 'Monthly contribution: ₹168-₹1,164',
                '₹5,000 pension': 'Monthly contribution: ₹210-₹1,454'
            },
            'government_cocontribution': 'Available for eligible subscribers for first 5 years',
            'exit_provisions': 'Premature exit allowed with applicable charges'
        },
        
        'Pradhan Mantri Mudra Yojana': {
            'full_description': 'MUDRA scheme provides micro-credit to small and micro enterprises and individuals for their income-generating activities.',
            'loan_categories': {
                'Shishu': 'Loans up to ₹50,000',
                'Kishore': 'Loans from ₹50,001 to ₹5 lakh',
                'Tarun': 'Loans from ₹5 lakh to ₹10 lakh'
            },
            'key_features': [
                'No collateral required',
                'Competitive interest rates',
                'Flexible repayment terms',
                'Special focus on women entrepreneurs'
            ],
            'eligible_activities': [
                'Food and textile production',
                'Trading and services',
                'Transport and equipment financing',
                'Community services'
            ]
        }
    }
    
    return scheme_details.get(scheme_name, {})

def check_eligibility(user_data, scheme_name):
    """Check if user is eligible for a specific scheme"""
    
    age = user_data['age']
    monthly_income = user_data['monthly_income']
    
    eligibility_criteria = {
        'Sukanya Samriddhi Yojana': {
            'age_limit': age <= 45,  # Parent can open for girl child
            'income_limit': True,  # No income limit
            'additional_conditions': ['Must have girl child under 10 years']
        },
        
        'Pradhan Mantri Jan Dhan Yojana (PMJDY)': {
            'age_limit': age >= 18,
            'income_limit': True,  # No income limit
            'additional_conditions': ['Must be Indian citizen']
        },
        
        'Atal Pension Yojana (APY)': {
            'age_limit': 18 <= age <= 40,
            'income_limit': True,  # No income limit
            'additional_conditions': ['Must have bank account']
        },
        
        'Pradhan Mantri Mudra Yojana': {
            'age_limit': age >= 18,
            'income_limit': monthly_income <= 100000,  # For micro-entrepreneurs
            'additional_conditions': ['Must have business plan or existing enterprise']
        },
        
        'Stand Up India': {
            'age_limit': 18 <= age <= 65,
            'income_limit': True,  # No specific income limit
            'additional_conditions': ['Must be woman entrepreneur', 'For greenfield enterprises']
        }
    }
    
    if scheme_name in eligibility_criteria:
        criteria = eligibility_criteria[scheme_name]
        is_eligible = criteria['age_limit'] and criteria['income_limit']
        return {
            'eligible': is_eligible,
            'criteria': criteria,
            'additional_requirements': criteria['additional_conditions']
        }
    
    return {'eligible': False, 'criteria': {}, 'additional_requirements': []}

def get_application_process(scheme_name):
    """Get step-by-step application process for schemes"""
    
    processes = {
        'Sukanya Samriddhi Yojana': [
            'Visit nearest bank branch or post office',
            'Carry required documents (birth certificate, ID proof, address proof)',
            'Fill the account opening form',
            'Make initial deposit (minimum ₹250)',
            'Receive account number and passbook',
            'Set up auto-debit for regular contributions (optional)'
        ],
        
        'Pradhan Mantri Jan Dhan Yojana (PMJDY)': [
            'Visit any participating bank branch',
            'Carry Aadhaar card and one photograph',
            'Fill the account opening form',
            'Complete KYC process',
            'Receive account number and RuPay debit card',
            'Activate mobile banking services'
        ],
        
        'Atal Pension Yojana (APY)': [
            'Ensure you have a savings bank account',
            'Visit your bank branch or apply online',
            'Fill the APY enrollment form',
            'Choose your pension amount (₹1,000 to ₹5,000)',
            'Provide Aadhaar and mobile number',
            'Set up auto-debit for monthly contributions',
            'Receive PRAN (Permanent Retirement Account Number)'
        ],
        
        'Pradhan Mantri Mudra Yojana': [
            'Prepare business plan and required documents',
            'Visit nearest bank, NBFC, or MFI',
            'Fill the MUDRA loan application form',
            'Submit documents and business proposal',
            'Undergo verification process',
            'Loan approval and disbursement',
            'Receive MUDRA card for future transactions'
        ]
    }
    
    return processes.get(scheme_name, [])

def get_contact_information():
    """Get contact information for scheme assistance"""
    
    return {
        'general_helpline': '1800-11-0001',
        'banking_helpline': '1800-180-1111',
        'pension_helpline': '1800-110-069',
        'women_helpline': '181',
        'websites': {
            'Sukanya Samriddhi Yojana': 'https://www.nsiindia.gov.in/',
            'PMJDY': 'https://pmjdy.gov.in/',
            'APY': 'https://www.npscra.nsdl.co.in/',
            'MUDRA': 'https://www.mudra.org.in/',
            'Stand Up India': 'https://www.standupmitra.in/'
        },
        'local_contacts': [
            'District Collector Office',
            'Block Development Office',
            'Anganwadi Centers',
            'Common Service Centers (CSC)',
            'Bank Branches'
        ]
    }
