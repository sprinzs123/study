import sqlite3
import math_calculation as calculi
import collections
import datetime
# This file is responsible for all SQL queries

# Some global variables that are going to be used
# modifier is modifier used to determine what week consequitive week I have been studying
time = datetime.datetime.now()
modifier = (time.year - 2019) * 52
current_week = 4
# current_week = time.isocalendar()[1] - 25 + modifier
day_of_week = (['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
empty = 0


# Class that contains all sql quesries
class Database:
    def __init__(self, db):
        DATABASE = 'C://Users//cooker//PycharmProjects//pdf_report//study_tracker.db'
        self.conn = sqlite3.connect(DATABASE)
        # self.conn = sqlite3.connect("study_tracker.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS study "
                    "(id,"
                    "week,"
                    "date,"
                    "day,"
                    "start,"
                    "end,"
                    "total,"
                    "project,"
                    "topic)")
        self.conn.commit()

# select entire database
    def view(self):
        self.cur.execute("SELECT*FROM study")
        rows = self.cur.fetchall()
        return rows

# on
# add new values to the SQL
    def insert(self, id, week, date, day_week, time_in, time_out, time_total, project, subject):
        self.cur.execute("INSERT INTO study VALUES(?,?,?,?,?,?,?,?,?)",
                            (id, week, date, day_week, time_in, time_out, time_total, project, subject))
        self.conn.commit()

# off
# used to finish current section and calculates time spent on task
    def done_studying(self):
        self.cur.execute("SELECT*FROM study")
        t1 = str(self.cur.fetchall()[-1][4])
        t2 = str(time.time())[0:5]
        self.cur.execute("UPDATE study SET end=?,total=? WHERE start=?", (t2, database.last_cell_time(), t1))
        self.conn.commit()

# return a dictionary keys=variable, value=hrs on that variable
# get data to make graphs
    def project_time(self, find):
        self.cur.execute("SELECT "+find+" FROM study GROUP BY "+find+"")
        project_names = self.cur.fetchall()
        full_dik = {}
        for goal in project_names:
            goal = (goal[0])
            self.cur.execute("SELECT total FROM study WHERE "+find+"=?", (goal,))
            all_times = self.cur.fetchall()
            self.conn.commit()
            duration = calculi.cal_time(all_times)
            split_time = duration.split(":")
            hours = int(split_time[0])
            full_dik.update({goal: hours})
        return full_dik

# return dictionary where get hours spend on topic/subject
    def project_breakdown(self, copare, column, find):
        self.cur.execute("SELECT "+copare+", total FROM study WHERE "+column+"=? ", (find,))
        rows = self.cur.fetchall()
        print(rows)
        c = collections.defaultdict(list)
        for a, b in rows:
            c[a].append(b)  # add to existing list or create a new one
        grouped_tpl = list(c.items())
        print(grouped_tpl)
        sum_lib = {}
        for each in grouped_tpl:
            duration = calculi.cal_time(each[1])
            # print(duration)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1]) / 60), 2)
            sum_lib.update({each[0]: hours+min})
        return sum_lib

# last n weeks reports
    def weeks_report(self, find, number):
        # start_week = current_week - number
        self.cur.execute("SELECT "+find+" FROM study WHERE week BETWEEN ? and ? GROUP BY "+find+"", (1, 3))
        all_names = self.cur.fetchall()
        print(all_names)
        self.conn.commit()
        full_dik = {}
        for goal in all_names:
            goal = (goal[0])
            self.cur.execute("SELECT total FROM study WHERE " + find + "=? and week BETWEEN ? and ? ", (goal, 1, 3))
            all_times = self.cur.fetchall()
            self.conn.commit()
            duration = calculi.cal_time(all_times)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1])/60), 2)
            full_dik.update({goal: hours+min})
        print(full_dik)
        return full_dik

# tot
# extract all total columns in order to calculate total time from the start
    def total(self):
        self.cur.execute("SELECT total FROM study")
        all = self.cur.fetchall()
        self.conn.commit()
        return calculi.cal_time(all)

# d
# returns how much spent a day
    def day_total(self, date):
        self.cur.execute("SELECT total FROM study WHERE date=?", (date,))
        rows = self.cur.fetchall()
        self.conn.commit()
        return calculi.cal_time(rows)

# select last row of total to determine if our recording started or not
    def return_last_total(self, week_id):
        self.cur.execute("SELECT total FROM study WHERE id=(?)", (week_id,))
        all=self.cur.fetchall()[-1]
        self.conn.commit()
        return calculi.cal_time(all)

# up
# updates specific row with values and condition we are been provided
# (new, old) when manual update method
    def update(self, column, new, old):
        self.cur.execute("UPDATE study SET "+column+"=? WHERE "+column+"=?", (new, old))
        self.conn.commit()

# output how much time elapsed since we started activity
# calculate time difference to 'total' cell deference is between 'start' and 'current time'
    def last_cell_time(self,):
        self.cur.execute("SELECT*FROM study")
        # select last item from table and in [4] possition that is our 'time started' value
        # t1 is started, t2 is current time. Use it to find difference
        t1 = str(self.cur.fetchall()[-1][4])
        t2 = str(time.time())[0:5]
        return calculi.time_dif(t1, t2)

# wbs
# time spent per day of particular week
    def week_breakdown_by_day(self, week, day):
        self.cur.execute("SELECT total FROM study WHERE id=? and day = ?", (week, day))
        all = self.cur.fetchall()
        self.conn.commit()
        return calculi.cal_time(all)

# w
# amount of time spent a week
    def study_report_week(self, week_id):
        self.cur.execute("SELECT total FROM study WHERE id=(?)", (week_id,))
        all = self.cur.fetchall()
        self.conn.commit()
        return calculi.cal_time(all)

# s
# returns ammout you been working on a current task
    def study_time(self):
        return database.last_cell_time()
database = Database("studying.db")


# database.weeks_report('topic', 1)
