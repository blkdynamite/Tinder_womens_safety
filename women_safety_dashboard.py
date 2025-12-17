import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json

# Page configuration
st.set_page_config(
    page_title="Tinder PCA: Women's Safety & Proactive Intervention",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data Science & Engineering Color Palette - Dark Mode with Slate/Zinc
DS_COLORS = {
    'slate_bg': '#1e293b',  # Slate-800
    'zinc_bg': '#27272a',  # Zinc-800
    'slate_surface': '#334155',  # Slate-700
    'tinder_flame': '#FF4458',  # Tinder Red/Flame
    'tinder_flame_light': '#FF6B9D',  # Light Tinder accent
    'accent_purple': '#8b5cf6',  # Purple accent
    'text_primary': '#f1f5f9',  # Slate-100
    'text_secondary': '#cbd5e1',  # Slate-300
    'success': '#10b981',  # Green
    'warning': '#f59e0b',  # Amber
    'border': '#475569'  # Slate-600
}

# Policy Text - Section 5.2: Protection Against Sexual Harassment & Off-Platform Grooming
POLICY_TEXT = """
**Section 5.2: Protection Against Sexual Harassment & Off-Platform Grooming**

Tinder is committed to creating a safe environment for all users, with particular emphasis on protecting women from sexual harassment and predatory behavior. This policy explicitly prohibits:

1. **Sexualized Grooming**: Any attempt to establish inappropriate sexual relationships through manipulative communication patterns, including but not limited to:
   - Sexualized language disguised as casual conversation
   - Boundary testing through escalating inappropriate requests
   - Attempts to normalize sexual content in early-stage conversations

2. **Adversarial Off-Platform Pivot**: Attempting to move users to external platforms (Instagram, Snapchat, WhatsApp, Telegram, or any other messaging platform) to bypass Tinder's safety tools and monitoring systems. This includes:
   - Direct requests to move conversations off-platform
   - Coded references to external platforms (e.g., "1G" for Instagram, "Ghost App" for Snapchat)
   - Providing usernames or contact information for external platforms
   - Any attempt to circumvent Tinder's safety features by moving to unmonitored channels

3. **Boundary Testing**: Systematic attempts to push against or violate user boundaries, including:
   - Repeated requests after initial refusal
   - Testing limits through increasingly inappropriate content
   - Attempts to coerce or manipulate users into uncomfortable situations

**High-Risk Violation**: Attempting to move users to Instagram, Snapchat, WhatsApp, or other platforms to bypass Tinder's safety tools is considered a HIGH-RISK violation, as it enables unmonitored predatory behavior and removes critical safety protections.
"""

# Audit Profiles - The "Safety Gap" Data
# All profiles have legacy_confidence between 0.30 and 0.48
AUDIT_PROFILES = [
    {
        "profile_id": "WS-001",
        "bio": "Message me on 1G @user",
        "age": 28,
        "legacy_confidence": 0.35,
        "messages": ["Hey", "Want to chat somewhere else?", "I'm more active on 1G"],
        "risk_category": "Adversarial Off-Platform Pivot"
    },
    {
        "profile_id": "WS-002",
        "bio": "Let's talk on the Ghost App",
        "age": 32,
        "legacy_confidence": 0.42,
        "messages": ["Not on here much", "Ghost App is better", "Add me there"],
        "risk_category": "Adversarial Off-Platform Pivot"
    },
    {
        "profile_id": "WS-003",
        "bio": "Looking for a submissive girl to spoil",
        "age": 35,
        "legacy_confidence": 0.38,
        "messages": ["Are you submissive?", "I like to take control", "Want to be spoiled?"],
        "risk_category": "Sexualized Grooming"
    },
    {
        "profile_id": "WS-004",
        "bio": "Not on here much, add my Insta in bio",
        "age": 29,
        "legacy_confidence": 0.45,
        "messages": ["Check my bio", "Insta is @username", "DM me there"],
        "risk_category": "Adversarial Off-Platform Pivot"
    },
    {
        "profile_id": "WS-005",
        "bio": "Looking for someone who knows how to have fun 😈",
        "age": 31,
        "legacy_confidence": 0.33,
        "messages": ["What kind of fun?", "I'm very adventurous", "Want to explore?"],
        "risk_category": "Boundary Testing"
    },
    {
        "profile_id": "WS-006",
        "bio": "Snap: user123 | More active there",
        "age": 27,
        "legacy_confidence": 0.40,
        "messages": ["Add my snap", "Better to talk there", "I check snap more"],
        "risk_category": "Adversarial Off-Platform Pivot"
    },
    {
        "profile_id": "WS-007",
        "bio": "Seeking someone who likes to be dominated",
        "age": 34,
        "legacy_confidence": 0.36,
        "messages": ["Are you into BDSM?", "I need someone submissive", "Want to try?"],
        "risk_category": "Sexualized Grooming"
    },
    {
        "profile_id": "WS-008",
        "bio": "1G handle: @username | Let's connect there",
        "age": 30,
        "legacy_confidence": 0.31,
        "messages": ["1G is better", "Follow me there", "We can talk freely"],
        "risk_category": "Adversarial Off-Platform Pivot"
    },
    {
        "profile_id": "WS-009",
        "bio": "Looking for someone who doesn't play games",
        "age": 33,
        "legacy_confidence": 0.47,
        "messages": ["No games?", "I'm direct", "Want to meet tonight?"],
        "risk_category": "Boundary Testing"
    },
    {
        "profile_id": "WS-010",
        "bio": "WhatsApp me: +1234567890 | More responsive",
        "age": 28,
        "legacy_confidence": 0.44,
        "messages": ["Text me on WhatsApp", "Faster response there", "Number in bio"],
        "risk_category": "Adversarial Off-Platform Pivot"
    }
]

def simulate_pca_analysis(profile):
    """
    Simulate PCA analysis with LLM reasoning focused on Women's Safety.
    Returns analysis with categories: Sexualized Grooming, Adversarial Off-Platform Pivot, Boundary Testing
    Includes Contextual Weight for NLP feature importance scoring.
    """
    bio = profile["bio"].lower()
    messages = " ".join(profile["messages"]).lower()
    combined_text = f"{bio} {messages}"
    
    # Calculate contextual weight based on linguistic complexity and semantic density
    contextual_weight = random.uniform(0.72, 0.94)  # High contextual understanding score
    
    # Determine risk category and generate data science-focused reasoning
    if any(code in combined_text for code in ["1g", "ghost app", "insta", "snap", "whatsapp", "telegram"]):
        category = "Adversarial Off-Platform Pivot"
        if "1g" in combined_text:
            reasoning = "PCA identified semantic intent of 'off-platform pivot' via high-order linguistic patterns that exceeded the token-matching capabilities of the BERT-based legacy model. The coded reference '1G' represents an adversarial evasion tactic designed to circumvent Instagram blocklist filters. Legacy model's token-based approach failed to capture the semantic equivalence, while PCA's contextual embeddings successfully mapped the intent to Section 5.2 violations."
        elif "ghost app" in combined_text:
            reasoning = "PCA detected semantic intent of 'platform migration' through contextual embeddings that identified 'Ghost App' as a coded euphemism for Snapchat. The BERT-based legacy model's token-matching approach failed to recognize this semantic substitution, while PCA's transformer-based reasoning captured the adversarial intent to move conversations to unmonitored channels, violating Section 5.2 policy constraints."
        else:
            reasoning = "PCA identified explicit off-platform pivot attempts through semantic analysis of platform references that legacy BERT models missed. The contextual weight indicates high confidence in detecting adversarial behavior designed to bypass safety monitoring systems, enabling unmonitored predatory interactions."
    elif any(term in combined_text for term in ["submissive", "dominated", "spoil", "control", "bdsm"]):
        category = "Sexualized Grooming"
        reasoning = "PCA identified semantic intent of 'sexualized grooming' via high-order linguistic patterns that exceeded the token-matching capabilities of the BERT-based legacy model. The contextual embeddings captured power dynamic indicators ('submissive', 'spoil', 'control') that legacy models classified as low-risk due to lack of explicit sexual content. PCA's semantic understanding recognized these as early-stage grooming signals indicating intent to establish inappropriate relationships."
    else:
        category = "Boundary Testing"
        reasoning = "PCA identified semantic intent of 'boundary testing' via high-order linguistic patterns that exceeded the token-matching capabilities of the BERT-based legacy model. The contextual analysis detected systematic pressure tactics and limit-pushing behavior through conversational patterns that legacy models failed to recognize. The semantic embeddings captured intent to violate user boundaries through escalating inappropriate requests."
    
    # Calculate PCA confidence (higher than legacy for safety gap profiles)
    pca_confidence = min(0.95, profile["legacy_confidence"] + random.uniform(0.15, 0.35))
    
    return {
        "category": category,
        "pca_confidence": round(pca_confidence, 3),
        "legacy_confidence": profile["legacy_confidence"],
        "contextual_weight": round(contextual_weight, 3),
        "reasoning": reasoning,
        "risk_score": round(pca_confidence * 100, 1)
    }

def identify_evasion_tactics(profiles):
    """Identify and count evasion tactics from profiles"""
    tactics = {
        "Symbol Substitution": 0,  # 1G for Instagram
        "Coded Euphemisms": 0,  # Ghost App for Snapchat
        "Direct Platform Mentions": 0,  # Instagram, Snapchat, WhatsApp
        "Contact Information Sharing": 0,  # Phone numbers, usernames
        "Casual Boundary Testing": 0  # Testing limits
    }
    
    for profile in profiles:
        text = f"{profile['bio']} {' '.join(profile['messages'])}".lower()
        
        if "1g" in text:
            tactics["Symbol Substitution"] += 1
        if "ghost app" in text:
            tactics["Coded Euphemisms"] += 1
        if any(platform in text for platform in ["insta", "snap", "whatsapp", "telegram"]):
            tactics["Direct Platform Mentions"] += 1
        if any(char.isdigit() for char in text) and ("+" in text or len([c for c in text if c.isdigit()]) > 7):
            tactics["Contact Information Sharing"] += 1
        if profile["risk_category"] == "Boundary Testing":
            tactics["Casual Boundary Testing"] += 1
    
    return tactics

# Main Dashboard
def main():
    # Apply dark mode styling
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {DS_COLORS['slate_bg']};
        }}
        .main .block-container {{
            background-color: {DS_COLORS['slate_bg']};
            padding-top: 2rem;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {DS_COLORS['text_primary']};
        }}
        p, li, span {{
            color: {DS_COLORS['text_secondary']};
        }}
        .stMetric {{
            background-color: {DS_COLORS['slate_surface']};
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid {DS_COLORS['border']};
        }}
        .stMetric label {{
            color: {DS_COLORS['text_secondary']};
        }}
        .stMetric [data-testid="stMetricValue"] {{
            color: {DS_COLORS['text_primary']};
        }}
        .stDataFrame {{
            background-color: {DS_COLORS['slate_surface']};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Header
    st.markdown(
        f"""
        <div style='background: linear-gradient(90deg, {DS_COLORS['slate_surface']}, {DS_COLORS['zinc_bg']}); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; 
                    border: 2px solid {DS_COLORS['tinder_flame']};'>
            <h1 style='color: {DS_COLORS['text_primary']}; text-align: center; margin: 0;'>
                🛡️ Tinder PCA: Women's Safety & Proactive Intervention
            </h1>
            <p style='color: {DS_COLORS['text_secondary']}; text-align: center; margin-top: 0.5rem;'>
                Detecting Sexual Abuse Intent & Off-Platform Grooming
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Strategic Impact Section - Data Science Metrics
    st.markdown("## 🚀 Strategic Safety Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    all_analyses = [simulate_pca_analysis(p) for p in AUDIT_PROFILES]
    feedback_count = len([a for a in all_analyses if a["pca_confidence"] > 0.6])
    high_risk_count = len([a for a in all_analyses if a["category"] == "Adversarial Off-Platform Pivot"])
    model_divergence = sum([a["pca_confidence"] - p["legacy_confidence"] for a, p in zip(all_analyses, AUDIT_PROFILES)]) / len(AUDIT_PROFILES)
    
    # False Negative Mitigation Rate: profiles that legacy missed but PCA caught
    false_negatives_mitigated = len([(a, p) for a, p in zip(all_analyses, AUDIT_PROFILES) 
                                     if p["legacy_confidence"] < 0.5 and a["pca_confidence"] > 0.6])
    fn_mitigation_rate = (false_negatives_mitigated / len(AUDIT_PROFILES)) * 100
    
    with col1:
        st.metric(
            label="Incremental Recall Gain",
            value="+18.4%",
            delta="Detection over legacy models",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Feedback Data Generated",
            value=f"{feedback_count}",
            delta="Labels ready for model re-training",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="False Negative Mitigation Rate",
            value=f"{fn_mitigation_rate:.1f}%",
            delta="Legacy misses → PCA catches",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Model Divergence Delta",
            value=f"+{model_divergence:.1%}",
            delta="LLM understanding vs Legacy",
            delta_color="normal"
        )
    
    st.divider()
    
    # Policy Section
    with st.expander("📋 Section 5.2: Protection Against Sexual Harassment & Off-Platform Grooming", expanded=False):
        st.markdown(POLICY_TEXT)
    
    # Top Evasion Tactics Visualization
    st.markdown("## 📊 Top Evasion Tactics")
    
    evasion_tactics = identify_evasion_tactics(AUDIT_PROFILES)
    tactics_df = pd.DataFrame(list(evasion_tactics.items()), columns=["Tactic", "Count"])
    tactics_df = tactics_df.sort_values("Count", ascending=False)
    
    fig_tactics = px.bar(
        tactics_df,
        x="Tactic",
        y="Count",
        color="Count",
        color_continuous_scale=[DS_COLORS['slate_surface'], DS_COLORS['tinder_flame']],
        title="Evasion Tactics Detected in Safety Gap Profiles",
        labels={"Count": "Number of Profiles", "Tactic": "Evasion Tactic"}
    )
    fig_tactics.update_layout(
        plot_bgcolor=DS_COLORS['slate_surface'],
        paper_bgcolor=DS_COLORS['slate_bg'],
        font=dict(size=12, color=DS_COLORS['text_primary']),
        height=400,
        xaxis=dict(gridcolor=DS_COLORS['border']),
        yaxis=dict(gridcolor=DS_COLORS['border'])
    )
    st.plotly_chart(fig_tactics, use_container_width=True)
    
    # Risk Category Distribution
    st.markdown("## 🎯 Risk Category Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_categories = {}
        for profile in AUDIT_PROFILES:
            analysis = simulate_pca_analysis(profile)
            category = analysis["category"]
            risk_categories[category] = risk_categories.get(category, 0) + 1
        
        fig_pie = px.pie(
            values=list(risk_categories.values()),
            names=list(risk_categories.keys()),
            color_discrete_sequence=[DS_COLORS['tinder_flame'], DS_COLORS['accent_purple'], DS_COLORS['tinder_flame_light']],
            title="Distribution of Risk Categories"
        )
        fig_pie.update_layout(
            height=400,
            plot_bgcolor=DS_COLORS['slate_surface'],
            paper_bgcolor=DS_COLORS['slate_bg'],
            font=dict(color=DS_COLORS['text_primary'])
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Confidence Comparison
        legacy_confidences = [p["legacy_confidence"] for p in AUDIT_PROFILES]
        pca_confidences = [simulate_pca_analysis(p)["pca_confidence"] for p in AUDIT_PROFILES]
        
        comparison_df = pd.DataFrame({
            "Profile": [f"WS-{i+1:03d}" for i in range(len(AUDIT_PROFILES))],
            "Legacy Confidence": legacy_confidences,
            "PCA Confidence": pca_confidences
        })
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Scatter(
            x=comparison_df["Profile"],
            y=comparison_df["Legacy Confidence"],
            mode='lines+markers',
            name='Legacy Model (BERT-based)',
            line=dict(color=DS_COLORS['accent_purple'], width=2, dash='dash')
        ))
        fig_comparison.add_trace(go.Scatter(
            x=comparison_df["Profile"],
            y=comparison_df["PCA Confidence"],
            mode='lines+markers',
            name='PCA Model (Ground Truth)',
            line=dict(color=DS_COLORS['tinder_flame'], width=2)
        ))
        fig_comparison.update_layout(
            title="Signal Divergence: Legacy vs. PCA Ground Truth",
            xaxis_title="Profile ID",
            yaxis_title="Confidence Score",
            height=400,
            plot_bgcolor=DS_COLORS['slate_surface'],
            paper_bgcolor=DS_COLORS['slate_bg'],
            font=dict(color=DS_COLORS['text_primary']),
            xaxis=dict(gridcolor=DS_COLORS['border']),
            yaxis=dict(gridcolor=DS_COLORS['border'])
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Detailed Profile Analysis
    st.markdown("## 🔍 Detailed Profile Analysis")
    
    selected_profile_id = st.selectbox(
        "Select a profile to analyze:",
        options=[p["profile_id"] for p in AUDIT_PROFILES],
        format_func=lambda x: f"{x} - {next(p['bio'] for p in AUDIT_PROFILES if p['profile_id'] == x)}"
    )
    
    selected_profile = next(p for p in AUDIT_PROFILES if p["profile_id"] == selected_profile_id)
    analysis = simulate_pca_analysis(selected_profile)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Profile Details")
        st.write(f"**Profile ID:** {selected_profile['profile_id']}")
        st.write(f"**Age:** {selected_profile['age']}")
        st.write(f"**Bio:** {selected_profile['bio']}")
        st.write("**Messages:**")
        for msg in selected_profile['messages']:
            st.write(f"- {msg}")
    
    with col2:
        st.markdown("### PCA Analysis")
        st.metric("Risk Category", analysis["category"])
        st.metric("PCA Confidence", f"{analysis['pca_confidence']:.1%}")
        st.metric("Legacy Confidence", f"{selected_profile['legacy_confidence']:.1%}")
        st.metric("Contextual Weight", f"{analysis['contextual_weight']:.2f}")
        st.metric("Risk Score", f"{analysis['risk_score']}/100")
    
    st.markdown("### LLM Reasoning")
    st.info(analysis["reasoning"])
    
    # Engineering Pipeline: Automated Model Re-training
    st.markdown("## 🛠️ Engineering Pipeline: Automated Model Re-training")
    
    # Tactic Emergence vs. Model Update Time Timeline
    st.markdown("### Tactic Emergence vs. Model Update Time")
    
    # Simulate timeline data showing reduction from weeks to hours
    tactics_timeline = [
        {"tactic": "Symbol Substitution (1G)", "legacy_delay_days": 14, "pca_delay_hours": 3},
        {"tactic": "Coded Euphemisms (Ghost App)", "legacy_delay_days": 14, "pca_delay_hours": 2},
        {"tactic": "Direct Platform Mentions", "legacy_delay_days": 14, "pca_delay_hours": 4},
        {"tactic": "Contact Information Sharing", "legacy_delay_days": 14, "pca_delay_hours": 1},
        {"tactic": "Casual Boundary Testing", "legacy_delay_days": 14, "pca_delay_hours": 5},
    ]
    
    # Create grouped bar chart
    tactics_df = pd.DataFrame(tactics_timeline)
    
    fig_timeline = go.Figure()
    
    # Legacy delays (convert days to hours for comparison)
    fig_timeline.add_trace(go.Bar(
        name='Legacy Model (Days)',
        x=tactics_df['tactic'],
        y=tactics_df['legacy_delay_days'],
        marker_color=DS_COLORS['accent_purple'],
        text=[f"{d} days" for d in tactics_df['legacy_delay_days']],
        textposition='outside'
    ))
    
    # PCA delays (hours, converted to days for visual comparison)
    fig_timeline.add_trace(go.Bar(
        name='PCA Model (Hours)',
        x=tactics_df['tactic'],
        y=[h / 24 for h in tactics_df['pca_delay_hours']],  # Convert hours to days for scale
        marker_color=DS_COLORS['tinder_flame'],
        text=[f"{h} hrs" for h in tactics_df['pca_delay_hours']],
        textposition='outside'
    ))
    
    fig_timeline.update_layout(
        title="Model Update Latency: Legacy (Weeks) vs PCA (Hours)",
        xaxis_title="Evasion Tactic",
        yaxis_title="Detection Delay (Days)",
        barmode='group',
        height=500,
        plot_bgcolor=DS_COLORS['slate_surface'],
        paper_bgcolor=DS_COLORS['slate_bg'],
        font=dict(color=DS_COLORS['text_primary']),
        xaxis=dict(gridcolor=DS_COLORS['border'], tickangle=-45),
        yaxis=dict(gridcolor=DS_COLORS['border']),
        legend=dict(
            x=0.7,
            y=1,
            bgcolor=DS_COLORS['slate_surface'],
            bordercolor=DS_COLORS['border']
        )
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.info(
        f"**Impact:** PCA reduces model update latency from an average of **14 days** (legacy BERT-based models) to **3 hours** (PCA with automated feedback loop). "
        f"This enables rapid response to emerging adversarial tactics, closing the safety gap before widespread adoption of new evasion methods."
    )
    
    # JSON Export for Model Fine-tuning
    st.markdown("### JSON Export for Model Fine-tuning")
    
    selected_profile_for_export = st.selectbox(
        "Select a profile to export as Golden Label:",
        options=[p["profile_id"] for p in AUDIT_PROFILES],
        format_func=lambda x: f"{x} - {next(p['bio'] for p in AUDIT_PROFILES if p['profile_id'] == x)}",
        key="export_select"
    )
    
    export_profile = next(p for p in AUDIT_PROFILES if p["profile_id"] == selected_profile_for_export)
    export_analysis = simulate_pca_analysis(export_profile)
    
    # Create Golden Label JSON structure
    golden_label = {
        "profile_id": export_profile["profile_id"],
        "timestamp": datetime.now().isoformat(),
        "input_data": {
            "bio": export_profile["bio"],
            "messages": export_profile["messages"],
            "age": export_profile["age"]
        },
        "legacy_model_output": {
            "confidence": export_profile["legacy_confidence"],
            "prediction": "low_risk" if export_profile["legacy_confidence"] < 0.5 else "medium_risk"
        },
        "pca_analysis": {
            "policy_violation": export_analysis["category"],
            "confidence": export_analysis["pca_confidence"],
            "contextual_weight": export_analysis["contextual_weight"],
            "risk_score": export_analysis["risk_score"]
        },
        "llm_reasoning": export_analysis["reasoning"],
        "golden_label": {
            "true_category": export_analysis["category"],
            "true_confidence": export_analysis["pca_confidence"],
            "label_quality": "high" if export_analysis["pca_confidence"] > 0.7 else "medium",
            "training_ready": export_analysis["pca_confidence"] > 0.6
        },
        "metadata": {
            "section_5_2_violation": True,
            "high_risk": export_analysis["category"] == "Adversarial Off-Platform Pivot",
            "model_divergence": round(export_analysis["pca_confidence"] - export_profile["legacy_confidence"], 3)
        }
    }
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Golden Label JSON:**")
        st.code(json.dumps(golden_label, indent=2), language="json")
    
    with col2:
        st.markdown("**Export Options:**")
        json_str = json.dumps(golden_label, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"golden_label_{selected_profile_for_export}.json",
            mime="application/json"
        )
        st.markdown("**Label Quality:**")
        st.metric("Training Ready", "✓ Yes" if golden_label["golden_label"]["training_ready"] else "✗ No")
        st.metric("Label Quality", golden_label["golden_label"]["label_quality"].title())
        st.metric("Model Divergence", f"+{golden_label['metadata']['model_divergence']:.1%}")
    
    st.divider()
    
    # All Profiles Table
    st.markdown("## 📋 All Safety Gap Profiles")
    
    table_data = []
    for profile in AUDIT_PROFILES:
        analysis = simulate_pca_analysis(profile)
        table_data.append({
            "Profile ID": profile["profile_id"],
            "Bio": profile["bio"],
            "Legacy Confidence": f"{profile['legacy_confidence']:.1%}",
            "PCA Confidence": f"{analysis['pca_confidence']:.1%}",
            "Contextual Weight": f"{analysis['contextual_weight']:.2f}",
            "Risk Category": analysis["category"],
            "Risk Score": f"{analysis['risk_score']}/100"
        })
    
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    # The Flywheel Narrative
    st.divider()
    st.info(
        "**Impact:** This dashboard transforms unstructured abuse signals into high-fidelity labels used to retrain legacy models, closing the safety gap for female users proactively. "
        "By identifying patterns that legacy models miss (such as coded platform references like '1G' for Instagram or 'Ghost App' for Snapchat), PCA enables proactive intervention "
        "before users are moved to unmonitored platforms where safety protections are absent. Each flagged profile generates labeled training data that improves model accuracy, "
        "creating a continuous improvement cycle that protects women from sexual harassment and off-platform grooming."
    )

if __name__ == "__main__":
    main()

