import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("MLS2021_Outfield.csv", index_col=False)


# Below 18 goalkeepers do not exist in the MLS, we move on
# df_keeper=pd.read_csv("MLS2021_keepers.csv",index_col=False)

# Getting players age 18 or lower
def getU(df=df, age=23):
    df_Uage = df[df.age <= age]
    return df_Uage


def removeNull(df):
    df = df[df.games > 0]
    return df


def getPosition(df, pos):
    df_pos = df[df.position == pos]
    return df_pos


df_U18 = getU(df, 18)

df_U21 = getU(df, 21)

df_U23 = getU()

df_U18 = removeNull(df_U18)

df_U21 = removeNull(df_U21)

df_U23 = removeNull(df_U23)

x = df_U18.position.unique()

y = df_U18.position.value_counts(sort=True)

plt.bar(x, y)

plt.xlabel("positions")

plt.ylabel("count")

plt.title("Positions of U_18")

plt.show()


def get_df_name(df):
    name = [x for x in globals() if globals()[x] is df][0]
    return name


def barDrawing(df, label):
    name = get_df_name(df)
    x = df[label].unique()
    y = df[label].value_counts(sort=True)
    plt.bar(x, y)
    plt.xlabel(label)
    plt.ylabel("count")
    plt.title(label + " of " + name)
    plt.show()


barDrawing(df_U18, 'position')

barDrawing(df_U18, 'age')

barDrawing(df_U18, 'games_starts')

barDrawing(df_U18, 'games')

barDrawing(df_U18, 'nationality')

barDrawing(df_U18, 'minutes_90s')

base_color = sns.color_palette()[0]


def boxplotting(df, xlabel, ylabel, color):
    sns.boxplot(data=df, x=xlabel, y=ylabel, color=color)
    plt.show()


boxplotting(df_U18, 'position', 'games_start', base_color)

# boxplotting(df_U18, 'position', 'cards_yellow', base_color)

boxplotting(df_U18, 'position', 'games', base_color)
