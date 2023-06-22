import os
import shutil
import logging


# Shoud check rights before running

def copy_srt_files():
    copy_cnt = 0
    for root, dirs, files in os.walk(movies_src_folder):
    # Should get all files then filter later
        for file in files:
            if not file.endswith('.srt'):
                continue

            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, movies_src_folder)
            dst_file_path = os.path.join(movies_dst_folder, relative_path)

            if not os.path.isdir(os.path.dirname(dst_file_path)):
                continue

            # Only for srt copy improve if for srt only
            if os.path.isfile(dst_file_path):
                src_modification_time = os.path.getmtime(src_file_path)
                dst_modification_time = os.path.getmtime(dst_file_path)

                if src_modification_time > dst_modification_time:
                    logging.info(f'copying {src_file_path} to {dst_file_path}')
                    shutil.copy2(src_file_path, dst_file_path)
                    copy_cnt += 1
            else: 
                logging.info(f'copying {src_file_path} to {dst_file_path}')
                shutil.copy2(src_file_path, dst_file_path)
                copy_cnt += 1

    return copy_cnt

def delete_deprecated_srt():
    delete_dir_cnt = 0
    for root, dirs, files in os.walk(os.path.join("/data", movies_dst_folder_relpath)):
        # Cleanup Dirst
        for dir in dirs:

            dst_dir_path = os.path.join(root, dir)
            relative_path = os.path.relpath(dst_dir_path, movies_dst_folder)
            src_dir_path = os.path.join(movies_src_folder, relative_path)

            if not os.path.isdir(src_dir_path):
                shutil.rmtree(dst_dir_path)
                delete_dir_cnt += 1
                
    for root, dirs, files in os.walk(os.path.join("/data", movies_dst_folder_relpath)):

        # Cleanup Files
        for file in files:

            dst_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(dst_file_path, movies_dst_folder)
            src_file_path = os.path.join(movies_src_folder, relative_path)

            if not os.path.isfile(src_file_path):
                os.remove(dst_file_path)

    return delete_dir_cnt
                
try:
    # Add dry run parameters
    movies_src_folder_relpath = os.path.normpath(os.environ.get('SRC_FOLDER_0'))
    movies_dst_folder_relpath = os.path.normpath(os.environ.get('DST_FOLDER_0'))

    movies_src_folder = os.path.join("/data", movies_src_folder_relpath)
    movies_dst_folder = os.path.join("/data", movies_dst_folder_relpath)

    if not os.environ.get('LOG_LEVEL'):
        logging.basicConfig(level='ERROR')
    else:
        logging.basicConfig(level=os.environ.get('LOG_LEVEL'))

    delete_dir_cnt = delete_deprecated_srt()
    logging.info(f'Deleted:{delete_dir_cnt} folders')
    copy_cnt = copy_srt_files()
    logging.info(f'Copied:{copy_cnt} files')

except Exception as e:
    logging.error(e, exc_info=True)