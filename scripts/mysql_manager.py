import mysql.connector
import face_registry
import yaml
import numpy

try:
    config = yaml.safe_load(open('./conf.yaml'))['database']

    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
except FileNotFoundError:
    print("[Error] Config file not found, run 'python setup' to set up latelogger")
    exit(1)
except mysql.connector.errors.ProgrammingError as e:
    print(f"[MySQL Error] {e} (Check config file)")
    exit(1)
except TypeError as e:
    print(f"[Error] {e}, check config file")
    exit(1)

cursor = db.cursor(buffered=True)

def save_encoding(lessonid: int, encoding: numpy.ndarray, name: str):
    lesson = get_lesson_name(lessonid)
    save_encoding_to_class(lesson, encoding, name)


def save_encoding_to_class(classname: str, encoding: numpy.ndarray, name: str):
    values = (name, encoding.dumps())
    cursor.execute(
        f"INSERT INTO {classname}_students (name, face_encoding) VALUES (%s, %s)", values)
    db.commit()


def save_encoding_raw(lessonid: int, registry_item: dict):
    save_encoding(lessonid, registry_item["encoding"], registry_item["name"])


def retrieve_encoding(lessonid: int, name: str):
    lesson = get_lesson_name(lessonid)

    cursor.execute(
        f"SELECT face_encoding FROM {lesson}_students WHERE name=\"{name}\"")

    result = []

    for x in cursor:
        result.append(x)

    return numpy.loads(result[0][0])


def load_all(lessonid: int):
    lesson = get_lesson_name(lessonid)

    try:
        cursor.execute(f"SELECT id,name,face_encoding FROM {lesson}_students")
    except mysql.connector.errors.ProgrammingError:
        print(f"[Error] Class '{lesson}' not found!")
        exit(1)

    students = ""
    length = 0

    for x in cursor:
        face_registry.load(numpy.loads(x[2]), x[1])
        students += ", " + x[1]
        length += 1

    students = students[2:]

    print(f"Loaded {length} students from class {lesson}: {students}")


def get_students(classname: str):
    cursor.execute(f"SELECT id,name FROM {classname}_students")
    return cursor.fetchall()


def rename_student(classname: str, id: int, newname: str):
    cursor.execute(
        f"UPDATE {classname}_students SET name=\"{newname}\" WHERE id={id}")
    db.commit()


def delete_student(classname: str, id: int):
    cursor.execute(f"DELETE FROM {classname}_students WHERE id={id}")
    db.commit()


def get_lesson_name(lessonid: int):
    try:
        cursor.execute(
            f"SELECT class FROM class_schedule WHERE lessonid={lessonid}")

        return cursor.fetchone()[0]
    except:
        return None


def get_lesson_time(lessonid: int):
    cursor.execute(
        f"SELECT day,time FROM class_schedule WHERE lessonid={lessonid}")
    return cursor.fetchone()


def get_lesson_by_time(day: int, time: int):
    cursor.execute(
        f"SELECT lessonid FROM class_schedule WHERE day={day} AND time={time}")
    try:
        return cursor.fetchone()[0]
    except:
        return None


def add_lesson(day: int, hour: int, classname: str):
    cursor.execute(
        f"INSERT INTO class_schedule (class, day, time) VALUES (%s, %s, %s)", (classname, day, hour))
    db.commit()


def modify_lesson(day: int, hour: int, classname: str):
    cursor.execute(
        f"UPDATE class_schedule SET class=\"{classname}\" WHERE day={day} AND time={hour}")
    db.commit()


def delete_lesson(day: int, hour: int):
    cursor.execute(
        f"DELETE FROM class_schedule WHERE day={day} AND time={hour}")
    db.commit()

def create_class(classname: str):
    if not classname.isalnum():
        raise ValueError(
            "Field 'classname' can only contain alphanumerical characters")
    if len(classname) > 3:
        raise ValueError("Field 'classname' can only be 3 or less characters")

    cursor.execute(
        f"CREATE TABLE {classname}_students (id INT NOT NULL AUTO_INCREMENT, name TINYTEXT NOT NULL, face_encoding BLOB NOT NULL, PRIMARY KEY(id))")

def clear_class(classname: str):
    cursor.execute(
        f"DELETE FROM {classname}_students")
    db.commit()

def delete_class(classname: str):
    cursor.execute(
        f"DROP TABLE {classname}_students")
    
def does_class_exist(classname: str):
    cursor.execute(f"SHOW TABLES LIKE '{classname}_students'")
    return cursor.fetchone() != None