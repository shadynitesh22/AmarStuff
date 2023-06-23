from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Jobs.models import Attendance


class Command(BaseCommand):
    help = 'Create attendance records for all users'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            Attendance.objects.create(user=user)
