
import requests
import re

def query_wikipedia(entity):
    info = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&titles={0}&rvsection=0&format=json".format(entity))
    data = info.json()
    data_box = data['query']['pages']
    for key, value in data_box.iteritems():
        data_box = value
        break

    data_box = data_box['revisions'][0]['*']
    return data_box

def search_text(text, term):
    position = text.find(term)
    equals_position = text[position:].find('=')
    end_position = text[position:].find('\n')

    value = text[position + equals_position + 1 : position + end_position]
    value = value.strip()
    return value


def parse_date(value):
    value_list = value.split('|')
    for item in value_list:
        try:
            return int(item)
        except (ValueError, UnicodeEncodeError):
            return


def parse_location(value):
    value_list = value.split(',')
    final_value = value_list[0]
    return final_value


search_map = {
    'birth_date': parse_date,
    'death_date': parse_date,
    'residence': parse_location,
}

def search_terms(text, search):
    for term in search:
        print '-'*30
        print term
        value = search_text(text, term)
        #print value
        parse_function = search_map[term]
        print parse_function(value)


#people = None

search = ['birth_date', 'death_date', 'residence']

with open('people.txt', 'r') as f:
    people = f.readlines()

for person in people:
    person = person.strip()

    print person
    text = query_wikipedia(person)
    search_terms(text, search)

