from ploneun.calendar.interfaces import ITableColumnProvider
from ploneun.missions.vocabulary import resolve_value
from zope.interface import Interface
from five import grok

class MissionColumnProvider(grok.Adapter):
    grok.implements(ITableColumnProvider)
    grok.context(Interface)
    grok.name('ploneun.missions.mission')

    def __init__(self, context):
        self.context = context

    def header_row(self):
        return [
            u'Date',
            u'Purpose',
            u'Location',
            u'Contact Person'
        ]

    def item_row(self, item):
        item_obj = item.getObject()
        location = []
        if item_obj.mission_city:
            location.append(item_obj.mission_city)
        if item_obj.country:
            country = resolve_value(
                self.context, 
                item_obj.country,
                'ploneun.vocabulary.country'
            )
            location.append(country)

        return [
            '%s - %s' % (item.start.strftime('%d %b'),
                            item.end.strftime('%d %b')),
            '<a href="%s">%s</a>' % (item.getURL(), item.Title()),
            ', '.join(location),
            item_obj.contactName
        ]

