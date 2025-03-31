from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError # Import IntegrityError
from rest_framework.views import APIView # Keep if other API views exist/planned
from rest_framework.response import Response # Keep if other API views exist/planned
from django.http import HttpResponse # Keep this import for placeholder views
from rest_framework.permissions import IsAuthenticated # Keep if other API views exist/planned
# No longer need json or mark_safe here
from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm # Import the new forms
from quiz.models import QuizAttempt # Import the QuizAttempt model
from datetime import date, timedelta
import calendar

# Removed UserActivityHeatmapData API view as it depended on ActivityLog and streak


@login_required
def user_profile(request):
    """
    Displays the user's profile page with streak and heatmap.
    """
    # Fetch quiz attempts for the logged-in user
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('timestamp') # Order chronologically

    # Prepare data for Chart.js
    chart_labels = [attempt.timestamp.strftime('%Y-%m-%d %H:%M') for attempt in quiz_attempts]
    chart_attempted_data = [attempt.questions_attempted for attempt in quiz_attempts]
    chart_correct_data = [attempt.questions_correct for attempt in quiz_attempts]

    chart_data = {
        'labels': chart_labels,
        'attempted': chart_attempted_data,
        'correct': chart_correct_data,
    }
    # Pass the dictionary directly

    context = {
        'quiz_attempts': quiz_attempts, # Keep original queryset if needed elsewhere
        'chart_data': chart_data, # Pass the data dictionary directly
        'user': request.user
    }
    return render(request, 'users/profile.html', context)


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


@login_required
def profile_edit_view(request):
    """
    Handles displaying and processing the profile update form.
    """
    if request.method == 'POST':
        # Pass request.FILES to handle the profile image upload
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile') # Redirect back to the profile view page using namespace
        else:
            # Add form validation errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if form.fields[field].label else field.capitalize()
                    messages.error(request, f"{field_name}: {error}")
            # No redirect here, fall through to re-render the form with errors
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})
