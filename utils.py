import requests
import pandas as pd

def queryMachineRefs(headers):
    query = (
        "{machines(where: {decommissionedAt: {_is_null: true}}) {\n"
        "  name\n"
        "  machineRef\n"
        "  machineId\n"
        "  }\n"
        "}\n"
    )

    response = requests.post('https://api.machinemetrics.com/proxy/graphql', json={'query':query}, headers=headers)
    data = response.json()
    machines_list = data['data']['machines']
    df = pd.DataFrame(machines_list, columns=['name', 'machineRef', 'machineId'])
    
    return df

def getSources(machineId_selected, headers):

    sources_url = f'https://api.machinemetrics.com/temporary-v2/machines/{machineId_selected}/sources'
    response = requests.get(sources_url, headers=headers)

    return response.json()

def identifySources (machineName, sources):

    sourceNames = []

    for source in sources:
        sourceName = source['adapterBinding']['adapterIntegration']['displayName']
        sourceNames.append(sourceName)
    
    # Construct the output string
    if sourceNames:
        sources_str = " and a ".join(sourceNames)
        return f"{machineName} has a {sources_str} adapters"
    else:
        return f"{machineName} has no adapters yet"

def getsourceId(sources, source_name):
    for source in sources:
        if source['adapterBinding']['adapterIntegration']['displayName'] == source_name:
            return source['sourceId']

def getsourceConfig(sourceId):
    #get config from sources json
    sourceConfig = sourceId['adapterBinding']['config']
    return sourceConfig
