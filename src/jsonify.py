import json
filename = 'reg.txt'

dict1 = {}

fields = ['register', 'hex', 'binary', 'decimal']

with open(filename) as fh:
    array = []
    for line in fh:
        description = list(line.strip().split(None,4))
        # print(description)
        
        dict2 = {}
        i = 0
        while i < len(fields):
            dict2[fields[i]] = description[i]
            i = i + 1
        
        array.append(dict2)
    
    # print(array)
    filepath = '../frontend/src/components/reg.json'
    jsonFile = open(filepath,'w')
    json.dump(array,jsonFile,indent=4)
    jsonFile.close()
    