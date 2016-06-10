# ignis

**_ignis is created by Vi Grey (https://vigrey.com) <vi@vigrey.com> and is licensed under the BSD 2-Clause License.  Read LICENSE for more license text._**

#### Platforms:
- BSD
- GNU/Linux
- OS X

#### Dependencies:
- Python >= 3.0

#### Install:
    $ sudo ./INSTALL.sh

#### UNINSTALL:
    $ sudo ./UNINSTALL.sh

#### Usage:
    $ ignis -h
    Usage: ignis [ OPTIONS ]... [ -o <path="./__website__"> ] [ <input_path="./"> ]

    Options:
      -h, --help                   Print Help (this message) and exit
          --include-extensions     Include .html and .htm extensions in @FILEPATH
          --include-htaccess       Include .htaccess to match ignis server
      -L, --LAN                    Open test server up to local network
      -M, --mock                   Run a mock website build
      -o, --output  <path>         Path for finished website (path=./__website__)
      -P, --port  <port>           Port for finished website (port=9999)
      -T, --test                   Run test web server after build
      -V, --verbose                Print verbose messages while building
      -v, --version                Print version information and exit

    Examples:
      ignis -o path/for/website path/to/files
      ignis --verbose -o example-site
      ignis -V -T -L -o example-site
      ignis -VTL
      ignis -VT --include-extensions
      ignis -TL --include-htaccess --include-extensions
      ignis --port 9090 -VTL
      ignis -MV

#### For Loops:

Handle *`content`* for every case in which a page's header has a *`variable`* that is *`value`* and then sort the cases by *`sort_variable`*.  If you place a negative symbol (-) in front of {sort_variable}, it will sort in reverse.  *`sort_variable`* will be sorted by its placement in the Unicode standard.

    [!- for {variable} is "value" by {sort_variable} -!]
      content
    [!- endfor -!]

Examples:

    <!-- Sort products by price (Low to High) -->
    [!- for {type} is "product" by {price} -!]
      [!- forprint {title} -!]
      <br><br>
      [!- forprint {price} -!]
    [!- endfor -!]

    <!-- Sort products by price (High to Low) -->
    [!- for {type} is "product" by -{price} -!]
      [!- forprint {title} -!]
      <br><br>
      [!- forprint {price} -!]
    [!- endfor -!]

#### If Statements:

Only handle *`content`* if the value of *`variable`* is *`value`* for the header the page this 'if' statement is on.  The word **not** can be used instead of **is** to see check if the value of *`variable`* is not *`value`*.  This differs from 'forif' commands because the value of *`variable`* is only taken from the header of the file currently being handled, not from any other file.

    [!- if {variable} is "value" -!]
      content
    [!- endif -!]

Examples:

    <!-- Check if the value of type is product -->
    [!- if {type} is "product" -!]
      This is a product and it costs:
      [!- print {price} -!]
    [!- endif -!]

    <!-- Check if the value of type is not product -->
    [!- if {type} not "product" -!]
      This is not a product
    [!- endif -!]

#### Forif Statements:

Only handle *`content`* if the value of *`variable`* is *`value`* from the header of the current iteration of a 'for' loop.  The word **not** can be used instead of **is** to see check if the value of *`variable`* is not *`value`*.  This differs from 'if' statements because the value of *`variable`* is not taken from the header of the file currently being handled.

    [!- forif {variable} is "value -!]
      content
    [!- endforif -!]

Examples:

    [!- for {date} is "2015-12-31" by {title} -!]
      <!-- Check if the value of type in the current iteration is product -->
      [!- forif {type} is "product" -!]
        This is a product and it costs:
        [!- print {price} -!]
      [!- endforif -!]

      <!-- Check if the value of type in the current iteration is not product -->
      [!- forif {type} not "product" -!]
        This is not a product
      [!- endforif -!]
    [!- endfor -!]

#### Print commands:

Print the value of *`variable`* for the header of the file this 'print' command is on.  This differs from 'forprint' commands because the value of *`variable`* is only taken from the header of the file currently being handled, not from any other file.

    [!- print {variable} -!]

Example:

    <!-- Will print the value of title from the current page's header -->
    [!- print {title} -!]

#### Forprint commands:

Print the value of the *`variable`* from the header of the current 'for' loop iteration.  This differs from 'print' commands because the value of *`variable`* is not taken from the header of the file currently being handled.

    [!- forprint {variable} -!]

Example:

    [!- for {type} is "product" by -{price} -!]
      <!-- Will print the value of title from the current iteration's header -->
      [!- forprint {title} -!]
    [!- endfor -!]

#### File Headers:

The file header is included on the top of pages that are not template files that you wish to manipulate with the **ignis** engine.  Variables will be created with anything to the right of the first equal sign being the value of that variable.  Variables can include letters, numbers, underscores and hyphens.  The file path of the file will be stored in the variable *`@FILEPATH`* and anything after the file header will be stored in the variable *`@CONTENT`*.  *`%TEMPLATE`* is the location of the template file for the page based on the root of the filesystem being the input path of the website.

Any file (excluding template files) you wish to use *`[!- -!]`* commands, statements, or loops to build or modify must have a file header, even if you leave it empty.  `!-header` must be the first line of the file and `-!` must start on a new line.  *`%TEMPLATE`* is not required, but is highly suggested to use.

    !-header
    %TEMPLATE=/path/to/template/file
    variable=value
    -!

Example:

    !-header
    %TEMPLATE=/templates/template.html
    type=product
    -!

In this example, the template file will be located at `templates/template.html` inside of the input path location specified when you run `ignis` in the command line.

#### Template Header:

The template header states that the file is a template and should not be written into the output path for the website, but instead should just be applied to pages that call for that template file specifically.

`!-template-!` must be the first line of any template file.

    !-template-!

#### Example Site:

This example site should be included in `/etc/ignis/example/` after installing **ignis**.  This example site is just to show how files can be formatted to work with the **ignis** engine.  To view the site at http://localhost:9999, you can use the command `$ ignis -T -o <output_path> -i /etc/ignis/example/` where *`<output_path>`* is the path were you want the website to be built.  This command will use the built-in web server in **ignis** to serve the website.
