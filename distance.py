import numpy as np
import pandas as pd
from math import sqrt, hypot

import csv_calculations as cc


# CALCULATE DISTANCE BETWEEN PLAYERS IN PIXELS USING THE EUCLIDEAN DISTANCE
def euclidean_distance_pixels(df2):
    x2_x1 = []
    y2_y1 = []

    for i in range(df2.shape[0]):
        x2_x1.append([df2['x'].loc[i] - df2['x'].loc[j] for j in range(df2.shape[0])])
        y2_y1.append([df2['y'].loc[i] - df2['y'].loc[j] for j in range(df2.shape[0])])

    # basically x2-x1 and y2-y1
    x2_x1 = pd.DataFrame(x2_x1)
    y2_y1 = pd.DataFrame(y2_y1)

    df_player_distance_ = []
    for i in range(df2.shape[0]):
        df_player_distance_.append(
            [sqrt(pow(x2_x1.iloc[i][j], 2) + pow(y2_y1.iloc[i][j], 2)) for j in range(df2.shape[0])]
        )

    df_player_distance_ = pd.DataFrame(df_player_distance_)
    df_player_distance_ = df_player_distance_.astype(int)
    return df_player_distance_


# CALCULATE DISTANCE BETWEEN PLAYERS IN METERS USING THE EUCLIDEAN DISTANCE
def euclidean_distance_meters(df3, distance_pixel):
    distance_meters = []

    for i in range(df3.shape[0]):
        distance_meters.append(
            [(df3['DC'].loc[i] + df3['DC'].loc[j]) * distance_pixel.iloc[i][j] / (df3['x'].loc[i] + df3['x'].loc[j])
             for j in range(df3.shape[0])]
        )

    distance_meters = pd.DataFrame(distance_meters)
    distance_meters = distance_meters
    distance_meters += distance_meters.mean()

    return distance_meters


# CALCULATE THE DISTANCE EACH PLAYER HAS FROM THE CAMERA RECORDING HIM
# REQUIRES focal length, height of each player, image height in pixels, and sensor height in mm
def players_from_camera_meters(df4):
    df4['CM'] = pd.DataFrame(np.random.randint(175, 190, size=(df4.shape[0], 1)))
    df4.loc[df4['h'] > df4['h'].mean() * 2, 'CM'] = 5000  # goalpost
    f_mm = 35
    image_height_px = 720
    sensor_height_mm = 44.3

    # I don't know what I am doing, I really don't
    df4.loc[df4['h'] * .8 > df4['w'], 'DC'] = \
        (f_mm * df4['CM'] * 10 * image_height_px) / ((df4['h'] + df4['w']) * sensor_height_mm)

    df4.loc[df4['h'] * .8 <= df4['w'], 'DC'] = \
        (f_mm * df4['CM'] * 10 * image_height_px) / ((df4['h'] * 0.4 + df4['w'] * 0.6) * sensor_height_mm)

    df4['DC'] = df4['DC'] / 1000
    df4['DC'] = df4['DC'].astype(int)

    return df4


# CALCULATING IF THE RED TEAM IS ON THE OFFENSE OR ON DEFENSE
def calculate_offense_defense(df5):
    possession_changed = [[0, 'GAME STARTED']]

    df_center = df5[(df5['h'] > df5['h'].mean() * 2)]
    df_center = df_center.drop(['ID', 'y', 'w', 'h'], axis=1)

    df_center.loc[df_center['x'] < 350, 'D/O'] = 'DEFENSE'
    df_center.loc[df_center['x'] > 700, 'D/O'] = 'OFFENSE'
    df_center['D/O'] = df_center['D/O'].replace(np.nan, 'JUST PLAYING')
    df_center = df_center.dropna()

    for i in range(df_center.shape[0] - 1):
        if df_center.iloc[i]['D/O'] != df_center.iloc[i + 1]['D/O']:
            possession_changed.append([i, df_center.iloc[i + 1]['D/O']])
    possession_changed = pd.DataFrame(possession_changed)

    return possession_changed


# CALCULATING RUNNING DISTANCE FOR EACH PLAYER
def calculate_running_distance_meters(df6):
    df6.drop(df6[df6['h'] > df6['h'].mean() * 2].index, inplace=True)  # dropping the center of the football field
    df_player_location = df6.drop(['Frame', 'x', 'y', 'w', 'h', 'CM'], axis=1)

    running_distance = pd.DataFrame()
    running_distance['x'] = df_player_location.groupby('ID')['DC'].sum() / 100

    running_distance['x'] = running_distance['x'].astype(int)

    # FIXME VALUE NUMBER HAS TO BE ACCORDING TO THE VIDEO LENGTH I GUESS
    # FIXME REPLACE THE 100 - 200 WITH MINUTES * 0.1 * 200 PROBABLY
    running_distance = running_distance.drop(running_distance[running_distance['x'] < 100].index)
    return running_distance


def manager(df):
    df = cc.read_and_clean(df)
    od_timestamps = calculate_offense_defense(df)
    return od_timestamps


# CALLS OUT ALL THE FUNCTIONS ABOVE
def manager_2(df, frame):
    df_ = df = cc.read_and_clean(df)
    od_timestamps = calculate_offense_defense(df)

    df = df[df['Frame'] == frame]
    df = df.reset_index(drop=True)
    euclidean_px = euclidean_distance_pixels(df)  # distance between players pixels

    df = players_from_camera_meters(df)
    df_ = players_from_camera_meters(df_)

    euclidean_m = euclidean_distance_meters(df, euclidean_px)  # distance between players meters
    df_running_distance = calculate_running_distance_meters(df_)
    df_running_distance = df_running_distance['x'].to_list()

    return od_timestamps, df_running_distance, euclidean_m

# if __name__ == '__main__':
#     desired_width = 320
#     pd.set_option('display.width', desired_width)
#     np.set_printoptions(linewidth=desired_width)
#     pd.set_option('display.max_columns', 23)
#     manager('player_detection/runs/track/exp/Tactical View- Pixellot C Coaching.txt', 46)
