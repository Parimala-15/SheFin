import streamlit as st
import pandas as pd
import plotly.express as px
import time

import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from ai_services import FinancialChatbot, CreditScorer, GoalPlanner
from financial_calculator import FinancialCalculator
from utils import format_currency, get_user_language, translate_text
from government_schemes import get_schemes_for_user
from translations import TRANSLATIONS

from mood_tracker import MoneyMoodTracker

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


# Initialize services globally with lazy loading for better performance
@st.cache_resource
def get_database():
    """Initialize database connection once and cache it"""
    from database_config import get_database_manager
    db = get_database_manager()
    db.init_database()
    return db


@st.cache_resource
def get_chatbot():
    """Initialize chatbot once and cache it"""
    from ai_services import FinancialChatbot
    return FinancialChatbot()


@st.cache_resource
def get_calculator():
    """Initialize calculator once and cache it"""
    from financial_calculator import FinancialCalculator
    return FinancialCalculator()


@st.cache_resource
def get_credit_scorer():
    """Initialize credit scorer once and cache it"""
    from ai_services import CreditScorer
    return CreditScorer()


@st.cache_resource
def get_goal_planner():
    """Initialize goal planner once and cache it"""
    from ai_services import GoalPlanner
    return GoalPlanner()


@st.cache_resource
def get_mood_tracker():
    """Initialize mood tracker once and cache it"""
    return MoneyMoodTracker()


# Lazy load services for better performance
db = get_database()
chatbot = get_chatbot()
calculator = get_calculator()
credit_scorer = get_credit_scorer()
goal_planner = get_goal_planner()
mood_tracker = get_mood_tracker()


def main():
    st.set_page_config(page_title="SheFin - AI Financial Companion for Women",
                       page_icon="💰",
                       layout="wide",
                       initial_sidebar_state="expanded")

    # Custom CSS for responsiveness
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        margin-bottom: 1rem;
        background: #f9f9f9;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: #f0f2f6;
    }
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0;
        }
        .feature-card {
            padding: 0.5rem;
        }
    }
    </style>
    """,
                unsafe_allow_html=True)

    # Language selector in sidebar
    st.sidebar.title("🌐 Language / भाषा / மொழி")
    language_options = {
        'English': 'english',
        'हिंदी (Hindi)': 'hindi',
        'தமிழ் (Tamil)': 'tamil'
    }
    selected_lang = st.sidebar.selectbox("Select Language",
                                         options=list(language_options.keys()),
                                         index=0)
    st.session_state.language = language_options[selected_lang]

    # Main header
    st.markdown(f"""
    <div class="main-header">
        <h1>💰 {translate_text('SheFin - AI Financial Companion for Women', st.session_state.language)}</h1>
        <p>{translate_text('Empowering women through personalized financial guidance', st.session_state.language)}</p>
    </div>
    """,
                unsafe_allow_html=True)

    # Authentication
    if not st.session_state.authenticated:
        show_auth_page()
        return

    # Navigation
    menu_options = [
        "🏠 Dashboard", "💬 AI Financial Coach", "💰 Budget Tracker",
        "🎯 Goal Planning", "📈 Investment Guide", "🎓 Financial Education",
        "😊 Money Mood Tracker", "🏛️ Government Schemes", "📊 Credit Score",
        "👤 Profile"
    ]

    selected_menu = st.sidebar.selectbox(
        translate_text("Navigation", st.session_state.language), menu_options)

    # Route to different pages
    if selected_menu == "🏠 Dashboard":
        show_dashboard()
    elif selected_menu == "💬 AI Financial Coach":
        show_ai_coach()
    elif selected_menu == "💰 Budget Tracker":
        show_budget_tracker()
    elif selected_menu == "🎯 Goal Planning":
        show_goal_planning()
    elif selected_menu == "📈 Investment Guide":
        show_investment_guide()
    elif selected_menu == "🎓 Financial Education":
        show_education_modules()
    elif selected_menu == "😊 Money Mood Tracker":
        show_mood_tracker()
    elif selected_menu == "🏛️ Government Schemes":
        show_government_schemes()
    elif selected_menu == "📊 Credit Score":
        show_credit_score()
    elif selected_menu == "👤 Profile":
        show_profile()


def show_auth_page():
    st.subheader(translate_text("Welcome to SheFin",
                                st.session_state.language))

    tab1, tab2 = st.tabs([
        translate_text("Login", st.session_state.language),
        translate_text("Register", st.session_state.language)
    ])

    with tab1:
        st.subheader(
            translate_text("Login to Your Account", st.session_state.language))
        email = st.text_input(
            translate_text("Email", st.session_state.language))
        password = st.text_input(translate_text("Password",
                                                st.session_state.language),
                                 type="password")

        if st.button(translate_text("Login", st.session_state.language)):
            user = db.authenticate_user(email, password)
            if user:
                st.session_state.user_id = user['id']
                st.session_state.authenticated = True
                st.success(
                    translate_text("Login successful!",
                                   st.session_state.language))
                st.rerun()
            else:
                st.error(
                    translate_text("Invalid credentials",
                                   st.session_state.language))

    with tab2:
        st.subheader(
            translate_text("Create New Account", st.session_state.language))
        name = st.text_input(
            translate_text("Full Name", st.session_state.language))
        email = st.text_input(
            translate_text("Email Address", st.session_state.language))
        age = st.number_input(translate_text("Age", st.session_state.language),
                              min_value=18,
                              max_value=100)
        monthly_income = st.number_input(translate_text(
            "Monthly Income (₹)", st.session_state.language),
                                         min_value=0)
        password = st.text_input(translate_text("Create Password",
                                                st.session_state.language),
                                 type="password")

        if st.button(translate_text("Register", st.session_state.language)):
            if name and email and password:
                user_id = db.create_user(name, email, age, monthly_income,
                                         password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.authenticated = True
                    st.success(
                        translate_text("Registration successful!",
                                       st.session_state.language))
                    st.rerun()
                else:
                    st.error(
                        translate_text(
                            "Registration failed. Email might already exist.",
                            st.session_state.language))
            else:
                st.error(
                    translate_text("Please fill all fields",
                                   st.session_state.language))


def show_dashboard():
    st.title(translate_text("📊 Financial Dashboard",
                            st.session_state.language))

    # Get user data
    user_data = db.get_user_profile(st.session_state.user_id)
    transactions = db.get_user_transactions(st.session_state.user_id)
    goals = db.get_user_goals(st.session_state.user_id)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    total_income = sum(
        [t['amount'] for t in transactions if t['type'] == 'income'])
    total_expenses = sum(
        [t['amount'] for t in transactions if t['type'] == 'expense'])
    savings = total_income - total_expenses
    active_goals = len([g for g in goals if g['status'] == 'active'])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{format_currency(total_income)}</h3>
            <p>{translate_text('Total Income', st.session_state.language)}</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{format_currency(total_expenses)}</h3>
            <p>{translate_text('Total Expenses', st.session_state.language)}</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{format_currency(savings)}</h3>
            <p>{translate_text('Net Savings', st.session_state.language)}</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{active_goals}</h3>
            <p>{translate_text('Active Goals', st.session_state.language)}</p>
        </div>
        """,
                    unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(
            translate_text("Income vs Expenses", st.session_state.language))
        if transactions:
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date'])
            monthly_data = df.groupby([df['date'].dt.to_period('M'),
                                       'type'])['amount'].sum().reset_index()
            monthly_data['date'] = monthly_data['date'].astype(str)

            fig = px.bar(monthly_data,
                         x='date',
                         y='amount',
                         color='type',
                         title=translate_text("Monthly Income vs Expenses",
                                              st.session_state.language))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(
                translate_text("No transaction data available",
                               st.session_state.language))

    with col2:
        st.subheader(
            translate_text("Expense Categories", st.session_state.language))
        if transactions:
            expense_data = [t for t in transactions if t['type'] == 'expense']
            if expense_data:
                df_expenses = pd.DataFrame(expense_data)
                category_sum = df_expenses.groupby('category')['amount'].sum()

                fig = px.pie(values=category_sum.values,
                             names=category_sum.index,
                             title=translate_text("Expense Distribution",
                                                  st.session_state.language))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    translate_text("No expense data available",
                                   st.session_state.language))
        else:
            st.info(
                translate_text("No transaction data available",
                               st.session_state.language))

    # Recent transactions
    st.subheader(
        translate_text("Recent Transactions", st.session_state.language))
    if transactions:
        recent_transactions = sorted(transactions,
                                     key=lambda x: x['date'],
                                     reverse=True)[:5]
        df_recent = pd.DataFrame(recent_transactions)
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info(
            translate_text(
                "No transactions found. Start by adding your income and expenses!",
                st.session_state.language))


