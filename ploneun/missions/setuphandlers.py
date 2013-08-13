from collective.grok import gs
from ploneun.missions import MessageFactory as _

@gs.importstep(
    name=u'ploneun.missions', 
    title=_('ploneun.missions import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ploneun.missions.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
