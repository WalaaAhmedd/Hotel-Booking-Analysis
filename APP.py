import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



#  PAGE CONFIGURATION


st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide"
)



#  LOAD DATA


@st.cache_data
def load_data():

    # Read the cleaned dataset
    df = pd.read_csv("cleaned_hotel_bookings.csv")

    # Make sure total_nights exists
    if "total_nights" not in df.columns:
        df["total_nights"] = (
            df["stays_in_weekend_nights"]
            + df["stays_in_week_nights"]
        )

    # Make sure cancellation_status exists
    if "cancellation_status" not in df.columns:
        df["cancellation_status"] = df["is_canceled"].map({
            0: "Not Canceled",
            1: "Canceled"
        })

    # Make sure month order is correct
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    df["arrival_date_month"] = pd.Categorical(
        df["arrival_date_month"],
        categories=months,
        ordered=True
    )

    return df


df = load_data()



# TITLE


st.title("🏨 Hotel Booking Analysis Dashboard")

st.write(
    "Interactive dashboard based on the Hotel Booking dataset."
)



# SIDEBAR FILTERS


st.sidebar.header("Filters")


# Hotel filter
hotel_options = ["All"] + sorted(df["hotel"].dropna().unique().tolist())

selected_hotel = st.sidebar.selectbox(
    "Hotel",
    hotel_options
)


# Year filter
year_options = ["All"] + sorted(
    df["arrival_date_year"].dropna().unique().tolist()
)

selected_year = st.sidebar.selectbox(
    "Arrival Year",
    year_options
)


# Market Segment filter
segment_options = ["All"] + sorted(
    df["market_segment"].dropna().unique().tolist()
)

selected_segment = st.sidebar.selectbox(
    "Market Segment",
    segment_options
)



#  APPLY FILTERS


filtered_df = df.copy()


if selected_hotel != "All":
    filtered_df = filtered_df[
        filtered_df["hotel"] == selected_hotel
    ]


if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["arrival_date_year"] == selected_year
    ]


if selected_segment != "All":
    filtered_df = filtered_df[
        filtered_df["market_segment"] == selected_segment
    ]


# Check if filters return no data
if filtered_df.empty:

    st.warning("No data available for the selected filters.")

    st.stop()



# TABS


overview_tab, bookings_tab, cancellation_tab, stay_tab = st.tabs(
    [
        "Overview",
        "Bookings",
        "Cancellations",
        "Stay"
    ]
)



# TAB 1 - OVERVIEW


with overview_tab:

    st.header("Overview")

    # Cancellation Rate
 

    cancellation_rate = (
        filtered_df["is_canceled"].mean() * 100
    )

    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )



    #  Hotel Distribution


    st.subheader("Hotel Distribution")

    hotel_counts = filtered_df["hotel"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x=hotel_counts.index,
        y=hotel_counts.values,
        ax=ax
    )

    ax.set_title("Number of Bookings by Hotel")
    ax.set_xlabel("Hotel")
    ax.set_ylabel("Number of Bookings")

    st.pyplot(fig)

    plt.close(fig)



# TAB 2 - BOOKINGS


with bookings_tab:

    st.header("Bookings Analysis")


    # Bookings by Month


    st.subheader("Bookings by Month")

    monthly_bookings = (
        filtered_df
        .groupby(
            "arrival_date_month",
            observed=True
        )
        .size()
        .reset_index(name="bookings")
    )


    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=monthly_bookings,
        x="arrival_date_month",
        y="bookings",
        marker="o",
        ax=ax
    )

    ax.set_title("Bookings by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Bookings")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    plt.close(fig)


   
    # Market Segment
  

    st.subheader("Market Segment")

    market = filtered_df["market_segment"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        x=market.values,
        y=market.index,
        ax=ax
    )

    ax.set_title("Bookings by Market Segment")
    ax.set_xlabel("Number of Bookings")
    ax.set_ylabel("Market Segment")

    st.pyplot(fig)

    plt.close(fig)



# TAB 3 - CANCELLATIONS


with cancellation_tab:

    st.header("Cancellation Analysis")


   
    # 5. Cancellation by Hotel


    st.subheader("Cancellation by Hotel")

    hotel_cancellation = (
        filtered_df
        .groupby("hotel")["is_canceled"]
        .mean()
        .mul(100)
        .reset_index()
    )


    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=hotel_cancellation,
        x="hotel",
        y="is_canceled",
        ax=ax
    )

    ax.set_title("Cancellation Rate by Hotel")
    ax.set_xlabel("Hotel")
    ax.set_ylabel("Cancellation Rate (%)")

    st.pyplot(fig)

    plt.close(fig)


  
    #  Cancellation Rate by Market Segment
   

    st.subheader("Cancellation Rate by Market Segment")

    segment_cancel = (
        filtered_df
        .groupby("market_segment")["is_canceled"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )


    fig, ax = plt.subplots(figsize=(10, 6))

    segment_cancel.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_title("Cancellation Rate by Market Segment")
    ax.set_xlabel("Cancellation Rate (%)")
    ax.set_ylabel("Market Segment")

    st.pyplot(fig)

    plt.close(fig)



    # Lead Time vs Cancellation
   

    st.subheader("Lead Time vs Cancellation")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=filtered_df,
        x="is_canceled",
        y="lead_time",
        ax=ax
    )

    ax.set_title("Lead Time by Cancellation Status")
    ax.set_xlabel("Canceled")
    ax.set_ylabel("Lead Time (days)")

    st.pyplot(fig)

    plt.close(fig)



# TAB 4 - STAY


with stay_tab:

    st.header("Stay & Hotel Pricing")


    
    #  ADR by Hotel
   

    st.subheader("ADR by Hotel")

    adr_by_hotel = (
        filtered_df
        .groupby("hotel")["adr"]
        .mean()
        .reset_index()
    )


    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=adr_by_hotel,
        x="hotel",
        y="adr",
        ax=ax
    )

    ax.set_title("Average Daily Rate by Hotel")
    ax.set_xlabel("Hotel")
    ax.set_ylabel("Average Daily Rate")

    st.pyplot(fig)

    plt.close(fig)


    
    # Length of Stay
 

    st.subheader("Length of Stay")

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.histplot(
        data=filtered_df,
        x="total_nights",
        bins=30,
        ax=ax
    )

    ax.set_title("Distribution of Total Nights")
    ax.set_xlabel("Total Nights")
    ax.set_ylabel("Number of Bookings")

    st.pyplot(fig)

    plt.close(fig)



# FOOTER


st.sidebar.markdown("---")

st.sidebar.write(
    f"Total records: {len(filtered_df):,}"
)