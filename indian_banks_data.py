"""
Indian Banks Loan Recommendation Database
Contains comprehensive data for major Indian banks across different loan types
Updated: 2025
"""

# ============================================================================
# HOME LOANS DATA
# ============================================================================
HOME_LOANS = {
    'SBI': {
        'bank_name': 'State Bank of India',
        'interest_rate_min': 7.50,
        'interest_rate_max': 8.95,
        'processing_fee': '0.35% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 18,
        'max_age': 70,
        'max_tenure': 30,
        'prepayment_charges': 'None',
        'special_features': ['Max Gain Scheme', 'Realty Scheme', '0.05% concession for women borrowers', 'Lowest rates for CIBIL ≥825'],
        'loan_amount_max': 100000000,
        'score': 95,
        'pros': ['Lowest interest rates in market', 'Largest network', 'Special schemes for women', 'No prepayment charges', 'Flexible tenure up to 30 years'],
        'cons': ['Documentation process can be lengthy', 'Processing time slightly longer than private banks'],
        'best_for': ['First-time home buyers', 'Women borrowers', 'High CIBIL score applicants', 'Long-term loans']
    },
    'HDFC': {
        'bank_name': 'HDFC Bank',
        'interest_rate_min': 8.15,
        'interest_rate_max': 8.75,
        'processing_fee': 'Up to 0.50% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 30,
        'prepayment_charges': 'None',
        'special_features': ['Instant Home Loan approval', 'Women borrower concession', 'Digital processing', 'Quick disbursement'],
        'loan_amount_max': 100000000,
        'score': 92,
        'pros': ['Instant approval facility', 'Quick disbursement', 'Excellent digital experience', 'Wide branch network', 'Premium customer service'],
        'cons': ['Slightly higher rates than SBI', 'Higher processing fee'],
        'best_for': ['Quick loan requirements', 'Tech-savvy borrowers', 'Existing HDFC customers', 'Premium banking experience']
    },
    'ICICI': {
        'bank_name': 'ICICI Bank',
        'interest_rate_min': 7.65,
        'interest_rate_max': 9.00,
        'processing_fee': 'Up to 0.50% of loan amount',
        'min_cibil': 750,
        'preferred_cibil': 800,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 30,
        'prepayment_charges': 'None',
        'special_features': ['Credit score-based rates', 'Instant Home Loan', 'Digital doorstep service', 'NRI home loans'],
        'loan_amount_max': 100000000,
        'score': 90,
        'pros': ['Competitive rates for high CIBIL scores', 'Fast processing', 'Doorstep service available', 'Strong digital platform'],
        'cons': ['Higher minimum CIBIL requirement', 'Stringent eligibility criteria'],
        'best_for': ['High credit score borrowers', 'NRI borrowers', 'Quick processing needs', 'Digital-first customers']
    },
    'Axis Bank': {
        'bank_name': 'Axis Bank',
        'interest_rate_min': 7.90,
        'interest_rate_max': 9.65,
        'processing_fee': '1% + GST (minimum ₹10,000)',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 30,
        'prepayment_charges': 'Applicable',
        'special_features': ['Asha Home Loan', 'Super Saver Home Loan', 'Special rates for women', 'Flexible repayment options'],
        'loan_amount_max': 100000000,
        'score': 85,
        'pros': ['Multiple loan variants', 'Good customer service', 'Flexible schemes', 'Balance transfer options'],
        'cons': ['Higher processing fee', 'Prepayment charges applicable', 'Higher maximum interest rates'],
        'best_for': ['Mid-income borrowers', 'Existing Axis Bank customers', 'Balance transfer seekers']
    },
    'Kotak Mahindra': {
        'bank_name': 'Kotak Mahindra Bank',
        'interest_rate_min': 8.70,
        'interest_rate_max': 9.50,
        'processing_fee': 'Up to 0.50% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 30,
        'prepayment_charges': 'None for floating rates',
        'special_features': ['No prepayment charges', 'NRI home loan options', 'Premium banking service', 'Personalized assistance'],
        'loan_amount_max': 100000000,
        'score': 83,
        'pros': ['No prepayment charges on floating', 'Good NRI services', 'Personalized service', 'Premium experience'],
        'cons': ['Higher interest rates', 'Limited branch network', 'Premium segment focus'],
        'best_for': ['NRI borrowers', 'Premium banking customers', 'Borrowers planning early closure']
    }
}

