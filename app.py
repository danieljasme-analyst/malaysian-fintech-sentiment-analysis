import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# Page config + styling
# ============================================================
st.set_page_config(
    page_title="Malaysian Fintech Sentiment Dashboard",
    page_icon="🇲🇾",
    layout="wide"
)

# ============================================================
# Load data
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/dashboard_data.csv")
    return df

@st.cache_data
def load_aspect_pivot():
    return pd.read_csv("data/aspect_sentiment_pivot.csv", index_col=0)

df = load_data()
aspect_pivot = load_aspect_pivot()

# ============================================================
# Sidebar navigation
# ============================================================
st.sidebar.title("🇲🇾 Fintech Sentiment Analysis")
st.sidebar.markdown("**UiTM ISP610** | Daniel")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "📱 App Deep-Dive", "🔥 Aspect Heatmap", "💬 Sample Reviews"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total reviews**: {len(df):,}")
st.sidebar.markdown(f"**Apps analyzed**: {df['app_name'].nunique()}")
st.sidebar.markdown(f"**Languages**: English, Malay, Manglish")

# ============================================================
# Page 1: Overview
# ============================================================
if page == "📊 Overview":
    st.title("Malaysian E-Wallet & Digital Banking Sentiment Analysis")
    st.markdown("*Multilingual sentiment analysis of 248,858 Google Play reviews*")
    
    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", f"{len(df):,}")
    col2.metric("Apps Analyzed", df["app_name"].nunique())
    col3.metric("Net-Negative Apps", "4 of 5")
    col4.metric("Transformer Accuracy (1-star)", "92.8%")
    
    st.markdown("---")
    
    # Average sentiment per app
    st.subheader("Average Sentiment Score per App")
    avg = (df.groupby("app_name")["transformer_score"]
             .mean().sort_values().reset_index())
    avg.columns = ["App", "Avg Sentiment"]
    
    fig = px.bar(
        avg, x="Avg Sentiment", y="App", orientation="h",
        color="Avg Sentiment", color_continuous_scale="RdYlGn",
        range_color=[-1, 1]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment distribution
    st.subheader("Sentiment Label Breakdown")
    label_dist = (df.groupby(["app_name", "transformer_label"])
                    .size().unstack(fill_value=0))
    label_pct = label_dist.div(label_dist.sum(axis=1), axis=0) * 100
    label_pct = label_pct[["negative", "neutral", "positive"]]
    
    fig2 = go.Figure()
    for label, color in zip(
        ["negative", "neutral", "positive"],
        ["#d62728", "#bbbbbb", "#2ca02c"]
    ):
        fig2.add_trace(go.Bar(
            y=label_pct.index, x=label_pct[label],
            name=label, orientation="h",
            marker_color=color
        ))
    fig2.update_layout(barmode="stack", height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key findings
    st.markdown("---")
    st.subheader("🎯 Key Findings")
    st.markdown("""
    - **4 out of 5 apps** show net-negative sentiment when Malay reviews are included
    - **MAE by Maybank** is the worst app in 5 of 9 aspect categories
    - **Setel** is the only app with positive aspect sentiment, driven by Mesra Points integration
    - **Login/Authentication** is the worst aspect industry-wide — likely tied to BNM's 2FA requirements
    - The multilingual transformer caught **41 percentage points** more 1-star complaints than VADER
    """)

# ============================================================
# Page 2: App Deep-Dive
# ============================================================
elif page == "📱 App Deep-Dive":
    st.title("App Deep-Dive")
    
    selected_app = st.selectbox(
        "Choose an app",
        sorted(df["app_name"].unique())
    )
    
    app_df = df[df["app_name"] == selected_app]
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews", f"{len(app_df):,}")
    col2.metric("Avg Star Rating", f"{app_df['score'].mean():.2f}")
    col3.metric("Avg Sentiment", f"{app_df['transformer_score'].mean():+.3f}")
    
    # Sentiment over time
    st.subheader("Sentiment Trend Over Time")
    app_df_dated = app_df.dropna(subset=["at"]).copy()
    app_df_dated["at"] = pd.to_datetime(app_df_dated["at"], errors="coerce")
    app_df_dated["year_month"] = app_df_dated["at"].dt.to_period("M").astype(str)
    
    trend = (app_df_dated.groupby("year_month")["transformer_score"]
                          .mean().reset_index())
    
    fig = px.line(trend, x="year_month", y="transformer_score", markers=True)
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Star rating distribution
    st.subheader("Star Rating Distribution")
    rating_dist = app_df["score"].value_counts().sort_index()
    fig2 = px.bar(
        x=rating_dist.index, y=rating_dist.values,
        labels={"x": "Star Rating", "y": "Number of Reviews"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# Page 3: Aspect Heatmap
# ============================================================
elif page == "🔥 Aspect Heatmap":
    st.title("Aspect-Based Sentiment Heatmap")
    st.markdown("""
    *Red cells indicate where each app fails worst. Green cells mark relative strengths.*
    
    ⚠️ **Note**: aspect-tagged reviews skew negative because users typically mention features only when complaining. Interpret **relative differences** between apps, not absolute scores.
    """)
    
    fig = px.imshow(
        aspect_pivot, text_auto=".2f",
        color_continuous_scale="RdYlGn",
        zmin=-1, zmax=1, aspect="auto"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Best/worst per aspect
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Best App per Aspect")
        for aspect in aspect_pivot.columns:
            best_app = aspect_pivot[aspect].idxmax()
            best_score = aspect_pivot[aspect].max()
            st.markdown(f"- **{aspect}**: {best_app} ({best_score:+.2f})")
    
    with col2:
        st.subheader("⚠️ Worst App per Aspect")
        for aspect in aspect_pivot.columns:
            worst_app = aspect_pivot[aspect].idxmin()
            worst_score = aspect_pivot[aspect].min()
            st.markdown(f"- **{aspect}**: {worst_app} ({worst_score:+.2f})")

# ============================================================
# Page 4: Sample Reviews
# ============================================================
elif page == "💬 Sample Reviews":
    st.title("Sample Reviews Explorer")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_app = st.selectbox("App", sorted(df["app_name"].unique()))
    with col2:
        selected_sentiment = st.selectbox(
            "Sentiment", ["negative", "neutral", "positive"]
        )
    with col3:
        selected_lang = st.selectbox(
            "Language", ["all", "english", "malay", "other"]
        )
    
    filtered = df[
        (df["app_name"] == selected_app)
        & (df["transformer_label"] == selected_sentiment)
    ]
    if selected_lang != "all":
        filtered = filtered[filtered["lang_group"] == selected_lang]
    
    st.markdown(f"**{len(filtered):,} reviews match your filters**")
    
    # Sort by extremity
    if selected_sentiment == "negative":
        filtered = filtered.sort_values("transformer_score", ascending=True)
    elif selected_sentiment == "positive":
        filtered = filtered.sort_values("transformer_score", ascending=False)
    
    for _, row in filtered.head(15).iterrows():
        with st.container():
            st.markdown(f"⭐ **{row['score']}** | "
                        f"`{row['transformer_label']}` "
                        f"(score: {row['transformer_score']:+.2f}) | "
                        f"{row['lang_group']}")
            st.markdown(f"> {row['content']}")
            st.markdown("---")