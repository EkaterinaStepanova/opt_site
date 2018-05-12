from django.db import models

# Create your models here.
'''
class MeasureInput(models.model):
    dimension     = IntegerField()
    bottom_border = CharField()
    upper_border  = CharField()
    r             = CharField()
    epsilon       = CharField()


class MeasureOutput(models.model):
    iterations_number = IntegerField()
    function_minimum  = FloatField()
    arg_minimum       = CharField()
    # execution time?'''

# one dimension f(x)


class Measure(models.Model):

    #in
    bottom_border = models.FloatField(default=0)
    upper_border  = models.FloatField(default=1)
    r             = models.FloatField(default=3.4)
    epsilon       = models.FloatField(default=0.001)
    #functions     = models.CharField()

    #out
    iterations_number = models.IntegerField(default=0)
    function_minimum  = models.FloatField(default=0)
    arg_minimum       = models.FloatField(default=0)

    '''client = models.ForeignKey(
        Client, 
        related_name='measures', 
        on_delete=models.CASCADE)

    owner = models.ForeignKey(
        'auth.User',
        related_name = 'measures',
        on_delete = models.CASCADE
        )'''

    # когда в последний раз измеряли
    date = models.DateTimeField()
    # название эксперимента. 
    # !TODO unique? нет, надо переделать
    name = models.CharField(max_length=200, unique=True)
    # использовали ли вообще шаблон
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.name


class Client(models.Model):
    TEACHER = 'Teacher'
    STUDENT = 'Student'
    POST_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=False, default='', unique=True)
    post = models.CharField(
        max_length=2,
        choices=POST_CHOICES,
        default=STUDENT,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ClientMeasure(models.Model):
    client = models.ForeignKey(
        Client, 
        related_name='clientmeasure', 
        on_delete=models.CASCADE)
    measure = models.ForeignKey(
        Measure, 
        on_delete=models.CASCADE)

    class Meta:
        # Order by score descending
        ordering = ('measure__date',)

    def __str__(self):
        return self.measure.name

'''
class MeasureInput(models.Model):
    bottom_border = models.FloatField()
    upper_border  = models.FloatField()
    r             = models.FloatField()
    epsilon       = models.FloatField()
    #functions     = models.CharField()


class MeasureOutput(models.Model):
    iterations_number = models.IntegerField()
    function_minimum  = models.FloatField()
    arg_minimum       = models.FloatField()


class Measure(models.Model):

    input = models.ForeignKey(
        MeasureInput, 
        on_delete=models.CASCADE)

    output = models.ForeignKey(
        MeasureOutput, 
        on_delete=models.CASCADE)

    client = models.ForeignKey(
        Client, 
        related_name='measures', 
        on_delete=models.CASCADE)

    owner = models.ForeignKey(
        'auth.User',
        related_name = 'measures',
        on_delete = models.CASCADE
        )

    # когда в последний раз измеряли
    date = models.DateTimeField()
    # название эксперимента.
    name = models.CharField(max_length=200, unique=True)
    # использовали ли вообще шаблон
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.name'''