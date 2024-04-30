import numpy as np
import heapq
import pandas as pd
import random
from math import floor
import matplotlib.pyplot as plt
from IPython.display import display, clear_output

plt.ion()

df_morning = pd.read_excel("Demend_Stats.xlsx", usecols='A:Q', nrows=19, sheet_name='Sheet1')  # read morning demand table
df_morning = df_morning.set_index(['Unnamed: 0'])  # define first column to index
df_evening = pd.read_excel("Demend_Stats.xlsx", usecols='A:Q', nrows=19, sheet_name='Sheet2')  # read evening demand table
df_evening = df_evening.set_index(['Unnamed: 0'])  # define first column to index

df_morning = df_morning.transpose()  # transpose the dataframe to read correctly the table (from and to)
df_evening = df_evening.transpose()  # transpose the dataframe to read correctly the table (from and to)


class Event():
    def __init__(self, time, event_type, curr_area = None, to = None):
        self.time = time  # time of the event
        self.event_type = event_type  # type of te event
        self.curr_area = curr_area  # current area of the customer
        self.to = to  # destination area of the customer
        heapq.heappush(P, self)  # add the event to events list

    def __lt__(self, event2):
        return self.time < event2.time


curr_time = 0  # define start of the day
sim_time = 16  # define Tmax
scooters = {'312': 15, '313': 15, '314': 15, '315': 15, '316': 15, '317': 15, '321': 15, '322': 15, '323': 15,\
            '324': 15, '325': 15, '326': 15, '331': 15, '332': 15, '333': 15, '341': 15}  # number of scooters per area
damaged_scooters = {'312': 0, '313': 0, '314': 0, '315': 0, '316': 0, '317': 0, '321': 0, '322': 0, '323': 0,\
                    '324': 0, '325': 0, '326': 0, '331': 0, '332': 0, '333': 0, '341': 0}  # number of damaged scooters per area
cal_scooter = {'312': 0, '313': 0, '314': 0, '315': 0, '316': 0, '317': 0, '321': 0, '322': 0, '323': 0,\
               '324': 0, '325': 0, '326': 0, '331': 0, '332': 0, '333': 0, '341': 0}  # Reference table for calculating the transfers
walks = {'312': 0, '313': 0, '314': 0, '315': 0, '316': 0, '317': 0, '321': 0, '322': 0, '323': 0, '324': 0,\
         '325': 0, '326': 0, '331': 0, '332': 0, '333': 0, '341': 0}  # number of walks from every area
Neighbors = {'312': [313, 317, 331], '313': [312, 314, 316], '314': [313, 315], '315': [314, 316, 323], \
             '316': [313, 315, 322, 317], '317': [312, 331, 316, 321], '321': [331, 317, 322, 326], \
             '322': [323, 316, 321, 325], '323': [315, 322, 325, 324], '324': [325, 323], '325': [324, 341, 326, 322, 323], \
             '326': [331, 321, 325, 333, 332], '331': [312, 317, 321, 326, 332], '332': [331, 326, 333], \
             '333': [332, 326, 341], '341': [325, 333]}  # dictionary of neighbors

leavers = 0  # number of leavers because damaged scooter or unavailability
transports = 0  # number of transports
area_i = [312, 313, 314, 315, 316, 317, 321, 322, 323, 324, 325, 326, 331, 332, 333, 341]  # list of all areas
rents = [0]*16  # list of number of rents per hour


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i-0.25, y[i], y[i])


def addlabels2(x, y):
    for i in range(len(x)):
        plt.text(i+0.2, y[i], y[i])


