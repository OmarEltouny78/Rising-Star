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
url_gol='https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/Bundesliga/Bundesliga2021_Keepers.csv'
for league in list:
    framename = 'df_' + league
    framenamegoal = 'df_' + league + '_goalies'
    players_link = 'https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/' + \
        league + '/' + league + '2021_Outfield.csv'
    framename = pd.read_csv(players_link, index_col=False, sep=',')
    goalies_link = 'https://raw.githubusercontent.com/OmarEltouny78/Rising-Star/main/' +league + '/' + league + '2021_Keepers.csv'
    framenamegoal = pd.read_csv(goalies_link, index_col=False, sep=',')
    outfield_list.append(framename)
    goalies_list.append(framenamegoal)

st.title('The Rising Star Scout')

st.header('Age distros')

league_dict = {'Premier League': 'PL', 'Ligue1': 'Ligue1', 'Bundesliga': 'Bundesliga',
               'SerieA': 'SerieA', 'LaLiga': 'LaLiga', 'UCL': 'UCL', 'UEL': 'UEL','Liga MX':'MX','Eredivisie':'Ered','Liga NOS':'NOS'}

option = st.selectbox('Choose a league', ('Premier League',
                                          'Ligue1', 'Bundesliga', 'SerieA', 'LaLiga', 'UCL', 'UEL','MX','Eredivisie','Liga NOS'))

for keys, values in league_dict.items():
    if option == keys:
        players_df = pd.read_csv(
            values+'/'+values+'2021_Outfield.csv', index_col=False)
        goalkeepers_df=pd.read_csv(values+'/'+values+'2021_Keepers.csv', index_col=False)


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
goalkeepers_df = convertAge(goalkeepers_df)

st.subheader(option +' outfield players')

st.bar_chart(players_df.newAge.value_counts())

st.subheader(option+ ' goalkeepers')

st.bar_chart(goalkeepers_df.newAge.value_counts())

age = st.number_input('Outfield: enter players maximum age')

#age2=st.number_input('Goalies: enter players maximum age')

players_U18_df = getUNos(players_df, age)

#goalies_U18_df=getUNos(goalkeepers_df,age2) 

num = st.number_input('Outfield: enter minimum number of games played')

players_U18_df = removeNull(players_U18_df, num)

#num2 = st.number_input('Goalies: enter minimum number of games played')

#goalies_U18_df = removeNull(goalies_U18_df, num2)

def getNames(df):
    stringname = 'Player names:'+'\n'
    for i in df.player:
        stringname += i + ','
    return stringname


names_U18 = getNames(players_U18_df)
st.write(names_U18)

#names_goalies=getNames(goalies_U18_df)
#st.write(names_goalies)

user_input = st.text_input('Outfield : copy player name into field to view profile')

#user_input1 = st.text_input('Goalies : copy player name into field to view profile')

def getMidSummary(summ,wtn_player):
    summary='';
    summary += ("Player crosses made " +
                        wtn_player.crosses.to_string(index=False) + '\n')
    summary += ("Player interceptions made " +
                        wtn_player.interceptions.to_string(index=False) + '\n')
    summary += ("Player tackles won " +
                        wtn_player.tackles_won.to_string(index=False) + '\n')
    return summary



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
    if 'MF' or 'DF' in wtn_player.position.to_string(index=False):
        summary+=getMidSummary(summary,wtn_player)
    return summary


summ = getSummary(players_U18_df, user_input)

#summ2=getSummary(goalies_U18_df,user_input1)



if summ != '':
    st.text(summ)


def getPosition(df, pos):
    df_pos = df[df.position == pos]
    return df_pos



