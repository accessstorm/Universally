from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuizConfigForm
from .utils import generate_quiz_questions # Import the generation function
from .models import QuizAttempt # Import the QuizAttempt model

@login_required
def configure_quiz_view(request):
    """
    Displays the quiz configuration form and handles its submission.
    """
    if request.method == 'POST':
        form = QuizConfigForm(request.POST)
        if form.is_valid():
            config = form.cleaned_data
            request.session['quiz_config'] = config # Store config

            # --- Call Gemini to generate questions ---
            questions = generate_quiz_questions(
                category=config['category'],
                num_questions=config['num_questions'],
                question_type=config['question_type']
            )

            if questions:
                # Store generated questions in session
                request.session['quiz_questions'] = questions
                request.session['current_question_index'] = 0 # Start at the first question
                messages.success(request, f"{len(questions)} questions generated successfully!")
                # Redirect to the page that starts the quiz
                return redirect('quiz:start_quiz') # Redirect to the actual quiz page
            else:
                messages.error(request, "Failed to generate quiz questions. Please try configuring again.")
                # Stay on the configuration page
        else:
            messages.error(request, "Please correct the errors in the configuration form.")
    else:
        form = QuizConfigForm()

    context = {'form': form}
    return render(request, 'quiz/configure_quiz.html', context)

# Placeholder views for later steps
@login_required
def start_quiz_view(request):
    """
    Starts the quiz: retrieves questions from session, sets up timer,
    and redirects to the first question.
    """
    quiz_config = request.session.get('quiz_config')
    quiz_questions = request.session.get('quiz_questions')

    if not quiz_config or not quiz_questions:
        messages.error(request, "Quiz configuration or questions not found. Please configure a new quiz.")
        return redirect('quiz:configure_quiz')

    # Reset or initialize quiz state if needed (e.g., answers)
    request.session['quiz_answers'] = {} # Store user answers here
    request.session['current_question_index'] = 0

    # Redirect to the view displaying the first question
    # We can pass the index or rely on the session state
    return redirect('quiz:quiz_question', question_index=0)


@login_required
def quiz_question_view(request, question_index):
    """
    Displays a specific quiz question and handles answer submission.
    """
    quiz_config = request.session.get('quiz_config')
    quiz_questions = request.session.get('quiz_questions')
    user_answers = request.session.get('quiz_answers', {})

    if not quiz_config or not quiz_questions:
        messages.error(request, "Quiz not found or expired. Please start a new one.")
        return redirect('quiz:configure_quiz')

    try:
        current_question = quiz_questions[question_index]
    except IndexError:
        messages.error(request, "Invalid question number.")
        # Maybe redirect to results if it's the end?
        return redirect('quiz:start_quiz') # Or configure page

    total_questions = len(quiz_questions)
    is_last_question = (question_index == total_questions - 1)

    if request.method == 'POST':
        # Process the submitted answer based on question type
        if current_question.get('type') == 'MSQ':
            answer = request.POST.getlist('answer') # Use getlist for checkboxes
        else:
            answer = request.POST.get('answer') # Use get for radio/textarea

        # Store the answer
        user_answers[str(question_index)] = answer # Use index as key
        request.session['quiz_answers'] = user_answers

        # Move to the next question or results page
        if is_last_question:
            # TODO: Redirect to results page
            messages.success(request, "Quiz completed!")
            return redirect('quiz:quiz_results')
        else:
            next_question_index = question_index + 1
            request.session['current_question_index'] = next_question_index
            return redirect('quiz:quiz_question', question_index=next_question_index)

    # GET request: Display the question
    context = {
        'question': current_question,
        'question_index': question_index,
        'total_questions': total_questions,
        'is_last_question': is_last_question,
        'time_limit_seconds': quiz_config.get('time_limit_minutes', 10) * 60, # Pass time limit
        # Pass previous answer if needed for display (e.g., pre-fill open text)
        'previous_answer': user_answers.get(str(question_index))
    }
    return render(request, 'quiz/quiz_question.html', context)


@login_required
def quiz_results_view(request):
    """
    Displays the quiz results after completion.
    """
    quiz_config = request.session.get('quiz_config')
    quiz_questions = request.session.get('quiz_questions')
    user_answers = request.session.get('quiz_answers')

    if not quiz_config or not quiz_questions or user_answers is None:
        messages.warning(request, "Quiz results not available or session expired.")
        return redirect('quiz:configure_quiz')

    # TODO: Implement scoring logic based on question type and correct answers
    score = 0
    results_details = []
    for index, question_data in enumerate(quiz_questions):
        user_answer = user_answers.get(str(index))
        is_correct = False
        q_type = question_data.get('type')

        # --- Scoring Logic ---
        if q_type == 'MCQ':
            correct_answer = question_data.get('correct_answer')
            if user_answer == correct_answer:
                is_correct = True
                score += 1
        elif q_type == 'MSQ':
            correct_answers = sorted(question_data.get('correct_answers', [])) # Sort for consistent comparison
            # Ensure user_answer is a list and sort it
            user_answer_list = sorted(user_answer if isinstance(user_answer, list) else [])
            if user_answer_list == correct_answers and correct_answers: # Check if lists match and not empty
                is_correct = True
                score += 1
        elif q_type == 'OPEN':
            # Auto-scoring for open questions is complex, skip for now
            is_correct = None # Indicate not auto-scored
            # Could potentially send to Gemini for evaluation later
            pass
        # --- End Scoring Logic ---

        results_details.append({
            'question': question_data['question'],
            'user_answer': user_answer,
            # Get correct answer(s) based on type
            'correct_answer': question_data.get('correct_answer') if q_type == 'MCQ' else question_data.get('correct_answers'),
            'is_correct': is_correct, # True, False, or None (for OPEN)
            'options': question_data.get('options'), # Include options for review
            'type': q_type
        })


    # Clear quiz data from session after displaying results? Optional.
    # request.session.pop('quiz_config', None)
    # request.session.pop('quiz_questions', None)
    # request.session.pop('quiz_answers', None)
    # request.session.pop('current_question_index', None)

    context = {
        'score': score,
        'total_questions': len(quiz_questions),
        'results': results_details,
        'config': quiz_config,
    }

    # --- Save the Quiz Attempt ---
    total_questions = len(quiz_questions)
    # Ensure we only save if there were questions
    if total_questions > 0:
        QuizAttempt.objects.create(
            user=request.user,
            questions_attempted=total_questions,
            questions_correct=score # 'score' variable holds the count of correct answers
        )
    # --- End Save Attempt ---

    # Clear quiz data from session after displaying results and saving attempt
    request.session.pop('quiz_config', None)
    request.session.pop('quiz_questions', None)
    request.session.pop('quiz_answers', None)
    request.session.pop('current_question_index', None)


    return render(request, 'quiz/quiz_results.html', context)
