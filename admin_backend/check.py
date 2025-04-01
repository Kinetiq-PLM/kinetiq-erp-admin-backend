import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_backend.settings')
django.setup()

from django.db import connection

# List all schemas
with connection.cursor() as cursor:
    cursor.execute("""
    SELECT schema_name 
    FROM information_schema.schemata
    ORDER BY schema_name
    """)
    schemas = cursor.fetchall()
    
    print("Available schemas in the database:")
    for schema in schemas:
        print(f"- {schema[0]}")
    
    # List all tables in all non-system schemas
    print("\nTables by schema:")
    for schema in schemas:
        if schema[0] not in ('pg_catalog', 'information_schema', 'pg_toast'):
            cursor.execute(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{schema[0]}'
            ORDER BY table_name
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"\nSchema: {schema[0]}")
                for table in tables:
                    print(f"- {table[0]}")