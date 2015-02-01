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

import glob
import os
import http.server
import re
import socketserver
import sys

VERSION = "1.0.0.0"
AUTHOR = "Vi Grey (http://pariahvi.com)"
HOST = "127.0.0.1"
PORT = 9999


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def get_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        if root[-1] == "/":
            root = root[: -1]
        if re.search("(/\.)", root) is None:
            for f in files:
                file_list.append(root + "/" + f)
    return file_list


# Starts a HTTP server at HOST:PORT with the root directory being path
def handle_http(path):
    global HOST
    os.chdir(path)
    server = socketserver.TCPServer((HOST, PORT), HTTPRequestHandler)
    message = ""
    if HOST == "0.0.0.0":
        message = " (Open to LAN)"
    print("Test server at http://localhost:" + str(PORT) + message +
          "\nPress Ctrl-C to stop server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("")


def help_print():
    print("Usage: ignis [ OPTIONS ]... [ -t <file> ] [ -i <path=\"./\"> ] " +
          "[ -o <path> ]\n\n Required:\n" +
          "  -i, --input  <path>      Input path of website content\n" +
          "  -o, --output  <path>     Output path for finished static " +
          "website\n" +
          "  -t, --template <file>    Template HTML file\n\n" +
          " Options:\n"
          "  -h, --help               Print Help (this message) and exit\n" +
          "  -L, --LAN                Open test server up to local network\n"
          "  -T, --test               Run test web server on port 9999 " +
          "after build\n"
          "  -V, --verbose            Print verbose messages while " +
          "building\n"
          "  -v, --version            Print version information and exit\n\n" +
          " Examples:\n" +
          "  ignis -t template.html -i content/text -o example-site\n" +
          "  ignis --verbose -t template/template.html -o example-site\n" +
          "  ignis -V -T -L -t template/template.html -o example-site\n" +
          "  ignis -VTL -t template/template.html -o example-site")


def version_print():
    print("ignis " + VERSION)


def main():
    global HOST
    help_flag = False
    version_flag = False
    template_flag = False
    output_flag = False
    http_flag = False
    lan_flag = False
    input_path = "."
    output_path = ""
    args = sys.argv[1:]
    x = 0
    while x < len(sys.argv[1:]):
        if len(args[x]) > 2 and args[x].find("--") == 0:
            if args[x][2:] == "help":
                help_flag = True
            elif args[x][2:] == "version":
                version_flag = True
            elif args[x][2:] == "test":
                http_flag = True
            elif args[x][2:] == "LAN":
                lan_flag = True
            elif args[x][2:] == "input":
                if len(args) > x + 1:
                    input_path = args[x + 1]
                    x += 1
                    break
                else:
                    print("ignis: no input path included\nTry 'ignis " +
                          "--help' for more information.")
                    sys.exit(2)
            elif args[x][2:] == "output":
                if len(args) > x + 1:
                    output_flag = True
                    output_path = args[x + 1]
                    x += 1
                    break
                else:
                    print("ignis: no output path included\nTry 'ignis " +
                          "--help' for more information.")
                    sys.exit(2)
            elif args[x][2:] != "":
                print("ignis: unrecognized option " + args[x] + "\nTry " +
                      "'ignis --help' for more information.")
                sys.exit(1)
        elif (len(args[x]) > 1 and args[x][0] == "-" and
              args[x].find("--") != 0):
            for y in args[x][1:]:
                if y == "h":
                    help_flag = True
                elif y == "v":
                    version_flag = True
                elif y == "T":
                    http_flag = True
                elif y == "L":
                    lan_flag = True
                elif len(y) == 1 and y == "i":
                    if len(args) > x + 1:
                        input_path = args[x + 1]
                        x += 1
                        break
                    else:
                        print("ignis: no input path included\nTry 'ignis " +
                              "--help' for more information.")
                        sys.exit(2)
                elif len(y) == 1 and y == "o":
                    if len(args) > x + 1:
                        output_flag = True
                        output_path = args[x + 1]
                        x += 1
                        break
                    else:
                        print("ignis: no path path included\nTry 'ignis " +
                              "--help' for more information.")
                        sys.exit(2)
                else:
                    print("ignis: unrecognized option " + args[x] + "\nTry " +
                          "'ignis --help' for more information.")
                    sys.exit(1)
        elif ("--".find(args[x]) == 0 and x != 0) or "--".find(args[x]) != 0:
            print("ignis: invalid option -- '" + args[x] + "'\nTry 'ignis " +
                  "--help' for more information.")
            sys.exit(1)
        x += 1
    if help_flag:
        help_print()
    elif version_flag:
        version_print()
    if output_flag:
        output_path = glob.glob(output_path)
        if len(output_path) == 1:
            output_path = output_path[0]
        else:
            print("ignis: too many output path posibilities")
    else:
        print("ignis: output path is required\nTry 'ignis " +
              "--help' for more information.")
        sys.exit(5)
    input_path = glob.glob(input_path)
    if len(input_path) == 1:
        input_path = input_path[0]
        print(get_files(input_path))
    else:
        print("ignis: too many input path posibilities")
        sys.exit(4)
    if http_flag:
        if lan_flag:
            HOST = "0.0.0.0"
        handle_http(output_path)
    else:
        if lan_flag:
            print("ignis: --test must be included to use LAN flag\n" +
                  "Try 'ignis --help' for more information.")

if __name__ == "__main__":
    main()
