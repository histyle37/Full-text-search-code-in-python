import sys
import json

#get close industries from search keyword
def industry_autocomplete(search):
    max_results = 20
    #read industries from file
    f = open("array.json")
    input_dict = json.load(f)
    #get similarity between keyword and industries, sort by similarity
    data = dict()
    for industry in input_dict:
        data[industry] = get_similarity(industry, search)
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    sorted_data = dict(filter(lambda elem: elem[1] > 0, sorted_data.items()))
    output_dict = [ x for x in sorted_data ]
    #get top close industries
    return output_dict[0: max_results]

#get similarity between two word; orgin, keyword
def get_similarity(origin : str, keyword : str):
    origin = origin.lower()
    keyword = keyword.lower()

    origin_array = origin.split() #split string into a list    
    keyword_array = keyword.split()

    sim = 0
    if origin.startswith(keyword): 
        sim = float('inf')
    else:
        for oid, origin in enumerate(origin_array):
            for kid, keyword in enumerate(keyword_array):
                for charid, x in enumerate(keyword):
                    substring = keyword[:charid+1]
                    if substring is not None:
                        sim += _get_similarity(origin, substring, oid, kid)

    return sim

def _get_similarity(origin : str, keyword : str, oid : int, kid : int):
    similarity = 0
    config = { 'same' : 100, 'starts_with_head' : 10, 'starts_with_sub_head' : 2, 'max_word_count': 6, 'contains': 6 }
    weight = 1.2 ** ((6 - oid) * (6 - kid))
    # weight2 = 1.2 ** (6 - kid)
    # weight = weight1 * weight2
    if origin == keyword:
        similarity = config['same'] * weight
    elif origin.startswith(keyword) :
        similarity = config['starts_with_head'] * weight * origin.count(keyword)
    elif origin.endswith(keyword) :
        similarity = config['starts_with_head'] * weight * origin.count(keyword)
    elif keyword in origin:
        similarity = config['contains'] * weight * origin.count(keyword)
    #contains

    return similarity

print(industry_autocomplete("machi shop"))