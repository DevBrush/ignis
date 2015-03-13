# ignis

**_ignis is created by Dev Brush Technology ([http://devbrush.com](http://devbrush.com)) <[feedback@devbrush.com](mailto:feedback@devbrush.com)> and is licensed under the BSD 2-Clause License.  Read LICENSE for more license text._**

##### ignis is in development.  No stable version is available yet.

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

Handle *content* for every case in which a page's header has a *variable* that is *value* and then sort the cases by *sort_variable*.  If you place a negative symbol (-) in front of {sort_variable}, it will sort in reverse.  *sort_variable* will be sorted by its placement in the Unicode standard.

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

Only handle *content* if the value of *variable* is *value* for the header the page this 'if' statement is on.  The word **not** can be used instead of **is** to see check if the value of *variable* is not *value*.

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

Only handle *content* if the value of *variable* is *value* from the header of the current iteration of a 'for' loop.  The word **not** can be used instead of **is** to see check if the value of *variable* is not *value*.

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

#### Print Statements:

Print the value of *variable* for the header of the page this 'print' command is on.

    [!- print {variable} -!]

Example:

	<!-- Will print the value of title from the current page's header -->
	[!- print {title} -!]

#### Forprint Statements:

Print the value of the *variable* from the header of the current 'for' loop iteration.

	[!- forprint {variable} -!]

Example:

	[!- for {type} is "product" by -{price} -!]
		<!-- Will print the value of title from the current iteration's header -->
    	[!- forprint {title} -!]
	[!- endfor -!]

#### File Headers:

The file header is included on the top of pages that are not template files that you wish to manipulate with the ignis engine.  Variables will be created with anything to the right of the first equal sign being the value of that variable.  Variables can include letters, numbers, underscores and hyphens.  The file path of the file will be stored in the variable @FILEPATH and anything after the file header will be stored in the variable @CONTENT.  %TEMPLATE is the location of the template file for the page.

	!-header
	%TEMPLATE=path/to/template/file
	variable=value
	-!

#### Template Header:

The !-template-! header states that the file is a template and should not be written into the output path for the website.  Templates are used 

	!-template-!