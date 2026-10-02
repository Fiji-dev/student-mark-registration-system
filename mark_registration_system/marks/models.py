from django.db import models

class Module(models.Model):
    module_code = models.CharField(max_length=10, unique=True)
    module_name = models.CharField(max_length=100)
    coursework1 = models.FloatField(default=0.0)  # Add default values
    coursework2 = models.FloatField(default=0.0)
    coursework3 = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.module_code} - {self.module_name}"


class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True)  # Ensure the student ID is unique
    student_name = models.CharField(max_length=100)  # Full name of the student
    gender = models.CharField(
        max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')]
    )  # Gender field with choices

    def __str__(self):
        return f"{self.student_id} - {self.student_name}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the student table
    module = models.ForeignKey(Module, on_delete=models.CASCADE)  # Link to the module table
    coursework1 = models.FloatField()  # Marks for coursework 1
    coursework2 = models.FloatField()  # Marks for coursework 2
    coursework3 = models.FloatField()  # Marks for coursework 3
    total_marks = models.FloatField(blank=True, null=True)  # Calculated total marks
    date_of_entry = models.DateField()  # Entry date for the marks

    def save(self, *args, **kwargs):
        # Automatically calculate total marks before saving
        self.total_marks = self.coursework1 + self.coursework2 + self.coursework3
        super().save(*args, **kwargs)

    @property
    def student_name(self):
        return self.student.student_name  # Access the name from the related Student model

    def __str__(self):
        return f"{self.student.student_name} - {self.module.module_code}"



class GenderDistribution(models.Model):
    label = models.CharField(max_length=50)
    count = models.IntegerField()

    def __str__(self):
        return self.label
