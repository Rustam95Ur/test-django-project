from django import forms
from .models import UploadSetting, GroupSetting


class SettingUpdateForm(forms.ModelForm):
    type_id = forms.IntegerField()
    title = forms.CharField(max_length=100, required=False)
    col_name = forms.CharField(max_length=200)
    type_val = forms.IntegerField(required=False)
    value = forms.CharField(max_length=200, required=False)

    class Meta:
        model = UploadSetting
        fields = ('type_id', 'title', 'value', 'type_val', 'group', 'col_name')


class GroupUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=225)
    is_active = forms.CheckboxInput()

    class Meta:
        model = GroupSetting
        fields = ('title', 'is_active')
