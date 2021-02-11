import pandas as pd
import numpy as np

df_MLS = pd.read_csv("MLS2021_Outfield.csv", index_col=False)

df_MLS_goalies = pd.read_csv("MLS2021_keepers.csv", index_col=False)

df_NOS = pd.read_csv("NOS2021_Outfield.csv", index_col=False)

df_NOS_goalies = pd.read_csv("NOS2021_Keepers.csv", index_col=False)

#print(df_NOS.age.head())


def convertAge(df):
    for index, row in df.iterrows():
        print(row.age)


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
# df_NOS_U18=getU(df_NOS,18)
# df_NOS_goalies_U18=getU(df_NOS_goalies)

df_MLS_U18 = removeNull(df_MLS_U18)
# df_MLS_goalies_U18=removeNull(df_MLS_goalies_U18)
# df_NOS_U18=removeNull(df_NOS_U18)
# df_NOS_goalies_U18=removeNull(df_NOS_goalies_U18)

#print(df_MLS_U18.position)


def getAttack(df):
    df = df[df.position == 'FW']
    return df


df_MLS_U18_attacker = getAttack(df_MLS_U18)

#print(df_MLS_U18_attacker.games.value_counts())


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


message = getAttSummary(players)

import pywhatkit

pywhatkit.sendwhatmsg('+201019867532',message,15,5)