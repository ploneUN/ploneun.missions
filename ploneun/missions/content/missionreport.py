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

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from collective.z3cform.widgets.enhancedtextlines import \
    EnhancedTextLinesFieldWidget
from plone.app.content.interfaces import INameFromTitle
from Acquisition import aq_parent

from ploneun.missions import MessageFactory as _
from zope.lifecycleevent import IObjectAddedEvent


# Interface class; used to define content-type schema.

class IMissionReport(form.Schema, IImageScaleTraversable):
    """
    UN Mission Report
    """


    report_outcome = schema.TextLine(
        title=_(u'Country / Regional Programme Outcome'),
        description=_(u'Enter outcome code here eg. IDN 101'),
        required=False
    )

    form.widget(report_outcome_text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    report_outcome_text = schema.Text(
        title=_(u'Contribution to Outcome'),
        description=_(u'Please describe briefly how your mission has'
            'contributed to realizing the relevant country/regional outcome.'),
        required=False
    )

    form.widget(report_author=AutocompleteMultiFieldWidget)
    report_author= schema.List(
        title=_(u'Author(s)'),
        description=_(u'List of Authors. Enter '
            'name to search, select and press Enter to add. Repeat to '
            'to add additional members with principal author first.'),
        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users"),
        default=[],
        missing_value=(),
        required=True,
    )


    form.widget(achievements_summary="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    achievements_summary = schema.Text(
        title=_(u'Achievements Summary'),
        description=_(u'Please fill this section in short telex style'),
        required=False
    )

    form.widget(mission_findings="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_findings = schema.Text(
        title=_(u'Mission Findings'),
        description=_(u'Please keep to approx 500 words. Other relevant documents'
                ' can be attached below.'),
        required=False
    )

    form.widget(mission_followup="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_followup = schema.Text(
        title=_(u'Follow-up actions/next steps'),
        description=_(u'In point form, include who should be doing what. '
                    u'One follow-up action per line.'),
        required=False
    )

    form.widget(mission_contact="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_contact = schema.Text(
        title=_(u'List of Contacts'),
        description=_(u'List of professionals and/or organizations met with '
            u'during the mission'),
        required=False
    )

    form.widget(mission_distribution=AutocompleteMultiFieldWidget)
    mission_distribution = schema.List(
        title=_(u'Distribution List'),
        description=_(u'Enter '
            'name to search, select and press Enter to add. Repeat to '
            'to add additional members.'),
        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users"),
        required=False
    )

class NameFromTitle(grok.Adapter):
    grok.implements(INameFromTitle)
    grok.context(IMissionReport)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return u'Mission Report'


@grok.subscribe(IMissionReport, IObjectAddedEvent)
def mission_report_title(obj, event):
    parent = aq_parent(obj)
    obj.title = u'Mission Report : %s' % parent.title
    obj.reindexObject()
