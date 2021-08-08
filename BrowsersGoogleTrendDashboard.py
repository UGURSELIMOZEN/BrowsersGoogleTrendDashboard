import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

st.write("""
# Browser's Google Trend Dashboard

""")

years = ['2004' ,'2005' ,'2006' ,'2007' ,'2008' , '2009' , '2010' ,
         '2011' ,'2012' ,'2013' ,'2014' ,'2015' ,'2016' ,'2017' ,'2018','2019']

browsers = ('Firefox' ,'Safari' ,'Explorer' ,'Chrome' ,'Opera')

start_date = st.sidebar.date_input('Start Date' , value = pd.to_datetime('2004-01-01'))
end_date = st.sidebar.date_input('End Date' , value = pd.to_datetime('2020-10-01'))

roll_means_plot = st.sidebar.checkbox('Rolling Means Plot')
rolling_period = st.sidebar.slider(' Rolling Means Period (Month) ', 3, 12)

yearly_comparison_plot = st.sidebar.checkbox('Yearly Comparison Plot')
select_browser = st.sidebar.selectbox("Browser" , browsers)
select_year = st.sidebar.multiselect("Year/Years" ,years)



df = pd.read_csv("worldwide_browser_trends.csv",parse_dates=['Month'], index_col='Month')
df.columns = ['Firefox' ,'Safari' ,'Chrome' ,'Explorer' ,'Opera']


if (roll_means_plot == True) & (yearly_comparison_plot == False) :
    new_df = df.loc[start_date : end_date ,]
    fig , ax = plt.subplots()
    st.subheader("{} Month Rolling Means Plot".format(rolling_period))
    ax = new_df.rolling(window=rolling_period).mean().plot(figsize=(14,6))
    ax.set_ylabel("Search Interest")
    st.pyplot()

elif (roll_means_plot == False) & (yearly_comparison_plot == False) :
    new_df = df.loc[start_date : end_date ,]
    fig , ax = plt.subplots()
    st.subheader("Search Interest Plot")
    ax = new_df.plot(figsize=(14,6))
    ax.set_ylabel("Search Interest")
    st.pyplot()

elif (roll_means_plot == False) & (yearly_comparison_plot == True) :
    trends = pd.DataFrame()
    for year in select_year :
        trends_per_year = df.loc[str(year), [str(select_browser)]].reset_index(drop=True)
        trends_per_year.rename(columns={str(select_browser): year}, inplace=True)
        trends = pd.concat([trends, trends_per_year], axis=1)
    fig , ax = plt.subplots()
    st.subheader("{} Search Interest Plot".format(select_browser))
    ax = trends.plot(figsize = (12 ,5))
    ax.set_ylabel('Search Interest')
    ax.set_xlabel('Month')
    st.pyplot()

st.sidebar.text("Built with  ❤️  Streamlit")
