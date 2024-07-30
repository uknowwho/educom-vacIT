from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileAllowed

class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))

class ProfileForm(FlaskForm):
    name = StringField('Voornaam', validators=[DataRequired(message="Vul je naam in")])
    last_name = StringField('Achternaam')
    email = StringField('Email', validators=[DataRequired(message="Vul je e-mail in"), Email(message="Vul een geldig e-mailadres in")])
    date_of_birth = DateField('Geboortedatum', format="%Y-%m-%d", validators=[Optional()])
    mobile = StringField('Telefoonnummer', validators=[Optional()])
    address = StringField('Adres', validators=[Optional()])
    postal_code = StringField('Postcode', validators=[Optional()])
    city = StringField('Woonplaats', validators=[Optional()])
    motivation = TextAreaField('Motivatie', validators=[Optional()])
    resume_pdf = FileField('CV (.pdf)', validators=[FileAllowed(['pdf'], 'PDF only!')])
    submit = SubmitField('Opslaan')
