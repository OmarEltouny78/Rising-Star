import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb


list=['MLS','Bundesliga','Ligue1','MX','LaLiga','PL','SAF','SerieA','NOS']

outfield_list=[]

goalies_list=[]

for league in list:
    framename='df_'+league
    framenamegoal='df_'+league+'_goalies'
    framename=pd.read_csv(league+'/'+league+'2021_Outfield.csv',index_col=False)
    framenamegoal=pd.read_csv(league+'/'+league+'2021_keepers.csv',index_col=False)
    outfield_list.append(framename)
    goalies_list.append(framenamegoal)
for outfield in outfield_list:
    print(outfield.head())
for goalies in goalies_list:
    print(goalies.head())
"""
df_MLS = pd.read_csv("MLS/MLS2021_Outfield.csv", index_col=False)

df_MLS_goalies = pd.read_csv("MLS/MLS2021_keepers.csv", index_col=False)

df_NOS = pd.read_csv("NOS2021_Outfield.csv", index_col=False)

df_NOS_goalies = pd.read_csv("NOS2021_Keepers.csv", index_col=False)


# print(df_NOS.age.head())


def convertAge(df):
    Aage = 2020-df.birth_year
    df['newAge'] = Aage
    return df


#print(df_NOS.birth_year)


st.write("""
# The rising star scout
""")

df_NOS = convertAge(df_NOS)

df_NOS_goalies=convertAge(df_NOS_goalies)
#print(df_NOS.newAge)

fig,ax=plt.subplots(1,4,figsize=(20,10))

fig.suptitle("Age distros graphs for Liga NOS and MLS")

sb.countplot(data=df_NOS,x='newAge',ax=ax[0])

ax[0].set_title('Liga NOS players')

sb.countplot(data=df_NOS_goalies,x='newAge',ax=ax[1])

ax[1].set_title('Liga NOS goalkeepers')


sb.countplot(data=df_MLS,x='age',ax=ax[2])

ax[2].set_title('MLS players')


sb.countplot(data=df_MLS_goalies,x='age',ax=ax[3])

ax[3].set_title('MLS goalkeepers')

st.pyplot(fig)



def getUNos(df,age):
    df_Uage = df[df.newAge <= age]
    return df_Uage


def getU(df, age):
    df_Uage = df[df.age <= age]
    return df_Uage


def removeNull(df):
    df = df[df.games > 0]
    return df


def getPosition(df, pos):
    df_pos = df[df.position == pos]
    return df_pos


# getting player under the age of 18
df_MLS_U18 = getU(df_MLS, 18)
# No under 18 keepers in MLS
df_MLS_goalies_U18 = getU(df_MLS_goalies, 18)
df_NOS_U18=getUNos(df_NOS,18)
# df_NOS_goalies_U18=getU(df_NOS_goalies)

df_MLS_U18 = removeNull(df_MLS_U18)


# df_MLS_goalies_U18=removeNull(df_MLS_goalies_U18)
df_NOS_U18=removeNull(df_NOS_U18)
# df_NOS_goalies_U18=removeNull(df_NOS_goalies_U18)

# print(df_MLS_U18.position)

#print(df_NOS_U18.head())


def getAttack(df):
    df = df[df.position == 'FW']
    return df


df_MLS_U18_attacker = getAttack(df_MLS_U18)

df_NOS_U18_attacker=getAttack(df_NOS_U18)

# print(df_MLS_U18_attacker.games.value_counts())

#print(df_NOS_U18_attacker.games.value_counts())


def getPlayers(df):
    playerShowOff = []
    df_player1 = df[df.games == 17.0]
    df_player2 = df[df.games == 8.0]
    df_player3 = df[df.games == 7.0]
    playerShowOff.append(df_player1)
    playerShowOff.append(df_player2)
    playerShowOff.append(df_player3)
    return playerShowOff


players = getPlayers(df_MLS_U18_attacker)


def getAttSummary(array):
    summary = ''
    summary += ('Forward Analysis' + '\n')
    for i in range(3):
        summary += ("Player name " + array[i].player.to_string(index=False) + '\n')
        summary += ("Player nationality " + array[i].nationality.to_string(index=False) + '\n')
        summary += ("Player squad " + array[i].squad.to_string(index=False) + '\n')
        summary += ("Player age " + array[i].age.to_string(index=False) + '\n')
        summary += ("Player games played " + array[i].games.to_string(index=False) + '\n')
        summary += ("Player games started " + array[i].games_starts.to_string(index=False) + '\n')
        summary += ("Player minutes played " + array[i].minutes.to_string(index=False) + '\n')
        summary += ("Player goals scored " + array[i].goals.to_string(index=False) + '\n')
        summary += ("Player assists made " + array[i].assists.to_string(index=False) + '\n')
    return summary


#sb.countplot(data=df_MLS_U18_attacker, x='goals_per90')

plt.show()

sb.countplot(data=df_MLS_U18_attacker, x='assists_per90')

#plt.show()

sb.countplot(data=df_MLS_U18_attacker, x='goals_assists_per90')

#plt.show()


p1 = df_MLS_U18_attacker[df_MLS_U18_attacker.goals_assists_per90 == 1.67]

p2 = df_MLS_U18_attacker[df_MLS_U18_attacker.goals_assists_per90 == 0.58]

p3 = df_MLS_U18_attacker[df_MLS_U18_attacker.goals_assists_per90 == 0.42]

p = []

p.append(p1)

p.append(p2)

p.append(p3)

pmessage = getAttSummary(p)

#print(pmessage)

message = getAttSummary(players)

import pywhatkit

"""