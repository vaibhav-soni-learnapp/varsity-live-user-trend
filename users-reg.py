import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go # type: ignore
import requests

@st.cache_data
def fetch_data(from_date, to_date):
    url = f"https://oracle.varsitylive.in/admin/platform-stats/users/users-created/range?fromDate={from_date}&toDate={to_date}"
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxODUyZmZmNi02N2RlLTRiNjYtYmIwMy01NDJlY2Q4YmZmNzMiLCJhZG0iOnRydWUsImlhdCI6MTcxMzQ0ODgxMSwiZXhwIjoxNzEzNTM1MjExLCJhdWQiOiJwbGF0bzowLjAuMSIsImlzcyI6InZhcnNpdHktbGl2ZSJ9.xLDKzC_vhs8U8z0hw2dVu7sm0qf4WwUuHu5coSPBKG0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['items'])
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values(by='date')
    else:
        return pd.DataFrame()

def plot_data(df):
    df['Cumulative'] = df['count'].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['date'], y=df['count'], name='Daily Count'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['Cumulative'], mode='lines+markers', name='Cumulative Count'))
    
    fig.update_layout(
        title='Item Count Over Time',
        xaxis_title='Date',
        yaxis_title='Count',
        template='plotly_dark',
        height=600,
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
    )
    return fig

def main():
    st.title('Varsity Live users registration trend')
    st.write("oracle.varsitylive.in/admin/platform-stats/users/users-created")

    with st.form("my_form"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=pd.to_datetime('2024-04-01'))
        with col2:
            end_date = st.date_input("End date", value=pd.to_datetime('2024-04-18'))

        
        submitted = st.form_submit_button("Submit")

    if submitted:
            df = fetch_data(start_date.isoformat(), end_date.isoformat())
            if not df.empty:
                fig = plot_data(df)
                fig.update_layout(title= 'Count Over Time')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No data available for the selected date range or an error occurred.")

    

if __name__ == "__main__":
    main()