def show_ai_coach():
    st.title(translate_text("💬 AI Financial Coach", st.session_state.language))
    st.write(
        translate_text(
            "Ask me anything about personal finance, investments, budgeting, or government schemes!",
            st.session_state.language))

    # Chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(
            translate_text("Ask your financial question...",
                           st.session_state.language)):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response with real-time generation
        with st.chat_message("assistant"):
            with st.spinner(
                    translate_text("Thinking...", st.session_state.language)):
                # Get user context for personalized advice
                user_data = db.get_user_profile(st.session_state.user_id)
                transactions = db.get_user_transactions(
                    st.session_state.user_id)

                # Create placeholder for streaming response
                response_placeholder = st.empty()

                # Get response from AI
                response = chatbot.get_financial_advice(
                    prompt, user_data, transactions, st.session_state.language)

                # Simulate real-time generation with streaming effect
                displayed_text = ""
                words = response.split()

                for i, word in enumerate(words):
                    displayed_text += word + " "
                    response_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.05)


# Small delay for typing effect

# Final response without cursor
                response_placeholder.markdown(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

    # Quick action buttons
    st.subheader(
        translate_text("Quick Financial Tips", st.session_state.language))
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
                translate_text("💰 Budgeting Tips", st.session_state.language)):
            advice = chatbot.get_budgeting_tips(st.session_state.language)
            st.info(advice)

    with col2:
        if st.button(
                translate_text("📈 Investment Basics",
                               st.session_state.language)):
            advice = chatbot.get_investment_basics(st.session_state.language)
            st.info(advice)

    with col3:
        if st.button(
                translate_text("🏛️ Government Schemes",
                               st.session_state.language)):
            advice = chatbot.get_government_schemes_info(
                st.session_state.language)
            st.info(advice)


