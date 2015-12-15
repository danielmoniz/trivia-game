
"""
parse_function should be a string corresponding to the name of a function.
"""

categories = {
    'people': {
        'file': 'people.txt',
        'questions': {
            'birth_date': {
                'question': 'In what year was {0} born?',
                'parse_function': 'parse_pipes',
            },
            'death_date': {
                'question': 'In what year did {0} die?',
                'parse_function': 'parse_pipes',
            },
            'term_start': {
                'question': 'When did {0} start their first term?',
                'parse_function': 'parse_pipes',
            },
        },
    },

    'cities': {
        'file': 'cities.txt',
        'questions': {
            'population_total': {
                'question': 'What is the population of the city proper of {0} (as of 2015)?',
                'parse_function': 'parse_population',
            },
            'pop_latest': {
                'question': 'What is the population of the city proper of {0} (as of 2015)?',
                'parse_function': 'parse_population',
            },
            'elevation_m': {
                'question': 'What is the elevation (in metres) of the city proper of {0} (as of 2015)?',
                'parse_function': 'parse_elevation',
            },
        },
    },

    'freestanding_structures': {
        'file': 'freestanding_structures.csv',
        'questions': {
            'architectural': {
                'other_names': ['architechtural'],
                'question': 'What is the architectural height (in metres) of the {0}?',
                'parse_function': 'parse_pipes',
                'unit': 'metres',
            },
            'architechtural': {
                'question': 'What is the architectural height (in metres) of the {0}?',
                'parse_function': 'parse_pipes',
                'unit': 'metres',
            },
            'antenna_spire': {
                'question': 'What is the antenna spire height (in metres) of the {0}?',
                'parse_function': 'parse_pipes',
                'unit': 'metres',
            },
        },
    },
}

