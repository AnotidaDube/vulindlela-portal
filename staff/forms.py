from django import forms
from .models import GalleryItem, StudentLifeItem, LeadershipProfile

class GalleryUploadForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'description', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class StudentLifeForm(forms.ModelForm):
    class Meta:
        model = StudentLifeItem
        fields = ['title', 'category', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Soccer Team'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class LeadershipForm(forms.ModelForm):
    class Meta:
        model = LeadershipProfile
        fields = ['name', 'position', 'category', 'image', 'passport_photo', 'bio', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'passport_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order (1=Top)'}),
        }