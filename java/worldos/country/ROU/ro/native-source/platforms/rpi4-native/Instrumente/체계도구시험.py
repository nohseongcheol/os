#!/usr/bin/env python3
"""real_date propriu 커널의 IP/ICMP, Stare_VALUE interoga_VALUE, 현지어 Comandă, 게스트 ieși_program valida."""
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


def Pornește():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumente=parser_48ee4b1b.parse_args()
    Project_rădăcină=Path(__file__).resolve().parents[1];Setări={};nume_tabel={}
    if Argumente.edition:
        Country_VALUE=Argumente.edition.resolve();Setări=json.loads((Country_VALUE/'native.json').read_text());nume_tabel=Setări['identifiers'];Project_rădăcină=Country_VALUE/Setări['source']/Setări['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALUE/'native-edition.py'),'check'])
        gazdă=Country_VALUE/'host/qemu'
        if gazdă.is_file():os.environ['QEMU_AARCH64']=str(gazdă)
    Instrumente=Project_rădăcină/Path(Setări.get('runner','Instrumente/executa_comandă.py')).parent
    sys.path.insert(0,str(Instrumente))
    def Citire(Nume):
        Cale=Instrumente/(nume_tabel.get(Nume,Nume)+'.py');caz_VALUE=importlib.util.spec_from_file_location('test_'+Nume,str(Cale));modul_VALUE=importlib.util.module_from_spec(caz_VALUE);caz_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    executare_modul=Citire('executa_comandă');rețea_modul=Citire('punte_3de4fe3a');Comandă=getattr(executare_modul,nume_tabel.get('Comandă','Comandă'));punte_Tip=getattr(rețea_modul,nume_tabel.get('punte_3de4fe3a','punte_3de4fe3a'))
    alias_VALUE=Setări.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adresă_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'afișa_ajutor'})
    sys.path.insert(0,str(Project_rădăcină/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_rădăcină);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Rezultat=Argumente.output or Project_rădăcină/'build/verification/system-tools';Rezultat.mkdir(parents=True,exist_ok=True)
    raport_VALUE={'passed':False,'country':Setări.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        control_cale=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as căuta_VALUE:căuta_VALUE.bind(('127.0.0.1',0));număr_port=căuta_VALUE.getsockname()[1]
            if not 50000<=număr_port<=50007:break
        with punte_Tip(număr_port,captura=True,invitat_adresa=ipTestText('10.0.2.20'),gazdă_adresa='127.0.0.2') as punte_VALUE:
            Proces_VALUE=subprocess.Popen(Comandă()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(control_cale)]+punte_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            alege_element=selectors.DefaultSelector();alege_element.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def primi(afișa_VALUE,Pornește=0,제한=45):
                끝=time.monotonic()+제한
                while afișa_VALUE not in LOG_RECORD[Pornește:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(afișa_VALUE)+'\n'+LOG_RECORD[Pornește:].decode('utf-8','replace'))
                    for Cheie_VALUE,_ in alege_element.select(.1):
                        date=Cheie_VALUE.fileobj.read(65536)
                        if date:LOG_RECORD.extend(date)
                return LOG_RECORD[Pornește:].decode('utf-8','replace').replace('\r\n','\n')
            def trimite(date):Proces_VALUE.stdin.write(date);Proces_VALUE.stdin.flush()
            def shell(SMS):
                SMS=ipTestText(SMS)
                print(raport_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;afișa_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Pornește=len(LOG_RECORD)
                trimite((SMS+'; echo; echo '+afișa_VALUE+'\n').encode())
                termina_un_apel_marcaj=('\r\n'+afișa_VALUE+'\r\n').encode();primi(termina_un_apel_marcaj,Pornește)
                termina_un_apel_poziție=LOG_RECORD.index(termina_un_apel_marcaj,Pornește)+len(termina_un_apel_marcaj)
                primi(b'jkoros-native> ',termina_un_apel_poziție)
                return LOG_RECORD[Pornește:].decode('utf-8','replace').replace('\r\n','\n')
            def verifica(SMS,*값들):
                replică=shell(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in replică,(SMS,VALUE,replică)
                return replică
            try:
                primi(b'jkoros-native> ')
                if not Argumente.poweroff_only:
                    ajutor_VALUE=verifica('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in ajutor_VALUE,(별칭,ajutor_VALUE)
                    verifica(alias_VALUE['help']+' system','Network / system')
                    verifica('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifica(alias_VALUE['ipconfig'],'inet 10.0.2.15');verifica('ip addr show','sl0: UP');verifica('ifconfig','sl0: UP')
                    for nul_Setări in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        eroare=verifica('ipconfig set '+nul_Setări+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in eroare,eroare
                        verifica('ipconfig','inet 10.0.2.15')
                    verifica('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifica(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifica('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifica('ip link set dev sl0 down','sl0: DOWN');verifica('ping -c 1 10.0.2.2; echo STATUS=$?','eroare -100','STATUS=1')
                    verifica('ipconfig up','sl0: UP')
                    verifica(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifica('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifica('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifica(alias_VALUE['route'],'10.0.2.2 sl0')
                    verifica('ftpd start','FTP listening')
                    verifica(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');verifica('ss','LISTEN')
                    verifica('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','eroare -16')
                    with ftplib.FTP() as client_VALUE:
                        client_VALUE.connect('127.0.0.2',număr_port,timeout=20);client_VALUE.login();date=b'Network address was changed in the guest.\n'
                        client_VALUE.storbinary('STOR net-state.txt',io.BytesIO(date));RECEIVED_date=bytearray();client_VALUE.retrbinary('RETR net-state.txt',RECEIVED_date.extend);assert RECEIVED_date==date;client_VALUE.delete('net-state.txt')
                    verifica('ftpd stop','FTP stopped');verifica('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    raport_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(verifica('df','RAM only'));verifica('echo disk-proof > sys-state.txt');후=저장값(verifica(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifica('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memorie_VALUE=verifica(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorie_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verifica(alias_VALUE['ps'],'kernel/shell');verifica(alias_VALUE['uptime'],'seconds')
                    stare_info=verifica(alias_VALUE['top']+' -n 2','kernel/shell');assert stare_info.count('PID SLOT STATE')==2,stare_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifica('terminal','TERMINAL READY');Pornește=len(LOG_RECORD);trimite(b'vi process.txt\n');primi(b'NORMAL',Pornește)
                    Pornește=len(LOG_RECORD);trimite(bytes([30,2,1,0,0,0,0]));primi(b'jkoros-native> ',Pornește)
                    intrare_Listă=verifica('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',intrare_Listă);assert 찾음 and int(찾음.group(2))>0,intrare_Listă
                    verifica('free','EL0 mapped KiB: '+찾음.group(2))
                    Pornește=len(LOG_RECORD);trimite(b'top\n');primi(b'PID SLOT STATE',Pornește);trimite(b'q');primi(b'jkoros-native> ',Pornește)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        Pornește=len(LOG_RECORD);trimite((alias_VALUE['df'][:-1]+'\t\n').encode());primi(b'RAM only',Pornește);primi(b'jkoros-native> ',Pornește)
                    raport_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as control_VALUE:
                    control_VALUE.settimeout(15);control_VALUE.connect(str(control_cale));flux_VALUE=control_VALUE.makefile('rwb');json.loads(flux_VALUE.readline());flux_VALUE.write(b'{"execute":"qmp_capabilities"}\n');flux_VALUE.flush()
                    while 'return' not in json.loads(flux_VALUE.readline()):pass
                    trimite((('poweroff' if Argumente.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Eveniment=json.loads(flux_VALUE.readline())
                        if Eveniment.get('event')=='SHUTDOWN':break
                    assert Eveniment['data']['guest'] and Eveniment['data']['reason']=='guest-shutdown',Eveniment
                    assert Proces_VALUE.wait(timeout=15)==0
                    raport_VALUE['shutdown']=Eveniment;raport_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                raport_VALUE['network_trace']=punte_VALUE.jurnal_de_urmărire
                assert Argumente.poweroff_only or any(intrare_VALUE['protocol']==1 and intrare_VALUE['direction']=='from_guest' for intrare_VALUE in punte_VALUE.jurnal_de_urmărire)
                raport_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                alege_element.close();(Rezultat/'serial.log').write_bytes(LOG_RECORD);(Rezultat/'report.json').write_text(json.dumps(raport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Cheie_VALUE:VALUE for Cheie_VALUE,VALUE in raport_VALUE.items() if Cheie_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Pornește()
