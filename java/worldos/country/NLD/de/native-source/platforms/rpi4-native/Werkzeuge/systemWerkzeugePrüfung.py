#!/usr/bin/env python3
"""tatsächlichDaten eigen 커널의 IP/ICMP, statuswertWert abfragenWert, 현지어 befehl, 게스트 verlassenProzessProgramm validieren."""
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


def ausführenVorgang():
    Strukturanalysierer=argparse.ArgumentParser();Strukturanalysierer.add_argument('--edition',type=Path);Strukturanalysierer.add_argument('--output',type=Path);Strukturanalysierer.add_argument('--poweroff-only',action='store_true');argumente=Strukturanalysierer.parse_args()
    projektWurzel=Path(__file__).resolve().parents[1];einstellungen={};nameTabelle={}
    if argumente.edition:
        landWert=argumente.edition.resolve();einstellungen=json.loads((landWert/'native.json').read_text());nameTabelle=einstellungen['identifiers'];projektWurzel=landWert/einstellungen['source']/einstellungen['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(landWert/'native-edition.py'),'check'])
        Wirtssystem=landWert/'host/qemu'
        if Wirtssystem.is_file():os.environ['QEMU_AARCH64']=str(Wirtssystem)
    Werkzeuge=projektWurzel/Path(einstellungen.get('runner','Werkzeuge/befehlAusführen.py')).parent
    sys.path.insert(0,str(Werkzeuge))
    def lesen(Name):
        pfad=Werkzeuge/(nameTabelle.get(Name,Name)+'.py');vertragWert=importlib.util.spec_from_file_location('test_'+Name,str(pfad));modulWert=importlib.util.module_from_spec(vertragWert);vertragWert.loader.exec_module(modulWert);return modulWert
    ausführungModul=lesen('befehlAusführen');netzwerkModul=lesen('netzwerkBrücke');befehl=getattr(ausführungModul,nameTabelle.get('befehl','befehl'));brückeTyp=getattr(netzwerkModul,nameTabelle.get('netzwerkBrücke','netzwerkBrücke'))
    alternativnameWert=einstellungen.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'iPAdresse','ping':'rückmeldungPrüfung','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'stromversorgungAusgeschaltet','help':'hilfeAnzeigen'})
    sys.path.insert(0,str(projektWurzel/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(projektWurzel);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Ausgabe=argumente.output or projektWurzel/'build/verification/system-tools';Ausgabe.mkdir(parents=True,exist_ok=True)
    berichtWert={'passed':False,'country':einstellungen.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    protokolldateiAufzeichnung=bytearray();folgeWert=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as vorläufigWert:
        steuerungPfad=Path(vorläufigWert)/'qmp.sock'
        while True:
            with socket.socket() as wertSuchen:wertSuchen.bind(('127.0.0.1',0));portNummer=wertSuchen.getsockname()[1]
            if not 50000<=portNummer<=50007:break
        with brückeTyp(portNummer,erfassen=True,gastAdresse=ipTestText('10.0.2.20'),wirtssystemAdresse='127.0.0.2') as brückeWert:
            prozessWert=subprocess.Popen(befehl()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(steuerungPfad)]+brückeWert.weitergeleitetArgument(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            auswählenElementeintrag=selectors.DefaultSelector();auswählenElementeintrag.register(prozessWert.stdout,selectors.EVENT_READ)
            def empfangen(wertAnzeigen,ausführenVorgang=0,grenzwertWert=45):
                endung=time.monotonic()+grenzwertWert
                while wertAnzeigen not in protokolldateiAufzeichnung[ausführenVorgang:]:
                    if time.monotonic()>endung or prozessWert.poll() is not None:raise AssertionError('Missing '+repr(wertAnzeigen)+'\n'+protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8','replace'))
                    for tasteWert,_ in auswählenElementeintrag.select(.1):
                        Daten=tasteWert.fileobj.read(65536)
                        if Daten:protokolldateiAufzeichnung.extend(Daten)
                return protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8','replace').replace('\r\n','\n')
            def senden(Daten):prozessWert.stdin.write(Daten);prozessWert.stdin.flush()
            def befehlshülle(Text):
                Text=ipTestText(Text)
                print(berichtWert['country'],Text,flush=True);folgeWert[0]+=1;wertAnzeigen='__SYSTEM_DONE_'+str(folgeWert[0])+'__';ausführenVorgang=len(protokolldateiAufzeichnung)
                senden((Text+'; echo; echo '+wertAnzeigen+'\n').encode())
                endeMarkierung=('\r\n'+wertAnzeigen+'\r\n').encode();empfangen(endeMarkierung,ausführenVorgang)
                endePosition=protokolldateiAufzeichnung.index(endeMarkierung,ausführenVorgang)+len(endeMarkierung)
                empfangen(b'jkoros-native> ',endePosition)
                return protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8','replace').replace('\r\n','\n')
            def überprüfen(Text,*werte):
                antwort=befehlshülle(Text)
                for Wert in werte:assert ipTestText(Wert) in antwort,(Text,Wert,antwort)
                return antwort
            try:
                empfangen(b'jkoros-native> ')
                if not argumente.poweroff_only:
                    hilfeWert=überprüfen('help system','ipconfig','ping','ps','top','df','poweroff')
                    for alternativName in alternativnameWert.values():assert alternativName in hilfeWert,(alternativName,hilfeWert)
                    überprüfen(alternativnameWert['help']+' system','Network / system')
                    überprüfen('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    überprüfen(alternativnameWert['ipconfig'],'inet 10.0.2.15');überprüfen('ip addr show','sl0: UP');überprüfen('ifconfig','sl0: UP')
                    for ungültigEinstellungen in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        fehler=überprüfen('ipconfig set '+ungültigEinstellungen+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in fehler,fehler
                        überprüfen('ipconfig','inet 10.0.2.15')
                    überprüfen('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    überprüfen(alternativnameWert['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    überprüfen('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    überprüfen('ip link set dev sl0 down','sl0: DOWN');überprüfen('ping -c 1 10.0.2.2; echo STATUS=$?','fehler -100','STATUS=1')
                    überprüfen('ipconfig up','sl0: UP')
                    überprüfen(alternativnameWert['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    überprüfen('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    überprüfen('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');überprüfen(alternativnameWert['route'],'10.0.2.2 sl0')
                    überprüfen('ftpd start','FTP listening')
                    überprüfen(alternativnameWert['netstat'],'10.0.2.20:21','LISTEN');überprüfen('ss','LISTEN')
                    überprüfen('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','fehler -16')
                    with ftplib.FTP() as anfragestelleWert:
                        anfragestelleWert.connect('127.0.0.2',portNummer,timeout=20);anfragestelleWert.login();Daten=b'Network address was changed in the guest.\n'
                        anfragestelleWert.storbinary('STOR net-state.txt',io.BytesIO(Daten));empfangenWertDaten=bytearray();anfragestelleWert.retrbinary('RETR net-state.txt',empfangenWertDaten.extend);assert empfangenWertDaten==Daten;anfragestelleWert.delete('net-state.txt')
                    überprüfen('ftpd stop','FTP stopped');überprüfen('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    berichtWert['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def gespeichert(Text):
                        gefundenWert=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Text);assert gefundenWert,Text;return tuple(map(int,gefundenWert.groups()))
                    davorWert=gespeichert(überprüfen('df','RAM only'));überprüfen('echo disk-proof > sys-state.txt');danachStatuswert=gespeichert(überprüfen(alternativnameWert['df'],'RAM only'))
                    assert danachStatuswert[1]-davorWert[1]==16384 and danachStatuswert[4]-davorWert[4]==1 and danachStatuswert[3]-davorWert[3]==11,(davorWert,danachStatuswert)
                    überprüfen('rm sys-state.txt');assert gespeichert(befehlshülle('df'))==davorWert
                    Speicher=überprüfen(alternativnameWert['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');mengeWert=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Speicher).groups()));assert 0<mengeWert[1]<=mengeWert[0] and mengeWert[1]+mengeWert[2]==mengeWert[0]
                    überprüfen(alternativnameWert['ps'],'kernel/shell');überprüfen(alternativnameWert['uptime'],'seconds')
                    zustandInformation=überprüfen(alternativnameWert['top']+' -n 2','kernel/shell');assert zustandInformation.count('PID SLOT STATE')==2,zustandInformation
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    überprüfen('terminal','TERMINAL READY');ausführenVorgang=len(protokolldateiAufzeichnung);senden(b'vi process.txt\n');empfangen(b'NORMAL',ausführenVorgang)
                    ausführenVorgang=len(protokolldateiAufzeichnung);senden(bytes([30,2,1,0,0,0,0]));empfangen(b'jkoros-native> ',ausführenVorgang)
                    eintragListe=überprüfen('ps','SUSPENDED','vi process.txt');gefundenWert=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',eintragListe);assert gefundenWert and int(gefundenWert.group(2))>0,eintragListe
                    überprüfen('free','EL0 mapped KiB: '+gefundenWert.group(2))
                    ausführenVorgang=len(protokolldateiAufzeichnung);senden(b'top\n');empfangen(b'PID SLOT STATE',ausführenVorgang);senden(b'q');empfangen(b'jkoros-native> ',ausführenVorgang)
                    # Test a multibyte prefix through the real shell completion path.
                    if alternativnameWert['df']!='df':
                        ausführenVorgang=len(protokolldateiAufzeichnung);senden((alternativnameWert['df'][:-1]+'\t\n').encode());empfangen(b'RAM only',ausführenVorgang);empfangen(b'jkoros-native> ',ausführenVorgang)
                    berichtWert['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as steuerungWert:
                    steuerungWert.settimeout(15);steuerungWert.connect(str(steuerungPfad));datenstromWert=steuerungWert.makefile('rwb');json.loads(datenstromWert.readline());datenstromWert.write(b'{"execute":"qmp_capabilities"}\n');datenstromWert.flush()
                    while 'return' not in json.loads(datenstromWert.readline()):pass
                    senden((('poweroff' if argumente.poweroff_only else alternativnameWert['poweroff'])+'\n').encode())
                    while True:
                        ereignis=json.loads(datenstromWert.readline())
                        if ereignis.get('event')=='SHUTDOWN':break
                    assert ereignis['data']['guest'] and ereignis['data']['reason']=='guest-shutdown',ereignis
                    assert prozessWert.wait(timeout=15)==0
                    berichtWert['shutdown']=ereignis;berichtWert['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                berichtWert['network_trace']=brückeWert.spurProtokolldatei
                assert argumente.poweroff_only or any(eintragWert['protocol']==1 and eintragWert['direction']=='from_guest' for eintragWert in brückeWert.spurProtokolldatei)
                berichtWert['passed']=True
            finally:
                if prozessWert.poll() is None:os.killpg(prozessWert.pid,signal.SIGTERM)
                try:prozessWert.wait(timeout=10)
                except subprocess.TimeoutExpired:prozessWert.kill();prozessWert.wait()
                auswählenElementeintrag.close();(Ausgabe/'serial.log').write_bytes(protokolldateiAufzeichnung);(Ausgabe/'report.json').write_text(json.dumps(berichtWert,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tasteWert:Wert for tasteWert,Wert in berichtWert.items() if tasteWert!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ausführenVorgang()
