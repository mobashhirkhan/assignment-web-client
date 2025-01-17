#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
        # # request = f"GET {host} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        # self.socket.send(request)
        # self.socket.shutdown(socket.SHUT_WR)
        # recv = self.recvall(self.socket)
        # print(recv)
        #
        # self.close()
        return None

    def get_code(self, data):
        #line = data.split("\r\n")[0]
        code = int(data.split(" ")[1])
        return code

    def get_headers(self, data):
        headers = data.split("\r\n\r\n")[0]
        return headers

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # code = 500
        # body = ""

        # parsing the url and getting port and host name
        parsed_url = urllib.parse.urlparse(url)
        port = parsed_url.port
        host = parsed_url.hostname

        # if host is none then assign local host as the host
        if host is None:
            host = "localhost"

        # assigning path and if we have no path then assigning "/" as path
        path = urllib.parse.quote(parsed_url.path)
        if path == '':
            path = '/'

        # if no port is specified we take port as 80
        # https://uofa-cmput404.github.io/cmput404-slides/04-HTTP.html#/17
        if port is None:
            port = 80

        # request statement from TA
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n"

        # If args are passed, add them to the request
        if args:
            request = request + urllib.parse.urlencode(args)

        # connect to server
        self.connect(host, port)

        # sending request
        self.sendall(request)

        # receiving response
        recv = self.recvall(self.socket)

        # closing connection
        self.close()

        # getting header, code and body
        header = self.get_headers(recv)
        code = self.get_code(recv)
        body = self.get_body(recv)

        print("Header")
        print(header)
        print("Code")
        print(code)
        print("Body")
        print(body)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # code = 500
        # body = ""

        # parsing the url and getting port and host name
        parsed_url = urllib.parse.urlparse(url)
        port = parsed_url.port
        host = parsed_url.hostname

        # if host is none then assign local host as the host
        if host is None:
            host = "localhost"

        # assigning path and if we have no path then assigning "/" as path
        path = urllib.parse.quote(parsed_url.path)
        if path == '':
            path = '/'

        # if no port is specified we take port as 80
        # https://uofa-cmput404.github.io/cmput404-slides/04-HTTP.html#/17
        if port is None:
            port = 80

        # getting arguments for POST
        if args is not None:
            args = urllib.parse.urlencode(args)
        else:
            args = ""

        # finding length of argument
        args_len = str(len(args))

        # request statement from TA
        request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {args_len}\r\nConnection: close\r\n\r\n{args}"

        # connect to server
        self.connect(host, port)

        # sending request
        self.sendall(request)

        # receiving response
        recv = self.recvall(self.socket)

        # closing connection
        self.close()

        # getting header, code and body
        header = self.get_headers(recv)
        code = self.get_code(recv)
        body = self.get_body(recv)

        print("Header")
        print(header)
        print("Code")
        print(code)
        print("Body")
        print(body)

        # self.socket.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
