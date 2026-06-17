from django.db import models
import uuid

class AIPredictionLog(models.Model):
    prediction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    module_name = models.CharField(max_length=100)
    request_source = models.CharField(max_length=100, default='api')
    input_payload = models.JSONField()
    output_payload = models.JSONField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    response_time_ms = models.FloatField()
    status = models.CharField(max_length=50) # 'SUCCESS', 'ERROR'
    error_message = models.TextField(null=True, blank=True)
    user_identifier = models.CharField(max_length=100, default='system')
    api_endpoint = models.CharField(max_length=200)

    class Meta:
        ordering = ['-timestamp']

class ChatbotLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.TextField()
    intent = models.CharField(max_length=100, null=True, blank=True)
    modules_used = models.JSONField(default=list)
    answer = models.TextField()
    confidence = models.FloatField(null=True, blank=True)
    response_time_ms = models.FloatField()
    status = models.CharField(max_length=50)

    class Meta:
        ordering = ['-timestamp']

class LLMInteractionLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.TextField()
    response = models.TextField()
    tools_called = models.JSONField(default=list)
    token_usage = models.IntegerField(default=0)
    response_time = models.FloatField()
    model_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='SUCCESS')
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
