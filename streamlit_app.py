import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib.pylab as plt 

STATE_LIST = ['AL','AZ','AR','CA','CO','CT','DE','FL','GA','ID','IL','IN','IA','KS','KY','LA','ME',
'MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI',
'SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache
def load_data():
    df = pd.read_csv('weather.csv')
    df = df[df['state'].isin(STATE_LIST)]
    df = df[df['station'] != 'NEW YORK JFK INTL AP']
    df = df[df['station'] != 'NEW YORK LAGUARDIA AP']
    df = df[df['station'] != 'HAYWARD AIR TERMINAL']
    df = df[df['station'] != 'LOS ANGELES INTL AP']
    df = df[df['station'] != 'CONCORD BUCHANAN FLD']
    df = df[df['station'] != 'ISLIP LI MACARTHUR AP']
    df['date'] = df['date'].map(lambda x: datetime.strptime(str(x), '%Y%m%d'))
    df['change'] = df['TMAX'] - df['TMIN']
    df['station'] = df['station'] + ' ' + df['state']
    return df

def map(data):
    option = st.selectbox(
         'Information to Display',
         ('Average Temperature', 'Daily Temperatrue Fluctuation', 'Temperature Fluctuation', 'Snow', 'Percipitation'))
     
    if(option == 'Daily Temperatrue Fluctuation'):
        decision = 'change'
    elif(option == 'Snow'):
        decision = 'SNOW'
    elif(option == 'Percipitation'):
        decision = 'PRCP'
    elif(option == 'Temperature Fluctuation'):
        op2 = st.selectbox(
        'Select time filters',
        ('Annual Averages', 'Seasonal Averages'))
        map = timeSelect(op2, 'avg')
        displayMap(map, 'avg')
        decision = ''
    else:
        decision = 'TAVG'

    if(decision != ''):
        op2 = st.selectbox(
            'Select time filters',
            ('Annual Averages', 'Seasonal Averages', 'Daily Averages'))
        map = timeSelect(op2, decision)
        displayMap(map, decision)

    
def stateData(data):
    state = st.selectbox(
         'State',
         STATE_LIST
    )
    option = st.selectbox(
         'Information to Display',
         ('Average Temperature Per Day','Temperature Change Per Day'))
    graph = data[data['state'] == state]
    graph = graph.groupby('date').mean().reset_index()
    if(option == 'Temperature Change Per Day'):
        graph['change'] = graph['TMAX'] - graph['TMIN']
        decision = 'change'
    else:
        decision = 'TAVG'
    lineplt(graph, decision)

def decision(data):
    maxTemp = st.slider('Maximum Temperature Threshold (F)', 0, 120, 120)
    minTemp = st.slider('Minimum Temperature Threshold (F)', -30, 100, -30)
    daily = st.slider('Daily Temperature Fluctuation', 15, 30, 30)
    dev = st.slider('Annual Temperature Standard Deviation)', 0, 25, 25)
    rainfall = st.slider('Maximum Annual Rainfall (in)', 0, 70, 70)
    snowfall = st.slider('Maximum Annual Snowfall (in)', 0, 90, 90)
    data = data.groupby(['state','date']).mean()
    data = data.groupby('state').agg({'TMAX':'max', 'TMIN':'min', 'SNOW':'sum','PRCP':'sum','change':'mean', 'TAVG':'std'}).reset_index()
    selection = data[data['TMAX'] < maxTemp]
    selection = selection[selection['TMIN'] > minTemp]
    selection = selection[selection['PRCP'] < rainfall]
    selection = selection[selection['SNOW'] < snowfall]
    selection = selection[selection['change'] < daily]
    selection = selection[selection['TAVG'] < dev]
    states = selection['state'].to_string(index=False)
    st.write(states)
    
    
def to_integer(dt_time, containerize):
    if containerize:
        return dt_time.month 
    return 32*dt_time.month + dt_time.day

def showGraph(df, decision):
    columns = st.slider('Columns', 5, 40, 10)
    asc = st.checkbox('Lowest to Highest')
    df = df.groupby('state').mean().reset_index()
    df = df.sort_values(by=decision, ascending = asc).head(columns)
    plot = sns.barplot(data=df, x = df['state'], y = df[decision], palette = sns.color_palette(n_colors=1))
    plt.setp(plot.get_xticklabels(), rotation=90)
    st.pyplot()

def displayMap(map, decision):
    blur = st.checkbox("Blur")
    large = st.checkbox("Large Points")
    add = 0
    if large:
        add = 6
    if blur:
        b = 15
        rad = 20 + add
    else:
        b = 1
        rad = 4 + add
    if(decision == 'avg'):
        minMap = map[['TAVG', 'latitude', 'longitude', 'station', 'state']].groupby(['station', 'latitude','longitude', 'state']).min().reset_index()
        maxMap = map[['TAVG', 'latitude', 'longitude', 'station', 'state']].groupby(['station', 'latitude','longitude', 'state']).max().reset_index()
        map = map[['TAVG', 'latitude', 'longitude', 'station', 'state']].groupby(['station', 'latitude','longitude', 'state']).mean().reset_index()
        map['avg'] = maxMap['TAVG'] - minMap['TAVG']
    
    else:
        map = map[[decision, 'latitude', 'longitude', 'station', 'state']].groupby(['station', 'latitude','longitude', 'state']).mean().reset_index()

    max_amount = float(map[decision].max())
    hmap = folium.Map(location=[40, -100], zoom_start=4)

    hm_wide = HeatMap(list(zip(map['latitude'].values, map['longitude'].values, map[decision].values)),
        min_opacity=0, max_val=max_amount, radius=rad, blur=b, max_zoom=5, control_scale = True)

    hmap.add_child(hm_wide)
    folium_static(hmap)
    graph = st.checkbox('Show Graph')
    if graph:
        showGraph(map, decision)


def timeSelect(op2, decision):    
    if(op2 == 'Daily Averages'):
        slider = st.slider('Date', datetime(2017, 1, 1).date(), datetime(2017, 9, 21).date(), datetime(2017, 1, 1).date())
        map = data[data['date'] == datetime.strptime(str(slider), '%Y-%m-%d')]
        return map.dropna()

    if(op2 == 'Annual Averages'):
        return data.dropna()
        
    if(op2 == 'Seasonal Averages'):
        season = st.selectbox(
            'Season',
            ('Winter', 'Spring', 'Summer', 'Fall'))
        if(season == 'Winter'):
            map = data[data['date'] < datetime.strptime('20170301', '%Y%m%d')]
            return map.dropna()
        elif(season == 'Spring'):
            map = data[data['date'] > datetime.strptime('20170301', '%Y%m%d')]
            map = map[map['date'] < datetime.strptime('20170601', '%Y%m%d')]
            return map.dropna()
        elif(season == 'Summer'):
            map = data[data['date'] > datetime.strptime('20170301', '%Y%m%d')]
            map = map[map['date'] < datetime.strptime('20170901', '%Y%m%d')]
            return map.dropna()
        else:
            st.write("Data Unavailable Displaying Annual Data")
            return data.dropna()
 
def lineplt(data, decision):
    group = st.checkbox('Group By Month')
    std = data[decision].std()
    mean = data[decision].mean()
    data = data.rename(columns={'TAVG':'Average Temperature','change':'Daily Temperature Change'})
    if decision=='TAVG':
        decision = 'Average Temperature'
    else:
        decision = 'Daily Temperature Change'
        
    if(group):
        check = st.checkbox('Show Range of Values')
        if(check):
            data['Month'] = data['date'].map(lambda x: to_integer(x, True))
            data = data.groupby('Month').agg({decision:['min','max']}).reset_index()
            ax = sns.lineplot(x=data['Month'], y=data[decision]['min'], data=data[decision], color='blue')
            ax = sns.lineplot(x=data['Month'], y=data[decision]['max'], data=data[decision], color='blue')
            ax.fill_between(data['Month'], data[decision]['min'], data[decision]['max'], color='blue')
            st.pyplot()
        else:
            data['Month'] = data['date'].map(lambda x: to_integer(x, True))
            data = data.groupby('Month').mean().reset_index()
            sns.barplot(x=data['Month'], y=data[decision], color='blue')
            st.pyplot()
    else:
        tread = st.checkbox('Show Tread Line')
        if tread:
            data['dateInt'] = data['date'].map(lambda x: to_integer(x, False))
            plot = sns.regplot(x=data['dateInt'], y = data[decision], order=1)
            plt.setp(plot.get_xticklabels(), rotation=90)
            st.pyplot()
        else:
            plot = sns.scatterplot(x=data['date'], y = data[decision])
            plt.setp(plot.get_xticklabels(), rotation=90)
            st.pyplot()
    st.write("Average: " + str(mean))
    st.write("Standard Deviation: " + str(std))
    


st.title('US Weather Data')
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

option = st.selectbox(
    'Please Select Exploration Tool',
    ('Please Select One', 'US Weather Data Map', 'Individual State Temperature Analysis', 'State Weather Filters'))
    
if option == 'US Weather Data Map':
    map(data)
elif option == 'Individual State Temperature Analysis':
    stateData(data)
elif option == 'State Weather Filters':
    decision(data)
else:
    st.write("select an option to begin")
