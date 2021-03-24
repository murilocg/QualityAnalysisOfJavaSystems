from query import Query
import metrics
import pandas as pd

def main(pageSize, limit, token):
    print("Starting script")
    query = Query(pageSize, token)
    arr = []
    print("Searching repositories on Github")
    while len(arr) < limit and query.hasNext():
        arr = arr + query.next()
    
    print("Processing Metrics for each repository")
    repos = metrics.proccess(arr)

    print("Exporting data")
    df = pd.DataFrame([r for r in repos])
    df.to_csv('report.csv', index=False)
    print("Data exported to file report.csv")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--token', metavar='path', required=True, help='Authentication token to Gihtub API')
    parser.add_argument('--pageSize', metavar='path', required=True, help='How many repositories retrieve per query')
    parser.add_argument('--limit', metavar='path', required=True, help='Maximum number of repositories that will be analyzed')
    args = parser.parse_args()
    main(pageSize=int(args.pageSize.strip()), limit=int(args.limit.strip()), token=args.token.strip())