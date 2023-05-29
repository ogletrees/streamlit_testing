from datetime import date,timedelta
import numpy as np
import pandas as pd
import streamlit as st

# get dates
today = date.today()
print("Today's date:", today)
date5 = today - timedelta(days = 7) # make it one week, 7 days
print(date5)

x = pd.date_range(date5, today, freq='D')
y = np.datetime_as_string(x, unit='D')
# all_days = np.arange(date5, today, dtype='M8[D]')
site = ['000000000035', 'Deans Bridge']
# site = ['000000000022','North Meadow Walk, Main Path']
# site = ['000000000209', 'ELGT Little France South']
# site = ['000000000208', 'Shawfair']
# build url for data
url = 'https://edintraveldata.drakewell.com/tfdaysreport.asp?node=EDINBURGH_CYCLE&cosit=' + site[0] + '&reportdate=' + str(date5) + '&enddate=' + str(today)



tables = pd.read_html(url)


df = tables[0].iloc[0:24, 0:9]
# combine cols

# name cols
df.columns = ['hours', str(y[0]), str(y[1]), str(y[2]), str(y[3]), str(y[4]), str(y[5]), str(y[6]), str(y[7])]
# to long format
df = df.melt(id_vars='hours')
df.columns = ['hour', 'date', 'count']
# make datetime col
df["dt"] = pd.to_datetime(df['date'] + ' ' + df['hour'])
# count to numbers
df['count'] = df['count'].str.replace('-','')
df["count"] = pd.to_numeric(df["count"])

# make page
st.set_page_config(
    page_title="Bike Counts",
    page_icon="✅",
    layout="wide",
)
# st.dataframe(df)
st.header("This is a plot of hourly bicycle counts - " + site[1] + ", Edinburgh")
st.line_chart(df, x='dt', y='count')