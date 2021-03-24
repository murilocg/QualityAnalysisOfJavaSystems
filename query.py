import requests
import json

queryFormat = """{
  search(type: REPOSITORY, first: $first, query: "language:Java,stars:>100,is:public", after: $after) {
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
  def __init__(self, first, token):
    self.after = ""
    self.first = first
    self.token = token

  def hasNext(self):
      return self.after != "null"

  def next(self):
    if not self.hasNext():
        return []
    data = parseData(executeQuery(self))
    endCursor = data['pageInfo']['endCursor']
    self.after = endCursor if endCursor != 'null' else 'null'
    return data['repositories']