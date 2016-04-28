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
from collective import dexteritytextindexer
from plone.formwidget.multifile import MultiFileFieldWidget
from z3c.form.browser.radio import RadioFieldWidget

from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from plone.z3cform.fieldsets.utils import move

#from z3c.form.interfaces import HIDDEN_MODE
import z3c.form

MissionType = SimpleVocabulary(
    [SimpleTerm(value=u'Domestic', title=_(u'Domestic')),
     SimpleTerm(value=u'International', title=_(u'International'))]
    )

# Interface class; used to define content-type schema.

class IMissionReport(form.Schema, IImageScaleTraversable):
    """
    UN Mission Report
    """
    title = schema.TextLine(
        title=u'Mission Title',
        required=True
    )

    overall_objective = schema.Text(
        title=u'Overall Objective',
        required=True
    )

#    dexteritytextindexer.searchable('report_outcome')
#    report_outcome = schema.TextLine(
#        title=_(u'Country / Regional Programme Outcome'),
#        description=_(u'Enter outcome code here eg. IDN 101'),
#        required=False
#    )

#    dexteritytextindexer.searchable('report_outcome_text')
#    form.widget(report_outcome_text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
#    report_outcome_text = schema.Text(
#        title=_(u'Contribution to Outcome'),
#        description=_(u'Please describe briefly how your mission has'
#            'contributed to realizing the relevant country/regional outcome.'),
#        required=False
#    )

#    dexteritytextindexer.searchable('report_author')
#    form.widget(report_author=AutocompleteMultiFieldWidget)
#    report_author= schema.List(
#        title=_(u'Author(s)'),
#        description=_(u'List of Authors. Enter '
#            'name to search, select and press Enter to add. Repeat to '
#            'to add additional members with principal author first.'),
#        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users"),
#        default=[],
#        missing_value=(),
#        required=True,
#    )


    report_author = schema.Text(
        title=u'Author(s)',
        required=True
    )


    dexteritytextindexer.searchable('mission_members')
    form.widget(mission_members=AutocompleteMultiFieldWidget)
    mission_members= schema.List(
        title=_(u'Mission Members'),
        description=_(u'List of Mission Members.'),
        value_type=schema.Choice(vocabulary=u"plone.principalsource.Users",),
        required=True,
    )

    #ILO Office

    startDate = schema.Date(
        title=_(u'Mission Start date'),
    )

    endDate  = schema.Date(
        title=_(u'Mission End date'),
    )

    form.widget(mission_type=RadioFieldWidget)
    mission_type = schema.Choice(
        title=_(u'Mission Type'),
        vocabulary=MissionType,
        required=True
    )


    dexteritytextindexer.searchable('mission_city')
    mission_city = schema.TextLine(
        title=_(u'City'),
        required=False
    )

    #Mission Location

    #Other

    #ILO themes

    #Theme
    
    mission_location_other = schema.TextLine(
        title = _(u'Other'),
        description = _(u'If Other was selected, please specify country location.'),
        required = False,
    )

    dexteritytextindexer.searchable('achievements_summary')
    form.widget(achievements_summary="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    achievements_summary = schema.Text(
        title=_(u'Summary of Main Achievements'),
        description=_(u'Please fill this section in short telex style'),
        required=False
    )

    dexteritytextindexer.searchable('mission_findings')
    form.widget(mission_findings="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_findings = schema.Text(
        title=_(u'Mission Findings'),
        description=_(u'Please keep to approx 500 words. Other relevant documents'
                ' can be attached below.'),
        required=False
    )

    dexteritytextindexer.searchable('mission_followup')
    form.widget(mission_followup="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_followup = schema.Text(
        title=_(u'Follow-up actions/next steps'),
        description=_(u'In point form, include who should be doing what. '
                    u'One follow-up action per line.'),
        required=False
    )

    dexteritytextindexer.searchable('mission_contact')
    form.widget(mission_contact="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    mission_contact = schema.Text(
        title=_(u'List of Contacts'),
        description=_(u'List of professionals and/or organizations met with '
            u'during the mission'),
        required=False
    )


