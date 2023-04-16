# LateLogger
**A student latency logger system for schools, written in Python**

## Features
#### Find students using webcam
Using [Adam Geitgey](https://github.com/ageitgey)'s [face_recognition](https://github.com/ageitgey/face_recognition) library,
LateLogger can extract people from a webcamera

#### Log the lateness of students
LateLogger detects the current class, and starts itself with the current configuration of students for accurate lateness detection.
After a class has ended, LateLogger logs the students' lateness.

#### Easily manage classes and students
LateLogger offers command-line tools for managing the class schedule, classes and students.

The following commands are avaiable:
- `python setup`: Set up the config file
- `python class_schedule <view|edit>`: Manage class schedule
- `python create_class <classname>`: Create a new class
- `python edit_class <classname>`: Edit an existing class
- `python delete_class <classname>`: Delete a class
- `python load_image <filename> <name> <class>`: Load a student from an image file
- `python webcam_test`: Test the webcam's configuration
- `python main.py [lessonid]`: Start LateLogger (additionally with a given lesson)

## Installation
### Requirements
- Python 3.10+
- macOS or Linux (Face recognition might not work on Windows)
- [`face_recognition`](https://github.com/ageitgey/face_recognition)
- `validators` python package
- Access to a MySQL server

### Installing on Mac or Linux
Install Python 3.10+ on your system
If you already have python installed, verify the version by running

```bash
python --version
```

Then, install [face_recognition](https://github.com/ageitgey/face_recognition) and `validators` by running

```bash
pip install face_recongition
pip install validators
```

Finally, download this repository by running
```bash
git clone https://github.com/Enecske/LateLogger
```
in the target folder.

### Setting LateLogger up
Set up LateLogger by running
```bash
python setup.py
```
Answer the questions in the prompt, and you're ready to go!
