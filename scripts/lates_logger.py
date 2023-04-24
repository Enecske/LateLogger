import json

def log(lesson: str, array: list[tuple[str, int]]):
    students = []
    for (student, lateness) in array:
        students.append({'name': student, 'lateness': lateness})

    json_object = {
        'class': lesson,
        'students': students
    }

    with open("lates.json", "w", encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)