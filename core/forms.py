from django import forms
from django.core.exceptions import ValidationError
from . import models

class NavbarItemForm(forms.ModelForm):
    class Meta:
        model = models.NavbarItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_button = cleaned_data.get('is_button')
        parent = cleaned_data.get('parent')

        if is_button and parent is not None:
            raise ValidationError("Button items cannot have a parent.")

        if is_button:
            # Check children if this is an existing instance
            if self.instance.pk:
                children = self.instance.children.all()
                if children.exists():
                    raise ValidationError("Button items cannot have children.")

        if parent and parent.is_button:
            raise ValidationError("Non-button items cannot have a button as parent.")

        return cleaned_data
