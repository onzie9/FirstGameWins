import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import math
pd.set_option('display.max_columns', None)


def theoretical_min_day(d: int, day_1_games: int) -> list:
    d_list = [2,4,6]
    d_list = [x*day_1_games for x in d_list]
    for i in range(3,d):
        d_list.append(d_list[i-1] + 2*d_list[i-3])
    return [day_1_games, max(d_list)]


def theoretical_min(num_teams: int, num_days: int) -> int:
    teams = 0
    day_1_games = 1
    while teams < num_teams:
        teams = theoretical_min_day(num_days, day_1_games)[1]
        day_1_games += 1
    return theoretical_min_day(num_days, day_1_games)[0]


# Task 1: Gather data.
no_date_url = "https://www.hockey-reference.com/leagues/NHL_{season}_games.html#games"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

dates = np.linspace(2000, 2023, 24)
season_first_loses = {}

for d in dates:
    d = str(d)[:-2]
    url = no_date_url.format(season = d)
    print(url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    games_section = soup.find("tbody"
                            )

    try:
        games = games_section.find_all('tr'
                            )
    except AttributeError:
        pass

    columns = ['game_date',
               'home_team',
               'visitor_team',
               'home_goals',
               'visitor_goals']

    data = []

    for i in range(1,len(games)):
        game_date = games[i].find('th', {'data-stat':'date_game'})
        visitor_team = games[i].find('td', {'data-stat': 'visitor_team_name'})
        visitor_goals = games[i].find('td', {'data-stat': 'visitor_goals'})
        home_team = games[i].find('td', {'data-stat': 'home_team_name'})
        home_goals = games[i].find('td', {'data-stat': 'home_goals'})
        data.append([game_date.a.text,
                     home_team.a.text,
                     visitor_team.a.text,
                     visitor_goals.text,
                     home_goals.text])

    df = pd.DataFrame(columns=columns, data=data)

    df['game_date'] = pd.to_datetime(df['game_date'])
    df['home_team'] = df['home_team'].astype(str)
    df['visitor_team'] = df['visitor_team'].astype(str)
    df['winning_team'] = np.where(df['home_goals'] > df['visitor_goals'], df['home_team'], df['visitor_team'])

    df.sort_values(by='game_date', inplace=True, ascending=True)

    # Task 2: How many days does it take before all teams play their first games?
    list_of_teams = df['home_team'].unique()

    first_play_date = []
    won_first_game = 0
    for team in list_of_teams:
        #df_team = df[(df['home_team']==team | df['visitor_team']==team) & df['winning_team']==team]
        df_team = df[(df['home_team'] == team) | (df['visitor_team'] == team)]
        first_game = df_team['game_date'].min()
        first_play_date.append(first_game)
        win_or_lose = df_team[df_team['game_date']==first_game]['winning_team'].values

        if win_or_lose == team:
            won_first_game += 1

    opening_day = min(first_play_date)
    all_teams_played = max(first_play_date)

    days_for_all_teams_to_play = (all_teams_played - opening_day).days + 1

    season_first_loses[d] = [days_for_all_teams_to_play,
                             won_first_game,
                             len(list_of_teams) - won_first_game,
                             len(list_of_teams),
                             d
                             ]

# Task 3: How many teams lost their first games? Won their first games?
# Completed under task 2 conveniently.

# Task 4: How close was that to the minimum/maximum?
# For each season, the theoretical maximum number of first game wins is n/k or floor(n/k) + 1 with k does not divide n
# for n as the number of teams, and k as the number of days it takes for them all to play a game.

# Task 5: What season was the closest to the minimum/maximum?

cols = ['days_to_play', 'first_game_wins', 'first_game_losses', 'num_teams', 'season']
seasons_df = pd.DataFrame(columns=cols,
                          data=[season_first_loses[d] for d in season_first_loses.keys()]
                          )

seasons_df['theoretical_min'] = seasons_df.apply(lambda x: theoretical_min(x['num_teams'], x['days_to_play']), axis=1)

seasons_df['reality_ratio'] = seasons_df['theoretical_min']/seasons_df['first_game_losses']

seasons_df.sort_values(by='reality_ratio', ascending=False, inplace=True)
print(seasons_df.iloc[0])

seasons_df.to_clipboard()