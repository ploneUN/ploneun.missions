from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.missionreport import IMissionReport
from zope.pagetemplate.pagetemplate import PageTemplate
from Acquisition import aq_parent
from plone import api

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionReport)
    grok.require('zope2.View')
    grok.template('missionreport_view')
    grok.name('view')

    def mission(self):
        return aq_parent(self.context)

    def detail_fields(self):
        fields = []

        fields.append({
            'id': 'achievements_summary',
            'title': 'Summary of Main Achievements',
            'render': self.context.achievements_summary,
        })

        fields.append({
            'id': 'mission_findings',
            'title': 'Mission Findings',
            'render': self.context.mission_findings,
        })

        fields.append({
            'id': 'mission_followup',
            'title': 'Follow-up actions/next steps',
            'render': self.context.mission_followup
        })

        return fields


    def distribution_emails(self):
        distribution_emails = []
        for u in (self.context.mission_distribution or []):
            user = api.user.get(username=u)
            distribution_emails.append('%s <%s>' % (
                user.getProperty('fullname'),
                user.getProperty('email')
            ))

        distribution_emails += (self.context.mission_distribution_others or [])

        return ', '.join(distribution_emails)


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
