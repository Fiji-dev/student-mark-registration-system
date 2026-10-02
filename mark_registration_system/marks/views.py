from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Student, Module, Mark
from .forms import InputMarkForm, UpdateMarkForm
from datetime import datetime
import json
from django.contrib.auth.views import LoginView


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to 'next' if it exists, else to home
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            return render(request, 'marks/login.html', {'error': 'Invalid username or password'})
    return render(request, 'marks/login.html')

# Home View
@login_required
def home(request):
    """Render the homepage with the count of students and modules."""
    num_students = Student.objects.count()
    num_modules = Module.objects.count()

    # Fetch recent activities or updates (e.g., latest marks added)
    recent_marks = Mark.objects.order_by('-date_of_entry')[:5]

    return render(request, "marks/home.html", {
        "num_students": num_students,
        "num_modules": num_modules,
        "recent_marks": recent_marks,  # Pass recent marks to the template
    })


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login')

def signup_view(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'marks/signup.html', {'form': form})

def input_mark(request):
    """Handle input of marks for students."""
    message = ""
    status = ""

    if request.method == 'POST':
        form = InputMarkForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Create or retrieve the student
            student, created = Student.objects.get_or_create(
                student_id=cleaned_data['student_id'],
                defaults={
                    'student_name': cleaned_data['student_name'],
                    'gender': cleaned_data['gender']
                }
            )

            # Check if the student name matches in case of an existing student
            if not created and student.student_name != cleaned_data['student_name']:
                message = f"Student ID {student.student_id} is already assigned to another name."
                status = "error"
                return render(request, 'marks/input_mark.html', {
                    'status': status,
                    'message': message,
                    'form': form,
                })

            # Create or retrieve the module
            module, created = Module.objects.get_or_create(
                module_code=cleaned_data['module_code'],
                defaults={
                    'module_name': cleaned_data['module_name']
                }
            )

            # Add or update the mark entry
            mark, created = Mark.objects.get_or_create(
                student=student,
                module=module,
                date_of_entry=cleaned_data['date_of_entry'],
                defaults={
                    'coursework1': cleaned_data['coursework1'],
                    'coursework2': cleaned_data['coursework2'],
                    'coursework3': cleaned_data['coursework3'],
                }
            )

            if not created:
                message = f"Marks for Student ID {student.student_id} in Module {module.module_code} already exist."
                status = "error"
            else:
                message = "Marks successfully added."
                status = "success"
        else:
            message = "Invalid form data."
            status = "error"
    else:
        form = InputMarkForm()

    return render(request, 'marks/input_mark.html', {
        'status': status,
        'message': message,
        'form': form,
    })

# Update Mark View
def update_mark(request):
    """Handle updates to marks for students."""
    message = ""
    status = ""

    if request.method == 'POST':
        form = UpdateMarkForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            try:
                # Find the mark entry to update
                mark = Mark.objects.get(
                    student__student_id=cleaned_data['student_id'],
                    module__module_code=cleaned_data['module_code'],
                    date_of_entry=cleaned_data['date_of_entry']
                )
                mark.coursework1 = cleaned_data['coursework1']
                mark.coursework2 = cleaned_data['coursework2']
                mark.coursework3 = cleaned_data['coursework3']
                mark.save()

                message = "Marks updated successfully."
                status = "success"
            except Mark.DoesNotExist:
                message = "No matching record found for the given details."
                status = "error"
        else:
            message = "Invalid form data."
            status = "error"
    else:
        form = UpdateMarkForm()

    return render(request, "marks/update_mark.html", {
        "status": status,
        "message": message,
        "form": form,
    })

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Mark

