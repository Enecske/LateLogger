from datetime import *
import scripts.lates_webcam as lates_webcam
import scripts.time_manager as time_manager
import scripts.mysql_manager as mysql_manager
import sys
from mysql.connector import ProgrammingError

while True:
    try:
        lessonid = 0

        try:
            lessonid = int(sys.argv[1])

        except IndexError as e:
            time = time_manager.get_lesson()
            if time == None or datetime.now().weekday() + 1 -4 > 5:
                print("[Error] There is no class now")
                exit(1)
            try:
                lessonid = mysql_manager.get_lesson_by_time(
                    datetime.now().weekday() + 1 -4, time)
                if lessonid == None:
                    print("[Error] There is no class now")
                    exit(1)
            except ProgrammingError as e:
                print(f"[MySQL Error] {str(e)}")
                exit(1)

        except ValueError as e:
            print(f"[Argument Error] {e}")
            exit(1)

        lates_webcam.start_webcam(lessonid)
    except KeyboardInterrupt:
        print(" Keyboard Interrupt - LateLogger stopped")
        exit(0)