import math_calculation as calculi
import sql_code as query
import datetime


completed_projects = ['review analysis', 'security app', 'mit']


# MAKE SURE THAT GRAPHS WORKS

# full_dict = (query.database.project_time('topic'))
# limit = 5
# title = 'Top '+str(limit)+' topics'
# y_title = 'Time(hrs)'
# x_title = 'Names'
# short_dict = calculi.sorted_dict(full_dict, limit)
# calculi.bar_graph(short_dict,  title, y_title, x_title,'html')

# MAKE SURE THAT GRAPHS WORKS

# global variables that are going to be used in this part
time = datetime.datetime.now()

# this is a custom modifier I am using to track number of weeks in couple instances
# since i started adding data in 2019 it gives me 0
# 52 is number weeks a year, so first week of 2020 I am going to have 52 weeks recorded

modifier = (time.year - 2019) * 52



# use this list in several occasions in order to determine day of the week

day_of_week = (['monday', 'tuesday', 'wednesday', 'thursday','friday','saturday','sunday'])
empty=0


# menu is that user is going to see and what commands to use
def commands(menu):
    if menu == 'on':
        if (query.database.view()[-1][-3]) == 0:
            print("you are already recording your study time")
        else:
            topic = (input("topic(SQL, syntax, pygal: "))
            projects = (input("what in particular(PROJECT, CHEKIO, MIT, study.db, review analysis): ")).lower()
            # I used '-25 + modifier' because I wanted to make sure that my beginning week in 1
            # '-25' is a week number I started this project
            week = time.isocalendar()[1] - 25 + modifier
            week_id = str(time.month) + str(week)
            date = str(time.date())
            day = day_of_week[time.isoweekday() - 1]
            time_in = str(time.time())[0:5]
            time_out = 0
            time_total = 0
            query.database.insert(week_id, week, date, day, time_in, time_out, time_total, projects, topic)
    # stop recording

    if menu == 'off':
        if (query.database.view()[-1][-3]) == 0:
            query.database.done_studying()
            print("please come again")
            print(str(query.database.study_time()) + " last study time")
            print(str(query.database.day_report(time.date()) + " you studied today"))
        else:
            print("you haven't started studying yet")

    if menu == 's':
        print(str(query.database.study_time()) + " is your current study time")

    if menu == 'd':
        print(str(query.database.day_report(time.date()) + " you studied today"))

    if menu == "wbs":
        week = time.isocalendar()[1] - 25 + modifier
        week_id = str(time.month) + str(week)
        print("find hours total for week and each day")
        print("weekID is number of the month + week")
        print("current weekID is " + str(week_id))
        week_id = input("enter your value")
        for x in day_of_week:
            print(str(query.database.week_breakdown_by_day(week_id, x)) + ' ' + x)
        print((query.database.study_report_week(week_id)) + " total")

    # total time combined
    if menu == 'tot':
        print(query.database.total() + " is your total time so far, keep it up!!!")

    # manually adds new entry into database
    if menu == "new":
        topic = input("enter your topic (syntax)")
        projects = input("enter your project (study.db)")
        week = time.isocalendar()[1] - 25 + modifier
        week_id = str(time.month) + str(week)
        date = input("enter your date '2019-09-18' format")
        day = day_of_week[time.isoweekday() - 1]
        time_in = input("enter start time (00:00)")
        time_out = input("enter end time (00:00)")
        time_total = calculi.time_dif(time_in, time_out)
        query.database.new(week_id, week, date, day, time_in, time_out, time_total, projects, topic)

    # view entire database can be used for debugging
    if menu == 'v':
        print(query.database.view())

    # update all values in specific column
    # can be use used for column IDs
    if menu == 'up':
        print('update column values')
        column = input('what column update')
        set_to = input('result')
        initial = input('initial value')
        query.database.update(column, set_to, initial)

do_it = 'tot'
commands(do_it)






















# class that would be responsible for making graphs
class Showgraph:
    def __init__(self, goal, y_lable, x_axis, title, lmt, second_goal, focus, show):
        self.y_lable = y_lable
        self.x_axis = x_axis
        self.title = title
        self.lmt = lmt
        self.goal = goal
        self.second_goal = second_goal
        self.focus = focus
        self.show = show


# bar graph for topics and subjects, can limit how many items to display
    def sum_graph(self,):
        full_dict = (query.database.project_time(self.goal))
        title = 'Top ' + str(self.lmt) + ' '+self.goal+'s'
        short_dict = calculi.sorted_dict(full_dict, self.lmt)
        calculi.bar_graph(short_dict, title, self.y_lable, self.x_axis, self.show)

# line graph for that shows all time studying
    def total_time(self):
        full_dict = (query.database.project_time(self.goal))
        title = 'All weeks study times'
        calculi.line_graph(full_dict, title, self.y_lable, self.x_axis, self.show)

# one continue line that goes up as time added to data base
    def conseq_add(self):
        full_dict = (query.database.project_time(self.goal))
        full_dict = calculi.conseq_add(full_dict)
        title = 'All weeks study times'
        calculi.line_graph(full_dict, title, self.y_lable, self.x_axis, self.show)

# bar graph that show breakdown of certain project or topic
# .project_breakdown('topic', 'project', 'review analysis') would give all topics in project
    def one_summary(self):
        full_dict = (query.database.project_breakdown(self.goal, self.second_goal, self.focus))
        title = self.title
        x_title = 'Names'
        short_dict = calculi.sorted_dict(full_dict, self.lmt)
        calculi.bar_graph(short_dict,  title, self.y_lable, self.x_axis, self.show)

# bar graph of all projects that been completed
    def done_proj(self):
        full_dict = (query.database.project_time(self.goal))
        full_dict = (calculi.completed(completed_projects, full_dict))
        title = 'All completed projects'
        calculi.horiz_bar(full_dict, title, self.y_lable, self.x_axis, self.show)

# line graph that compares weekly progress and overall progress for last n weeks
    def past_history(self):
        full_dict = (query.database.weeks_report(self.goal, self.lmt))
        conseq_dik = calculi.conseq_add(full_dict)
        all_list = list(full_dict.values())
        conseq_list = list(conseq_dik.values())
        calculi.multiple_line(all_list, conseq_list, self.title, self.y_lable, self.x_axis, self.show)

# (total, weekly, title, conseq, y_title, x_title, output)

#
# x_axis = 'x axis go here'
# y_axis = 'Time(hrs)'
# title = 'this is title'
# limit = 10
# find = 'topic'
# focus = 'review analysis'
# compare = 'project'
# output = 'html'
# graphing = Showgraph(find, y_axis, x_axis, title, limit, compare, focus, output).one_summary()
# graphing.sum_graph()








