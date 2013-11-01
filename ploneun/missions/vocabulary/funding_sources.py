from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from ploneun.missions import MessageFactory as _

class FundingSources(grok.GlobalUtility):
    grok.name('ploneun.missions.funding_sources')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': u'Multilateral',
        'title': _(u'Term Title'),
    },{
        'value': u'Bilateral',
        'title': _(u'Bilateral')
    },{
        'value': u'Private Sector',
        'title': _(u'Private Sector')
    },{
        'value': u'Financial Instituition',
        'title': _(u'Financial Instituition')
    },{
        'value': u'Government',
        'title': _(u'Government')
    },{
        'value': u'CSO',
        'title': _(u'CSO')
    },{
        'value': u'Non-Profit Foundation',
        'title': _(u'Non-Profit Foundation')
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(**i))
        return SimpleVocabulary(terms)
