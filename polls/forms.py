from django import forms
from .models import *

class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ("image","name","content","author",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("by","rating","description")
        widgets = {'description':forms.TextInput(attrs={'class':'form-control','textholder':'your experience'})}

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("product","details","phone_number","address","confirm",)
        widgets = {'details':forms.TextInput(attrs={'class':'form-control','textholder':'details for your order'}),
                   'phone_number':forms.TextInput(attrs={'class':'form-control','textholder':'your phone number for contact'}),
                   'address':forms.TextInput(attrs={'class':'form-control','textholder':'your deleviery address'})}
