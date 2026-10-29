#!/usr/bin/env python3
"""stvarni_podaci 자체 커널의 IP/ICMP, Status_VALUE upit_VALUE, 현지어 komanda, 게스트 Izađi_program potvrditi."""
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


def koristiti():
    analizator_48ee4b1b=argparse.ArgumentParser();analizator_48ee4b1b.add_argument('--edition',type=Path);analizator_48ee4b1b.add_argument('--output',type=Path);analizator_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=analizator_48ee4b1b.parse_args()
    radnja_koren=Path(__file__).resolve().parents[1];Postavke={};ime_tabela={}
    if 인수.edition:
        Kantri_VALUE=인수.edition.resolve();Postavke=json.loads((Kantri_VALUE/'native.json').read_text());ime_tabela=Postavke['identifiers'];radnja_koren=Kantri_VALUE/Postavke['source']/Postavke['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Kantri_VALUE/'native-edition.py'),'check'])
        host=Kantri_VALUE/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    Alatke=radnja_koren/Path(Postavke.get('runner','Alatke/Izvrši_komanda.py')).parent
    sys.path.insert(0,str(Alatke))
    def 읽기(ime):
        putanja=Alatke/(ime_tabela.get(ime,ime)+'.py');ugovor_VALUE=importlib.util.spec_from_file_location('test_'+ime,str(putanja));modul_VALUE=importlib.util.module_from_spec(ugovor_VALUE);ugovor_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=읽기('Izvrši_komanda');Mreža_modul=읽기('mrežni_most');komanda=getattr(실행모듈,ime_tabela.get('komanda','komanda'));most_tip=getattr(Mreža_modul,ime_tabela.get('mrežni_most','mrežni_most'))
    prečica_VALUE_0a38607b=Postavke.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresa','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'emisija_pomoć_na_mreži'})
    sys.path.insert(0,str(radnja_koren/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(radnja_koren);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or radnja_koren/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    izveštaj_VALUE={'passed':False,'country':Postavke.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_snimi=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrola_putanja=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));broj_porta=SEARCH_VALUE.getsockname()[1]
            if not 50000<=broj_porta<=50007:break
        with most_tip(broj_porta,uhvatiti=True,gost_adresa=ipTestText('10.0.2.20'),host_adresa='127.0.0.2') as most_VALUE:
            Proces_VALUE=subprocess.Popen(komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrola_putanja)]+most_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_stavka=selectors.DefaultSelector();CHOOSE_stavka.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def primiti(emisija_VALUE,koristiti=0,제한=45):
                끝=time.monotonic()+제한
                while emisija_VALUE not in LOG_snimi[koristiti:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(emisija_VALUE)+'\n'+LOG_snimi[koristiti:].decode('utf-8','replace'))
                    for Ključ_VALUE,_ in CHOOSE_stavka.select(.1):
                        podaci=Ključ_VALUE.fileobj.read(65536)
                        if podaci:LOG_snimi.extend(podaci)
                return LOG_snimi[koristiti:].decode('utf-8','replace').replace('\r\n','\n')
            def poslati(podaci):Proces_VALUE.stdin.write(podaci);Proces_VALUE.stdin.flush()
            def ljuska(SMS):
                SMS=ipTestText(SMS)
                print(izveštaj_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;emisija_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';koristiti=len(LOG_snimi)
                poslati((SMS+'; echo; echo '+emisija_VALUE+'\n').encode())
                završiti_razgovor_označivač=('\r\n'+emisija_VALUE+'\r\n').encode();primiti(završiti_razgovor_označivač,koristiti)
                završiti_razgovor_pozicija=LOG_snimi.index(završiti_razgovor_označivač,koristiti)+len(završiti_razgovor_označivač)
                primiti(b'jkoros-native> ',završiti_razgovor_pozicija)
                return LOG_snimi[koristiti:].decode('utf-8','replace').replace('\r\n','\n')
            def verifikovati(SMS,*값들):
                odgovor=ljuska(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in odgovor,(SMS,VALUE,odgovor)
                return odgovor
            try:
                primiti(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    pomoć_na_mreži_VALUE=verifikovati('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in prečica_VALUE_0a38607b.values():assert 별칭 in pomoć_na_mreži_VALUE,(별칭,pomoć_na_mreži_VALUE)
                    verifikovati(prečica_VALUE_0a38607b['help']+' system','Network / system')
                    verifikovati('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifikovati(prečica_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');verifikovati('ip addr show','sl0: UP');verifikovati('ifconfig','sl0: UP')
                    for nevažeći_Postavke in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        greška=verifikovati('ipconfig set '+nevažeći_Postavke+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in greška,greška
                        verifikovati('ipconfig','inet 10.0.2.15')
                    verifikovati('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifikovati(prečica_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifikovati('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifikovati('ip link set dev sl0 down','sl0: DOWN');verifikovati('ping -c 1 10.0.2.2; echo STATUS=$?','greška -100','STATUS=1')
                    verifikovati('ipconfig up','sl0: UP')
                    verifikovati(prečica_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifikovati('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifikovati('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifikovati(prečica_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    verifikovati('ftpd start','FTP listening')
                    verifikovati(prečica_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');verifikovati('ss','LISTEN')
                    verifikovati('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','greška -16')
                    with ftplib.FTP() as klijent_VALUE:
                        klijent_VALUE.connect('127.0.0.2',broj_porta,timeout=20);klijent_VALUE.login();podaci=b'Network address was changed in the guest.\n'
                        klijent_VALUE.storbinary('STOR net-state.txt',io.BytesIO(podaci));RECEIVED_podaci=bytearray();klijent_VALUE.retrbinary('RETR net-state.txt',RECEIVED_podaci.extend);assert RECEIVED_podaci==podaci;klijent_VALUE.delete('net-state.txt')
                    verifikovati('ftpd stop','FTP stopped');verifikovati('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    izveštaj_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(verifikovati('df','RAM only'));verifikovati('echo disk-proof > sys-state.txt');후=저장값(verifikovati(prečica_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifikovati('rm sys-state.txt');assert 저장값(ljuska('df'))==전
                    Memorija_VALUE=verifikovati(prečica_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorija_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verifikovati(prečica_VALUE_0a38607b['ps'],'kernel/shell');verifikovati(prečica_VALUE_0a38607b['uptime'],'seconds')
                    status_informacije=verifikovati(prečica_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert status_informacije.count('PID SLOT STATE')==2,status_informacije
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifikovati('terminal','TERMINAL READY');koristiti=len(LOG_snimi);poslati(b'vi process.txt\n');primiti(b'NORMAL',koristiti)
                    koristiti=len(LOG_snimi);poslati(bytes([30,2,1,0,0,0,0]));primiti(b'jkoros-native> ',koristiti)
                    stavka_Lista=verifikovati('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',stavka_Lista);assert 찾음 and int(찾음.group(2))>0,stavka_Lista
                    verifikovati('free','EL0 mapped KiB: '+찾음.group(2))
                    koristiti=len(LOG_snimi);poslati(b'top\n');primiti(b'PID SLOT STATE',koristiti);poslati(b'q');primiti(b'jkoros-native> ',koristiti)
                    # Test a multibyte prefix through the real shell completion path.
                    if prečica_VALUE_0a38607b['df']!='df':
                        koristiti=len(LOG_snimi);poslati((prečica_VALUE_0a38607b['df'][:-1]+'\t\n').encode());primiti(b'RAM only',koristiti);primiti(b'jkoros-native> ',koristiti)
                    izveštaj_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                    kontrola_VALUE.settimeout(15);kontrola_VALUE.connect(str(kontrola_putanja));tok_VALUE=kontrola_VALUE.makefile('rwb');json.loads(tok_VALUE.readline());tok_VALUE.write(b'{"execute":"qmp_capabilities"}\n');tok_VALUE.flush()
                    while 'return' not in json.loads(tok_VALUE.readline()):pass
                    poslati((('poweroff' if 인수.poweroff_only else prečica_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        događaj=json.loads(tok_VALUE.readline())
                        if događaj.get('event')=='SHUTDOWN':break
                    assert događaj['data']['guest'] and događaj['data']['reason']=='guest-shutdown',događaj
                    assert Proces_VALUE.wait(timeout=15)==0
                    izveštaj_VALUE['shutdown']=događaj;izveštaj_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                izveštaj_VALUE['network_trace']=most_VALUE.evidencija_praćenja
                assert 인수.poweroff_only or any(stavka_VALUE['protocol']==1 and stavka_VALUE['direction']=='from_guest' for stavka_VALUE in most_VALUE.evidencija_praćenja)
                izveštaj_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                CHOOSE_stavka.close();(출력/'serial.log').write_bytes(LOG_snimi);(출력/'report.json').write_text(json.dumps(izveštaj_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ključ_VALUE:VALUE for Ključ_VALUE,VALUE in izveštaj_VALUE.items() if Ključ_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':koristiti()
