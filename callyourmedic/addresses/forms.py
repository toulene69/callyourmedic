__author__ = 'apoorv'


from django import forms
from models import Address

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('address_status',)
