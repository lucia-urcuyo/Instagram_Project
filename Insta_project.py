import json
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

accesstoken= ''

while accesstoken== '':
    st.write('Enter your Instagram account ID:')
    instaID = st.text_input('Instagram account ID')

    st.write('Enter your access token:')
    accesstoken = st.text_input('Access token')


#instaID = 17841446768661835
#accesstoken = 'EAAP6OFrPKd8BAN8rXOZBrYZAMo1GtElOYYBaqm4TZBb6eMagqPIlEq7XNHwnzlZCyFIvR2zaNXhogOLAo9EgVr0t1Ao8POVkbrdMeiXi5dkK6FsJqlQPCKaZB6acz3uY4wu1CZAzz9vZCh6fkQ43HWBdaA5gQyjITO2gOJffYY9PGdZAt351s93GvbDnWhu8qWXVtdI8v2TM0tD58ltS9xQyosvG2fLJv6j2wwyvz8OkZA8uCTt3h0uwsc4YzhzrY52MZD'

# Function 1: Asks for a URL and returns media IDs into a dataframe
def link_to_mediaID(link):
    try:
        dm = requests.get(link)
        mid = json.loads(dm.content)
        jid = (mid.get('data'))
        dfID = pd.DataFrame.from_dict(jid)
        return dfID
    except:
        print("An error occurred. Invalid URL")


# Function 2: Asks for media ID and desired attribute and returns the data
def data_from_mediaID(mediaID, attribute_type):
    domain2 = 'https://graph.facebook.com/v3.0/'

    try:
        aurl = domain2 + mediaID + '/insights/' + attribute_type + '?' + access_token
        dmid = requests.get(aurl)
        dd = json.loads(dmid.content)
        z = dd['data'][0]
        attribute_d = z.get('values')
        ad = pd.DataFrame.from_dict(attribute_d)
        return ad.iloc[0, 0]
    except:
        # Attribute must be one of the following values: impressions, reach, carousel_album_impressions,
        # carousel_album_reach, carousel_album_engagement, carousel_album_saved, carousel_album_video_views,
        # taps_forward, taps_back, exits, replies, engagement, saved, video_views, likes, comments, shares,
        # plays, total_interactions, follows, profile_visits, profile_activity, navigation"
        return (0)


# Function 3: Asks for media ID and desired fields and returns the data
def data_from_mediaID2(mediaID, field):
    domain3 = 'https://graph.facebook.com/v14.0/'

    try:
        furl = domain3 + mediaID + '?fields=' + field + '&' + access_token
        mediafd = requests.get(furl)
        fdata = json.loads(mediafd.content)
        fd = fdata.get(field)

        return fd
    except:
        return (0)


# First part of our URL
domain = "https://graph.facebook.com/v9.0/"

# Always stays the same, no need to change, 2nd part of URL
my_insta_id = str(instaID)

# Need to generate a new one every 60 min, 4th part of URL
access_token = 'access_token=' + str(accesstoken)

# Build URL
urlformedia = domain + my_insta_id + "/media?" + access_token

# Pull data from URL
datamedia = requests.get(urlformedia)
mediaID = json.loads(datamedia.content)

# Get all of the URL's containing the Media ID's

bull = True
counter = 1

urllist = [urlformedia]

while bull == True:

    try:
        # Grab URL and make it a json object

        x = requests.get(urllist[counter - 1])
        y = json.loads(x.content)

        # Get the next URL from the json object

        a = y.get('paging')
        b = a.get('next')

        # Store next URL in the next position

        urllist.append(b)

        # Add one to our counter to keep track of loops

        counter += 1

    except:

        bull = False

# Get all of the Media ID's from the URL's

counter1 = 0
IDlist = link_to_mediaID(urllist[0])

while (counter-1) > (counter1+1):
    IDlist = pd.concat([IDlist, link_to_mediaID(urllist[counter1+1])])

    counter1 += 1


# Forloop to get attribute values for each media id

plays = []
likes = []
comments = []
impressions = []
engagement = []
reach = []
saved = []
shares = []
total_interactions = []
follows = []
profile_visits = []
profile_activity = []
navigation = []
timestamp = []
permalink = []
caption = []

