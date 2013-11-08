from five import grok
from ploneun.calendar.interfaces import ICalendarDataExtender
from zope.interface import Interface
from plone import api
from ploneun.missions.vocabulary import resolve_value

class MissionCalendarDataExtender(grok.Adapter):
    grok.context(Interface)
    grok.implements(ICalendarDataExtender)
    grok.name('ploneun.missions.mission')

    def __init__(self, context):
        self.context = context

    def __call__(self, brain):
        obj = brain.getObject()
        result = []
        members = (obj.mission_members or [])
        if members:
            result.append(api.user.get(username=member).getProperty('fullname'))
        country = resolve_value(self.context, mission.country,
                                'ploneun.vocabulary.country')
        result.append(country)
        return {
            'footnote': ', '.join(result)
        }

