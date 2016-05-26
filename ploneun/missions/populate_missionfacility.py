from zope.globalrequest import getRequest
from plone.api import content as contentapi
from zope.app.container.interfaces import IObjectAddedEvent
from ploneun.missions.content.mission_facility import IMissionFacility
from five import grok

index_text = '''
<p>To enter your missions into the calendar, 
simply click on the "Add Mission" in the box on the left side and follow 
the instructions. After filling in and submitting the completed form, 
mission will show in the appropriate calendar.</p>

<p>You can begin drafting your mission report already from the calendar entry i.e. 
all the mission related information entered into the mission calendar can be automatically 
moved directly into your mission report draft by simply clicking on "Create new mission report"
at the bottom of your completed calendar entry. This function will save you time 
and allow you to complete large parts of your mission report before you have even departed.</p>

<p>You can browse by a specific date, month or year when viewing the calendar</p>
'''

#@grok.subscribe(IMissionFacility, IObjectAddedEvent)
def populate_calendar(obj, event):

    if obj.has_key('index'):
        return

    index = contentapi.create(obj, 'Document', id='index', title=obj.Title())

    index.setText(index_text)
    index.reindexObject()
    obj.setDefaultPage('index')

    # create container for missions

    mission_container = contentapi.create(obj, 'Folder', id='missions',
            title=u'Missions')

    # create all missions collection
    collection = contentapi.create(obj, 'Collection', id='all-missions',
                                    title=u'All Missions')


    collection.setLayout('solgemafullcalendar_view')

    collection.query = [
        {'i': 'portal_type', 
         'o': 'plone.app.querystring.operation.selection.is', 
         'v': ['ploneun.missions.mission']}, 
        {'i': 'path', 
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../missions'}
    ]

    collection.reindexObject()

    # create all mission reports collection

    collection = contentapi.create(obj, 'Collection', id='all-missionreports',
                                    title=u'All Mission Reports')


    collection.query = [
        {'i': 'portal_type', 
         'o': 'plone.app.querystring.operation.selection.is', 
         'v': ['ploneun.missions.missionreport']}, 
        {'i': 'path', 
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../missions'}
    ]

    # create my missions collection
    collection = contentapi.create(obj, 'Collection', id='my-missions',
            title=u'My Missions')
    collection.setLayout('solgemafullcalendar_view')

    collection.query = [
        {'i': 'portal_type',
         'o': 'plone.app.querystring.operation.selection.is',
         'v': ['ploneun.missions.mission']},
        {'i': 'path',
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../missions'},
        {'i': 'Creator', 
         'o': 'plone.app.querystring.operation.string.currentUser'}
    ]

    collection.reindexObject()

    # create my mission reports collection
    collection = contentapi.create(obj, 'Collection', id='my-missionreports',
            title=u'My Mission Reports')

    collection.query = [
        {'i': 'portal_type',
         'o': 'plone.app.querystring.operation.selection.is',
         'v': ['ploneun.missions.mission']},
        {'i': 'path',
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../missions'},
        {'i': 'Creator', 
         'o': 'plone.app.querystring.operation.string.currentUser'}
    ]

    collection.reindexObject()

    # create my mission reports drafts collection

    collection = contentapi.create(obj, 'Collection',
            id='my-missionreport-drafts',
            title=u'My Mission Report Drafts')

    collection.query = [
        {'i': 'portal_type',
         'o': 'plone.app.querystring.operation.selection.is',
         'v': ['ploneun.missions.missionreport']},
        {'i': 'path',
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../missions'},
        {'i': 'Creator', 
         'o': 'plone.app.querystring.operation.string.currentUser'},
        {'i': 'review_state', 
         'o': 'plone.app.querystring.operation.selection.is', 
         'v': ['internal', 'private']}
    ]

    collection.reindexObject()

    # create search collection
    collection = contentapi.create(obj, 'Topic', id='search-missions',
                                    title=u'Search Missions')

    collection = contentapi.create(obj, 'Topic', id='search-missionreports',
                                    title=u'Search Mission Reports')


    obj.reindexObject()

    request = getRequest()
    request.response.redirect(index.absolute_url())
