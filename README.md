Pasty
=====
Pasty is a beautiful looking next generation pastebot.

It sports following features:
  - Post can be treaded as
    - markdown
    - plain code
    - plain text
  - autosave
  - chronological posts
  - view all posts (sorted chronologically)
  - beautiful material design
  - mobile compatible
  - command line client
  - posts are plain text files
    - which reside in a chronological folder structure

Requirements
------------
### CMD client
```sh
$ pip install requests
```

### Server
```sh
$ pip install flask
```

Compatibility
-------------
Pasty can be used by any modern web browser. The command line interface is compatible with UNIX-like operating systems (Linux, Mac OS) as well as with windows. Although the pasty server is designed to run only in UNIX-like operating systems. (I may add windows support later)

Deployment
----------
### CMD client
Create a `.pasty.conf` file in your home directory and fill it with the URL of the pasty server:
```sh
https://your.pasty.server.example.com
```

Then just execute the `pasty` python file with following parameter:
```sh
$ pasty <title-of-post> <file-whose-content-gets-postet>
```

### Server
You basically don't need to configure anything. Pasty can run standalone by running `python3 web.py`.

For a production environment I recommend to use a web server which serves pasty as a wsgi: (eg. apache)
```xml
DocumentRoot <pasty-root-dir>

# important set the CWD to the pasty root dir with the home=<cwd> directive
WSGIDaemonProcess pasty user=www-data home=<pasty-root-dir>
WSGIScriptAlias / <pasty-root-dir>/web.wsgi

<Directory <pasty-root-dir>
        WSGIProcessGroup pasty
        WSGIApplicationGroup %{GLOBAL}
        require all granted
</Directory>
```

**NOTE**: Pasty *requires that the current working directory is set to the pasty root directory*. Which is the directory where `web.py` is located. So you will have to execute it from there if you are running standalone or you have to set it in the web server config.

TODO
----
  - write tests

LICENSE
--------
> Pasty is a pastebot Copyright (C) 2016 Anastassios Martakos
>
> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by > the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

> You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
