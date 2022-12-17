from django.db import models
from django.conf import settings

RUNTYPES = (
    ('EASY', 'Easy run'),
    ('ENDURANCE', 'Endurance run'),
    ('TEMPO', 'Tempo run'),
    ('INTERVALS', 'Interval run'),
    ('UNCATEGORISED', 'Uncagetorised run'),
)


class Plan(models.Model):
    runtype = models.CharField(max_length=13, choices=RUNTYPES, default='UNCATEGORISED')
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'Plan: {self.date} - {self.description}'

class Run(models.Model):

    UNITS = (
        ('KM', 'Kilometres'),
        ('MI', 'Miles'),
    )

    runtype = models.CharField(max_length=13, choices=RUNTYPES, default='UNCATEGORISED')
    date = models.DateField(auto_now=False, auto_now_add=False)
    units = models.CharField(max_length=2, choices=UNITS, default='KM')

    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pace = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    avg_HR = models.IntegerField(null=True)
    notes = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)


    def __str__(self):
        return f'Run: {self.date} - {self.time}, {self.distance} {self.units.lower()}'


class Race(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=False)
    name = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.name}'