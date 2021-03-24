
import subprocess
import pandas as pd
import os
import shutil
from datetime import datetime
from git import Repo

def cloneRepository(url, name = ""):
    path = os.getcwd() + "/" + name
    Repo.clone_from(url, path)

def getMaturidade(dateStr):
    createdAt = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now()
    diff = today - createdAt
    return round(diff.days/365, 2)

def mapRepo(repo, metrics):
    return {
        "Nome": repo['name'],
        "Popularidade": repo['stargazers']['totalCount'],
        "Atividade": repo['releases']['totalCount'],
        "Maturidade": getMaturidade(repo['createdAt']),
        "CBO": metrics['cbo'],
        "WMC": metrics['wmc'],
        "DIT": metrics['dit'],
        "LOC": metrics['loc'],
        "Url": repo['url']
    }

def proccess_repo(repo, path):
    cloneRepository(repo['url'], path)
    subprocess.call(['java', '-jar', './ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar', path, 'true', '0', 'False'])
    ck_metrics = pd.read_csv("class.csv", usecols = ["cbo", "wmc", "dit", "loc"])
    median = ck_metrics.median()
    return mapRepo(repo, median)

def clear(path):
    shutil.rmtree(path)
    os.remove('class.csv')
    os.remove('method.csv')

def proccess(repos):
    data = []
    for r in repos:
        print("Metrics for repository:" + r['name'])
        path = "repositories/" + r['name']
        data.append(proccess_repo(r, path))
        clear(path)
    return data