for day in range(350):  # the simulation runs 350 days (50 weeks)
    curr_time = 0  # define start of the day
    number_of_rent_scooter = 0  # number of scooters in rent, only for bonus part
    P = []  # list of event, sort by time
    Event(16, 'transportation')
    for i in area_i:  # creates the first arrivals for each area
        for j in area_i:
            if df_morning[i][j] > 0:
                lamda = df_morning[i][j]
                x = np.random.exponential(1 / lamda)
                Event(x, 'scooter arrival', i, j)
            else:  # creates the first arrivals for each area if there is no arrival in morning
                if df_evening[i][j] > 0:
                    lamda = df_evening[i][j]
                    x = np.random.exponential(1 / lamda)
                    Event(x + 8, 'scooter arrival', i, j)

    event = heapq.heappop(P)
    while curr_time <= sim_time:  # the daily simulation runs 16 hours
        # i = event.curr_area
        # j = event.to
        if event.event_type == 'scooter arrival':
            if scooters[f'{event.curr_area}'] > 0:  # we have at least one scooter in the current area
                y = np.random.uniform(2 / 60, 3 / 60)
                Event(curr_time + y, "end of walking", event.curr_area, event.to)
            else:
                s = np.random.uniform(0, 1)
                if s <= 0.5:
                    # smart way of choosing neighbor to walk to- the neighbor with the most available scooter
                    max_scoot = 0
                    max_scooter_neighbor = 0
                    for neighbor in (Neighbors[f'{event.curr_area}']):
                        if scooters[f'{neighbor}'] > 0:
                            if scooters[f'{neighbor}'] > max_scoot:
                                max_scoot = scooters[f'{neighbor}']
                                max_scooter_neighbor = neighbor
                    if max_scoot > 0:
                        walks[f'{event.curr_area}'] += 1
                        w = np.random.normal(8 / 60, 2 / 60)
                        Event(curr_time + w, "walking to neighbor", max_scooter_neighbor, event.to)
                    else:
                        leavers += 1  # no available scooters - user is giving up service
                else:
                    leavers += 1  # in 50% the user give yp immediately
            if event.time < 8:  # create next arriving - if it's morning time
                lamda_1 = df_morning[event.curr_area][event.to]
                x = np.random.exponential(1 / lamda_1)
                Event(event.time + x, "scooter arrival", event.curr_area, event.to)
            else:  # create next arriving - if it's evening time
                lamda_1 = df_evening[event.curr_area][event.to]
                if lamda_1 > 0:
                    x = np.random.exponential(1 / lamda_1)
                    Event(event.time + x, "scooter arrival", event.curr_area, event.to)

        elif event.event_type == 'end of walking':
            z = np.random.normal(15 / 60, 3 / 60)
            if scooters[f'{event.curr_area}'] > 0 and (z + curr_time) < 16:
                scooters[f'{event.curr_area}'] -= 1  # drops one scooter from the current area
                rents[floor(curr_time)] += 1  # add one rent for this hour
                number_of_rent_scooter += 1
                Event(curr_time + z, "rental end", event.curr_area, event.to)
            else:
                leavers += 1  # no available scooters - user is giving up service or the service will finish after 22:00

        elif event.event_type == 'walking to neighbor':
            z = np.random.normal(15 / 60, 3 / 60)
            if scooters[f'{event.curr_area}'] > 0 and (z + curr_time) < 16:
                scooters[f'{event.curr_area}'] -= 1  # drops one scooter from the current area
                rents[floor(curr_time)] += 1  # add one rent for this hour
                number_of_rent_scooter += 1
                Event(curr_time + z, "rental end", event.curr_area, event.to)
            else:
                leavers += 1  # no available scooters - user is giving up service or the service will finish after 22:00

        elif event.event_type == 'rental end':
            p = np.random.uniform(0, 1)
            number_of_rent_scooter -= 1
            if p < 0.005:  # if scooter is damaged
                leavers += 1  # user is giving up service because od damaged scooter
                damaged_scooters[f'{event.curr_area}'] += 1  # add one scooter for the starting area
            else:
                scooters[f'{event.to}'] += 1  # the customer finish his ride - add one scooter for the destination area

        elif event.event_type == 'transportation':
            for area in area_i:
                cal_scooter[f'{area}'] = scooters[f'{area}'] + damaged_scooters[f'{area}']  # The total number of scooters in each area

            for area in area_i:
                if cal_scooter[f'{area}'] != 15:
                    if cal_scooter[f'{area}'] > 15:  # in any area where there are more than 15 scooters, we will add the difference to transports
                        transports += (cal_scooter[f'{area}'] - 15)
            scooters = {'312': 15, '313': 15, '314': 15, '315': 15, '316': 15, '317': 15, '321': 15, '322': 15, '323': 15, \
                        '324': 15, '325': 15, '326': 15, '331': 15, '332': 15, '333': 15,
                        '341': 15}  # number of scooters per area
            damaged_scooters = {'312': 0, '313': 0, '314': 0, '315': 0, '316': 0, '317': 0, '321': 0, '322': 0, '323': 0, \
                                    '324': 0, '325': 0, '326': 0, '331': 0, '332': 0, '333': 0, '341': 0}  # number of damaged scooters per area
            cal_scooter = {'312': 0, '313': 0, '314': 0, '315': 0, '316': 0, '317': 0, '321': 0, '322': 0, '323': 0, \
                               '324': 0, '325': 0, '326': 0, '331': 0, '332': 0, '333': 0,
                               '341': 0}  # Reference table for calculating the transfers
        ###########################  Bonus Part  ##########################################################
        width = 0.25
        ind = np.arange(16)
        pl_walks = list(walks.values())
        pl_scooter = list(scooters.values())
        plt.cla()
        plt.title(f'time: {event.time} \n number of scooter in rent: {number_of_rent_scooter} \n \
        number of leavers: {leavers}  number of transports: {transports}', fontsize=20)
        plt.xlabel("area")
        plt.bar(ind - 0.2, pl_scooter, width, label = 'number of available scooters per area')
        addlabels(area_i, pl_scooter)
        plt.bar(ind + 0.2, pl_walks, width, label = 'number of walks from every area')
        plt.xticks(ind + width/2, area_i)
        plt.legend()
        addlabels2(area_i, pl_walks)
        clear_output(wait=True)
        plt.pause(0.001)
        plt.show()
        #####################################################################################################
        event = heapq.heappop(P)
        curr_time = event.time


hours = [0] * 16
for i in range(6, 22):
    hours[i - 6] = str(i) + ":00"


for area in area_i:
    walks[f'{area}'] = walks[f'{area}']/350
rents_list = [a / 350 for a in (rents)]
transports = transports / 350
leavers = leavers/350
print(f'number of walks in day from every area is:{walks}')
print(f'number of leavers per every day is: {leavers}')
print(f'number of transports per every day is: {transports}')
print(f'number of rents per hours per every day is: {rents_list}')

# values = list(walks.values())
#
# plt.bar(range(len(walks)), values, tick_label=area_i)
# plt.show()
#
# plt.bar(range(16), rents_list, align='center', color='green')  # the first-rate of total 100 iterations
# plt.xticks(range(16), hours)
# plt.title('Number of rents per hours per every week is')
# plt.show()





