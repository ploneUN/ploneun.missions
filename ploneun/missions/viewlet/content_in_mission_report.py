from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets import interfaces as manager
from ploneun.missions.interfaces import IProductSpecific
from Products.ATContentTypes.interfaces.file import IATFile
from plone.app.blob.interfaces import IATBlobFile
from ploneun.missions.content.missionreport import IMissionReport
from Acquisition import aq_parent

grok.templatedir('templates')

class ContentInMissionReport(grok.Viewlet):
    grok.context(IContentish)
    grok.viewletmanager(manager.IBelowContentTitle)
    grok.template('content_in_mission_report')
    grok.layer(IProductSpecific)

    def available(self):
        if not (
            IATFile.providedBy(self.context) or
            IATBlobFile.providedBy(self.context)
            ):
            return False
        return bool(self.mission_report())

    def mission_report(self):
        parent = aq_parent(self.context)
        if IMissionReport.providedBy(parent):
            return parent
        return None
