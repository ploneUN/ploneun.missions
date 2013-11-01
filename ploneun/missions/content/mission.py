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

from plone.app.textfield import RichText
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


# Interface class; used to define content-type schema.

class IMission(IBasic, IImageScaleTraversable):
    """
    Plone UN Mission
    """

    title = schema.TextLine(title=u'Mission', 
                            description=u'Brief title of mission. eg. '
                            'Public Consultation for UN Workshop.')

    description = schema.Text(title=u'Overall Objective', 
                              description=u'Briefly describe the objectives '
                              'of the mission.')

    startDate = schema.Datetime(
        title=_(u'Start date'),
    )

    endDate  = schema.Datetime(
        title=_(u'End date'),
    )
    
    output_stream = schema.Choice(
        vocabulary='ploneun.missions.output_streams',
        title=_(u'Output Stream'),
        description=_(u'Select Streams'),
        required=True,
    )

    output_contribution = RichText(
        title=_(u'Contribution to selected output stream'),
        description=_(u'Please describe briefly how your '
                      'mission has contributed to realizing the '
                      'relevant stream outcome'),
    )

    mission_funding_source = schema.Choice(
        title=_(u'Source of Mission Funding'),
        vocabulary=u'ploneun.missions.funding_sources',
        required=True,
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

    form.widget(mission_support_staff=AutocompleteMultiFieldWidget)
    mission_support_staff= schema.List(
        title=_(u'Support Staff'),
        description=_(u'List of support staff '
                      'that have made a contribution to the success '
                      'of the mission. Enter name to search. Select and '
                      'press enter to add. Repeat to add additional staff.'),
        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users"),
        required=False,
    )

    mission_scope= schema.Choice(
        title=_(u'Mission Scope'),
        vocabulary='ploneun.missions.mission_scope',
    )

    country = schema.Choice(
        title=_(u'Country'),
        description=_(u'If Mission Scope is International, please select '
                      'a country.'),
        vocabulary='ploneun.vocabulary.country',
        required=True,
        default=u'ID',
        missing_value = None,
    )

    form.widget(mission_location=EnhancedTextLinesFieldWidget)
    mission_location= schema.Tuple(
        title=_(u'City / Location (One per line)'),
        description=_(u'Fill in city or location name and click Add button.'),
        value_type=schema.TextLine(),
        missing_value=(),
        required=True,
    )
