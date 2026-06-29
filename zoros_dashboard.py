"""
ZOROS UNIWAY — Streamlit Analytics Dashboard
Run: streamlit run zoros_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ZOROS UNIWAY Dashboard",
    page_icon="⚡",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark background */
  .stApp { background-color: #0d0f14; }

  /* KPI metric cards */
  [data-testid="metric-container"] {
    background: #1c2030;
    border: 1px solid #252a3a;
    border-radius: 14px;
    padding: 16px 20px;
  }
  [data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }
  [data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
  }

  /* Section headers */
  h1, h2, h3 { color: #f1f5f9 !important; }

  /* Sidebar */
  [data-testid="stSidebar"] { background-color: #151820 !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

  /* Divider */
  hr { border-color: #252a3a; }
</style>
""", unsafe_allow_html=True)

# ── Embedded Data (paste your CSV content here, or load from file) ──
CSV_DATA = """date,description,category,Work amount,Amount usage,Earn,notes
1/4/2026,Ac Ftting,service,4000,0,900,contact:6385899844
1/4/2026,petrol,expense,0,50,0,For Work
1/4/2026,Note,expense,0,100,0,Accountes
1/4/2026,Clambu,expense,0,50,0,For service
1/4/2026,Fan Fitting,service,250,0,50,contact:9444256839
2/4/2026,Motor repair,service,600,0,200,contact:9042129527
20/4/2026,Document,expense,0,50,0,For Office
22/4/2026,Ac Service,service,1250,0,250,contact:9150944428
28/4/2026,Motor repair,service,600,0,200,contact:9003176548
30/4/2026,petrol,expense,0,200,0,Ramanathapuram
21/5/2026,Electrical work,service,1300,0,200,contact:9444256839
24/6/2026,Electrical work,service,2300,0,200,contact:8883404630
24/6/2026,Door Glass,service,4500,0,500,contact:8883404630
25/6/2026,Recharge,expense,0,200,0,recharge
"""

# ── Load Data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(CSV_DATA))
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["month"] = df["date"].dt.strftime("%b %Y")
    df["day_label"] = df["date"].dt.strftime("%d %b")
    return df

df = load_data()

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background:#f97316;border-radius:10px;padding:12px 16px;text-align:center;margin-bottom:4px;">
        <span style="color:white;font-size:18px;font-weight:700;letter-spacing:1px;">⚡ ZOROS UNIWAY</span><br>
        <span style="color:rgba(255,255,255,0.75);font-size:11px;">Service Dashboard</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    categories = ["All"] + df["category"].unique().tolist()
    selected_cat = st.selectbox("Category", categories)

    months = ["All"] + df["month"].unique().tolist()
    selected_month = st.selectbox("Month", months)

    st.markdown("---")
    st.markdown("### 📁 Upload Your CSV")
    uploaded = st.file_uploader("Replace with your own data", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        df["date"] = pd.to_datetime(df["date"], dayfirst=True)
        df["month"] = df["date"].dt.strftime("%b %Y")
        df["day_label"] = df["date"].dt.strftime("%d %b")
        st.success("Data loaded!")

    st.markdown("---")
    st.caption("ZOROS UNIWAY · MSME Incubation Center · Kilakarai")

# ── Apply Filters ───────────────────────────────────────────────────
filtered = df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["category"] == selected_cat]
if selected_month != "All":
    filtered = filtered[filtered["month"] == selected_month]

# ── Header ──────────────────────────────────────────────────────────
st.markdown("## ⚡ ZOROS UNIWAY — Operations Dashboard")
st.markdown(f"**Period:** {df['date'].min().strftime('%d %b %Y')} → {df['date'].max().strftime('%d %b %Y')}  |  Showing **{len(filtered)}** of {len(df)} records")
st.markdown("---")

# ── KPI Cards ───────────────────────────────────────────────────────
services = filtered[filtered["category"] == "service"]
expenses = filtered[filtered["category"] == "expense"]

total_earn     = services["Earn"].sum()
total_expense  = expenses["Amount usage"].sum()
net_profit     = total_earn - total_expense
total_work_val = filtered["Work amount"].sum()
margin         = (net_profit / total_earn * 100) if total_earn > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Earned",    f"₹{total_earn:,}",     f"{len(services)} service entries")
k2.metric("💸 Total Expenses",  f"₹{total_expense:,}",  f"{len(expenses)} expense entries")
k3.metric("📈 Net Profit",      f"₹{net_profit:,}",     f"{margin:.1f}% margin")
k4.metric("🔧 Total Work Value",f"₹{total_work_val:,}", "Across all services")

st.markdown("---")

