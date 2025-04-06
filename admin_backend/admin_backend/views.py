from django.shortcuts import render

def main_dashboard(request):
    """Main dashboard view that shows summary information from all apps"""
    return render(request, 'admin_backend/dashboard.html', {
        'active_app': 'dashboard'
    })