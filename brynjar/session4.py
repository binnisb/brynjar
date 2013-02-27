# -*- coding: utf-8 -*-
import operator
import sys
import datetime
from matplotlib.pylab import plot
def get_commits_for_pythonkurs(start=0,end=100000,users_name=[],skip_names=set()):
    import requests
    from dateutil import parser
    import pandas as pd
    with open("/home/binni/MasterProject/scilifelabpython/Brynjar/secret") as secret:
        password = secret.read().strip()
    AUTH = ("binnisb",password)
    COMMITS_URL =  "https://api.github.com/repos/pythonkurs/{0}/commits"
    REPOS_URL = "https://api.github.com/orgs/pythonkurs/repos"
    if not users_name:
        users = requests.get(REPOS_URL, auth=AUTH)
        users_data = users.json()
        users_name = [user["name"] for user in users_data]
    commit_history = {"committer_name":[], "commit_date":[],"commit_message":[]}
    for i,user in enumerate(users_name[start:end]):
        if user in skip_names:
            print>>sys.stderr, "Skipping {0}, since its in skip_names parameter".format(user)
            continue
        commit_response = requests.get(COMMITS_URL.format(user),auth=AUTH)
        commits = commit_response.json()
        try:
            commits[0]
        except KeyError as ex:
            print>>sys.stderr, "Uninitialized direcotry, Name: {0}, skipped".format(user)
            continue
        for d in commits:
            commit_history["committer_name"].append(user)
            commit_history["commit_message"].append(d["commit"]["message"])
            commit_history["commit_date"].append(parser.parse(d["commit"]["author"]["date"]))
    df = pd.DataFrame(commit_history)
    return df

def get_most_common_day_and_hour(df):
    df["day"] = df.commit_date.apply(lambda x: x.strftime("%A"))
    day = _group_by_key("day",df)
    df["hour"] = df.commit_date.apply(lambda x: x.hour)
    hour = _group_by_key("hour",df)
    return (day,hour)
    
def get_commits_pr_day(df):
    df["date"] = df.commit_date.apply(lambda x: datetime.datetime(x.year, x.month, x.day))
    date = df.groupby("date").groups
    return date

def _group_by_key(column,df):
    groupped = df.groupby(column)
    return max(groupped.groups.iterkeys(),key=(lambda k: len(groupped.groups[k])))

if __name__=="__main__":
    df = get_commits_for_pythonkurs()
    (day,hour) = get_most_common_day_and_hour(df)
    date = get_commits_pr_day(df)
    print day,hour
    plot(sorted(date.keys()), [len(date[x]) for x in sorted(date.keys())] )
