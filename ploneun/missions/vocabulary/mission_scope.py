from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource

class MissionScope(grok.GlobalUtility):
    grok.name('ploneun.missions.mission_scope')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': u'International',
        'title': _(u'International'),
    }, {
        'value': u'National',
        'title': _(u'National'),
    }, {
        'value': u'Regional',
        'title': _(u'Regional')
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(**i))
        return SimpleVocabulary(terms)
