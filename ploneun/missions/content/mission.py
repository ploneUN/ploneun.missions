from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from collective.z3cform.widgets.enhancedtextlines import \
    EnhancedTextLinesFieldWidget
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.dexterity.behaviors.metadata import IBasic

import p01.vocabulary.country

from ploneun.missions import MessageFactory as _
from collective import dexteritytextindexer


# Interface class; used to define content-type schema.

class IMission(IBasic, IImageScaleTraversable):
    """
    Plone UN Mission
    """

    title = schema.TextLine(title=u'Mission', 
                            description=u'Brief title of mission. eg. '
                            'Public Consultation for UN Workshop.')

    description = schema.Text(title=u'Mission Objective', 
                              description=u'Briefly describe the objectives '
                              'of the mission.')

    mission_scope= schema.Choice(
        title=_(u'Mission Scope'),
        vocabulary='ploneun.missions.mission_scope',
    )

    mission_city = schema.TextLine(
        title=_(u'City'),
        required=False
    )

    country = schema.Choice(
        title=_(u'Country'),
        description=_(u'If Mission Scope is International, please select '
                      'a country.'),
        vocabulary='ploneun.vocabulary.country',
        required=True,
        missing_value = None,
    )

    startDate = schema.Datetime(
        title=_(u'Start date'),
    )

    endDate  = schema.Datetime(
        title=_(u'End date'),
    )

    form.widget(mission_members=AutocompleteMultiFieldWidget)
    mission_members= schema.List(
        title=_(u'Mission Members'),
        description=_(u'List of Mission Members. Enter '
                      'name to search, select and press Enter to add. Repeat to '
                      'to add additional members.'),
        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users",),
        required=True,
    )

    dexteritytextindexer.searchable('text')
    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    text = schema.Text(
        title=_(u'Notes'),
        required=False
    )

    contactName = schema.TextLine(
        title=_(u'Contact Person'),
        required=False
    )

    contactEmail = schema.TextLine(
        title=_(u'Contact Person Email'),
        required=False
    )

    contactPhone = schema.TextLine(
        title=_(u'Contact Person Phone'),
        required=False
    )
