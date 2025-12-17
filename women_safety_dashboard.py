import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import time

# Page configuration
st.set_page_config(
    page_title="Tinder PCA: Women's Safety & Proactive Intervention",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data Science & Engineering Color Palette - Sophisticated Slate with Tinder Accents
DS_COLORS = {
    'slate_bg': '#f8fafc',  # Slate-50 - Light background for readability
    'zinc_bg': '#f1f5f9',  # Slate-100
    'slate_surface': '#ffffff',  # White for cards/surfaces
    'slate_border': '#e2e8f0',  # Slate-200 for borders
    'tinder_flame': '#FF4458',  # Tinder Red/Flame
    'tinder_flame_light': '#FF6B9D',  # Light Tinder accent
    'accent_purple': '#8b5cf6',  # Purple accent
    'text_primary': '#0f172a',  # Slate-900 - Dark text for readability
    'text_secondary': '#475569',  # Slate-600
    'text_muted': '#64748b',  # Slate-500
    'success': '#10b981',  # Green
    'warning': '#f59e0b',  # Amber
    'border': '#cbd5e1'  # Slate-300
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

def show_blank_slate():
    """Display blank slate view before audit is run"""
    # Header
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {DS_COLORS['slate_surface']} 0%, {DS_COLORS['zinc_bg']} 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; 
                    border-left: 4px solid {DS_COLORS['tinder_flame']};
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: {DS_COLORS['text_primary']}; text-align: center; margin: 0; font-size: 2rem;'>
                🛡️ Tinder PCA: Women's Safety & Proactive Intervention
            </h1>
            <p style='color: {DS_COLORS['text_secondary']}; text-align: center; margin-top: 0.5rem; font-size: 1.1rem;'>
                Detecting Sexual Abuse Intent & Off-Platform Grooming
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Idle message
    st.markdown(
        f"""
        <div style='background-color: {DS_COLORS['slate_surface']}; padding: 3rem; border-radius: 10px; 
                    text-align: center; border: 2px dashed {DS_COLORS['slate_border']}; margin-bottom: 2rem;'>
            <h2 style='color: {DS_COLORS['text_secondary']}; margin-bottom: 1rem;'>⏸️ System Idle</h2>
            <p style='color: {DS_COLORS['text_secondary']}; font-size: 1.1rem;'>
                Waiting for profile batch...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Start Audit Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Policy Audit", use_container_width=True, type="primary", key="start_audit"):
            st.session_state.running_simulation = True
            st.rerun()
    
    # Sample Data Queue Section
    st.markdown("## 📋 Sample Data Queue")
    st.markdown("**Profiles pending analysis:**")
    
    queue_data = []
    for profile in AUDIT_PROFILES:
        queue_data.append({
            "Profile ID": profile["profile_id"],
            "Bio": profile["bio"],
            "Age": profile["age"],
            "Message Count": len(profile["messages"]),
            "Status": "⏳ Pending"
        })
    
    queue_df = pd.DataFrame(queue_data)
    st.dataframe(queue_df, use_container_width=True, hide_index=True)
    
    st.info(
        "**Note:** These profiles represent the 'safety gap' - cases where legacy models scored between 0.30-0.48 confidence. "
        "Click 'Start Policy Audit' to run PCA analysis and reveal policy violations."
    )

def run_simulation():
    """Run the simulation with progress indicators"""
    # Header
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {DS_COLORS['slate_surface']} 0%, {DS_COLORS['zinc_bg']} 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; 
                    border-left: 4px solid {DS_COLORS['tinder_flame']};
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: {DS_COLORS['text_primary']}; text-align: center; margin: 0; font-size: 2rem;'>
                🛡️ Tinder PCA: Women's Safety & Proactive Intervention
            </h1>
            <p style='color: {DS_COLORS['text_secondary']}; text-align: center; margin-top: 0.5rem; font-size: 1.1rem;'>
                Detecting Sexual Abuse Intent & Off-Platform Grooming
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.status("🔌 Connecting to PCA LLM Engine...", expanded=True) as status:
        time.sleep(1)
        status.update(label="📥 Ingesting Safety Policies...", state="running")
        time.sleep(1)
        status.update(label="🔍 Analyzing Linguistic Divergence...", state="running")
        time.sleep(1)
        status.update(label="📊 Generating Policy Violation Reports...", state="running")
        time.sleep(1)
        status.update(label="✅ Audit Complete!", state="complete")
    
    # Set audit complete and reset simulation flag
    st.session_state.audit_complete = True
    st.session_state.running_simulation = False
    
    # Show success animation
    st.balloons()
    
    # Success message
    st.success("🎉 Policy audit completed successfully! Dashboard data loaded.")
    
    # Rerun to show the full dashboard
    time.sleep(0.5)
    st.rerun()

# Initialize Session State
def init_session_state():
    """Initialize session state variables"""
    if 'audit_complete' not in st.session_state:
        st.session_state.audit_complete = False
    if 'running_simulation' not in st.session_state:
        st.session_state.running_simulation = False

# Main Dashboard
def main():
    # Initialize session state
    init_session_state()
    
    # Sidebar with reset functionality
    with st.sidebar:
        st.markdown("## 🛠️ Control Panel")
        st.markdown("---")
        
        if st.session_state.audit_complete:
            st.success("✅ Audit Complete")
            if st.button("🔄 Reset Audit", use_container_width=True, type="secondary"):
                st.session_state.audit_complete = False
                st.session_state.running_simulation = False
                st.rerun()
        else:
            st.info("⏸️ System Idle")
        
        st.markdown("---")
        st.markdown("### System Status")
        status_text = "🟢 Active" if st.session_state.audit_complete else "🟡 Idle"
        st.markdown(f"**Status:** {status_text}")
        
        st.markdown("---")
        st.markdown("### About")
        st.caption("Tinder PCA: Women's Safety Dashboard")
        st.caption("Policy-Constrained Analysis Engine")
    
    # Apply sophisticated styling with better readability
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {DS_COLORS['slate_bg']};
        }}
        .main .block-container {{
            background-color: {DS_COLORS['slate_bg']};
            padding-top: 2rem;
            max-width: 95%;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {DS_COLORS['text_primary']};
            font-weight: 600;
        }}
        p, li, span, div {{
            color: {DS_COLORS['text_primary']};
        }}
        .stMetric {{
            background-color: {DS_COLORS['slate_surface']};
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid {DS_COLORS['slate_border']};
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stMetric label {{
            color: {DS_COLORS['text_secondary']};
            font-weight: 500;
        }}
        .stMetric [data-testid="stMetricValue"] {{
            color: {DS_COLORS['text_primary']};
            font-weight: 700;
        }}
        .stDataFrame {{
            background-color: {DS_COLORS['slate_surface']};
        }}
        .stSelectbox label, .stTextInput label {{
            color: {DS_COLORS['text_primary']};
            font-weight: 500;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Check if simulation is running
    if st.session_state.running_simulation and not st.session_state.audit_complete:
        run_simulation()
        return
    
    # Check if audit is complete - show blank slate or full dashboard
    if not st.session_state.audit_complete:
        show_blank_slate()
        return
    
    # Full Dashboard - Only shown after audit is complete
    # Header
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {DS_COLORS['slate_surface']} 0%, {DS_COLORS['zinc_bg']} 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; 
                    border-left: 4px solid {DS_COLORS['tinder_flame']};
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: {DS_COLORS['text_primary']}; text-align: center; margin: 0; font-size: 2rem;'>
                🛡️ Tinder PCA: Women's Safety & Proactive Intervention
            </h1>
            <p style='color: {DS_COLORS['text_secondary']}; text-align: center; margin-top: 0.5rem; font-size: 1.1rem;'>
                Detecting Sexual Abuse Intent & Off-Platform Grooming
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Incoming Audit Queue - Moved to top for Live Triage flow
    st.markdown("## 📥 Incoming Audit Queue: High-Risk Grey Area")
    st.caption("Profiles below are scored as 'Safe' (0.3-0.5) by production BERT models but flagged for PCA Deep-Scan.")
    
    # Build table data
    table_data = []
    all_analyses = []
    for profile in AUDIT_PROFILES:
        analysis = simulate_pca_analysis(profile)
        all_analyses.append(analysis)
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
    
    # Display table with column styling
    st.dataframe(
        df_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Profile ID": st.column_config.TextColumn("Profile ID", width="small"),
            "Bio": st.column_config.TextColumn("Bio", width="large"),
            "Legacy Confidence": st.column_config.TextColumn(
                "Legacy Confidence",
                width="medium",
                help="BERT-based model confidence score"
            ),
            "PCA Confidence": st.column_config.TextColumn(
                "PCA Confidence",
                width="medium",
                help="PCA LLM confidence score"
            ),
            "Contextual Weight": st.column_config.TextColumn("Contextual Weight", width="small"),
            "Risk Category": st.column_config.TextColumn("Risk Category", width="medium"),
            "Risk Score": st.column_config.TextColumn("Risk Score", width="small")
        }
    )
    
    # Add CSS to highlight columns - Visual mapping of the confidence gap
    st.markdown(
        f"""
        <style>
        /* Highlight Legacy Confidence column (3rd column) in grey */
        div[data-testid="stDataFrame"] table thead th:nth-child(3),
        div[data-testid="stDataFrame"] table tbody td:nth-child(3) {{
            background-color: #e2e8f0 !important;
            font-weight: 600;
            color: #475569 !important;
        }}
        /* Highlight PCA Confidence column (4th column) in Tinder Flame red */
        div[data-testid="stDataFrame"] table thead th:nth-child(4),
        div[data-testid="stDataFrame"] table tbody td:nth-child(4) {{
            background-color: rgba(255, 68, 88, 0.15) !important;
            color: {DS_COLORS['tinder_flame']} !important;
            font-weight: 700;
        }}
        </style>
        """,
        unsafe_allow_html=True
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
        color_continuous_scale=['#e2e8f0', DS_COLORS['tinder_flame']],
        title="Evasion Tactics Detected in Safety Gap Profiles",
        labels={"Count": "Number of Profiles", "Tactic": "Evasion Tactic"}
    )
    fig_tactics.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13, color=DS_COLORS['text_primary']),
        height=450,
        autosize=True,
        margin=dict(l=50, r=50, t=60, b=100),
        xaxis=dict(
            gridcolor=DS_COLORS['slate_border'],
            tickangle=-45,
            title_font=dict(size=13),
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor=DS_COLORS['slate_border'],
            title_font=dict(size=13),
            tickfont=dict(size=11)
        ),
        title_font=dict(size=16, color=DS_COLORS['text_primary'])
    )
    st.plotly_chart(fig_tactics, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
    
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
            height=450,
            autosize=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color=DS_COLORS['text_primary']),
            title_font=dict(size=15, color=DS_COLORS['text_primary']),
            margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(
                font=dict(size=11, color=DS_COLORS['text_primary']),
                bgcolor='white',
                bordercolor=DS_COLORS['slate_border'],
                borderwidth=1
            )
        )
        fig_pie.update_traces(textfont=dict(size=12, color=DS_COLORS['text_primary']))
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
    
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
            line=dict(color=DS_COLORS['accent_purple'], width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig_comparison.add_trace(go.Scatter(
            x=comparison_df["Profile"],
            y=comparison_df["PCA Confidence"],
            mode='lines+markers',
            name='PCA Model (Ground Truth)',
            line=dict(color=DS_COLORS['tinder_flame'], width=3),
            marker=dict(size=8)
        ))
        fig_comparison.update_layout(
            title="Signal Divergence: Legacy vs. PCA Ground Truth",
            xaxis_title="Profile ID",
            yaxis_title="Confidence Score",
            height=450,
            autosize=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color=DS_COLORS['text_primary']),
            title_font=dict(size=15, color=DS_COLORS['text_primary']),
            margin=dict(l=50, r=30, t=60, b=50),
            xaxis=dict(
                gridcolor=DS_COLORS['slate_border'],
                title_font=dict(size=13),
                tickfont=dict(size=11),
                tickangle=-45
            ),
            yaxis=dict(
                gridcolor=DS_COLORS['slate_border'],
                title_font=dict(size=13),
                tickfont=dict(size=11)
            ),
            legend=dict(
                font=dict(size=11, color=DS_COLORS['text_primary']),
                bgcolor='white',
                bordercolor=DS_COLORS['slate_border'],
                borderwidth=1
            )
        )
        st.plotly_chart(fig_comparison, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
    
    # Detailed Profile Analysis
    st.markdown("## 🔍 Detailed Profile Analysis")
    st.caption("Select a profile from the queue above to view detailed PCA reasoning and analysis.")
    
    # Get the analysis for the selected profile (use the same analyses from table generation)
    selected_profile_id = st.selectbox(
        "Select a profile to analyze:",
        options=[p["profile_id"] for p in AUDIT_PROFILES],
        format_func=lambda x: f"{x} - {next(p['bio'] for p in AUDIT_PROFILES if p['profile_id'] == x)}",
        key="profile_selector"
    )
    
    selected_profile = next(p for p in AUDIT_PROFILES if p["profile_id"] == selected_profile_id)
    # Use the same analysis that was generated for the table
    analysis = next(a for a, p in zip(all_analyses, AUDIT_PROFILES) if p["profile_id"] == selected_profile_id)
    
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
        autosize=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, color=DS_COLORS['text_primary']),
        title_font=dict(size=16, color=DS_COLORS['text_primary']),
        margin=dict(l=50, r=30, t=60, b=120),
        xaxis=dict(
            gridcolor=DS_COLORS['slate_border'],
            tickangle=-45,
            title_font=dict(size=13),
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor=DS_COLORS['slate_border'],
            title_font=dict(size=13),
            tickfont=dict(size=11)
        ),
        legend=dict(
            x=0.7,
            y=1.02,
            bgcolor='white',
            bordercolor=DS_COLORS['slate_border'],
            borderwidth=1,
            font=dict(size=11, color=DS_COLORS['text_primary'])
        )
    )
    fig_timeline.update_traces(textfont=dict(size=10, color=DS_COLORS['text_primary']))
    st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
    
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

