import argparse
import gzip
import http.server
import os
import shutil
import socketserver
import sys
import time

from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

root_directory = "/home/userdata/workspace-TESTUUID/"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/upcheck":
			self.send_response(HTTPStatus.OK)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(b"OK")
		else:
			super().do_GET()

	def do_POST(self):
		if self.path == "/uploadFile":
			content_length = int(self.headers["Content-Length"])
			post_data = self.rfile.read(content_length)

			# Parse the form data
			form_data = parse_qs(post_data.decode("utf-8"))

			# Get the uploaded file
			file_data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")

			# Save the file to the root directory
			filename = form_data["file"][0]
			file_path = os.path.join(root_directory, "userdata", filename)
			with open(file_path, "w") as file:
				file.write(file_data)

			self.send_response(HTTPStatus.OK)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(b"File uploaded successfully")
		else:
			super().do_POST()

class MyTCPServer(socketserver.TCPServer):
	allow_reuse_address = True

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--addr", default=":8080", help="http service address")
	parser.add_argument("--root", default="/home/userdata/workspace-TESTUUID/", help="root directory for user files")
	args = parser.parse_args()

	global root_directory
	root_directory = args.root

	handler = MyHTTPRequestHandler
	httpd = MyTCPServer(("", int(args.addr.split(":")[1])), handler)

	print("Go server listening on port", args.addr)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()

if __name__ == "__main__":
	main()