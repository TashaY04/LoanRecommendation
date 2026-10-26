<p align="center">
<img width="2560" height="640" alt="banner" src="https://github.com/user-attachments/assets/99a26e81-03fe-4fa1-8bcf-a7b1b88a2557" />
</p>
<p align="center">
<img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white">
<img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-app-FF4B4B?style=flat-square&logo=streamlit&logoColor=white">
<img alt="XGBoost" src="https://img.shields.io/badge/XGBoost-model-006400?style=flat-square">
<img alt="Scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white">
<img alt="Docling" src="https://img.shields.io/badge/Docling-PDF parsing-1F7A6D?style=flat-square">
<img alt="Plotly" src="https://img.shields.io/badge/Plotly-charts-3F4F75?style=flat-square&logo=plotly&logoColor=white">
<img alt="Accuracy" src="https://img.shields.io/badge/accuracy-95%25+-brightgreen?style=flat-square">
<img alt="License" src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square">
</p>
<p align="center">
<a href="#overview">Overview</a> ·
<a href="#features">Features</a> ·
<a href="#document-parsing">Document parsing</a> ·
<a href="#model">Model</a> ·
<a href="#architecture">Architecture</a> ·
<a href="#screenshots">Screenshots</a> ·
<a href="#getting-started">Getting started</a> ·
<a href="#roadmap">Roadmap</a>
</p>

**Overview**
LoanEase helps an applicant find out whether they are likely to be approved for a loan, how confident the model is, and what they could change to improve their chances.
It is built around an XGBoost classifier trained on 8,000+ loan application records. Feature engineering (18+ financial features), Grid Search tuning and 5-fold cross-validation bring it to 95%+ accuracy. A Streamlit app wraps the model with interactive Plotly charts, EMI estimates and tailored suggestions.
The latest addition is document parsing. Instead of typing in every figure, you can upload a bank statement PDF and LoanEase reads it with Docling to pull out the information the assessment needs.
LoanEase is a decision-support project. Its output is a prediction, not a lending decision.

**Why I built it**
Loan decisions are usually slow and hard to read from the applicant's side. People get a yes or no without knowing why. LoanEase tries to fix that with:
an instant eligibility prediction
a confidence score next to every result
EMI estimates and a simple financial analysis
suggestions on what to improve
no manual data entry when a bank statement is available
local inference, so your data stays on your machine.

**Features**
<p align="center">
<img width="2400" height="1040" alt="features" src="https://github.com/user-attachments/assets/82a35c86-5c6f-4453-9530-14fdb4a69b3f" />

**Document parsing**
<p align="center">
<img width="2400" height="660" alt="document-pipeline" src="https://github.com/user-attachments/assets/b1ee5c47-399f-44d9-a912-a2c1c3100fe3" />
</p>

_Upload_: you provide a bank statement as a PDF.</p>
_Parse:_ Docling extracts the text, tables and document structure.</p>
_Structure:_ the extracted content is turned into the inputs the loan assessment uses.</p>
_Assess:_ those inputs go through the same XGBoost model and financial analysis as a manual entry.</p>
_Recommend_: you get the eligibility result, probability, EMI and suggestions.</p>

**Model**
<p align="center">
<img width="2400" height="860" alt="ml-highlights" src="https://github.com/user-attachments/assets/13a0e72a-7406-49a6-9910-600794912e3f" />
</p>

**Algorithm**
XGBoost classifier
Data
8,000+ loan applications
Features
18+ engineered financial features
Tuning
Grid Search CV
Validation
5-fold cross-validation
Metrics
Accuracy, Precision, Recall, F1, ROC-AUC

**Performance**
<p align="center">
<img width="787" alt="Model performance" src="https://github.com/user-attachments/assets/465de54d-a48e-4355-bc1e-fdcd142f866e" />
</p>

**Architecture**
<p align="center">
<img width="2000" height="1120" alt="architecture" src="https://github.com/user-attachments/assets/9e26a402-71c1-47d2-8dee-d925bd561ff5" />
</p>

**Workflow**
<p align="center">
<img width="648" alt="Project workflow" src="https://github.com/user-attachments/assets/21c2491e-2f98-41f0-a00b-c125d4b1e9d4" />
</p>

**Tech stack**
Area
Tools
Language
Python
App
Streamlit
Machine learning
XGBoost, scikit-learn
Document parsing
Docling
Data
pandas, NumPy
Charts
Plotly, Matplotlib
Tuning and validation
Grid Search CV, 5-fold cross-validation

**Screenshots**
<p align="center">
<img width="49%" alt="LoanEase screenshot 1" src="https://github.com/user-attachments/assets/d67a5a60-448b-4cb8-937a-aa0fe553c2e1" />
<img width="49%" alt="LoanEase screenshot 2" src="https://github.com/user-attachments/assets/e69c2530-7f13-4ceb-a125-c8de2a0216c4" />
</p>
<p align="center">
<img width="49%" alt="LoanEase screenshot 3" src="https://github.com/user-attachments/assets/8c23d1bb-5290-4af9-a08c-7aad076013ff" />
<img width="49%" alt="LoanEase screenshot 4" src="https://github.com/user-attachments/assets/b49a6c69-9a08-4867-9132-a3754af719e1" />
</p>
<p align="center">
<img width="49%" alt="LoanEase screenshot 5" src="https://github.com/user-attachments/assets/938d8a30-2994-4cc5-872b-9dfea38f4c14" />
<img width="49%" alt="LoanEase screenshot 6" src="https://github.com/user-attachments/assets/d7a96125-3f8b-4fd1-b6eb-81595a7f6f97" />
</p>
<p align="center">
<img width="49%" alt="LoanEase screenshot 7" src="https://github.com/user-attachments/assets/d38ab8d4-dd79-47bc-8896-b02c2da9ece0" />
<img width="49%" alt="LoanEase screenshot 8" src="https://github.com/user-attachments/assets/6df3de78-d952-44a9-9670-ddcf5aa43002" />
</p>

**Getting started**
1. git clone <https://github.com/TashaY04/LoanRecommendation.git>
2. cd LoanRecommendation
3. pip install -r requirements_streamlit.txt
4. python train_model.py      # trains and saves the model
5. streamlit run app.py       # starts the app
​
Full technical notes (project structure, feature engineering, hyperparameters, customization, troubleshooting) are in DEVELOPER_GUIDE.md.
Roadmap

Bank API integration

Explainable AI with SHAP

PDF loan reports

AI financial assistant

Multi-bank loan comparison

Cloud deployment

User authentication

Mobile app
Author
Tanisha Yadav (@TashaY04)
Computer Science Engineer · AI and full-stack developer
If the project helped you, a star on the repo is always appreciated.
