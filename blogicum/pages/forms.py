from django import forms
from .models import StaticPage


class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ['title', 'content', 'slug', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 10}
            ),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
