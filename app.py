import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import subprocess
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
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 { color: white; font-size: 3rem; font-weight: 800; margin: 0; }
    .main-header p { color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem; }
    .result-approved {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 2rem; border-radius: 15px; text-align: center; color: white;
        box-shadow: 0 10px 30px rgba(16,185,129,0.3);
    }
    .result-rejected {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2rem; border-radius: 15px; text-align: center; color: white;
        box-shadow: 0 10px 30px rgba(239,68,68,0.3);
    }
    .result-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; }
    .result-message { font-size: 1.2rem; opacity: 0.95; }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; padding: 0.75rem 2rem;
        font-size: 1.1rem; font-weight: 600; border-radius: 10px;
    }
    .info-box {
        background: #eff6ff; border-left: 4px solid #3b82f6;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4; border-left: 4px solid #10b981;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .warning-box {
        background: #fffbeb; border-left: 4px solid #f59e0b;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL — auto-trains if pkl files missing
# ============================================================================
@st.cache_resource
def load_model_artifacts():
    if not os.path.exists('loan_eligibility_model.pkl'):
        with st.spinner("Training model for the first time — this takes about 60 seconds..."):
            subprocess.run(['python', 'train_model.py'], check=True)
    try:
        model            = joblib.load('loan_eligibility_model.pkl')
        scaler           = joblib.load('scaler.pkl')
        label_encoders   = joblib.load('label_encoders.pkl')
        with open('model_metadata.json', 'r') as f:
            metadata     = json.load(f)
        feature_importance = pd.read_csv('feature_importance.csv')
        return model, scaler, label_encoders, metadata, feature_importance
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        st.stop()

# ── Call the function and unpack OUTSIDE and AFTER the function definition ──
artifacts = load_model_artifacts()
if artifacts is None:
    st.stop()
model, scaler, label_encoders, metadata, feature_importance = artifacts

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def create_gauge_chart(value, title):
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
                {'range': [0, 30],  'color': '#fee2e2'},
                {'range': [30, 70], 'color': '#fef3c7'},
                {'range': [70, 100],'color': '#d1fae5'}
            ],
            'threshold': {'line': {'color': "#ef4444", 'width': 4}, 'thickness': 0.75, 'value': 50}
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
    if prediction == 1:
        if probability >= 0.9:
            return "🌟 **Excellent!** Your profile is outstanding. Highly likely to get approved with the best rates."
        elif probability >= 0.75:
            return "✨ **Very Good!** Your application looks strong. Great chance of approval."
        else:
            return "👍 **Good!** You meet the criteria. Consider improving your CIBIL score for better rates."
    else:
        if probability <= 0.3:
            return "⚠️ **Work Needed**: Significant improvement needed. Focus on credit history and reducing debt."
        elif probability <= 0.5:
            return "📈 **Almost There**: Improve your CIBIL score and debt-to-income ratio."
        else:
            return "💡 **Borderline**: Small improvements could make a difference."

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
# SIDEBAR
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
    for _, row in feature_importance.head(5).iterrows():
        percentage = row['importance'] * 100
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: 600; font-size: 0.9rem;">{row['feature']}</span>
                <span style="color: #6366f1; font-weight: 700;">{percentage:.1f}%</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 10px; height: 8px;">
                <div style="background: linear-gradient(90deg, #667eea, #764ba2);
                     width: {percentage}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("💡 **Tip:** Higher CIBIL score and lower debt ratios significantly improve approval chances!")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["🎯 Predict Eligibility", "📊 Model Analytics", "ℹ️ About"])