# ── Chart Colors ────────────────────────────────────────────────────
PALETTE = ["#f97316","#6366f1","#22d3ee","#a3e635","#10b981","#ec4899","#f59e0b"]
DARK_BG  = "#151820"
CARD_BG  = "#1c2030"
GRID     = "#252a3a"
TEXT     = "#f1f5f9"
MUTED    = "#64748b"

def dark_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(color=TEXT, size=15), x=0),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=MUTED, size=12),
        margin=dict(l=16, r=16, t=40, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
    )
    fig.update_xaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED))
    return fig

# ── Row 1: Line + Bar ───────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("#### 📈 Daily Earnings Trend")
    daily = filtered.groupby("day_label")["Earn"].sum().reset_index()
    daily = daily[daily["Earn"] > 0]
    fig_line = px.line(
        daily, x="day_label", y="Earn",
        markers=True,
        color_discrete_sequence=["#10b981"],
    )
    fig_line.update_traces(
        line=dict(width=2.5),
        marker=dict(size=8, color="#10b981", line=dict(color=CARD_BG, width=2)),
        fill="tozeroy",
        fillcolor="rgba(16,185,129,0.08)"
    )
    fig_line.update_layout(xaxis_title="Date", yaxis_title="Earn (₹)")
    dark_layout(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.markdown("#### 🥧 Service vs Expense Split")
    cat_counts = filtered["category"].value_counts().reset_index()
    cat_counts.columns = ["category", "count"]
    fig_pie = px.pie(
        cat_counts, names="category", values="count",
        color_discrete_sequence=["#10b981", "#ef4444"],
        hole=0.62,
    )
    fig_pie.update_traces(
        textfont=dict(color=TEXT),
        marker=dict(line=dict(color=CARD_BG, width=3))
    )
    dark_layout(fig_pie)
    fig_pie.update_layout(legend=dict(
        orientation="h", y=-0.1, x=0.5, xanchor="center",
        font=dict(color=MUTED)
    ))
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Bar by Service + Expense Breakdown ───────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔧 Earn by Service Type")
    svc_earn = (
        services.groupby("description")["Earn"]
        .sum()
        .reset_index()
        .sort_values("Earn", ascending=False)
    )
    fig_bar = px.bar(
        svc_earn, x="description", y="Earn",
        color="description",
        color_discrete_sequence=PALETTE,
        text="Earn",
    )
    fig_bar.update_traces(
        texttemplate="₹%{text}",
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
        marker_line_width=0,
    )
    fig_bar.update_layout(
        xaxis_title="Service", yaxis_title="Earn (₹)",
        showlegend=False,
        bargap=0.3,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    dark_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.markdown("#### 💸 Expense Breakdown")
    exp_data = expenses[expenses["Amount usage"] > 0].copy()
    exp_data["label"] = exp_data["description"] + " (" + exp_data["day_label"] + ")"
    fig_hbar = px.bar(
        exp_data, x="Amount usage", y="label",
        orientation="h",
        color="description",
        color_discrete_sequence=["#ef4444","#f59e0b","#f97316","#22d3ee"],
        text="Amount usage",
    )
    fig_hbar.update_traces(
        texttemplate="₹%{text}",
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
        marker_line_width=0,
    )
    fig_hbar.update_layout(
        xaxis_title="Amount (₹)", yaxis_title="",
        showlegend=False,
    )
    dark_layout(fig_hbar)
    st.plotly_chart(fig_hbar, use_container_width=True)

# ── Row 3: Monthly Summary Bar ──────────────────────────────────────
st.markdown("#### 📅 Monthly Earn vs Expense")
monthly = df.groupby("month").agg(
    Earn=("Earn", "sum"),
    Expense=("Amount usage", "sum")
).reset_index()

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Bar(
    name="Earn", x=monthly["month"], y=monthly["Earn"],
    marker_color="#10b981", marker_line_width=0,
))
fig_monthly.add_trace(go.Bar(
    name="Expense", x=monthly["month"], y=monthly["Expense"],
    marker_color="#ef4444", marker_line_width=0,
))
fig_monthly.update_layout(
    barmode="group", bargap=0.25,
    xaxis_title="Month", yaxis_title="Amount (₹)",
    legend=dict(orientation="h", y=1.1, font=dict(color=MUTED)),
)
dark_layout(fig_monthly)
st.plotly_chart(fig_monthly, use_container_width=True)

# ── Raw Data Table ──────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 🗂 Transaction Records")
display_cols = ["date", "description", "category", "Work amount", "Amount usage", "Earn", "notes"]
st.dataframe(
    filtered[display_cols].sort_values("date"),
    use_container_width=True,
    hide_index=True,
)

# ── Download button ─────────────────────────────────────────────────
csv_out = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data as CSV",
    data=csv_out,
    file_name="zoros_filtered.csv",
    mime="text/csv",
)
