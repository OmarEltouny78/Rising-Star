stats = ["player", "nationality", "position", "squad", "age", "birth_year", "games", "games_starts", "minutes", "goals",
         "assists", "pens_made", "pens_att", "cards_yellow", "cards_red", "goals_per90", "assists_per90",
         "goals_assists_per90", "goals_pens_per90", "goals_assists_pens_per90"]
stats3 = ["players_used", "possession", "games", "games_starts", "minutes", "goals", "assists", "pens_made", "pens_att",
          "cards_yellow", "cards_red", "goals_per90", "assists_per90", "goals_assists_per90", "goals_pens_per90",
          "goals_assists_pens_per90"]
# goalkeeping(keepers)
keepers = ["player", "nationality", "position", "squad", "age", "birth_year", "games_gk", "games_starts_gk",
           "minutes_gk", "goals_against_gk", "goals_against_per90_gk", "shots_on_target_against", "saves", "save_pct",
           "wins_gk", "draws_gk", "losses_gk", "clean_sheets", "clean_sheets_pct", "pens_att_gk", "pens_allowed",
           "pens_saved", "pens_missed_gk"]
keepers3 = ["players_used", "games_gk", "games_starts_gk", "minutes_gk", "goals_against_gk", "goals_against_per90_gk",
            "shots_on_target_against", "saves", "save_pct", "wins_gk", "draws_gk", "losses_gk", "clean_sheets",
            "clean_sheets_pct", "pens_att_gk", "pens_allowed", "pens_saved", "pens_missed_gk"]

# shooting(shooting)
shooting = ["player", "nationality", "position", "squad", "age", "birth_year", "minutes_90s", "goals", "pens_made",
            "pens_att", "shots_total", "shots_on_target", "shots_on_target_pct", "shots_total_per90",
            "shots_on_target_per90", "goals_per_shot", "goals_per_shot_on_target"]
shooting2 = ["minutes_90s", "goals", "pens_made", "pens_att", "shots_total", "shots_on_target", "shots_on_target_pct",
             "shots_total_per90", "shots_on_target_per90", "goals_per_shot", "goals_per_shot_on_target"]
shooting3 = ["goals", "pens_made", "pens_att", "shots_total", "shots_on_target", "shots_on_target_pct",
             "shots_total_per90", "shots_on_target_per90", "goals_per_shot", "goals_per_shot_on_target"]

# playingtime(playingtime)
playingtime = ["player", "nationality", "position", "squad", "age", "birth_year", "minutes_90s", "games", "minutes",
               "minutes_per_game", "minutes_pct", "games_starts", "minutes_per_start", "games_subs", "minutes_per_sub",
               "unused_subs", "points_per_match", "on_goals_for", "on_goals_against", "plus_minus", "plus_minus_per90",
               "plus_minus_wowy"]
playingtime2 = ["games", "minutes", "minutes_per_game", "minutes_pct", "games_starts", "minutes_per_start",
                "games_subs", "minutes_per_sub", "unused_subs", "points_per_match", "on_goals_for", "on_goals_against",
                "plus_minus", "plus_minus_per90", "plus_minus_wowy"]

# miscallaneous(misc)
misc = ["player", "nationality", "position", "squad", "age", "birth_year", "minutes_90s", "cards_yellow", "cards_red",
        "cards_yellow_red", "fouls", "fouled", "offsides", "crosses", "interceptions", "tackles_won", "pens_won",
        "pens_conceded", "own_goals"]
misc2 = ["cards_yellow", "cards_red", "cards_yellow_red", "fouls", "fouled", "offsides", "crosses", "interceptions",
         "tackles_won", "pens_won", "pens_conceded", "own_goals"]

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import sys, getopt
import csv


