# ~~ made by sed_cat ~~

# This ensures that the user is logging in
# and creates a database relation to store and crosscheck login information

from passencrypt import pass_encryption
import sqlite3
import logging


def user_verify(usr_pass):
    conn = sqlite3.connect('filespider.sqlite')  # will create new database if not found in local dir
    cur = conn.cursor()

    # setting up a logger
    logging.basicConfig(filename='dump.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger()  # getting an object called logger

    # sql command to create a table to store encrypted password
    cur.execute('''CREATE TABLE IF NOT EXISTS pass
        (id INTEGER PRIMARY KEY, password TEXT UNIQUE)''')

    # check to see if user has already set up the database
    cur.execute('SELECT password FROM pass LIMIT 1')
    enc_pass = cur.fetchone()
    if enc_pass is None:
        print('\n\n\nSetting up new database.....')
        new_pass = usr_pass
        print('New password has been set!')
        # sql to insert new password into database
        cur.execute('''INSERT INTO pass (password)
            VALUES (?)''', (pass_encryption(new_pass), ))
        conn.commit()  # saving changes
        logger.info('New user set')
        cur.close()
        return True

    # password checking if password already had been set
    # user_pass = pass_encryption(input('Enter your password: '))
    user_pass = pass_encryption(usr_pass)
    enc_pass = enc_pass[0]
    if user_pass == enc_pass:
        print('~~~ Login Successful!!! ~~~')
        logger.info('Successful login')
        cur.close()
        return True
    print('~~~ !!! Unsuccessful login. Wrong password !!! ~~~')
    logger.info('Unsuccessful login attempt\n')
    cur.close()
    return False
