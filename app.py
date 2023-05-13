import os
from dotenv import load_dotenv
import shutil

load_dotenv('C:/Users/decau/Documents/Informatique/ashuflex/.env')

movie_src = os.path.normpath(os.environ.get('movie_src'))
movie_dst = os.path.normpath(os.environ.get('movie_dst'))

def copy_srt_files(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:

            if not file.endswith('.srt'):
                continue

            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_file_path, source_dir)
            destination_file_path = os.path.join(destination_dir, relative_path)
            
            if not os.path.isdir(os.path.dirname(destination_file_path)):
                continue
            
            if os.path.isfile(destination_file_path):
                source_modification_time = os.path.getmtime(source_file_path)
                destination_modification_time = os.path.getmtime(destination_file_path)
                
                if source_modification_time > destination_modification_time:
                    shutil.copy2(source_file_path, destination_file_path)
            else:
                shutil.copy2(source_file_path, destination_file_path)

copy_srt_files(movie_src, movie_dst)
