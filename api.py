
import requests
import locale

total_questions = 0
bad_searches = []
empty_entities = []

def query_wikipedia(entity):
    """
    Queries Wikipedia for an articke about 'entity'.
    Returns the article's first section of text, including (most importantly)
    the data box on the right.
    """
    print entity + ' -----'
    info = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&titles={0}&rvsection=0&format=json".format(entity))
    data = info.json()
    data_box = data['query']['pages']
    for key, value in data_box.iteritems():
        data_box = value
        break

    try:
        data_box = data_box['revisions'][0]['*']
    except KeyError:
        bad_searches.append(entity)
        return
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


def parse_pipes(value):
    feet_to_meters = 0.3048
    """
    Parses text separated by pipes. Attempts to return the most meaningful data
    possible, prioritizing numbers and order.
    """
    value_list = value.split('|')
    try:
        if value_list[2]=="ft":
	    value_list[1] = int(value_list[1]) * feet_to_meters
            value_list[1] = unicode(value_list[1])
    except IndexError:
        pass
    return_value = None
    for item in value_list:
        try:
            return_value = float(item.replace(',', ''))
            return_value = int(return_value)
        except (ValueError, UnicodeEncodeError):
            pass

        if return_value:
            return return_value


def parse_raw_data(value):
    """The basic parsing performed on all data.
    """
    value_list = value.split('<')
    return value_list[0].strip()


def parse_population(value):
    return prettify_number(value)


def metres(value):
    return "{0}m".format(value)


def parse_elevation(value):
    elevation = prettify_number(value)
    return elevation + 'm'


def parse_answer(raw_answer, question_info):
    parse_function = question_info['parse_function']
    clean_data = parse_raw_data(raw_answer)
    if clean_data:
        answer = parse_function(clean_data)
        if answer and 'unit' in question_info:
            answer = question_info['unit'](answer)

        return answer


def prettify_number(raw_value):
    """Makes a number pretty by (say) adding commas.
    """
    try:
        number = int(raw_value)
    except ValueError:
        return raw_value

    locale.setlocale(locale.LC_ALL, 'en_US')
    raw_number = locale.format("%d", number, grouping=True)
    return raw_number


def print_card(question_data, entity):
    print question_data['question'].format(entity)
    print question_data['answer']


def generate_answers(text, category_info, entity):
    num_entity_questions = 0
    for search_term, question_data in category_info['questions'].iteritems():
        raw_answer = search_text(text, search_term)
        answer = parse_answer(raw_answer, question_data)
        if not answer:
            continue
        question_data['answer'] = answer
        print_card(question_data, entity)
        num_entity_questions += 1
    return num_entity_questions


categories = {
    'people': {
        'file': 'people.txt',
        'questions': {
            'birth_date': {
                'question': 'In what year was {0} born?',
                'parse_function': parse_pipes,
            },
            'death_date': {
                'question': 'In what year did {0} die?',
                'parse_function': parse_pipes,
            },
        },
    },

    'cities': {
        'file': 'cities.txt',
        'questions': {
            'population_total': {
                'question': 'What is the population of the city proper of {0} (as of 2015)?',
                'parse_function': parse_population,
            },
            'pop_latest': {
                'question': 'What is the population of the city proper of {0} (as of 2015)?',
                'parse_function': parse_population,
            },
            'elevation_m': {
                'question': 'What is the elevation (in metres) of the city proper of {0} (as of 2015)?',
                'parse_function': parse_elevation,
            },
        },
    },

    'freestanding_structures': {
        'file': 'freestanding_structures.csv',
        'questions': {
            'architectural': {
                'other_names': ['architechtural'],
                'question': 'What is the architectural height (in metres) of the {0}?',
                'parse_function': parse_pipes,
                'unit': metres,
            },
            'architechtural': {
                'question': 'What is the architectural height (in metres) of the {0}?',
                'parse_function': parse_pipes,
                'unit': metres,
            },
            'antenna_spire': {
                'question': 'What is the antenna spire height (in metres) of the {0}?',
                'parse_function': parse_pipes,
                'unit': metres,
            },
        },
    },
}


answers = {}

for category, category_info in categories.iteritems():
    with open(category_info['file'], 'r') as f:
        entities = f.readlines()

    for entity in entities:
        entity = entity.strip()
        # Use only the first comma-separated chunk of the entity to search 
        searchable_entity = entity.split(',')[0].strip()

        text = query_wikipedia(searchable_entity)
        if not text:
            continue
        num_entity_questions = generate_answers(text, category_info, entity)
        total_questions += num_entity_questions

        if not num_entity_questions:
            empty_entities.append(entity)


print '\nBad searches: --------------'
for search in bad_searches:
    print search

print '\nEmpty entities: --------------'
for entity in empty_entities:
    print entity

print '\nNumber of questions:'
print total_questions



