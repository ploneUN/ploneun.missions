from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility

def resolve_value(context, value, vocabulary):
    factory = getUtility(IVocabularyFactory, name=vocabulary)
    vocab = factory(context)
    return vocab.getTerm(value).title
