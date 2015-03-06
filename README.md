# ignis

**_ignis is created by Dev Brush Technology ([http://devbrush.com](http://devbrush.com)) <[feedback@devbrush.com](mailto:feedback@devbrush.com)> and is licensed under the BSD 2-Clause License.  Read LICENSE for more license text._**

#### ignis is in heavy development.  No stable version is available yet.

#### Platforms:
- BSD
- GNU/Linux
- OS X

#### Dependencies
- Python >= 3.0

#### Install:
    $ sudo ./INSTALL.sh

#### UNINSTALL
    $ sudo ./UNINSTALL.sh

#### Usage
    $ ignis -h
    Usage: ignis [ OPTIONS ]... [ -o <path="./__website__"> ] [ <input_path="./"> ]

    Options:
      -h, --help               Print Help (this message) and exit
      -L, --LAN                Open test server up to local network
      -M, --mock               Run a mock website build
      -o, --output  <path>     Output path for finished website (path=./__website__)
      -P, --port  <port>       Port for finished website (port=9999)
      -T, --test               Run test web server after build
      -V, --verbose            Print verbose messages while building
      -v, --version            Print version information and exit

    Examples:
      ignis -o path/for/website path/to/files
      ignis --verbose -o example-site
      ignis -V -T -L -o example-site
      ignis -VTL
      ignis --port 9090 -VTL
      ignis -MV

#### For Loops
    [!- for {variable} is "value" by {sort_variable} -!]

    [!- endfor -!]

#### Print Statement
    [!- print {variable} -!]
