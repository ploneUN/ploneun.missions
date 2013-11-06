from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.missionreport import IMissionReport
from zope.pagetemplate.pagetemplate import PageTemplate
from Acquisition import aq_parent

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionReport)
    grok.require('zope2.View')
    grok.template('missionreport_view')
    grok.name('view')

    def mission(self):
        return aq_parent(self.context)

    def attachments(self):
        brains = self.context.portal_catalog({
            'portal_type': 'File',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1
            }
        })
        pt = PageTemplate()
        pt.write('<metal:macro use-macro="widgetmacro"></metal:macro>')
        result = []
        for brain in brains:
            obj = brain.getObject()
            macro = obj.widget('file', mode='view')
            widget = pt.pt_render({
                'context': obj,
                'widgetmacro': macro,
                'here': obj,
                'accessor': obj.getFile,
                'field': obj.getField('file'),
                'fieldName': 'file'
            })
            result.append(widget)
        return result
