from rest_framework import serializers
from task.models import Task, CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'description', 
            'assigned_to_username', 
            'created_by_username', 
            'due_date', 
            'status', 
            'completion_report', 
            'worked_hours', 
        ]
        read_only_fields = [
            'id', 
        ]

class TaskUpdateSerializer(serializers.ModelSerializer):
    completion_report = serializers.CharField(required=False)
    worked_hours = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    class Meta:
        model = Task
        fields = [
            'status', 
            'completion_report', 
            'worked_hours'
        ]
    
    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError(
                    "Completion report is required when marking task as completed."
                )
            if not data.get('worked_hours'):
                raise serializers.ValidationError(
                    "Worked hours is required when marking task as completed."
                )
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'assigned_to_username', 
            'status', 
            'completion_report', 
            'worked_hours', 
            'updated_at'
        ]