# ============================================================================
# TAB 1: PREDICTION
# ============================================================================
with tab1:
    st.header("Enter Your Details")
    st.markdown("Fill in the information below to check your loan eligibility instantly.")

    with st.form("loan_application_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("👤 Personal Information")
            age         = st.number_input("Age", min_value=18, max_value=80, value=35)
            education   = st.selectbox("Education Level", ['High School', 'Bachelor', 'Master', 'PhD'])
            dependents  = st.number_input("Number of Dependents", min_value=0, max_value=10, value=1)

        with col2:
            st.subheader("💼 Employment Details")
            employment_type = st.selectbox("Employment Type", ['Salaried', 'Self-Employed', 'Business'])
            annual_income   = st.number_input("Annual Income (₹)", min_value=100000, max_value=50000000, value=600000, step=50000)
            work_experience = st.number_input("Work Experience (years)", min_value=0, max_value=50, value=5)

        with col3:
            st.subheader("💳 Credit & Financial Info")
            cibil_score          = st.number_input("CIBIL Score", min_value=300, max_value=900, value=700, step=10)
            credit_history_years = st.number_input("Credit History (years)", min_value=0, max_value=30, value=5)
            existing_loans       = st.number_input("Number of Existing Loans", min_value=0, max_value=10, value=0)

        st.markdown("---")
        col4, col5, col6 = st.columns(3)

        with col4:
            st.subheader("🏠 Loan & Property Details")
            loan_amount  = st.number_input("Loan Amount Requested (₹)", min_value=50000, max_value=50000000, value=500000, step=50000)
            loan_purpose = st.selectbox("Loan Purpose", ['Home', 'Personal', 'Education', 'Business', 'Vehicle'])

        with col5:
            property_ownership = st.selectbox("Property Ownership", ['Owned', 'Rented', 'Mortgaged'])
            city_tier          = st.selectbox("City Tier", options=[1, 2, 3], help="1: Metro, 2: Tier-2, 3: Tier-3")

        with col6:
            monthly_debt = st.number_input("Monthly Debt/EMI (₹)", min_value=0, max_value=500000, value=10000, step=1000)

        st.markdown("---")
        submitted = st.form_submit_button("🚀 Check Eligibility", use_container_width=True)

    if submitted:
        with st.spinner("🔮 Analyzing your profile with AI..."):
            monthly_income         = annual_income / 12
            debt_to_income_ratio   = min((monthly_debt / monthly_income), 1.0)
            loan_to_income_ratio   = loan_amount / annual_income
            age_income_product     = age * annual_income / 1000000
            experience_to_age_ratio= work_experience / age

            input_data = pd.DataFrame({
                'Age': [age], 'Annual_Income': [annual_income],
                'CIBIL_Score': [cibil_score], 'Employment_Type': [employment_type],
                'Work_Experience_Years': [work_experience], 'Loan_Amount_Requested': [loan_amount],
                'Loan_Purpose': [loan_purpose], 'Existing_Loans': [existing_loans],
                'Credit_History_Years': [credit_history_years], 'Monthly_Debt': [monthly_debt],
                'Dependents': [dependents], 'Education_Level': [education],
                'Property_Ownership': [property_ownership], 'City_Tier': [city_tier],
                'Monthly_Income': [monthly_income], 'Debt_to_Income_Ratio': [debt_to_income_ratio],
                'Loan_to_Income_Ratio': [loan_to_income_ratio],
                'Age_Income_Product': [age_income_product],
                'Experience_to_Age_Ratio': [experience_to_age_ratio]
            })

            for col in ['Employment_Type', 'Loan_Purpose', 'Education_Level', 'Property_Ownership']:
                input_data[col] = label_encoders[col].transform(input_data[col])

            input_scaled = scaler.transform(input_data)
            prediction   = model.predict(input_scaled)[0]
            probability  = model.predict_proba(input_scaled)[0]

            st.session_state.user_profile = {
                'age': age, 'annual_income': annual_income, 'cibil_score': cibil_score,
                'employment_type': employment_type, 'work_experience': work_experience,
                'loan_amount': loan_amount, 'loan_purpose': loan_purpose,
                'existing_loans': existing_loans, 'credit_history_years': credit_history_years,
                'monthly_debt': monthly_debt, 'dependents': dependents, 'education': education,
                'property_ownership': property_ownership, 'city_tier': city_tier,
                'debt_to_income_ratio': debt_to_income_ratio,
                'loan_to_income_ratio': loan_to_income_ratio,
                'prediction': prediction, 'probability': probability
            }
            st.session_state.prediction_done = True

    if 'prediction_done' in st.session_state and st.session_state.prediction_done:
        d = st.session_state.user_profile
        age = d['age']; annual_income = d['annual_income']; cibil_score = d['cibil_score']
        employment_type = d['employment_type']; work_experience = d['work_experience']
        loan_amount = d['loan_amount']; loan_purpose = d['loan_purpose']
        existing_loans = d['existing_loans']; credit_history_years = d['credit_history_years']
        monthly_debt = d['monthly_debt']; dependents = d['dependents']
        education = d['education']; property_ownership = d['property_ownership']
        city_tier = d['city_tier']; debt_to_income_ratio = d['debt_to_income_ratio']
        loan_to_income_ratio = d['loan_to_income_ratio']
        prediction = d['prediction']; probability = d['probability']

        st.markdown("---")
        st.header("📋 Results")

        if prediction == 1:
            st.markdown("""
            <div class="result-approved">
                <div class="result-title">✅ LOAN APPROVED!</div>
                <div class="result-message">Congratulations! You are eligible for the loan.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-rejected">
                <div class="result-title">❌ LOAN NOT APPROVED</div>
                <div class="result-message">Unfortunately, you don't meet the current eligibility criteria.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("### 📈 Confidence Score")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(create_gauge_chart(probability[1], "Approval Probability"), use_container_width=True)
        with col_g2:
            st.plotly_chart(create_gauge_chart(probability[0], "Rejection Probability"), use_container_width=True)

        st.markdown("### 💡 Personalized Recommendation")
        recommendation = get_recommendation_message(prediction, probability[1])
        box_class = "success-box" if prediction == 1 else "warning-box"
        st.markdown(f'<div class="{box_class}">{recommendation}</div>', unsafe_allow_html=True)

        st.markdown("### 🔑 Key Factors Analysis")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            status = "✅ Excellent" if cibil_score >= 750 else "⚠️ Needs Improvement" if cibil_score >= 650 else "❌ Poor"
            st.metric("CIBIL Score", f"{cibil_score}", status)
        with fc2:
            status = "✅ Good" if debt_to_income_ratio <= 0.4 else "⚠️ High" if debt_to_income_ratio <= 0.6 else "❌ Very High"
            st.metric("Debt-to-Income Ratio", f"{debt_to_income_ratio:.2%}", status)
        with fc3:
            status = "✅ Reasonable" if loan_to_income_ratio <= 3 else "⚠️ High" if loan_to_income_ratio <= 5 else "❌ Very High"
            st.metric("Loan-to-Income Ratio", f"{loan_to_income_ratio:.2f}x", status)

        with st.expander("📊 View Detailed Score Breakdown"):
            summary_df = pd.DataFrame({
                'Feature': ['Age','Annual Income','CIBIL Score','Employment Type','Work Experience',
                            'Loan Amount','Existing Loans','Monthly Debt','Dependents','Credit History'],
                'Value': [f"{age} years", f"₹{annual_income:,}", str(cibil_score), employment_type,
                          f"{work_experience} years", f"₹{loan_amount:,}", str(existing_loans),
                          f"₹{monthly_debt:,}", str(dependents), f"{credit_history_years} years"]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 🏦 Get Personalized Bank Recommendations")
        st.markdown('<div class="info-box"><strong>🎯 Next Step:</strong> We can recommend the best Indian banks for your loan!</div>', unsafe_allow_html=True)

        if 'show_bank_recommendations' not in st.session_state:
            st.session_state.show_bank_recommendations = False

        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            if st.button("🏦 Recommend Best Banks for My Loan", key="recommend_banks_btn", use_container_width=True):
                st.session_state.show_bank_recommendations = True

        if st.session_state.show_bank_recommendations:
            st.markdown("---")
            st.markdown("## 🏦 Your Personalized Bank Recommendations")
            user_profile = {'cibil_score': cibil_score, 'annual_income': annual_income,
                            'loan_amount': loan_amount, 'age': age}
            with st.spinner("🔍 Analyzing best banks for your profile..."):
                recommendations = get_loan_recommendations(loan_purpose, user_profile)

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                 padding: 1.5rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 2rem;">
                <h3 style="margin: 0; color: white;">🏆 Top 3 Banks for {loan_purpose} Loan</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Based on your profile and current market rates</p>
            </div>""", unsafe_allow_html=True)

            for rank, rec in enumerate(recommendations, 1):
                bank_data   = rec['data']
                medal       = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                border_color= "#FFD700" if rank == 1 else "#C0C0C0" if rank == 2 else "#CD7F32"

                st.markdown(f"""
                <div style="border: 3px solid {border_color}; border-radius: 15px; padding: 1.5rem;
                     margin-bottom: 2rem; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #1f2937; margin: 0;">{medal} #{rank} - {rec['bank_name']}</h2>
                    <p style="color: #6366f1; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                        Match Score: {rec['score']}/100</p>
                </div>""", unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("Interest Rate", f"{bank_data['interest_rate_min']:.2f}% - {bank_data['interest_rate_max']:.2f}%")
                with c2:
                    st.metric("Processing Fee", bank_data['processing_fee'])
                with c3:
                    qualifies = "✅ You Qualify" if cibil_score >= bank_data['min_cibil'] else "❌ Below Requirement"
                    st.metric("Min CIBIL Required", str(bank_data['min_cibil']), delta=qualifies)
                with c4:
                    if 'max_tenure' in bank_data:
                        st.metric("Max Tenure", f"{bank_data['max_tenure']} years")

                st.markdown("#### 💡 Why We Recommend This Bank:")
                for reason in rec['match_reasons']:
                    st.markdown(f"✅ {reason}")

                cp, cc = st.columns(2)
                with cp:
                    st.markdown("##### ✅ **Advantages:**")
                    for pro in bank_data['pros']:
                        st.markdown(f"• {pro}")
                with cc:
                    st.markdown("##### ⚠️ **Considerations:**")
                    for con in bank_data['cons']:
                        st.markdown(f"• {con}")

                st.markdown("##### 🎯 **Best Suited For:**")
                st.markdown(f'<div class="info-box">{" • ".join(bank_data["best_for"])}</div>', unsafe_allow_html=True)

                if bank_data.get('special_features'):
                    st.markdown("##### ⭐ **Special Features:**")
                    feat_cols = st.columns(min(len(bank_data['special_features']), 3))
                    for fi, feat in enumerate(bank_data['special_features']):
                        with feat_cols[fi % 3]:
                            st.markdown(f"""
                            <div style="background:#eff6ff;padding:0.8rem;border-radius:8px;
                                 margin:0.3rem 0;border-left:3px solid #3b82f6;font-size:0.9rem;">
                                🌟 {feat}</div>""", unsafe_allow_html=True)

                emi = (loan_amount * (bank_data['interest_rate_min']/1200) *
                       (1 + bank_data['interest_rate_min']/1200)**60) / \
                      ((1 + bank_data['interest_rate_min']/1200)**60 - 1)

                with st.expander(f"📖 Read Detailed Analysis for {rec['bank_name']}"):
                    meets = 'exceeds' if cibil_score >= bank_data['preferred_cibil'] else \
                            'meets' if cibil_score >= bank_data['min_cibil'] else 'is below'
                    req_type = 'preferred' if cibil_score >= bank_data['preferred_cibil'] else 'minimum'
                    req_val  = bank_data['preferred_cibil'] if cibil_score >= bank_data['preferred_cibil'] else bank_data['min_cibil']
                    income_meets = 'comfortably meets' if annual_income >= bank_data['min_income'] * 24 else 'meets'
                    st.markdown(f"""
### Comprehensive Analysis

**Bank Overview:**
{rec['bank_name']} offers {loan_purpose.lower()} loans at **{bank_data['interest_rate_min']:.2f}% – {bank_data['interest_rate_max']:.2f}%** p.a.

**Your Eligibility Match:**
- CIBIL score **{cibil_score}** {meets} their {req_type} requirement of **{req_val}**
- Annual income ₹{annual_income:,} {income_meets} their income criteria
- Age {age} years falls within their range ({bank_data.get('min_age','N/A')} – {bank_data.get('max_age','N/A')})

**Financial Impact:**
- Estimated EMI (₹{loan_amount:,} over 5 years): ₹{emi:,.0f}/month at lowest rate
- Processing Fee: {bank_data['processing_fee']}
- Prepayment Charges: {bank_data.get('prepayment_charges','Check with bank')}

**Next Steps:**
1. Visit the bank's official website or nearest branch
2. Keep ID proof, address proof, income proof, and bank statements ready
3. Mention your CIBIL score ({cibil_score}) for better rates
4. Compare final offers before deciding
                    """)
                st.markdown("---")

            tc1, tc2 = st.columns(2)
            with tc1:
                st.markdown("""
                <div class="success-box"><strong>✅ Do's:</strong><br>
                • Compare offers from all 3 banks<br>• Negotiate using your CIBIL score<br>
                • Check for hidden charges<br>• Read all terms carefully<br>
                • Keep documents ready</div>""", unsafe_allow_html=True)
            with tc2:
                st.markdown("""
                <div class="warning-box"><strong>⚠️ Don'ts:</strong><br>
                • Don't apply to multiple banks simultaneously<br>• Don't accept the first offer<br>
                • Don't ignore prepayment terms<br>• Don't provide false information<br>
                • Don't borrow more than you can repay</div>""", unsafe_allow_html=True)

            st.markdown("---")
            _, col_reset, _ = st.columns([1, 2, 1])
            with col_reset:
                if st.button("🔄 Check Different Loan Type", key="reset_recommendations"):
                    st.session_state.show_bank_recommendations = False
                    st.rerun()

# ============================================================================
# TAB 2: MODEL ANALYTICS
# ============================================================================
with tab2:
    st.header("📊 Model Performance Analytics")
    st.subheader("🎯 Performance Metrics")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1: st.metric("Accuracy",  f"{metadata['test_accuracy']*100:.2f}%",  "High")
    with mc2: st.metric("Precision", f"{metadata['test_precision']*100:.2f}%", "High")
    with mc3: st.metric("Recall",    f"{metadata['test_recall']*100:.2f}%",    "High")
    with mc4: st.metric("F1-Score",  f"{metadata['test_f1']*100:.2f}%",        "High")

    st.markdown("---")
    st.subheader("🎯 Feature Importance Analysis")
    cc1, cc2 = st.columns([2, 1])
    with cc1:
        fig_bar = px.bar(feature_importance.head(10), x='importance', y='feature',
                         orientation='h', title='Top 10 Most Important Features',
                         labels={'importance': 'Importance Score', 'feature': 'Feature'},
                         color='importance', color_continuous_scale='Viridis')
        fig_bar.update_layout(height=500, showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    with cc2:
        fig_pie = px.pie(feature_importance.head(5), values='importance', names='feature',
                         title='Top 5 Features Distribution',
                         color_discrete_sequence=px.colors.sequential.Viridis)
        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Complete Feature Importance Table")
    sdf = feature_importance.copy()
    sdf['importance'] = sdf['importance'].apply(lambda x: f"{x:.4f}")
    sdf['rank'] = range(1, len(sdf) + 1)
    st.dataframe(sdf[['rank','feature','importance']], use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("⚙️ Model Hyperparameters")
    params_df = pd.DataFrame({'Parameter': list(metadata['best_params'].keys()),
                               'Value':     list(metadata['best_params'].values())})
    cp1, cp2 = st.columns(2)
    with cp1: st.dataframe(params_df, use_container_width=True, hide_index=True)
    with cp2:
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
This **AI-Powered Loan Eligibility Prediction System** uses advanced machine learning to predict loan approval with **95%+ accuracy**.

---
### 🧠 How It Works
1. **Data Collection** — Enter your personal, financial, and employment details
2. **Feature Engineering** — System calculates derived features like debt-to-income ratio
3. **AI Analysis** — XGBoost classifier analyses your profile using 18+ features
4. **Instant Decision** — Get results with confidence scores and recommendations

---
### 🔑 Key Factors for Loan Approval
1. **CIBIL Score** — Above 750: Excellent | 650–750: Good | Below 650: Difficult
2. **Debt-to-Income Ratio** — Below 30%: Excellent | 30–50%: Good | Above 50%: Risk
3. **Annual Income** — Higher income = higher eligibility
4. **Work Experience** — 5+ years preferred
5. **Existing Loans** — Fewer existing loans = better chances

---
### 🛠️ Technology Stack
- **ML**: XGBoost with Grid Search hyperparameter tuning
- **UI**: Streamlit with custom CSS
- **Visualisation**: Plotly
- **Data**: Pandas, NumPy, Scikit-learn

---
### 📧 Disclaimer
For **informational purposes only**. Actual loan approval depends on bank policies and documentation. Always consult financial institutions for official applications.
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p><strong>AI Loan Eligibility Predictor</strong> | Powered by XGBoost & Streamlit</p>
    <p>© 2025 | Built with ❤️ using Machine Learning</p>
</div>
""", unsafe_allow_html=True)
