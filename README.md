Pasty
=====
Pasty is a modern irc pastebot in material design.

It has the following features:
  - Text can be treaded as
    - markdown
    - code block
    - plain text
  - autosave
  - overview of all posts (chronological)
    - posts can be deleted
  - Automatically post to an IRC server
  - beautiful material design
  - mobile compatible
  - command line client
  - posts are plain text files
    - which reside in a chronological folder structure
  - Save submitters username when using apache2's auth (or setting the `REMOTE_USER` environment variable)
  - File upload (currently web only)

Requirements
------------
### CMD client
```sh
$ pip install requests
```

### Server
```sh
$ pip install flask irc
```

Compatibility
-------------
python2 and python3

Pasty can be used by any modern web browser. The command line client is compatible with Linux, Mac OS as well as with windows. Although the pasty server is designed to run only on Linux or Mac OS. (I may add windows support later)

Deployment
----------
### CMD client
Create a `.pasty.conf` file in your home directory and specify the pasty server as well as the default channel to which should be posted (without the `#`):
```sh
server: https://your.pasty.server.example.com
channel: example-channel
```

Use `pasty --help` for more information about the cmd tool.

### Server
Configure the server:
```sh
# FILE: pasty_server.conf
---
pasty:
  url: <service-url>

irc:
  server: <irc-hostname>
  port: 6667
  username: <username-of-pasty>
  channels:
    - <channel1>
    - <channel2>
```
NOTE: you mustn't start channel names with `#`

To run the server you can simply run `python3 web.py` but for a production environment I recommend you to use a web server which serves pasty as `wsgi`: (eg. apache)
```xml
DocumentRoot <pasty-root-dir>

WSGIDaemonProcess pasty user=www-data
WSGIScriptAlias / <pasty-root-dir>/web.wsgi

<Directory <pasty-root-dir>
        WSGIProcessGroup pasty
        WSGIApplicationGroup %{GLOBAL}
        require all granted
</Directory>
```

TODO
----
  - write tests
  - delete uploaded files individually
  - file upload over cmd

LICENSE
--------
> Pasty is a pastebot Copyright (C) 2016 Anastassios Martakos
>
> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by > the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

> You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
