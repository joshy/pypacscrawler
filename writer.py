import os

OUTPUT_DIR = 'data'


def get_file_name(month: str, day: str, mod: str):
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if month:
        return file_name + month + '.csv'
    else:
        return file_name + day + '-' + mod + '.csv'


def write_file(data_frame, file_name):
    data_frame.to_csv(file_name, header=True, index=False, sep=';')


def debug_file(debug, cmds):
    with open(debug, 'w') as command_file:
        for cmd in cmds:
            command_file.write(' '.join(cmd))
            command_file.write('\n')
