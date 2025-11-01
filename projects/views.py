from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project

def project_list(request):
    all_projects = Project.objects.all()
    featured_project = all_projects.filter(title__icontains="GitHub").first()
    main_projects = all_projects.exclude(id=featured_project.id) if featured_project else all_projects

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": main_projects,
            "featured": featured_project,
        },
    )

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/project_detail.html", {"project": project})

def contact(request):
    return render(request, "projects/contact.html")

# AJAX endpoint for demos
def demo_api(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        demo_type = request.POST.get("demo_type")
        response_html = ""

        if demo_type == "resume":
            resume_choice = request.POST.get("resume")
            sample_matches = {
                "Data Analyst Resume": [
                    "Analysis and Reporting Analyst",
                    "Data Analyst",
                    "COOP and Emergency Intern",
                    "Geographic Information Systems Specialist",
                    "Associate Data Scientist",
                ],
                "Healthcare Nurse Resume": [
                    "WTC Case Management Nurse",
                    "Supervising Public Health Nurse, Bureau of School Health/SH Nursing Services & Prof Dev",
                    "Public Health Nurse, I, Bureau of School Health",
                    "Supervising Health Nurse, Bureau of School Health/SH Nursing Services & Prof Dev",
                    "Staff Nurse (Part-Time)", 
                ],
                "Software Engineer Resume": [
                    "Software Engineer",
                    "Senior Data Engineer",
                    "DevOps Engineer",
                    "Certified IT Developer (Applications)",
                    "Web Application Developer", 
                ],
                "Financial Analyst Resume": [
                    "Senior/Supervising Analyst  Environmental Sustainability and Resiliency",
                    "Investment Officer- Fixed Income",
                    "Risk Officer (Asset Management)", 
                    "Energy Program Analyst", 
                    "Staff Analyst", 
                ],
                "Graphic Designer Resume": [
                    "Graphic Design College Intern",
                    "Project Manager",
                    "Architectural Designer",
                    "Multimedia Designer/Systems Analyst",
                    "UX Designer", 
                ],
            }
            jobs = sample_matches.get(resume_choice, [])
            response_html = "<h6>Top Matches:</h6><ul>" + "".join(f"<li>{j}</li>" for j in jobs) + "</ul>"

        elif demo_type == "basketball_archetype":
            player_choice = request.POST.get("player")
            sample_archetypes = {
                "LeBron James": "All-NBA Level Star",
                "Klay Thompson": "3 & D Wing/ Floor Spacer",
                "Steven Adams": "Rim Protector/ Putback Big",
                "Devin Booker": "Primary Creator/ Star Guard",
                "Jordan Clarkson": "Low-Usage Role Guard",
                "Anthony Davis": "Rim-Running Big/ Defensive Anchor",
                "Jalen Johnson": "Versatile Forward/ Secondary Scorer",
            }
            archetype = sample_archetypes.get(player_choice, "Unknown")
            response_html = f"<h6>Archetype:</h6><p>{archetype}</p>"

        elif demo_type == "player_peak":
            player_choice = request.POST.get("player")
            player_stats = {
                "Dyson Daniels": {"minutes": 32, "points": 15, "rebounds": 5, "assists": 5, "steals": 2, "blocks": 1},
                "Jalen Williams": {"minutes": 33, "points": 23, "rebounds": 5, "assists": 5, "steals": 1, "blocks": 1},
                "Walker Kessler": {"minutes": 29, "points": 12, "rebounds": 10, "assists": 2, "steals": 1, "blocks": 2},
                "Paolo Banchero": {"minutes": 35, "points": 27, "rebounds": 8, "assists": 5, "steals": 1, "blocks": 1},
                "Shaedon Sharpe": {"minutes": 33, "points": 21, "rebounds": 5, "assists": 3, "steals": 1, "blocks": 0},
                "Jalen Duran": {"minutes": 29, "points": 14, "rebounds": 10, "assists": 3, "steals": 1, "blocks": 1},
            }
            stats = player_stats.get(player_choice)
            if stats:
                response_html = f"""
                    <h6>{player_choice} – Peak Per-Game Stats</h6>
                    <ul>
                        <li>Minutes: {stats['minutes']}</li>
                        <li>Points: {stats['points']}</li>
                        <li>Rebounds: {stats['rebounds']}</li>
                        <li>Assists: {stats['assists']}</li>
                        <li>Steals: {stats['steals']}</li>
                        <li>Blocks: {stats['blocks']}</li>
                    </ul>
                """
            else:
                response_html = "<p>No stats available.</p>"

        return JsonResponse({"html": response_html})

    return JsonResponse({"error": "Invalid request"}, status=400)