for i in IDlist['id']:
    plays.append(data_from_mediaID(i, 'plays'))
    likes.append(data_from_mediaID(i, 'likes'))
    comments.append(data_from_mediaID(i, 'comments'))
    impressions.append(data_from_mediaID(i, 'impressions'))
    engagement.append(data_from_mediaID(i, 'engagement'))
    reach.append(data_from_mediaID(i, 'reach'))
    saved.append(data_from_mediaID(i, 'saved'))
    shares.append(data_from_mediaID(i, 'shares'))
    total_interactions.append(data_from_mediaID(i, 'total_interactions'))
    follows.append(data_from_mediaID(i, 'follows'))
    profile_visits.append(data_from_mediaID(i, 'profile_visits'))
    profile_activity.append(data_from_mediaID(i, 'profile_activity'))
    navigation.append(data_from_mediaID(i, 'navigation'))
    timestamp.append(data_from_mediaID2(i, 'timestamp'))
    permalink.append(data_from_mediaID2(i, 'permalink'))
    caption.append(data_from_mediaID2(i, 'caption'))

# Add timestampt to ID list
IDlist['timestamp'] = timestamp

# Split timestamp into 2 columns: date and time
timestamp = IDlist['timestamp'].str.split(pat='T', n=-1, expand=True)
date = IDlist['date'] = timestamp[0]
time = IDlist['time'] = timestamp[1]

# Create 2 columns with the name of the week day and the number of the week day
IDlist['my dates'] = pd.to_datetime(IDlist['date'])
IDlist['num_day_of_week'] = IDlist['my dates'].dt.dayofweek

