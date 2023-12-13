from django import forms
from .models import Student, School, GachaBanner
from django.forms import widgets
from django.core.exceptions import ValidationError

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
        widgets = {
            'rarity': widgets.RadioSelect,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'admin/widgets/clearable_file_input_with_preview.html'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

class GachaBannerAdminForm(forms.ModelForm):


    # Override widgets for rate fields
    rate_widget = forms.TextInput(attrs={'type': 'number', 'step': '0.5', 'value': '0.0', 'min': '0.0', 'max': '100.0'})

    rate_3_star = forms.DecimalField(widget=rate_widget)
    rate_2_star = forms.DecimalField(widget=rate_widget)
    rate_1_star = forms.DecimalField(widget=rate_widget)

    def clean(self):
        cleaned_data = super().clean()

        rate_3_star = cleaned_data.get('rate_3_star')
        rate_2_star = cleaned_data.get('rate_2_star')
        rate_1_star = cleaned_data.get('rate_1_star')

        is_pickup = cleaned_data.get('is_pickup')
        not_pickup = cleaned_data.get('not_pickup')

        # Ensure that students in is_pickup and not_pickup are distinct
        common_students = is_pickup & not_pickup
        print(common_students)
        if common_students:
            raise ValidationError("The students in is_pickup and not_pickup.")

        # Ensure that the sum of rates is equal to 100%
        total_rate = rate_3_star + rate_2_star + rate_1_star
        if total_rate != 100.0:
            raise ValidationError("The sum of rates must equal 100%.")
    
    class Meta:
        model = GachaBanner
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
