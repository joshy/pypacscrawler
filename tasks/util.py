

def dict_to_str(parameter_dict):
    return ''.join(['{}_{}'.format(k,v) for k,v in parameter_dict.items()])