# ============================================================================
# PERSONAL LOANS DATA
# ============================================================================
PERSONAL_LOANS = {
    'SBI': {
        'bank_name': 'State Bank of India',
        'interest_rate_min': 10.05,
        'interest_rate_max': 15.05,
        'processing_fee': 'Up to 1.50% (Min. ₹1,000; Max. ₹15,000)',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 6,
        'loan_amount_min': 25000,
        'loan_amount_max': 2000000,
        'score': 93,
        'pros': ['Competitive interest rates', 'Flexible processing fee', 'Trusted public sector bank', 'Wide branch network', 'Lower rates compared to private banks'],
        'cons': ['Longer processing time', 'More documentation required', 'Stricter verification'],
        'best_for': ['Salaried employees', 'Government employees', 'Cost-conscious borrowers', 'First-time loan takers']
    },
    'HDFC': {
        'bank_name': 'HDFC Bank',
        'interest_rate_min': 9.99,
        'interest_rate_max': 24.00,
        'processing_fee': '₹3,499 - ₹6,500 + GST',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 20000,
        'min_age': 21,
        'max_age': 60,
        'max_tenure': 7,
        'loan_amount_min': 50000,
        'loan_amount_max': 4000000,
        'score': 90,
        'pros': ['Instant approval available', 'Quick disbursement', 'Minimal documentation', 'Excellent digital platform', 'Pre-approved offers for existing customers'],
        'cons': ['Higher maximum rates', 'Fixed processing fee', 'Higher income requirement'],
        'best_for': ['Urgent fund requirements', 'Existing HDFC customers', 'High income borrowers', 'Medical emergencies']
    },
    'ICICI': {
        'bank_name': 'ICICI Bank',
        'interest_rate_min': 10.45,
        'interest_rate_max': 16.50,
        'processing_fee': 'Up to 2% + GST',
        'min_cibil': 750,
        'preferred_cibil': 800,
        'min_income': 18000,
        'min_age': 23,
        'max_age': 58,
        'max_tenure': 5,
        'loan_amount_min': 50000,
        'loan_amount_max': 2500000,
        'score': 88,
        'pros': ['Fast approval process', 'Doorstep service', 'Flexible repayment', 'Pre-approved offers', 'Digital-first approach'],
        'cons': ['Higher CIBIL requirement', 'Higher processing fee', 'Shorter maximum tenure'],
        'best_for': ['High credit score borrowers', 'Existing ICICI customers', 'Working professionals', 'Short-term needs']
    },
    'Axis Bank': {
        'bank_name': 'Axis Bank',
        'interest_rate_min': 9.99,
        'interest_rate_max': 17.15,
        'processing_fee': '1% - 1.5%',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 60,
        'max_tenure': 5,
        'loan_amount_min': 50000,
        'loan_amount_max': 4000000,
        'score': 87,
        'pros': ['Competitive starting rates', 'High loan amounts available', 'Good customer service', 'Special offers for salary accounts'],
        'cons': ['Variable rate range', 'Moderate processing fee'],
        'best_for': ['Salary account holders', 'Debt consolidation', 'Wedding expenses', 'Home renovation']
    },
    'Kotak Mahindra': {
        'bank_name': 'Kotak Mahindra Bank',
        'interest_rate_min': 9.98,
        'interest_rate_max': 17.20,
        'processing_fee': '1.1% - 1.5% + Taxes',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 18000,
        'min_age': 21,
        'max_age': 60,
        'max_tenure': 5,
        'loan_amount_min': 50000,
        'loan_amount_max': 2500000,
        'score': 85,
        'pros': ['Very competitive starting rate', 'Minimal documentation', 'Quick processing', 'Premium service'],
        'cons': ['Higher maximum rates', 'Limited branch network'],
        'best_for': ['Premium customers', 'Quick approvals', 'Urban borrowers']
    }
}

