# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
    PLONE3 = True
except ImportError:
    PLONE3 = False

TYPES_TO_VERSION = ('FormOnline',)

def setupVarious(context):

    if context.readDataFile('auslfe.formonline.content_various.txt') is None:
        return


def setVersionedTypes(context):
    '''
    Setup handler to put under version control the specified portal types
    
    '''

    if PLONE3:
        if context.readDataFile('auslfe.formonline.content_types.txt') is None:
            return
    
        portal=context.getSite()
        portal_repository = getToolByName(portal, 'portal_repository')
        versionable_types = list(portal_repository.getVersionableContentTypes())
        for type_id in TYPES_TO_VERSION:
            if type_id not in versionable_types:
                # use append() to make sure we don't overwrite any
                # content-types which may already be under version control
                versionable_types.append(type_id)
                # Add default versioning policies to the versioned type
                for policy_id in DEFAULT_POLICIES:
                    portal_repository.addPolicyForContentType(type_id, policy_id)
         
        portal_repository.setVersionableContentTypes(versionable_types)
