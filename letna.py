#%%
import requests
from key import apikey
import json
import time
from nested_dict import nested_dict

#%%
letna = { # brano odsud: https://developer.o2.cz/portal/resources/zsj.geojson, otevrete napr. v QGISu
    '305961': 'škvára', # škvára a park před Kachlíkem
    '130320': 'sady', # Stalin, sady a půlka přiléhající Vltavy
}

age = {
    '1': '8-18', 
    '2': '19-25', 
    '3': '26-35', 
    '4': '36-55',
    '5': '56+',
}

gender = {
    '1': 'kluci', 
    '2': 'holky',
}

headers = {
    'Accept': 'application/json',
    'apikey': apikey['key'],
}

#%%
out = nested_dict()
for hour in range(15, 20): # hodiny pro stažení, koncovou hodinu uvádět +1
    for zsj in letna:
        for grp in gender:
            r = requests.get('https://developer.o2.cz/sociodemo/api/gender/' 
            + str(zsj) 
            + '?g=' + grp
            + '&occurenceType=2&hour=' + str(hour), headers=headers)
            if r.status_code == 200:
                out[str(hour)][letna[zsj]][gender[grp]] = int(r.json()['count'])
            else:
                out[str(hour)][letna[zsj]][gender[grp]] = None
        
        for grp in age:
            r = requests.get('https://developer.o2.cz/sociodemo/api/age/' 
            + str(zsj) 
            + '?ageGroup=' + grp
            + '&occurenceType=2&hour=' + str(hour), headers=headers)
            if r.status_code == 200:
                out[str(hour)][letna[zsj]][age[grp]] = int(r.json()['count'])
            else:
                out[str(hour)][letna[zsj]][age[grp]] = None
            
#%%
r = requests.get('https://developer.o2.cz/sociodemo/api/info', headers=headers)
tstamp = r.json()['backendDataFrom']

with open('./sociodemo_' + tstamp + '.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(out.to_dict(), ensure_ascii=False, indent=4))

#%%
# Brno-střed zdraví Prahu 7
r = requests.get('https://developer.o2.cz/mobility/api/transit/550973/500186?uniques=1&fromType=2&toType=2', headers=headers)
ri = requests.get('https://developer.o2.cz/mobility/api/info', headers=headers)

print('Z Brna-střed přijelo do Prahy 7 ' + ri.json()['backendDataFrom'] + ' ' + r.json()['count'] + ' lidí')
