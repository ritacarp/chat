from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, email_validator, EqualTo, ValidationError
import re



class ChatInvitationForm(FlaskForm):
    from_name = StringField('From Name', validators=[DataRequired()])
    from_email = StringField('From Email', validators=[DataRequired()])
    to_names = StringField('To Names', validators=[DataRequired()])
    to_emails = StringField('To Emails', validators=[DataRequired()])
    submit = SubmitField('Send invitation to chat')


    def validate_from_email(form, field):
        # pass the regular expression 
        # and the string in search() method 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(not re.search(regex,field.data)):
            note = f"{field.data} is not a valid email address."
            field.errors.append(note)
            # raise ValidationError('From Email address is not valid')


    def validate_to_emails(form, field):
        # pass the regular expression 
        # and the string in search() method 
        isValid = True
        toList = field.data.split(",")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        
        for sendTo in toList:
            if(not re.search(regex,sendTo.strip())):
                isValid = False
                note = f"{sendTo} is not a valid email address."
                field.errors.append(note)

        #if not isValid:
        #    raise ValidationError(field.errors)
