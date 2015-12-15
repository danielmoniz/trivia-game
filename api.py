
import requests
import locale
import re

import datetime
import dateparser

import questions
import date

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
    Does this by counting characters until key is found, then narrowing down
    the relevant data and cleaning up.
    """
    term_position = text.find(term)
    equals_position = text[term_position:].find('=')
    end_position = text[term_position:].find('\n')

    value = text[term_position + equals_position + 1 : term_position + end_position]
    value = value.strip()
    return value


def get_era(garbage):
    """
    Parses a string of text and determines the relevant era (BCE or CE).
    Uses a very naive approach. Will likely cause issues, for example, when a
    person is born BCE and dies CE.
    """
    era = 'CE'
    if 'AD' in garbage or 'CE' in garbage:
        era = 'CE'
    if 'BC' in garbage or 'BCE' in garbage:
        era = 'BCE'
    return era

def remove_era_text(garbage):
    garbage = garbage.replace('BCE', '').replace('BC', '').replace('CE', '').replace('AD', '').strip()
    return garbage

def clean_raw_date_text(garbage):
    garbage = garbage.replace('{', '|').strip()
    garbage = garbage.replace('}', '|').strip()
    # remove certain types of parentheses and their contents
    garbage = re.sub(r'\([^)]*\)', '|', garbage).strip()
    garbage = re.sub(r'\<[^>]*\>', '|', garbage).strip()
    return garbage

def parse_year(garbage):
    date = parse_date(garbage)
    if not date: return
    return date.year_only()

def parse_date(garbage, test=False):
    """
    Takes text as input that is potentially full of useless information.
    Parses the text to find a date and returns a datetime object if possible.
    Returns None if no datetime object can be made.
    """
    garbage = clean_raw_date_text(garbage)

    era = get_era(garbage)
    garbage = remove_era_text(garbage)

    value_list = garbage.split('|')

    date_and_time = dateparser.parse(value_list[0])
    now = datetime.datetime.utcnow()
    if date_and_time and not (date_and_time.month is now.month and date_and_time.day is now.day):
        return date.Date.from_datetime(date_and_time, era)

    # keep track of multiple dates if provided
    date_lists = []
    date_list = []
    date_lists.append(date_list)
    for value in value_list:
        try:
            number = int(value)
        except ValueError:
            continue

        if len(date_list) >= 3:
            date_list = []
            date_lists.append(date_list)
        date_list.append(value)

    date_string = ' '.join(date_lists[0])
    date_and_time = dateparser.parse(date_string)
    if date_and_time:
        return date.Date.from_datetime(date_and_time, era)
    return date_and_time


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
    if isinstance(value, basestring) and value[-1] == 'm':
        return value
    return "{0}m".format(value)


def parse_elevation(value):
    elevation = prettify_number(value)
    return metres(elevation)


def parse_answer(raw_answer, question_info):
    parse_function = question_info['parse_function']
    clean_data = parse_raw_data(raw_answer)
    if clean_data:
        answer = globals()[parse_function](clean_data)
        if answer and 'unit' in question_info:
            unit_function = question_info['unit']
            answer = globals()[unit_function](answer)

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



raw_text_values = [] # test code

def generate_answers(text, category_info, entity):
    num_entity_questions = 0
    for search_term, question_data in category_info['questions'].iteritems():
        raw_answer = search_text(text, search_term)
        raw_text_values.append(raw_answer)
        answer = parse_answer(raw_answer, question_data)
        if not answer:
            continue
        question_data['answer'] = answer
        print_card(question_data, entity)
        num_entity_questions += 1
    return num_entity_questions


def start_search():
    total_questions = 0
    for category, category_info in questions.categories.iteritems():
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

    '''
    print '-'*40
    for value in raw_text_values:
        print value
    '''


if __name__ == '__main__':
    start_search()

