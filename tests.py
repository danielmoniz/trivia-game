
import unittest
import datetime

import api

class APITest(unittest.TestCase):

    def test_metres(self):
        self.assertEqual(api.metres('543'), '543m')
        self.assertEqual(api.metres(543), '543m')
        self.assertEqual(api.metres('543m'), '543m')

    def test_partial_date_parsing(self):
        garbage = '1973'
        date = api.parse_date(garbage)
        self.assertEqual(date.year, 1973)

    def test_parse_date(self):
        garbage = 'dgh'
        date = api.parse_date(garbage)
        self.assertIsNone(date)

        garbage = 'march 22, 1972'
        date = api.parse_date(garbage)
        self.assert_date(date, 1972, 3, 22)

        garbage = '3 April 1922'
        date = api.parse_date(garbage)
        self.assert_date(date, 1922, 4, 3)

        garbage = '{{birth date |1858|10|27}}'
        date = api.parse_date(garbage)
        self.assert_date(date, 1858, 10, 27)

        garbage = '28 January 1547 (aged 55)'
        date = api.parse_date(garbage)
        self.assert_date(date, 1547, 1, 28)

        garbage = '{{Death date and age|df=yes|1901|1|22|1819|5|24}}'
        date = api.parse_date(garbage)
        self.assert_date(date, 1901, 1, 22)

        garbage = '{{Death date and age|df=yes|1901|1|6|1819|5|7}}'
        date = api.parse_date(garbage)
        self.assert_date(date, 1901, 1, 6)

        garbage = "{{nowrap|20 March [[Old Style and New Style dates|1726/7]]<!-- This is the generally accepted manner of recording Newton's death date. Please do not change without discussion. --> (aged 84)}}<br>{{small|<nowiki>[</nowiki>[[Old Style and New Style dates|OS]]: {{death date|1726|03|20|df=y}}<br>&nbsp;[[Old Style and New Style dates|NS]]: {{death date|1727|03|31|df=y}}<nowiki>]</nowiki><!--end small:-->}}{{lower|0.1em|<ref name='OSNS'/>}}"
        date = api.parse_date(garbage)
        self.assert_date(date, 1726, 3, 20)

        garbage = '25 December 1642<br>{{small|<nowiki>[</nowiki>[[Old Style and New Style dates|NS]]: {{Birth date|1643|01|04|df=y}}<nowiki>]</nowiki>}}{{lower|0.1em|<ref name="OSNS"/>}}'
        date = api.parse_date(garbage)
        self.assert_date(date, 1642, 12, 25)

        '''
        # need to support dates BC/BCE
        garbage = '13 July 100 BC'
        date = api.parse_date(garbage)
        self.assertEqual(date.year, -49)
        self.assertEqual(date.month, 10)
        self.assertEqual(date.day, 0)
        '''

    def test_era_date_parsing(self):
        garbage = '632|6|8|570 CE'
        date = api.parse_date(garbage)
        self.assert_date(date, 632, 6, 8)

        garbage = '632|6|8|570 AD'
        date = api.parse_date(garbage)
        self.assert_date(date, 632, 6, 8)

        garbage = '{{death date and age|632|6|8|570||}} CE'
        date = api.parse_date(garbage)
        self.assert_date(date, 632, 6, 8)

        garbage = '{{death date and age|632|6|8|570||}} AD'
        date = api.parse_date(garbage)
        self.assert_date(date, 632, 6, 8)

        garbage = '{{c.|570}} CE'
        date = api.parse_date(garbage, test=True)
        self.assertEqual(date.year, 570)

        garbage = '1400 BC'
        date = api.parse_date(garbage)
        self.assert_date(date, 1400, None, None, 'BCE')

        garbage = '13 July 100 BC'
        date = api.parse_date(garbage)
        self.assert_date(date, 100, 7, 13, 'BCE')

        garbage = '{{c.|570}} BCE'
        date = api.parse_date(garbage, test=True)
        self.assert_date(date, 570, None, None, 'BCE')

        garbage = '632|6|8|570 BC'
        date = api.parse_date(garbage)
        self.assert_date(date, 632, 6, 8, 'BCE')


    def assert_date(self, date, year, month, day, era='CE'):
        self.assertEqual(date.year, year)
        if month:
            self.assertEqual(date.month, month)
        if day:
            self.assertEqual(date.day, day)
        self.assertEqual(date.era, era)
        print date




if __name__ == '__main__':
    unittest.main()
