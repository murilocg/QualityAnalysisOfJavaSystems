import process_metrics
import os.path
import extract_raw_data
import pandas as pd
    
def main(pageSize, limit, token):

    extract_raw_data.start(pageSize, limit, token)

    if not os.path.exists('raw_data'):
        raise Exception("There's no Raw Data")
    
    max_page = limit/pageSize
    process_metrics.start(max_page, pageSize)

    if not os.path.exists('process_data'):
        raise Exception("There's no Proccessed Data")

    df = pd.concat([pd.read_csv('process_data/' + str(x) + '.csv') for x in range(1, max_page + 1)])
    df.to_csv('report.csv', index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--token', metavar='path', required=True, help='Authentication token to Gihtub API')
    parser.add_argument('--pageSize', metavar='path', required=True, help='How many repositories retrieve per query')
    parser.add_argument('--limit', metavar='path', required=True, help='Maximum number of repositories that will be analyzed')
    args = parser.parse_args()
    main(pageSize=int(args.pageSize.strip()), limit=int(args.limit.strip()), token=args.token.strip())