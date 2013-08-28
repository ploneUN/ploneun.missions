from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.mission import Imission

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(Imission)
    grok.require('zope2.View')
    grok.template('mission_view')
    grok.name('view')

