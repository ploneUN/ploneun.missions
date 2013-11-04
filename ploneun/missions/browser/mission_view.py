from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.mission import IMission
from ploneun.missions.vocabulary import resolve_value
import urllib

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMission)
    grok.require('zope2.View')
    grok.template('mission_view')
    grok.name('view')

    def contains_missionreport(self):
        # Checks for Mission Report in Current Mission
        context = self.context

        cur_path = '/'.join(context.getPhysicalPath())

        path = {}
        path['query'] = cur_path
        path['depth'] = 1

        contentFilter = {}
        contentFilter['path'] = path
        contentFilter['portal_type'] = 'ploneun.missions.missionreport'

        return bool(context.portal_catalog.queryCatalog(contentFilter))


    def missionreport_title(self):
        return urllib.quote(u'Mission Report : %s' % self.context.title)

    def detail_fields(self):
        fields = []

        members = []
        mtool = self.context.portal_membership
        for member in self.context.mission_members:
            m = mtool.getMemberById(member)
            members.append(
                '"%s" &lt;%s&gt;' % (
                    m.getProperty('fullname'),
                    m.getProperty('email')
                )
            )

        fields.append({
            'id': 'members',
            'title': 'Mission Members',
            'render': ('<ul>%s</ul>' % ''.join(['<li>%s</li>' % i for i in (
                members)])) if members else ''
        })

        toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime

        fields.append({
            'id': 'dates',
            'title': 'When',
            'render': '%s - %s' % (toLocalizedTime(self.context.startDate),
                                    toLocalizedTime(self.context.endDate))
        })

        location = []
        if self.context.mission_city:
            location.append(self.context.mission_city)
        if self.context.country:
            country = resolve_value(self.context, 
                self.context.country,
                'ploneun.vocabulary.country'
            )
            location.append(country)

        fields.append({
            'id': 'location',
            'title': 'Location',
            'render': ', '.join(location)
        })


        contact = [self.context.contactName or '']

        if self.context.contactEmail:
            if self.context.contactName:
                contact = ['"%s"' % self.context.contactName]
            contact.append('&lt;%s&gt;' % self.context.contactEmail)

        if self.context.contactPhone:
            contact.append('(%s)' % self.context.contactPhone)

        if (''.join(contact)).strip():
            fields.append({
                'id': 'contact',
                'title': 'Contact',
                'render': ' '.join(contact)
            })

        if self.context.text:
            fields.append({
                'id': 'text',
                'title': 'Note',
                'render': self.context.text
            })
    
        return fields
