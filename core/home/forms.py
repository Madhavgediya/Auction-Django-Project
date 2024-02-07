from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']  # Include 'confirm_password' in fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Password and confirm password do not match.")

        return cleaned_data



class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', max_digits=10, decimal_places=2)
 