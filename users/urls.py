from django.urls import path
# Import necessary views
from .views import (
    UserActivityHeatmapData,
    user_profile,
    user_achievements,
    signup_view,
    login_view,
    logout_view
)

app_name = 'users'

urlpatterns = [
    # 5️⃣ Streak Tracking & Heatmap (Profile & Heatmap API)
    path('profile/', user_profile, name='profile'),
    path('api/activity-heatmap/', UserActivityHeatmapData.as_view(), name='activity_heatmap_data'),

    # 7️⃣ Gamification (Achievements - placed here for now)
    path('profile/achievements/', user_achievements, name='user_achievements'), # Added achievements URL

    # Authentication URLs
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
