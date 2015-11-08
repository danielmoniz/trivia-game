
import requests


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
            pass
    return


search_map = {
    'birth_date': parse_date,
    'death_date': parse_date,
}

def search_terms(text, search):
    answers = {}
    for term in search:
        value = search_text(text, term)
        #print value
        parse_function = search_map[term]
        answer = parse_function(value)

        if answer is not None:
            answers[term] = answer

    return answers


search = ['birth_date', 'death_date']
questions = {
        'birth_date': 'In what year was {0} born?',
        'death_date': 'In what year did {0} die?',
        }
answers = {}

with open('people.txt', 'r') as f:
    people = f.readlines()

for person in people:
    person = person.strip()

    text = query_wikipedia(person)
    answers[person] = search_terms(text, search)

print answers

for entity, answers in answers.iteritems():
    for search, answer in answers.iteritems():
        print questions[search].format(entity)
        print answer



