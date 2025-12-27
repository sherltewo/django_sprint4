from django import forms
from .models import Post, Category, Location
from django.utils import timezone
from .models import Comment


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        label='Дата публикации',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now,
        help_text='Установите дату в будущем для отложенной публикации'
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'location', 'image', 'pub_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'category': 'Выберите существующую категорию',
            'location': 'Выберите местоположение (необязательно)',
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(
            is_published=True
        )
        self.fields['location'].queryset = Location.objects.all()
        self.fields['location'].required = False

        if self.instance and self.instance.pk:
            self.fields['pub_date'].initial = self.instance.pub_date

        if hasattr(self, 'delete_mode') and self.delete_mode:
            for field in self.fields:
                self.fields[field].disabled = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            }),
        }
        labels = {
            'text': 'Комментарий'
        }


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'text': 'Редактировать комментарий'
        }
