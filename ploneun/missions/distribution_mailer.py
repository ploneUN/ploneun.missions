from five import grok
from ploneun.missions.content.missionreport import IMissionReport
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from collective.pdfexport.interfaces import IPDFConverter
from zope.component import getUtility
from ploneun.missions.indexer import get_mission
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email import Encoders
from zope.component.interfaces import ComponentLookupError
from Products.CMFPlone.utils import safe_unicode
from plone import api
from zope.component.hooks import getSite
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        return False
    return True

@grok.subscribe(IMissionReport, IAfterTransitionEvent)
def send_distribution_list(obj, event):
    if not event.new_state.id in ['internally_published']:
        return
    #other
    all_email = list()
    report_authors = obj.report_author
    mission_members = []
    if get_mission(obj):
        mission_members = get_mission(obj).mission_members
    mission_distribution = obj.mission_distribution
    
    for md in mission_distribution:
        other_usr = obj.portal_membership.getMemberById(md)
        if other_usr:
            all_email.append(other_usr.getProperty('email'))
    
    distribution_others = obj.mission_distribution_others
    for dist_other in distribution_others:
        if validateaddress(dist_other):
            all_email.append(dist_other)
    

    #creator
    creator = obj.Creator()
    creator_info = obj.portal_membership.getMemberInfo(creator)
    creator_full_name = creator_info['fullname']
    creator_email = obj.portal_membership.getMemberById(creator).getProperty('email')
    all_email.append(creator_email)
    
    #for i in set(report_authors + mission_members + [creator]):
    #    email = obj.portal_membership.getMemberById(i).getProperty('email')
    #    all_email.append(email)

    #all_email.extend(mission_distribution)
    filtered_email = list(set(all_email))
    
    
    converter = getUtility(IPDFConverter)
    import pdb; pdb.set_trace()
    pdf = converter.convert(obj)

    mailhost = obj.MailHost

    if not mailhost:
        raise ComponentLookupError('You must have a Mailhost utility to'
                                   'execute this action')

    from_address = obj.email_from_address
    if not from_address:
        raise ValueError('You must provide a source address for this'
                         'action or enter an email in the portal properties')
    from_name = obj.email_from_name
    source = "%s <%s>" % (from_name, from_address)

    event_title = safe_unicode(safe_unicode(obj.Title()))
    subject = event_title

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source

    body = """You can view the full report online at:

    %(url)s

    --
    This is a system message from %(site_name)s.

    """ % {
        'url': obj.absolute_url(),
        'site_name': getSite().title
    }

    body_safe = body.encode('utf-8')
    htmlPart = MIMEText(body_safe, 'plain', 'utf-8')
    msg.attach(htmlPart)

    # generated pdf attachments

    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(pdf.buf)
    Encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment',
                          filename=subject + '.pdf')
    msg.attach(attachment)

    #attactments in the report
    file_brains = obj.getFolderContents()
    for file_brain in file_brains:
        file = file_brain.getObject().getFile()
        ctype = file.getContentType()
        filename = file.filename
        
        maintype, subtype = ctype.split(('/'), 1)
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(str(file))
        Encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=filename)
        msg.attach(attachment)
    
    for atch in ['attachment1', 'attachment2', 'attachment3', 'attachment4', 'attachment5']:
        attach = getattr(obj, atch)
        if attach:
            ctype = attach.contentType
            filename = attach.filename
            maintype, subtype = ctype.split(('/'), 1)
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(str(attach.data))
            Encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)
        

    #send email
    for recipient in filtered_email:
        # skip broken recipients
        if not recipient:
            continue
        if '@' not in recipient:
            continue

        del msg['To']
        msg['To'] = recipient
        mailhost.send(msg.as_string())
