from query import Query
import pandas as pd
from datetime import datetime
import os.path

def getMaturidade(dateStr):
    createdAt = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now()
    diff = today - createdAt
    return round(diff.days/365, 2)

def convert(repo):
    return {
        "Nome": repo['name'],
        "Popularidade": repo['stargazers']['totalCount'],
        "Atividade": repo['releases']['totalCount'],
        "Maturidade": getMaturidade(repo['createdAt']),
        "Url": repo['url']
    }

def extract_raw_data(query):
    while query.hasNext():
        try:
            arr = query.next()
            df = pd.DataFrame([convert(r) for r in arr])
            df.to_csv('raw_data/' + str(query.num_pages()) + '.csv', index=False)
        except:
            print('Error searching on Github GraphQL')
            return False
    return True

def start(state, pageSize, limit, token):
    query = Query(pageSize, limit, token)
    
    if (any(state)):
        query.after = state['after']
        query.total = int(state['total'])
    
    if query.hasNext():
        print("Step: Extract Raw Data")
        extract_raw_data(query)
        state = {"after": query.after, "total": str(query.total)}
    else:
        print("Skipping Step: Extract Raw Data")
    return state
