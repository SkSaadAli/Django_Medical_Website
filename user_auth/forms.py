from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder':'Type the username'
        })
        
        self.fields['password'].widget.attrs.update({
            'type':'password',
            'placeholder':'Type password'
        })
        self.fields['password_confirm'].widget.attrs.update({
            'placeholder':'confirm password'
        })
        self.fields['profile_picture'].widget.attrs.update({
            'placeholder':'Select the profile Picture'
        })
        self.fields['profile_type'].widget.attrs.update({
            'placeholder':'Select the profile type'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder':'xyz@example.com'
        })
        self.fields['address_line1'].widget.attrs.update({
            'placeholder':'Address Line 1'
        })
        self.fields['city'].widget.attrs.update({
            'placeholder':'City'
        })
        # self.fields['state'].widget.attrs.update({
        #     'placeholder':'State'
        # })
        self.fields['pincode'].widget.attrs.update({
            'placeholder':'Pincode'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder':'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder':'Last Name'
        })
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_type', 'profile_picture', 'username', 'email', 'password', 'password_confirm', 'address_line1', 'city', 'pincode']


