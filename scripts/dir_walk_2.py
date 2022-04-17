import re
import multiprocessing
import os
import timeit
import typing
from datetime import datetime
from typing import Tuple, Any

search_path = ''


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    date_format = d.strftime('%d %b %Y')
    return date_format


def write_in_file(FileName, file_path, cwd):
    global search_path

    last_mod_time = os.stat(file_path + FileName).st_mtime  # returns timestamp
    m_date = convert_date(last_mod_time)  # last modification date
    file_size = os.stat(file_path + FileName).st_size / 1000  # return size in bytes, 1000 bytes = 1 Kb
    with open('info_file.csv', 'a', encoding='UTF-8') as file_01:
        if os.stat(cwd + 'info_file.csv').st_size == 0:
            file_01.write(
                'src_path' + ',' + 'dst_File Name' + ',' + 'dst_Mod Date' + ',' + 'File Size(in Kb)' + ',' + 'File Path' + '\n')
        file_01.write(str(search_path) + ',' + str(FileName) + ',' + str(m_date) + ',' + str(file_size) + ',' + str(
            file_path) + '\n')


def search_in_list(dir_path: str, name: str, file_list: list) -> Any:
    disp_messages = list()
    locations_list = list()
    regex_pattern = re.compile(name, re.IGNORECASE)
    for fileName in file_list:
        if regex_pattern.search(fileName):
            file_path = os.path.realpath(os.path.join(dir_path, fileName))
            disp_messages.append(f"Found {fileName} in {dir_path}")
            locations_list.append(file_path)
    return disp_messages, locations_list


def driver(params: typing.Iterator, manager_dict):
    search_index = 0
    manager_dict['locs'] = []
    manager_dict['messages'] = []
    for search_index, param in enumerate(params):
        param: Tuple[str, str, list, set]
        message_list, locations_list = search_in_list(*param)
        if message_list:
            manager_dict['messages'] = manager_dict['messages'] + message_list
            manager_dict['locs'] = manager_dict['locs'] + locations_list

    manager_dict['search_count'] = search_index


def main(s_filename: str, searchPath: str):
    searchPath = os.path.realpath(searchPath)

    for DIR_PATH, directory_name, files in os.walk(searchPath):
        yield DIR_PATH, s_filename, files


def start_process(file_name, destination_path):
    start_time = timeit.default_timer()
    print("Fetching files...\n")
    parameters_gen = main(file_name, destination_path)
    print("starting Search...\n")

    manager_dict = multiprocessing.Manager().dict()
    p = multiprocessing.Process(target=driver, args=(parameters_gen, manager_dict))
    p.start()
    p.join()

    # p.close()
    end_time = timeit.default_timer()
    if 'locs' not in dict(manager_dict):
        manager_dict['locs'] = []
    all_found = dict(manager_dict)['locs']
    print(f"{len(all_found)} file{'s' if len(all_found) else ''} for current search tag: {file_name}")

    print(f"Time taken: {(end_time - start_time):.02f} seconds")
    return dict(manager_dict)

# if __name__ == '__main__':
#     start_process()
