from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('configure/', views.configure_quiz_view, name='configure_quiz'),
    path('start/', views.start_quiz_view, name='start_quiz'),
    # Use question_index instead of question_id as it's based on list index
    path('question/<int:question_index>/', views.quiz_question_view, name='quiz_question'),
    path('results/', views.quiz_results_view, name='quiz_results'),
]
