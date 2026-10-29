#!/usr/bin/env python3
"""skutočný_údaje vlastné 커널의 IP/ICMP, Stav_VALUE dotaz_VALUE, 현지어 Príkaz, 게스트 Skončiť_program overiť_5fb2b747."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def Spustiť_2():
    analyzátor_48ee4b1b=argparse.ArgumentParser();analyzátor_48ee4b1b.add_argument('--edition',type=Path);analyzátor_48ee4b1b.add_argument('--output',type=Path);analyzátor_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumenty=analyzátor_48ee4b1b.parse_args()
    akcia_koreň=Path(__file__).resolve().parents[1];Nastavenia={};názov_tabuľka={}
    if Argumenty.edition:
        Country_VALUE=Argumenty.edition.resolve();Nastavenia=json.loads((Country_VALUE/'native.json').read_text());názov_tabuľka=Nastavenia['identifiers'];akcia_koreň=Country_VALUE/Nastavenia['source']/Nastavenia['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALUE/'native-edition.py'),'check'])
        hostiteľ=Country_VALUE/'host/qemu'
        if hostiteľ.is_file():os.environ['QEMU_AARCH64']=str(hostiteľ)
    Nástroje=akcia_koreň/Path(Nastavenia.get('runner','Nástroje/Vykonať_príkaz.py')).parent
    sys.path.insert(0,str(Nástroje))
    def Čítanie(Názov):
        Cesta=Nástroje/(názov_tabuľka.get(Názov,Názov)+'.py');prípad_VALUE=importlib.util.spec_from_file_location('test_'+Názov,str(Cesta));modul_VALUE=importlib.util.module_from_spec(prípad_VALUE);prípad_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Čítanie('Vykonať_príkaz');sieť_modul=Čítanie('sieťový_most');Príkaz=getattr(실행모듈,názov_tabuľka.get('Príkaz','Príkaz'));most_Typ=getattr(sieť_modul,názov_tabuľka.get('sieťový_most','sieťový_most'))
    alias_VALUE=Nastavenia.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adresa_IP','ping':'test_odpoveď','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'zobraziť_Pomocník'})
    sys.path.insert(0,str(akcia_koreň/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(akcia_koreň);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Výstup=Argumenty.output or akcia_koreň/'build/verification/system-tools';Výstup.mkdir(parents=True,exist_ok=True)
    správa_VALUE={'passed':False,'country':Nastavenia.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        riadenie_cesta=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Hľadať_VALUE:Hľadať_VALUE.bind(('127.0.0.1',0));číslo_portu=Hľadať_VALUE.getsockname()[1]
            if not 50000<=číslo_portu<=50007:break
        with most_Typ(číslo_portu,snímať=True,hosť_adresa=ipTestText('10.0.2.20'),hostiteľ_adresa='127.0.0.2') as most_VALUE:
            Proces_VALUE=subprocess.Popen(Príkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(riadenie_cesta)]+most_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_položka=selectors.DefaultSelector();CHOOSE_položka.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def dostať(zobraziť_VALUE_487749b8,Spustiť_2=0,제한=45):
                끝=time.monotonic()+제한
                while zobraziť_VALUE_487749b8 not in LOG_RECORD[Spustiť_2:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(zobraziť_VALUE_487749b8)+'\n'+LOG_RECORD[Spustiť_2:].decode('utf-8','replace'))
                    for Kľúč_VALUE,_ in CHOOSE_položka.select(.1):
                        údaje=Kľúč_VALUE.fileobj.read(65536)
                        if údaje:LOG_RECORD.extend(údaje)
                return LOG_RECORD[Spustiť_2:].decode('utf-8','replace').replace('\r\n','\n')
            def odoslať(údaje):Proces_VALUE.stdin.write(údaje);Proces_VALUE.stdin.flush()
            def 셸(Spracovanie_textu):
                Spracovanie_textu=ipTestText(Spracovanie_textu)
                print(správa_VALUE['country'],Spracovanie_textu,flush=True);SEQUENCE_VALUE[0]+=1;zobraziť_VALUE_487749b8='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Spustiť_2=len(LOG_RECORD)
                odoslať((Spracovanie_textu+'; echo; echo '+zobraziť_VALUE_487749b8+'\n').encode())
                ukončiť_hovor_fixka=('\r\n'+zobraziť_VALUE_487749b8+'\r\n').encode();dostať(ukončiť_hovor_fixka,Spustiť_2)
                ukončiť_hovor_pozícia=LOG_RECORD.index(ukončiť_hovor_fixka,Spustiť_2)+len(ukončiť_hovor_fixka)
                dostať(b'jkoros-native> ',ukončiť_hovor_pozícia)
                return LOG_RECORD[Spustiť_2:].decode('utf-8','replace').replace('\r\n','\n')
            def overiť(Spracovanie_textu,*값들):
                odozva=셸(Spracovanie_textu)
                for VALUE in 값들:assert ipTestText(VALUE) in odozva,(Spracovanie_textu,VALUE,odozva)
                return odozva
            try:
                dostať(b'jkoros-native> ')
                if not Argumenty.poweroff_only:
                    Pomocník_VALUE=overiť('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in Pomocník_VALUE,(별칭,Pomocník_VALUE)
                    overiť(alias_VALUE['help']+' system','Network / system')
                    overiť('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    overiť(alias_VALUE['ipconfig'],'inet 10.0.2.15');overiť('ip addr show','sl0: UP');overiť('ifconfig','sl0: UP')
                    for neplatné_Nastavenia in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        chyba=overiť('ipconfig set '+neplatné_Nastavenia+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in chyba,chyba
                        overiť('ipconfig','inet 10.0.2.15')
                    overiť('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    overiť(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    overiť('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    overiť('ip link set dev sl0 down','sl0: DOWN');overiť('ping -c 1 10.0.2.2; echo STATUS=$?','chyba -100','STATUS=1')
                    overiť('ipconfig up','sl0: UP')
                    overiť(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    overiť('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    overiť('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');overiť(alias_VALUE['route'],'10.0.2.2 sl0')
                    overiť('ftpd start','FTP listening')
                    overiť(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');overiť('ss','LISTEN')
                    overiť('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','chyba -16')
                    with ftplib.FTP() as klient_VALUE:
                        klient_VALUE.connect('127.0.0.2',číslo_portu,timeout=20);klient_VALUE.login();údaje=b'Network address was changed in the guest.\n'
                        klient_VALUE.storbinary('STOR net-state.txt',io.BytesIO(údaje));RECEIVED_údaje=bytearray();klient_VALUE.retrbinary('RETR net-state.txt',RECEIVED_údaje.extend);assert RECEIVED_údaje==údaje;klient_VALUE.delete('net-state.txt')
                    overiť('ftpd stop','FTP stopped');overiť('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    správa_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Spracovanie_textu):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Spracovanie_textu);assert 찾음,Spracovanie_textu;return tuple(map(int,찾음.groups()))
                    전=저장값(overiť('df','RAM only'));overiť('echo disk-proof > sys-state.txt');후=저장값(overiť(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    overiť('rm sys-state.txt');assert 저장값(셸('df'))==전
                    Pamäť_VALUE=overiť(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Pamäť_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    overiť(alias_VALUE['ps'],'kernel/shell');overiť(alias_VALUE['uptime'],'seconds')
                    stav_informácia=overiť(alias_VALUE['top']+' -n 2','kernel/shell');assert stav_informácia.count('PID SLOT STATE')==2,stav_informácia
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    overiť('terminal','TERMINAL READY');Spustiť_2=len(LOG_RECORD);odoslať(b'vi process.txt\n');dostať(b'NORMAL',Spustiť_2)
                    Spustiť_2=len(LOG_RECORD);odoslať(bytes([30,2,1,0,0,0,0]));dostať(b'jkoros-native> ',Spustiť_2)
                    položka_Zoznam=overiť('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',položka_Zoznam);assert 찾음 and int(찾음.group(2))>0,položka_Zoznam
                    overiť('free','EL0 mapped KiB: '+찾음.group(2))
                    Spustiť_2=len(LOG_RECORD);odoslať(b'top\n');dostať(b'PID SLOT STATE',Spustiť_2);odoslať(b'q');dostať(b'jkoros-native> ',Spustiť_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        Spustiť_2=len(LOG_RECORD);odoslať((alias_VALUE['df'][:-1]+'\t\n').encode());dostať(b'RAM only',Spustiť_2);dostať(b'jkoros-native> ',Spustiť_2)
                    správa_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as riadenie_VALUE:
                    riadenie_VALUE.settimeout(15);riadenie_VALUE.connect(str(riadenie_cesta));Stream_VALUE=riadenie_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    odoslať((('poweroff' if Argumenty.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Udalosť=json.loads(Stream_VALUE.readline())
                        if Udalosť.get('event')=='SHUTDOWN':break
                    assert Udalosť['data']['guest'] and Udalosť['data']['reason']=='guest-shutdown',Udalosť
                    assert Proces_VALUE.wait(timeout=15)==0
                    správa_VALUE['shutdown']=Udalosť;správa_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                správa_VALUE['network_trace']=most_VALUE.denník_sledovania
                assert Argumenty.poweroff_only or any(položka_VALUE['protocol']==1 and položka_VALUE['direction']=='from_guest' for položka_VALUE in most_VALUE.denník_sledovania)
                správa_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                CHOOSE_položka.close();(Výstup/'serial.log').write_bytes(LOG_RECORD);(Výstup/'report.json').write_text(json.dumps(správa_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kľúč_VALUE:VALUE for Kľúč_VALUE,VALUE in správa_VALUE.items() if Kľúč_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Spustiť_2()
