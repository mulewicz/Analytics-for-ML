import plotly.express as px
import streamlit as st
import pandas as pd

@st.cache_data
def table1(df):
    total_users = df["uuid"].nunique()
    avg_requests = df["requests_cnt"].mean()
    total_spent = df["spent_amount"].sum()
    avg_spent = df["spent_amount"].mean()
    enterprise_pct = (df["license"].eq("Enterprise").mean()) * 100
    avg_days_active = df.groupby("uuid")["day_id"].nunique().mean()
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Total Users", f"{total_users:,}")
    col2.metric("Avg Requests", f"{avg_requests:.1f}")
    col3.metric("Total Spent", f"{total_spent:,.2f}")
    col4.metric("Avg Spent ", f"{avg_spent:.2f}")
    col5.metric("Enterprise %", f"{enterprise_pct:.1f}%")
    col6.metric("Days Active", f"{avg_days_active:,}")

    pivot = df.pivot_table(
        index="feature",
        columns="model",
        values="requests_cnt",
        aggfunc="mean").round(1)

    st.dataframe(pivot.style.background_gradient(cmap="BuPu"), use_container_width=True)

@st.cache_data
def plot1(df):
    fig = px.box(
        df,
        x="model",
        y="requests_cnt",
        color="license",
        title="Requests count per model and license",
        color_discrete_sequence=px.colors.sequential.BuPu
)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Requests count"
    )
    fig.update_yaxes(range=[0, 170])

    st.plotly_chart(fig)
@st.cache_data
def plot2(df):
    fig = px.box(
        df,
        x="model",
        y="spent_amount",
        color="license",
        title="Amount of units spent per model and license",
        color_discrete_map={
            "Premium": "#edf8fb", "Basic": "#b3cde3", "Enterprise": "#8856a7", "Standard": "#810f7c"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Amount of units"
    )
    fig.update_yaxes(range=[0, 30])
    st.plotly_chart(fig)
@st.cache_data
def plot3(df):
    pivot = df.pivot_table(
        index="feature",
        columns="model",
        values="spent_amount",
        aggfunc="mean"
    )

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="BuPu",
        aspect="auto",
        title="Average spent amount per feature and model"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Feature"
    )
    st.plotly_chart(fig)
@st.cache_data
def plot4(df):
    stats = (
        df.groupby("model")
        .agg(
            requests_mean=("requests_cnt", "mean"),
            spend_mean=("spent_amount", "mean"),
            requests_std=("requests_cnt", "std"),
            spend_std=("spent_amount", "std"),
        )
        .reset_index()
    )

    melted = stats.melt(id_vars="model", var_name="stat", value_name="value")

    fig = px.bar(
        melted,
        x="stat",
        y="value",
        color="model",
        title="Summary Statistics per Model",
        color_discrete_sequence=px.colors.sequential.BuPu
    )
    st.plotly_chart(fig)
@st.cache_data
def plot5(df):
    corr = df[["requests_cnt", "spent_amount"]].corr().iloc[0, 1]

    fig = px.scatter(
        df,
        x="requests_cnt",
        y="spent_amount",
        title=f"Activity vs Spending (corr = {corr:.2f})",
        trendline="ols",
        opacity=0.8,
        color_continuous_scale="BuPu"
    )
    fig.update_xaxes(range=[0, 6000])
    fig.update_yaxes(range=[0, 2000])

    fig.update_traces(
        marker=dict(color="#b3cde3", size=6, line=dict(width=1, color="white")),
        selector=dict(mode="markers")
    )
    st.plotly_chart(fig)


@st.cache_data
def plot6(df):
    fig = px.scatter(
        df,
        x="requests_cnt",
        y="spent_amount",
        color="license",
        title="Requests count per model and license",
        trendline="ols",
        opacity=0.8,
        color_discrete_map={
            "Premium": "#edf8fb",
            "Basic": "#b3cde3",
            "Enterprise": "#8856a7",
            "Standard": "#810f7c"
        }
    )
    st.plotly_chart(fig)


