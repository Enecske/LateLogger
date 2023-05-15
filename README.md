# LateLogger
**A student lateness logger system for schools, written in Python**

## Features
#### Find students using a webcam
Using [Adam Geitgey](https://github.com/ageitgey)'s [face_recognition](https://github.com/ageitgey/face_recognition) library,
LateLogger can extract people from a web camera

#### Log the lateness of students
LateLogger detects the current class and starts itself with the current configuration of students for accurate lateness detection.
After a class has ended, LateLogger logs the students' lateness.

#### Easily manage classes and students
LateLogger offers command-line tools for managing the class schedule, classes and students.

The following commands are available:
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
- [Python 3.10+](https://www.python.org/)
- macOS or Linux (Face recognition might not work on Windows)
- [`face_recognition`](https://github.com/ageitgey/face_recognition)
- `validators` python package
- `events` python package
- Access to a MySQL server

### Installing on Mac or Linux
Install [Python 3.10+](https://www.python.org/downloads/) on your system\
If you already have Python installed, verify the version by running

```bash
python --version
```
*NOTE: If you have multiple versions of Python installed, you may need to use `python3` instead of `python` in bash shells*

Then, install [face_recognition](https://github.com/ageitgey/face_recognition), `validators` and `events` by running

```bash
pip install face_recongition
pip install validators
pip install events
```

Finally, download this repository by running
```bash
git clone https://github.com/Enecske/LateLogger
```
in the target folder.

### Setting LateLogger up
Set up LateLogger by running
```bash
python setup
```
Answer the questions in the prompt, and you're ready to go!

## Usage
After LateLogger is set up, run it with
```bash
python main.py
```
This will start LateLogger with the default settings (no set time or class)\
Time configuration is available by running
```bash
python main.py <weekday> <shifthour> <shiftminute>
```
- `weekday` is the day of the week (Monday is 1, Tuesday is 2 etc.)
- `shifthour` is a value between -23 and 23 that the hour should be shifted with
- `shiftminute` is a value between -59 and 59 that the minute should be shifted with

Launching LateLogger is also available with a single lesson, using
```bash
python main.py <lessonid>
```
- `lessonid` is the id of the lesson

## Configuring
LateLogger provides user-friendly command line tools for managing students and classes

### Editing the class schedule
The class schedule contains all the data necessary for LateLogger to know what class is currently

Managing the class schedule can be done with the following command:
```bash
python class_schedule <view|edit>
```

If you specified edit in the command, an additional terminal will appear:
```
  │  Mon  │  Tue  │  Wed  │  Thu  │  Fri  │
──┼───────┼───────┼───────┼───────┼───────┤
1 │9    9c│       │       │       │       │
2 │1    8a│       │       │       │       │
3 │2    9c│       │       │       │       │
4 │3   10b│       │       │       │       │
5 │       │       │       │       │       │
6 │4    9a│       │       │       │       │
7 │5    9b│       │6    9c│       │10  12a│

> 
```
*Example output*

#### Commands in the class schedule editor:
- `help`: Show the commands
- `show`: Display the class schedule
- `add <day> <hour> <class>`: Add a lesson in a given time
- `modify <day> <hour> <class>`: Modify the lesson in a given time
- `delete <day> <hour>`: Delete a lesson in a given time
- `exit`; `q`: Exit the class schedule editor