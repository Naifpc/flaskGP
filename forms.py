from wtforms import Form, StringField, PasswordField,validators,SubmitField

class AccountForm(Form):
    username = StringField('username', [validators.length(min=3, max=25)])
    password = PasswordField('password', [validators.length(min=4, max=25)])
    submit = SubmitField('submit')
class UserForm(Form):
    username = StringField('username', [validators.length(min=3, max=25)])
    submit = SubmitField('submit')