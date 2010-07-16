from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_base, aq_parent
from auslfe.formonline.content import formonline_contentMessageFactory as _
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
from email.MIMEText import MIMEText
from Products.CMFPlone.utils import safe_unicode
import socket
from Products.CMFPlone.utils import log_exc, log
from email.Utils import parseaddr, formataddr
from email.MIMEMultipart import MIMEMultipart

def getTextIfPendingApproval():
    mailText = '<p>Dear user,<br />this is a personal communication regarding the Form Online: <strong>${formonline_title}</strong>, placed on: ${insertion_date}, by the user ${formonline_owner}.</p><p>It is waiting for your approval. Following the link to the Form Online you can make your changes.</p><p>Link to Form Online: <a class="reference" href="${formonline_url}">${formonline_url}</a>,</p><p>kind regards</p>'
    return mailText

def getTextIfPendingDispatch():
    mailText = '<p>Dear user,<br />this is a personal communication regarding the Form Online: <strong>${formonline_title}</strong>, placed on: ${insertion_date}, by the user ${formonline_owner}.</p><p>It is waiting for dispatch. Following the link to the Form Online you can make your changes.</p><p>Link to Form Online: <a class="reference" href="${formonline_url}">${formonline_url}</a>,</p><p>kind regards</p>'
    return mailText

def formOnlineNotificationMail(formonline,event):
    """
    When the state of a Form Online changes in one of the states in ['pending_approval','pending_dispatch'], send a notification email.
    """
    portal_workflow = getToolByName(formonline,'portal_workflow')
    review_state = portal_workflow.getInfoFor(formonline,'review_state')
    
    addresses = []
    text = ''
    
    if review_state == 'pending_approval':
        addresses = getAddresses('Editor',formonline)
        text = getTextIfPendingApproval()
    elif review_state == 'pending_dispatch':
        addresses = getAddresses('Reviewer',formonline)
        text = getTextIfPendingDispatch()
    
    if addresses:
        sendNotificationMail(formonline,text,addresses)
    
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
    users = []
    for user,roles,role_type,name in globals_roles:
        if role in roles:
            users.append(pm.getMemberById(user).getProperty('email'))
    return users

def sendNotificationMail(formonline,text,addresses):
    
    portal_url = getToolByName(formonline, 'portal_url')
    portal = portal_url.getPortalObject()
    portal_membership = getToolByName(portal, 'portal_membership')
    
    plone_utils = getToolByName(portal, 'plone_utils')
    charset = plone_utils.getSiteEncoding()
    def su(value):
        return safe_unicode(value, encoding=charset)
    
    formonlineCreator = formonline.Creator()
    formonlineCreatorInfo = portal_membership.getMemberInfo(formonlineCreator)
    formonlineAuthor = formonlineCreator
    if formonlineCreatorInfo:
        formonlineAuthor = formonlineCreatorInfo['fullname'] or formonlineCreator

    insertion_date = formonline.toLocalizedTime(formonline.created())
    
    mailText = _('formonline_notification_email', text, mapping=dict(formonline_title = su(formonline.title_or_id()),
                                                                     insertion_date = su(insertion_date),
                                                                     formonline_owner = su(formonlineAuthor),
                                                                     formonline_url = su(formonline.absolute_url()),
                                                                     ))
    
    subject = u"[%s] - %s" % (su('Modulistica Online'),su('Comunicazione personale'))
    
    sendEmail(formonline, addresses, subject, mailText)
        
def sendEmail(formonline, addresses, subject, rstText, cc = None):
    """
    Send a email to the list of addresses
    """
    portal_url  = getToolByName(formonline, 'portal_url')
    plone_utils = getToolByName(formonline, 'plone_utils')

    portal      = portal_url.getPortalObject()
    mailHost    = plone_utils.getMailHost()
    charset     = portal.getProperty('email_charset', '')
    if not charset:
        charset = plone_utils.getSiteEncoding()
        
    from_address = portal.getProperty('email_from_address', '')

    if not from_address:
        log('Cannot send notification email: email sender address not set')
        return
    
    from_name = portal.getProperty('email_from_name', '')

    mfrom = formataddr((from_name, from_address))
    if parseaddr(mfrom)[1] != from_address:
        # formataddr probably got confused by special characters.
        mfrom - from_address


    email_msg = MIMEMultipart('alternative')
    email_msg.epilogue = ''

    # Translate the body text
    ts = getGlobalTranslationService()
    rstText = ts.translate('formonline_notification_email', rstText, context=formonline)
    # We must choose the body charset manually
    for body_charset in 'US-ASCII', charset, 'UTF-8':
        try:
            rstText = rstText.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    textPart = MIMEText(rstText, 'plain', body_charset)
    email_msg.attach(textPart)
    
    render_html= renderBodyHTML(rstText)
    
    htmlPart = MIMEText(render_html,
                        'html', body_charset)
    email_msg.attach(htmlPart)

    subject = safe_unicode(subject, charset)
    
    formonline.plone_log("INVIO EMAIL a: %s" % ", ".join(addresses))
    
    for address in addresses:
        address = safe_unicode(address, charset)
        try:
            # Note that charset is only used for the headers, not
            # for the body text as that is a Message already.
            mailHost.secureSend(message = email_msg,
                                mto = address,
                                mcc = cc,
                                mfrom = mfrom,
                                subject = subject,
                                charset = charset)
        except socket.error, exc:
            log_exc(('Could not send email from %s to %s regarding issue '
                     'in tracker %s\ntext is:\n%s\n') % (
                    mfrom, address, formonline.absolute_url(), email_msg))
            log_exc("Reason: %s: %r" % (exc.__class__.__name__, str(exc)))
        except:
            raise

def renderBodyHTML(rstText, lang='en', charset='utf-8'):
    """Convert the body HTML into a full XHTML transitional document.
    """

    kwargs = {'lang': lang,
              'charset': charset,
              'body': rstText,
              }
    
    return htmlTemplate % kwargs

htmlTemplate = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xml:lang="%(lang)s"
      lang="%(lang)s">

  <head>
     <meta http-equiv="Content-Type" content="text/html; charset=%(charset)s" />

    <style type="text/css" media="all">
<!--
BODY {
    font-size: 0.9em;
}

H4 {
    font-size: 1.2em;
    font-weight: bold;
}

DT {
    font-weight: bold;
}
-->
    </style>

  </head>


  <body>
%(body)s
  </body>
</html>
"""