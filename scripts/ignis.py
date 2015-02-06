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
    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if os.path.isfile(path + "index.html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open(path + "index.html", "rb").read())
            elif os.path.isfile(path + "index.htm"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open(path + "index.htm", "rb").read())
            else:
                self.send_response(404, "File not found")
                return None
        elif not re.search("\..*$", self.path):
            if os.path.isfile(path + ".html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open(path + ".html", "rb").read())
            elif os.path.isfile(path + ".htm"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(open(path + ".html", "rb").read())
            else:
                self.send_response(404, "File not found")
                return None
        elif os.path.isfile(path):
            self.send_response(200)
            self.send_header("Content-type", self.guess_type(self.path))
            self.end_headers()
            self.wfile.write(open(path, "rb").read())
        else:
            self.send_response(404, "File not found")
            return None
        return

    def log_message(self, format, *args):
        pass


class HandleTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def get_files(input_path, output_path):
    file_list = []
    for root, dirs, files in os.walk(input_path):
        if root[-1] == "/":
            root = root[: -1]
        if re.search("(/\.)", root) is None and output_path not in root:
            for f in files:
                file_list.append(root + "/" + f)
    return file_list


def handle_files(input_files, input_path, output_path, verbose):
    header_list = []
    for f in input_files:
        input_file = open(f, "rb")
        if verbose:
            print("Reading " + f)
        input_content = input_file.read()
        input_content = input_content.replace(b"\r\n", b"\n")
        if verbose:
            print("Checking " + f + " for header values")
        header_vars, is_header = get_header(f, input_content)
        header_list.append((header_vars, is_header))
    for t in header_list:
        file_content = open(t[0][b"@FILEPATH"], "rb").read()
        header_vars = t[0]
        if "@ISTEMPLATE" not in header_vars:
            if t[1]:
                tmp_output_path = output_path
                tmp_input_path = input_path
                tmp_template_root_path = input_path
                tmp_template_path = t[0][b"%TEMPLATE"].decode("utf-8")
                if tmp_output_path[-1] != "/":
                    tmp_output_path += "/"
                if tmp_template_root_path[-1] != "/":
                    tmp_template_root_path += "/"
                if tmp_input_path[0] == "/":
                    tmp_input_path = tmp_input_path[1:]
                if tmp_template_path[0] == "/":
                    tmp_template_path = tmp_template_path[1:]
                tmp_input_path = header_vars[b"@FILEPATH"][len(tmp_input_path) + 2:]
                template_path = (tmp_template_root_path + tmp_template_path)
                template_file = open(template_path, "rb")
                template_content = template_file.read()
                template_content = template_content[12:]
                pointer = 0
                if verbose:
                    print("Building " + tmp_output_path +
                          tmp_input_path)
                while True:
                    pointer_start = template_content[pointer:].find(b"[!-")
                    if pointer_start >= 0:
                        pointer_end = template_content[
                            pointer + pointer_start:].find(b"-!]")
                        if pointer_end >= 0:
                            replaced_content = template_content[
                                pointer + pointer_start: + pointer +
                                pointer_start + pointer_end + 3]
                            template_content = template_content.replace(
                                replaced_content, handle_variables(
                                header_vars, header_list, replaced_content))
                            pointer += pointer_start + pointer_end + 3
                        else:
                            break
                    else:
                        break
                # Remove beginning and trailing newline characters and spaces
                template_content = template_content.replace(b"\r\n", b"\n")
                while len(template_content) > 0:
                    if (template_content[0] == ord("\n") or
                            template_content[0] == ord(" ")):
                        template_content = template_content[1:]
                    elif (template_content[-1] == ord("\n") or
                            template_content[-1] == ord(" ")):
                        template_content = template_content[: -1]
                    else:
                        break
                file_content = template_content
            tmp_output_path = output_path
            tmp_input_path = input_path
            if tmp_output_path[-1] != "/":
                tmp_output_path += "/"
            if tmp_input_path[0] == "/":
                tmp_input_path = tmp_input_path[1:]
            tmp_input_path = header_vars[b"@FILEPATH"][len(tmp_input_path) + 2:]
            os.makedirs(tmp_output_path + "/".join(
                tmp_input_path.split("/")[: -1]), 0o755, True)
            write_file = open(tmp_output_path + tmp_input_path, "wb")
            if verbose:
                print("Writing " + tmp_output_path + tmp_input_path)
            write_file.write(file_content)
    if verbose:
        print("")


#def handle_for(, bool):
#    


def handle_variables(header_vars, header_list, replaced_content):
    final_content = b""
    replaced_content = replaced_content.replace(b"[!-", b"")
    replaced_content = replaced_content.replace(b"-!]", b"")
    content_list = replaced_content.split(b" ")
    content_list = list(filter(None, content_list))
    x = 0
    while x < len(content_list):
        if len(content_list[x]) > 1:
            # TODO handle for statement
            if content_list[x][0] = b"for":
                if len(content_list[x])
                for_replace = 

            # handle variables
            if (content_list[x][0] == ord("{") and
                    content_list[x][-1] == ord("}")):
                if len(content_list[x]) > 2:
                    variable = content_list[x][1: -1]
                    if x > 0:
                        if content_list[x - 1] == b"print":
                            if variable in header_vars:
                                final_content += header_vars[variable]
                    else:
                        print("ignis: command needed before variable " +
                              variable.decode("utf-8"))
                        sys.exit(1)
        x += 1
    if len(final_content) > 0:
        while final_content[-1] == ord(b"\n"):
            final_content = final_content[: -1]
    return final_content


def get_header(file_path, content):
    header_vars = {}
    header_content = b""
    is_content_file = False
    header_vars[b"@FILEPATH"] = os.path.abspath(file_path)
    if content.find(b"!-template-!") == 0:
        header_vars["@ISTEMPLATE"] = True
        return header_vars, is_content_file
    start = content.find(b"!-header\n")
    if start == 0:
        end = content[start:].find(b"\n-!\n")
        if end >= 0:
            header_content = content[9: end]
            for var in header_content.split(b"\n"):
                if var != b"":
                    key_end = var.find(b"=")
                    if key_end < 0:
                        print("ignis: incorrectly formatted header line " +
                              var.decode("utf-8") + " in " +
                              os.path.abspath(file_path))
                        sys.exit(7)
                    if not re.match(b"^[A-Za-z0-9_-]*$", var[: key_end]):
                        if var[: key_end] != b"%TEMPLATE":
                            print("ignis: invalid header value name " +
                                  var[: key_end].decode("utf-8") + " in " +
                                  os.path.abspath(file_path))
                            sys.exit(8)
                    header_vars[var[: key_end]] = var[key_end + 1:]
            if b"%TEMPLATE" not in header_vars:
                print("ignis: %TEMPLATE required as a header line in " +
                      os.path.abspath(file_path))
                sys.exit(9)
            is_content_file = True
            content = content[end + 4:]
            while content[0] == ord(b"\n"):
                content = content[1:]
            header_vars[b"@CONTENT"] = content
        else:
            print("ignis: header section in " + os.path.abspath(file_path) +
                  " must end with -!")
            sys.exit(6)
    return header_vars, is_content_file


# Starts a HTTP server at HOST:PORT with the root directory being path
def handle_http(path):
    os.chdir(path)
    global HOST
    server = HandleTCPServer((HOST, PORT), HTTPRequestHandler)
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
    print("Usage: ignis [ OPTIONS ]... [ -i <path=\"./\"> ] " +
          "[ -o <path=\"__website__\"> ] \n\n Required:\n" +
          "  -i, --input  <path>      Input path of website content\n" +
          "  -o, --output  <path>     Output path for finished static " +
          "website\n\n" +
          " Options:\n"
          "  -h, --help               Print Help (this message) and exit\n" +
          "  -L, --LAN                Open test server up to local network\n"
          "  -T, --test               Run test web server on port 9999 " +
          "after build\n"
          "  -V, --verbose            Print verbose messages while " +
          "building\n"
          "  -v, --version            Print version information and exit\n\n" +
          " Examples:\n" +
          "  ignis -i path/to/files -o path/for/website\n" +
          "  ignis --verbose -o example-site\n" +
          "  ignis -V -T -L -o example-site\n" +
          "  ignis -VTL")


def version_print():
    print("ignis " + VERSION)


def main():
    global HOST
    help_flag = False
    version_flag = False
    verbose_flag = False
    http_flag = False
    lan_flag = False
    verbose = False
    input_path = "."
    output_path = "__website__"
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
            elif args[x][2:] == "verbose":
                verbose_flag = True
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
                elif y == "V":
                    verbose_flag = True
                elif y == "L":
                    lan_flag = True
                elif len(args[x][1:]) == 1 and y == "i":
                    if len(args) > x + 1:
                        input_path = args[x + 1]
                        x += 1
                        break
                    else:
                        print("ignis: no input path included\nTry 'ignis " +
                              "--help' for more information.")
                        sys.exit(2)
                elif len(args[x][1:]) == 1 and y == "o":
                    if len(args) > x + 1:
                        output_path = args[x + 1]
                        x += 1
                        break
                    else:
                        print("ignis: no output path included\nTry 'ignis " +
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
    if help_flag or version_flag:
        if help_flag:
            help_print()
        else:
            version_print()
        sys.exit(0)
    if lan_flag and not http_flag:
        print("ignis: --test must be included to use LAN flag\n" +
              "Try 'ignis --help' for more information.")
        sys.exit(10)
    if verbose_flag:
        verbose = True
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    if input_path == output_path:
        print("ignis: input path and output path cannot be the same path")
        sys.exit(11)
    if input_path[-1] == "/":
        input_path = input_path[: -1]
    handle_files(get_files(input_path, output_path),
                 input_path, output_path, verbose)
    if http_flag:
        if lan_flag:
            HOST = "0.0.0.0"
        handle_http(output_path)

if __name__ == "__main__":
    main()
