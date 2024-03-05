from wtforms import Form, StringField, PasswordField,validators,SubmitField

class UserForm(Form):
    username = StringField('Username', [validators.length(min=3, max=25)])
    password = PasswordField('Password', [validators.length(min=4, max=25)])
    submit = SubmitField('Submit')