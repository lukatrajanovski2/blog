from django import forms
from .models import Post, Comment

# 1. Формата за нов пост / пријава
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image') # Тргната е images бидејќи ја правиме преку JavaScript

# 2. Формата за коментари (Оваа фалеше и затоа пукна серверот!)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': forms.TextInput(attrs={
                'placeholder': 'Твоето име / прекар (или остави празно за Анонимен)', 
                'style': 'width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Сподели го твоето искуство со овој скемер...', 
                'rows': 3, 
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px;'
            }),
        }