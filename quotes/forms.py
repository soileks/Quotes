from django import forms
from .models import Quote, Source

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'type', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название фильма или книги'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год выпуска'}),
        }
        labels = {
            'title': 'Название',
            'type': 'Тип',
            'year': 'Год',
        }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите текст цитаты'
            }),
            'source': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'value': 1
            }),
        }
        labels = {
            'text': 'Текст цитаты',
            'source': 'Источник',
            'weight': 'Вес (1-10)',
        }