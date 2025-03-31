from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError # Import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse # Keep this import for placeholder views
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog, User
from .forms import CustomUserCreationForm, CustomAuthenticationForm # Import the new forms
from datetime import date, timedelta
import calendar

class UserActivityHeatmapData(APIView):
    """
    Provides activity data for the logged-in user for a heatmap display.
    Returns data for the last N months (e.g., 6 months).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        months_to_show = 6 # Number of past months to include data for

        # Calculate the date range
        today = date.today()
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1) # Go to start of previous month
        for _ in range(months_to_show - 1):
             start_date = (start_date - timedelta(days=1)).replace(day=1)

        # Fetch activity logs within the date range
        activity_logs = ActivityLog.objects.filter(
            user=user,
            activity_date__gte=start_date,
            activity_date__lte=today
        ).values_list('activity_date', flat=True)

        # Convert dates to strings for JSON serialization
        activity_dates_str = [d.strftime('%Y-%m-%d') for d in activity_logs]

        # Prepare data structure suitable for a heatmap (e.g., simple list of dates)
        # More complex structures could be used depending on the specific heatmap library
        heatmap_data = {
            "startDate": start_date.strftime('%Y-%m-%d'),
            "endDate": today.strftime('%Y-%m-%d'),
            "activityDates": activity_dates_str,
            "currentStreak": user.streak # Include current streak
        }

        return Response(heatmap_data)

@login_required
def user_profile(request):
    """
    Displays the user's profile page with streak and heatmap.
    """
    # The request.user object is available in the template context by default
    # when using DjangoTemplates backend and RequestContext processor.
    # No need to explicitly pass it unless you need to add more context.
    return render(request, 'users/profile.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect logged-in users away from signup
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('dashboard') # Redirect to dashboard after successful signup
            except IntegrityError:
                # This is a fallback in case form validation didn't catch a duplicate
                messages.error(request, 'Username or Email already exists. Please choose a different one.')
                # No redirect here, fall through to re-render the form below
        else:
            # Add form validation errors to messages for display in the template
            for field, errors in form.errors.items():
                for error in errors:
                    # Use field.label or field name, and the error message from the form
                    field_name = form.fields[field].label if form.fields[field].label else field.capitalize()
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = CustomUserCreationForm()
    # Render the signup page with the form (containing errors if any)
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect logged-in users away from login
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}.")
                # Redirect to the 'next' URL if it exists, otherwise to dashboard
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('dashboard')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            # Add form validation errors (e.g., if fields are empty)
            for field, errors in form.errors.items():
                 for error in errors:
                     field_name = form.fields[field].label if form.fields[field].label else field.capitalize()
                     messages.error(request, f"{field_name}: {error}")
            # Add a generic error if the form is invalid but no specific user/pass error occurred
            if not form.errors:
                 messages.error(request,"Invalid username or password.")

    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('landing_page') # Redirect to landing page after logout


@login_required
def user_achievements(request):
    """
    Placeholder view for displaying user achievements and badges.
    """
    # In a real implementation, fetch achievements for request.user
    # and pass them to the template context.
    context = {
        'achievements': [] # Placeholder
    }
    # Render a template (e.g., 'users/achievements.html')
    # return render(request, 'users/achievements.html', context)
    return HttpResponse("User achievements page placeholder.") # Simple response for now