def view_mark(request):
    """Display marks for a specific module with pagination and filtering."""
    module_code = request.GET.get('module_code')
    page = request.GET.get('page', 1)

    if not module_code:
        return render(request, 'marks/view_mark.html', {
            'status': 'error',
            'message': 'Module code is required'
        })

    # Fetch marks and include related student and module details
    marks = Mark.objects.filter(module__module_code__icontains=module_code).select_related('student', 'module').order_by('id')

    if not marks.exists():
        return render(request, 'marks/view_mark.html', {
            'status': 'error',
            'message': f'No marks found for module code: {module_code}'
        })

    # Add pagination
    paginator = Paginator(marks, 10)  # Show 10 marks per page
    paginated_marks = paginator.get_page(page)

    # Prepare the marks data for the template
    marks_data = [
        {
            'student_id': mark.student.student_id,
            'student_name': mark.student.student_name,
            'coursework1': mark.coursework1,
            'coursework2': mark.coursework2,
            'coursework3': mark.coursework3,
            'total_marks': mark.total_marks,
            'module_code': mark.module.module_code,
        }
        for mark in paginated_marks
    ]

    return render(request, 'marks/view_mark.html', {
        'marks': marks_data,
        'module_code': module_code,
        'paginator': paginated_marks,
    })

from django.shortcuts import render
from django.db.models import Count
from .models import Module, Mark, Student  # Import models directly

import json

def visualization_view(request):
    # Fetch data for the bar chart, line chart, and stacked bar chart
    modules = Module.objects.all()
    marks = Mark.objects.all()

    # Bar Chart: Total marks per module
    bar_chart_data = {
        "labels": [module.module_name for module in modules],
        "total_marks": [
            sum(
                mark.coursework1 + mark.coursework2 + mark.coursework3
                for mark in marks.filter(module=module)
            )
            for module in modules
        ],
    }

    # Line Chart: Total marks over time (grouped by date of entry)
    line_chart_labels = sorted(
        {mark.date_of_entry for mark in marks}
    )  # Unique dates sorted
    line_chart_data = {
        "labels": [str(date) for date in line_chart_labels],
        "total_marks": [
            sum(
                mark.coursework1 + mark.coursework2 + mark.coursework3
                for mark in marks.filter(date_of_entry=date)
            )
            for date in line_chart_labels
        ],
    }

    # Pie Chart: Gender distribution
    gender_distribution = Student.objects.values("gender").annotate(count=Count("gender"))
    pie_chart_data = {
        "labels": [entry["gender"] for entry in gender_distribution],
        "values": [entry["count"] for entry in gender_distribution],
    }

    # Stacked Bar Chart: Coursework marks per module
    stacked_bar_chart_data = {
        "labels": [module.module_name for module in modules],
        "coursework1_values": [
            sum(mark.coursework1 for mark in marks.filter(module=module))
            for module in modules
        ],
        "coursework2_values": [
            sum(mark.coursework2 for mark in marks.filter(module=module))
            for module in modules
        ],
        "coursework3_values": [
            sum(mark.coursework3 for mark in marks.filter(module=module))
            for module in modules
        ],
    }

    context = {
        "bar_chart_data": json.dumps(bar_chart_data),
        "line_chart_data": json.dumps(line_chart_data),
        "pie_chart_data": json.dumps(pie_chart_data),
        "stacked_bar_chart_data": json.dumps(stacked_bar_chart_data),
    }

    return render(request, "marks/visualization.html", context)

# Get Stats View
def get_stats(request):
    """Return the number of students and modules as JSON response."""
    try:
        num_students = Student.objects.count()
        num_modules = Module.objects.count()

        # Calculate additional stats
        average_marks = Mark.objects.aggregate(
            avg_coursework1=models.Avg('coursework1'),
            avg_coursework2=models.Avg('coursework2'),
            avg_coursework3=models.Avg('coursework3')
        )

        gender_distribution = Student.objects.values('gender').annotate(count=models.Count('gender'))

        return JsonResponse({
            'num_students': num_students,
            'num_modules': num_modules,
            'average_marks': {
                'coursework1': average_marks['avg_coursework1'],
                'coursework2': average_marks['avg_coursework2'],
                'coursework3': average_marks['avg_coursework3'],
            },
            'gender_distribution': list(gender_distribution),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)