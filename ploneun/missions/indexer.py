from plone.indexer import indexer
from five import grok
from ploneun.missions.content.mission import IMission
from ploneun.missions.content.missionreport import IMissionReport
from DateTime import DateTime
from Acquisition import aq_chain
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from zope.lifecycleevent import IObjectModifiedEvent
from plone import api

def get_mission(obj):
    for i in aq_chain(obj):
        if IMission.providedBy(i):
            return i
    return None

@indexer(IMission)
def mission_start(obj):
    if obj.startDate:
        return DateTime(obj.startDate)

@indexer(IMission)
def mission_end(obj):
    if obj.endDate:
        return DateTime(obj.endDate)

@indexer(IMission)
def mission_country(obj):
    return obj.country

@indexer(IMission)
def mission_has_missionreport(obj):
    for i in obj.values():
        if IMissionReport.providedBy(i):
            if api.content.get_state(i) != 'private':
                return True
    return False

@indexer(IMissionReport)
def missionreport_description(obj):
    mission = get_mission(obj)
    return mission.Description()


@indexer(IMissionReport)
def missionreport_country(obj):
    mission = get_mission(obj)
    return mission.country

@indexer(IMissionReport)
def missionreport_ilo_themes(obj):
    mission = get_mission(obj)
    return mission.ilo_themes

@indexer(IMissionReport)
def missionreport_ilo_regions(obj):
    mission = get_mission(obj)
    return mission.ilo_regions

@indexer(IMissionReport)
def missionreport_missionscope(obj):
    mission = get_mission(obj)
    return mission.mission_scope

@indexer(IMission)
def mission_missionscope(obj):
    return obj.mission_scope

@grok.subscribe(IMissionReport, IAfterTransitionEvent)
def reindex_mission_on_report_workflow_update(obj, event):
    mission = get_mission(obj)
    mission.reindexObject()

@grok.subscribe(IMission, IObjectModifiedEvent)
def reindex_missionreport_on_mission_modification(obj, event):
    for i in obj.values():
        if IMissionReport.providedBy(i):
            i.reindexObject()
