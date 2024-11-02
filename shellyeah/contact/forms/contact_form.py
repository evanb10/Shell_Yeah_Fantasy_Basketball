from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    subject = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'What\'s On Your Mind?', 'style': 'width: 300px;', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'sample@email.com', 'style': 'width: 300px;', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Tell me more...', 'style': 'width: 300px;', 'class': 'form-control'}))