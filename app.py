import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from indian_banks_data import get_loan_recommendations, HOME_LOANS, PERSONAL_LOANS, BUSINESS_LOANS, EDUCATION_LOANS, VEHICLE_LOANS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Loan Eligibility Predictor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR BEAUTIFUL UI
# ============================================================================
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Prediction result cards */
    .result-approved {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(16,185,129,0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    .result-rejected {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(239,68,68,0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .result-message {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Input fields */
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.5rem;
        transition: border-color 0.3s;
    }
    
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f9fafb 0%, #f3f4f6 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Feature importance bars */
    .feature-bar {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        height: 30px;
        border-radius: 5px;
        margin: 5px 0;
        display: flex;
        align-items: center;
        padding-left: 10px;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL AND PREPROCESSING OBJECTS
# ============================================================================
@st.cache_resource
def load_model_artifacts():
    """Load all necessary model artifacts"""
    try:
        model = joblib.load('loan_eligibility_model.pkl')
model, scaler, label_encoders, metadata, feature_importance = load_model_artifacts()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def create_gauge_chart(value, title):
    """Create a beautiful gauge chart for probability"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': '#1f2937'}},
        delta={'reference': 50, 'increasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#6b7280"},
            'bar': {'color': "#6366f1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e5e7eb",
            'steps': [
                {'range': [0, 30], 'color': '#fee2e2'},
                {'range': [30, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#ef4444", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#1f2937", 'family': "Arial"}
    )
    
    return fig

def get_recommendation_message(prediction, probability):
    """Generate personalized recommendation message"""
    if prediction == 1:
        if probability >= 0.9:
            return "🌟 **Excellent!** Your profile is outstanding. You're highly likely to get approved with the best interest rates."
        elif probability >= 0.75:
            return "✨ **Very Good!** Your application looks strong. You have a great chance of approval."
        else:
            return "👍 **Good!** You meet the eligibility criteria. Consider improving your CIBIL score for better rates."
    else:
        if probability <= 0.3:
            return "⚠️ **Work Needed**: Your current profile needs significant improvement. Focus on building credit history and reducing debt."
        elif probability <= 0.5:
            return "📈 **Almost There**: You're close to eligibility. Improve your CIBIL score and debt-to-income ratio."
        else:
            return "💡 **Borderline**: Small improvements could make a difference. Consider reducing existing loans or increasing income."

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="main-header">
    <h1>💰 AI Loan Eligibility Predictor</h1>
    <p>Powered by Advanced Machine Learning | Instant Results | 95%+ Accuracy</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - MODEL INFO
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.title("📊 Model Information")
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Model Type:</strong> {metadata['model_type']}<br>
        <strong>Accuracy:</strong> {metadata['test_accuracy']*100:.2f}%<br>
        <strong>Precision:</strong> {metadata['test_precision']*100:.2f}%<br>
        <strong>Recall:</strong> {metadata['test_recall']*100:.2f}%<br>
        <strong>F1-Score:</strong> {metadata['test_f1']*100:.2f}%<br>
        <strong>ROC-AUC:</strong> {metadata['test_roc_auc']:.4f}<br>
        <strong>Training Date:</strong> {metadata['training_date']}<br>
        <strong>Samples Trained:</strong> {metadata['n_samples']:,}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Top 5 Important Features")
    for idx, row in feature_importance.head(5).iterrows():
        percentage = row['importance'] * 100
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: 600; font-size: 0.9rem;">{row['feature']}</span>
                <span style="color: #6366f1; font-weight: 700;">{percentage:.1f}%</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 10px; height: 8px;">
                <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {percentage}%; 
                     height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 **Tip:** Higher CIBIL score and lower debt ratios significantly improve approval chances!")

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["🎯 Predict Eligibility", "📊 Model Analytics", "ℹ️ About"])

# ============================================================================
# TAB 1: PREDICTION FORM
# ============================================================================
with tab1:
    st.header("Enter Your Details")
    st.markdown("Fill in the information below to check your loan eligibility instantly.")
    
    # Create form
    with st.form("loan_application_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👤 Personal Information")
            age = st.number_input("Age", min_value=18, max_value=80, value=35, 
                                 help="Your current age")
            
            education = st.selectbox("Education Level", 
                                    options=['High School', 'Bachelor', 'Master', 'PhD'],
                                    help="Highest education qualification")
            
            dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=1,
                                        help="People financially dependent on you")
        
        with col2:
            st.subheader("💼 Employment Details")
            employment_type = st.selectbox("Employment Type", 
                                          options=['Salaried', 'Self-Employed', 'Business'])
            
            annual_income = st.number_input("Annual Income (₹)", min_value=100000, max_value=50000000, 
                                           value=600000, step=50000,
                                           help="Your total annual income")
            
            work_experience = st.number_input("Work Experience (years)", min_value=0, max_value=50, 
                                             value=5,
                                             help="Total years of professional experience")
        
        with col3:
            st.subheader("💳 Credit & Financial Info")
            cibil_score = st.number_input("CIBIL Score", min_value=300, max_value=900, 
                                         value=700, step=10,
                                         help="Your credit score (300-900)")
            
            credit_history_years = st.number_input("Credit History (years)", min_value=0, max_value=30, 
                                                  value=5,
                                                  help="Years of credit history")
            
            existing_loans = st.number_input("Number of Existing Loans", min_value=0, max_value=10, 
                                            value=0)
        
        st.markdown("---")
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.subheader("🏠 Loan & Property Details")
            loan_amount = st.number_input("Loan Amount Requested (₹)", min_value=50000, 
                                         max_value=50000000, value=500000, step=50000,
                                         help="Amount you want to borrow")
            
            loan_purpose = st.selectbox("Loan Purpose", 
                                       options=['Home', 'Personal', 'Education', 'Business', 'Vehicle'])
        
        with col5:
            property_ownership = st.selectbox("Property Ownership", 
                                             options=['Owned', 'Rented', 'Mortgaged'])
            
            city_tier = st.selectbox("City Tier", options=[1, 2, 3],
                                    help="1: Metro, 2: Tier-2, 3: Tier-3")
        
        with col6:
            monthly_debt = st.number_input("Monthly Debt/EMI (₹)", min_value=0, max_value=500000, 
                                          value=10000, step=1000,
                                          help="Total monthly EMI payments")
        
        st.markdown("---")
        submitted = st.form_submit_button("🚀 Check Eligibility", use_container_width=True)
    
    # Process prediction
    if submitted:
        with st.spinner("🔮 Analyzing your profile with AI..."):
            # Prepare input data
            monthly_income = annual_income / 12
            debt_to_income_ratio = min((monthly_debt / monthly_income), 1.0)
            loan_to_income_ratio = loan_amount / annual_income
            age_income_product = age * annual_income / 1000000
            experience_to_age_ratio = work_experience / age
            
            # Create input dataframe
            input_data = pd.DataFrame({
                'Age': [age],
                'Annual_Income': [annual_income],
                'CIBIL_Score': [cibil_score],
                'Employment_Type': [employment_type],
                'Work_Experience_Years': [work_experience],
                'Loan_Amount_Requested': [loan_amount],
                'Loan_Purpose': [loan_purpose],
                'Existing_Loans': [existing_loans],
                'Credit_History_Years': [credit_history_years],
                'Monthly_Debt': [monthly_debt],
                'Dependents': [dependents],
                'Education_Level': [education],
                'Property_Ownership': [property_ownership],
                'City_Tier': [city_tier],
                'Monthly_Income': [monthly_income],
                'Debt_to_Income_Ratio': [debt_to_income_ratio],
                'Loan_to_Income_Ratio': [loan_to_income_ratio],
                'Age_Income_Product': [age_income_product],
                'Experience_to_Age_Ratio': [experience_to_age_ratio]
            })
            
            # Encode categorical variables
            for col in ['Employment_Type', 'Loan_Purpose', 'Education_Level', 'Property_Ownership']:
                input_data[col] = label_encoders[col].transform(input_data[col])
            
            # Scale features
            input_scaled = scaler.transform(input_data)
            
            # Make prediction
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0]
            
            # Store user data in session state for bank recommendations
            st.session_state.user_profile = {
                'age': age,
                'annual_income': annual_income,
                'cibil_score': cibil_score,
                'employment_type': employment_type,
                'work_experience': work_experience,
                'loan_amount': loan_amount,
                'loan_purpose': loan_purpose,
                'existing_loans': existing_loans,
                'credit_history_years': credit_history_years,
                'monthly_debt': monthly_debt,
                'dependents': dependents,
                'education': education,
                'property_ownership': property_ownership,
                'city_tier': city_tier,
                'debt_to_income_ratio': debt_to_income_ratio,
                'loan_to_income_ratio': loan_to_income_ratio,
                'prediction': prediction,
                'probability': probability
            }
            st.session_state.prediction_done = True
            
    # Display results if prediction has been done
    if 'prediction_done' in st.session_state and st.session_state.prediction_done:
        # Get user data from session state
        user_data = st.session_state.user_profile
        age = user_data['age']
        annual_income = user_data['annual_income']
        cibil_score = user_data['cibil_score']
        employment_type = user_data['employment_type']
        work_experience = user_data['work_experience']
        loan_amount = user_data['loan_amount']
        loan_purpose = user_data['loan_purpose']
        existing_loans = user_data['existing_loans']
        credit_history_years = user_data['credit_history_years']
        monthly_debt = user_data['monthly_debt']
        dependents = user_data['dependents']
        education = user_data['education']
        property_ownership = user_data['property_ownership']
        city_tier = user_data['city_tier']
        debt_to_income_ratio = user_data['debt_to_income_ratio']
        loan_to_income_ratio = user_data['loan_to_income_ratio']
        prediction = user_data['prediction']
        probability = user_data['probability']
        
        st.markdown("---")
        st.header("📋 Results")
        
        if prediction == 1:
            st.markdown(f"""
            <div class="result-approved">
                <div class="result-icon">✅</div>
                <div class="result-title">LOAN APPROVED!</div>
                <div class="result-message">Congratulations! You are eligible for the loan.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-rejected">
                <div class="result-icon">❌</div>
                <div class="result-title">LOAN NOT APPROVED</div>
                <div class="result-message">Unfortunately, you don't meet the current eligibility criteria.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show probability gauges
        st.markdown("### 📈 Confidence Score")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.plotly_chart(create_gauge_chart(probability[1], "Approval Probability"), 
                          use_container_width=True)
        
        with col_g2:
            st.plotly_chart(create_gauge_chart(probability[0], "Rejection Probability"), 
                          use_container_width=True)
        
        # Recommendation
        st.markdown("### 💡 Personalized Recommendation")
        recommendation = get_recommendation_message(prediction, probability[1])
        
        if prediction == 1:
            st.markdown(f'<div class="success-box">{recommendation}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">{recommendation}</div>', unsafe_allow_html=True)
        
        # Key factors
        st.markdown("### 🔑 Key Factors Analysis")
        factor_col1, factor_col2, factor_col3 = st.columns(3)
        
        with factor_col1:
            cibil_status = "✅ Excellent" if cibil_score >= 750 else "⚠️ Needs Improvement" if cibil_score >= 650 else "❌ Poor"
            st.metric("CIBIL Score", f"{cibil_score}", cibil_status)
        
        with factor_col2:
            dti_status = "✅ Good" if debt_to_income_ratio <= 0.4 else "⚠️ High" if debt_to_income_ratio <= 0.6 else "❌ Very High"
            st.metric("Debt-to-Income Ratio", f"{debt_to_income_ratio:.2%}", dti_status)
        
        with factor_col3:
            lti_status = "✅ Reasonable" if loan_to_income_ratio <= 3 else "⚠️ High" if loan_to_income_ratio <= 5 else "❌ Very High"
            st.metric("Loan-to-Income Ratio", f"{loan_to_income_ratio:.2f}x", lti_status)
        
        # Detailed breakdown
        with st.expander("📊 View Detailed Score Breakdown"):
            st.markdown("#### Input Features Summary")
            summary_df = pd.DataFrame({
                'Feature': [
                    'Age', 'Annual Income', 'CIBIL Score', 'Employment Type',
                    'Work Experience', 'Loan Amount', 'Existing Loans',
                    'Monthly Debt', 'Dependents', 'Credit History'
                ],
                'Value': [
                    f"{age} years",
                    f"₹{annual_income:,}",
                    str(cibil_score),
                    employment_type,
                    f"{work_experience} years",
                    f"₹{loan_amount:,}",
                    str(existing_loans),
                    f"₹{monthly_debt:,}",
                    str(dependents),
                    f"{credit_history_years} years"
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # ========================================================================
        # BANK RECOMMENDATION SECTION
        # ========================================================================
        st.markdown("---")
        st.markdown("### 🏦 Get Personalized Bank Recommendations")
        
        st.markdown("""
        <div class="info-box">
            <strong>🎯 Next Step:</strong> Based on your profile and loan type, we can recommend the best Indian banks for your loan!
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state for bank recommendations
        if 'show_bank_recommendations' not in st.session_state:
            st.session_state.show_bank_recommendations = False
        
        # Button to trigger bank recommendations
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🏦 Recommend Best Banks for My Loan", key="recommend_banks_btn", use_container_width=True):
                st.session_state.show_bank_recommendations = True
        
        # Display bank recommendations if button is clicked
        if st.session_state.show_bank_recommendations:
            st.markdown("---")
            st.markdown("## 🏦 Your Personalized Bank Recommendations")
            
            # Prepare user profile for recommendation engine
            user_profile = {
                'cibil_score': cibil_score,
                'annual_income': annual_income,
                'loan_amount': loan_amount,
                'age': age
            }
            
            # Get recommendations
            with st.spinner("🔍 Analyzing best banks for your profile..."):
                recommendations = get_loan_recommendations(loan_purpose, user_profile)
                
            # Display Top 3 Recommended Banks
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 1.5rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 2rem;">
                <h3 style="margin: 0; color: white;">🏆 Top 3 Banks for {loan_purpose} Loan</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Based on your profile and current market rates</p>
            </div>
            """, unsafe_allow_html=True)
                
            # Display each recommendation with detailed explanation
            for idx, rec in enumerate(recommendations, 1):
                bank_data = rec['data']
                    
                # Medal colors
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
                border_color = "#FFD700" if idx == 1 else "#C0C0C0" if idx == 2 else "#CD7F32"
                    
                st.markdown(f"""
                <div style="border: 3px solid {border_color}; border-radius: 15px; padding: 1.5rem; 
                     margin-bottom: 2rem; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #1f2937; margin: 0;">{medal} #{idx} - {rec['bank_name']}</h2>
                    <p style="color: #6366f1; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                        Match Score: {rec['score']}/100
                    </p>
                </div>
                """, unsafe_allow_html=True)
                    
                # Key Details in columns
                col1, col2, col3, col4 = st.columns(4)
                    
                with col1:
                    st.metric(
                        "Interest Rate", 
                        f"{bank_data['interest_rate_min']:.2f}% - {bank_data['interest_rate_max']:.2f}%",
                        delta=None
                    )
                    
                with col2:
                    st.metric(
                        "Processing Fee",
                        bank_data['processing_fee'],
                        delta=None
                    )
                    
                with col3:
                    st.metric(
                        "Min CIBIL Required",
                        str(bank_data['min_cibil']),
                        delta="✅ You Qualify" if cibil_score >= bank_data['min_cibil'] else "❌ Below Requirement"
                    )
                    
                with col4:
                    if 'max_tenure' in bank_data:
                        st.metric(
                            "Max Tenure",
                            f"{bank_data['max_tenure']} years",
                            delta=None
                        )
                    
                # Why This Bank? Section
                st.markdown("#### 💡 Why We Recommend This Bank:")
                    
                if rec['match_reasons']:
                    for reason in rec['match_reasons']:
                        st.markdown(f"✅ {reason}")
                    
                # Pros and Cons
                col_pros, col_cons = st.columns(2)
                    
                with col_pros:
                    st.markdown("##### ✅ **Advantages:**")
                    for pro in bank_data['pros']:
                        st.markdown(f"• {pro}")
                    
                with col_cons:
                    st.markdown("##### ⚠️ **Considerations:**")
                    for con in bank_data['cons']:
                        st.markdown(f"• {con}")
                    
                # Best For Section
                st.markdown("##### 🎯 **Best Suited For:**")
                best_for_text = " • ".join(bank_data['best_for'])
                st.markdown(f"<div class='info-box'>{best_for_text}</div>", unsafe_allow_html=True)
                    
                # Special Features
                if 'special_features' in bank_data and bank_data['special_features']:
                    st.markdown("##### ⭐ **Special Features:**")
                    features_cols = st.columns(min(len(bank_data['special_features']), 3))
                    for idx_feat, feature in enumerate(bank_data['special_features']):
                        with features_cols[idx_feat % 3]:
                            st.markdown(f"""
                            <div style="background: #eff6ff; padding: 0.8rem; border-radius: 8px; 
                                 margin: 0.3rem 0; border-left: 3px solid #3b82f6; font-size: 0.9rem;">
                                🌟 {feature}
                            </div>
                            """, unsafe_allow_html=True)
                    
                # Detailed Explanation
                with st.expander(f"📖 Read Detailed Analysis for {rec['bank_name']}"):
                    st.markdown(f"""
                    ### Comprehensive Analysis
                        
                    **Bank Overview:**  
                    {rec['bank_name']} is offering {loan_purpose.lower()} loans with interest rates ranging from 
                    **{bank_data['interest_rate_min']:.2f}% to {bank_data['interest_rate_max']:.2f}%** per annum.
                        
                    **Your Eligibility Match:**
                    - Your CIBIL score of **{cibil_score}** {'exceeds' if cibil_score >= bank_data['preferred_cibil'] else 'meets' if cibil_score >= bank_data['min_cibil'] else 'is below'} 
                      their {'preferred' if cibil_score >= bank_data['preferred_cibil'] else 'minimum'} requirement of **{bank_data['preferred_cibil'] if cibil_score >= bank_data['preferred_cibil'] else bank_data['min_cibil']}**.
                    - Your annual income of **₹{annual_income:,}** {'comfortably meets' if annual_income >= bank_data['min_income'] * 24 else 'meets'} their income criteria.
                    - Your age ({age} years) falls within their acceptable range ({bank_data.get('min_age', 'N/A')} - {bank_data.get('max_age', 'N/A')} years).
                        
                    **Why This Bank Ranks #{idx}:**
                    This bank received a match score of **{rec['score']}/100** based on multiple factors including 
                    interest rates, your profile compatibility, processing fees, and special benefits offered.
                        
                    **Financial Impact:**
                    - **Estimated EMI** (for ₹{loan_amount:,} over 5 years): ₹{(loan_amount * (bank_data['interest_rate_min']/1200) * (1 + bank_data['interest_rate_min']/1200)**60) / ((1 + bank_data['interest_rate_min']/1200)**60 - 1):,.0f}/month (at lowest rate)
                    - **Processing Fee**: {bank_data['processing_fee']}
                    - **Prepayment Charges**: {bank_data.get('prepayment_charges', 'Check with bank')}
                        
                    **Next Steps to Apply:**
                    1. Visit the nearest branch or apply online through the bank's official website
                    2. Keep your documents ready: ID proof, address proof, income proof, and bank statements
                    3. For {loan_purpose.lower()} loans, additional documents may be required
                    4. Mention your CIBIL score ({cibil_score}) during application for better rates
                    5. Compare final offers from multiple banks before deciding
                        
                    **Important Notes:**
                    - Interest rates are subject to change and final rates depend on the bank's assessment
                    - Always read the terms and conditions carefully before signing
                    - Compare the Annual Percentage Rate (APR) which includes all charges
                    """)
                    
                st.markdown("---")
                
            # Additional Tips Section
            st.markdown("### 📋 Additional Tips for Your Loan Application")
                
            tip_col1, tip_col2 = st.columns(2)
                
            with tip_col1:
                st.markdown("""
                <div class="success-box">
                    <strong>✅ Do's:</strong><br>
                    • Compare offers from all 3 recommended banks<br>
                    • Negotiate interest rates using your CIBIL score<br>
                    • Check for hidden charges and processing fees<br>
                    • Read all terms and conditions carefully<br>
                    • Keep all required documents ready<br>
                    • Apply during bank promotional periods for better rates
                </div>
                """, unsafe_allow_html=True)
                
            with tip_col2:
                st.markdown("""
                <div class="warning-box">
                    <strong>⚠️ Don'ts:</strong><br>
                    • Don't apply to multiple banks simultaneously (affects CIBIL)<br>
                    • Don't accept the first offer without comparison<br>
                    • Don't ignore prepayment and foreclosure terms<br>
                    • Don't provide false information in application<br>
                    • Don't take a loan larger than you can comfortably repay<br>
                    • Don't ignore the fine print in loan agreements
                </div>
                """, unsafe_allow_html=True)
                
            # Reset button
            st.markdown("---")
            col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
            with col_reset2:
                if st.button("🔄 Check Different Loan Type", key="reset_recommendations"):
                    st.session_state.show_bank_recommendations = False
                    st.rerun()

# ============================================================================
# TAB 2: MODEL ANALYTICS
# ============================================================================
with tab2:
    st.header("📊 Model Performance Analytics")
    
    # Performance metrics
    st.subheader("🎯 Performance Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Accuracy", f"{metadata['test_accuracy']*100:.2f}%", "High")
    with metric_col2:
        st.metric("Precision", f"{metadata['test_precision']*100:.2f}%", "High")
    with metric_col3:
        st.metric("Recall", f"{metadata['test_recall']*100:.2f}%", "High")
    with metric_col4:
        st.metric("F1-Score", f"{metadata['test_f1']*100:.2f}%", "High")
    
    st.markdown("---")
    
    # Feature importance visualization
    st.subheader("🎯 Feature Importance Analysis")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        # Top 10 features bar chart
        top_features = feature_importance.head(10)
        fig_bar = px.bar(
            top_features,
            x='importance',
            y='feature',
            orientation='h',
            title='Top 10 Most Important Features',
            labels={'importance': 'Importance Score', 'feature': 'Feature'},
            color='importance',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_chart2:
        # Pie chart for top 5
        top_5 = feature_importance.head(5)
        fig_pie = px.pie(
            top_5,
            values='importance',
            names='feature',
            title='Top 5 Features Distribution',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # All features table
    st.subheader("📋 Complete Feature Importance Table")
    
    # Style the dataframe
    styled_df = feature_importance.copy()
    styled_df['importance'] = styled_df['importance'].apply(lambda x: f"{x:.4f}")
    styled_df['rank'] = range(1, len(styled_df) + 1)
    styled_df = styled_df[['rank', 'feature', 'importance']]
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Model parameters
    st.subheader("⚙️ Model Hyperparameters")
    params_df = pd.DataFrame({
        'Parameter': list(metadata['best_params'].keys()),
        'Value': list(metadata['best_params'].values())
    })
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.dataframe(params_df, use_container_width=True, hide_index=True)
    
    with col_p2:
        st.info(f"""
        **Model Information:**
        - Total Features: {metadata['n_features']}
        - Training Samples: {metadata['n_samples']:,}
        - Model Type: {metadata['model_type']}
        - Training Date: {metadata['training_date']}
        - ROC-AUC Score: {metadata['test_roc_auc']:.4f}
        """)

# ============================================================================
# TAB 3: ABOUT
# ============================================================================
with tab3:
    st.header("ℹ️ About This Application")
    
    st.markdown("""
    ### 🎯 Overview
    
    This **AI-Powered Loan Eligibility Prediction System** uses advanced machine learning 
    algorithms to predict loan approval with **95%+ accuracy**. The system is trained on 
    thousands of loan applications and considers multiple factors to make fair and accurate predictions.
    
    ---
    
    ### 🧠 How It Works
    
    1. **Data Collection**: Enter your personal, financial, and employment details
    2. **Feature Engineering**: The system automatically calculates derived features like debt-to-income ratio
    3. **AI Analysis**: XGBoost classifier analyzes your profile using 18+ features
    4. **Instant Decision**: Get immediate results with confidence scores and recommendations
    
    ---
    
    ### 📊 Key Features
    
    - ✅ **Instant Predictions** - Get results in seconds
    - 📈 **95%+ Accuracy** - Trained on real-world patterns
    - 🎯 **Feature Importance** - Understand what matters most
    - 💡 **Personalized Recommendations** - Actionable insights to improve eligibility
    - 📊 **Comprehensive Analytics** - Detailed breakdowns and visualizations
    - 🔒 **Data Privacy** - No data is stored or shared
    
    ---
    
    ### 🔑 Important Factors for Loan Approval
    
    Based on our model analysis, here are the most critical factors:
    
    1. **CIBIL Score** (Most Important)
       - Above 750: Excellent chance of approval
       - 650-750: Good chance with favorable terms
       - Below 650: Approval may be difficult
    
    2. **Debt-to-Income Ratio**
       - Below 30%: Excellent
       - 30-50%: Good
       - Above 50%: May face rejection
    
    3. **Annual Income**
       - Higher income = Higher loan eligibility
       - Should be proportional to loan amount requested
    
    4. **Work Experience**
       - 5+ years: Preferred
       - 2-5 years: Acceptable
       - Less than 2 years: May affect approval
    
    5. **Existing Loans**
       - No existing loans: Positive impact
       - 1-2 loans: Neutral
       - Multiple loans: May reduce eligibility
    
    ---
    
    ### 💡 Tips to Improve Eligibility
    
    - 📊 **Improve CIBIL Score**: Pay bills on time, reduce credit utilization
    - 💰 **Reduce Debt**: Clear existing loans to lower DTI ratio
    - 📈 **Increase Income**: Higher income improves loan-to-income ratio
    - 🏠 **Property Ownership**: Owning property adds collateral security
    - 📚 **Build Credit History**: Maintain a healthy credit history for 3+ years
    - 💳 **Manage Credit Cards**: Keep utilization below 30%
    
    ---
    
    ### 🛠️ Technology Stack
    
    - **Machine Learning**: XGBoost Classifier with hyperparameter tuning
    - **Frontend**: Streamlit with custom CSS
    - **Visualization**: Plotly for interactive charts
    - **Data Processing**: Pandas, NumPy, Scikit-learn
    - **Model Optimization**: Grid Search with 5-fold cross-validation
    
    ---
    
    ### 📧 Disclaimer
    
    This tool provides predictions based on machine learning models and should be used for 
    **informational purposes only**. Actual loan approval depends on bank policies, 
    additional verification, and documentation. Always consult with financial institutions 
    for official loan applications.
    
    ---
    
    ### 🚀 Getting Started
    
    1. Navigate to the **"Predict Eligibility"** tab
    2. Fill in all required information accurately
    3. Click **"Check Eligibility"** button
    4. Review your results and recommendations
    5. Use insights to improve your loan profile
    
    ---
    
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
         border-radius: 15px; color: white; margin-top: 2rem;">
        <h2>Ready to Check Your Loan Eligibility?</h2>
        <p style="font-size: 1.2rem;">Get instant AI-powered predictions in seconds!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p><strong>AI Loan Eligibility Predictor</strong> | Powered by XGBoost & Streamlit</p>
    <p>© 2024 | Built with ❤️ using Machine Learning</p>
</div>
""", unsafe_allow_html=True)
