from django.db import models
from users.models import User


class Course(models.Model):
    """Courses"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = [['code'], ['code', 'name']]

    def __str__(self):
        return self.name


class Laboratory(models.Model):
    """Laboratory Courses"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='laboratories'
    )
    professors = models.ManyToManyField(User)
    # professors = models.ManyToManyField(User, related_name='teaching_labs')
    # students = models.ManyToManyField(User, related_name='take_labs')
    # users = models.ManyToManyField(User, related_name='laboratories')
    labschedule = models.ManyToManyField('LabSchedule')

    class Meta:
        unique_together = [['course', 'name']]

    @property
    def get_professors(self):
        """Return a list of instructors"""
        professors = self.professors.all()
        return [u.get_short_name() for u in professors]

    def __str__(self):
        return self.name


class Semester(models.Model):
    SEMESTER_CHOICES = (
        (1, 'Primer Semestre'),
        (2, 'Segundo Semestre'),
        (3, 'Escuela de Vacaciones de Junio'),
        (4, 'Escuela de Vacaciones de Diciembre')
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    year = models.PositiveSmallIntegerField()
    kind = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    date_start = models.DateField(verbose_name='Inicio de Semestre')
    date_end = models.DateField(verbose_name='Fin de Semestre')
    assigment_start = models.DateField(verbose_name='Inicio del Periodo de asignación')
    assigment_end = models.DateField(verbose_name='Fin del Periodo de asignación')

    class Meta:
        unique_together = [['year', 'kind']]

    @property
    def semester_choices_as_dict(self):
        """Return SEMESTER_CHOICES as dictionary"""
        return dict((k, v) for k, v in self.SEMESTER_CHOICES)

    def kind_str(self, key):
        """
        Given key return string format representation.
        Emulation of model.get_<field>_display().
        """
        semester_choices = self.semester_choices_as_dict
        return semester_choices[key]

    def __str__(self):
        return f'{self.year} {self.get_kind_display()}'


class LabSchedule(models.Model):
    """Define hours and day of Lab"""
    DAYS = {
        128: 'MON',
        64: 'TUE',
        32: 'WED',
        16: 'THU',
        8: 'FRI',
        4: 'SAT',
        2: 'SUN'
    }
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    time_start = models.TimeField()
    time_end = models.TimeField()
    weekdays = models.PositiveSmallIntegerField(verbose_name='Días')
    capacity = models.PositiveSmallIntegerField(default=20, verbose_name='Máxima cantidad de estudiantes')

    @property
    def weekdays_list(self):
        container = list()
        for key, value in self.DAYS.items():
            if key & self.weekdays == key:
                container.append(value)
        return container

    def __str__(self):
        return f'{self.time_start}-{self.time_end} {self.weekdays_list}'


class Assignment(models.Model):
    """
    Asignación
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='assignments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # labschedule = models.ForeignKey(LabSchedule, on_delete=models.CASCADE)
