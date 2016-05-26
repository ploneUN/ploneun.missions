from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer

from ploneun.missions import MessageFactory as _
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget


# Interface class; used to define content-type schema.

class IMissionFacility(form.Schema, IImageScaleTraversable):
    """
    
    """
    top_result = schema.TextLine(
            title=u'Number of latest Mission Reports to display',
            description=u"If set to 0, all will be displayed.",
            required=False,
            default=u'5')
    pass

alsoProvides(IMissionFacility, IFormFieldProvider)

class missionFacilityAddForm(dexterity.AddForm):
    grok.name('ploneun.missions.missionfacility')
    form.wrap(False)
    
    def updateFields(self):
        super(missionFacilityAddForm, self).updateFields()
        self.fields['IDublinCore.description'].widgetFactory = WysiwygFieldWidget
        return True
    

class missionFacilityEditForm(dexterity.EditForm):
    grok.context(IMissionFacility)
    
    def updateFields(self):
        super(missionFacilityEditForm, self).updateFields()
        self.fields['IDublinCore.description'].widgetFactory = WysiwygFieldWidget
        return True
