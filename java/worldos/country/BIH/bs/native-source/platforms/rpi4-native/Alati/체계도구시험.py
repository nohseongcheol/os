#!/usr/bin/env python3
"""stvaran_podaci 자체 커널의 IP/ICMP, stanje_VALUE upit_VALUE, 현지어 Naredba, 게스트 izaći_program ovjeriti."""
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
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');Argumenti=해석기.parse_args()
    projicirati_koijen=Path(__file__).resolve().parents[1];Postavke={};naziv_tabela={}
    if Argumenti.edition:
        나라=Argumenti.edition.resolve();Postavke=json.loads((나라/'native.json').read_text());naziv_tabela=Postavke['identifiers'];projicirati_koijen=나라/Postavke['source']/Postavke['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        organizator=나라/'host/qemu'
        if organizator.is_file():os.environ['QEMU_AARCH64']=str(organizator)
    Alati=projicirati_koijen/Path(Postavke.get('runner','Alati/Izvrši_komanda.py')).parent
    sys.path.insert(0,str(Alati))
    def Čitaj(Naziv):
        Putanja=Alati/(naziv_tabela.get(Naziv,Naziv)+'.py');slučaj_VALUE=importlib.util.spec_from_file_location('test_'+Naziv,str(Putanja));modul_VALUE=importlib.util.module_from_spec(slučaj_VALUE);slučaj_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Čitaj('Izvrši_komanda');Mreža_modul=Čitaj('Mreža_most');Naredba=getattr(실행모듈,naziv_tabela.get('Naredba','Naredba'));most_TYPE=getattr(Mreža_modul,naziv_tabela.get('Mreža_most','Mreža_most'))
    prečica_VALUE_0a38607b=Postavke.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresa','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'program_pomoć'})
    sys.path.insert(0,str(projicirati_koijen/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(projicirati_koijen);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Ispis=Argumenti.output or projicirati_koijen/'build/verification/system-tools';Ispis.mkdir(parents=True,exist_ok=True)
    izvještaj_VALUE={'passed':False,'country':Postavke.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_red=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrola_put=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Traži_VALUE:Traži_VALUE.bind(('127.0.0.1',0));broj_priključka=Traži_VALUE.getsockname()[1]
            if not 50000<=broj_priključka<=50007:break
        with most_TYPE(broj_priključka,snimiti=True,gost_adresa=ipTestText('10.0.2.20'),organizator_adresa='127.0.0.2') as most_VALUE:
            proces_VALUE=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrola_put)]+most_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_stavka=selectors.DefaultSelector();CHOOSE_stavka.register(proces_VALUE.stdout,selectors.EVENT_READ)
            def 받기(program_VALUE,Pokreni=0,제한=45):
                끝=time.monotonic()+제한
                while program_VALUE not in LOG_red[Pokreni:]:
                    if time.monotonic()>끝 or proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(program_VALUE)+'\n'+LOG_red[Pokreni:].decode('utf-8','replace'))
                    for ključ_VALUE,_ in CHOOSE_stavka.select(.1):
                        podaci=ključ_VALUE.fileobj.read(65536)
                        if podaci:LOG_red.extend(podaci)
                return LOG_red[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
            def poslati(podaci):proces_VALUE.stdin.write(podaci);proces_VALUE.stdin.flush()
            def ljuska(Tekst):
                Tekst=ipTestText(Tekst)
                print(izvještaj_VALUE['country'],Tekst,flush=True);SEQUENCE_VALUE[0]+=1;program_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Pokreni=len(LOG_red)
                poslati((Tekst+'; echo; echo '+program_VALUE+'\n').encode())
                끝표시=('\r\n'+program_VALUE+'\r\n').encode();받기(끝표시,Pokreni)
                završiti_položaj=LOG_red.index(끝표시,Pokreni)+len(끝표시)
                받기(b'jkoros-native> ',završiti_položaj)
                return LOG_red[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
            def potvrditi(Tekst,*값들):
                odgovoriti=ljuska(Tekst)
                for VALUE in 값들:assert ipTestText(VALUE) in odgovoriti,(Tekst,VALUE,odgovoriti)
                return odgovoriti
            try:
                받기(b'jkoros-native> ')
                if not Argumenti.poweroff_only:
                    pomoć_VALUE=potvrditi('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in prečica_VALUE_0a38607b.values():assert 별칭 in pomoć_VALUE,(별칭,pomoć_VALUE)
                    potvrditi(prečica_VALUE_0a38607b['help']+' system','Network / system')
                    potvrditi('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    potvrditi(prečica_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');potvrditi('ip addr show','sl0: UP');potvrditi('ifconfig','sl0: UP')
                    for nevažeće_Postavke in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        GRESKA=potvrditi('ipconfig set '+nevažeće_Postavke+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in GRESKA,GRESKA
                        potvrditi('ipconfig','inet 10.0.2.15')
                    potvrditi('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    potvrditi(prečica_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    potvrditi('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    potvrditi('ip link set dev sl0 down','sl0: DOWN');potvrditi('ping -c 1 10.0.2.2; echo STATUS=$?','GRESKA -100','STATUS=1')
                    potvrditi('ipconfig up','sl0: UP')
                    potvrditi(prečica_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    potvrditi('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    potvrditi('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');potvrditi(prečica_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    potvrditi('ftpd start','FTP listening')
                    potvrditi(prečica_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');potvrditi('ss','LISTEN')
                    potvrditi('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','GRESKA -16')
                    with ftplib.FTP() as klijent_VALUE:
                        klijent_VALUE.connect('127.0.0.2',broj_priključka,timeout=20);klijent_VALUE.login();podaci=b'Network address was changed in the guest.\n'
                        klijent_VALUE.storbinary('STOR net-state.txt',io.BytesIO(podaci));RECEIVED_podaci=bytearray();klijent_VALUE.retrbinary('RETR net-state.txt',RECEIVED_podaci.extend);assert RECEIVED_podaci==podaci;klijent_VALUE.delete('net-state.txt')
                    potvrditi('ftpd stop','FTP stopped');potvrditi('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    izvještaj_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(potvrditi('df','RAM only'));potvrditi('echo disk-proof > sys-state.txt');후=저장값(potvrditi(prečica_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    potvrditi('rm sys-state.txt');assert 저장값(ljuska('df'))==전
                    Memorija_VALUE=potvrditi(prečica_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorija_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    potvrditi(prečica_VALUE_0a38607b['ps'],'kernel/shell');potvrditi(prečica_VALUE_0a38607b['uptime'],'seconds')
                    stanje_informacija=potvrditi(prečica_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert stanje_informacija.count('PID SLOT STATE')==2,stanje_informacija
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    potvrditi('terminal','TERMINAL READY');Pokreni=len(LOG_red);poslati(b'vi process.txt\n');받기(b'NORMAL',Pokreni)
                    Pokreni=len(LOG_red);poslati(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Pokreni)
                    unos_spisak=potvrditi('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',unos_spisak);assert 찾음 and int(찾음.group(2))>0,unos_spisak
                    potvrditi('free','EL0 mapped KiB: '+찾음.group(2))
                    Pokreni=len(LOG_red);poslati(b'top\n');받기(b'PID SLOT STATE',Pokreni);poslati(b'q');받기(b'jkoros-native> ',Pokreni)
                    # Test a multibyte prefix through the real shell completion path.
                    if prečica_VALUE_0a38607b['df']!='df':
                        Pokreni=len(LOG_red);poslati((prečica_VALUE_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Pokreni);받기(b'jkoros-native> ',Pokreni)
                    izvještaj_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                    kontrola_VALUE.settimeout(15);kontrola_VALUE.connect(str(kontrola_put));tok_VALUE=kontrola_VALUE.makefile('rwb');json.loads(tok_VALUE.readline());tok_VALUE.write(b'{"execute":"qmp_capabilities"}\n');tok_VALUE.flush()
                    while 'return' not in json.loads(tok_VALUE.readline()):pass
                    poslati((('poweroff' if Argumenti.poweroff_only else prečica_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        događaj=json.loads(tok_VALUE.readline())
                        if događaj.get('event')=='SHUTDOWN':break
                    assert događaj['data']['guest'] and događaj['data']['reason']=='guest-shutdown',događaj
                    assert proces_VALUE.wait(timeout=15)==0
                    izvještaj_VALUE['shutdown']=događaj;izvještaj_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                izvještaj_VALUE['network_trace']=most_VALUE.trag_LOG
                assert Argumenti.poweroff_only or any(unos_VALUE['protocol']==1 and unos_VALUE['direction']=='from_guest' for unos_VALUE in most_VALUE.trag_LOG)
                izvještaj_VALUE['passed']=True
            finally:
                if proces_VALUE.poll() is None:os.killpg(proces_VALUE.pid,signal.SIGTERM)
                try:proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:proces_VALUE.kill();proces_VALUE.wait()
                CHOOSE_stavka.close();(Ispis/'serial.log').write_bytes(LOG_red);(Ispis/'report.json').write_text(json.dumps(izvještaj_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ključ_VALUE:VALUE for ključ_VALUE,VALUE in izvještaj_VALUE.items() if ključ_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Pokreni()