def show_budget_tracker():
    st.title(
        translate_text("💰 Smart Budget Tracker", st.session_state.language))

    tab1, tab2, tab3 = st.tabs([
        translate_text("Add Transaction", st.session_state.language),
        translate_text("View Transactions", st.session_state.language),
        translate_text("Budget Analysis", st.session_state.language)
    ])

    with tab1:
        st.subheader(
            translate_text("Add New Transaction", st.session_state.language))

        col1, col2 = st.columns(2)
        with col1:
            transaction_type = st.selectbox(
                translate_text("Type", st.session_state.language), [
                    translate_text("Income", st.session_state.language),
                    translate_text("Expense", st.session_state.language)
                ])
            amount = st.number_input(translate_text("Amount (₹)",
                                                    st.session_state.language),
                                     min_value=0.0,
                                     step=1.0)

        with col2:
            if transaction_type == translate_text("Expense",
                                                  st.session_state.language):
                categories = [
                    "Food", "Transportation", "Healthcare", "Education",
                    "Shopping", "Utilities", "Entertainment", "Other"
                ]
            else:
                categories = [
                    "Salary", "Business", "Investment Returns",
                    "Government Benefits", "Other"
                ]

            category = st.selectbox(
                translate_text("Category", st.session_state.language),
                categories)
            date = st.date_input(
                translate_text("Date", st.session_state.language),
                datetime.now())

        description = st.text_input(
            translate_text("Description (Optional)",
                           st.session_state.language))

        if st.button(
                translate_text("Add Transaction", st.session_state.language)):
            if amount > 0:
                transaction_type_en = "expense" if transaction_type == translate_text(
                    "Expense", st.session_state.language) else "income"
                db.add_transaction(st.session_state.user_id,
                                   transaction_type_en, amount, category,
                                   description, date)
                st.success(
                    translate_text("Transaction added successfully!",
                                   st.session_state.language))
                st.rerun()
            else:
                st.error(
                    translate_text("Please enter a valid amount",
                                   st.session_state.language))

    with tab2:
        st.subheader(
            translate_text("Transaction History", st.session_state.language))
        transactions = db.get_user_transactions(st.session_state.user_id)

        if transactions:
            df = pd.DataFrame(transactions)
            df = df.sort_values('date', ascending=False)

            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                type_filter = st.selectbox(
                    translate_text("Filter by Type",
                                   st.session_state.language),
                    ["All", "Income", "Expense"])
            with col2:
                if transactions:
                    categories = df['category'].unique().tolist()
                    category_filter = st.selectbox(
                        translate_text("Filter by Category",
                                       st.session_state.language),
                        ["All"] + categories)
            with col3:
                date_range = st.selectbox(
                    translate_text("Date Range", st.session_state.language),
                    ["All Time", "Last 30 Days", "Last 90 Days", "This Year"])

            # Apply filters
            filtered_df = df.copy()
            if type_filter != "All":
                filtered_df = filtered_df[filtered_df['type'] ==
                                          type_filter.lower()]
            if category_filter != "All":
                filtered_df = filtered_df[filtered_df['category'] ==
                                          category_filter]

            if date_range != "All Time":
                today = datetime.now()
                if date_range == "Last 30 Days":
                    start_date = today - timedelta(days=30)
                elif date_range == "Last 90 Days":
                    start_date = today - timedelta(days=90)
                else:  # This Year
                    start_date = datetime(today.year, 1, 1)

                filtered_df['date'] = pd.to_datetime(filtered_df['date'])
                filtered_df = filtered_df[filtered_df['date'] >= start_date]

            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info(
                translate_text(
                    "No transactions found. Add your first transaction!",
                    st.session_state.language))

    with tab3:
        st.subheader(
            translate_text("Budget Analysis & Insights",
                           st.session_state.language))

        transactions = db.get_user_transactions(st.session_state.user_id)
        if transactions:
            # AI-powered budget insights
            user_data = db.get_user_profile(st.session_state.user_id)
            insights = chatbot.get_budget_insights(transactions, user_data,
                                                   st.session_state.language)

            st.markdown(f"""
            <div class="feature-card">
                <h4>{translate_text('AI Budget Insights', st.session_state.language)}</h4>
                <p>{insights}</p>
            </div>
            """,
                        unsafe_allow_html=True)

            # Spending trends
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date'])

            # Monthly spending trend
            monthly_expenses = df[df['type'] == 'expense'].groupby(
                df['date'].dt.to_period('M'))['amount'].sum()

            if len(monthly_expenses) > 1:
                fig = px.line(x=monthly_expenses.index.astype(str),
                              y=monthly_expenses.values,
                              title=translate_text("Monthly Spending Trend",
                                                   st.session_state.language))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(
                translate_text("Add some transactions to see budget analysis",
                               st.session_state.language))


