import pandas as pd
import os.path

def save_state(base_name, data):
    df = pd.DataFrame([data])
    df.to_csv(base_name + '/state.csv', index=False)

def load_previous_state(base_name):
    if not os.path.exists(base_name):
        os.mkdir(base_name)
    if (os.path.isfile(base_name + '/state.csv')):
        df = pd.read_csv(base_name + "/state.csv")
        return df.iloc[0].to_dict()
    return {}

def load_process_data_state():
    state = load_previous_state('process_data')
    if(any(state)):
        return int(state['file_index']), int(state['item_index'])
    else:
        return 1, 0

def save_process_data_state(file_index, item_index):
    save_state('process_data', { 'file_index': file_index, 'item_index': item_index})

def load_raw_data_state():
    state = load_previous_state('raw_data')
    if(any(state)):
        return state['after'], int(state['total'])
    else:
        return "", 0

def save_raw_data_state(after, total):
    save_state('raw_data', { 'after': after, 'total': total})

