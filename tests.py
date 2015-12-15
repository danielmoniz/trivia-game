
import unittest
import datetime

import api

class APITest(unittest.TestCase):

    def test_metres(self):
        self.assertEqual(api.metres('543'), '543m')
        self.assertEqual(api.metres(543), '543m')
        self.assertEqual(api.metres('543m'), '543m')


    def test_parse_date(self):
        garbage = 'dgh'
        date = api.parse_date(garbage)
        self.assertIsNone(date)

        garbage = 'march 22, 1972'
        date = api.parse_date(garbage)
        self.assertEqual(date.year, 1972)
        self.assertEqual(date.month, 3)
        self.assertEqual(date.day, 22)

        garbage = '3 April 1922'
        date = api.parse_date(garbage)
        self.assertEqual(date.year, 1922)
        self.assertEqual(date.month, 4)
        self.assertEqual(date.day, 3)

        garbage = '{{birth date |1858|10|27}}'
        date = api.parse_date(garbage)
        self.assertEqual(date.year, 1858)
        self.assertEqual(date.month, 10)
        self.assertEqual(date.day, 27)



if __name__ == '__main__':
    unittest.main()
