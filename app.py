"""
ESG Integration in Credit Risk Governance:
A Comparative Case Study of DBS Bank and Emirates NBD
Complete Streamlit Dashboard – app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Credit Risk Governance",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
DBS_COLOR      = "#E31837"
ENBD_COLOR     = "#005B99"
ACCENT_GREEN   = "#2ECC71"
ACCENT_AMBER   = "#F39C12"
ACCENT_RED     = "#E74C3C"
BG_DARK        = "#0F1117"
CARD_BG        = "#1E2130"
TEXT_LIGHT     = "#FAFAFA"

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Main background */
  .stApp {{ background-color: {BG_DARK}; color: {TEXT_LIGHT}; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #1a1f36 0%, #0d1117 100%);
      border-right: 1px solid #2d3250;
  }}

  /* Cards */
  .metric-card {{
      background: {CARD_BG};
      border-radius: 12px;
      padding: 20px 24px;
      border-left: 4px solid {ACCENT_GREEN};
      margin-bottom: 16px;
  }}
  .metric-card h2 {{ font-size: 2rem; margin: 4px 0; color: {ACCENT_GREEN}; }}
  .metric-card p  {{ margin: 0; color: #9aa3bf; font-size: 0.85rem; }}

  /* Section header */
  .section-header {{
      background: linear-gradient(90deg, {CARD_BG} 0%, #0F1117 100%);
      border-left: 4px solid {ACCENT_GREEN};
      padding: 10px 18px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 18px;
  }}

  /* Page title */
  h1 {{ color: {TEXT_LIGHT} !important; }}

  /* Divider */
  hr {{ border-color: #2d3250; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    # ── ESG Master Datasheet ──────────────────
    esg_raw = pd.read_csv("ESG-Master_Datasheet.csv", header=None, skiprows=8)
    esg_raw.columns = esg_raw.iloc[0]
    esg_df = esg_raw.drop(0).reset_index(drop=True)
    esg_df.columns.name = None

    numeric_cols = ["Year", "Governance", "SustainableFinance",
                    "ClimateRisk", "Disclosure", "RegulatoryAlignment"]
    for c in numeric_cols:
        esg_df[c] = pd.to_numeric(esg_df[c], errors="coerce")

    esg_df["Overall_ESG_Score"] = esg_df[
        ["Governance", "SustainableFinance", "ClimateRisk",
         "Disclosure", "RegulatoryAlignment"]
    ].mean(axis=1).round(2)

    # ── Regulatory Gap Analysis ───────────────
    reg_df = pd.read_csv("Regulatory_Gap_Analysis.csv")

    # ── Scenario Analysis ─────────────────────
    scen_df = pd.read_csv("scenario_analysis.csv")

    return esg_df, reg_df, scen_df


try:
    esg_df, reg_df, scen_df = load_data()
    data_loaded = True
except FileNotFoundError as e:
    data_loaded = False
    load_error = str(e)

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ESG Governance")
    st.markdown("**Credit Risk Dashboard**")
    st.markdown("---")

    page = st.radio(
        "Navigate to",
        options=[
            "📊 Executive Dashboard",
            "📈 ESG Evolution Analysis",
            "⚖️ Regulatory Alignment",
            "🔮 Scenario Planning",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#9aa3bf;'>DBS Bank &nbsp;|&nbsp; Emirates NBD<br/>"
        "ESG Credit Risk Governance Study</small>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# GUARD: data not found
# ─────────────────────────────────────────────
if not data_loaded:
    st.error(f"⚠️  Could not load data files: {load_error}")
    st.info(
        "Place these three CSV files in the **same folder** as `app.py` and restart:\n"
        "- `ESG-Master_Datasheet.csv`\n"
        "- `Regulatory_Gap_Analysis.csv`\n"
        "- `scenario_analysis.csv`"
    )
    st.stop()


# ═════════════════════════════════════════════════════════════════════
# PAGE 1 – EXECUTIVE DASHBOARD
# ═════════════════════════════════════════════════════════════════════
if page == "📊 Executive Dashboard":

    st.markdown(
        "# 🌿 ESG Integration in Credit Risk Governance\n"
        "### Comparative Case Study: DBS Bank & Emirates NBD"
    )
    st.markdown("---")

    # ── KPI Cards ────────────────────────────────────────────────────
    dbs_latest  = esg_df[esg_df["Bank"] == "DBS"].sort_values("Year").iloc[-1]
    enbd_latest = esg_df[esg_df["Bank"] == "Emirates NBD"].sort_values("Year").iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
          <p>🏦 DBS Bank — Overall ESG</p>
          <h2>{dbs_latest['Overall_ESG_Score']:.1f} / 5</h2>
          <p>Latest year: {int(dbs_latest['Year'])}</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{ENBD_COLOR};">
          <p>🏦 Emirates NBD — Overall ESG</p>
          <h2 style="color:{ENBD_COLOR};">{enbd_latest['Overall_ESG_Score']:.1f} / 5</h2>
          <p>Latest year: {int(enbd_latest['Year'])}</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        avg_compliance = reg_df.groupby("Bank")["Score"].mean()
        dbs_comp  = avg_compliance.get("DBS", 0)
        enbd_comp = avg_compliance.get("Emirates NBD", 0)
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{ACCENT_AMBER};">
          <p>✅ Avg Regulatory Compliance</p>
          <h2 style="color:{ACCENT_AMBER};">DBS {dbs_comp:.1f}</h2>
          <p>Emirates NBD: {enbd_comp:.1f} (out of 5)</p>
        </div>""", unsafe_allow_html=True)

    with col4:
        scenarios = scen_df["Scenario"].nunique()
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:#9B59B6;">
          <p>🔮 Scenarios Analysed</p>
          <h2 style="color:#9B59B6;">{scenarios}</h2>
          <p>Across 2 banks</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Overview Line Chart ───────────────────────────────────────────
    st.markdown('<div class="section-header"><b>📈 Overall ESG Score Trajectory</b></div>',
                unsafe_allow_html=True)

    fig_line = px.line(
        esg_df, x="Year", y="Overall_ESG_Score", color="Bank",
        color_discrete_map={"DBS": DBS_COLOR, "Emirates NBD": ENBD_COLOR},
        markers=True,
        title="ESG Score Over Time",
        labels={"Overall_ESG_Score": "Avg ESG Score (1–5)", "Year": "Year"},
    )
    fig_line.update_layout(
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT, legend_title_text="Bank",
        yaxis=dict(range=[0, 5.5], gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ── Radar / Spider Chart ──────────────────────────────────────────
    st.markdown('<div class="section-header"><b>🕸️ ESG Dimensions — Latest Year Comparison</b></div>',
                unsafe_allow_html=True)

    dims = ["Governance", "SustainableFinance", "ClimateRisk",
            "Disclosure", "RegulatoryAlignment"]

    dbs_vals  = [float(dbs_latest[d])  for d in dims]
    enbd_vals = [float(enbd_latest[d]) for d in dims]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=dbs_vals + [dbs_vals[0]], theta=dims + [dims[0]],
        fill="toself", name="DBS Bank",
        line_color=DBS_COLOR, fillcolor=DBS_COLOR, opacity=0.3,
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=enbd_vals + [enbd_vals[0]], theta=dims + [dims[0]],
        fill="toself", name="Emirates NBD",
        line_color=ENBD_COLOR, fillcolor=ENBD_COLOR, opacity=0.3,
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor=CARD_BG,
            radialaxis=dict(visible=True, range=[0, 5], gridcolor="#2d3250",
                            color=TEXT_LIGHT),
            angularaxis=dict(color=TEXT_LIGHT),
        ),
        paper_bgcolor=CARD_BG, font_color=TEXT_LIGHT,
        title="ESG Dimension Radar — Latest Available Year",
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ── Key Insights ─────────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>💡 Key Insights</b></div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**🏆 DBS Bank** leads across all five ESG dimensions, reflecting "
                "MAS-driven regulatory integration and Singapore's mature sustainability ecosystem.")
    with c2:
        st.info("**📈 Emirates NBD** demonstrates strong recent growth, with governance "
                "reaching 5/5 in 2025, signalling accelerating ESG maturity in the UAE.")
    with c3:
        st.info("**⚡ Climate Risk** is the most contested dimension, showing the widest "
                "historic gap between the two banks and the greatest convergence opportunity.")


