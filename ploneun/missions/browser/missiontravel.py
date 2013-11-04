from five import grok
from Products.CMFCore.interfaces import IContentish
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarMarker
from ploneun.missions.vocabulary import resolve_value
from datetime import datetime
import calendar

grok.templatedir('templates')

class MissionTravel(grok.View):
    grok.context(ISolgemaFullcalendarMarker)
    grok.name('missiontravel')
    grok.require('zope2.View')
    grok.template('missiontravel')

    def _extract_days(self, start, end, year, month):
        if start.month() == month and end.month() == month:
            return range(start.day(), end.day() + 1)
        elif start.month() == month:
            final = calendar.monthrange(year, month)[1]
            return range(start.day(), final+1)
        elif end.month() == month:
            return range(1, end.day() +1 )
        else:
            raise AssertionError
    
    
    def items(self):
        now = datetime.now()
        month = int(self.request.get('month', now.month))
        year = int(self.request.get('year', now.year))

        results = self.context.results()

        def filter_month_year_type(item):
            if item.portal_type != 'ploneun.missions.mission':
                return False
            if not item.start:
                return False
            if item.start.month() == month and item.start.year() == year:
                return True
            return False

        return filter(filter_month_year_type, results)

    def countries(self):
        data = {}
        now = datetime.now()
        month = int(self.request.get('month', now.month))
        year = int(self.request.get('year', now.year))

        for item in self.items():
            obj = item.getObject()
            country = obj.country
            data.setdefault(country,  {})
            days = self._extract_days(item.start, item.end, year, month)
            members = obj.mission_members or []
            for member in members:
                data[country].setdefault(member, {})
                data[country][member].setdefault('days', [])
                data[country][member]['days'] += days
                data[country][member]['days'] = list(
                    set(data[country][member]['days'])
                )

        result = []

        for country, people in sorted(data.items(), key=lambda x:x[0]):
            if not country.strip():
                continue
            r = []
            for person, info in sorted(people.items(), key=lambda x:x[0]):
                o = {'name': person}
                o.update(info)
                r.append(o)

            result.append({
                'name': resolve_value(
                    self.context, country,
                    'ploneun.vocabulary.country'
                ),
                'people': r
            })

        return result

    def days(self):
        now = datetime.now()
        month = int(self.request.get('month', now.month))
        year = int(self.request.get('year', now.year))
        finalday = calendar.monthrange(year, month)[1]
        return range(1, finalday + 1)

    def months(self):
        thismonth = datetime.now().month
        month = int(self.request.get('month', thismonth))
        return [{'value': i, 'name': n,
            'selected': i == month} for i, n in enumerate(
            calendar.month_name) if i
        ]

    def monthTitle(self):
        month = self.month()
        return calendar.month_name[month].upper()

    def month(self):
        thismonth = datetime.now().month
        return int(self.request.get('month', thismonth))

