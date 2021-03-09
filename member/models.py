from django.db import models
from django.contrib.auth.models import User
from member.constants import MEMBER_ROLE, GENDER_CHOICES, COURSE_CHOICES, BRANCH_CHOICES

# Create your models here.

class Member(models.Model):
    enrollment_number = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200, null=True)
    role = models.IntegerField(choices=MEMBER_ROLE, default=1)
    phone_number = models.IntegerField(default=None, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=7, default=None, null=True)
    course = models.CharField(choices=COURSE_CHOICES, max_length=7, default=None, null=True)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=30, default=None, null=True)

    def __str__(self):
        return self.student_name
    def __user__(self):
        return "%s" % self.user.username