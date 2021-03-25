import process_metrics
import os.path
import extract_raw_data
import pandas as pd
    
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


def main(pageSize, limit, token):

    previous_state = load_previous_state('raw_data')
    next_state = extract_raw_data.start(previous_state, pageSize, limit, token)
    save_state('raw_data', next_state)

    if not os.path.exists('raw_data'):
        raise Exception("There's no Raw Data")
    
    previous_state = load_previous_state('process_data')
    max_page = limit/pageSize
    next_state = process_metrics.start(previous_state, max_page, pageSize)
    save_state('process_data', next_state)

    # if not os.path.exists('process_data'):
    #     raise Exception("There's no Proccessed Data")

    # df = pd.concat([pd.read_csv('process_data/' + str(x) + '.csv') for x in range(1, max_page)])
    # df.to_csv(base_name + 'report.csv', index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--token', metavar='path', required=True, help='Authentication token to Gihtub API')
    parser.add_argument('--pageSize', metavar='path', required=True, help='How many repositories retrieve per query')
    parser.add_argument('--limit', metavar='path', required=True, help='Maximum number of repositories that will be analyzed')
    args = parser.parse_args()
    main(pageSize=int(args.pageSize.strip()), limit=int(args.limit.strip()), token=args.token.strip())