# ═════════════════════════════════════════════════════════════════════
# PAGE 2 – ESG EVOLUTION ANALYSIS
# ═════════════════════════════════════════════════════════════════════
elif page == "📈 ESG Evolution Analysis":

    st.title("📈 ESG Evolution Analysis")
    st.markdown("Explore how each bank's ESG dimensions have evolved year-by-year.")
    st.markdown("---")

    # Bank selector
    bank_choice = st.selectbox(
        "Select Bank",
        options=["Both Banks", "DBS Bank", "Emirates NBD"],
        index=0,
    )

    dims = ["Governance", "SustainableFinance", "ClimateRisk",
            "Disclosure", "RegulatoryAlignment"]

    if bank_choice == "Both Banks":
        plot_df = esg_df.copy()
    elif bank_choice == "DBS Bank":
        plot_df = esg_df[esg_df["Bank"] == "DBS"].copy()
    else:
        plot_df = esg_df[esg_df["Bank"] == "Emirates NBD"].copy()

    # ── Multi-Dimension Line Charts ───────────────────────────────────
    st.markdown('<div class="section-header"><b>📊 Dimension-Level Evolution</b></div>',
                unsafe_allow_html=True)

    melted = plot_df.melt(
        id_vars=["Bank", "Year"],
        value_vars=dims,
        var_name="Dimension",
        value_name="Score",
    )

    color_seq = [DBS_COLOR, ENBD_COLOR, ACCENT_GREEN, ACCENT_AMBER, "#9B59B6"]

    if bank_choice == "Both Banks":
        fig_multi = px.line(
            melted, x="Year", y="Score",
            color="Bank", facet_col="Dimension", facet_col_wrap=3,
            color_discrete_map={"DBS": DBS_COLOR, "Emirates NBD": ENBD_COLOR},
            markers=True,
            title="ESG Dimension Scores — Both Banks",
        )
    else:
        fig_multi = px.line(
            melted, x="Year", y="Score",
            color="Dimension", markers=True,
            color_discrete_sequence=color_seq,
            title=f"ESG Dimension Scores — {bank_choice}",
        )

    fig_multi.update_layout(
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT,
        yaxis=dict(range=[0, 5.5], gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
    )
    fig_multi.update_yaxes(range=[0, 5.5])
    st.plotly_chart(fig_multi, use_container_width=True)

    # ── Heatmap ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>🌡️ ESG Score Heatmap</b></div>',
                unsafe_allow_html=True)

    heatmap_bank = st.radio(
        "Heatmap — Bank",
        options=["DBS Bank", "Emirates NBD"],
        horizontal=True,
    )
    hm_key = "DBS" if heatmap_bank == "DBS Bank" else "Emirates NBD"
    hm_df  = esg_df[esg_df["Bank"] == hm_key][["Year"] + dims].set_index("Year")
    hm_df  = hm_df.astype(float)

    fig_heat = go.Figure(data=go.Heatmap(
        z=hm_df.values,
        x=dims,
        y=[str(int(y)) for y in hm_df.index],
        colorscale="RdYlGn",
        zmin=1, zmax=5,
        text=hm_df.values,
        texttemplate="%{text}",
        colorbar=dict(title="Score", tickfont=dict(color=TEXT_LIGHT)),
    ))
    fig_heat.update_layout(
        title=f"ESG Heatmap — {heatmap_bank}",
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT,
        xaxis=dict(title="ESG Dimension"),
        yaxis=dict(title="Year"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Raw Data Table ────────────────────────────────────────────────
    with st.expander("📋 View Raw ESG Data"):
        st.dataframe(
            plot_df.style.background_gradient(
                subset=dims, cmap="RdYlGn", vmin=1, vmax=5
            ),
            use_container_width=True,
        )


# ═════════════════════════════════════════════════════════════════════
# PAGE 3 – REGULATORY ALIGNMENT & GAP ANALYSIS
# ═════════════════════════════════════════════════════════════════════
elif page == "⚖️ Regulatory Alignment":

    st.title("⚖️ Regulatory Alignment & Gap Analysis")
    st.markdown("Assess how DBS and Emirates NBD align against key ESG regulatory requirements.")
    st.markdown("---")

    # ── Gap Analysis Table ────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>📋 Regulatory Compliance Table</b></div>',
                unsafe_allow_html=True)

    def color_status(val):
        if val == "Fully Aligned":
            return f"background-color: #1e4d2b; color: {ACCENT_GREEN};"
        elif val == "Partially Aligned":
            return f"background-color: #4d3b00; color: {ACCENT_AMBER};"
        else:
            return f"background-color: #4d1a1a; color: {ACCENT_RED};"

    styled = (
        reg_df.style
        .applymap(color_status, subset=["Status"])
        .background_gradient(subset=["Score"], cmap="RdYlGn", vmin=1, vmax=5)
        .set_properties(**{"background-color": CARD_BG, "color": TEXT_LIGHT})
    )
    st.dataframe(styled, use_container_width=True)

    st.markdown("---")

    # ── Compliance Bar Chart ───────────────────────────────────────────
    st.markdown('<div class="section-header"><b>📊 Compliance Score by Requirement & Bank</b></div>',
                unsafe_allow_html=True)

    fig_bar = px.bar(
        reg_df, x="Requirement", y="Score", color="Bank",
        barmode="group",
        color_discrete_map={"DBS": DBS_COLOR, "Emirates NBD": ENBD_COLOR},
        title="Regulatory Compliance Scores (1–5 scale)",
        text="Score",
    )
    fig_bar.update_layout(
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT, xaxis_tickangle=-20,
        yaxis=dict(range=[0, 5.5], gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Status Summary ────────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>🗂️ Alignment Status Summary</b></div>',
                unsafe_allow_html=True)

    status_summary = (
        reg_df.groupby(["Bank", "Status"])
        .size()
        .reset_index(name="Count")
    )
    fig_pie = px.pie(
        status_summary, names="Status", values="Count",
        facet_col="Bank",
        color="Status",
        color_discrete_map={
            "Fully Aligned": ACCENT_GREEN,
            "Partially Aligned": ACCENT_AMBER,
            "Not Aligned": ACCENT_RED,
        },
        title="Alignment Status Distribution",
    )
    fig_pie.update_layout(paper_bgcolor=CARD_BG, font_color=TEXT_LIGHT)
    st.plotly_chart(fig_pie, use_container_width=True)

    # ── Gap Highlights ────────────────────────────────────────────────
    gaps = reg_df[reg_df["Status"] != "Fully Aligned"]
    if not gaps.empty:
        st.markdown('<div class="section-header"><b>⚠️ Identified Compliance Gaps</b></div>',
                    unsafe_allow_html=True)
        for _, row in gaps.iterrows():
            st.warning(
                f"**{row['Bank']}** — {row['Requirement']}: "
                f"*{row['Status']}* (Score {row['Score']}/5)  \n"
                f"Evidence: {row['Evidence']}"
            )


# ═════════════════════════════════════════════════════════════════════
# PAGE 4 – SCENARIO PLANNING
# ═════════════════════════════════════════════════════════════════════
elif page == "🔮 Scenario Planning":

    st.title("🔮 Scenario Planning & Stress Testing")
    st.markdown(
        "Explore how regulatory and market scenarios would affect "
        "each bank's ESG credit risk profile."
    )
    st.markdown("---")

    # ── Scenario Dropdown ─────────────────────────────────────────────
    scenarios = scen_df["Scenario"].unique().tolist()
    selected_scenario = st.selectbox("Select Scenario", options=scenarios)

    scen_filtered = scen_df[scen_df["Scenario"] == selected_scenario]

    # ── Current vs Scenario Score Chart ───────────────────────────────
    st.markdown('<div class="section-header"><b>📊 Current vs Projected ESG Score</b></div>',
                unsafe_allow_html=True)

    melted_scores = scen_filtered.melt(
        id_vars=["Bank"],
        value_vars=["CurrentScore", "ScenarioScore"],
        var_name="Type", value_name="Score",
    )
    melted_scores["Type"] = melted_scores["Type"].map(
        {"CurrentScore": "Current Score", "ScenarioScore": "Projected Score"}
    )

    fig_scenario = px.bar(
        melted_scores, x="Bank", y="Score", color="Type",
        barmode="group",
        color_discrete_map={
            "Current Score": "#4A90D9",
            "Projected Score": ACCENT_GREEN,
        },
        title=f"Scenario: {selected_scenario}",
        text="Score",
    )
    fig_scenario.update_layout(
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT,
        yaxis=dict(range=[0, 110], gridcolor="#2d3250", title="Score"),
        xaxis=dict(gridcolor="#2d3250"),
    )
    fig_scenario.update_traces(textposition="outside")
    st.plotly_chart(fig_scenario, use_container_width=True)

    # ── Impact Gauge ──────────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>⚡ Impact Magnitude by Bank</b></div>',
                unsafe_allow_html=True)

    cols = st.columns(len(scen_filtered))
    for i, (_, row) in enumerate(scen_filtered.iterrows()):
        with cols[i]:
            impact_color = (ACCENT_GREEN if row["Impact"] <= 4
                            else ACCENT_AMBER if row["Impact"] <= 7
                            else ACCENT_RED)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row["Impact"],
                title={"text": f"{row['Bank']}<br><sub>Impact Score</sub>",
                       "font": {"color": TEXT_LIGHT}},
                gauge={
                    "axis": {"range": [0, 15], "tickcolor": TEXT_LIGHT},
                    "bar": {"color": impact_color},
                    "bgcolor": CARD_BG,
                    "steps": [
                        {"range": [0, 4],  "color": "#1e4d2b"},
                        {"range": [4, 8],  "color": "#4d3b00"},
                        {"range": [8, 15], "color": "#4d1a1a"},
                    ],
                    "threshold": {
                        "line": {"color": "white", "width": 2},
                        "thickness": 0.75,
                        "value": row["Impact"],
                    },
                },
                number={"font": {"color": impact_color, "size": 36}},
            ))
            fig_gauge.update_layout(
                paper_bgcolor=CARD_BG, font_color=TEXT_LIGHT,
                height=280,
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

    # ── Scenario Comparison Table ─────────────────────────────────────
    st.markdown('<div class="section-header"><b>📋 Scenario Data</b></div>',
                unsafe_allow_html=True)

    def color_impact(val):
        if isinstance(val, (int, float)):
            if val <= 4:
                return f"color: {ACCENT_GREEN};"
            elif val <= 7:
                return f"color: {ACCENT_AMBER};"
            else:
                return f"color: {ACCENT_RED};"
        return ""

    styled_scen = (
        scen_filtered.style
        .applymap(color_impact, subset=["Impact"])
        .set_properties(**{"background-color": CARD_BG, "color": TEXT_LIGHT})
    )
    st.dataframe(styled_scen, use_container_width=True)

    # ── All-Scenario Impact Chart ─────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header"><b>🔄 All Scenarios — Impact Overview</b></div>',
                unsafe_allow_html=True)

    fig_all = px.bar(
        scen_df, x="Scenario", y="Impact", color="Bank",
        barmode="group",
        color_discrete_map={"DBS": DBS_COLOR, "Emirates NBD": ENBD_COLOR},
        title="Impact Score Across All Scenarios",
        text="Impact",
    )
    fig_all.update_layout(
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
        font_color=TEXT_LIGHT, xaxis_tickangle=-15,
        yaxis=dict(gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
    )
    fig_all.update_traces(textposition="outside")
    st.plotly_chart(fig_all, use_container_width=True)

    # ── Recommendations ───────────────────────────────────────────────
    st.markdown('<div class="section-header"><b>💡 Strategic Recommendations</b></div>',
                unsafe_allow_html=True)

    rec_map = {
        "Stricter Climate Regulation": {
            "DBS": (
                "DBS is well-positioned with existing TCFD disclosures and MAS ERM "
                "integration. Recommend deepening Scope 3 financed-emissions tracking "
                "and stress-testing the Responsible Financing Framework against net-zero pathways."
            ),
            "Emirates NBD": (
                "Emirates NBD should accelerate climate risk governance and scenario "
                "analysis capabilities. Priority actions: align with TCFD fully, "
                "establish internal carbon pricing, and integrate UAE Climate Pledges "
                "into lending policy."
            ),
        },
        "Mandatory ISSB Reporting": {
            "DBS": (
                "DBS has mature disclosure infrastructure. Recommend aligning existing "
                "TCFD and SGX sustainability reporting to IFRS S1/S2 standards and "
                "assuring ESG data through an independent third party."
            ),
            "Emirates NBD": (
                "Emirates NBD faces a higher adjustment burden. Immediate priorities: "
                "establish an ISSB readiness task force, map current disclosures to "
                "IFRS S1/S2 gaps, and pilot assured reporting on climate metrics."
            ),
        },
        "Enhanced ESG Governance": {
            "DBS": (
                "Governance is already at 5/5. Focus on cascading ESG accountability "
                "to business unit heads, embedding ESG KPIs in executive remuneration, "
                "and expanding the sustainability committee scope."
            ),
            "Emirates NBD": (
                "Strengthen Board-level ESG expertise through targeted training and "
                "recruiting independent directors with climate finance backgrounds. "
                "Link senior management compensation to ESG targets."
            ),
        },
        "Carbon Intensive Portfolio Exposure": {
            "DBS": (
                "Leverage the Responsible Financing Framework to reduce exposure in "
                "carbon-intensive sectors. Establish sector-specific financed-emissions "
                "targets with annual milestones aligned to 1.5 °C scenarios."
            ),
            "Emirates NBD": (
                "Given the UAE's hydrocarbon-linked economy, develop a transition finance "
                "strategy. Engage key corporate clients on credible decarbonisation plans "
                "and create green financing incentives to redirect capital flows."
            ),
        },
    }

    default_rec = {
        "DBS": "Continue advancing ESG integration and sharing best practices regionally.",
        "Emirates NBD": "Prioritise closing identified gaps to reach parity with leading peers.",
    }

    recs = rec_map.get(selected_scenario, default_rec)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{DBS_COLOR};">
          <p>🏦 DBS Bank</p>
          <p style="color:{TEXT_LIGHT}; font-size:0.95rem;">{recs.get('DBS', default_rec['DBS'])}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{ENBD_COLOR};">
          <p>🏦 Emirates NBD</p>
          <p style="color:{TEXT_LIGHT}; font-size:0.95rem;">{recs.get('Emirates NBD', default_rec['Emirates NBD'])}</p>
        </div>""", unsafe_allow_html=True)
