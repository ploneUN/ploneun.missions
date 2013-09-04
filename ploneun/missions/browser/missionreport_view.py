from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.missionreport import IMissionReport

from Acquisition import aq_parent

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionReport)
    grok.require('zope2.View')
    grok.template('missionreport_view')
    grok.name('view')

    def mission(self):
        return aq_parent(self.context)
