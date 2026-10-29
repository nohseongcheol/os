#!/usr/bin/env python3
"""stvaran_podaci vlastiti 커널의 IP/ICMP, Stanje_VALUE upit_VALUE, 현지어 Naredba, 게스트 Izlaz_program potvrditi."""
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


def Pokreni():
    analizator_48ee4b1b=argparse.ArgumentParser();analizator_48ee4b1b.add_argument('--edition',type=Path);analizator_48ee4b1b.add_argument('--output',type=Path);analizator_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumenti=analizator_48ee4b1b.parse_args()
    akcija_korijen=Path(__file__).resolve().parents[1];Postavke={};naziv_tablica={}
    if Argumenti.edition:
        Country_VALUE=Argumenti.edition.resolve();Postavke=json.loads((Country_VALUE/'native.json').read_text());naziv_tablica=Postavke['identifiers'];akcija_korijen=Country_VALUE/Postavke['source']/Postavke['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALUE/'native-edition.py'),'check'])
        domaćin=Country_VALUE/'host/qemu'
        if domaćin.is_file():os.environ['QEMU_AARCH64']=str(domaćin)
    Alati=akcija_korijen/Path(Postavke.get('runner','Alati/Izvrši_naredba.py')).parent
    sys.path.insert(0,str(Alati))
    def Čitaj(Ime):
        PUTANJA=Alati/(naziv_tablica.get(Ime,Ime)+'.py');slučaj_VALUE=importlib.util.spec_from_file_location('test_'+Ime,str(PUTANJA));modul_VALUE=importlib.util.module_from_spec(slučaj_VALUE);slučaj_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Čitaj('Izvrši_naredba');mreža_modul=Čitaj('most_3de4fe3a');Naredba=getattr(실행모듈,naziv_tablica.get('Naredba','Naredba'));most_TYPE=getattr(mreža_modul,naziv_tablica.get('most_3de4fe3a','most_3de4fe3a'))
    prečac_VALUE_0a38607b=Postavke.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresa','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'emisija_pomoć'})
    sys.path.insert(0,str(akcija_korijen/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(akcija_korijen);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Izlaz=Argumenti.output or akcija_korijen/'build/verification/system-tools';Izlaz.mkdir(parents=True,exist_ok=True)
    izvješće_VALUE={'passed':False,'country':Postavke.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_zapis=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrola_put=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Traži_VALUE:Traži_VALUE.bind(('127.0.0.1',0));broj_priključka=Traži_VALUE.getsockname()[1]
            if not 50000<=broj_priključka<=50007:break
        with most_TYPE(broj_priključka,snimiti=True,gost_adresa=ipTestText('10.0.2.20'),domaćin_adresa='127.0.0.2') as most_VALUE:
            Proces_VALUE=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrola_put)]+most_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_artikl=selectors.DefaultSelector();CHOOSE_artikl.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def primiti(emisija_VALUE,Pokreni=0,제한=45):
                끝=time.monotonic()+제한
                while emisija_VALUE not in LOG_zapis[Pokreni:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(emisija_VALUE)+'\n'+LOG_zapis[Pokreni:].decode('utf-8','replace'))
                    for Ključ_VALUE,_ in CHOOSE_artikl.select(.1):
                        podaci=Ključ_VALUE.fileobj.read(65536)
                        if podaci:LOG_zapis.extend(podaci)
                return LOG_zapis[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
            def slati(podaci):Proces_VALUE.stdin.write(podaci);Proces_VALUE.stdin.flush()
            def ljuska(Tekst):
                Tekst=ipTestText(Tekst)
                print(izvješće_VALUE['country'],Tekst,flush=True);SEQUENCE_VALUE[0]+=1;emisija_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Pokreni=len(LOG_zapis)
                slati((Tekst+'; echo; echo '+emisija_VALUE+'\n').encode())
                završiti_razgovor_marker=('\r\n'+emisija_VALUE+'\r\n').encode();primiti(završiti_razgovor_marker,Pokreni)
                završiti_razgovor_položaj=LOG_zapis.index(završiti_razgovor_marker,Pokreni)+len(završiti_razgovor_marker)
                primiti(b'jkoros-native> ',završiti_razgovor_položaj)
                return LOG_zapis[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
            def provjeriti(Tekst,*값들):
                odgovor=ljuska(Tekst)
                for VALUE in 값들:assert ipTestText(VALUE) in odgovor,(Tekst,VALUE,odgovor)
                return odgovor
            try:
                primiti(b'jkoros-native> ')
                if not Argumenti.poweroff_only:
                    pomoć_VALUE=provjeriti('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in prečac_VALUE_0a38607b.values():assert 별칭 in pomoć_VALUE,(별칭,pomoć_VALUE)
                    provjeriti(prečac_VALUE_0a38607b['help']+' system','Network / system')
                    provjeriti('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    provjeriti(prečac_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');provjeriti('ip addr show','sl0: UP');provjeriti('ifconfig','sl0: UP')
                    for nevaljan_Postavke in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        GREŠKA=provjeriti('ipconfig set '+nevaljan_Postavke+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in GREŠKA,GREŠKA
                        provjeriti('ipconfig','inet 10.0.2.15')
                    provjeriti('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    provjeriti(prečac_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    provjeriti('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    provjeriti('ip link set dev sl0 down','sl0: DOWN');provjeriti('ping -c 1 10.0.2.2; echo STATUS=$?','GREŠKA -100','STATUS=1')
                    provjeriti('ipconfig up','sl0: UP')
                    provjeriti(prečac_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    provjeriti('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    provjeriti('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');provjeriti(prečac_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    provjeriti('ftpd start','FTP listening')
                    provjeriti(prečac_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');provjeriti('ss','LISTEN')
                    provjeriti('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','GREŠKA -16')
                    with ftplib.FTP() as klijent_VALUE:
                        klijent_VALUE.connect('127.0.0.2',broj_priključka,timeout=20);klijent_VALUE.login();podaci=b'Network address was changed in the guest.\n'
                        klijent_VALUE.storbinary('STOR net-state.txt',io.BytesIO(podaci));RECEIVED_podaci=bytearray();klijent_VALUE.retrbinary('RETR net-state.txt',RECEIVED_podaci.extend);assert RECEIVED_podaci==podaci;klijent_VALUE.delete('net-state.txt')
                    provjeriti('ftpd stop','FTP stopped');provjeriti('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    izvješće_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(provjeriti('df','RAM only'));provjeriti('echo disk-proof > sys-state.txt');후=저장값(provjeriti(prečac_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    provjeriti('rm sys-state.txt');assert 저장값(ljuska('df'))==전
                    Memorija_VALUE=provjeriti(prečac_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorija_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    provjeriti(prečac_VALUE_0a38607b['ps'],'kernel/shell');provjeriti(prečac_VALUE_0a38607b['uptime'],'seconds')
                    stanje_informacija=provjeriti(prečac_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert stanje_informacija.count('PID SLOT STATE')==2,stanje_informacija
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    provjeriti('terminal','TERMINAL READY');Pokreni=len(LOG_zapis);slati(b'vi process.txt\n');primiti(b'NORMAL',Pokreni)
                    Pokreni=len(LOG_zapis);slati(bytes([30,2,1,0,0,0,0]));primiti(b'jkoros-native> ',Pokreni)
                    unos_Popis=provjeriti('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',unos_Popis);assert 찾음 and int(찾음.group(2))>0,unos_Popis
                    provjeriti('free','EL0 mapped KiB: '+찾음.group(2))
                    Pokreni=len(LOG_zapis);slati(b'top\n');primiti(b'PID SLOT STATE',Pokreni);slati(b'q');primiti(b'jkoros-native> ',Pokreni)
                    # Test a multibyte prefix through the real shell completion path.
                    if prečac_VALUE_0a38607b['df']!='df':
                        Pokreni=len(LOG_zapis);slati((prečac_VALUE_0a38607b['df'][:-1]+'\t\n').encode());primiti(b'RAM only',Pokreni);primiti(b'jkoros-native> ',Pokreni)
                    izvješće_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                    kontrola_VALUE.settimeout(15);kontrola_VALUE.connect(str(kontrola_put));tok_VALUE=kontrola_VALUE.makefile('rwb');json.loads(tok_VALUE.readline());tok_VALUE.write(b'{"execute":"qmp_capabilities"}\n');tok_VALUE.flush()
                    while 'return' not in json.loads(tok_VALUE.readline()):pass
                    slati((('poweroff' if Argumenti.poweroff_only else prečac_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Događaj=json.loads(tok_VALUE.readline())
                        if Događaj.get('event')=='SHUTDOWN':break
                    assert Događaj['data']['guest'] and Događaj['data']['reason']=='guest-shutdown',Događaj
                    assert Proces_VALUE.wait(timeout=15)==0
                    izvješće_VALUE['shutdown']=Događaj;izvješće_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                izvješće_VALUE['network_trace']=most_VALUE.zapis_praćenja
                assert Argumenti.poweroff_only or any(unos_VALUE['protocol']==1 and unos_VALUE['direction']=='from_guest' for unos_VALUE in most_VALUE.zapis_praćenja)
                izvješće_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                CHOOSE_artikl.close();(Izlaz/'serial.log').write_bytes(LOG_zapis);(Izlaz/'report.json').write_text(json.dumps(izvješće_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ključ_VALUE:VALUE for Ključ_VALUE,VALUE in izvješće_VALUE.items() if Ključ_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Pokreni()