# ============================================================================
# BUSINESS LOANS DATA
# ============================================================================
BUSINESS_LOANS = {
    'SBI': {
        'bank_name': 'State Bank of India',
        'interest_rate_min': 8.00,
        'interest_rate_max': 11.50,
        'processing_fee': '0.50% - 1.50% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 200000,
        'business_vintage': 3,
        'max_tenure': 10,
        'loan_amount_max': 50000000,
        'score': 96,
        'pros': ['Lowest interest rates for MSMEs', 'Government scheme benefits', 'Mudra loan facility', 'Largest MSME lender', 'Flexible tenure', 'Special schemes for women entrepreneurs'],
        'cons': ['More documentation required', 'Longer processing time', 'Collateral requirements for larger loans'],
        'best_for': ['MSMEs', 'Manufacturing businesses', 'Government scheme beneficiaries', 'Startups', 'Women entrepreneurs']
    },
    'HDFC': {
        'bank_name': 'HDFC Bank',
        'interest_rate_min': 10.75,
        'interest_rate_max': 22.50,
        'processing_fee': '2% - 3% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 300000,
        'business_vintage': 2,
        'max_tenure': 7,
        'loan_amount_max': 5000000,
        'score': 88,
        'pros': ['Quick approval', 'Minimal documentation', 'Up to ₹50 lakh unsecured', 'Digital process', 'Fast disbursement'],
        'cons': ['Higher interest rates', 'Higher processing fee', 'Lower maximum loan amount'],
        'best_for': ['Small businesses', 'Working capital needs', 'Trade finance', 'Urgent business requirements', 'Service businesses']
    },
    'ICICI': {
        'bank_name': 'ICICI Bank',
        'interest_rate_min': 10.50,
        'interest_rate_max': 22.00,
        'processing_fee': '1.5% - 2.5% + GST',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 300000,
        'business_vintage': 3,
        'max_tenure': 7,
        'loan_amount_max': 20000000,
        'score': 87,
        'pros': ['CGTMSE scheme benefits', 'Secured and unsecured options', 'Good for established businesses', 'Branch network support'],
        'cons': ['Higher rates compared to SBI', 'Stricter eligibility', 'Business vintage requirement'],
        'best_for': ['Established businesses', 'Expansion projects', 'Equipment purchase', 'Retail businesses']
    },
    'Axis Bank': {
        'bank_name': 'Axis Bank',
        'interest_rate_min': 11.50,
        'interest_rate_max': 20.00,
        'processing_fee': '1% - 2% + GST',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 250000,
        'business_vintage': 2,
        'max_tenure': 5,
        'loan_amount_max': 5000000,
        'score': 84,
        'pros': ['Flexible loan amounts', 'Good for SMEs', 'Balance transfer facility', 'Overdraft facility'],
        'cons': ['Moderate interest rates', 'Shorter tenure', 'Higher rates for new businesses'],
        'best_for': ['Small and medium enterprises', 'Trading businesses', 'Balance transfer', 'Working capital']
    },
    'Kotak Mahindra': {
        'bank_name': 'Kotak Mahindra Bank',
        'interest_rate_min': 12.99,
        'interest_rate_max': 14.50,
        'processing_fee': '1.5% - 3% of loan amount',
        'min_cibil': 750,
        'preferred_cibil': 800,
        'min_income': 300000,
        'business_vintage': 3,
        'max_tenure': 5,
        'loan_amount_max': 5000000,
        'score': 80,
        'pros': ['Premium service', 'Relationship-based pricing', 'Personalized solutions', 'Quick processing for existing customers'],
        'cons': ['Higher CIBIL requirement', 'Higher rates', 'Limited to established businesses', 'Premium segment focus'],
        'best_for': ['Premium business customers', 'Existing Kotak relationship', 'Service industry', 'Professional services']
    }
}

