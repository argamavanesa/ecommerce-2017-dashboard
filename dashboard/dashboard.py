from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


# Page Config
st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide",
)

sns.set(style="darkgrid")

# Load Data
DATA_PATH = Path(__file__).with_name("all_data.csv")


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(DATA_PATH)


df_all = load_data()

if df_all.empty:
    st.error("File all_data.csv tidak ditemukan.")
    st.stop()


date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "review_creation_date",
    "review_answer_timestamp",
]

for col in date_columns:
    df_all[col] = pd.to_datetime(df_all[col], format="mixed", errors="coerce")


# Preparasi Data
df_all = df_all[df_all["order_purchase_timestamp"].dt.year == 2017].copy()
df_all = df_all.sort_values("order_purchase_timestamp")


#agregasi data penjualan dan revenue secara bulanan

df_monthly_sales = df_all.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "payment_value": "sum"
})

df_monthly_sales.index = df_monthly_sales.index.strftime('%Y-%m')
df_monthly_sales = df_monthly_sales.reset_index()

df_monthly_sales.rename(columns={
    "order_purchase_timestamp": "order_month",
    "order_id": "order_count",
    "payment_value": "revenue"
}, inplace=True)


#agregasi review secara bulanan

# filter data review tahun 2017
df_review_2017 = df_all[df_all["review_creation_date"].dt.year == 2017].copy()

# agregasi bulanan: jumlah review per bulan dan rata-rata review score per bulan
df_monthly_review = df_review_2017.resample(rule='M', on='review_creation_date').agg({
    "order_id": "nunique",
    "review_score": "mean"
})

df_monthly_review.index = df_monthly_review.index.strftime('%Y-%m')
df_monthly_review = df_monthly_review.reset_index()

df_monthly_review.rename(columns={
    "review_creation_date": "review_month",
    "order_id": "review_count",
    "review_score": "avg_review_score"
}, inplace=True)

# bulatkan rata-rata review ke 2 angka desimal
df_monthly_review["avg_review_score"] = df_monthly_review["avg_review_score"].round(2)


# =========================
# Distribusi Rating Review (2017)
# =========================

df_review_distribution_2017 = df_review_2017["review_score"].value_counts().sort_index().reset_index()

df_review_distribution_2017.columns = ["review_score", "review_count"]


# filter data tahun 2017
df_operational_2017 = df_all[df_all["order_purchase_timestamp"].dt.year == 2017].copy()

# agregasi bulanan
monthly_operational_df = df_operational_2017.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",          # jumlah order
    "payment_value": "sum",        # jumlah nilai transaksi
    "delivery_time": "mean",        # rata-rata waktu pengiriman
    "answer_time": "mean",          # rata-rata waktu respons review
    "review_score": "mean"          # rata-rata kepuasan pelanggan
})

monthly_operational_df.index = monthly_operational_df.index.strftime('%Y-%m')
monthly_operational_df = monthly_operational_df.reset_index()

monthly_operational_df.rename(columns={
    "order_purchase_timestamp": "order_month",
    "order_id": "order_count",
    "payment_value": "avg_payment_value",
    "delivery_time": "avg_delivery_time",
    "answer_time": "avg_answer_time",
    "review_score": "avg_review_score"
}, inplace=True)

# rapikan angka desimal
monthly_operational_df["avg_payment_value"] = monthly_operational_df["avg_payment_value"].round(2)
monthly_operational_df["avg_delivery_time"] = monthly_operational_df["avg_delivery_time"].round(2)
monthly_operational_df["avg_answer_time"] = monthly_operational_df["avg_answer_time"].round(2)
monthly_operational_df["avg_review_score"] = monthly_operational_df["avg_review_score"].round(2)

monthly_operational_df.head()

operational_corr_df = monthly_operational_df[
    ["order_count", "avg_payment_value", "avg_delivery_time", "avg_answer_time", "avg_review_score"]
].corr()


# RFM tetap dipakai di dashboard
recent_date = df_all["order_purchase_timestamp"].max()

