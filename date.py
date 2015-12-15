
class Date(object):

    def __init__(self, year, month, day, era):
        self.year = year
        self.month = month
        self.day = day
        self.era = era

    def year_only(self):
        self.month = None
        self.day = None
        return self

    @classmethod
    def from_datetime(cls, datetime_object, era):
        return cls(datetime_object.year, 
                datetime_object.month, 
                datetime_object.day, 
                era)

    def __str__(self):
        text = {}
        era = ' {}'.format(self.era)
        month = '/{}'.format(self.month)
        day = '/{}'.format(self.day)
        if self.year > 1000 and self.era == 'CE':
            era = ''
        if not self.month:
            month = ''
            day = ''
        return "{self.year}{month}{day}{era}".format(self=self, month=month, day=day, era=era)

