# ignis

**_ignis is created by Vi Grey ([http://pariahvi.com](http://pariahvi.com)) <[development@pariahvi.com](mailto:development@pariahvi.com)> and is licensed under the BSD 2-Clause License.  Read LICENSE for more license text._**

#### ignis is in heavy development.  No stable version is available yet.

#### Platforms:
- BSD
- GNU/Linux
- OS X

#### Dependencies
- Python >= 3.0

#### Usage
    $ ignis -h
    Usage: ignis [ OPTIONS ]... [ -o <path="./__website__"> ] [ <input_path="./"> ]

    Options:
      -h, --help               Print Help (this message) and exit
      -L, --LAN                Open test server up to local network
      -o, --output  <path>     Output path for finished static website
      -T, --test               Run test web server on port 9999 after build
      -V, --verbose            Print verbose messages while building
      -v, --version            Print version information and exit

    Examples:
      ignis -o path/for/website path/to/files
      ignis --verbose -o example-site
      ignis -V -T -L -o example-site
      ignis -VTL
