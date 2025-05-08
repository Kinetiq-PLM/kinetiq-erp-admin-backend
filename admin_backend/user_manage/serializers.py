# user_manage/serializers.py
from rest_framework import serializers
from .models import User, RolePermission
import uuid

class RolePermissionSerializer(serializers.ModelSerializer):
    department_permissions = serializers.MultipleChoiceField(
        choices = [
            # Accounting
            ('Accounting/', 'Accounting'),
            ('Accounting/Chart of Accounts', 'Accounting/Chart of Accounts'),
            ('Accounting/Journal', 'Accounting/Journal'),
            ('Accounting/Journal Entry', 'Accounting/Journal Entry'),
            ('Accounting/General Ledger', 'Accounting/General Ledger'),
            ('Accounting/General Ledger Accounts', 'Accounting/General Ledger Accounts'),
            ('Accounting/Official Receipts', 'Accounting/Official Receipts'),
            ('Accounting/Payroll Accounting', 'Accounting/Payroll Accounting'),
            ('Accounting/Tax and Remittance', 'Accounting/Tax and Remittance'),
            ('Accounting/Accounts Payable Receipts', 'Accounting/Accounts Payable Receipts'),

            # Administration
            ('Administration/', 'Administration'),
            ('Administration/User', 'Administration/User'),
            ('Administration/Item Masterlist', 'Administration/Item Masterlist'),
            ('Administration/Business Partner Masterlist', 'Administration/Business Partner Masterlist'),
            ('Administration/Audit Logs', 'Administration/Audit Logs'),
            ('Administration/Policy', 'Administration/Policy'),
            ('Administration/Currency', 'Administration/Currency'),
            ('Administration/Warehouse', 'Administration/Warehouse'),
            ('Administration/Notification', 'Administration/Notification'),

            # CRM
            ('CRM/', 'CRM'),
            ('CRM/Leads', 'CRM/Leads'),
            ('CRM/Opportunity', 'CRM/Opportunity'),
            ('CRM/Campaign', 'CRM/Campaign'),
            ('CRM/Contacts', 'CRM/Contacts'),
            ('CRM/Cases', 'CRM/Cases'),

            # Distribution
            ('Distribution/', 'Distribution'),
            ('Distribution/External Delivery', 'Distribution/External Delivery'),
            ('Distribution/Internal Delivery', 'Distribution/Internal Delivery'),
            ('Distribution/Picking', 'Distribution/Picking'),
            ('Distribution/Packing', 'Distribution/Packing'),
            ('Distribution/Shipment', 'Distribution/Shipment'),
            ('Distribution/Rework', 'Distribution/Rework'),

            # Financials
            ('Financials/', 'Financials'),
            ('Financials/Reports', 'Financials/Reports'),
            ('Financials/Validations', 'Financials/Validations'),
            ('Financials/Approvals', 'Financials/Approvals'),
            ('Financials/Forms', 'Financials/Forms'),

            # Human Resources
            ('Human Resources/', 'Human Resources'),
            ('Human Resources/Employees', 'Human Resources/Employees'),
            ('Human Resources/Recruitment', 'Human Resources/Recruitment'),
            ('Human Resources/Attendance Tracking', 'Human Resources/Attendance Tracking'),
            ('Human Resources/Payroll', 'Human Resources/Payroll'),
            ('Human Resources/Departments', 'Human Resources/Departments'),
            ('Human Resources/Workforce Allocation', 'Human Resources/Workforce Allocation'),
            ('Human Resources/Leave Requests', 'Human Resources/Leave Requests'),
            ('Human Resources/Employee Performance', 'Human Resources/Employee Performance'),
            ('Human Resources/Employee Salary', 'Human Resources/Employee Salary'),

            # Inventory
            ('Inventory/', 'Inventory'),
            ('Inventory/Shelf Life', 'Inventory/Shelf Life'),
            ('Inventory/P-Counts', 'Inventory/P-Counts'),
            ('Inventory/Stock Flow', 'Inventory/Stock Flow'),

            # Job Posting
            ('Job Posting/', 'Job Posting'),

            # Management
            ('Management/', 'Management'),
            ('Management/Dashboard', 'Management/Dashboard'),
            ('Management/Project Approval', 'Management/Project Approval'),
            ('Management/User Roles', 'Management/User Roles'),
            ('Management/Access Control', 'Management/Access Control'),
            ('Management/Settings', 'Management/Settings'),

            # MRP
            ('MRP/', 'MRP'),
            ('MRP/Material Requirements Planning', 'MRP/Material Requirements Planning'),
            ('MRP/Bills Of Material', 'MRP/Bills Of Material'),
            ('MRP/Product Materials', 'MRP/Product Materials'),

            # Operations
            ('Operations/', 'Operations'),
            ('Operations/Goods Tracking', 'Operations/Goods Tracking'),
            ('Operations/Internal Transfer', 'Operations/Internal Transfer'),
            ('Operations/Delivery Approval', 'Operations/Delivery Approval'),
            ('Operations/Delivery Receipt', 'Operations/Delivery Receipt'),
            ('Operations/Item Removal', 'Operations/Item Removal'),

            # Production
            ('Production/', 'Production'),
            ('Production/Equipment and Labor', 'Production/Equipment and Labor'),
            ('Production/Cost of Production', 'Production/Cost of Production'),

            # Project Management
            ('Project Management/', 'Project Management'),
            ('Project Management/Project List', 'Project Management/Project List'),
            ('Project Management/Project Planning', 'Project Management/Project Planning'),
            ('Project Management/Project Request', 'Project Management/Project Request'),
            ('Project Management/Tasks', 'Project Management/Tasks'),
            ('Project Management/Report Monitoring', 'Project Management/Report Monitoring'),
            ('Project Management/Warranty Monitoring', 'Project Management/Warranty Monitoring'),
            ('Project Management/Project Cost', 'Project Management/Project Cost'),

            # Project Request
            ('Project Request/', 'Project Request'),

            # Purchase Request
            ('Purchase Request/', 'Purchase Request'),

            # Purchasing
            ('Purchasing/', 'Purchasing'),
            ('Purchasing/Purchase Request List', 'Purchasing/Purchase Request List'),
            ('Purchasing/Puchase Quotation List', 'Purchasing/Puchase Quotation List'),
            ('Purchasing/Purchase Order Status', 'Purchasing/Purchase Order Status'),
            ('Purchasing/A/P Invoice', 'Purchasing/A/P Invoice'),
            ('Purchasing/Credit Memo', 'Purchasing/Credit Memo'),
            ('Purchasing/Vendor Application Form', 'Purchasing/Vendor Application Form'),

            # Sales
            ('Sales/', 'Sales'),
            ('Sales/Quotation', 'Sales/Quotation'),
            ('Sales/Order', 'Sales/Order'),
            ('Sales/Delivery', 'Sales/Delivery'),
            ('Sales/Transactions', 'Sales/Transactions'),

            # Support & Services
            ('Support & Services/', 'Support & Services'),
            ('Support & Services/Service Ticket', 'Support & Services/Service Ticket'),
            ('Support & Services/Service Call', 'Support & Services/Service Call'),
            ('Support & Services/Service Request', 'Support & Services/Service Request'),
            ('Support & Services/Warranty Renewal', 'Support & Services/Warranty Renewal'),
            ('Support & Services/Service Analysis', 'Support & Services/Service Analysis'),
            ('Support & Services/Service Billing', 'Support & Services/Service Billing'),
            ('Support & Services/Service Report', 'Support & Services/Service Report'),
            ('Support & Services/Service Contract', 'Support & Services/Service Contract'),

            # Report Generator
            ('Report Generator/', 'Report Generator'),

            # Workforce Request
            ('Workforce Request/', 'Workforce Request'),

            # Employee Request (not listed in main choices but exists in submodules)
            ('Employee Request/', 'Employee Request'),
            ('Employee Request/Resignation Request', 'Employee Request/Resignation Request'),
            ('Employee Request/Overtime Request', 'Employee Request/Overtime Request'),
            ('Employee Request/Leave Request', 'Employee Request/Leave Request'),
        ],
        required=False
    )
    
    class Meta:
        model = RolePermission
        fields = ['role_id', 'role_name', 'description', 'permissions', 'department_permissions']
        read_only_fields = ['role_id', 'permissions']  # Make original permissions read-only

    def to_representation(self, instance):
        """Convert stored comma-separated string to list for UI"""
        representation = super().to_representation(instance)
        
        # Parse the stored permissions string into a list
        if instance.permissions:
            representation['department_permissions'] = instance.permissions.split(',')
        else:
            representation['department_permissions'] = []
            
        # Remove the original permissions field from the output
        representation.pop('permissions', None)
        
        return representation
    
    def create(self, validated_data):
        # Extract the department_permissions list
        department_permissions = validated_data.pop('department_permissions', [])
        
        # Convert to comma-separated string
        permissions_string = ','.join(department_permissions)
        validated_data['permissions'] = permissions_string
        
        # Generate a unique role_id
        role_id = f"ADMIN-ROLE-{uuid.uuid4().hex[:6]}"
        validated_data['role_id'] = role_id
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Extract the department_permissions list
        department_permissions = validated_data.pop('department_permissions', None)
        
        if department_permissions is not None:
            # Convert to comma-separated string
            permissions_string = ','.join(department_permissions)
            validated_data['permissions'] = permissions_string
        
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    role_details = RolePermissionSerializer(source='role', read_only=True)
    
    # Replace the CharField with a PrimaryKeyRelatedField to create a dropdown
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=RolePermission.objects.all().order_by('role_name'),
        required=False,
        allow_null=True,
        label='Role'
    )

    # Add this field to make password optional during updates
    password = serializers.CharField(
        write_only=True,  # Hide password in responses
        required=False,   # Make it optional for updates
        style={'input_type': 'password'}  # For UI rendering as password field
    )
    
    # Add a display field for showing role names in the dropdown
    role_display = serializers.SerializerMethodField(read_only=True)
    
    def get_role_display(self, obj):
        if obj.role:
            return obj.role.role_name
        return None
    
    class Meta:
        model = User
        fields = ['user_id', 'employee_id', 'first_name', 'last_name', 'email', 
                 'password', 'role_id', 'role_display', 'role_details', 'status', 'type', 
                 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'employee_id', 'created_at', 'updated_at', 'role_display']
    
    def create(self, validated_data):
        # Generate a unique user_id
        user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"
        validated_data['user_id'] = user_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # For update: if password is empty or not provided, remove it from validated_data
        if 'password' in validated_data and not validated_data['password']:
            validated_data.pop('password')

        # Preserve the role if not provided in the update data
        if 'role' in validated_data and not validated_data['role']:
            validated_data.pop('role')
        
        updated_instance = super().update(instance, validated_data)
        
        # If password was updated, call the hash function
        from django.db import connection
        if 'password' in validated_data:
            with connection.cursor() as cursor:
                cursor.execute("SELECT admin.hash_user_passwords();")
        
        return updated_instance
    
    def validate_password(self, value):
        """Add custom validation for password if needed."""
        if value and len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


class RoleChoiceSerializer(serializers.ModelSerializer):
    """Lightweight serializer for role dropdown options"""
    class Meta:
        model = RolePermission
        fields = ['role_id', 'role_name']