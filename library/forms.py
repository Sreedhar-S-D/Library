from django.forms import fields
from library.models import Review
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#d
class ReaderUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
#d
class ReaderForm(forms.ModelForm):
    class Meta:
        model=models.Reader
        fields=['isfaculty','dept','head_shot']
#d
class Reader_PnoForm(forms.ModelForm):
    class Meta:
        model=models.Reader_Pno
        fields=['pnumber']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields='__all__'

class Book_CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Book_Category
        fields=['category']
#
class Book_AuthorForm(forms.ModelForm):
    class Meta:
        model=models.Book_Author
        fields=['author']

class PublisherForm(forms.ModelForm):
    class Meta:
        model=models.Publisher
        fields=['pname','pid','year']

class PublishedByForm(forms.ModelForm):
    class Meta:
        model=models.PublishedBy
        fields=['isbn']

        
class StaffForm(forms.ModelForm):
    class Meta:
        model=models.Staff
        fields=['head_shot']

class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

class KeepsTrackForm(forms.ModelForm):
    class Meta:
        model=models.KeepsTrack
        fields='__all__'
        


class MaintainsForm(forms.ModelForm):
    class Meta:
        model=models.Maintains
        fields='__all__'

class IssuedToForm(forms.ModelForm):
    class Meta:
        model=models.IssuedTo
        fields='__all__'

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100,)
   password = forms.CharField(widget=forms.PasswordInput())

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = [
            'isbn',
            'review'
        ]

