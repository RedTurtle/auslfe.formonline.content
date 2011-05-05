"""Definition of the FormOnline content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import ATDocument, ATDocumentSchema

from auslfe.formonline.content.interfaces import IFormOnline
from auslfe.formonline.content.config import PROJECTNAME

FormOnlineSchema = ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

FormOnlineSchema['title'].storage = atapi.AnnotationStorage()
FormOnlineSchema['description'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
FormOnlineSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(FormOnlineSchema, moveDiscussion=False)

class FormOnline(ATDocument):
    """Description of the Example Type"""
    implements(IFormOnline)

    meta_type = "FormOnline"
    schema = FormOnlineSchema
    
    _at_rename_after_creation = False # is better to keep autocreated ids

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(FormOnline, PROJECTNAME)
