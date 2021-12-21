from django.shortcuts import render

# This is the view that you imported in the frontend/urls.py
def index(request, *args, **kwargs):
    return render(request, "frontend/index.html")  # notice the template used here