from five import grok
from plone.directives import dexterity, form
from ploneun.missions.content.mission_facility import IMissionFacility

grok.templatedir('templates')

def is_number(val):
    try:
        float(val)
        return True
    except Exception:
        return False

class Index(dexterity.DisplayForm):
    grok.context(IMissionFacility)
    grok.require('zope2.View')
    grok.template('mission_facility_view')
    grok.name('view')

    
    def mission_reports(self):
        context = self.context
        top_number = 5
        if is_number(context.top_result):
            top_number = int(context.top_result)
        
        brains = context.portal_catalog({'path':{'query':'/'.join(context.getPhysicalPath()),
                                                 'depth':1},
                                         'portal_type':'ploneun.missions.missionreport',
                                         'review_state':'shared_intranet',
                                         'sort_on':'created',
                                         'sort_order':'reverse'})
        return brains[:top_number]