# ============================================================================
# EDUCATION LOANS DATA
# ============================================================================
EDUCATION_LOANS = {
    'SBI': {
        'bank_name': 'State Bank of India',
        'interest_rate_min': 8.30,
        'interest_rate_max': 10.90,
        'processing_fee': 'Nil',
        'min_cibil': 650,
        'preferred_cibil': 700,
        'min_income': 0,  # Parents/guarantors income
        'min_age': 18,
        'max_age': 35,
        'max_tenure': 15,
        'loan_amount_max': 30000000,
        'score': 98,
        'pros': ['Lowest rates for premier institutions (IIT/IIM/NIT)', 'Scholar Loan Scheme at 8.30%', 'No processing fee', 'Up to ₹3 crore for international studies', 'Flexible repayment', 'Moratorium period available'],
        'cons': ['Longer processing for international education', 'Collateral required for loans above ₹7.5 lakh'],
        'best_for': ['IIT/IIM/NIT students', 'International education', 'Medical/Engineering courses', 'Students from lower income families']
    },
    'HDFC': {
        'bank_name': 'HDFC Bank',
        'interest_rate_min': 10.50,
        'interest_rate_max': 13.50,
        'processing_fee': '1% of loan amount',
        'min_cibil': 650,
        'preferred_cibil': 700,
        'min_income': 300000,
        'min_age': 18,
        'max_age': 35,
        'max_tenure': 15,
        'loan_amount_max': 15000000,
        'score': 90,
        'pros': ['Preferential rates for top colleges', 'Up to ₹150 lakh loan', 'Quick approval', 'Simple documentation', 'Covers tuition, living, and travel costs'],
        'cons': ['Processing fee applicable', 'Higher rates than SBI', 'Co-applicant mandatory'],
        'best_for': ['Top tier colleges', 'MBA aspirants', 'Study abroad programs', 'Professional courses']
    },
    'ICICI': {
        'bank_name': 'ICICI Bank',
        'interest_rate_min': 10.25,
        'interest_rate_max': 14.00,
        'processing_fee': '0.50% - 1% of loan amount',
        'min_cibil': 650,
        'preferred_cibil': 700,
        'min_income': 250000,
        'min_age': 18,
        'max_age': 35,
        'max_tenure': 15,
        'loan_amount_max': 20000000,
        'score': 88,
        'pros': ['iSMART education loan scheme', 'Vidyalakshmi scheme at 9.70%', 'CGFSEL scheme available', 'Flexible repayment options', 'Digital application process'],
        'cons': ['Variable rates based on course', 'Collateral for higher amounts', 'Guarantor required'],
        'best_for': ['Government scheme beneficiaries', 'Engineering/Medical students', 'Domestic and international education']
    },
    'Bank of Baroda': {
        'bank_name': 'Bank of Baroda',
        'interest_rate_min': 9.15,
        'interest_rate_max': 11.15,
        'processing_fee': 'Nil',
        'min_cibil': 650,
        'preferred_cibil': 700,
        'min_income': 0,
        'min_age': 18,
        'max_age': 35,
        'max_tenure': 15,
        'loan_amount_max': 30000000,
        'score': 92,
        'pros': ['Competitive rates for premier institutions', 'No processing fee', 'Wide network', 'Good for international studies', 'Special rates for women students'],
        'cons': ['Processing time longer', 'Branch dependent service'],
        'best_for': ['Premier institutions', 'International students', 'Rural students', 'Women students']
    },
    'Indian Overseas Bank': {
        'bank_name': 'Indian Overseas Bank',
        'interest_rate_min': 8.75,
        'interest_rate_max': 10.50,
        'processing_fee': 'Nil',
        'min_cibil': 650,
        'preferred_cibil': 700,
        'min_income': 0,
        'min_age': 18,
        'max_age': 35,
        'max_tenure': 15,
        'loan_amount_max': 20000000,
        'score': 85,
        'pros': ['Very low interest rates', 'No processing fee', 'Good for domestic education', 'Simple application'],
        'cons': ['Limited loan amount', 'Smaller branch network', 'Slower processing'],
        'best_for': ['Domestic education', 'Budget-conscious students', 'Regional colleges']
    }
}

# ============================================================================
# VEHICLE/AUTO LOANS DATA
# ============================================================================
VEHICLE_LOANS = {
    'SBI': {
        'bank_name': 'State Bank of India',
        'interest_rate_min': 7.20,
        'interest_rate_max': 9.45,
        'processing_fee': '₹5,000 or 0.40% (whichever is higher)',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 7,
        'loan_amount_max': 10000000,
        'score': 95,
        'pros': ['Lowest interest rates', 'Up to 90% financing', 'Flexible tenure', 'Low processing fee', 'Fast approval', 'Special rates for electric vehicles'],
        'cons': ['Slightly longer documentation', 'Branch visit may be required'],
        'best_for': ['New car buyers', 'Low cost financing', 'Electric vehicle buyers', 'First-time car buyers']
    },
    'HDFC': {
        'bank_name': 'HDFC Bank',
        'interest_rate_min': 8.80,
        'interest_rate_max': 10.25,
        'processing_fee': '₹3,500 - ₹5,000',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 20000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 7,
        'loan_amount_max': 10000000,
        'score': 92,
        'pros': ['Quick approval', 'Minimal documentation', 'Digital process', 'Up to 100% on-road price financing', 'Doorstep service', 'Pre-approved offers'],
        'cons': ['Higher rates than SBI', 'Higher income requirement'],
        'best_for': ['Quick financing needs', 'Existing HDFC customers', 'Premium car buyers', 'Urgent requirements']
    },
    'ICICI': {
        'bank_name': 'ICICI Bank',
        'interest_rate_min': 8.50,
        'interest_rate_max': 11.25,
        'processing_fee': '₹3,499 - ₹5,000',
        'min_cibil': 750,
        'preferred_cibil': 800,
        'min_income': 18000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 7,
        'loan_amount_max': 10000000,
        'score': 90,
        'pros': ['100% on-road funding available', 'Fast processing', 'Flexible EMI options', 'Used car loans available', 'Digital doorstep service'],
        'cons': ['Higher CIBIL requirement', 'Higher rates for used cars', 'Processing fee on higher side'],
        'best_for': ['High credit score borrowers', 'New and used car buyers', '100% financing seekers', 'Quick approval needs']
    },
    'Canara Bank': {
        'bank_name': 'Canara Bank',
        'interest_rate_min': 8.45,
        'interest_rate_max': 9.80,
        'processing_fee': '0.50% of loan amount',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 7,
        'loan_amount_max': 5000000,
        'score': 87,
        'pros': ['Competitive rates', 'Public sector trust', 'Good for salaried employees', 'Flexible repayment'],
        'cons': ['Longer processing time', 'More documentation', 'Limited digital services'],
        'best_for': ['Government employees', 'PSU employees', 'Cost-conscious buyers']
    },
    'Union Bank': {
        'bank_name': 'Union Bank of India',
        'interest_rate_min': 8.45,
        'interest_rate_max': 9.70,
        'processing_fee': '0.50% of loan amount (Max ₹5,000)',
        'min_cibil': 700,
        'preferred_cibil': 750,
        'min_income': 15000,
        'min_age': 21,
        'max_age': 65,
        'max_tenure': 7,
        'loan_amount_max': 5000000,
        'score': 85,
        'pros': ['Low interest rates', 'Capped processing fee', 'Good for two-wheelers', 'Special schemes for women'],
        'cons': ['Limited digital presence', 'Slower processing'],
        'best_for': ['Two-wheeler loans', 'Budget car buyers', 'Women borrowers', 'Public sector preference']
    }
}