rfm_df = df_all.groupby("customer_unique_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "payment_value": "sum"
})

rfm_df.rename(columns={
    "order_purchase_timestamp": "Recency",
    "order_id": "Frequency",
    "payment_value": "Monetary"
}, inplace=True)

rfm_df["Monetary"] = rfm_df["Monetary"].round(2)

# RFM Ranking, Scoring, and Segmentation
rfm_df["R_rank"] = rfm_df["Recency"].rank(ascending=False)
rfm_df["F_rank"] = rfm_df["Frequency"].rank(ascending=True)
rfm_df["M_rank"] = rfm_df["Monetary"].rank(ascending=True)

rfm_df["R_rank_norm"] = (rfm_df["R_rank"] / rfm_df["R_rank"].max()) * 100
rfm_df["F_rank_norm"] = (rfm_df["F_rank"] / rfm_df["F_rank"].max()) * 100
rfm_df["M_rank_norm"] = (rfm_df["M_rank"] / rfm_df["M_rank"].max()) * 100

rfm_df["RFM_Score"] = (
    0.50 * rfm_df["R_rank_norm"] +
    0.30 * rfm_df["F_rank_norm"] +
    0.20 * rfm_df["M_rank_norm"]
)

rfm_df["RFM_Score"] = (rfm_df["RFM_Score"] * 0.05).round(2)

rfm_df["Customer_segment"] = np.where(
    rfm_df["RFM_Score"] > 4.0, "High Value Customers",
    np.where(
        rfm_df["RFM_Score"] > 3.0, "Medium Value Customers",
        np.where(
            rfm_df["RFM_Score"] > 1.6, "Low Value Customers",
            "Lost Customers"
        )
    )
)


# Compact insight helpers
peak_sales_row = df_monthly_sales.loc[df_monthly_sales["order_count"].idxmax()]
lowest_sales_row = df_monthly_sales.loc[df_monthly_sales["order_count"].idxmin()]
peak_revenue_row = df_monthly_sales.loc[df_monthly_sales["revenue"].idxmax()]

peak_review_row = df_monthly_review.loc[df_monthly_review["review_count"].idxmax()]
lowest_rating_row = df_monthly_review.loc[df_monthly_review["avg_review_score"].idxmin()]

top_corr_series = operational_corr_df["avg_review_score"].drop("avg_review_score").sort_values(key=lambda s: s.abs(), ascending=False)
top_corr_name = top_corr_series.index[0]
top_corr_value = top_corr_series.iloc[0]

total_orders = int(df_all["order_id"].nunique())
total_revenue = float(df_all["payment_value"].sum())
avg_rating = float(df_all["review_score"].mean())

rfm_segment_counts = rfm_df["Customer_segment"].value_counts()


# HEADER 
st.title("Dashboard E-Commerce Public Dataset (2017)")
st.caption("Ringkasan interaktif penjualan, kepuasan pelanggan, faktor operasional, dan segmentasi RFM.")


# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Revenue", f"{total_revenue:,.2f}")
col3.metric("Avg Rating", f"{avg_rating:.2f}")

st.markdown("---")


tab_overview, tab_sales, tab_customer, tab_rfm = st.tabs([
    "Overview",
    "Sales and Revenue",
    "Customer Satisfaction",
    "RFM",
])


