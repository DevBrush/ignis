#!/usr/bin/env python3

# Copyright (C) 2015, Vi Grey
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import sys
from os import listdir
from os.path import isfile, join

VERSION = '1.0.0.0'
AUTHOR = 'Vi Grey (http://pariahvi.com)'


def help_print():
    print("Usage: ignis [ OPTIONS ]... [ -t <file> ] [ -i <path=\"./\"> ] " +
          "[ -o <path> ]\n\n Required:\n" +
          "  -i, --input  <path>      Input path of website content\n" +
          "  -o, --output  <path>     Output path for finished static " +
          "website\n" +
          "  -t, --template <file>    Template HTML file\n\n" +
          " Options:\n"
          "  -h, --help               Print Help (this message) and exit\n" +
          "      --test               Run test web server on port 9999 " +
          "after build\n"
          "  -v, --verbose            Print verbose messages while " +
          "processing\n"
          "      --version            Print version information and exit\n\n" +
          " Examples:\n" +
          "  ignis -t template.html -i content/text -o example-site\n" +
          "  ignis -t template/template.html -o example-site\n" +
          "  ignis --verbose -t template/template.html -o example-site\n" +
          "  ignis -v --test -t template/template.html -o example-site")


def version_print():
    print("ignis " + VERSION)


def main():
    help_flag = False
    version_flag = False
    for arg in sys.argv[1:]:
        if len(arg) > 2 and arg.find("--") == 0:
            if arg[2:] == "help":
                help_flag = True
            elif arg[2:] == "version":
                version_flag = True
            elif arg[2:] != "":
                print("ignis: unrecognized option " + arg + "\nTry 'ignis " +
                      "--help' for more information.")
                sys.exit(1)
        elif len(arg) > 1 and arg[0] == "-" and arg.find("--") != 0:
            for x in arg[1:]:
                if x == "h":
                    help_flag = True
                else:
                    print("ignis: unrecognized option " + arg + "\nTry " +
                          "'ignis --help' for more information.")
                    sys.exit(1)
        elif "--".find(arg) != 0:
            print("ignis: invalid option -- '" + arg + "'\nTry 'ignis " +
                  "--help' for more information.")
            sys.exit(1)
    if help_flag or version_flag:
        if help_flag:
            help_print()
        else:
            version_print()

if __name__ == "__main__":
    main()