#    mission_distribution = schema.Text(
#        title=u'Distribution List (Members)',
#        description=_(u'Comma separated list of who a copy of this mission report should be sent to. Select previous email addresses from drop down list, or type new email address followed by a comma. Copy will be sent, when Mission Report state is submitted.'),
#        required=True
#    )

#    mission_distribution_others = schema.Text(
#        title=u'Distribution List (Others)',
#        description=_(u'Comma separated list of who a copy of this mission report should be sent to. Select previous email addresses from drop down list, or type new email address followed by a comma. Copy will be sent, when Mission Report state is submitted.'),
#        required=True
#    )

    dexteritytextindexer.searchable('mission_distribution')
    form.widget(mission_distribution=AutocompleteMultiFieldWidget)
    mission_distribution = schema.List(
        title=_(u'Distribution List (Members)'),
        description=_(u'Enter name to search, select and press Enter to add. '
            'Repeat to add additional members'),
        value_type=schema.Choice(vocabulary='plone.principalsource.Users'),
        required=False
    )

    dexteritytextindexer.searchable('mission_distribution_others')
    mission_distribution_others = schema.List(
        title=_(u'Distribution List (Others)'),
        description=_(u'Add email addreses of unregistered members here.  One address for each line'),
        required=False,
        value_type=schema.TextLine()
    )

    attachment1 = NamedBlobFile(
            title=_(u"Attachment 1"),
            description=_(u"Please attach a file"),
            required=False,
        )

    attachment2 = NamedBlobFile(
            title=_(u"Attachment 2"),
            description=_(u"Please attach a file"),
            required=False,
        )

    attachment3 = NamedBlobFile(
            title=_(u"Attachment 3"),
            description=_(u"Please attach a file"),
            required=False,
        )

    attachment4 = NamedBlobFile(
            title=_(u"Attachment 4"),
            description=_(u"Please attach a file"),
            required=False,
        )

    attachment5 = NamedBlobFile(
            title=_(u"Attachment 5"),
            description=_(u"Please attach a file"),
            required=False,
        )
    
    @invariant
    def formValidation(self):
        if self.startDate > self.endDate:
            raise Invalid(u"Start date should not be later than end date.")




alsoProvides(IMissionReport, IFormFieldProvider)


#reorder fields on add form
class missionReportAddForm(dexterity.AddForm):
    grok.name('ploneun.missions.missionreport')
    form.wrap(False)
    def updateFields(self):
        super(missionReportAddForm, self).updateFields()
        if 'IILOCountries.mission_location' in self.fields.keys():
            move(self, 'IILOCountries.mission_location', after='mission_city')
        
        if 'IILOOffices.ilo_offices' in self.fields.keys():
            move(self, 'IILOOffices.ilo_offices', after='mission_members')

        
            
        
        if 'IILOOffices.mission_location_other' in self.fields.keys():
            move(self, 'IILOOffices.mission_location_other', after='IILOCountries.mission_location')

        if 'IILOTheme.ilo_themes' in self.fields.keys():
            move(self, 'IILOTheme.ilo_themes', after='mission_location_other')
        if 'IILOTheme.theme_other' in self.fields.keys():
            move(self, 'IILOTheme.theme_other', after='IILOTheme.ilo_themes')
            
        
    

#reorder fields on edit form
class missionReportEditForm(dexterity.EditForm):
    grok.context(IMissionReport)
    def updateFields(self):
        super(missionReportEditForm, self).updateFields()
        
        if 'IILOCountries.mission_location' in self.fields.keys():
            move(self, 'IILOCountries.mission_location', after='mission_city')
        
        if 'IILOOffices.ilo_offices' in self.fields.keys():
            move(self, 'IILOOffices.ilo_offices', after='mission_members')


        if 'IILOTheme.ilo_themes' in self.fields.keys():
            move(self, 'IILOTheme.ilo_themes', after='mission_location_other')
        if 'IILOTheme.theme_other' in self.fields.keys():
            move(self, 'IILOTheme.theme_other', after='IILOTheme.ilo_themes')

class NameFromTitle(grok.Adapter):
    grok.implements(INameFromTitle)
    grok.context(IMissionReport)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return u'Mission Report'

