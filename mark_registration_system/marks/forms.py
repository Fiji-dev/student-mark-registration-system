from django import forms
from django.core.exceptions import ValidationError

# Form for Inputting Marks
class InputMarkForm(forms.Form):
    student_id = forms.CharField(
        max_length=50, 
        label='Student ID', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student ID'})
    )
    student_name = forms.CharField(
        max_length=100, 
        label='Student Name', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student Name'})
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')], 
        label='Gender', 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    module_code = forms.CharField(
        max_length=50, 
        label='Module Code', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Module Code'})
    )
    module_name = forms.CharField(
        max_length=100, 
        label='Module Name', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Module Name'})
    )
    coursework1 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 1', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 1 Marks'})
    )
    coursework2 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 2', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 2 Marks'})
    )
    coursework3 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 3', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 3 Marks'})
    )
    date_of_entry = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label='Date of Entry'
    )

    def clean(self):
        """Custom validation for coursework marks and other fields."""
        cleaned_data = super().clean()

        coursework1 = cleaned_data.get("coursework1")
        coursework2 = cleaned_data.get("coursework2")
        coursework3 = cleaned_data.get("coursework3")

        # Validate total marks if necessary
        if coursework1 is not None and coursework2 is not None and coursework3 is not None:
            total_marks = coursework1 + coursework2 + coursework3
            if total_marks > 300:
                raise ValidationError("Total marks for all coursework cannot exceed 300.")

        return cleaned_data


# Form for Updating Marks
class UpdateMarkForm(forms.Form):
    student_id = forms.CharField(
        max_length=50, 
        label='Student ID', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student ID'})
    )
    module_code = forms.CharField(
        max_length=50, 
        label='Module Code', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Module Code'})
    )
    coursework1 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 1', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 1 Marks'})
    )
    coursework2 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 2', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 2 Marks'})
    )
    coursework3 = forms.IntegerField(
        min_value=0, max_value=100, 
        label='Coursework 3', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coursework 3 Marks'})
    )
    date_of_entry = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label='Date of Entry'
    )

    def clean(self):
        """Custom validation for coursework marks and other fields."""
        cleaned_data = super().clean()

        coursework1 = cleaned_data.get("coursework1")
        coursework2 = cleaned_data.get("coursework2")
        coursework3 = cleaned_data.get("coursework3")

        # Validate total marks if necessary
        if coursework1 is not None and coursework2 is not None and coursework3 is not None:
            total_marks = coursework1 + coursework2 + coursework3
            if total_marks > 300:
                raise ValidationError("Total marks for all coursework cannot exceed 300.")

        return cleaned_data
