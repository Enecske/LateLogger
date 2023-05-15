from events import Events

__events: Events = Events()

# Registering existing events
__events.lesson_ended += lambda lessonid: None
__events.lesson_started += lambda lessonid: None
__events.shutdown += lambda: None

def addEventListener(event: str, callback: callable):
    try:
        __events.__dict__[event] += callback
    except KeyError:
        print(f"[Error] Event '{event}' does not exist")