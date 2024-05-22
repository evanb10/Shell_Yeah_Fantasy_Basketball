from django import forms
from ..models import Manager

class PlayerForm(forms.Form):
    on_roster = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    # https://stackoverflow.com/questions/19947538/django-form-with-unknown-number-of-checkbox-fields-and-multiple-actions
    # https://django-users.narkive.com/SwhaRqpM/beginner-creating-a-form-with-variable-number-of-checkboxes
    # Define choices for radio buttons (including Lamp Shade)
    # MANAGER_CHOICES = [('None', '--- None ---')] + [
    #     (manager.pk, manager.display_name) for manager in Manager.objects.all()
    # ]
    # No longer using the above method as makemigrations did not work
    # Moved the DB query to __init__ as suggested by @Nate:
    # https://stackoverflow.com/questions/39535983/migration-clashes-with-forms-py
    managers = forms.ChoiceField(
        choices=[('','')],
        widget=forms.RadioSelect,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)

        # Load choices here so db calls are not made during migrations.
        self.fields['managers'].choices = [('None', '-- None --')] + [(manager.pk, manager.display_name) for manager in Manager.objects.all()]