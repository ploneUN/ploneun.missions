from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource

class OutputStreams(grok.GlobalUtility):
    grok.name('ploneun.missions.output_streams')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': u'Institutions and Processes',
        'title': u'Institutions and Processes',
    },{
        'value': u'Legal and Regulatory Frameworks',   
        'title': u'Legal and Regulatory Frameworks',
    },{
        'value': u'Legal and Regulatory Frameworks',
        'title': u'Legal and Regulatory Frameworks',
    },{
        'value': u'Strategic Programs',
        'title': u'Strategic Programs'
    },{
        'value': u'Changes to Work Paradigm and Culture',
        'title': u'Changes to Work Paradigm and Culture'
    },{
        'value': u'Inclusion / Involvement of Stakeholders',
        'title': u'Inclusion / Involvement of Stakeholders'
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(**i))
        return SimpleVocabulary(terms)
