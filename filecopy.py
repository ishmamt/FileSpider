# ~~ made by sed_cat ~~

# this script has the actual cop functions

# imports
import os
import shutil
import logging
import sqlite3


def db_check(target, destination):
    # sql for connecting and manipulating the database
    conn = sqlite3.connect('filespider.sqlite')  # will create new database if not found in local dir
    cur = conn.cursor()

    # sql query to find if the given file exists in database
    cur.execute('''SELECT file_id FROM copied
        WHERE targ_dir = ? AND dest_dir = ?''', (target, destination))
    file_id = cur.fetchone()
    if file_id is None:
        cur.close()
        return False
    cur.close()
    return True


def dir_check(destination):
    # sql for connecting and manipulating the database
    conn = sqlite3.connect('filespider.sqlite')  # will create new database if not found in local dir
    cur = conn.cursor()
    # sql query to find if the given file directory exists in database
    cur.execute('''SELECT file_id FROM copied
        WHERE dest_dir = ?''', (destination, ))
    file_id = cur.fetchone()
    if file_id is None:
        cur.close()
        return False
    cur.close()
    return True


def createdir(target, destination):
    # this fucntion will copy the exact file structure of the target dir to the destination dir
    # we will perform an os.walk to go through all the files in dir

    # setting up a logger
    logging.basicConfig(filename='dump.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger()  # getting an object called logger

    # sql for connecting and manipulating the database
    conn = sqlite3.connect('filespider.sqlite')  # will create new database if not found in local dir
    cur = conn.cursor()
    # sql command for creating a table to store all the files that have been copied
    cur.execute('''CREATE TABLE IF NOT EXISTS copied
        (file_id INTEGER PRIMARY KEY, targ_dir TEXT, dest_dir TEXT)''')

    # checking if directories exists
    if not os.path.isdir(target) or not os.path.isdir(destination):
        print(f'~~~~ !!!! The target directory: {target} or the destination directory: {destination} does not exist !!!! ~~~~')
        logger.warning('Target dir or destination dir does not exist\n')
        exit()

    # the os.walk() goes through all files in dir, even in folders
    for root, dir, folders in os.walk(target):
        dest_dir = os.path.join(destination, root[len(target) + 1:])  # this creates the proper destinaton dir
        # len(target) + 1 is to make sure we don't end with a /

        # check if it had already been copied
        if dir_check(dest_dir):
            # file alrady exists at the destination location
            logger.info(f'The directory:  ({dest_dir})  has already been copied')
            continue

        # creating new directories
        if not os.path.isdir(dest_dir):
            # if the dest_dir doesn't exist it will create the folders
            try:
                os.mkdir(dest_dir)  # os.mkdir() creates the target dir structure in the destination dir
                logger.info(f'The path:  ({dest_dir})  has been created')
            except:
                print(f'~~~~ !!! Could not create file destination directory: {dest_dir} !!! ~~~~')
                logger.warning(f'Error creating the path:  ({dest_dir})\n')
                exit()
        else:
            # dest_dir already exists
            logger.info(f'The path:  ({dest_dir})  already exists')


def copyfile(target, destination):
    # this function will copy the files of the target dir
    # we will perform os.walk to go through all the files in dir

    # setting up a logger
    logging.basicConfig(filename='dump.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger()  # getting an object called logger

    # sql for connecting and manipulating the database
    conn = sqlite3.connect('filespider.sqlite')  # will create new database if not found in local dir
    cur = conn.cursor()

    # checking if directories exists
    if not os.path.isdir(target) or not os.path.isdir(destination):
        print(f'~~~~ !!!! The target directory: {target} or the destination directory: {destination} does not exist !!!! ~~~~')
        logger.warning('Target dir or destination dir does not exist\n')
        exit()

    count = 0  # for counting successful copies
    print('Copying.....')
    for root, dir, folders in os.walk(target):
        for file in folders:
            target_dir = os.path.join(root, file)
            dest_dir = os.path.join(destination, root[len(target) + 1:])

            # checking database if the file has already been copied
            if db_check(target_dir, dest_dir):
                # file alrady exists at the destination location
                logger.info(f'The file:  ({target_dir})  has already been copied')
                continue
            try:
                # copying the files
                shutil.copy2(target_dir, dest_dir)
                count += 1

                # sql command for updating the database
                cur.execute('''INSERT OR IGNORE INTO copied
                    (targ_dir, dest_dir) VALUES (?, ?)''', (target_dir, dest_dir))
                conn.commit()

                logger.info(f'The file:  ({target_dir})  has been copied')
            except:
                print(f'~~~~ !!! Failed to copy: {target_dir} !!! ~~~~')
                logger.warning(f'Failed to copy the file:  ({target_dir})')

    print(f'~~~ Successfully copied {count} files ~~~')
    logger.info(f'Successfully copied {count} files\n')
    cur.close()
    return count
