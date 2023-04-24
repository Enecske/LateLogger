def find_tuple(list: list, tuple_index: int, value: any):
    for i in range(len(list)):
        if list[i][tuple_index] == value:
            return i
        
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)