from django.shortcuts import render
from django.db import connection

def list_assets(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin.assets")
        assets = cursor.fetchall()
    
    return render(request, 'assets_list.html', {'assets': assets})