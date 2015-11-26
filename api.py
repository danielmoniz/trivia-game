
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
    """
    Find the value of a given key in Wikipedia text.
    Does this by counting characters until key is found, then grabbing data 
    after the equals and cleaning up.
    """
    term_position = text.find(term)
    equals_position = text[term_position:].find('=')
    end_position = text[term_position:].find('\n')

    value = text[term_position + equals_position + 1 : term_position + end_position]
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


def parse_large_number(raw_value):
    try:
        population = int(raw_value)
    except ValueError:
        return raw_value

    locale.setlocale(locale.LC_ALL, 'en_US')
    raw_population = locale.format("%d", population, grouping=True)
    return raw_population


def parse_raw_data(value):
    value_list = value.split('<')
    return value_list[0].strip()


def parse_population(value):
    return parse_large_number(value)


def parse_elevation(value):
    elevation = parse_large_number(value)
    return elevation + 'm'


def search_terms(text, search):
    answers = {}
    for term in search:
        value = search_text(text, term)
        parse_function = search_map[term]
        clean_data = parse_raw_data(value)
        if clean_data:
            answer = parse_function(clean_data)

            if answer is not None:
                answers[term] = answer

    return answers


questions = {
        'birth_date': 'In what year was {0} born?',
        'death_date': 'In what year did {0} die?',
        'population_total': 'What is the population of the city proper of {0} (as of 2015)?',
        'elevation_m': 'What is the elevation (in metres) of the city proper of {0} (as of 2015)?',
        }

files = {
    'people.txt': {
        'search_keys': ['birth_date', 'death_date'],
    },
    'cities.txt': {
        'search_keys': ['population_total', 'elevation_m'],
    }
}

search_map = {
    'birth_date': parse_date,
    'death_date': parse_date,
    'population_total': parse_population,
    'elevation_m': parse_elevation,
}

answers = {}


for file_name, info in files.iteritems():
    with open(file_name, 'r') as f:
        entities = f.readlines()

    for entity in entities:
        entity = entity.strip()
        searchable_entity = entity.split(',')[0].strip()

        text = query_wikipedia(searchable_entity)
        if text:
            answers[entity] = search_terms(text, info['search_keys'])


print answers


for entity, answer_set in answers.iteritems():
    for search, answer in answer_set.iteritems():
        print questions[search].format(entity)
        print answer



