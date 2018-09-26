import json
import os

dct = {}
for _, _, files in os.walk('json'):
    for file in files:
        novel = file[:-5]
        jsn = json.load(open('json/%s'%file, encoding='utf8'))
        for name in jsn:
            if name in dct:
                print(name)
                dct[name].append(novel)
            else:
                dct[name] = [novel]
s = json.dumps(dct, ensure_ascii=False)

with open('output.json', 'w', encoding='utf8') as fout:
    fout.write(s)