def get_tables(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    player_table = all_tables[1]
    return player_table, team_table


def get_frame(features, player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all('tr')
    for row in rows_player:
        if (row.find('th', {"scope": "row"}) != None):

            for f in features_wanted_player:
                cell = row.find("td", {"data-stat": f})
                a = cell.text.strip().encode()
                text = a.decode("utf-8")
                if (text == ''):
                    text = '0'
                if ((f != 'player') & (f != 'nationality') & (f != 'position') & (f != 'squad') & (f != 'age') & (
                        f != 'birth_year')):
                    text = float(text.replace(',', ''))
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player


def get_frame_team(features, team_table):
    pre_df_squad = dict()
    # Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = features
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if (row.find('th', {"scope": "row"}) != None):
            name = row.find('th', {"data-stat": "squad"}).text.strip().encode().decode("utf-8")
            if 'squad' in pre_df_squad:
                pre_df_squad['squad'].append(name)
            else:
                pre_df_squad['squad'] = [name]
            for f in features_wanted_squad:
                cell = row.find("td", {"data-stat": f})
                a = cell.text.strip().encode()
                text = a.decode("utf-8")
                if (text == ''):
                    text = '0'
                if ((f != 'player') & (f != 'nationality') & (f != 'position') & (f != 'squad') & (f != 'age') & (
                        f != 'birth_year')):
                    text = float(text.replace(',', ''))
                if f in pre_df_squad:
                    pre_df_squad[f].append(text)
                else:
                    pre_df_squad[f] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    return df_squad


def frame_for_category(category, top, end, features):
    url = (top + category + end)
    player_table, team_table = get_tables(url)
    df_player = get_frame(features, player_table)
    return df_player


def frame_for_category_team(category, top, end, features):
    url = (top + category + end)
    player_table, team_table = get_tables(url)
    df_team = get_frame_team(features, team_table)
    return df_team


def get_outfield_data(top, end):
    df1 = frame_for_category('stats', top, end, stats)
    df2 = frame_for_category('shooting', top, end, shooting2)
    df8 = frame_for_category('misc', top, end, misc2)
    df = pd.concat([df1, df2, df8], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def get_keeper_data(top, end):
    df1 = frame_for_category('keepers', top, end, keepers)
    df = pd.concat([df1], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def get_team_data(top, end):
    df1 = frame_for_category_team('stats', top, end, stats3)
    df4 = frame_for_category_team('shooting', top, end, shooting3)
    df10 = frame_for_category_team('misc', top, end, misc2)
    df = pd.concat([df1, df4, df10], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df


import os

folder_names = {'22':'MLS','32': 'NOS', '21': 'SAF', '31': 'MX', '9': 'PL', '13': 'Ligue1', '20': 'Bundesliga', '11': 'SerieA',
                '12': 'LaLiga','37':'Pro','8':'UCL','19':'UEL','24':'Brasilero','23':'Ered','30':'Russian','70':'SaudiLeague'}
reader = {'22':'/Major-League-Soccer-Stats','32': '/Primeira-Liga-Stats', '21': '/Superliga-Argentina-Stats', '31': '/Liga-MX-Stats',
          '9': '/Premier-League-Stats', '13': '/Ligue-1-Stats', '20': '/Bundesliga-Stats', '11': '/Serie-A-Stats',
          '12': '/La-Liga-Stats','37':'/Belgian-First-Division-A-Stats','8':'/Champions-League-Stats','19':'/Europa-League-Stats','24':'/Serie-A-Stats','23':'/Dutch-Eredivisie-Stats','30':'/Russian-Premier-League-Stats','70':'/Saudi-Professional-League-Stats'}
"""
league='/Primeira-Liga-Stats'

df_outfield = get_outfield_data('https://fbref.com/en/comps/32/', '/Primeira-Liga-Stats')

df_outfield.to_csv("NOS/NOS2021_Outfield.csv", index=False)

print(df_outfield.head())

df_goalkeepers = get_keeper_data('https://fbref.com/en/comps/32/', '/Primeira-Liga-Stats')

df_goalkeepers.to_csv("NOS/NOS2021_Keepers.csv", index=False)

print(df_goalkeepers.head())
"""
for keys, values in folder_names.items():
    path = os.path.join(r'C:\Users\omart\PycharmProjects\bussinessStart', values)
    if not os.path.isdir(path):
        os.makedirs(path)

    for k, v in reader.items():
        if keys == k:
            df_outfield = get_outfield_data('https://fbref.com/en/comps/' + k + '/', v)
            df_outfield.to_csv(values + "/" + values + "2021_Outfield.csv", index=False)
            print(df_outfield.head())
            df_goalkeepers = get_keeper_data('https://fbref.com/en/comps/' + k + '/', v)
            df_goalkeepers.to_csv(values + "/" + values + "2021_Keepers.csv", index=False)
            print(df_goalkeepers.head())
