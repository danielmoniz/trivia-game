
import requests
import locale


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


def parse_population(value):
    value_list = value.split('<')
    raw_population = value_list[0].strip()

    try:
        population = int(raw_population)
        locale.setlocale(locale.LC_ALL, 'en_US')
        raw_population = locale.format("%d", population, grouping=True)
    except ValueError:
        pass
    if not raw_population:
        return
    return raw_population


search_map = {
    'birth_date': parse_date,
    'death_date': parse_date,
    'population_total': parse_population,
}

def search_terms(text, search):
    answers = {}
    for term in search:
        value = search_text(text, term)
        parse_function = search_map[term]
        answer = parse_function(value)

        if answer is not None:
            answers[term] = answer

    return answers


search_keys = ['birth_date', 'death_date', 'population_total']
questions = {
        'birth_date': 'In what year was {0} born?',
        'death_date': 'In what year did {0} die?',
        'population_total': 'What is the population of the city proper of {0} (as of 2015)?',
        }
answers = {}

files = ('people.txt', 'cities.txt')
files = {
    'people.txt': {
        'search_keys': ['birth_date', 'death_date'],
    },
    'cities.txt': {
        'search_keys': ['population_total'],
    }
}


for file_name, info in files.iteritems():
    with open(file_name, 'r') as f:
        entities = f.readlines()

    for entity in entities:
        entity = entity.strip()

        text = query_wikipedia(entity)
        if text:
            answers[entity] = search_terms(text, info['search_keys'])


for entity, answer_set in answers.iteritems():
    for search, answer in answer_set.iteritems():
        print questions[search].format(entity)
        print answer



