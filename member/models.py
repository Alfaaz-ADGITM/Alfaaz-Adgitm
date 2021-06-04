from django.db import models
from django.contrib.auth.models import User
from member.constants import MEMBER_ROLE, GENDER_CHOICES, COURSE_CHOICES, BRANCH_CHOICES

# Create your models here.

class Member(models.Model):
    enrollment_number = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200, null=True)
    role = models.IntegerField(choices=MEMBER_ROLE, default=1)
    phone_number = models.IntegerField(default=None, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    course = models.IntegerField(choices=COURSE_CHOICES, default=1)
    branch = models.IntegerField(choices=BRANCH_CHOICES, default=1)
    def __str__(self):
        return self.student_name
    def __user__(self):
        return "%s" % self.user.username

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    #student = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    photo = models.ImageField(null=False)