def show_goal_planning():
    st.title(
        translate_text("🎯 Goal-Based Financial Planning",
                       st.session_state.language))

    tab1, tab2 = st.tabs([
        translate_text("My Goals", st.session_state.language),
        translate_text("Create New Goal", st.session_state.language)
    ])

    with tab1:
        goals = db.get_user_goals(st.session_state.user_id)

        if goals:
            for goal in goals:
                progress = (goal['current_amount'] /
                            goal['target_amount']) * 100

                st.markdown(f"""
                <div class="feature-card">
                    <h4>{goal['name']}</h4>
                    <p><strong>{translate_text('Target Amount', st.session_state.language)}:</strong> ₹{format_currency(goal['target_amount'])}</p>
                    <p><strong>{translate_text('Current Amount', st.session_state.language)}:</strong> ₹{format_currency(goal['current_amount'])}</p>
                    <p><strong>{translate_text('Target Date', st.session_state.language)}:</strong> {goal['target_date']}</p>
                    <p><strong>{translate_text('Progress', st.session_state.language)}:</strong> {progress:.1f}%</p>
                </div>
                """,
                            unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.progress(progress / 100)

                with col2:
                    add_amount = st.number_input(
                        f"{translate_text('Add to', st.session_state.language)} {goal['name']} (₹)",
                        min_value=0.0,
                        key=f"add_{goal['id']}")
                    if st.button(
                            f"{translate_text('Update', st.session_state.language)} {goal['name']}",
                            key=f"update_{goal['id']}"):
                        if add_amount > 0:
                            db.update_goal_progress(
                                goal['id'],
                                goal['current_amount'] + add_amount)
                            st.success(
                                translate_text("Goal updated successfully!",
                                               st.session_state.language))
                            st.rerun()

                # AI recommendations for achieving goal
                if progress < 100:
                    recommendation = goal_planner.get_goal_recommendations(
                        goal, st.session_state.language)
                    st.info(f"💡 {recommendation}")

                st.divider()
        else:
            st.info(
                translate_text(
                    "No goals created yet. Create your first financial goal!",
                    st.session_state.language))

    with tab2:
        st.subheader(
            translate_text("Create New Financial Goal",
                           st.session_state.language))

        goal_name = st.text_input(
            translate_text("Goal Name", st.session_state.language))
        target_amount = st.number_input(translate_text(
            "Target Amount (₹)", st.session_state.language),
                                        min_value=1000)
        target_date = st.date_input(
            translate_text("Target Date", st.session_state.language),
            min_value=datetime.now() + timedelta(days=30))
        initial_amount = st.number_input(translate_text(
            "Initial Amount (₹)", st.session_state.language),
                                         min_value=0)

        goal_category = st.selectbox(
            translate_text("Goal Category", st.session_state.language), [
                "Emergency Fund", "Child Education", "House Purchase",
                "Business", "Marriage", "Retirement", "Healthcare", "Other"
            ])

        if st.button(translate_text("Create Goal", st.session_state.language)):
            if goal_name and target_amount > 0:
                goal_id = db.create_goal(st.session_state.user_id, goal_name,
                                         target_amount, target_date,
                                         initial_amount, goal_category)
                if goal_id:
                    st.success(
                        translate_text("Goal created successfully!",
                                       st.session_state.language))

                    # Generate AI-powered action plan
                    user_data = db.get_user_profile(st.session_state.user_id)
                    transactions = db.get_user_transactions(
                        st.session_state.user_id)
                    action_plan = goal_planner.create_action_plan(
                        goal_name, target_amount, target_date, user_data,
                        transactions, st.session_state.language)

                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{translate_text('AI-Generated Action Plan', st.session_state.language)}</h4>
                        <p>{action_plan}</p>
                    </div>
                    """,
                                unsafe_allow_html=True)

                    st.rerun()
                else:
                    st.error(
                        translate_text("Failed to create goal",
                                       st.session_state.language))
            else:
                st.error(
                    translate_text("Please fill all required fields",
                                   st.session_state.language))


def show_investment_guide():
    st.title(
        translate_text("📈 Investment Education & Recommendations",
                       st.session_state.language))

    tab1, tab2, tab3 = st.tabs([
        translate_text("Investment Basics", st.session_state.language),
        translate_text("Personalized Recommendations",
                       st.session_state.language),
        translate_text("Investment Calculator", st.session_state.language)
    ])

    with tab1:
        st.subheader(
            translate_text("Learn About Investments",
                           st.session_state.language))

        investment_topics = {
            translate_text("Mutual Funds", st.session_state.language):
            "mutual_funds",
            translate_text("Fixed Deposits", st.session_state.language):
            "fixed_deposits",
            translate_text("Gold Investment", st.session_state.language):
            "gold",
            translate_text("PPF & ELSS", st.session_state.language):
            "tax_saving",
            translate_text("SIP (Systematic Investment Plan)", st.session_state.language):
            "sip"
        }

        selected_topic = st.selectbox(
            translate_text("Choose a topic to learn",
                           st.session_state.language),
            list(investment_topics.keys()))

        if st.button(
                translate_text("Get Educational Content",
                               st.session_state.language)):
            content = chatbot.get_investment_education(
                investment_topics[selected_topic], st.session_state.language)
            st.markdown(f"""
            <div class="feature-card">
                <h4>{selected_topic}</h4>
                <p>{content}</p>
            </div>
            """,
                        unsafe_allow_html=True)

    with tab2:
        st.subheader(
            translate_text("📚 Educational Content", st.session_state.language))

        content_categories = {
            translate_text("Investment Basics", st.session_state.language):
            "basics",
            translate_text("Stocks & Share Market", st.session_state.language):
            "stocks",
            translate_text("Mutual Funds & SIP", st.session_state.language):
            "mutual_funds",
            translate_text("Retirement Planning", st.session_state.language):
            "retirement",
            translate_text("Emergency Fund", st.session_state.language):
            "emergency_fund"
        }

        selected_category = st.selectbox(
            translate_text("Choose Learning Topic", st.session_state.language),
            list(content_categories.keys()))

        if st.button(
                translate_text("Get Educational Content",
                               st.session_state.language)):
            with st.spinner(
                    translate_text("Generating educational content...",
                                   st.session_state.language)):
                educational_content = chatbot.get_investment_education(
                    content_categories[selected_category],
                    st.session_state.language)

                if educational_content:
                    st.success(
                        translate_text(
                            "Educational content generated successfully!",
                            st.session_state.language))

                    # Display content in structured format
                    st.markdown(f"""
                    <div class="feature-card" style="margin: 1rem 0; padding: 1.5rem;">
                        <div style="color: #4CAF50; margin-bottom: 1rem; font-size: 1.2em;">
                            📚 {selected_category}
                        </div>
                        <div style="line-height: 1.6; white-space: pre-wrap;">
                            {educational_content}
                        </div>
                    </div>
                    """,
                                unsafe_allow_html=True)
                else:
                    st.warning(
                        translate_text(
                            "Content generation failed. Please try again.",
                            st.session_state.language))

    with tab2:
        st.subheader(
            translate_text("Personalized Investment Recommendations",
                           st.session_state.language))

        user_data = db.get_user_profile(st.session_state.user_id)
        transactions = db.get_user_transactions(st.session_state.user_id)

        col1, col2 = st.columns(2)
        with col1:
            risk_tolerance = st.selectbox(
                translate_text("Risk Tolerance", st.session_state.language), [
                    translate_text("Conservative", st.session_state.language),
                    translate_text("Moderate", st.session_state.language),
                    translate_text("Aggressive", st.session_state.language)
                ])

        with col2:
            investment_horizon = st.selectbox(
                translate_text("Investment Horizon",
                               st.session_state.language), [
                                   translate_text("Short-term (1-3 years)",
                                                  st.session_state.language),
                                   translate_text("Medium-term (3-5 years)",
                                                  st.session_state.language),
                                   translate_text("Long-term (5+ years)",
                                                  st.session_state.language)
                               ])

        investment_amount = st.number_input(translate_text(
            "Amount to Invest (₹)", st.session_state.language),
                                            min_value=500)

        if st.button(
                translate_text("Get Recommendations",
                               st.session_state.language)):
            recommendations = chatbot.get_investment_recommendations(
                user_data, risk_tolerance, investment_horizon,
                investment_amount, st.session_state.language)

            st.markdown(f"""
            <div class="feature-card">
                <h4>{translate_text('Personalized Investment Recommendations', st.session_state.language)}</h4>
                <p>{recommendations}</p>
            </div>
            """,
                        unsafe_allow_html=True)

    with tab3:
        st.subheader(
            translate_text("Investment Calculators",
                           st.session_state.language))

        calc_type = st.selectbox(
            translate_text("Calculator Type", st.session_state.language), [
                translate_text("SIP Calculator", st.session_state.language),
                translate_text("Compound Interest", st.session_state.language),
                translate_text("Goal-based Investment",
                               st.session_state.language)
            ])

        if calc_type == translate_text("SIP Calculator",
                                       st.session_state.language):
            col1, col2, col3 = st.columns(3)
            with col1:
                monthly_sip = st.number_input(translate_text(
                    "Monthly SIP Amount (₹)", st.session_state.language),
                                              min_value=500)
            with col2:
                annual_return = st.slider(
                    translate_text("Expected Annual Return (%)",
                                   st.session_state.language), 5, 20, 12)
            with col3:
                years = st.slider(
                    translate_text("Investment Period (Years)",
                                   st.session_state.language), 1, 30, 10)

            if st.button(
                    translate_text("Calculate SIP Returns",
                                   st.session_state.language)):
                result = calculator.calculate_sip(monthly_sip, annual_return,
                                                  years)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        translate_text("Total Investment",
                                       st.session_state.language),
                        f"₹{format_currency(result['total_investment'])}")
                with col2:
                    st.metric(
                        translate_text("Total Returns",
                                       st.session_state.language),
                        f"₹{format_currency(result['total_returns'])}")
                with col3:
                    st.metric(
                        translate_text("Wealth Gained",
                                       st.session_state.language),
                        f"₹{format_currency(result['wealth_gained'])}")

        elif calc_type == translate_text("Compound Interest",
                                         st.session_state.language):
            col1, col2, col3 = st.columns(3)
            with col1:
                principal = st.number_input(translate_text(
                    "Principal Amount (₹)", st.session_state.language),
                                            min_value=1000)
            with col2:
                annual_return = st.slider(
                    translate_text("Annual Interest Rate (%)",
                                   st.session_state.language), 1, 15, 8)
            with col3:
                years = st.slider(
                    translate_text("Investment Period (Years)",
                                   st.session_state.language), 1, 30, 5)

            if st.button(
                    translate_text("Calculate Compound Interest",
                                   st.session_state.language)):
                result = calculator.calculate_compound_interest(
                    principal, annual_return, years)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        translate_text("Principal", st.session_state.language),
                        f"₹{format_currency(result['principal'])}")
                with col2:
                    st.metric(
                        translate_text("Final Amount",
                                       st.session_state.language),
                        f"₹{format_currency(result['final_amount'])}")
                with col3:
                    st.metric(
                        translate_text("Interest Earned",
                                       st.session_state.language),
                        f"₹{format_currency(result['interest_earned'])}")

        elif calc_type == translate_text("Goal-based Investment",
                                         st.session_state.language):
            col1, col2, col3 = st.columns(3)
            with col1:
                target_amount = st.number_input(translate_text(
                    "Target Amount (₹)", st.session_state.language),
                                                min_value=10000)
            with col2:
                years = st.slider(
                    translate_text("Time Period (Years)",
                                   st.session_state.language), 1, 30, 10)
            with col3:
                expected_return = st.slider(
                    translate_text("Expected Return (%)",
                                   st.session_state.language), 5, 20, 12)

            if st.button(
                    translate_text("Calculate Required Investment",
                                   st.session_state.language)):
                result = calculator.calculate_goal_based_investment(
                    target_amount, years, expected_return)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        translate_text("Required Monthly SIP",
                                       st.session_state.language),
                        f"₹{format_currency(result['required_monthly'])}")
                with col2:
                    st.metric(
                        translate_text("Total Investment",
                                       st.session_state.language),
                        f"₹{format_currency(result['total_investment'])}")
                with col3:
                    st.metric(
                        translate_text("Target Amount",
                                       st.session_state.language),
                        f"₹{format_currency(result['target_amount'])}")


def show_education_modules():
    st.title(
        translate_text("🎓 Financial Education Hub", st.session_state.language))

    tab1, tab2 = st.tabs([
        translate_text("Text-based Learning", st.session_state.language),
        translate_text("Video Learning", st.session_state.language)
    ])

    with tab1:
        # Education levels
        level = st.selectbox(
            translate_text("Choose your level", st.session_state.language), [
                translate_text("Beginner", st.session_state.language),
                translate_text("Intermediate", st.session_state.language),
                translate_text("Advanced", st.session_state.language)
            ])

    # Education modules based on level
    if level == translate_text("Beginner", st.session_state.language):
        modules = [
            translate_text("What is Money Management?",
                           st.session_state.language),
            translate_text("Creating Your First Budget",
                           st.session_state.language),
            translate_text("Understanding Bank Accounts",
                           st.session_state.language),
            translate_text("Basic Saving Strategies",
                           st.session_state.language),
            translate_text("Understanding Interest", st.session_state.language)
        ]
    elif level == translate_text("Intermediate", st.session_state.language):
        modules = [
            translate_text("Investment Fundamentals",
                           st.session_state.language),
            translate_text("Mutual Funds vs Fixed Deposits",
                           st.session_state.language),
            translate_text("Insurance Planning", st.session_state.language),
            translate_text("Tax Planning Basics", st.session_state.language),
            translate_text("Emergency Fund Creation",
                           st.session_state.language)
        ]
    else:  # Advanced
        modules = [
            translate_text("Portfolio Diversification",
                           st.session_state.language),
            translate_text("Advanced Tax Strategies",
                           st.session_state.language),
            translate_text("Retirement Planning", st.session_state.language),
            translate_text("Real Estate Investment",
                           st.session_state.language),
            translate_text("Financial Independence", st.session_state.language)
        ]

    selected_module = st.selectbox(
        translate_text("Select a module", st.session_state.language), modules)

    if st.button(translate_text("Start Learning", st.session_state.language)):
        content = chatbot.get_investment_education(selected_module,
                                                   st.session_state.language)

        st.markdown(f"""
        <div class="feature-card">
            <h4>{selected_module}</h4>
            <p>{content}</p>
        </div>
        """,
                    unsafe_allow_html=True)

        # Track learning progress
        db.track_learning_progress(st.session_state.user_id, selected_module,
                                   level)

    with tab2:
        st.subheader(
            translate_text("📹 Educational Video Library",
                           st.session_state.language))

        education_video_topics = {
            translate_text("Budgeting & Money Management", st.session_state.language):
            "budgeting",
            translate_text("Saving Strategies", st.session_state.language):
            "saving",
            translate_text("Debt Management", st.session_state.language):
            "debt",
            translate_text("Insurance Planning", st.session_state.language):
            "insurance",
            translate_text("Tax Planning", st.session_state.language):
            "taxes"
        }

        selected_topic = st.selectbox(
            translate_text("Choose Educational Topic",
                           st.session_state.language),
            list(education_video_topics.keys()))

        if st.button(translate_text("Get Educational Content",
                                    st.session_state.language),
                     key="education_content"):
            with st.spinner(
                    translate_text("Generating educational content...",
                                   st.session_state.language)):
                educational_content = chatbot.get_investment_education(
                    education_video_topics[selected_topic],
                    st.session_state.language)

                if educational_content:
                    st.success(
                        translate_text(
                            "Educational content generated successfully!",
                            st.session_state.language))

                    # Display content in structured format
                    st.markdown(f"""
                    <div class="feature-card" style="margin: 1rem 0; padding: 1.5rem;">
                        <div style="color: #4ECDC4; margin-bottom: 1rem; font-size: 1.2em;">
                            📚 {selected_topic}
                        </div>
                        <div style="line-height: 1.6; white-space: pre-wrap;">
                            {educational_content}
                        </div>
                    </div>
                    """,
                                unsafe_allow_html=True)
                else:
                    st.warning(
                        translate_text(
                            "Content generation failed. Please try again.",
                            st.session_state.language))

    # Learning progress
    st.subheader(
        translate_text("Your Learning Progress", st.session_state.language))
    progress = db.get_learning_progress(st.session_state.user_id)

    if progress:
        df_progress = pd.DataFrame(progress)
        st.dataframe(df_progress, use_container_width=True)

        # Progress visualization
        level_counts = df_progress['level'].value_counts()
        fig = px.bar(x=level_counts.index,
                     y=level_counts.values,
                     title=translate_text("Modules Completed by Level",
                                          st.session_state.language))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            translate_text("Start learning to track your progress!",
                           st.session_state.language))


def show_government_schemes():
    st.title(
        translate_text("🏛️ Government Financial Schemes for Women",
                       st.session_state.language))

    user_data = db.get_user_profile(st.session_state.user_id)
    schemes = get_schemes_for_user(user_data)

    st.subheader(
        translate_text("Schemes You May Be Eligible For",
                       st.session_state.language))

    for scheme in schemes:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{translate_text(scheme['name'], st.session_state.language)}</h4>
            <p><strong>{translate_text('Description', st.session_state.language)}:</strong> {translate_text(scheme['description'], st.session_state.language)}</p>
            <p><strong>{translate_text('Benefits', st.session_state.language)}:</strong> {translate_text(scheme['benefits'], st.session_state.language)}</p>
            <p><strong>{translate_text('Eligibility', st.session_state.language)}:</strong> {translate_text(scheme['eligibility'], st.session_state.language)}</p>
            <p><strong>{translate_text('How to Apply', st.session_state.language)}:</strong> {translate_text(scheme['how_to_apply'], st.session_state.language)}</p>
        </div>
        """,
                    unsafe_allow_html=True)

    # AI assistant for scheme queries
    st.subheader(
        translate_text("Ask About Government Schemes",
                       st.session_state.language))
    scheme_query = st.text_input(
        translate_text("Ask about any government scheme...",
                       st.session_state.language))

    if st.button(translate_text("Get Information",
                                st.session_state.language)) and scheme_query:
        response = chatbot.get_scheme_information(scheme_query, user_data,
                                                  st.session_state.language)
        st.info(response)