@st.cache_data
def plot7(df):
    corr_over_time = (
        df.groupby("day_id")[["requests_cnt", "spent_amount"]]
        .corr().iloc[0::2, -1].reset_index()
        .rename(columns={"spent_amount": "corr"})
    )

    fig = px.line(
        corr_over_time,
        x="day_id",
        y="corr",
        title="Daily correlation between activity and spending",
        template="plotly_dark",
        markers=True
    )

    fig.update_traces(
        line=dict(color="#8856a7", width=2),
        marker=dict(color="#b3cde3", size=6)
    )

    st.plotly_chart(fig)


@st.cache_data
def plot8(df):
    pivot = df.pivot_table(
        index="feature",
        columns="model",
        values="requests_cnt",
        aggfunc="mean"
    )

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="BuPu",
        aspect="auto",
        title="Average spent amount per feature and model"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Model",
        yaxis_title="Feature"
    )
    st.plotly_chart(fig)


@st.cache_data
def plot9(df):
    df["day_id"] = pd.to_datetime(df["day_id"])
    daily = df.groupby("day_id")[["requests_cnt", "spent_amount"]].sum().reset_index()
    fig = px.line(
        daily,
        x="day_id",
        y="spent_amount",
        title="Daily Trends in Spending",
        template="plotly_dark",
        markers=True
    )

    fig.update_traces(
        line=dict(color="#8856a7", width=2),
        marker=dict(color="#b3cde3", size=6)
    )
    st.plotly_chart(fig)


def plot10(df):
    df["day_id"] = pd.to_datetime(df["day_id"])
    df["week"] = df["day_id"].dt.to_period("W").apply(lambda r: r.start_time)
    weekly = df.groupby("week")[["requests_cnt", "spent_amount"]].sum().reset_index()
    fig = px.line(
        weekly,
        x="week",
        y=["requests_cnt", "spent_amount"],
        title="Weekly Trends in Requests and Spending",
        template="plotly_dark",
        markers=True
    )
    fig.update_traces(
        line=dict(color="#8856a7", width=2),
        marker=dict(color="#b3cde3", size=6)
    )
    st.plotly_chart(fig)


@st.cache_data
def plot11(df):
    df["day_id"] = pd.to_datetime(df["day_id"])
    df["month"] = df["day_id"].dt.month
    monthly_by_license = (
        df.groupby(["month", "license"])[["requests_cnt", "spent_amount"]]
        .sum()
        .reset_index()
    )
    fig = px.line(
        monthly_by_license,
        x="month",
        y="requests_cnt",
        color="license",
        title="Monthly Trends in Requests and Spending",
        template="plotly_dark",
        markers=True,
        color_discrete_map={
            "Premium": "#edf8fb",
            "Basic": "#b3cde3",
            "Enterprise": "#8856a7",
            "Standard": "#810f7c"
        }
    )
    st.plotly_chart(fig)

@st.cache_data
@st.cache_data
def plot12(df):
    funnel = pd.DataFrame({
        "stage": [
            "Used app",
            "Used multiple features",
            "Spent > 100 credits"
        ],
        "users": [
            df["uuid"].nunique(),
            df.groupby("uuid")["feature"].nunique().gt(1).sum(),
            df.groupby("uuid")["spent_amount"].sum().gt(100).sum()
        ]
    })

    fig = px.funnel(
        funnel,
        x="users",
        y="stage",
        title="User Engagement Funnel",
        template="plotly_dark",
        color_discrete_sequence=["#8856a7"]
    )
    st.plotly_chart(fig)


@st.cache_data
def plot13(df):
    user_days = df.groupby(["uuid", "license"])["day_id"].nunique().reset_index(name="days_active")

    fig = px.histogram(
        user_days,
        x="days_active",
        color="license",
        title="User Retention (days active) by License Type",
        barmode="stack",
        color_discrete_map={
            "Premium": "#edf8fb", "Basic": "#b3cde3", "Enterprise": "#8856a7", "Standard": "#810f7c"
        },
        template="plotly_dark"
    )

    fig.update_layout(
        bargap=0.2,
        xaxis_title="Days Active",
        yaxis_title="Number of Users",
        legend_title="License Type"
    )
    st.plotly_chart(fig)


@st.cache_data
def plot14(df):
    df["spend_per_req"] = df["spent_amount"] / df["requests_cnt"]
    avg = df.groupby("license")["spend_per_req"].mean().reset_index()

    fig = px.bar(
        avg,
        x="license",
        y="spend_per_req",
        title="Average Spend per Request by License",
        template="plotly_dark",
        color_discrete_sequence=["#8856a7"]
    )
    st.plotly_chart(fig)


