Clear Files on FTP Server
====================

#### Overview

Connects a ftp server and cycles through the directories deleting files older than a certain date.  Everything is specified in the settings.ini file.

#### Compatibility

Python 3.4+

#### Getting Started

Just run it first and it will generate a stock settings file.  From there it will exit and you can set up the settings.ini file with your information.  Then just re-run it and it will do its thing.

```
[ftp]
server = ftp.server.com
user = some_user
password = default
directories = dir1 dir2 dir3
cutoff_days = 7
```

Enjoy!