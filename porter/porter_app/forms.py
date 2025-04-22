from django import forms
from .models import MyUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserSignupForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=MyUser.user_types)
    adhar_no = forms.CharField(max_length=16, required=False)
    bank_account_number = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up'))
