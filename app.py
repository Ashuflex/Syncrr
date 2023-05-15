import os
import shutil

movies_src_folder_relpath = os.path.normpath(os.environ.get('MOVIES_SRC_FOLDER_RELPATH'))
movies_dst_folder_relpath = os.path.normpath(os.environ.get('MOVIES_DST_FOLDER_RELPATH'))

movies_src_folder = os.path.join("/data", movies_src_folder_relpath)
movies_dst_folder = os.path.join("/data", movies_dst_folder_relpath)

def copy_srt_files():
    for root, dirs, files in os.walk(movies_src_folder):
        for file in files:

            if not file.endswith('.srt'):
                continue

            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, movies_src_folder)
            dst_file_path = os.path.join(movies_dst_folder, relative_path)
            
            if not os.path.isdir(os.path.dirname(dst_file_path)):
                continue

            if os.path.isfile(dst_file_path):
                src_modification_time = os.path.getmtime(src_file_path)
                dst_modification_time = os.path.getmtime(dst_file_path)
                
                if src_modification_time > dst_modification_time:
                    shutil.copy2(src_file_path, dst_file_path)
            else:
                shutil.copy2(src_file_path, dst_file_path)

def delete_deprecated_srt():
    for root, dirs, files in os.walk(os.path.join("/data", movies_dst_folder_relpath)):
        for file in files:

            if not file.endswith('.srt'):
                continue

            dst_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(dst_file_path, movies_dst_folder)
            src_file_path = os.path.join(movies_src_folder, relative_path)

            if not os.path.isfile(src_file_path):
                os.remove(dst_file_path)
                
copy_srt_files()
delete_deprecated_srt()
