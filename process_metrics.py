
import subprocess
import pandas as pd
import os
import shutil
from datetime import datetime
from git import Repo

def formatMetrics(metrics):
    return {
        "CBO": metrics['cbo'],
        "WMC": metrics['wmc'],
        "DIT": metrics['dit'],
        "LOC": metrics['loc']
    }

def clear(path):
    shutil.rmtree(path)
    os.remove('class.csv')
    os.remove('method.csv')

def process_repositories(df, item_index, max_itens):
    repos = []
    for ii in range(item_index, max_itens):
        r = df.iloc[ii].to_dict()
        path = "repositories/" + r['Nome']
        try:
            subprocess.call(['git', 'clone', r['Url'] + ".git", path])
            subprocess.call(['java', '-jar', './ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar', path, 'false', '0', 'False' ])
            ck_metrics = pd.read_csv("class.csv", usecols = ["cbo", "wmc", "dit", "loc"])
            metrics = ck_metrics.median()
            r.update(formatMetrics(metrics))
            repos.append(r)
        except:
            print("[ERROR] Calculating metrics for repository:" + r['Nome'])
            return repos, i, False
        finally:
            clear(path)

    return repos, max_itens, True

def process_files(file_index, item_index, max_files, max_itens):
    for fi in range(file_index, max_files + 1):
        df = pd.read_csv('raw_data/' + str(fi) + '.csv')
        repos, ii, sucess = process_repositories(df, item_index, max_itens)
        if(sucess):
            df = pd.DataFrame(repos)
            df.to_csv('process_data/'+ str(fi) + '.csv', index=False)
            df = pd.DataFrame([{"file_index": fi, "item_index": ii}])
            df.to_csv('process_data/state.csv', index=False)
            item_index = 0
        else:
            return fi, ii
    return max_files, max_itens

def start(state, max_files, max_itens):
    file_index = 1
    item_index = 0

    if (any(state)):
        file_index = int(state['file_index'])
        item_index = int(state['item_index'])
    
    if (not (file_index == max_files and item_index == max_itens)):
        print("Step: Process Data")
        fi, ii = process_files(file_index, item_index, max_files, max_itens)
        state = {"file_index": fi, "item_index": ii}
    else:
        print("Skipping Step: Process Data")
    return state

