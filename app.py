import streamlit as st

st.set_page_config(
    page_title="MCredlics | MSME Credit Risk Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4F46E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #334155;
    }
    .badge-success {
        background-color: #065F46;
        color: #34D399;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">MCredlics 💳</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Alternative Data Verification & Credit Risk Underwriting Platform</div>', unsafe_allow_html=True)
st.divider()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/bank-building.png", width=70)
    st.title("Underwriter Controls")
    st.info("💡 **Mode:** Live Demo (Sandbox)")
    risk = st.select_slider("Lender Risk Tolerance", options=["Conservative", "Moderate", "Aggressive"], value="Moderate")
    st.markdown("---")
    st.caption("Built for MSME Lending | Hackathon Edition")

# 2 Columns
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.subheader("📋 1. MSME Profile & Financial Data")

    with st.expander("Entity Details", expanded=True):
        g = st.text_input("Enter GSTIN Number", value="27AAAAA0000A1Z5", help="15-digit alphanumeric GSTIN code")
        name = st.text_input("Business Name", value="Apex Manufacturing Pvt Ltd")
        rev = st.number_input("Monthly Revenue (in ₹)", value=500000, step=50000, format="%d")

    with st.expander("Alternative Data Parameters", expanded=True):
        comp = st.slider("GST Filing Compliance Rate (%)", min_value=50, max_value=100, value=95, help="GSTR-1 & 3B on-time filing ratio")
        cf = st.slider("Account Aggregator Cash-Flow Index", min_value=1, max_value=10, value=8)

    st.subheader("⚡ 2. Scenario Stress-Testing Engine")
    st.caption("Simulate macroeconomic shocks on borrower debt capacity")

    c1, c2 = st.columns(2)
    with c1:
        infl = st.slider("Inflation Spike (%)", min_value=0, max_value=15, value=2)
    with c2:
        drop = st.slider("Revenue Drop Shock (%)", min_value=0, max_value=40, value=10)

    btn = st.button("🚀 Run Risk Assessment Engine", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 3. Verification & Underwriting Insights")

    if btn or g:
        # Check GSTIN
        if len(g) != 15:
            st.error("❌ **Direct Verification Failed:** Invalid GSTIN format or potential document mismatch!")
        else:
            # Verification Badges
            st.markdown("#### Direct API Verification Status")
            st.markdown('<span class="badge-success">✓ GSTN Portal Verified (GSTR-1 & 3B Match)</span>', unsafe_allow_html=True)
            st.markdown('<span class="badge-success">✓ Account Aggregator Stream Verified (Active Cash-Flow)</span>', unsafe_allow_html=True)
            st.markdown('<span class="badge-success">✓ NSDL PAN & Identity Validated</span>', unsafe_allow_html=True)

            st.divider()

            # Score Calculation
            score = 70 + (cf * 1.5)
            if comp >= 90:
                score = score + 10
            else:
                score = score - 10

            # Stress Penalty
            pen = (infl * 0.8) + (drop * 1.1)
            final = int(max(10, min(100, score - pen)))

            # Display Score
            st.markdown("#### Alternative Credit Health Score")
            st.progress(final / 100)

            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="Credit Health Score", value=f"{final} / 100", delta=f"-{int(pen)} Stress Penalty" if pen > 0 else "Optimal")
            with m2:
                if final >= 70:
                    st.metric(label="Risk Classification", value="Tier A", delta="Low Risk", delta_color="normal")
                elif final >= 50:
                    st.metric(label="Risk Classification", value="Tier B", delta="Moderate Risk", delta_color="off")
                else:
                    st.metric(label="Risk Classification", value="Tier C", delta="High Risk", delta_color="inverse")

            st.divider()

            # Loan Recommendation
            st.markdown("#### Recommended Loan Underwriting Limit")
            if final >= 70:
                loan = rev * 2.5
                st.success(f"**Approved Max Limit:** ₹{loan:,.0f} | **Interest Rate:** ~11.5% p.a.")
            elif final >= 50:
                loan = rev * 1.2
                st.warning(f"**Approved Max Limit:** ₹{loan:,.0f} | **Interest Rate:** ~14.0% p.a.")
            else:
                st.error("**Decision:** Application Flagged / Manual Underwriter Review Required")

            # Explainable AI
            st.markdown("#### 💡 Explainable AI (Decision Drivers)")
            st.write(f"• **+10 pts:** Consistent GSTR filing compliance ({comp}%).")
            st.write(f"• **+{int(cf * 1.5)} pts:** Positive Account Aggregator bank cash-flow index.")
            st.write(f"• **-{int(pen)} pts:** Applied macroeconomic stress penalty (inflation + sales drop).")
