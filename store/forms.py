from .models import Review
from django.forms import ModelForm

class review_form(ModelForm):
    class Meta:
        model = Review
        fields = ['content']