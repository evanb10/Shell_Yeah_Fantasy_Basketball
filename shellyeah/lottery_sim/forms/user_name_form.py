from django import forms

class UserNameForm(forms.Form):
   user_name = forms.CharField(required = True, label="User Name", widget=forms.TextInput(
       attrs = {
           'class':'form-control',
           'type':'text',
           'placeholder':'User Name',
       }
   ),
       error_messages = {
           'required' : "This field is required",
           'invalid' : "This field is invalid",
   })

   def clean(self):
       cleaned_data = super().clean()
       #Do Stuff