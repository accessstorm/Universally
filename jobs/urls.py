from django.urls import path
from .views import question_feed, submit_answer # Placeholder imports

app_name = 'jobs' # Or 'questions' if you rename the app later

urlpatterns = [
    # 4️⃣ AI Interview Questions
    path('', question_feed, name='question_feed'), # Maps to /questions/
    path('submit/<int:question_id>/', submit_answer, name='submit_answer'), # Maps to /questions/submit/<question_id>/
]
