from django import forms
from .models import UserProfile

from django import forms as d_forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        type = d_forms.ChoiceField(choices=[("OWNER", "Owner"), ("TENANT", "Tenant")])
        # self.fields['property_owner'] = forms.BooleanField(required=False)
        # self.fields['property_owner'].label = 'Register as property owner ?'
        self.fields['email'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['username'].widget.attrs['autofocus'] = ''

    # def save(self, request):
    #     property_owner = self.cleaned_data.pop('property_owner')
    #     user = super(CustomSignupForm, self).save(request)
    #     return user
    # Put in custom signup logic

    def custom_signup(self, request, user):
        # Set the user's type from the form reponse
        user.type = self.cleaned_data["type"]
        # Save the user's type to their database record
        user.save()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'default_type': 'User Type',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