def show_credit_score():
    st.title(
        translate_text("📊 Credit Score Simulation & Tips",
                       st.session_state.language))

    st.info(
        translate_text(
            "This is a simulated credit score based on your financial behavior patterns",
            st.session_state.language))

    user_data = db.get_user_profile(st.session_state.user_id)
    transactions = db.get_user_transactions(st.session_state.user_id)

    # Calculate simulated credit score
    credit_score = credit_scorer.calculate_score(user_data, transactions)

    # Display credit score
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(translate_text("Credit Score", st.session_state.language),
                  credit_score['score'])

    with col2:
        st.metric(translate_text("Score Range", st.session_state.language),
                  credit_score['range'])

    with col3:
        color = "green" if credit_score[
            'score'] >= 750 else "orange" if credit_score[
                'score'] >= 650 else "red"
        st.markdown(f"<h3 style='color: {color}'>{credit_score['grade']}</h3>",
                    unsafe_allow_html=True)

    # Score breakdown
    st.subheader(translate_text("Score Factors", st.session_state.language))

    factors = credit_score['factors']
    for factor, score in factors.items():
        st.progress(
            score / 100,
            text=
            f"{translate_text(factor, st.session_state.language)}: {score}%")

    # Improvement tips
    st.subheader(
        translate_text("How to Improve Your Credit Score",
                       st.session_state.language))
    tips = credit_scorer.get_improvement_tips(credit_score,
                                              st.session_state.language)

    for i, tip in enumerate(tips, 1):
        st.markdown(f"""
        <div class="feature-card">
            <h5>{translate_text('Tip', st.session_state.language)} {i}</h5>
            <p>{tip}</p>
        </div>
        """,
                    unsafe_allow_html=True)


