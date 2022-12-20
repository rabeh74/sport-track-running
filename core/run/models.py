from django.db import models
from django.conf import settings

from django.db.models import QuerySet, Manager

RUNTYPES = (
    ('EASY', 'Easy run'),
    ('ENDURANCE', 'Endurance run'),
    ('TEMPO', 'Tempo run'),
    ('INTERVALS', 'Interval run'),
    ('UNCATEGORISED', 'Uncagetorised run'),
)
# if queryset plan is updated delete cash key
# customize queyset
class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('plans_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)

class CustomPlanManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

class Plan(models.Model):
    runtype = models.CharField(max_length=13, choices=RUNTYPES, default='UNCATEGORISED')
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    objects=CustomPlanManager()
    def __str__(self):
        return f'Plan: {self.date} - {self.description}'

# if queryset Run is updated delete cash key
# customize queyset

class CustomRunQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('Run_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)

class CustomRunManager(Manager):
    def get_queryset(self):
        return CustomRunQuerySet(self.model, using=self._db)


class Run(models.Model):

    UNITS = (
        ('KM', 'Kilometres'),
        ('MI', 'Miles'),
    )

    runtype = models.CharField(max_length=13, choices=RUNTYPES, default='UNCATEGORISED')
    date = models.DateField(auto_now=False, auto_now_add=True)
    units = models.CharField(max_length=2, choices=UNITS, default='KM')

    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pace = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    avg_HR = models.IntegerField(null=True)
    notes = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

    objects=CustomRunManager()
    def __str__(self):
        return f'Run: {self.date} , {self.distance} {self.units.lower()}'


class Race(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=True)
    name = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.name}'