import pytest
from cropanalysis import *


#  The month should be in the range of crop_cal 1,2,3
def test_climatology01():
    new_date = dt.datetime.strptime('12-02-2015','%d-%m-%Y')
    state='alabama'
    years=5
    column='ndvi'
    
    assert climatology(column,state,new_date,years) == None , 'SUCCESS'

#  The month should be in the range of crop_cal 1,2,3
def test_climatology02():
    new_date = dt.datetime.strptime('12-08-2017','%d-%m-%Y')
    state='alabama'
    years=10
    column='ndvi'
    # print(type(new_date))
    # dset = insets()
    assert climatology(column,state,new_date,years) != None , 'SUCCESS'

# climatology -- number of years must be atleast 5
def test_climatology03():
    new_date = dt.datetime.strptime('12-08-2017','%d-%m-%Y')
    state='alabama'
    years=3
    column='ndvi'
    
    assert climatology(column,state,new_date,years) == None , 'SUCCESS'
