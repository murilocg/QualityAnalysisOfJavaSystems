import requests
import json

queryFormat = """{
  search(type: REPOSITORY, first: $first, query: "language:Java stars:>100", after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        url
        name
        createdAt
        stargazers { totalCount }
        releases{ totalCount } 
      }
    }
  }
}"""

endpoint = "https://api.github.com/graphql"

def executeQuery(params):
    query = createQuery(params.first, params.after)
    request = requests.post(endpoint, json = {'query': query}, headers = {
      'Content-Type': 'application/json',
      'Authorization': 'bearer ' + params.token
    })

    if  request.status_code == 200:
        return request.json()
    raise Exception("A query falhou: {}. {}".format(request.status_code, query))

def parseData(res):
  search = res['data']['search']
  return { "repositories": search['nodes'], "pageInfo": search['pageInfo'] }

def createQuery(first, after):
  q = queryFormat.replace("$after", "null") if after == "" else queryFormat.replace("$after", '"%s"' % after)
  return q.replace("$first", '%d' % first)

class Query:
  def __init__(self, first, limit, token, after = "", total = 0):
    self.first = first
    self.limit = limit
    self.token = token
    self.after = after
    self.total = total

  def hasNext(self):
      return self.total < self.limit

  def num_pages(self):
    return self.total/self.first
  
  def next(self):
    if not self.hasNext():
        return []
    # if self.num_pages() == 5:
    #   raise Exception("Deu ruim!")
    data = parseData(executeQuery(self))
    endCursor = data['pageInfo']['endCursor']
    self.after = endCursor if endCursor != 'null' else 'null'
    repos = data['repositories']
    self.total+=len(repos)
    return repos