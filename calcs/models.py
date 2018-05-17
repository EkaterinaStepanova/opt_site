from django.db import models


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

    # когда в последний раз измеряли
    date = models.DateTimeField(auto_now_add=True)
    # название эксперимента. 
    name = models.CharField(max_length=200)
    # нашелся ли минимум
    result_exist = models.BooleanField(default=False)
    # добавить причину, если не нашелся
    exit_reason = models.CharField(max_length=200, default='default')

    # GLOBAL_SEARCH = 'gs'
    # PIYAVSKY = 'pi'
    # METHOD_CHOICES = (
    #     (GLOBAL_SEARCH, 'global_search'),
    #     (PIYAVSKY, 'piyavsky'),
    # )
    # method = models.CharField(
    #     max_length=2,
    #     choices=METHOD_CHOICES,
    # )

    class Meta:
        ordering = ('date',)

    def get_method(self):
        # if self.method in self.GLOBAL_SEARCH:
        #     return 'global_search'
        # if self.method in self.PIYAVSKY:
        #     return 'piyavsky'
        return 'global_search'

    def __str__(self):
        return self.name