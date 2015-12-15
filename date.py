
class Date(object):

    def __init__(self, year, month, day, era):
        self.year = year
        self.month = month
        self.day = day
        self.era = era

    @classmethod
    def from_datetime(cls, datetime_object, era):
        return cls(datetime_object.year, 
                datetime_object.month, 
                datetime_object.day, 
                era)

    def __str__(self):
        era_text = ' {}'.format(self.era)
        if self.year > 1000 and self.era == 'CE':
            era_text = ''
        return "{self.year}/{self.month}/{self.day}{era_text}".format(self=self, era_text=era_text)