@st.cache_data
def plot15(df):
    df["spend_per_req"] = df["spent_amount"] / df["requests_cnt"]
    avg = df.groupby("model")["spend_per_req"].mean().reset_index()

    fig = px.bar(
        avg,
        x="model",
        y="spend_per_req",
        color_discrete_sequence=["#b3cde3"],
        title="Average Spend per Request by Model",
        template="plotly_dark"
    )
    st.plotly_chart(fig)


@st.cache_data
def plot16(df):
    user_sum = (
        df.groupby(["uuid", "license"])[["requests_cnt", "spent_amount"]]
        .sum()
        .reset_index()
    )

    user_sum["is_power"] = user_sum.groupby("license")["spent_amount"] \
        .transform(lambda x: x > x.quantile(0.9))
    top_users = (
        user_sum.sort_values(["license", "spent_amount"], ascending=[True, False])
        .groupby("license")
        .head(5)
    )

    fig = px.bar(
        top_users,
        x="uuid",
        y="spent_amount",
        color="license",
        title="Top 5 Power Users per License",
        template="plotly_dark",
        color_discrete_map={
            "Premium": "#edf8fb", "Basic": "#b3cde3", "Enterprise": "#8856a7", "Standard": "#810f7c"
        }
    )
    fig.update_layout(xaxis={"categoryorder": "total descending"})
    st.plotly_chart(fig)

@st.cache_data
def plot17(df):
    df.groupby("feature")

    fig = px.histogram(
        df,
        x="feature",
        color_discrete_sequence=["#b3cde3"],
        title="Histogram of Features"
    )
    return fig


def plot18(df):
    df.groupby("license")

    fig = px.histogram(
        df,
        x="license",
        color_discrete_sequence=["#810f7c"],
        title="Histogram of Licenses"
    )
    return fig
    
