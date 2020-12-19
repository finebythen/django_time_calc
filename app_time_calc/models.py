from django.db import models


KEY_VALUES = (
    ('-', '-'),
    ('A', 'Abwesend'),
    ('K', 'Krank'),
    ('U', 'Urlaub'),
)


class TimeEntry(models.Model):
    date = models.DateField(null=False, blank=False)
    time_start = models.TimeField(null=False, blank=False)
    time_end = models.TimeField(null=False, blank=False)
    time_rest = models.TimeField(null=False, blank=False)
    key_values = models.CharField(max_length=10, null=False, blank=False, choices=KEY_VALUES, default=KEY_VALUES[0][1])
    status_confirmed = models.BooleanField(default=False)
    user_created = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'user_created', 'time_start']

    def __str__(self):
        return f"Eintrag: {self.date} ({self.time_start} - {self.time_end}), von {self.user_created}"
