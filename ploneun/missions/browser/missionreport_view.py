from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.missionreport import Imissionreport

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(Imissionreport)
    grok.require('zope2.View')
    grok.template('missionreport_view')
    grok.name('view')

