# forms.py
from django import forms

class PercentageAllocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        teams = kwargs.pop('teams')# if 'teams' in kwargs else None # Get teams data

        super(PercentageAllocationForm, self).__init__(*args, **kwargs)

        # if teams is not None:
        for team in teams:
            print(team)
            self.fields[f'percentage_{team.name}'] = forms.DecimalField(
                label=team.name, min_value=0, max_value=100, required=True, initial=team.odds,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
