import csv, datetime, os, pandas
from tools import config
from path import Path


###############################
# VARIABLES

class Data():
    LIKES = "likes"
    COMMENTS = "comments"
    FOLLOWS = "follows"
    UNFOLLOWS = "unfollows"
    ERRORS = "errors"


###############################
# FUNCTIONS

def check_paths():
    data_path = Path(config.data.statistics_folder)
    likes_file = data_path / "likes.csv"
    comments_file = data_path / "comments.csv"
    follows_file = data_path / "follows.csv"
    unfollows_file = data_path / "unfollows.csv"
    errors_file = data_path / "errors.csv"

    if not data_path.exists():
        os.makedirs(data_path)

    if not likes_file.exists():
        with open(likes_file, 'w') as f:
            f.write(",date,amount\n")
    
    if not comments_file.exists():
        with open(comments_file, 'w') as f:
            f.write(",date,amount\n")
    
    if not follows_file.exists():
        with open(follows_file, 'w') as f:
            f.write(",date,amount\n")

    if not unfollows_file.exists():
        with open(unfollows_file, 'w') as f:
            f.write(",date,amount\n")
    
    if not errors_file.exists():
        with open(errors_file, 'w') as f:
            f.write(",date,message\n")


def get(data_type=Data.LIKES, hours=1):
    check_paths()
    data_path = Path(config.data.statistics_folder)
    filepath = data_path / (data_type + ".csv")
    df = pandas.read_csv(filepath, index_col=0, parse_dates=[1])

    data = 0
    p = datetime.datetime.now() - datetime.timedelta(hours=hours)

    for row in df.itertuples():
        if row.date > p:
            data += row.amount
    return data
    

def update(data_type=Data.LIKES, amount=1, message=""):
    check_paths()
    data_path = Path(config.data.statistics_folder)
    filepath = data_path / (data_type + ".csv")
    df = pandas.read_csv(filepath, index_col=0, parse_dates=[1])

    if data_type == Data.ERRORS:
        df = df.append({"date":datetime.datetime.now(), "message":message}, ignore_index=True)
    else:
        df = df.append({"date":datetime.datetime.now(), "amount":amount}, ignore_index=True)

    df.to_csv(filepath)
