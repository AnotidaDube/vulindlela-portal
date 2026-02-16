from django import forms
from .models import Mark

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'term', 'score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
