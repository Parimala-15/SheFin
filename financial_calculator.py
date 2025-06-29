import math
from datetime import datetime, timedelta

class FinancialCalculator:
    def calculate_sip(self, monthly_amount, annual_return_rate, years):
        """Calculate SIP (Systematic Investment Plan) returns"""
        monthly_rate = annual_return_rate / (12 * 100)
        total_months = years * 12
        
        # Future Value of SIP formula
        if monthly_rate > 0:
            future_value = monthly_amount * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
        else:
            future_value = monthly_amount * total_months
        
        total_investment = monthly_amount * total_months
        total_returns = future_value
        wealth_gained = future_value - total_investment
        
        return {
            'total_investment': total_investment,
            'total_returns': total_returns,
            'wealth_gained': wealth_gained,
            'monthly_amount': monthly_amount,
            'years': years,
            'annual_return': annual_return_rate
        }
    
    def calculate_compound_interest(self, principal, annual_rate, years, compounding_frequency=1):
        """Calculate compound interest"""
        amount = principal * (1 + annual_rate / (100 * compounding_frequency)) ** (compounding_frequency * years)
        interest = amount - principal
        
        return {
            'principal': principal,
            'final_amount': amount,
            'interest_earned': interest,
            'annual_rate': annual_rate,
            'years': years
        }
    
    def calculate_goal_based_investment(self, target_amount, years, expected_return):
        """Calculate required monthly investment for a goal"""
        monthly_rate = expected_return / (12 * 100)
        total_months = years * 12
        
        if monthly_rate > 0:
            required_monthly = target_amount * monthly_rate / (((1 + monthly_rate) ** total_months - 1) * (1 + monthly_rate))
        else:
            required_monthly = target_amount / total_months
        
        total_investment = required_monthly * total_months
        
        return {
            'target_amount': target_amount,
            'required_monthly': required_monthly,
            'total_investment': total_investment,
            'years': years,
            'expected_return': expected_return
        }
    
    def calculate_retirement_corpus(self, current_age, retirement_age, monthly_expenses, inflation_rate=6):
        """Calculate retirement corpus needed"""
        years_to_retirement = retirement_age - current_age
        
        # Calculate future monthly expenses considering inflation
        future_monthly_expenses = monthly_expenses * (1 + inflation_rate / 100) ** years_to_retirement
        
        # Assume 25 years post-retirement life
        retirement_years = 25
        
        # Calculate total corpus needed (considering inflation during retirement too)
        total_corpus_needed = 0
        for year in range(retirement_years):
            annual_expenses = future_monthly_expenses * 12 * (1 + inflation_rate / 100) ** year
            # Discount back to retirement date (assuming 4% real return during retirement)
            present_value = annual_expenses / (1 + 0.04) ** year
            total_corpus_needed += present_value
        
        return {
            'current_age': current_age,
            'retirement_age': retirement_age,
            'current_monthly_expenses': monthly_expenses,
            'future_monthly_expenses': future_monthly_expenses,
            'total_corpus_needed': total_corpus_needed,
            'years_to_save': years_to_retirement
        }
    
    def calculate_emi(self, principal, annual_rate, years):
        """Calculate EMI for loan"""
        monthly_rate = annual_rate / (12 * 100)
        total_months = years * 12
        
        if monthly_rate > 0:
            emi = principal * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
        else:
            emi = principal / total_months
        
        total_payment = emi * total_months
        total_interest = total_payment - principal
        
        return {
            'emi': emi,
            'total_payment': total_payment,
            'total_interest': total_interest,
            'principal': principal,
            'years': years,
            'annual_rate': annual_rate
        }
    
    def calculate_emergency_fund(self, monthly_expenses, months=6):
        """Calculate emergency fund requirement"""
        emergency_fund = monthly_expenses * months
        
        return {
            'monthly_expenses': monthly_expenses,
            'months_coverage': months,
            'emergency_fund_needed': emergency_fund,
            'recommendation': f"Keep ₹{emergency_fund:,.0f} as emergency fund to cover {months} months of expenses"
        }
    
    def calculate_insurance_need(self, age, annual_income, dependents, existing_savings=0):
        """Calculate life insurance requirement"""
        # Human Life Value method with modifications for women
        working_years_left = 60 - age
        
        # Income replacement (considering career breaks for women)
        income_replacement = annual_income * working_years_left * 0.8  # 80% replacement
        
        # Add expenses for dependents
        dependent_expenses = dependents * 500000  # ₹5 lakh per dependent
        
        # Emergency fund
        emergency_fund = annual_income * 1  # 1 year income
        
        # Total insurance need
        total_insurance_need = income_replacement + dependent_expenses + emergency_fund - existing_savings
        total_insurance_need = max(total_insurance_need, annual_income * 10)  # Minimum 10x annual income
        
        return {
            'age': age,
            'annual_income': annual_income,
            'dependents': dependents,
            'total_insurance_need': total_insurance_need,
            'income_replacement': income_replacement,
            'dependent_expenses': dependent_expenses,
            'emergency_component': emergency_fund
        }
    
    def calculate_child_education_corpus(self, child_current_age, target_age, current_education_cost, inflation_rate=8):
        """Calculate corpus needed for child's education"""
        years_to_education = target_age - child_current_age
        
        # Future cost of education
        future_education_cost = current_education_cost * (1 + inflation_rate / 100) ** years_to_education
        
        # Add buffer for unexpected expenses
        total_corpus_needed = future_education_cost * 1.2  # 20% buffer
        
        return {
            'child_current_age': child_current_age,
            'target_age': target_age,
            'years_to_save': years_to_education,
            'current_cost': current_education_cost,
            'future_cost': future_education_cost,
            'total_corpus_needed': total_corpus_needed,
            'inflation_rate': inflation_rate
        }
    
    def calculate_tax_savings(self, annual_income, investments_80c=0, health_insurance=0, home_loan_interest=0):
        """Calculate tax savings under various sections"""
        # Income tax slabs for FY 2023-24 (New Regime)
        tax_slabs = [
            (300000, 0),      # Up to 3L - 0%
            (600000, 5),      # 3L to 6L - 5%
            (900000, 10),     # 6L to 9L - 10%
            (1200000, 15),    # 9L to 12L - 15%
            (1500000, 20),    # 12L to 15L - 20%
            (float('inf'), 30) # Above 15L - 30%
        ]
        
        def calculate_tax(income):
            tax = 0
            prev_limit = 0
            for limit, rate in tax_slabs:
                if income > prev_limit:
                    taxable_in_slab = min(income, limit) - prev_limit
                    tax += taxable_in_slab * rate / 100
                    prev_limit = limit
                else:
                    break
            return tax
        
        # Tax without deductions
        tax_without_deductions = calculate_tax(annual_income)
        
        # Tax with deductions
        total_deductions = min(investments_80c, 150000) + min(health_insurance, 25000)
        taxable_income = max(annual_income - total_deductions - home_loan_interest, 0)
        tax_with_deductions = calculate_tax(taxable_income)
        
        tax_saved = tax_without_deductions - tax_with_deductions
        
        return {
            'annual_income': annual_income,
            'tax_without_deductions': tax_without_deductions,
            'tax_with_deductions': tax_with_deductions,
            'tax_saved': tax_saved,
            'total_deductions': total_deductions,
            'effective_tax_rate': (tax_with_deductions / annual_income) * 100 if annual_income > 0 else 0
        }