def get_loan_recommendations(loan_type, user_profile):
    """
    Get top 3 bank recommendations based on loan type and user profile
    
    Parameters:
    - loan_type: str (Home, Personal, Business, Education, Vehicle)
    - user_profile: dict with keys: cibil_score, annual_income, loan_amount, age
    
    Returns:
    - List of top 3 recommended banks with scores and detailed reasoning
    """
    
    # Select appropriate loan database
    loan_db = {
        'Home': HOME_LOANS,
        'Personal': PERSONAL_LOANS,
        'Business': BUSINESS_LOANS,
        'Education': EDUCATION_LOANS,
        'Vehicle': VEHICLE_LOANS
    }.get(loan_type, HOME_LOANS)
    
    recommendations = []
    
    for bank_code, bank_data in loan_db.items():
        # Calculate dynamic score based on user profile
        score = bank_data['score']
        reasons = []
        
        # CIBIL Score matching
        if user_profile['cibil_score'] >= bank_data['preferred_cibil']:
            score += 10
            reasons.append(f"Your CIBIL score ({user_profile['cibil_score']}) exceeds their preferred threshold ({bank_data['preferred_cibil']})")
        elif user_profile['cibil_score'] >= bank_data['min_cibil']:
            score += 5
            reasons.append(f"Your CIBIL score ({user_profile['cibil_score']}) meets their minimum requirement")
        else:
            score -= 20
            reasons.append(f"Your CIBIL score is below their minimum requirement ({bank_data['min_cibil']})")
        
        # Income matching
        if user_profile['annual_income'] >= bank_data['min_income'] * 24:  # 2x income requirement
            score += 8
            reasons.append(f"Your income substantially exceeds their requirement")
        elif user_profile['annual_income'] >= bank_data['min_income'] * 12:
            score += 4
            reasons.append(f"Your income meets their requirement comfortably")
        
        # Interest rate benefit
        avg_rate = (bank_data['interest_rate_min'] + bank_data['interest_rate_max']) / 2
        if avg_rate <= 10:
            score += 5
            reasons.append(f"Offers competitive interest rates (avg {avg_rate:.2f}%)")
        
        # Loan amount compatibility
        if 'loan_amount_max' in bank_data:
            if user_profile['loan_amount'] <= bank_data['loan_amount_max']:
                score += 3
                reasons.append(f"Can accommodate your loan amount requirement")
        
        # Age compatibility
        if 'min_age' in bank_data and 'max_age' in bank_data:
            if bank_data['min_age'] <= user_profile['age'] <= bank_data['max_age']:
                score += 2
        
        recommendations.append({
            'bank_code': bank_code,
            'bank_name': bank_data['bank_name'],
            'score': score,
            'data': bank_data,
            'match_reasons': reasons
        })
    
    # Sort by score and return top 3
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:3]
