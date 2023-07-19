#!/usr/bin/env python3

from quiz.models import Attendance
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'user', 'date','late', 'inout')
