from django import forms
from django.core.exceptions import ValidationError

from .models import GachaBanner, GachaTransaction, GachaType
from student_app.models import Student

from django.contrib.admin.widgets import FilteredSelectMultiple

class GachaTypeAdminForm(forms.ModelForm):
    # Override widgets for rate fields
    rate_widget = forms.TextInput(attrs={
        'type': 'number', 
        'step': '0.5', 
        'value': '0.0', 
        'min': '0.0', 
        'max': '100.0',
    })

    pickup_rate = forms.DecimalField(widget=rate_widget)
    r3_rate = forms.DecimalField(widget=rate_widget)
    r2_rate = forms.DecimalField(widget=rate_widget)
    r1_rate = forms.DecimalField(widget=rate_widget)

    def clean(self):
        cleaned_data = super().clean()

        # Ensure that the sum of rates is equal to 100%
        total_rate = sum(cleaned_data.get(f'r{i}_rate', 0) for i in [3, 2, 1])
        if total_rate != 100.0:
            raise ValidationError({
                'r3_rate': f"The sum of rates must be 100%. (Current sum: {total_rate})",
                'r2_rate': f"The sum of rates must be 100%. (Current sum: {total_rate})",
                'r1_rate': f"The sum of rates must be 100%. (Current sum: {total_rate})",
            })
        
        # Ensure that pickup_rate must less than r3_rate
        if cleaned_data.get('pickup_rate') >= cleaned_data.get('r3_rate'):
            raise ValidationError({
                'pickup_rate': "The pickup rate must be less than the r3 rate ",
            })
        
    class Meta:
        model = GachaType
        fields = '__all__'

class GachaBannerAdminForm(forms.ModelForm):

    image = forms.ImageField(
        label="Portrait",
        widget=forms.ClearableFileInput(), 
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'admin/widgets_banner.html'

        existing_not_pickup_id = [student.id for student in self.initial.get('not_pickup', [])]
        self.fields['is_pickup'].label = 'Pickup 3★ Students'
        self.fields['is_pickup'].queryset = Student.objects.filter(rarity=3).exclude(id__in=existing_not_pickup_id).order_by('name')

        existing_pickup_id = [student.id for student in self.initial.get('is_pickup', [])]
        self.fields['not_pickup'].label = 'Available Students'
        self.fields['not_pickup'].queryset = Student.objects.exclude(id__in=existing_pickup_id).order_by('-rarity', 'name', 'version')
    
    def clean(self):
        cleaned_data = super().clean()

        is_pickup = cleaned_data.get('is_pickup')
        not_pickup = cleaned_data.get('not_pickup')

        # Ensure that students in is_pickup and not_pickup are distinct
        common_students = is_pickup & not_pickup
        if common_students:
            raise ValidationError({
                'is_pickup': "A student cannot be marked for both pickup and not pickup.",
                'not_pickup': "A student cannot be marked for both pickup and not pickup.",
            })

    class Meta:
        model = GachaBanner
        fields = '__all__'
        widgets = {
            'is_pickup': FilteredSelectMultiple('★★★ students', is_stacked=False),
            'not_pickup': FilteredSelectMultiple('students', is_stacked=False),
        }

class GachaTransactionAdminForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        banner = cleaned_data.get('banner')
        student = cleaned_data.get('student')

        is_student_pickup = student in banner.is_pickup.all()
        is_student_not_pickup = student in banner.not_pickup.all()

        if not (is_student_pickup or is_student_not_pickup):
            raise ValidationError(f'{student} is not in {banner}, CHEATER!')

    class Meta:
        model = GachaTransaction
        fields = '__all__'