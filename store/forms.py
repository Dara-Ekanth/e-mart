from .models import Review,rate_choices
from django import forms

class review_form(forms.ModelForm):
    rating = forms.ChoiceField(choices=rate_choices,widget=forms.Select(),required=True)
    class Meta:
        model = Review
        fields = ['content']