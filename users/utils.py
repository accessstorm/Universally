from datetime import date, timedelta
from .models import ActivityLog

def calculate_streak(user):
    """
    Calculates the current consecutive day streak for a user based on ActivityLog.
    """
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Get the user's activity dates, ordered most recent first
    activity_dates = list(ActivityLog.objects.filter(user=user).order_by('-activity_date').values_list('activity_date', flat=True))

    if not activity_dates:
        return 0 # No activity yet

    # Check if the most recent activity was today or yesterday
    if activity_dates[0] != today and activity_dates[0] != yesterday:
        return 0 # Streak broken

    streak = 0
    expected_date = activity_dates[0] # Start from the most recent activity date

    for activity_date in activity_dates:
        if activity_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1) # Expect the previous day next
        elif activity_date < expected_date:
            # Gap detected, but check if the loop just started (i.e., first date was yesterday)
            # If the first date was yesterday, and the second date is older than the day before yesterday, the streak is 1.
            # If the first date was today, and the second date is older than yesterday, the streak is 1.
             if streak == 1 and activity_dates[0] == yesterday and activity_date < yesterday - timedelta(days=1):
                 break # Streak was just 1 (yesterday)
             elif streak == 1 and activity_dates[0] == today and activity_date < today - timedelta(days=1):
                 break # Streak was just 1 (today)
             elif streak > 1:
                 break # Gap detected after a streak > 1

    return streak

def update_user_streak(user):
    """
    Calculates and updates the user's streak field.
    """
    current_streak = calculate_streak(user)
    if user.streak != current_streak:
        user.streak = current_streak
        user.save(update_fields=['streak'])
    return current_streak

def record_activity(user):
    """
    Records an activity for the user for the current date if not already recorded,
    and updates their streak.
    """
    today = date.today()
    # Use get_or_create to avoid duplicate entries for the same day
    log_entry, created = ActivityLog.objects.get_or_create(user=user, activity_date=today)
    
    # Update streak regardless of whether the entry was created or already existed
    # This handles cases where the script runs multiple times a day or catches up streaks
    updated_streak = update_user_streak(user)

    return log_entry, created, updated_streak
