from plone.indexer import indexer
from five import grok
from ploneun.missions.content.mission import IMission
from DateTime import DateTime

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
def mission_country(obj):
    return obj.country
