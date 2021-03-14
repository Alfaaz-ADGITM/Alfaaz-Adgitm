from django.contrib import admin
from .models import Member

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'enrollment_number',
        'student_name',
        'role',
        'phone_number',
        'gender',
        'course',
        'branch']