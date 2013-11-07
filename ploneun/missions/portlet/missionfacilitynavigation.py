from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner, aq_chain
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ploneun.missions import MessageFactory as _

from ploneun.missions.content.mission_facility import IMissionFacility

class IMissionFacilityNavigation(IPortletDataProvider):
    """
    Define your portlet schema here
    """
    pass

class Assignment(base.Assignment):
    implements(IMissionFacilityNavigation)

    @property
    def title(self):
        return _('Mission Facility Navigation')

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/missionfacilitynavigation.pt')

    @property
    def available(self):
        if self.facility():
                return True
        return False

    def facility(self):
        for item in aq_chain(self.context):
            if IMissionFacility.providedBy(item):
                return item
        return None

    def links(self):
        facility = self.facility()
        url = facility.absolute_url()
        return [{
            'id': 'add-mission',
            'title': _('Add Mission'),
            'url': '%s/missions/++add++ploneun.missions.mission' % url
        },{
            'id': 'view-all',
            'title': _('View All Missions'),
            'url': '%s/all-missions' % url
        },{
            'id': 'view-travel-table',
            'title': _('View All Missions (Table)'),
            'url': '%s/all-missions/missiontravel' % url
        },{
            'id': 'view-mission-reports',
            'title': _('View All Mission Reports'),
            'url': '%s/all-missionreports' % url
        },{
            'id': 'view-my-missions',
            'title': _('My Missions'),
            'url': '%s/my-missions' % url
        },{
            'id': 'view-my-missionreport',
            'title': _('My Mission Reports'),
            'url': '%s/my-missionreports' % url
        },{
            'id': 'view-my-missionreport-drafts',
            'title': _('My Mission Report Drafts'),
            'url': '%s/my-missionreport-drafts' % url
        },{
            'id': 'view-my-missions-without-reports',
            'title': _('My Missions Without Reports'),
            'url': '%s/my-missions-without-reports' % url,
        },{
            'id': 'search-missions',
            'title': _(u'Search Missions'),
            'url': '%s/search-missions' % url
        },{
            'id': 'search-missionreports',
            'title': _(u'Search Mission Reports'),
            'url': '%s/search-missionreports' % url,
        }]

class AddForm(base.NullAddForm):
    form_fields = form.Fields(IMissionFacilityNavigation)
    label = _(u"Add Mission Facility Navigation")
    description = _(u"Navigation for Mission Facilities")

    def create(self):
        return Assignment()
