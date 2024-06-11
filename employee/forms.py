from django import forms
from .models import Document, SignedContract

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['aadhaar_card', 'pan_card', 'light_bill', 'photo']

class SignedContractUploadForm(forms.ModelForm):
    class Meta:
        model = SignedContract
        fields = ['contract', 'signature']