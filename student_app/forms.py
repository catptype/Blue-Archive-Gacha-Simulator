from django import forms
from .models import Student, School
from django.forms import widgets

class StudentAdminForm(forms.ModelForm):
    rarity = forms.TypedChoiceField(
        choices=Student._meta.get_field('rarity').choices,
        widget=forms.RadioSelect(attrs={'class': 'inline-radio'}),
        coerce=int,
        empty_value=None,
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all().order_by('name'),
        empty_label="Select school",  # Set the custom text for the blank choice
        required=True,
    )
    is_limited = forms.TypedChoiceField(
        label="Is limited",
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect(attrs={'class': 'inline-radio'}),
        coerce=lambda x: x == 'True',  # Ensure True/False values are used
        initial=False,
    )
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(), 
        required=False,
    )

    class Meta:
        model = Student
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'admin/widgets/student_preview.html'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
        self.fields['version'].widget.can_add_related = True

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'