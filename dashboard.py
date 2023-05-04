import json
import pandas as pd
import streamlit as st
import plotly.express as px

file = "/Users/raphaelseghier/PYTHON/streamlit/zhou_all_reviews.json"

with open(file) as f:
    data = json.load(f)


# create dataframe from data 
df = pd.DataFrame(data)

# add a column numberReviews that counts the number of rows starting from botton to top
df = df.assign(numberReviews = df.shape[0] - df.index.values)

df['publishedAtDate'] = pd.to_datetime(df['publishedAtDate'])
df_weekly = df.groupby(pd.Grouper(key='publishedAtDate', freq='W-MON'))['numberReviews'].sum().reset_index()

fig = px.bar(df_weekly, x='publishedAtDate', y='numberReviews') #title='Number of Reviews per Week'



#==================

import requests
# set API key and place ID
API_KEY = "AIzaSyDc_Np7pVDPOYMB2qQ7hnrQ50I57AtoNNU"
place_id = "ChIJ-_qWiCmrQjQRpb-XYGT_5BE"

# set parameters for place details request
params = {
"key": API_KEY,
"place_id": place_id,
"fields": "name,rating,reviews,user_ratings_total",
}

# send request to Google Maps Places API for place details
response = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params=params)
data = response.json()

# display place details response
#print(data)

##################

place_details = data

name = place_details['result']['name']
rating = place_details['result']['rating']
reviews = place_details['result']['reviews']
user_ratings_total = place_details['result']['user_ratings_total']


st.write(f"Restaurant: {name}")
st.write(f"Current Rating: {rating}")
st.write(f"Total Number of Reviews: {user_ratings_total}")

st.write("### Number of Reviews per Week")

#display chart
st.plotly_chart(fig)

st.write("### Latest Ratings")
st.write("------")

for review in reviews:
    st.write(f"Author: {review['author_name']}")
    st.write(f"Rating: {review['rating']}")
    st.write(f"Review: {review['text']}")
    st.write("------")
