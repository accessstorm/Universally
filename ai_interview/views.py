from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    """
    Renders the main landing page.
    """
    return render(request, 'landing_page.html')

@login_required
def dashboard(request):
    """
    Renders the main user dashboard page.
    """
    # Pass any necessary context to the dashboard template here
    context = {} 
    return render(request, 'dashboard.html', context)
