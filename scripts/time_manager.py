from datetime import *
from scripts import mysql_manager, event_manager

lesson_times = [(8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 15)]
lesson_starts = [(7, 45), (8, 45), (9, 45), (10, 45), (11, 45), (12, 45), (13, 45)]
lesson_ends = [(8, 45), (9, 45), (10, 45), (11, 45), (12, 45), (13, 45), (15, 0)]

shift: tuple[int, int] = (0, 0)

def shift_time(time: datetime, shift: tuple[int, int]):
    hour = time.hour + shift[0]
    minute = time.minute + shift[1]

    while minute < 0:
        minute += 60
        hour -= 1

    return (int(hour), int(minute), time.second)

def get_time(): return shift_time(datetime.now(), shift)

def get_lesson():
    shifted = shift_time(datetime.now(), shift)
    curr_hour = shifted[0]
    curr_minute = shifted[1]
    current = curr_minute + (curr_hour * 60)

    if current >= lesson_ends[-1][1] + (lesson_ends[-1][0] * 60):
        print("Today's lessons ended, shutting LateLogger down... Goodbye!")
        event_manager.__events.shutdown()
        exit(0)

    min_dist = 100
    lesson = None
    for i in range(len(lesson_starts)):
        hour, minute = lesson_starts[i]
        minute += hour * 60

        temp = current - minute

        if(temp < min_dist and temp >= 0):
            min_dist = temp
            lesson = i + 1

    return lesson

def get_lateness(lessonid: int):
    lesson = mysql_manager.get_lesson_time(lessonid)[1] - 1

    shifted = shift_time(datetime.now(), shift)

    curr_hour = shifted[0]
    curr_minute = shifted[1]
    current = curr_minute + (curr_hour * 60)

    hour, minute = lesson_times[lesson]
    minute += hour * 60

    temp = current - minute

    return temp

def is_end():
    shifted = shift_time(datetime.now(), shift)

    curr_hour = shifted[0]
    curr_minute = shifted[1]
    current = curr_minute + (curr_hour * 60)

    min_dist = 100
    for i in range(len(lesson_ends)):
        hour, minute = lesson_ends[i]
        minute += hour * 60

        temp = current - minute

        if temp == 0:
            return True
        
    return False