from django.contrib.auth.models import User
from .models import BookReview, Profile, BookInstance
from django import forms


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class CreateBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back']