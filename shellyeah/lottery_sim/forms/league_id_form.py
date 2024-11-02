from django import forms

class LeagueForm(forms.Form):
    league_id = forms.CharField(required=True,label='League ID')
