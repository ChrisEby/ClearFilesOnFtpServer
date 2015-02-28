__author__ = 'Chris Eby'

from ftplib import FTP, error_perm
from datetime import datetime, timedelta
from configparser import ConfigParser
from os import path


def main():
    config_file = 'settings.ini'

    # Check if the ini file exists, create if not
    if not path.isfile(config_file):
        create_ini(config_file)
        print(config_file, ' not found, a default one has been created.  Set it up and then re-run.')
        quit()

    # Read in all the settings
    config = ConfigParser()
    config.read(config_file)
    server = config.get('ftp', 'server')
    user = config.get('ftp', 'user')
    password = config.get('ftp', 'password')
    directories = config.get('ftp', 'directories').split()
    cutoff_days = config.getint('ftp', 'cutoff_days')

    print('Connecting to FTP')
    with FTP(server) as ftp:
        ftp.login(user, password)

        print('Cycle through directories')
        for directory in directories:
            print('ftp-cwd - ', directory)
            ftp.cwd(directory)

            cutoff = datetime.now() - timedelta(days=cutoff_days)
            print('Filter files by date')
            files = filter_files(ftp, cutoff)
            print('Delete filtered files')
            delete_files(ftp, files)

            print('ftp-cwd - ..')
            ftp.cwd('..')

        print('ftp-quit')
        ftp.quit()  # overkill I suppose


def filter_files(ftp, cutoff):
    """
    Fetches then filters the files in the directory that are older than the cut off date.
    :rtype : list
    """
    files = []
    filtered_files = []

    try:
        files = ftp.nlst()
    except error_perm as resp:
        if str(resp) == "550 No files found":
            print('No files found in this directory')
        else:
            raise

    print('len(files) ', len(files))
    print('files ', files)

    for file in files:
        mod_time = get_modtime(ftp, file)
        if mod_time < cutoff:
            filtered_files.append(file)

    print('len(filtered_files) ', len(filtered_files))
    print('filtered_files ', filtered_files)

    return filtered_files


def delete_files(ftp, files):
    """
    Deletes the files specified from the current directory.
    """

    for file in files:
        print('file ', file)
        ftp.delete(file)


def get_modtime(ftp, filename):
    """
    Get the modtime of a file.
    :rtype : datetime
    """
    resp = ftp.sendcmd('MDTM ' + filename)

    if resp[:3] == '213':
        s = resp[3:].strip()
        mod_time = datetime.strptime(s,'%Y%m%d%H%M%S')
        return mod_time
    return datetime.min


def create_ini(config_file):
    config = ConfigParser()
    config['ftp'] = {
        'server': 'ftp.server.com',
        'user': 'some_user',
        'password': 'default',
        'directories': 'dir1 dir2 dir3',
        'cutoff_days': '7'
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    main()