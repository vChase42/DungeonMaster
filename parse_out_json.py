import json
import re

def getDict(string: str):
    matches = re.findall(r'\{.*?\}', string)
    return  json.loads(matches[0])