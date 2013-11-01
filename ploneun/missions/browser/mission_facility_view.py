from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.mission_facility import IMissionFacility

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionFacility)
    grok.require('zope2.View')
    grok.template('mission_facility_view')
    grok.name('view')

