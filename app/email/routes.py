from flask import render_template, flash, redirect, request, url_for, session, current_app
from app.email import bp
from app.email.forms import ChatInvitationForm

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import urllib.parse


@bp.route('/invite_to_chat', methods=['GET', 'POST'])
def invite_to_chat():
    # chatRoom = request.args.get('room')
    # if chatRoom is None:
    #   chatRoom="RitaChatRoom"

    form = ChatInvitationForm()
    name = session.get('name', '')
    room = session.get('room', '')

    
    if form.validate_on_submit():
        thisURL = request.url
        o = urllib.parse.urlsplit(request.url)
        chatURL = o.scheme + "://" + o.hostname + "/?room=" + room 
        print(f"the url in route email.invite_to_chat is {thisURL};  the chat url is {chatURL}")

        from_name = form.from_name.data
        from_email = form.from_email.data
        to_names = form.to_names.data
        to_emails = form.to_emails.data
        send_chat_invitation_email(from_name, from_email, to_names, to_emails, chatURL)
        flash('Your invitation has been sent.  Please close this tab to continue',"success")
        return render_template('email/chat_invitation_sent.html',
                           title='Invitation sent', name=name, room=room, toNames=to_names, toEmails=to_emails )
        

        
    return render_template('email/chat_invitation.html',
                           title='Invite to chat', form=form, name=name, room=room )


def send_chat_invitation_email(from_name, from_email, to_names, to_emails, chatURL):
    
    recipients=[]
    toList = to_emails.split(",")
    for sendTo in toList:
        recipients.append(sendTo)
        
    gmail_send_email('Invitation to chat with me',
            sender=from_email,
            recipients=recipients,
            text_body=render_template('email/email_chat_invitation.txt',chatURL=chatURL, fromName=from_name,  toNames=to_names,),
            html_body=render_template('email/email_chat_invitation.html',chatURL=chatURL,fromName=from_name, toNames=to_names)
            )


def gmail_send_email(subject, sender, recipients, text_body, html_body):
    # Described at this URL  https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
    
    port = os.environ.get('MAIL_PORT')  # For starttls
    smtp_server = os.environ.get('MAIL_SERVER')
    
    sender_email = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')

    receiver_email = recipients
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    # message["To"] = [receiver_email]
    message["To"] = ', '.join(receiver_email)

    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    #context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    connection = smtplib.SMTP(smtp_server, port)
    connection.starttls(context=context)
    connection.login(sender_email, password)

    print(f"\n\n1)  gmail_send_email:  sender_email = {sender_email}")


    connection.sendmail(sender_email, receiver_email, message.as_string())
    
    print(f"\n\n2)  chat_invitation_email:  recipients =  {receiver_email}\n\n")

        





    
