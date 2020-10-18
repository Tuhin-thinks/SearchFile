import multiprocessing
import os
import timeit
from datetime import datetime
from typing import Tuple, Any

search_path = ''
manager_dict = {}


# q = multiprocessing.Queue()


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
    global q
    found_match =list()
    count = 0
    for fileName in file_list:
        if name.lower() in fileName.lower():
            file_directory = os.path.realpath(os.path.join(dir_path, fileName))

            output_string = f'{fileName} found at {file_directory}'
            found_match.append(output_string)

            count += 1

    return found_match


def driver(params, manager_dict):
    search_index = 0
    for search_index, param in enumerate(params):
        param: Tuple[str, str, list, set]
        res = search_in_list(*param)
        if res:
            if 'locs' in manager_dict:
                manager_dict['locs'].extend(list(res))
            else:
                manager_dict['locs'] = list(res)
    manager_dict['search_count'] = search_index
    # return manager_dict


def main(s_filename: str, searchPath: str):
    searchPath = os.path.realpath(searchPath)

    parameters = []
    for DIR_PATH, directory_name, files in os.walk(searchPath):
        parameters.append((DIR_PATH, s_filename, files))

    return parameters


def start_process(file_name, destination_path):
    # file_name = input("search for:")  # 'dil'
    # destination_path = 'C:\\Users\\tuhin Mitra\\Desktop\\All Python Resources'  # 'C:\\Users\\tuhin Mitra\\Music\\'

    start_time = timeit.default_timer()
    print("Fetching files...\n")
    parameters = main(file_name, destination_path)
    print("starting processing...\n")
    global manager_dict
    manager_dict = multiprocessing.Manager().dict()
    p = multiprocessing.Process(target=driver, args=(parameters, manager_dict))
    p.start()
    p.join()
    end_time = timeit.default_timer()

    all_found = manager_dict['locs']
    print(f"Found {len(all_found)} file{'s' if len(all_found) else ''} for current search tag: {file_name}")

    print(f"Time taken: {(end_time - start_time):.02f} seconds")
    return dict(manager_dict)

# if __name__ == '__main__':
#     start_process()
