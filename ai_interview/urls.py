"""
URL configuration for ai_interview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static
# Removed auth_views and signup_view imports as they are handled in users.urls
from .views import landing_page, dashboard

urlpatterns = [
    # 1️⃣ Home Page
    path('', landing_page, name='landing_page'),

    # 3️⃣ Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # 8️⃣ Admin Panel
    path('admin/', admin.site.urls),

    # 2️⃣ User Authentication (Now handled via include below)
    # Removed direct paths for login, logout, signup

    # App-specific URLs (using include)
    # Include all user-related URLs (auth, profile, etc.) under 'accounts/'
    path('accounts/', include('users.urls')), # Changed prefix from 'users/'

    # 4️⃣ AI Interview Questions (Assuming 'jobs' app handles specific job-related questions/prep)
    path('jobs/', include('jobs.urls')), # Changed prefix to 'jobs/' for consistency

    # NEW: Quiz Generation & Interface
    path('quiz/', include('quiz.urls')),

    # NEW: CSV Predictor
    path('predictor/', include('predictor.urls')),

    # 6️⃣ Mock AI Interview Mode

    # 6️⃣ Mock AI Interview Mode
    # path('mock-interview/', include('mock_interview.urls')), # Placeholder

    # 7️⃣ Gamification
    # path('leaderboard/', include('gamification.urls')), # Placeholder for leaderboard

    # Note: /profile/ and /profile/achievements/ are now under /accounts/profile/ etc.
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
