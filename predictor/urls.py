from django.urls import path
from . import views

app_name = 'predictor' # Define app namespace

urlpatterns = [
    path('', views.predictor_view, name='predictor_tool'),
    # Add other predictor-related URLs here if needed later
]