def show_profile():
    st.title(translate_text("👤 User Profile", st.session_state.language))

    user_data = db.get_user_profile(st.session_state.user_id)

    tab1, tab2 = st.tabs([
        translate_text("Profile Information", st.session_state.language),
        translate_text("Settings", st.session_state.language)
    ])

    with tab1:
        st.subheader(
            translate_text("Profile Details", st.session_state.language))

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(translate_text("Name",
                                                st.session_state.language),
                                 value=user_data['name'])
            age = st.number_input(translate_text("Age",
                                                 st.session_state.language),
                                  value=user_data['age'],
                                  min_value=18,
                                  max_value=100)

        with col2:
            email = st.text_input(translate_text("Email",
                                                 st.session_state.language),
                                  value=user_data['email'],
                                  disabled=True)
            monthly_income = st.number_input(
                translate_text("Monthly Income (₹)",
                               st.session_state.language),
                value=int(user_data['monthly_income']),
                min_value=0)

        if st.button(
                translate_text("Update Profile", st.session_state.language)):
            db.update_user_profile(st.session_state.user_id, name, age,
                                   monthly_income)
            st.success(
                translate_text("Profile updated successfully!",
                               st.session_state.language))
            st.rerun()

        # Profile statistics
        st.subheader(
            translate_text("Your Financial Journey",
                           st.session_state.language))

        transactions = db.get_user_transactions(st.session_state.user_id)
        goals = db.get_user_goals(st.session_state.user_id)
        learning_progress = db.get_learning_progress(st.session_state.user_id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                translate_text("Total Transactions",
                               st.session_state.language), len(transactions))
        with col2:
            st.metric(
                translate_text("Active Goals", st.session_state.language),
                len(goals))
        with col3:
            st.metric(
                translate_text("Modules Completed", st.session_state.language),
                len(learning_progress))

    with tab2:
        st.subheader(translate_text("App Settings", st.session_state.language))

        # Notification preferences
        st.checkbox(translate_text("Email Notifications",
                                   st.session_state.language),
                    value=True)
        st.checkbox(translate_text("Goal Reminders",
                                   st.session_state.language),
                    value=True)
        st.checkbox(translate_text("Educational Content Updates",
                                   st.session_state.language),
                    value=True)

        # Data export
        st.subheader(
            translate_text("Data Management", st.session_state.language))

        if st.button(
                translate_text("Export My Data", st.session_state.language)):
            user_data = {
                'profile':
                db.get_user_profile(st.session_state.user_id),
                'transactions':
                db.get_user_transactions(st.session_state.user_id),
                'goals':
                db.get_user_goals(st.session_state.user_id),
                'learning_progress':
                db.get_learning_progress(st.session_state.user_id)
            }

            json_data = json.dumps(user_data, indent=2, default=str)
            st.download_button(
                label=translate_text("Download Data as JSON",
                                     st.session_state.language),
                data=json_data,
                file_name=f"shefin_data_{st.session_state.user_id}.json",
                mime="application/json")

        # Logout
        if st.button(translate_text("Logout", st.session_state.language)):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.rerun()


