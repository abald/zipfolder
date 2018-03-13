# -*- coding: utf-8 -*-
import os
import zipfile
import datetime
import time
import logging

logging.basicConfig(filename="sample.log", level=logging.INFO)
logging.info("Старт программы архивации.")

WORK_PATH = 'W:\\Тест\\' #Директория которую архивируем
ZIP_PATH =  'W:\\arc\\' #Директория куда архивируем

log_time = time.ctime(time.time())
date = datetime.datetime.today().strftime("%d-%m-%Y")
ZIP_FILE_PATH = ZIP_PATH + date + '.zip'
logging.info("%s Рабочая директория %s: " % (log_time, WORK_PATH))
logging.info("%s Директория архивов %s: " % (log_time, ZIP_PATH))

#Функция сжатия файлов в директории
def zipfile_def(WORK_PATH, ZIP_FILE_PATH):
    fantasy_zip = zipfile.ZipFile(ZIP_FILE_PATH, 'w')
    for folder, subfolders, files in os.walk(WORK_PATH):
        for file in files:
            fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), WORK_PATH), compress_type = zipfile.ZIP_DEFLATED)
    fantasy_zip.close()

#Функция поиска старого файла
def find_old_file(ZIP_PATH):
    file_list = os.listdir(ZIP_PATH)
    file_list=[os.path.join(ZIP_PATH, file) for file in file_list]
    file_list = [file for file in file_list if os.path.isfile(file)]
    old_file = min(file_list, key=os.path.getctime)
    return(old_file)

#Функция поиска нового файла
def find_new_file(ZIP_PATH):
    file_list = os.listdir(ZIP_PATH)
    file_list=[os.path.join(ZIP_PATH, file) for file in file_list]
    file_list = [file for file in file_list if os.path.isfile(file)]
    new_file = max(file_list, key=os.path.getctime)
    return(new_file)



# Проверяем есть ли файл:
# если нет то создаем новый архив
# если файл есть, дописываем ему .old
file_list = os.listdir(ZIP_PATH)
if file_list:
    logging.info("%s Список файлов %s" % (log_time, file_list))
    old_file = find_old_file(ZIP_PATH)
    new_file = find_new_file(ZIP_PATH)
    if old_file == new_file:
        os.rename(new_file,new_file+'.old')
        zipfile_def(WORK_PATH, ZIP_FILE_PATH)
        logging.info("%s Добавили старому файлу %s .old, запустили сжатие" % (log_time, new_file))
    else:
        os.remove(old_file)
        os.rename(new_file,new_file+'.old')
        zipfile_def(WORK_PATH, ZIP_FILE_PATH)
        logging.info("%s Удалили файл %s , переименовали предыдущий архив в  %s.old, запустили сжатие" % (log_time, old_file, new_file))
else:
    zipfile_def(WORK_PATH, ZIP_FILE_PATH)
    logging.info("%s Старых файлов нет, запустили сжатие" % (log_time))

#Проверяем создался ли файл, и сравниваем его с предыдущим,
#Если новый файл >= старого то Архивирование прошло удачно
#Если новый файл < старого то Ошибка
old_file = find_old_file(ZIP_PATH)
new_file = find_new_file(ZIP_PATH)
size_new_file = (str(os.path.getsize(new_file)//1024) + "Kb")
size_old_file = (str(os.path.getsize(old_file)//1024) + "Kb")
logging.info("%s Старый архив %s размером %s" % (log_time, old_file, size_old_file))
logging.info("%s Новый архив %s размером %s" % (log_time, new_file, size_new_file))
if size_new_file >= size_old_file:
    logging.info("%s Архивация прошла успешно" % (log_time))
else:
    logging.info("%s Архивация завершилась с ошибкой"% (log_time))
