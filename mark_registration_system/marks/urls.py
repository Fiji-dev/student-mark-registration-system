from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Corrected to use function-based view
    path('home/', views.home, name='home'),  # Home page
    path('input_mark/', views.input_mark, name='input_mark'),  # Input marks page
    path('update_mark/', views.update_mark, name='update_mark'),  # Update marks page
    path('view_marks/', views.view_mark, name='view_marks'),  # View marks page
    path('visualization/', views.visualization_view, name='visualization'),  # Visualization page
    path('get_stats/', views.get_stats, name='get_stats'),  # Get statistics page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('', RedirectView.as_view(url='login/')),  # Redirect to home page
]
