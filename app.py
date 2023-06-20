import os
import shutil
import logging
import typing
from singleton import Singleton_Global_Variables

def get_source_folder(prefix: str = "SRC_FOLDER") -> str:
    """
    Function to find the source folder based on a prefix.

    Checks the environment prefix "{prefix}_0". By default, :envvar:`SRC_FOLDER_0`.

    :return: Returns the source folder
    """""""""
    if not (source_folder := os.environ.get(f"{prefix}_0")):
        raise ValueError(f"Cannot find environment variable {prefix}_0")
    return os.path.normpath(source_folder)



def find_all_dst_folders(prefix: str = "DST_FOLDER") -> typing.List[str]:
    """
    Function to find all destination folders based on a prefix.
    
    Checks the environment variable "{prefix}_0", "{prefix}_1", ..., "{prefix}_N",  
     by default :envvar:`DST_FOLDER_0` at least.
    
    :return: list of normalized path of destination foldersesds    :param prefix: Prefix to find the 
    """""""""
    counter: bool = 0
    run_search: bool = True
    list_result_dst_folders: typing.List[str] = list()
    while run_search:
        if var_bla := os.environ.get(f"{prefix}_{counter}"):
            counter += 1
            list_result_dst_folders.append(os.path.normpath(var_bla))
        else:
            run_search = False
    return list_result_dst_folders



def copy_srt_files() -> int:
    """
    Copies srt files.

    Uses movies_src_folder from outer scope.

    :return: Number of copied files
    """
    copy_cnt: int = 0
    singleton_global_variables = Singleton_Global_Variables()
    logging_level_detailed = singleton_global_variables.detailed_message()
    logging_level_count = singleton_global_variables.counter_messages()
    dry_run_state = singleton_global_variables.get_dry_run_state()
    logging.debug(f"The current state of dry_run_state in copy_srt_file is {dry_run_state}")
    for root, dirs, files in os.walk(movies_src_folder):
    # Should get all files then filter later
        for file_iter in files:
            if not file_iter.endswith('.srt'):
                continue

            src_file_path = os.path.join(root, file_iter)
            relative_path = os.path.relpath(src_file_path, movies_src_folder)
            for movies_dst_folder_iter in movies_dst_folder:
                dst_file_path_iter = os.path.join(movies_dst_folder_iter, relative_path)
                if not os.path.isdir(os.path.dirname(dst_file_path_iter)):
                    continue
                
                # Only for srt copy improve if for srt only
                if os.path.isfile(dst_file_path_iter):
                    src_modification_time = os.path.getmtime(src_file_path)
                    dst_modification_time = os.path.getmtime(dst_file_path_iter)

                    if src_modification_time > dst_modification_time:
                        logging.log(msg = f'copying {src_file_path} to {dst_file_path_iter}',
                         level=logging_level_detailed)
                        if not dry_run_state:
                            shutil.copy2(src_file_path, dst_file_path_iter)
                        copy_cnt += 1
                else: 
                    logging.log(msg=f'copying {src_file_path} to {dst_file_path_iter}',
                     level=logging_level_detailed)
                    if not dry_run_state:
                        shutil.copy2(src_file_path, dst_file_path_iter)
                    copy_cnt += 1
    logging.log(msg = f'Copied:{copy_cnt} files', level=logging_level_count)

def delete_deprecated_srt() -> int:
    """
    Delete srt folders.

    Uses the list of folders movies_dst_folder_relpath (outer scope).

    :return: Number of deleted folders
    """
    delete_dir_cnt: int = 0
    singleton_global_variables = Singleton_Global_Variables()
    dry_run_state = singleton_global_variables.get_dry_run_state()
    logging.debug(f"The current state of dry_run_state in delete_deprecated_srt is {dry_run_state}")
    logging_level_count = singleton_global_variables.counter_messages()
    for movies_dst_folder_relpath_iter in movies_dst_folder_relpath:
        for root, dirs, files in os.walk(os.path.join("/data", movies_dst_folder_relpath_iter)):
            # Cleanup Dirst
            for dir in dirs:

                dst_dir_path = os.path.join(root, dir)
                #relative_path = os.path.relpath(dst_dir_path, movies_dst_folder)
                relative_path = os.path.relpath(dst_dir_path, movies_dst_folder_relpath_iter)
                src_dir_path = os.path.join(movies_src_folder, relative_path)

                if not os.path.isdir(src_dir_path):
                    if not dry_run_state:
                        shutil.rmtree(dst_dir_path)
                    logging.debug(f'Deleting {dst_dir_path}')
                    delete_dir_cnt += 1
                    
        for root, dirs, files in os.walk(os.path.join("/data", movies_dst_folder_relpath_iter)):
            # Cleanup Files
            for file_iter in files:

                dst_file_path = os.path.join(root, file_iter)
                #relative_path = os.path.relpath(dst_dir_path, movies_dst_folder)
                relative_path = os.path.relpath(dst_dir_path, movies_dst_folder_relpath_iter)
                src_file_path = os.path.join(movies_src_folder, relative_path)

                if not os.path.isfile(src_file_path):
                    if not dry_run_state:
                        os.remove(dst_file_path)
                    logging.debug(f"Deleting {dst_file_path}")
    logging.log(msg = f'Deleted:{delete_dir_cnt} folders', level = logging_level_count)
                
try:
    # Add dry run parameters
    movies_src_folder_relpath: str = get_source_folder()
    # movies_dst_folder_relpath = os.path.normpath(os.environ.get('DST_FOLDER_0'))
    movies_dst_folder_relpath: typing.List[str] = find_all_dst_folders() 
    movies_src_folder: str = os.path.join("/data", get_source_folder())
    movies_dst_folder: typing.List[str] = \
        [os.path.join("/data", dst_folder_iter) for dst_folder_iter in movies_dst_folder_relpath]
    
    singleton_global_variables = Singleton_Global_Variables()

    
    if not os.environ.get('LOG_LEVEL'):
        value_logging = logging.ERROR
    else:
        dict_mapping_levels = logging.getLevelNamesMapping()
        try:
            value_logging = dict_mapping_levels[os.environ.get('LOG_LEVEL')]
        except KeyError: # Python < 3.11.
            dict_mapping_levels = {'DEBUG': logging.DEBUG, 
                        'INFO': logging.INFO,
                        'WARNING': logging.WARNING,
                        'ERROR': logging.ERROR
                        }
            try:
                value_logging = dict_mapping_levels[os.environ.get('LOG_LEVEL')]
            except KeyError:
                raise KeyError(f"Cannot interpret LOG_LEVEL environment variable {os.environ.get('LOG_LEVEL')}")
    singleton_global_variables.set_logging_level(value_logging)
    singleton_global_variables.set_dry_run_state()
    logging.basicConfig(level=value_logging)

    delete_deprecated_srt()
    copy_srt_files()

except Exception as e:
    logging.error(e, exc_info=True)