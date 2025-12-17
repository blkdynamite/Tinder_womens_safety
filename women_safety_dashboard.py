import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Tinder PCA: Women's Safety & Proactive Intervention",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Trust & Safety Color Palette
TRUST_SAFETY_COLORS = {
    'primary': '#8B2E8B',  # Deep Purple
    'secondary': '#FF4458',  # Tinder Red
    'accent': '#FF6B9D',  # Pink accent
    'success': '#4CAF50',
    'warning': '#FF9800',
    'background': '#F5F5F5'
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
    """
    bio = profile["bio"].lower()
    messages = " ".join(profile["messages"]).lower()
    combined_text = f"{bio} {messages}"
    
    # Determine risk category and generate reasoning
    if any(code in combined_text for code in ["1g", "ghost app", "insta", "snap", "whatsapp", "telegram"]):
        category = "Adversarial Off-Platform Pivot"
        if "1g" in combined_text:
            reasoning = "Legacy filters missed '1G' as a keyword; PCA identified it as an intentional evasion of the Instagram blocklist to facilitate unmonitored messaging. The coded reference demonstrates adversarial behavior designed to bypass platform safety tools."
        elif "ghost app" in combined_text:
            reasoning = "PCA detected 'Ghost App' as a coded reference to Snapchat, which legacy models failed to flag. This represents a deliberate attempt to move conversations to an unmonitored platform where safety protections are absent."
        else:
            reasoning = "PCA identified explicit off-platform pivot attempts that legacy models missed. Moving conversations to external platforms removes critical safety monitoring and enables predatory behavior in unmonitored environments."
    elif any(term in combined_text for term in ["submissive", "dominated", "spoil", "control", "bdsm"]):
        category = "Sexualized Grooming"
        reasoning = "PCA detected sexualized grooming patterns through coded language that legacy models classified as low-risk. The use of terms like 'submissive' and 'spoil' in early-stage profiles indicates intent to establish inappropriate power dynamics and sexualized relationships."
    else:
        category = "Boundary Testing"
        reasoning = "PCA identified boundary testing behavior through patterns of directness and pressure tactics that legacy models failed to recognize. The profile demonstrates intent to push against user boundaries and test limits systematically."
    
    # Calculate PCA confidence (higher than legacy for safety gap profiles)
    pca_confidence = min(0.95, profile["legacy_confidence"] + random.uniform(0.15, 0.35))
    
    return {
        "category": category,
        "pca_confidence": round(pca_confidence, 3),
        "legacy_confidence": profile["legacy_confidence"],
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
    # Header
    st.markdown(
        f"""
        <div style='background: linear-gradient(90deg, {TRUST_SAFETY_COLORS['primary']}, {TRUST_SAFETY_COLORS['secondary']}); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>
                🛡️ Tinder PCA: Women's Safety & Proactive Intervention
            </h1>
            <p style='color: white; text-align: center; margin-top: 0.5rem; opacity: 0.9;'>
                Detecting Sexual Abuse Intent & Off-Platform Grooming
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Strategic Impact Section
    st.markdown("## 🚀 Strategic Safety Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Safety Gap Coverage",
            value="+18.4%",
            delta="Detection over legacy models",
            delta_color="normal"
        )
    
    with col2:
        feedback_count = len([p for p in AUDIT_PROFILES if simulate_pca_analysis(p)["pca_confidence"] > 0.6])
        st.metric(
            label="Feedback Data Generated",
            value=f"{feedback_count}",
            delta="Labels ready for model re-training",
            delta_color="normal"
        )
    
    with col3:
        high_risk_count = len([p for p in AUDIT_PROFILES if simulate_pca_analysis(p)["category"] == "Adversarial Off-Platform Pivot"])
        st.metric(
            label="High-Risk Violations",
            value=f"{high_risk_count}",
            delta="Off-platform pivot attempts",
            delta_color="inverse"
        )
    
    with col4:
        avg_confidence_boost = sum([simulate_pca_analysis(p)["pca_confidence"] - p["legacy_confidence"] for p in AUDIT_PROFILES]) / len(AUDIT_PROFILES)
        st.metric(
            label="Avg Confidence Boost",
            value=f"+{avg_confidence_boost:.1%}",
            delta="PCA vs Legacy",
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
        color_continuous_scale=["#8B2E8B", "#FF4458"],
        title="Evasion Tactics Detected in Safety Gap Profiles",
        labels={"Count": "Number of Profiles", "Tactic": "Evasion Tactic"}
    )
    fig_tactics.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        height=400
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
            color_discrete_sequence=[TRUST_SAFETY_COLORS['primary'], TRUST_SAFETY_COLORS['secondary'], TRUST_SAFETY_COLORS['accent']],
            title="Distribution of Risk Categories"
        )
        fig_pie.update_layout(height=400)
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
            name='Legacy Model',
            line=dict(color=TRUST_SAFETY_COLORS['primary'], width=2, dash='dash')
        ))
        fig_comparison.add_trace(go.Scatter(
            x=comparison_df["Profile"],
            y=comparison_df["PCA Confidence"],
            mode='lines+markers',
            name='PCA Model',
            line=dict(color=TRUST_SAFETY_COLORS['secondary'], width=2)
        ))
        fig_comparison.update_layout(
            title="Confidence Comparison: Legacy vs PCA",
            xaxis_title="Profile ID",
            yaxis_title="Confidence Score",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white"
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
        st.metric("Risk Score", f"{analysis['risk_score']}/100")
    
    st.markdown("### LLM Reasoning")
    st.info(analysis["reasoning"])
    
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

