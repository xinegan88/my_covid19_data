import pandas as pd
import chart_functions
from chart_functions import generate_map,generate_bar_chart,county_map

def sort_states(states):
    states = states.sort_values(['date','cases'], ascending = True)
    states.reset_index()
    return states

def recent_dates(states):
    recent_date = states['date'].iloc[-1]
    print()
    print("The most recent data available is from: ",recent_date,"\n")
    states = states[states.date == recent_date]
    return states

def merge_df(pops_df,states):
    pops_df.columns = ['state', 'code', 'population']
    map_df = states.merge(pops_df, on='state')
    return map_df

def calculate_rate(map_df):
    map_df['rate'] = round((100000 * map_df.cases / map_df.population),2)
    return map_df

def usa_data():
    print("Importing most recent data from New York Times...\n")
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    states = recent_dates(sort_states(states))
    print(states.head(),"\n")

    print("Importing population data by state...\n")
    pops_df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")
    pops_df = pops_df.drop('Rank', axis=1)

    print("Aggregating totals...\n")
    map_df = merge_df(pops_df,states)

    print("Sorting by infection rate...\n")
    map_df = calculate_rate(map_df)
    map_df = map_df.sort_values(['rate'], ascending = False)

    recent_date = states['date'].iloc[-1]
    print("Displaying chart of states with the highest infection rate as of ",recent_date,"\n")
    map_df = map_df.reset_index()
    map_df = map_df.drop(['index','date'], axis=1)
    print(map_df.head(10),"\n")

    print("Generating map in browser window...\n")
    print("Be patient...\n")
    generate_map(map_df)

    print("Generating graph in browser window...\n")
    print("Be patient...\n")
    us = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    us = us.drop('deaths', axis = 1)
    us_diff = us[['cases']].diff()
    us = us.join(us_diff, rsuffix='_new')
    us_7day = us[['cases_new']].rolling(7).mean()
    us = us.join(us_7day, rsuffix='_avg')
    us = us.reset_index()
    us = us.drop('index', axis=1)
    generate_bar_chart(us)

def state_data(state_name):
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    state = state_name.title()
    print("Extracting NYT data for ",state_name)
    state = states[states.state == state_name]
    state = state.drop('deaths', axis = 1)
    ny_diff = state[['cases']].diff()
    state = state.join(ny_diff, rsuffix='_new')
    print()

    print("Calculating 7-day average of new cases...\n")
    state_7day = state[['cases_new']].rolling(7).mean()
    state = state.join(state_7day, rsuffix='_avg')
    state = state.reset_index()
    state = state.drop('index', axis=1)

    print("\nGenerating graph in browser window...\n\n Be patient...\n\n")
    generate_bar_chart(state)

def county_data(state):
    state_name = state.title()
    print("COVID-19 Infection Rate in Your State")
    counties = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
    counties = counties[counties.state == state_name]
#counties['fips'].fillna('36061', inplace = True)
#recent_date = counties['date'].iloc[-1]
    print("Searching for Cases by County...\n")
    counties = counties[counties.date == counties['date'].iloc[-1]]
    counties = counties[counties['county'] != "Unknown"]
    counties = counties.sort_values(by=['county']).reset_index()
    counties = counties.drop(['deaths','state'], axis=1)

    print("Retrieving Population Data...\n")
    pop_df = pd.read_csv("co-est2019-alldata.csv", encoding = "cp437")
    pop_df = pop_df[['STNAME','CTYNAME','POPESTIMATE2019']]
    pop_df.columns = ['state','county name','population']
    pop_df = pop_df[pop_df.state == state_name]
    pop_df = pop_df[pop_df['county name'] != state_name]
    pop_df = pop_df.drop(['state'], axis = 1)
    pop_df = pop_df.reset_index()
    pop_df = pop_df.drop(['index'], axis = 1)
#pop_df = pop_df.map(lambda x: x.encode('unicode-escape').decode('utf-8'))
    print(pop_df,"\n")
    pop_df = pop_df.sort_values(by=['county name'])
    pop_df = pop_df.reset_index()

    print("Merging Population Data...\n")
    map_df = pd.concat([counties,pop_df], axis=1)
    map_df = map_df.drop(['index','county name'], axis = 1)
    map_df = calculate_rate(map_df)

    print("Displaying counties with the highest infection rate...\n")
    print(map_df.head())

    print("\nGenerating map in browser window...\n")
    print("Be patient...\n")
    county_map(map_df)
