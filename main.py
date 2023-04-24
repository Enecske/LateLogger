from datetime import *
from scripts import lates_webcam, time_manager, mysql_manager
import sys
from mysql.connector import ProgrammingError

mode = 'default'

match len(sys.argv):
    case 2:
        mode = 'setlesson'
    case 4:
        mode = 'settime'
    case 1:
        mode = 'default'
    case _:
        print("[Error] Arguments not match, usage: 'python main.py [<lessonid>|<<weekday> <hour> <minute>>]'")
        exit(1)

while True:
    try:
        lessonid = 0

        if mode == 'setlesson':
            try:
                lessonid = int(sys.argv[1])
            except ValueError as e:
                print(f"[Argument Error] {e}")
                exit(1)

        else:
            day = datetime.now().weekday() + 1

            if mode == 'settime':   
                try:
                    day = int(sys.argv[1])
                    hour = int(sys.argv[2])
                    minute = int(sys.argv[3])

                    if day < 1 or day > 5:
                        raise ValueError("field 'day' must be between 1 and 5")
                    if hour < -23 or hour > 23:
                        raise ValueError("field 'hour' must be between -23 and 23")
                    if minute < -59 or minute > 59:
                        raise ValueError("field 'minute' must be between -59 and 59")
                except ValueError as e:
                    print(f"[Argument Error] {e}")
                    exit(1)

                shift = (hour, minute)
                time_manager.shift = shift
            
            time = time_manager.get_lesson()
            if time == None or day > 5:
                print("[Error] There is no class now")
                exit(1)
            try:
                lessonid = mysql_manager.get_lesson_by_time(
                    day, time)
                if lessonid == None:
                    print("[Error] There is no class now")
                    exit(1)
            except ProgrammingError as e:
                print(f"[MySQL Error] {str(e)}")
                exit(1)

        lates_webcam.start_webcam(lessonid, mode != 'setlesson')
    except KeyboardInterrupt:
        print(" Keyboard Interrupt - LateLogger stopped")
        exit(0)