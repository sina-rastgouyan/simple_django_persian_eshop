def group_list(custom_list, size=4):
    grouped_list = []
    group_size = size
    my_range = range(0, len(custom_list), group_size)
    for i in my_range:
        grouped_list.append(custom_list[i:i + group_size])

    return grouped_list
