from Products.CMFCore.utils import getToolByName

def formOnlineNotificationMail(formonline,event):
    """
    When the state of a Form Online changes in one of the states in ['pending_approval','pending_dispatch'], send a notification email.
    """
    
    #import pdb;pdb.set_trace()
    
    portal_workflow = getToolByName(formonline,'portal_workflow')
    review_state = portal_workflow.getInfoFor(formonline,'review_state')
    
    addresses = []
    
    if review_state == 'pending_approval':
        addresses = getAddresses('Editor',formonline)
    elif review_state == 'pending_dispatch':
        addresses = getAddresses('Reviewer',formonline)
    
    if addresses:
        sendNotificationMail(formonline,review_state,addresses)

def getAddresses(role,formonline):
    """Returns a list of email of users with a specific role on a Form Online content, from a local roles structure."""
    pm = getToolByName(formonline,'portal_membership')    
    local_roles = formonline.get_local_roles()
    users = []
    for user,roles in local_roles:
        if role in roles:
            users.append(pm.getMemberById(user).getProperty('email'))
    return users

def sendNotificationMail(formonline,review_state,addresses):

    pass
    

#    watchers_managers = tracker.getWatchersManagersEmailAddresses(issue)
#    
#    portal_url = getToolByName(issue, 'portal_url')
#    portal = portal_url.getPortalObject()
#    portal_membership = getToolByName(portal, 'portal_membership')
#    
#    issueCreator = issue.Creator()
#    issueCreatorInfo = portal_membership.getMemberInfo(issueCreator)
#    issueAuthor = issueCreator
#    if issueCreatorInfo:
#        issueAuthor = issueCreatorInfo['fullname'] or issueCreator
#        segnalatore = portal_membership.getMemberById(issueCreator)
#        issueCreatorEmail = issue.getContactEmail() or segnalatore.getProperty('email') or None
#
#    addresses = ()
#    creator = response.creator
#    if creator == issue.responsibleManager:
#        if issueCreatorInfo:
#            addresses=(issueCreatorEmail,)
#        else:
#            addresses=(issue.getContactEmail(),)
#        cc = watchers_managers
#    else:
#        addresses = watchers_managers
#        cc = None
#        
#    plone_utils = getToolByName(portal, 'plone_utils')
#
#    charset = plone_utils.getSiteEncoding()
#
#    # We are going to use the same encoding everywhere, so we will
#    # make that easy.
#
#    def su(value):
#        return safe_unicode(value, encoding=charset)
#    
#    if creator == issue.responsibleManager:
#        fromName = None
#    else:
#        fromName = su(issueAuthor)
#
#    creatorInfo = portal_membership.getMemberInfo(creator)
#    if creatorInfo and creatorInfo['fullname']:
#        responseAuthor = creatorInfo['fullname']
#    else:
#        responseAuthor = creator
#    
#    responseAuthor = su(responseAuthor)
#    responseText = su(response.text)
#    paras = responseText.split(u'\n\n')[:2]
#    wrapper = textwrap.TextWrapper(initial_indent=u'    ',
#                                   subsequent_indent=u'    ')
#    responseDetails = u'\n\n'.join([wrapper.fill(p) for p in paras])
#    
#    responseDetails = responseDetails.strip()
#    responseDetails = responseText
#    
#    if creator == issue.responsibleManager:
#        text = getTextIfManager()
#    else:
#        text = getTextIfNoManager()
#
#    data_inserimento = issue.toLocalizedTime(issue.created())                                               
#    
#    issueText = issue.getDetails(mimetype="text/x-web-intelligent")
#    parasIssueText = issueText.split('\n\n')[:2]
#    issueDetails = '\n\n'.join([wrapper.fill(p) for p in parasIssueText])
#        
#    mailText = _('poi_email_new_response_template', text, mapping=dict(
#                                                                        issue_author = su(issueAuthor),
#                                                                        issue_title = su(issue.title_or_id()),
#                                                                        response_author = responseAuthor,
#                                                                        response_details = responseDetails,
#                                                                        issue_details = issueDetails,
#                                                                        issue_url = su(issue.absolute_url()),
#                                                                        data_inserimento = su(data_inserimento),
#                                                                        data_invio = su(DateTime().Date()),
#                                                                        issue_number = su(issue.id),
#                                                                        ))
#
#    if creator == issue.responsibleManager:
#        subject = u"[%s] - %s" % (su(tracker.getExternalTitle()),
#                                      su('Comunicazione personale'))
#    else:
#        subject = u"[%s] - Re: %s" % (su(tracker.getExternalTitle()),
#                                      su('Comunicazione personale'))
#    
#    tracker.sendNotificationEmail(addresses, subject, mailText, directHTMLbody=True, cc=cc, from_name=fromName)
#        
#
#def getTextIfManager():
#
#    mailText = '<p>Gentile utente <strong>${formonline_overseer}</strong>,<br />questa e\' una comunicazione personale relativa alla Modulistica Online: <strong>${formonline_title}</strong>, inserita in data: ${data_inserimento}, dall\'utente ${formonline_owner}</p>.<p>La informiamo che essa è in attesa della Sua approvazione. Seguendo il link alla modulistica online Le sara\' possibile effetturare le proprie modifiche.</p><p>Link alla modulistica online: <a class="reference" href="${formonline_url}">${formonline_url}</a></p><p>Cordiali saluti</p>'
#    return mailText
#
#
#def getTextIfNoManager():
#
#    mailText = '<p>Gentile utente <strong>${formonline_reviewer}</strong>,<br />questa e\' una comunicazione personale relativa alla Modulistica Online: <strong>${formonline_title}</strong>, inserita in data: ${data_inserimento}, dall\'utente ${formonline_owner}</p>.<p>La informiamo che essa è in attesa di evasione. Seguendo il link alla modulistica online Le sara\' possibile effetturare le proprie revisioni.</p><p>Link alla modulistica online: <a class="reference" href="${formonline_url}">${formonline_url}</a></p><p>Cordiali saluti</p>'
#    return mailText