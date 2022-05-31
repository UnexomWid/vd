def dict_append_list(dict, key, value):
    if key not in dict:
        dict[key] = value.strip()
    else:
        dict[key] += f', {value.strip()}'
