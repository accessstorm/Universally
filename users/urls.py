from django.urls import path
# Import necessary views
from .views import (
    # UserActivityHeatmapData, # Removed as the view was removed
    user_profile,
    profile_edit_view, # Add import for the edit view
    user_achievements,
    signup_view,
    login_view,
    logout_view
)

app_name = 'users'

urlpatterns = [
    # Profile URLs
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'), # Add URL for editing profile

    # 7️⃣ Gamification (Achievements - placed here for now)
    path('profile/achievements/', user_achievements, name='user_achievements'), # Added achievements URL

    # Authentication URLs
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
