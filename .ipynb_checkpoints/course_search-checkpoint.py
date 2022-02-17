'''
course_search is a Python script using a terminal based menu to help
students search for courses they might want to take at Brandeis
'''

from schedule import Schedule
import sys

schedule = Schedule()

TOP_LEVEL_MENU = '''
quit
reset
term  (filter by term)
course (filter by coursenum, e.g. COSI 103a)
instructor (filter by instructor)
subject (filter by subject, e.g. COSI, or LALS)
title  (filter by phrase in title)
description (filter by phrase in description)
timeofday (filter by day and time, e.g. meets at 11 on Wed)
waiting_list (filter by number of students in waiting list)
independent (filter by independent_study == true or independent_study == false.)
'''

terms = {c['term'] for c in schedule.courses}

def topmenu():
    '''
    topmenu is the top level loop of the course search app
    '''
    global schedule
    while True:
        #moved schedule.load_courses() inside the loop to allow for consecutive queries.
        schedule.load_courses()
        schedule = schedule.enrolled(range(5,1000)) # eliminate courses with no students
        command = input(">> (h for help) ")
        if command=='quit':
            return
        elif command in ['h','help']:
            print(TOP_LEVEL_MENU)
            print('-'*40+'\n\n')
            continue
        elif command in ['r','reset']:
            schedule.load_courses()
            schedule = schedule.enrolled(range(5,1000))
            continue
        elif command in ['t', 'term']:
            term = input("enter a term:"+str(terms)+":")
            schedule = schedule.term([term]).sort('subject')
        elif command in ['s','subject']:
            subject = input("enter a subject:")
            schedule = schedule.subject([subject])
        #filters the courses by number of students in waiting list
        elif command in ['w', "waiting_list"]:
            waiting_number = input("enter a number:")
            schedule = schedule.waiting(waiting_number)
        elif command in ['ti', 'title']:
            title_name = input("enter a title:")
            schedule = schedule.title(title_name)
        elif command in ['d', 'description']:
            descrip = input("enter a description:")
            schedule = schedule.description(descrip)
        elif command in ['i', 'independent']:
            truth_value = input("enter 't' for True or 'f' for False:")
            truth_value = True if truth_value == "t" else False
            schedule = schedule.independent(truth_value)
        else:
            print('command',command,'is not supported')
            continue

        print("courses has",len(schedule.courses),'elements',end="\n\n")
        print('here are the first 10')
        for course in schedule.courses[:10]:
            print_course(course)
        print('\n'*3)

def print_course(course):
    '''
    print_course prints a brief description of the course 
    '''
    print(course['subject'],course['coursenum'],course['section'],
          course['name'],course['term'],course['instructor'], course['waiting'])

if __name__ == '__main__':
    topmenu()