def show_mood_tracker():
    st.title("😊 Money Mood Tracker")

    tab1, tab2, tab3 = st.tabs(
        ["Today's Mood", "Mood Insights", "Mood Calendar"])

    with tab1:
        st.subheader("How are you feeling about money today?")

        # Mood selection with emojis
        col1, col2 = st.columns([2, 1])

        with col1:
            mood_options = {}
            for key, data in mood_tracker.mood_categories.items():
                mood_options[
                    f"{data['emoji']} {data['name']} - {data['description']}"] = key

            selected_mood_display = st.selectbox(
                "Select your current money mood:", list(mood_options.keys()))
            selected_mood = mood_options[selected_mood_display]

            # Mood intensity
            intensity = st.slider(
                "How strong is this feeling? (1=mild, 5=very strong)", 1, 5, 3)

            # Spending trigger
            spending_trigger = st.selectbox(
                "What triggered this feeling today?",
                ["None"] + list(mood_tracker.spending_triggers.values()))

            # Optional spending amount
            amount_spent = st.number_input("Amount spent today (if any) ₹",
                                           min_value=0.0,
                                           value=0.0)

            # Notes
            notes = st.text_area(
                "Any additional notes about your money mood today?",
                max_chars=200)

        with col2:
            # Display selected mood emoji large
            if selected_mood:
                mood_emoji = mood_tracker.mood_categories[selected_mood][
                    'emoji']
                st.markdown(f"""
                <div style="text-align: center; font-size: 100px; margin: 20px 0;">
                    {mood_emoji}
                </div>
                """,
                            unsafe_allow_html=True)

        # Save mood button
        if st.button("Save Today's Mood", type="primary"):
            trigger_key = None
            if spending_trigger != "None":
                # Find the key for the selected trigger
                for key, value in mood_tracker.spending_triggers.items():
                    if value == spending_trigger:
                        trigger_key = key
                        break

            success = mood_tracker.log_mood(st.session_state.user_id,
                                            selected_mood, intensity,
                                            trigger_key, notes,
                                            int(amount_spent))

            if success:
                st.success("Mood logged successfully! 🎉")
                st.balloons()
            else:
                st.error("Failed to save mood. Please try again.")

    with tab2:
        st.subheader("Your Money Mood Insights")

        # Get insights
        insights = mood_tracker.get_mood_insights(st.session_state.user_id)

        # Display summary
        st.markdown(f"""
        <div class="feature-card">
            <h3>{insights['summary']}</h3>
            <p><strong>Total mood entries:</strong> {insights['total_entries']}</p>
            <p><strong>Emotional spending:</strong> ₹{format_currency(insights['emotional_spending'])}</p>
        </div>
        """,
                    unsafe_allow_html=True)

        # Patterns
        if insights['patterns']:
            st.subheader("Patterns & Trends")
            for pattern in insights['patterns']:
                st.write(f"• {pattern}")

        # Recommendations
        if insights['recommendations']:
            st.subheader("Personalized Recommendations")
            for rec in insights['recommendations']:
                st.write(f"💡 {rec}")

        # Mood streaks
        streaks = mood_tracker.get_mood_streaks(st.session_state.user_id)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Positive Streak",
                      f"{streaks['current_positive_streak']} days")
        with col2:
            st.metric("Best Positive Streak",
                      f"{streaks['best_positive_streak']} days")

        # Charts
        history = mood_tracker.get_mood_history(st.session_state.user_id,
                                                days=30)
        if history:
            # Mood trend chart
            df_history = pd.DataFrame(history)
            df_history['date'] = pd.to_datetime(df_history['date'])

            # Convert mood to numeric for trending
            mood_scores = {
                'excited': 5,
                'happy': 4,
                'confident': 4,
                'neutral': 3,
                'worried': 2,
                'frustrated': 2,
                'stressed': 1,
                'guilty': 1
            }
            df_history['mood_score'] = df_history['mood_type'].map(mood_scores)

            # Line chart for mood trends
            fig = px.line(df_history,
                          x='date',
                          y='mood_score',
                          title="Money Mood Trend (Last 30 Days)",
                          labels={
                              'mood_score': 'Mood Score (1-5)',
                              'date': 'Date'
                          })
            st.plotly_chart(fig, use_container_width=True)

            # Pie chart for mood distribution
            mood_counts = df_history['mood_type'].value_counts()
            fig_pie = px.pie(values=mood_counts.values,
                             names=mood_counts.index,
                             title="Mood Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.subheader("Money Mood Calendar")

        # Month/Year selector
        col1, col2 = st.columns(2)
        with col1:
            selected_month = st.selectbox(
                "Month",
                range(1, 13),
                index=datetime.now().month - 1,
                format_func=lambda x: datetime(2023, x, 1).strftime('%B'))
        with col2:
            selected_year = st.selectbox("Year", range(2023, 2026), index=1)

        # Get calendar data
        calendar_data = mood_tracker.get_mood_calendar_data(
            st.session_state.user_id, selected_month, selected_year)

        # Display calendar view
        st.subheader(
            f"Mood Calendar - {datetime(selected_year, selected_month, 1).strftime('%B %Y')}"
        )

        # Create calendar grid
        import calendar
        cal = calendar.monthcalendar(selected_year, selected_month)

        # Calendar headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        cols = st.columns(7)
        for i, day in enumerate(days):
            cols[i].write(f"**{day}**")

        # Calendar days
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].write("")
                else:
                    mood_data = calendar_data.get(day)
                    if mood_data:
                        emoji = mood_data['emoji']
                        mood_name = mood_data['mood']
                        cols[i].markdown(f"""
                        <div style="text-align: center; padding: 5px; border: 1px solid #ddd; border-radius: 5px;">
                            <div style="font-size: 20px;">{emoji}</div>
                            <div style="font-size: 12px;">{day}</div>
                        </div>
                        """,
                                         unsafe_allow_html=True)
                    else:
                        cols[i].markdown(f"""
                        <div style="text-align: center; padding: 5px;">
                            <div style="font-size: 12px;">{day}</div>
                        </div>
                        """,
                                         unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {e}")
