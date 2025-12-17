# Tinder PCA: Women's Safety & Proactive Intervention Dashboard

A Streamlit-based dashboard designed to detect sexual abuse intent and Instagram/Off-platform grooming attempts on Tinder. This tool uses Policy-Constrained Analysis (PCA) to identify safety gaps that legacy models miss, specifically focusing on protecting women from predatory behavior.

## 🎯 Purpose

This dashboard transforms unstructured abuse signals into high-fidelity labels used to retrain legacy models, closing the safety gap for female users proactively. It identifies patterns that legacy models miss (such as coded platform references like '1G' for Instagram or 'Ghost App' for Snapchat), enabling proactive intervention before users are moved to unmonitored platforms.

## 🚀 Features

### Core Functionality
- **Policy-Constrained Analysis (PCA)**: Advanced detection system that identifies safety violations missed by legacy models
- **Safety Gap Detection**: Profiles with legacy confidence scores between 0.30-0.48 that require additional scrutiny
- **Risk Categorization**: Classifies threats into three categories:
  - **Sexualized Grooming**: Manipulative communication patterns establishing inappropriate sexual relationships
  - **Adversarial Off-Platform Pivot**: Attempts to move users to external platforms (Instagram, Snapchat, WhatsApp) to bypass safety tools
  - **Boundary Testing**: Systematic attempts to push against or violate user boundaries

### Dashboard Components
- **Strategic Safety Impact Metrics**: Real-time metrics showing safety gap coverage, feedback data generation, and high-risk violations
- **Top Evasion Tactics Visualization**: Interactive charts showing common evasion methods (Symbol Substitution, Coded Euphemisms, etc.)
- **Risk Category Distribution**: Visual breakdown of detected threat types
- **Confidence Comparison**: Side-by-side comparison of Legacy vs PCA model confidence scores
- **Detailed Profile Analysis**: In-depth examination of individual profiles with LLM reasoning

## 📋 Policy Framework

The dashboard enforces **Section 5.2: Protection Against Sexual Harassment & Off-Platform Grooming**, which explicitly prohibits:

1. **Sexualized Grooming**: Any attempt to establish inappropriate sexual relationships through manipulative communication
2. **Adversarial Off-Platform Pivot**: Attempting to move users to external platforms to bypass Tinder's safety tools
3. **Boundary Testing**: Systematic attempts to push against or violate user boundaries

**High-Risk Violation**: Attempting to move users to Instagram, Snapchat, WhatsApp, or other platforms to bypass Tinder's safety tools is considered a HIGH-RISK violation.

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd Tinder_womens_safety
   ```

2. **Install required dependencies**
   ```bash
   pip install streamlit pandas plotly
   ```

   Or install from a requirements file (if provided):
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Running the Dashboard

1. **Start the Streamlit application**
   ```bash
   streamlit run women_safety_dashboard.py
   ```

2. **Access the dashboard**
   - The dashboard will automatically open in your default web browser
   - If it doesn't, navigate to `http://localhost:8501`

### Using the Dashboard

1. **View Strategic Impact**: Check the top metrics to see safety gap coverage and feedback data generation
2. **Explore Evasion Tactics**: Review the "Top Evasion Tactics" chart to understand common bypass methods
3. **Analyze Risk Categories**: Examine the distribution of different threat types
4. **Review Individual Profiles**: Select a profile from the dropdown to see detailed analysis with LLM reasoning
5. **Export Data**: Use the "All Safety Gap Profiles" table to review all flagged profiles

## 📊 Key Metrics

- **Safety Gap Coverage**: +18.4% detection improvement over legacy models
- **Feedback Data Generated**: Number of high-confidence labels ready for model re-training
- **High-Risk Violations**: Count of off-platform pivot attempts detected
- **Average Confidence Boost**: Improvement in detection confidence vs legacy models

## 🎨 Design

The dashboard uses a **Trust & Safety color palette**:
- **Deep Purple** (#8B2E8B): Primary color for trust and safety
- **Tinder Red** (#FF4458): Secondary color for alerts and high-risk items
- **Pink Accent** (#FF6B9D): Supporting color for visualizations

## 📁 Project Structure

```
Tinder_womens_safety/
├── women_safety_dashboard.py  # Main Streamlit dashboard application
└── README.md                  # This file
```

## 🔍 How It Works

1. **Profile Ingestion**: The dashboard analyzes profiles with legacy confidence scores between 0.30-0.48 (the "safety gap")
2. **PCA Analysis**: Each profile is analyzed using Policy-Constrained Analysis to identify:
   - Coded platform references (e.g., "1G" for Instagram, "Ghost App" for Snapchat)
   - Sexualized grooming patterns
   - Boundary testing behavior
3. **LLM Reasoning**: Provides detailed explanations of why legacy models missed specific threats
4. **Label Generation**: High-confidence detections generate labeled training data for model improvement
5. **Continuous Improvement**: The flywheel effect - more data leads to better models, which detect more threats

## 🛡️ Safety Impact

This dashboard enables:
- **Proactive Intervention**: Detecting threats before users are moved to unmonitored platforms
- **Model Improvement**: Generating high-quality labeled data for retraining legacy models
- **Gap Closure**: Identifying and addressing blind spots in existing safety systems
- **Women's Protection**: Specifically focused on protecting female users from sexual harassment and grooming

## 📝 Example Detection Patterns

The dashboard identifies various evasion tactics:

- **Symbol Substitution**: "1G" instead of "Instagram"
- **Coded Euphemisms**: "Ghost App" instead of "Snapchat"
- **Direct Platform Mentions**: Explicit references to Instagram, Snapchat, WhatsApp
- **Contact Information Sharing**: Phone numbers, usernames for external platforms
- **Casual Boundary Testing**: Testing limits through increasingly inappropriate content

## 🔄 The Flywheel Effect

**Impact**: This dashboard transforms unstructured abuse signals into high-fidelity labels used to retrain legacy models, closing the safety gap for female users proactively. By identifying patterns that legacy models miss, PCA enables proactive intervention before users are moved to unmonitored platforms where safety protections are absent. Each flagged profile generates labeled training data that improves model accuracy, creating a continuous improvement cycle.

## 🤝 Contributing

This is a specialized tool for Tinder's Trust & Safety team. For questions or improvements, please contact the development team.

## 📄 License

Internal use only - Tinder Trust & Safety Team

## ⚠️ Disclaimer

This dashboard is designed for internal Trust & Safety operations. All profile data and analysis should be handled according to Tinder's privacy and data protection policies.

---

**Built with ❤️ for Women's Safety**

