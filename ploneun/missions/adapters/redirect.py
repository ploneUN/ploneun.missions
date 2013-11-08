from inigo.redirecttocontainer.base import BaseRedirector
from five import grok
from Products.ATContentTypes.interfaces.file import IATFile
from plone.app.blob.interfaces import IATBlobFile
from ploneun.missions.content.missionreport import IMissionReport

class RedirectFileToMissionReport(BaseRedirector):
    grok.context(IATFile)
    grok.name('ploneun.mission.redirectfiletomissionreport')
    container_iface = IMissionReport
    direct_parent = True


class RedirectBlobFileToMissionReport(BaseRedirector):
    grok.context(IATBlobFile)
    grok.name('ploneun.mission.redirectblobfiletomissionreport')
    container_iface = IMissionReport
    direct_parent = True
