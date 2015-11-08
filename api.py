
import requests
import re

info = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&titles=Albert%20Einstein&rvsection=0&format=json")
data = info.json()
data_box = data['query']['pages']['736']['revisions'][0]['*']

search = ['birth_date', 'death_date', 'residence']

def search_text(text, term):
    position = data_box.find(term)
    equals_position = data_box[position:].find('=')
    end_position = data_box[position:].find('\n')

    value = data_box[position + equals_position + 1 : position + end_position]
    value = value.strip()
    return value


def parse_date(value):
    value_list = value.split('|')
    final_value = value_list[2]
    return final_value


def parse_location(value):
    value_list = value.split(',')
    final_value = value_list[0]
    return final_value


search_map = {
    'birth_date': parse_date,
    'death_date': parse_date,
    'residence': parse_location,
}

for term in search:
    print '-'*30
    print term
    value = search_text(data_box, term)
    print value
    parse_function = search_map[term]
    print parse_function(value)

