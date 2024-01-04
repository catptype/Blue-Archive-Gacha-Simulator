from django import forms
from .models import Student, School, Version

class StudentAdminForm(forms.ModelForm):
    rarity = forms.TypedChoiceField(
        choices=Student._meta.get_field('rarity').choices,
        widget=forms.RadioSelect(),
        coerce=int,
        empty_value=None,
    )
    version = forms.ModelChoiceField(
        queryset=Version.objects.all(),
        empty_label="Select version",  # Set the custom text for the blank choice
        required=True,
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all().order_by('name'),
        empty_label="Select school",  # Set the custom text for the blank choice
        required=True,
    )
    is_limited = forms.TypedChoiceField(
        label="Is limited",
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect(),
        coerce=lambda x: x == 'True',  # Ensure True/False values are used
        initial=False,
    )
    image = forms.ImageField(
        label="Portrait",
        widget=forms.ClearableFileInput(), 
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'admin/widgets_portrait.html'

    class Meta:
        model = Student
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'