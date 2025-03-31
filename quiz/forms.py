from django import forms

class QuizConfigForm(forms.Form):
    # Define choices for question types
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice (MCQ)'),
        ('MSQ', 'Multiple Select (MSQ)'),
        # ('NAT', 'Numerical Answer Type (NAT)'), # NAT might be harder to auto-grade reliably
        ('OPEN', 'Open Ended / Descriptive'),
    ]

    # Define choices for categories (example, can be expanded)
    CATEGORY_CHOICES = [
        ('python', 'Python'),
        ('django', 'Django'),
        ('javascript', 'JavaScript'),
        ('react', 'React'),
        ('data_structures', 'Data Structures'),
        ('algorithms', 'Algorithms'),
        ('system_design', 'System Design'),
        ('behavioral', 'Behavioral'),
        # Add more categories as needed
    ]

    num_questions = forms.IntegerField(
        min_value=1,
        max_value=20, # Set a reasonable max
        initial=5,
        label="Number of Questions",
        widget=forms.NumberInput(attrs={'class': 'py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Category / Subject",
        widget=forms.Select(attrs={'class': 'py-3 px-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600'})
    )
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES,
        label="Question Type",
        widget=forms.Select(attrs={'class': 'py-3 px-4 pe-9 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600'})
    )
    time_limit_minutes = forms.IntegerField(
        min_value=1,
        max_value=120, # Max 2 hours
        initial=10,
        label="Time Limit (minutes)",
        widget=forms.NumberInput(attrs={'class': 'py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600'})
    )
    # Add difficulty level later if needed
    # difficulty = forms.ChoiceField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], ...)
