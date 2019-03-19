import requests
import json

url_postprof = 'http://127.0.0.1:5000/postprofessor'
url_postcourse = 'http://127.0.0.1:5000/postcourse'
url_postprofcourse = 'http://127.0.0.1:5000/postprofcourse'

with open('Courses_total.csv') as f:
    f.readline()
    for l in f:
        l = l.rstrip('\n').split(',')
        r = requests.post(url=url_postprofcourse,json={'cname':l[2],'pname':l[1]})

