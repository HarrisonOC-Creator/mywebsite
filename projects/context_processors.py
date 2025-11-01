from datetime import datetime
from .models import Project

def portfolio_years(request):
    # Default to current year if no projects exist
    current_year = datetime.now().year
    first_project = Project.objects.order_by("id").first()
    if first_project:
        start_year = first_project.created_at.year if hasattr(first_project, "created_at") else current_year
    else:
        start_year = current_year

    return {
        "start_year": start_year,
        "current_year": current_year,
    }