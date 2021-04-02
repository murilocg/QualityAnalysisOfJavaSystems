
import subprocess
import pandas as pd
import os
import shutil
from datetime import datetime
from git import Repo
import state_manager

def formatMetrics(metrics):
    return {
        "CBO": metrics['cbo'],
        "WMC": metrics['wmc'],
        "DIT": metrics['dit'],
        "LOC": metrics['loc']
    }

def clear(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.remove('class.csv')
    os.remove('method.csv')

def process_metrics(path, url):
    subprocess.call(['git', 'clone', url + ".git", path])
    subprocess.call(['java', '-jar', './ck/target/ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar', path, 'false', '0', 'False' ])
    ck_metrics = pd.read_csv("class.csv", usecols = ["cbo", "wmc", "dit", "loc"])
    metrics = ck_metrics.median()
    return formatMetrics(metrics)

def process_repositories(df, item_index, max_itens):
    repos = []
    for ii in range(item_index, max_itens):
        r = df.iloc[ii].to_dict()
        print("#---------- Processing repository " + str(ii) + " ---------#")
        path = "repositories/" + r['Nome']
        try:
            r.update(process_metrics(path, r['Url']))
            repos.append(r)
        except (Exception) as e:
            print("[ERROR] Calculating metrics for repository:" + r['Nome'])
            print(e)
            return repos, ii
        finally:
            clear(path)
    return repos, max_itens

def write_process_data(repos, fi, ii):
    df = pd.DataFrame(repos)
    df.to_csv('process_data/'+ str(fi) + '.csv', index=False)
    state_manager.save_process_data_state(fi, ii)

def load_items(item_index):
    items = []
    if item_index > 0:
        df = pd.read_csv('process_data/' + str(fi) + '.csv')
        items = df.T.to_dict().values()
    return items

def process_files(file_index, item_index, max_files, max_itens):
    
    fi = file_index
    ii = item_index
    items = load_items(ii)

    while(fi <= max_files):
        df = pd.read_csv('raw_data/' + str(fi) + '.csv')
        repos, ii, sucess = process_repositories(df, ii, max_itens)
        items = items + repos
        write_process_data(items, fi, ii)
        if ii == max_itens:
            items = []
            ii= 0
            fi+=1
        else:
            break

def start(max_files, max_itens):
    file_index, item_index = state_manager.load_process_data_state()
    
    if file_index == max_files and item_index == max_itens:
        print("Skipping Step: Process Data")
    elif item_index == max_itens:
        process_files(file_index + 1, 0, max_files, max_itens)
    else:
        process_files(file_index, item_index, max_files, max_itens)