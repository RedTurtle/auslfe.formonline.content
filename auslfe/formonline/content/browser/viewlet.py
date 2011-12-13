# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class WorkflowInfoViewlet(common.ViewletBase):
    """A viewlet for showing Workflow Help infos for Form Online enabled contents"""

    render = ViewPageTemplateFile('workflow_info_viewlet.pt')

    @property
    def portal_workflow(self):
        context = aq_inner(self.context)
        return getMultiAdapter((context, self.request), name=u'plone_tools').workflow()