@st.cache_data
def plot19(df):
    d = df.copy()
    d["day_id"] = pd.to_datetime(d["day_id"])
    days_active = (
        d.groupby(["uuid", "license"])["day_id"]
        .nunique()
        .reset_index(name="days_active")
    )
    avg_ret = (
        days_active.groupby("license")["days_active"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        avg_ret,
        x="license",
        y="days_active",
        title="Average Retention (Days Active) by License",
        template="plotly_dark",
        color="license",
        color_discrete_map={
            "Premium": "#edf8fb",
            "Basic": "#b3cde3",
            "Enterprise": "#8856a7",
            "Standard": "#810f7c"
        },
        text="days_active"
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(
        yaxis_title="Average days active",
        xaxis_title="License",
        uniformtext_minsize=10,
        uniformtext_mode="show"
    )
    st.plotly_chart(fig)

@st.cache_data
def plot20(df):
    user = df.groupby(["uuid", "day_id"])[["requests_cnt", "spent_amount"]].sum().reset_index()
    summary = user.groupby("uuid")[["requests_cnt", "spent_amount"]].sum().reset_index()

    req_thr = summary["requests_cnt"].median()
    spend_thr = summary["spent_amount"].median()

    def seg(row):
        if row.requests_cnt <= req_thr and row.spent_amount <= spend_thr:
            return "Low activity, low spend"
        if row.requests_cnt > req_thr and row.spent_amount <= spend_thr:
            return "High activity, low spend (free users)"
        if row.requests_cnt <= req_thr and row.spent_amount > spend_thr:
            return "High spend, low activity (power buyers)"
        return "High both (core users)"

    summary["segment"] = summary.apply(seg, axis=1)

    merged = df.merge(summary[["uuid", "segment"]], on="uuid", how="left")
    merged["day_id"] = pd.to_datetime(merged["day_id"])

    segment_daily = merged.groupby(["day_id", "segment"])["uuid"].nunique().reset_index(name="users")

    fig = px.area(
        segment_daily,
        x="day_id",
        y="users",
        color="segment",
        title="User Behaviour Segments Over Time",
        template="plotly_dark",
        color_discrete_map={
            "Low activity, low spend": "#b3cde3",
            "High activity, low spend (free users)": "#6497b1",
            "High spend, low activity (power buyers)": "#8856a7",
            "High both (core users)": "#810f7c"
        }
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Users",
        legend_title="User Segment",
        hovermode="x unified",
        hoverlabel=dict(bgcolor="black", font_size=12)
    )

    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def summary_kpis(df):
    df["day_id"] = pd.to_datetime(df["day_id"])

    total_users = df["uuid"].nunique()
    total_requests = df["requests_cnt"].sum()
    total_spent = df["spent_amount"].sum()
    avg_spent = df["spent_amount"].mean()
    avg_requests = df["requests_cnt"].mean()
    enterprise_pct = df["license"].eq("Enterprise").mean() * 100

    df["spend_per_req"] = df["spent_amount"] / df["requests_cnt"]
    avg_spend_per_req = df["spend_per_req"].mean()
    best_model = df.groupby("model")["spend_per_req"].mean().idxmin()
    worst_model = df.groupby("model")["spend_per_req"].mean().idxmax()

    user_days = df.groupby(["uuid"])["day_id"].nunique()
    avg_days_active = user_days.mean()
    retained_7d = (user_days > 7).mean() * 100
    retained_30d = (user_days > 30).mean() * 100

    users_multiple_features = df.groupby("uuid")["feature"].nunique().gt(1).sum()
    users_spent_over_100 = df.groupby("uuid")["spent_amount"].sum().gt(100).sum()
    conversion_multifeature = users_multiple_features / total_users * 100
    conversion_spender = users_spent_over_100 / total_users * 100

    corr_req_spent = df[["requests_cnt", "spent_amount"]].corr().iloc[0, 1]
    daily = df.groupby("day_id")[["requests_cnt", "spent_amount"]].sum().reset_index()
    avg_daily_spend = daily["spent_amount"].mean()
    peak_day = daily.loc[daily["spent_amount"].idxmax(), "day_id"].strftime("%b %d")
    peak_spend = daily["spent_amount"].max()

    user_sum = df.groupby("uuid")["spent_amount"].sum()
    top_10pct_contrib = user_sum[user_sum > user_sum.quantile(0.9)].sum() / user_sum.sum() * 100

    st.markdown("### Overall Summary KPIs")
    with st.expander("High-level usage: "):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Users", f"{total_users:,}")
        c2.metric("Total Requests", f"{total_requests:,}")
        c3.metric("Total Spent", f"{total_spent:,.0f}")
        c4.metric("Avg Requests/User", f"{avg_requests:.1f}")
        c5.metric("Avg Spend/User", f"{avg_spent:.1f}")

    with st.expander("`Efficiency: `"):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Avg Spend per Request", f"{avg_spend_per_req:.3f}")
        c2.metric("Best Model (Cost-Efficient)", best_model)
        c3.metric("Most Expensive Model", worst_model)
        c4.metric("Enterprise % of Users", f"{enterprise_pct:.1f}%")
        c5.metric("Corr(Requests–Spend)", f"{corr_req_spent:.2f}")

    with st.expander("`Engagement: `"):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Avg Active Days/User", f"{avg_days_active:.1f}")
        c2.metric("Retention >7 days", f"{retained_7d:.1f}%")
        c3.metric("Retention >30 days", f"{retained_30d:.1f}%")
        c4.metric("Users Using >1 Feature", f"{conversion_multifeature:.1f}%")
        c5.metric("Users Spent >100", f"{conversion_spender:.1f}%")

    with st.expander("Power Usage: "):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Avg Daily Spend", f"{avg_daily_spend:,.0f}")
        c2.metric("Peak Day", peak_day)
        c3.metric("Peak Spending", f"{peak_spend:,.0f}")
        c4.metric("Top 10% Spend Share", f"{top_10pct_contrib:.1f}%")
        c5.metric("Most Recent Date", df["day_id"].max().strftime("%b %d"))

    st.markdown("---")
    st.caption("KPIs summarizing usage, efficiency, retention, and spending behavior across all models and licenses.")

@st.cache_data
def summary(df):
    st.markdown("### Behavioural Segments Snapshot")
    user_summary = df.groupby("uuid")[["requests_cnt", "spent_amount"]].sum().reset_index()
    req_thr = user_summary["requests_cnt"].median()
    spend_thr = user_summary["spent_amount"].median()

    def classify(row):
        if row.requests_cnt <= req_thr and row.spent_amount <= spend_thr:
            return "Low activity, low spend"
        elif row.requests_cnt > req_thr and row.spent_amount <= spend_thr:
            return "High activity, low spend (free users)"
        elif row.requests_cnt <= req_thr and row.spent_amount > spend_thr:
            return "High spend, low activity (power buyers)"
        else:
            return "High both (core users)"

    user_summary["segment"] = user_summary.apply(classify, axis=1)
    segment_counts = user_summary["segment"].value_counts().reset_index()
    segment_counts.columns = ["segment", "users"]

    fig = px.pie(
        segment_counts,
        names="segment",
        values="users",
        title="User Composition by Behaviour Segment",
        color="segment",
        color_discrete_map={
            "Low activity, low spend": "#b3cde3",
            "High activity, low spend (free users)": "#6497b1",
            "High spend, low activity (power buyers)": "#8856a7",
            "High both (core users)": "#810f7c"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
         **Core users** are the smallest group but contribute most of the spend.  
         **Free users** dominate the population — opportunity to improve monetization.  
         **Power buyers** are steady but few — retention and loyalty should be maintained.  
         **Low users** represent inactive or trial accounts.
    """)

    st.divider()

    st.markdown("### Model and License Insights")
    model_stats = (
        df.groupby("model")[["requests_cnt", "spent_amount"]]
          .mean()
          .sort_values("spent_amount", ascending=False)
          .reset_index()
    )

    fig_model = px.bar(
        model_stats,
        x="model",
        y="spent_amount",
        title="Average Spend by Model",
        text_auto=".2f",
        template="plotly_dark",
        color="model",
        color_discrete_sequence=px.colors.sequential.BuPu
    )
    st.plotly_chart(fig_model, use_container_width=True)

    st.markdown("""
        * **Models C and D** dominate both spending and usage — they are the platform’s most utilized and valuable models.  
        * **Models A and B** remain underused, suggesting potential optimization or feature refinement.  
        * **Model E** shows balanced, consistent usage across features — likely a general-purpose model.
    """)

    st.divider()

    st.markdown("### Retention and Engagement")
    user_days = df.groupby(["uuid", "license"])["day_id"].nunique().reset_index(name="days_active")
    avg_retention = user_days.groupby("license")["days_active"].mean().reset_index()

    fig_ret = px.bar(
        avg_retention,
        x="license",
        y="days_active",
        title="Average Retention (Days Active) by License",
        template="plotly_dark",
        color="license",
        color_discrete_map={
            "Premium": "#edf8fb",
            "Basic": "#b3cde3",
            "Enterprise": "#8856a7",
            "Standard": "#810f7c"
        },
        text_auto=".1f"
    )
    st.plotly_chart(fig_ret, use_container_width=True)

    st.markdown("""
        * **Premium** and **Enterprise** users show the longest retention periods.  
        * **Basic** and **Standard** users dominate early activity but churn sooner.  
        * Retention follows a bimodal pattern — short-term trial users and long-term engaged members.
    """)

    st.divider()

    st.markdown("### Overall Growth & Correlations")
    corr = df[["requests_cnt", "spent_amount"]].corr().iloc[0, 1]
    st.metric("Activity-Spend Correlation", f"{corr:.2f}", help="How strongly usage relates to spending")

    st.markdown("""
        * Spending and activity show a **strong linear correlation (≈0.94)**, confirming a clear usage-based pricing model.  
        * Weekly cycles are visible — engagement peaks on weekdays and dips over weekends.  
        * Total engagement and spending show **steady month-over-month growth**, led by Premium and Enterprise users.
    """)

    st.divider()

    st.markdown("### Executive Summary")
    st.info("""
         **Models C & D** are the core drivers of engagement and revenue.  
         **Free users** dominate usage but not revenue — conversion potential is high.  
         **Premium/Enterprise** tiers deliver strong retention and sustained activity.  
         Spending scales linearly with activity — predictable, healthy business model.  
         Weekly usage patterns suggest optimizing operations around weekday peaks.  
         Low engagement models (A, B) may benefit from improved positioning or feature expansion.
    """)
