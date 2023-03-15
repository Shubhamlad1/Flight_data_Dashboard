import streamlit as st
from db_connector import DB
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px





db= DB()

st.sidebar.title("Flight  Data Dashboard")

user_options= st.sidebar.selectbox("Menu", ["Select One", "Check Flights", "Flights Analysis"])

if user_options == "Check Flights":
    st.title("Select Source and Destination")

    col1, col2, col3 = st.columns(3)

    city= db.fetch_city()

    with col1:
        source = st.selectbox("Source", city)

    with col2:
        destination = st.selectbox("Destination", city)
        

    if st.button("Search"):
        try:
            City_names= db.fetch_flights_details(source, destination)
            if len(City_names) >0:
                data= pd.DataFrame(City_names)

                st.dataframe(data)
            else:
                st.error("No Flights Available")
        except Exception as e:
            st.error(e)

elif user_options == "Flights Analysis":
    st.title("Flights Analytics")

    airline, frequency= db.fetch_airline_info()

    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))

    st.header("Flight Frequency")
    st.plotly_chart(fig)

    city, frequency1= db.busy_airport()


    fig = px.bar(
        x=city,
        y=frequency1,
        title="Busy Airtports"
    )


    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.title("""
        Flight Data Live Dashboard
        Dataset is kept on Microsoft SQL server. Streamlit is used to create basic dashboard.
    """)

