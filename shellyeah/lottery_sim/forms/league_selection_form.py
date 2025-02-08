# forms.py
from django import forms
from django.utils.safestring import mark_safe

class LeagueSelectionForm(forms.Form):
    selected_league = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[]  # We’ll populate choices dynamically in the view.
    )
