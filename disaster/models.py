# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AiMonitoringAipredictionlog(models.Model):
    prediction_id = models.CharField(primary_key=True, max_length=32)
    timestamp = models.DateTimeField()
    module_name = models.CharField(max_length=100)
    request_source = models.CharField(max_length=100)
    input_payload = models.JSONField()
    output_payload = models.JSONField(blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    response_time_ms = models.FloatField()
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)
    user_identifier = models.CharField(max_length=100)
    api_endpoint = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ai_monitoring_aipredictionlog'


class AiMonitoringChatbotlog(models.Model):
    log_id = models.CharField(primary_key=True, max_length=32)
    timestamp = models.DateTimeField()
    question = models.TextField()
    intent = models.CharField(max_length=100, blank=True, null=True)
    modules_used = models.JSONField()
    answer = models.TextField()
    confidence = models.FloatField(blank=True, null=True)
    response_time_ms = models.FloatField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ai_monitoring_chatbotlog'


class AiMonitoringLlminteractionlog(models.Model):
    log_id = models.CharField(primary_key=True, max_length=32)
    session_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    question = models.TextField()
    response = models.TextField()
    tools_called = models.JSONField()
    token_usage = models.IntegerField()
    response_time = models.FloatField()
    model_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ai_monitoring_llminteractionlog'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DmdAiPredictionLog(models.Model):
    prediction_type = models.CharField(max_length=100)
    input_data = models.JSONField()
    prediction_result = models.JSONField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dmd_ai_prediction_log'


class DmdArea(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_flood_prone = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_area'
        unique_together = (('ward', 'name'),)


class DmdAwarenessProgram(models.Model):
    title = models.CharField(max_length=200)
    program_date = models.DateField()
    citizens_trained = models.PositiveIntegerField()
    volunteers_registered = models.PositiveIntegerField()
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_awareness_program'


class DmdBudget(models.Model):
    year = models.IntegerField()
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    utilized_amount = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_budget'


class DmdBuilding(models.Model):
    name = models.CharField(max_length=200)
    year_built = models.PositiveIntegerField()
    condition = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=20)
    evacuation_required = models.IntegerField()
    is_active = models.IntegerField()
    area = models.ForeignKey(DmdArea, models.DO_NOTHING)
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_building'


class DmdBuildingInspection(models.Model):
    inspection_date = models.DateField()
    inspector_name = models.CharField(max_length=150)
    findings = models.TextField()
    recommendation = models.TextField()
    next_inspection_date = models.DateField(blank=True, null=True)
    document = models.CharField(max_length=100, blank=True, null=True)
    building = models.ForeignKey(DmdBuilding, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_building_inspection'


class DmdDisasterCategory(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    is_natural = models.IntegerField()
    max_risk_score = models.PositiveIntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dmd_disaster_category'


class DmdEmergencyContact(models.Model):
    department_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=30)
    availability = models.CharField(max_length=50)
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_emergency_contact'


class DmdEquipment(models.Model):
    name = models.CharField(max_length=150)
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    in_use_quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=30)
    last_inspection = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_equipment'


class DmdIncident(models.Model):
    incident_number = models.CharField(unique=True, max_length=30)
    title = models.CharField(max_length=255)
    description = models.TextField()
    incident_date = models.DateField()
    reported_time = models.DateTimeField()
    response_started_time = models.DateTimeField(blank=True, null=True)
    resolved_time = models.DateTimeField(blank=True, null=True)
    cause = models.CharField(max_length=200, blank=True, null=True)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=30)
    affected_people = models.PositiveIntegerField()
    injured_people = models.PositiveIntegerField()
    death_count = models.PositiveIntegerField()
    houses_damaged = models.PositiveIntegerField()
    roads_blocked = models.PositiveIntegerField()
    estimated_loss_amount = models.DecimalField(max_digits=15, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    incident_photo = models.CharField(max_length=100, blank=True, null=True)
    damage_document = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    area = models.ForeignKey(DmdArea, models.DO_NOTHING)
    disaster_category = models.ForeignKey(DmdDisasterCategory, models.DO_NOTHING)
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_incident'


class DmdIncidentResponse(models.Model):
    assigned_time = models.DateTimeField()
    arrival_time = models.DateTimeField(blank=True, null=True)
    completion_time = models.DateTimeField(blank=True, null=True)
    members_deployed = models.PositiveIntegerField()
    vehicles_used = models.PositiveIntegerField()
    boats_used = models.PositiveIntegerField()
    equipment_used = models.PositiveIntegerField()
    response_result = models.CharField(max_length=20, blank=True, null=True)
    officer_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    incident = models.ForeignKey(DmdIncident, models.DO_NOTHING)
    team = models.ForeignKey('DmdResponseTeam', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_incident_response'


class DmdMockDrill(models.Model):
    location = models.CharField(max_length=200)
    drill_type = models.CharField(max_length=100)
    date = models.DateField()
    participants = models.PositiveIntegerField()
    remarks = models.TextField(blank=True, null=True)
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_mock_drill'


class DmdResourceUsage(models.Model):
    quantity_used = models.PositiveIntegerField()
    used_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    equipment = models.ForeignKey(DmdEquipment, models.DO_NOTHING)
    incident = models.ForeignKey(DmdIncident, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_resource_usage'


class DmdResponseTeam(models.Model):
    team_code = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=150)
    team_leader = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    members_count = models.PositiveIntegerField()
    vehicles_count = models.PositiveIntegerField()
    boats_count = models.PositiveIntegerField()
    equipment_count = models.PositiveIntegerField()
    specialization = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_response_team'


class DmdVehicle(models.Model):
    vehicle_number = models.CharField(unique=True, max_length=30)
    vehicle_type = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20)
    last_service_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    ward = models.ForeignKey('DmdWard', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_vehicle'


class DmdWard(models.Model):
    name = models.CharField(unique=True, max_length=100)
    code = models.CharField(unique=True, max_length=20)
    description = models.TextField(blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)
    area_sq_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    current_risk_level = models.CharField(max_length=20)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dmd_ward'


class DmdWeatherHistory(models.Model):
    date = models.DateField()
    rainfall_mm = models.DecimalField(max_digits=8, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.PositiveIntegerField()
    water_level_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    alert_level = models.CharField(max_length=20, blank=True, null=True)
    ward = models.ForeignKey(DmdWard, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dmd_weather_history'
