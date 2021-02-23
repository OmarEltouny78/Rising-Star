import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb

list = ['PL', 'Ligue1', 'Bundesliga', 'SerieA',
        'LaLiga', 'UCL', 'UEL', 'NOS', 'Ered', 'Russian']

outfield_list = []

goalies_list = []

url = 'https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/PL/PL2021_Outfield.csv'

for league in list:
    framename = 'df_' + league
    framenamegoal = 'df_' + league + '_goalies'
    players_link = 'https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/' + \
        league + '/' + league + '2021_Outfield.csv'
    framename = pd.read_csv(players_link, index_col=False, sep=',')
    # goalies_link = 'https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/' + \
    #league + '/' + league + '2021_keepers.csv'
    #framenamegoal = pd.read_csv(goalies_link, index_col=False, sep=',')
    outfield_list.append(framename)
    # goalies_list.append(framenamegoal)

st.title('The Rising Star Scout')

st.header('Age distros')

league_dict = {'Premier League': 'PL', 'Ligue1': 'Ligue1', 'Bundesliga': 'Bundesliga',
               'SerieA': 'SerieA', 'LaLiga': 'LaLiga', 'UCL': 'UCL', 'UEL': 'UEL'}

option = st.selectbox('Choose a league', ('Premier League',
                                          'Ligue1', 'Bundesliga', 'SerieA', 'LaLiga', 'UCL', 'UEL'))

for keys, values in league_dict.items():
    if option == keys:
        players_df = pd.read_csv(
            values+'/'+values+'2021_Outfield.csv', index_col=False)
        goalkeepers_df = pd.read_csv(
            values+'/'+values+'2021_keepers.csv', index_col=False)


def convertAge(df):
    Aage = 2021 - df.birth_year
    df['newAge'] = Aage
    return df


def getUNos(df, age):
    df_Uage = df[df.newAge <= age]
    return df_Uage


def removeNull(df, num=0):
    if len(df.index != 0):
        df = df[df.games > num]
    return df


players_df = convertAge(players_df)
#goalkeepers_df = convertAge(goalkeepers_df)

st.subheader('outfield')

st.bar_chart(players_df.newAge.value_counts())

# st.subheader('goalkeepers')

# st.bar_chart(goalkeepers_df.newAge.value_counts())

age = st.number_input('Enter players maximum age')

players_U18_df = getUNos(players_df, age)

num = st.number_input('Enter minimum number of games played')

players_U18_df = removeNull(players_U18_df, num)


def getNames(df):
    stringname = 'Player names:'+'\n'
    for i in df.player:
        stringname += i + ','
    return stringname


names_U18 = getNames(players_U18_df)
st.write(names_U18)

user_input = st.text_input('Enter player name to view profile')


def getSummary(df, name):
    summary = ''
    wtn_player = df[df.player == name]
    summary += ("Player name " +
                wtn_player.player.to_string(index=False) + '\n')
    summary += ("Player nationality " +
                wtn_player.nationality.to_string(index=False) + '\n')
    summary += ("Player position " +
                wtn_player.position.to_string(index=False) + '\n')
    summary += ("Player squad " +
                wtn_player.squad.to_string(index=False) + '\n')
    summary += ("Player age " +
                wtn_player.newAge.to_string(index=False) + '\n')
    summary += ("Player games played " +
                wtn_player.games.to_string(index=False) + '\n')
    summary += ("Player games started " +
                wtn_player.games_starts.to_string(index=False) + '\n')
    summary += ("Player minutes played " +
                wtn_player.minutes.to_string(index=False) + '\n')
    summary += ("Player goals scored " +
                wtn_player.goals.to_string(index=False) + '\n')
    summary += ("Player assists made " +
                wtn_player.assists.to_string(index=False) + '\n')
    return summary


summ = getSummary(players_U18_df, user_input)


if summ != '':
    st.text(summ)


def getPosition(df, pos):
    df_pos = df[df.position == pos]
    return df_pos


def getAttSummary(array):
    summary = ''
    summary += ('Forward Analysis' + '\n')
    for i in range(len(array)):
        if not array[i].empty:
            summary += ("Player name " +
                        array[i].player.to_string(index=False) + '\n')
            summary += ("Player nationality " +
                        array[i].nationality.to_string(index=False) + '\n')
            summary += ("Player squad " +
                        array[i].squad.to_string(index=False) + '\n')
            summary += ("Player age " +
                        array[i].newAge.to_string(index=False) + '\n')
            summary += ("Player games played " +
                        array[i].games.to_string(index=False) + '\n')
            summary += ("Player games started " +
                        array[i].games_starts.to_string(index=False) + '\n')
            summary += ("Player minutes played " +
                        array[i].minutes.to_string(index=False) + '\n')
            summary += ("Player goals scored " +
                        array[i].goals.to_string(index=False) + '\n')
            summary += ("Player assists made " +
                        array[i].assists.to_string(index=False) + '\n')
    return summary


def getMidSummary(array):
    summary = ''
    summary += ('Midfielder Analysis' + '\n')
    for i in range(len(array)):
        if not array[i].empty:
            summary += ("Player name " +
                        array[i].player.to_string(index=False) + '\n')
            summary += ("Player nationality " +
                        array[i].nationality.to_string(index=False) + '\n')
            summary += ("Player squad " +
                        array[i].squad.to_string(index=False) + '\n')
            summary += ("Player age " +
                        array[i].newAge.to_string(index=False) + '\n')
            summary += ("Player games played " +
                        array[i].games.to_string(index=False) + '\n')
            summary += ("Player games started " +
                        array[i].games_starts.to_string(index=False) + '\n')
            summary += ("Player minutes played " +
                        array[i].minutes.to_string(index=False) + '\n')
            summary += ("Player goals scored " +
                        array[i].goals.to_string(index=False) + '\n')
            summary += ("Player assists made " +
                        array[i].assists.to_string(index=False) + '\n')
            summary += ("Player crosses made " +
                        array[i].crosses.to_string(index=False) + '\n')
            summary += ("Player interceptions made " +
                        array[i].interceptions.to_string(index=False) + '\n')
            summary += ("Player tackles won " +
                        array[i].tackles_won.to_string(index=False) + '\n')
    return summary


def getDefSummary(array):
    summary = ''
    summary += ('Defender Analysis' + '\n')
    for i in range(len(array)):
        if not array[i].empty:
            summary += ("Player name " +
                        array[i].player.to_string(index=False) + '\n')
            summary += ("Player nationality " +
                        array[i].nationality.to_string(index=False) + '\n')
            summary += ("Player squad " +
                        array[i].squad.to_string(index=False) + '\n')
            summary += ("Player age " +
                        array[i].newAge.to_string(index=False) + '\n')
            summary += ("Player games played " +
                        array[i].games.to_string(index=False) + '\n')
            summary += ("Player games started " +
                        array[i].games_starts.to_string(index=False) + '\n')
            summary += ("Player minutes played " +
                        array[i].minutes.to_string(index=False) + '\n')
            summary += ("Player assists made " +
                        array[i].assists.to_string(index=False) + '\n')
            summary += ("Player crosses made " +
                        array[i].crosses.to_string(index=False) + '\n')
            summary += ("Player interceptions made " +
                        array[i].interceptions.to_string(index=False) + '\n')
            summary += ("Player tackles won " +
                        array[i].tackles_won.to_string(index=False) + '\n')
    return summary