with tab_overview:
    left_col, right_col = st.columns([2, 1])

    with left_col:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_monthly_sales["order_month"], df_monthly_sales["order_count"], marker='o', linewidth=2)
        ax.set_title("Month-over-Month Sales (2017)", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Jumlah Order", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

    with right_col:
        st.info(f"Peak sales: {peak_sales_row['order_month']} ({int(peak_sales_row['order_count']):,} orders)")
        st.info(f"Lowest sales: {lowest_sales_row['order_month']} ({int(lowest_sales_row['order_count']):,} orders)")
        st.success(f"Revenue peak: {peak_revenue_row['order_month']} ({peak_revenue_row['revenue']:,.2f})")
        st.info("Dashboard ini fokus pada tren 2017, customer satisfaction, operasional, dan RFM.")


with tab_sales:
    sales_left, sales_right = st.columns([2, 1])

    with sales_left:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_monthly_sales["order_month"], df_monthly_sales["order_count"], marker='o')

        ax.set_title("Month-over-Month Sales (2017)", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Jumlah Order", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_monthly_sales["order_month"], df_monthly_sales["revenue"], marker='o')

        ax.set_title("Month-over-Month Revenue (2017)", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Revenue", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

    with sales_right:
        st.info(f"Lowest sales: {lowest_sales_row['order_month']} | {int(lowest_sales_row['order_count']):,} orders")
        st.info(f"Highest sales: {peak_sales_row['order_month']} | {int(peak_sales_row['order_count']):,} orders")
        st.info(f"Highest revenue: {peak_revenue_row['order_month']} | {peak_revenue_row['revenue']:,.2f}")
        st.success("Tren: meningkat sepanjang 2017")
        st.dataframe(df_monthly_sales[["order_month", "order_count", "revenue"]], use_container_width=True)


with tab_customer:
    customer_left, customer_right = st.columns([2, 1])

    with customer_left:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_monthly_review["review_month"], df_monthly_review["review_count"], marker='o')
        ax.set_title("Jumlah Monthly Reviews (2017)", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Jumlah Reviews", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_monthly_review["review_month"], df_monthly_review["avg_review_score"], marker='o')
        ax.set_title("Rata-Rata Monthly Ratings (2017)", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Review Score", fontsize=12)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

    with customer_right:
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = ["#dbeafe", "#93c5fd", "#60a5fa", "#3b82f6", "#1d4ed8"]
        ax.pie(
            df_review_distribution_2017["review_count"],
            labels=df_review_distribution_2017["review_score"],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
        )
        ax.set_title("Distribusi Rating Review (2017)", fontsize=14)
        st.pyplot(fig)

        st.info(f"Peak review volume: {peak_review_row['review_month']} ({int(peak_review_row['review_count']):,})")
        st.info(f"Lowest avg rating: {lowest_rating_row['review_month']} ({lowest_rating_row['avg_review_score']:.2f})")
        st.success("Rating 4-5 masih dominan")


with tab_rfm:
    rfm_left, rfm_right = st.columns([2, 1])

    with rfm_left:
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ["#dbeafe", "#93c5fd", "#60a5fa", "#3b82f6"]

        ax.pie(
            rfm_segment_counts,
            labels=rfm_segment_counts.index,
            autopct="%.0f%%",
            startangle=90,
            colors=colors
        )

        ax.set_title("Customer Segmentation based on RFM (2017)", fontsize=14)
        st.pyplot(fig)

    with rfm_right:
        st.metric("Average Recency (hari)", round(rfm_df["Recency"].mean(), 1))
        st.metric("Average Frequency", round(rfm_df["Frequency"].mean(), 2))
        st.metric("Average Monetary", round(rfm_df["Monetary"].mean(), 2))
        st.info("Low value + lost customers masih dominan")
        st.info("Ada peluang reactivation untuk segmen rendah")


st.markdown("---")


st.subheader("Correlation Overview")
heat_left, heat_right = st.columns([2, 1])

with heat_left:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        operational_corr_df,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        linewidths=0.5,
        ax=ax
    )
    ax.set_title("Correlation Heatmap of Operational Factors", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

with heat_right:
    st.info(f"Korelasi terkuat dengan rating: {top_corr_name} ({top_corr_value:.2f})")
    st.success("Delivery time adalah key driver")
    st.dataframe(operational_corr_df, use_container_width=True)


st.markdown("---")


st.header("Conclusion")
st.info("Sales naik sepanjang 2017, dengan puncak di November.")
st.info("Review volume naik, tapi rating rata-rata menunjukan tren menurun di akhir tahun.")
st.info("Delivery time punya hubungan terkuat dengan kepuasan pelanggan.")
