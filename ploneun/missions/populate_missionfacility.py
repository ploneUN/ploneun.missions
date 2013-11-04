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

@grok.subscribe(IMissionFacility, IObjectAddedEvent)
def populate_calendar(obj, event):

    if obj.has_key('index'):
        return

    index = contentapi.create(obj, 'Document', id='index', title=obj.Title())

    index.setText(index_text)
    index.reindexObject()
    obj.setDefaultPage('index')

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
         'v': '../'}
    ]

    collection.reindexObject()

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
         'v': '../'},
        {'i': 'Creator', 
         'o': 'plone.app.querystring.operation.string.currentUser'}
    ]

    collection.reindexObject()

    # create search collection
    collection = contentapi.create(obj, 'Collection', id='search',
                                    title=u'Search')


    collection.query = [
        {'i': 'portal_type', 
         'o': 'plone.app.querystring.operation.selection.is', 
         'v': ['ploneun.missions.mission']}, 
        {'i': 'path', 
         'o': 'plone.app.querystring.operation.string.relativePath',
         'v': '../'}
    ]

    collection.reindexObject()
    obj.reindexObject()

    request = getRequest()
    request.response.redirect(index.absolute_url())
