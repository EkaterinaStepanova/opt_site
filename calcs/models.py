from django.db import models
from django.contrib.auth.models import User


class Measure(models.Model):

    #in
    bottom_border = models.FloatField(default=0)
    upper_border  = models.FloatField(default=1)
    r             = models.FloatField(default=3.4)
    epsilon       = models.FloatField(default=0.001)
    function     = models.CharField(max_length=200, default='1 + x*x - cos(18*x*x)')

    #out
    iterations_number = models.IntegerField(default=0)
    function_minimum  = models.FloatField(default=0)
    arg_minimum       = models.FloatField(default=0)

    # когда в последний раз измеряли
    date = models.DateTimeField(auto_now_add=True)
    # название эксперимента. 
    name = models.CharField(max_length=200)
    # нашелся ли минимум
    result_exist = models.BooleanField(default=False)
    # добавить причину, если не нашелся
    exit_reason = models.CharField(max_length=200, default='default')
    # имя графика
    graph_image_filename = models.CharField(max_length=200,  default='')

    GLOBAL_SEARCH = 'global_search'
    PIYAVSKY = 'piyavsky'
    METHOD_CHOICES = (
        (GLOBAL_SEARCH, 'global_search'),
        (PIYAVSKY, 'piyavsky'),
    )
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default=GLOBAL_SEARCH,
    )

    owner = models.ForeignKey(
        User,
        related_name = 'measure',
        on_delete = models.CASCADE
        )

    class Meta:
        ordering = ('date',)

    def get_method(self):
        if self.method in self.METHOD_CHOICES[0]:
            return 'global_search'
        if self.method in self.METHOD_CHOICES[1]:
            return 'piyavsky'

    def __str__(self):
        return self.name