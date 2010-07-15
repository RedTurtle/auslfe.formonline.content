from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_base, aq_parent

def formOnlineNotificationMail(formonline,event):
    """
    When the state of a Form Online changes in one of the states in ['pending_approval','pending_dispatch'], send a notification email.
    """
    portal_workflow = getToolByName(formonline,'portal_workflow')
    review_state = portal_workflow.getInfoFor(formonline,'review_state')
    
    addresses = []
    
    if review_state == 'pending_approval':
        addresses = getAddresses('Editor',formonline)
    elif review_state == 'pending_dispatch':
        addresses = getAddresses('Reviewer',formonline)
    
    if addresses:
        sendNotificationMail(formonline,review_state,addresses)
    
def get_inherited(formonline):
    """Return True if local roles are inherited here.
    """
    if getattr(aq_base(formonline), '__ac_local_roles_block__', None):
        return False
    return True

def get_global_roles(formonline):
    """Returns a tuple with the acquired local roles."""
    formonline = aq_inner(formonline)
    
    if not get_inherited(formonline):
        return []
    
    portal = getToolByName(formonline, 'portal_url').getPortalObject()
    result = []
    
    local_roles = formonline.acl_users._getLocalRolesForDisplay(formonline)
    for user, roles, role_type, name in local_roles:
        result.append([user, list(roles), role_type, name])
    
    cont = True
    if portal != formonline:
        parent = aq_parent(formonline)
        while cont:
            if not getattr(parent, 'acl_users', False):
                break
            userroles = parent.acl_users._getLocalRolesForDisplay(parent)
            for user, roles, role_type, name in userroles:
                # Find user in result
                found = 0
                for user2, roles2, type2, name2 in result:
                    if user2 == user:
                        # Check which roles must be added to roles2
                        for role in roles:
                            if not role in roles2:
                                roles2.append(role)
                        found = 1
                        break
                if found == 0:
                    # Add it to result and make sure roles is a list so
                    # we may append and not overwrite the loop variable
                    result.append([user, list(roles), role_type, name])
            if parent == portal:
                cont = False
            elif not get_inherited(parent):
                # Role acquired check here
                cont = False
            else:
                parent = aq_parent(parent)

    # Tuplize all inner roles
    for pos in range(len(result)-1,-1,-1):
        result[pos][1] = tuple(result[pos][1])
        result[pos] = tuple(result[pos])

    return tuple(result)

def getAddresses(role,formonline):
    """Returns a list of email of users with a specific role on a Form Online content, from a local roles structure."""
    pm = getToolByName(formonline,'portal_membership')
    globals_roles = get_global_roles(formonline)
    print globals_roles
    users = []
    for user,roles,role_type,name in globals_roles:
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