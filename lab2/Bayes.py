__author__ = 'Den'

from os import listdir
from os.path import join, isfile

for f in listdir('pu1'):
    print(isfile(f))