days = {0: 'Mon', 1: 'Tues', 2: 'Weds', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

IDlist['day_of_week'] = IDlist['num_day_of_week'].apply(lambda x: days[x])

num_day_of_week = IDlist['num_day_of_week']
day_of_week = IDlist['day_of_week']

# Add attribute values columns to ID list dataframe
IDlist['plays'] = plays
IDlist['likes'] = likes
IDlist['comments'] = comments
IDlist['impressions'] = impressions
IDlist['engagement'] = engagement
IDlist['reach'] = reach
IDlist['saved'] = saved
IDlist['shares'] = shares
IDlist['total_interactions'] = total_interactions
IDlist['follows'] = follows
IDlist['profile_visits'] = profile_visits
IDlist['profile_activity'] = profile_activity
IDlist['navigation'] = navigation
IDlist['date'] = date
IDlist['time'] = time
IDlist['num_day_of_week'] = num_day_of_week
IDlist['day_of_week'] = day_of_week
IDlist['permalink'] = permalink
IDlist['caption'] = caption

# Forloop to count number of hastags for each post
cap = IDlist['caption'].iloc[0]

hashtags = []

for cap in IDlist['caption']:

        hashtag_count = 0

        for hasht in cap:

                if hasht == '#':
                        hashtag_count = hashtag_count + 1

        hashtags.append(hashtag_count)

# Add hashtags column to IDlist dataframe
IDlist['hashtags'] = hashtags

# Split time into 3 columns: hour, minutes, seconds
time2 = IDlist['time'].str.split(pat=':', n=-1, expand=True)

# Add hour posted column to IDlist
IDlist['hour posted'] = time2[0]

# Reverse order and reindex dataframe
IDlist = IDlist.iloc[::-1]
IDlist = IDlist.reset_index(drop=True)

# Select rows where plays = 0
PhotosData = IDlist[IDlist['plays'] == 0]
IDPD = PhotosData
IDPD = IDPD.index.tolist()

# Create new data frame with the removed rows selected above
ReelsData = IDlist.drop(
        labels=IDPD,
        axis=0,
        inplace=False)

# Drop all columns that dont apply to reels and columns that we don't need (timestamp, my dates and time)
ReelsData = ReelsData.drop(
        labels=["impressions", "engagement", "follows", "profile_visits", "profile_activity", "navigation", "timestamp",
                'time', 'my dates'],
        axis=1,
        inplace=False)

# Drop timestamp, my dates and time columns from PhotosData
PhotosData = PhotosData.drop(
    labels = ["likes", "comments", "plays", "shares", "total_interactions", "follows", "profile_visits",
                'profile_activity', 'navigation'],
    axis=1,
    inplace=False)

# Forloop to get attribute values for each media id

likes = []
comments = []

for i in PhotosData['id']:
    likes.append(data_from_mediaID2(str(i), 'like_count'))
    comments.append(data_from_mediaID2(str(i), 'comments_count'))

PhotosData['likes'] = likes
PhotosData['comments'] = comments



# Create an index column because for some reason pycharm doesn't understand when we call it
index = []
count = 0
for i in ReelsData['id']:
        index.append(count)
        count = count + 1

ReelsData.insert(0, 'index', index)

# Create a column that measures the enjoyment: the percentage of viewers that liked the video
ReelsData['enjoyment'] = (ReelsData['likes']/ReelsData['plays']) * 100

# Create a shortened version of the caption columns to make it fit better in the tooltip of the graphs below
ReelsData['shortcap'] = ReelsData['caption'].str[:25]

# Bar plots for all variables

likesplot = px.bar(ReelsData, x="index", y="likes", color="day_of_week", title="Likes", hover_data=['shortcap', 'hour posted', 'hashtags'])

# likesplot.show()

enjoyplot = px.bar(ReelsData, x="index", y="enjoyment", color="day_of_week", title="Enjoyment", hover_data=['shortcap', 'hour posted', 'hashtags'])

# enjoyplot.show()

playsplot = px.bar(ReelsData, x="index", y="plays", color="day_of_week", title="Plays", hover_data=['shortcap','hour posted', 'hashtags'])

# playsplot.show()

commentsplot = px.bar(ReelsData, x="index", y="comments", color="day_of_week", title="Comments", hover_data=['shortcap', 'hour posted', 'hashtags'])

# commentsplot.show()

# count how many reels where posted on each day of the week
postsperday = ReelsData.groupby('day_of_week')['index'].count()

# convert pandas series to dataframes
postdailycount = postsperday.to_frame()

# Set index as new column (day_of_week)
postdailycount.reset_index(inplace=True)

# rename 'index' column to 'dailycount'
postdailycount.rename({'index': 'dailycount'}, axis=1, inplace=True)

# set 'dailycount' column as a variable
dailycount = postdailycount['dailycount']

# get the play counts for each day separately, not using this yet
saturdayposts = postdailycount.loc[postdailycount['day_of_week'] == 'Sat']

# get daily average plays
avgdailyplays = ReelsData.groupby('day_of_week')['plays'].mean()

# convert pandas series to dataframes
dailyplaysmean = avgdailyplays.to_frame()

# Set index as new column (day_of_week)
dailyplaysmean.reset_index(inplace=True)

# add daily count as a new column
dailyplaysmean['dailycount'] = dailycount

# Reorder index according to day of the week
dailyplaysmean = dailyplaysmean.reindex([1, 5, 6, 4, 0, 2, 3])

# Make a bar plots of average plays per day
dailyplaysplot = px.bar(dailyplaysmean, x="day_of_week", y="plays", title='Average Daily Plays', hover_data=['dailycount'])
# dailyplaysplot.show()

# Extract data from each day of the week separately
sunday = ReelsData.loc[ReelsData['day_of_week'] == 'Sun']
monday = ReelsData.loc[ReelsData['day_of_week'] == 'Mon']
tuesday = ReelsData.loc[ReelsData['day_of_week'] == 'Tues']
wednesday = ReelsData.loc[ReelsData['day_of_week'] == 'Weds']
thursday = ReelsData.loc[ReelsData['day_of_week'] == 'Thurs']
friday = ReelsData.loc[ReelsData['day_of_week'] == 'Fri']
saturday = ReelsData.loc[ReelsData['day_of_week'] == 'Sat']

# calculate the average of plays per hour each day
meanplayssun = sunday.groupby('hour posted')['plays'].mean()
meanplaysmon = monday.groupby('hour posted')['plays'].mean()
meanplaystues = tuesday.groupby('hour posted')['plays'].mean()
meanplaysweds = wednesday.groupby('hour posted')['plays'].mean()
meanplaysthurs = thursday.groupby('hour posted')['plays'].mean()
meanplaysfri = friday.groupby('hour posted')['plays'].mean()
meanplayssat = saturday.groupby('hour posted')['plays'].mean()

# convert pandas series to dataframes
sunplays = meanplayssun.to_frame()
monplays = meanplaysmon.to_frame()
tuesplays = meanplaystues.to_frame()
wedsplays = meanplaysweds.to_frame()
thursplays = meanplaysthurs.to_frame()
friplays = meanplaysfri.to_frame()
satplays = meanplayssat.to_frame()

# Set index as new column (hour posted), so that it can be used in the barplot
sunplays.reset_index(inplace=True)
monplays.reset_index(inplace=True)
tuesplays.reset_index(inplace=True)
wedsplays.reset_index(inplace=True)
thursplays.reset_index(inplace=True)
friplays.reset_index(inplace=True)
satplays.reset_index(inplace=True)

# calculate the count of plays per hour each day
postcountsun = sunday.groupby('hour posted')['plays'].count()
postcountmon = monday.groupby('hour posted')['plays'].count()
postcounttues = tuesday.groupby('hour posted')['plays'].count()
postcountweds = wednesday.groupby('hour posted')['plays'].count()
postcountthurs = thursday.groupby('hour posted')['plays'].count()
postcountfri = friday.groupby('hour posted')['plays'].count()
postcountsat = saturday.groupby('hour posted')['plays'].count()

# convert pandas series to dataframes
postcsun = postcountsun.to_frame()
postcmon = postcountmon.to_frame()
postctues = postcounttues.to_frame()
postcweds = postcountweds.to_frame()
postcthurs = postcountthurs.to_frame()
postcfri = postcountfri.to_frame()
postcsat = postcountsat.to_frame()

# Rename the column as 'count'
# Set index as new column (hour posted) in order to be able to add it as a new column to the plays charts
# Set the count column as a variable
# Add count column to each day's plays chart
postcsun.rename({'plays': 'count'}, axis=1, inplace=True)
postcsun.reset_index(inplace=True)
count = postcsun['count']
sunplays['count'] = count

postcmon.rename({'plays': 'count'}, axis=1, inplace=True)
postcmon.reset_index(inplace=True)
count = postcmon['count']
monplays['count'] = count

postctues.rename({'plays': 'count'}, axis=1, inplace=True)
postctues.reset_index(inplace=True)
count = postctues['count']
tuesplays['count'] = count

postcweds.rename({'plays': 'count'}, axis=1, inplace=True)
postcweds.reset_index(inplace=True)
count = postcweds['count']
wedsplays['count'] = count

postcthurs.rename({'plays': 'count'}, axis=1, inplace=True)
postcthurs.reset_index(inplace=True)
count = postcthurs['count']
thursplays['count'] = count

postcfri.rename({'plays': 'count'}, axis=1, inplace=True)
postcfri.reset_index(inplace=True)
count = postcfri['count']
friplays['count'] = count

postcsat.rename({'plays': 'count'}, axis=1, inplace=True)
postcsat.reset_index(inplace=True)
count = postcsat['count']
satplays['count'] = count

# Make bar plots of average plays per hour each day
sunplaysplot = px.bar(sunplays, x="hour posted", y="plays", title="Sunday", hover_data=['count'])
# sunplaysplot.show()

monplaysplot = px.bar(monplays, x="hour posted", y="plays", title="Monday", hover_data=['count'])
# monplaysplot.show()

tuesplaysplot = px.bar(tuesplays, x="hour posted", y="plays", title="Tuesday", hover_data=['count'])
# tuesplaysplot.show()

wedsplaysplot = px.bar(wedsplays, x="hour posted", y="plays", title="Wednesday", hover_data=['count'])
# wedsplaysplot.show()

thursplaysplot = px.bar(thursplays, x="hour posted", y="plays", title="Thursday", hover_data=['count'])
# thursplaysplot.show()

friplaysplot = px.bar(friplays, x="hour posted", y="plays", title="Friday", hover_data=['count'])
# friplaysplot.show()

satplaysplot = px.bar(satplays, x="hour posted", y="plays", title='Saturday', hover_data=['count'])
# satplaysplot.show()

# Show all charts in streamlit
# st.plotly_chart(dailyplaysplot, use_container_width=True)
# st.plotly_chart(sunplaysplot, use_container_width=True)
# st.plotly_chart(monplaysplot, use_container_width=True)
# st.plotly_chart(tuesplaysplot, use_container_width=True)
# st.plotly_chart(wedsplaysplot, use_container_width=True)
# st.plotly_chart(thursplaysplot, use_container_width=True)
# st.plotly_chart(friplaysplot, use_container_width=True)
# st.plotly_chart(satplaysplot, use_container_width=True)
# st.plotly_chart(likesplot, use_container_width=True)
# st.plotly_chart(enjoyplot, use_container_width=True)
# st.plotly_chart(commentsplot, use_container_width=True)
# st.plotly_chart(playsplot, use_container_width=True)


# Create an index column because for some reason pycharm doesn't understand when we call it
index = []
count = 0
for i in PhotosData['id']:
        index.append(count)
        count = count + 1

PhotosData.insert(0, 'index', index)


# Create a shortened version of the caption columns to make it fit better in the tooltip of the graphs below
PhotosData['shortcap'] = PhotosData['caption'].str[:25]

# Bar plots for all variables

likesplot = px.bar(PhotosData, x="index", y="likes", color="day_of_week", title="Likes", hover_data=['shortcap', 'hour posted', 'hashtags'])

# likesplot.show()

commentsplot = px.bar(PhotosData, x="index", y="comments", color="day_of_week", title="Comments", hover_data=['shortcap', 'hour posted', 'hashtags'])

# commentsplot.show()

# count how many photos where posted on each day of the week
postsperday = PhotosData.groupby('day_of_week')['index'].count()

# convert pandas series to dataframes
postdailycount = postsperday.to_frame()

# Set index as new column (day_of_week)
postdailycount.reset_index(inplace=True)

# rename 'index' column to 'dailycount'
postdailycount.rename({'index': 'dailycount'}, axis=1, inplace=True)

# set 'dailycount' column as a variable
dailycount = postdailycount['dailycount']

# get the likes counts for each day separately, not using this yet
saturdayposts = postdailycount.loc[postdailycount['day_of_week'] == 'Sat']

# get daily average plays
avgdailylikes = PhotosData.groupby('day_of_week')['likes'].mean()

# convert pandas series to dataframes
dailylikesmean = avgdailylikes.to_frame()

# Set index as new column (day_of_week)
dailylikesmean.reset_index(inplace=True)

# add daily count as a new column
dailylikesmean['dailycount'] = dailycount

# Reorder index according to day of the week
dailyplaysmean = dailylikesmean.reindex([1, 5, 6, 4, 0, 2, 3])

# Make a bar plots of average plays per day
dailylikesplot = px.bar(dailylikesmean, x="day_of_week", y="likes", title='Average Daily Likes', hover_data=['dailycount'])
# dailylikesplot.show()

# Extract data from each day of the week separately
sunday = PhotosData.loc[PhotosData['day_of_week'] == 'Sun']
monday = PhotosData.loc[PhotosData['day_of_week'] == 'Mon']
tuesday = PhotosData.loc[PhotosData['day_of_week'] == 'Tues']
wednesday = PhotosData.loc[PhotosData['day_of_week'] == 'Weds']
thursday = PhotosData.loc[PhotosData['day_of_week'] == 'Thurs']
friday = PhotosData.loc[PhotosData['day_of_week'] == 'Fri']
saturday = PhotosData.loc[PhotosData['day_of_week'] == 'Sat']

# calculate the average of plays per hour each day
meanlikessun = sunday.groupby('hour posted')['likes'].mean()
meanlikesmon = monday.groupby('hour posted')['likes'].mean()
meanlikestues = tuesday.groupby('hour posted')['likes'].mean()
meanlikesweds = wednesday.groupby('hour posted')['likes'].mean()
meanlikesthurs = thursday.groupby('hour posted')['likes'].mean()
meanlikesfri = friday.groupby('hour posted')['likes'].mean()
meanlikessat = saturday.groupby('hour posted')['likes'].mean()

# convert pandas series to dataframes
sunlikes = meanlikessun.to_frame()
monlikes = meanlikesmon.to_frame()
tueslikes = meanlikestues.to_frame()
wedslikes = meanlikesweds.to_frame()
thurslikes = meanlikesthurs.to_frame()
frilikes = meanlikesfri.to_frame()
satlikes = meanlikessat.to_frame()

# Set index as new column (hour posted), so that it can be used in the barplot
sunlikes.reset_index(inplace=True)
monlikes.reset_index(inplace=True)
tueslikes.reset_index(inplace=True)
wedslikes.reset_index(inplace=True)
thurslikes.reset_index(inplace=True)
frilikes.reset_index(inplace=True)
satlikes.reset_index(inplace=True)

# calculate the count of likes per hour each day
postcountsun = sunday.groupby('hour posted')['likes'].count()
postcountmon = monday.groupby('hour posted')['likes'].count()
postcounttues = tuesday.groupby('hour posted')['likes'].count()
postcountweds = wednesday.groupby('hour posted')['likes'].count()
postcountthurs = thursday.groupby('hour posted')['likes'].count()
postcountfri = friday.groupby('hour posted')['likes'].count()
postcountsat = saturday.groupby('hour posted')['likes'].count()

# convert pandas series to dataframes
postcsun = postcountsun.to_frame()
postcmon = postcountmon.to_frame()
postctues = postcounttues.to_frame()
postcweds = postcountweds.to_frame()
postcthurs = postcountthurs.to_frame()
postcfri = postcountfri.to_frame()
postcsat = postcountsat.to_frame()

# Rename the column as 'count'
# Set index as new column (hour posted) in order to be able to add it as a new column to the plays charts
# Set the count column as a variable
# Add count column to each day's plays chart
postcsun.rename({'likes': 'count'}, axis=1, inplace=True)
postcsun.reset_index(inplace=True)
count = postcsun['count']
sunlikes['count'] = count

postcmon.rename({'likes': 'count'}, axis=1, inplace=True)
postcmon.reset_index(inplace=True)
count = postcmon['count']
monlikes['count'] = count

postctues.rename({'likes': 'count'}, axis=1, inplace=True)
postctues.reset_index(inplace=True)
count = postctues['count']
tueslikes['count'] = count

postcweds.rename({'likes': 'count'}, axis=1, inplace=True)
postcweds.reset_index(inplace=True)
count = postcweds['count']
wedslikes['count'] = count

postcthurs.rename({'likes': 'count'}, axis=1, inplace=True)
postcthurs.reset_index(inplace=True)
count = postcthurs['count']
thurslikes['count'] = count

postcfri.rename({'likes': 'count'}, axis=1, inplace=True)
postcfri.reset_index(inplace=True)
count = postcfri['count']
frilikes['count'] = count

postcsat.rename({'likes': 'count'}, axis=1, inplace=True)
postcsat.reset_index(inplace=True)
count = postcsat['count']
satlikes['count'] = count

# Make bar plots of average plays per hour each day
sunlikesplot = px.bar(sunlikes, x="hour posted", y="likes", title="Sunday", hover_data=['count'])
# sunlikesplot.show()

monlikesplot = px.bar(monlikes, x="hour posted", y="likes", title="Monday", hover_data=['count'])
# monlikesplot.show()

tueslikesplot = px.bar(tueslikes, x="hour posted", y="likes", title="Tuesday", hover_data=['count'])
# tueslikesplot.show()

wedsplaysplot = px.bar(wedslikes, x="hour posted", y="likes", title="Wednesday", hover_data=['count'])
# wedslikesplot.show()

thursplaysplot = px.bar(thurslikes, x="hour posted", y="likes", title="Thursday", hover_data=['count'])
# thurslikesplot.show()

friplaysplot = px.bar(frilikes, x="hour posted", y="likes", title="Friday", hover_data=['count'])
# frilikesplot.show()

satplaysplot = px.bar(satlikes, x="hour posted", y="likes", title='Saturday', hover_data=['count'])
# satlikesplot.show()

# Show all charts in streamlit
# st.plotly_chart(dailylikesplot, use_container_width=True)
# st.plotly_chart(sunlikesplot, use_container_width=True)
# st.plotly_chart(monlikesplot, use_container_width=True)
# st.plotly_chart(tueslikesplot, use_container_width=True)
# st.plotly_chart(wedslikesplot, use_container_width=True)
# st.plotly_chart(thurslikesplot, use_container_width=True)
# st.plotly_chart(frilikesplot, use_container_width=True)
# st.plotly_chart(satlikesplot, use_container_width=True)
# st.plotly_chart(commentsplot, use_container_width=True)

Reelsbutton = st.button("Reels")

Photosbutton = st.button("Photos")

if Reelsbutton:
        # streamlit Title
        st.markdown("<h1 style='text-align: center; color: Black;'>Instagram Dashboard</h1>", unsafe_allow_html=True)

        # total statistics: likes, plays, average enjoyment, comments

        # Reels Data Label
        st.markdown("<h2 style='text-align: center; color: black;'>Reels Data</h2>", unsafe_allow_html=True)
        # total reel statistics: likes, plays, average enjoyment, comment

        # lifetime statistics per post using a drop down menu: likes, plays, enjoyment, comments
        st.markdown("<h4 style='text-align: left; color: black;'>Statistics Per Post</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Statistics per post',
                ('Likes', 'Plays', 'Enjoyment', 'Comments'),
                label_visibility="hidden")
        if option == 'Likes':
                st.plotly_chart(likesplot, use_container_width=True)
        if option == 'Plays':
                st.plotly_chart(playsplot, use_container_width=True)
        if option == 'Enjoyment':
                st.plotly_chart(enjoyplot, use_container_width=True)
        if option == 'Comments':
                st.plotly_chart(commentsplot, use_container_width=True)

        # Daily chart
        st.markdown("<h4 style='text-align: left; color: black;'>Daily Plays</h4>", unsafe_allow_html=True)

        st.plotly_chart(dailyplaysplot, use_container_width=True)

        # Hourly plays per day using a drop down menu: monday-sunday
        st.markdown("<h4 style='text-align: left; color: black;'>Average Hourly Plays</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Average Hourly Plays',
                ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                label_visibility="hidden")
        if option == 'Monday':
                st.plotly_chart(monplaysplot, use_container_width=True)
        elif option == 'Tuesday':
                st.plotly_chart(tuesplaysplot, use_container_width=True)
        elif option == 'Wednesday':
                st.plotly_chart(wedsplaysplot, use_container_width=True)
        elif option == 'Thursday':
                st.plotly_chart(thursplaysplot, use_container_width=True)
        elif option == 'Friday':
                st.plotly_chart(friplaysplot, use_container_width=True)
        elif option == 'Saturday':
                st.plotly_chart(satplaysplot, use_container_width=True)
        elif option == 'Sunday':
                st.plotly_chart(sunplaysplot, use_container_width=True)

if Photosbutton:
        # streamlit Title
        st.markdown("<h1 style='text-align: center; color: Black;'>Instagram Dashboard</h1>", unsafe_allow_html=True)

        # total statistics: likes, comments

        # Photos Data Label
        st.markdown("<h2 style='text-align: center; color: black;'>Photos Data</h2>", unsafe_allow_html=True)
        # total reel statistics: likes, comment

        # lifetime statistics per post using a drop down menu: likes, comments
        st.markdown("<h4 style='text-align: left; color: black;'>Statistics Per Post</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Statistics per post',
                ('Likes', 'Comments'),
                label_visibility="hidden")
        if option == 'Likes':
                st.plotly_chart(likesplot, use_container_width=True)
        if option == 'Comments':
                st.plotly_chart(commentsplot, use_container_width=True)

        # Daily chart
        st.markdown("<h4 style='text-align: left; color: black;'>Daily Likes</h4>", unsafe_allow_html=True)

        st.plotly_chart(dailylikesplot, use_container_width=True)

        # Hourly likes per day using a drop down menu: monday-sunday
        st.markdown("<h4 style='text-align: left; color: black;'>Average Hourly Likes</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Average Hourly Likes',
                ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                label_visibility="hidden")
        if option == 'Monday':
                st.plotly_chart(monlikesplot, use_container_width=True)
        elif option == 'Tuesday':
                st.plotly_chart(tueslikesplot, use_container_width=True)
        elif option == 'Wednesday':
                st.plotly_chart(wedslikesplot, use_container_width=True)
        elif option == 'Thursday':
                st.plotly_chart(thurslikesplot, use_container_width=True)
        elif option == 'Friday':
                st.plotly_chart(frilikesplot, use_container_width=True)
        elif option == 'Saturday':
                st.plotly_chart(satlikesplot, use_container_width=True)
        elif option == 'Sunday':
                st.plotly_chart(sunlikesplot, use_container_width=True)


