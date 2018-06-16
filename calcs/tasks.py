from optsite.celery import app
from calcs.models import Measure
from celery.exceptions import SoftTimeLimitExceeded
from django.db import models

from math import cos, pi, fabs
import uuid

import pylab
from matplotlib import mlab
import os
from py_expression_eval import Parser
import numpy as np

def f_(x):
    #return 10 + x*x - 10*cos(2*pi*x)
    return 1 + x*x - cos(18*x*x)

#-----------Strongin----------------------
    
def get_m_S(M, r):
    if M < 0.0000001:
        return 1
    else:
        return r*M
        
def R_S(m, a, b, c, d):
    buf = m * (b - a)
    res = (buf + (d - c)*(d - c)/buf-
                2*(d + c))
    return res

def global_search(measure):

    a=measure.bottom_border
    b=measure.upper_border
    r=measure.r
    epsilon=measure.epsilon

    try:
        parser = Parser()
        func = parser.parse(measure.function)
        f = lambda x: func.evaluate({func.variables()[0]: x})


        x = [a, b]
        z = [f(a), f(b)]
        t = 1
        k = 2 
        M = fabs((z[1] - z[0])/(x[1] - x[0]))
        while (x[t] - x[t-1] > epsilon):
            for i in range(1, k):
                M_buf = fabs((z[i] - z[i-1])/(x[i] - x[i-1]))
                if M_buf > M:
                    M = M_buf
            #2
            m = get_m_S(M, r)
            #3
            R_max = R_S(m, x[0], x[1], z[0], z[1])
            t = 1
            for i in range(2, k):
                R_buf = R_S(m, x[i-1], x[i], z[i-1], z[i])
                if ( R_buf > R_max ):
                    R_max = R_buf
                    t = i
            #4       
            x_new = (x[t] + x[t-1])/2 - (z[t] - z[t-1])/2/m
            z_new = f(x_new)
            
            if x_new > x[k-1]:
                x.append(x_new)
                z.append(z_new)
            else:
                for i in range(0, k):
                    if x_new < x[i]:
                        x.insert(i, x_new)
                        z.insert(i, z_new)
                        break
            k = k + 1
            #5 and #1
            
        min_x = x[0]
        min_z = z[0] 
        for i in range(1, k):
            if f(x[i]) < min_z:
                min_x = x[i]
                min_z = f(x[i])
    

        measure.iterations_number = k
        measure.function_minimum = min_z
        measure.arg_minimum = min_x
        measure.result_exist = True
        
        #print("Strongin. Minimum on ",k," iteration: f(",min_x,") = ",min_z)
        
        #drawing
        xmin = a
        xmax = b
        dx = (float)(xmax-xmin)/200
        xlist = np.arange(xmin, xmax, dx)
        ylist1 = [f(x) for x in xlist]
        fig = pylab.figure(0)
        pylab.subplot()
        pylab.plot(xlist, ylist1, "b-") 
        pylab.plot(x, z, "o") 
        pylab.plot(min_x, min_z, "ro")  
        #fig.suptitle('Strongin '+str(k)+' iterations. X = '+str(min_x), fontsize=12)


        filename = str(uuid.uuid1())+'.jpg'
        fig.savefig('media/'+filename)
        fig.clear()
        measure.graph_image_filename = filename

    except Exception as exc:
        measure.result_exist = False
        measure.exit_reason = str(exc)

    return measure
    #pylab.show()

#----------End of Strongin--------------

#---------------Piyavsky----------------

def get_m_P(M, r):
    if M < 0.0000001:
        return 1
    else:
        return r*M
        
def R_P(m, a, b, c, d):
    buf = m * (b - a)
    return 0.5 * m * (b - a) - 0.5 * (c + d)

def piyavsky(measure):
    a=measure.bottom_border
    b=measure.upper_border
    r=measure.r
    epsilon=measure.epsilon

    try:
        parser = Parser()
        func = parser.parse(measure.function)
        f = lambda x: func.evaluate({func.variables()[0]: x})

        x = [a, b]
        z = [f(a), f(b)]
        t = 1
        k = 2 
        M = fabs((z[1] - z[0])/(x[1] - x[0]))
        while (x[t] - x[t-1] > epsilon):
            for i in range(1, k):
                M_buf = fabs((z[i] - z[i-1])/(x[i] - x[i-1]))
                if M_buf > M:
                    M = M_buf
            #2
            m = get_m_P(M, r)
            #3
            R_max = R_P(m, x[0], x[1], z[0], z[1])
            t = 1
            for i in range(2, k):
                R_buf = R_P(m, x[i-1], x[i], z[i-1], z[i])
                if ( R_buf > R_max ):
                    R_max = R_buf
                    t = i
            #4       
            x_new = (x[t] + x[t-1])/2 - (z[t] - z[t-1])/2/m
            z_new = f(x_new)
            
            if x_new > x[k-1]:
                x.append(x_new)
                z.append(z_new)
            else:
                for i in range(0, k):
                    if x_new < x[i]:
                        x.insert(i, x_new)
                        z.insert(i, z_new)
                        break
            k = k + 1
            #5 and #1
            
        min_x = x[0]
        min_z = z[0] 
        for i in range(1, k):
            if f(x[i]) < min_z:
                min_x = x[i]
                min_z = f(x[i])
    

        measure.iterations_number = k
        measure.function_minimum = min_z
        measure.arg_minimum = min_x
        measure.result_exist = True

        #print("Piyavsky. Minimum on ",k," iteration: f(",min_x,") = ",min_z)

        #drawing
        xmin = a
        xmax = b
        dx = (float)(xmax-xmin)/200
        xlist = np.arange(xmin, xmax, dx)
        ylist = [f(x) for x in xlist]
        fig = pylab.figure(1)
        pylab.subplot()
        pylab.plot(xlist, ylist, "b-") 
        pylab.plot(x, z, "o") 
        pylab.plot(min_x, min_z, "ro")  
        #fig.suptitle('Piyavsky '+str(k)+' iterations. X = '+str(min_x), fontsize=12)

        filename = str(uuid.uuid1())+'.jpg'
        fig.savefig('media/'+filename)
        fig.clear()
        measure.graph_image_filename = filename

    except Exception as exc:
        measure.result_exist = False
        measure.exit_reason = str(exc)

    return measure
    #pylab.show()

#----------End of Piyavsky--------------

@app.task(time_limit=15, soft_time_limit=10)
def minimize(measure_id):
    measure = Measure.objects.get(pk=measure_id)
    if not os.path.exists('media'):
        os.makedirs('media')
    try:
        result = globals()[measure.get_method()](measure)
        result.save()
        return result.result_exist
    except SoftTimeLimitExceeded:
        measure.result_exist = False
        measure.exit_reason = str(SoftTimeLimitExceeded)
    return False
    


#----------End of Iterations------------
    
# a = float(input("Enter left border: "))
# b = float(input("Enter right border: "))
# epsilon = 0.01
# r = 2
# globSearch(a, b, r, epsilon)
# piyavskiy(a, b, r, epsilon)
# iterations(a, b, epsilon)
# pylab.show()
# globSearch(-3.5, 5.5, 2, 0.01)    
# globSearch(-2.5, 2.0, 2, 0.1)         
        
            
