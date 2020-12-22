from django import forms
from .models import AgentImage


class ImageUpdateForm(forms.ModelForm):
    code = forms.CharField(max_length=200)
    image = forms.ImageField()

    class Meta:
        model = AgentImage
        fields = ('code', 'image')

