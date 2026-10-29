#!/usr/bin/env python3
"""aktuell_Daten 자체 커널의 IP/ICMP, Status_VALUE Requête_VALUE, 현지어 Befeel, 게스트 Schluss_App validéieren."""
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


def Laf():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    projezéieren_Racinn=Path(__file__).resolve().parents[1];Astellungen={};Numm_Tabell={}
    if 인수.edition:
        나라=인수.edition.resolve();Astellungen=json.loads((나라/'native.json').read_text());Numm_Tabell=Astellungen['identifiers'];projezéieren_Racinn=나라/Astellungen['source']/Astellungen['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        Host=나라/'host/qemu'
        if Host.is_file():os.environ['QEMU_AARCH64']=str(Host)
    Tools=projezéieren_Racinn/Path(Astellungen.get('runner','Tools/ausféieren_Befeel.py')).parent
    sys.path.insert(0,str(Tools))
    def 읽기(Numm):
        Wee=Tools/(Numm_Tabell.get(Numm,Numm)+'.py');Job_VALUE=importlib.util.spec_from_file_location('test_'+Numm,str(Wee));Modüll_VALUE=importlib.util.module_from_spec(Job_VALUE);Job_VALUE.loader.exec_module(Modüll_VALUE);return Modüll_VALUE
    실행모듈=읽기('ausféieren_Befeel');Reseau_Modüll=읽기('Reseau_Bréck');Befeel=getattr(실행모듈,Numm_Tabell.get('Befeel','Befeel'));Bréck_TYPE=getattr(Reseau_Modüll,Numm_Tabell.get('Reseau_Bréck','Reseau_Bréck'))
    Alias_VALUE=Astellungen.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_Adress','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'Show_Hëllef'})
    sys.path.insert(0,str(projezéieren_Racinn/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(projezéieren_Racinn);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or projezéieren_Racinn/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    mellen_VALUE={'passed':False,'country':Astellungen.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_Rei=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        Kontroll_Wee=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Sich_VALUE:Sich_VALUE.bind(('127.0.0.1',0));접속번호=Sich_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with Bréck_TYPE(접속번호,ophuelen=True,Gaascht_Adress=ipTestText('10.0.2.20'),Host_Adress='127.0.0.2') as Bréck_VALUE:
            Prozess_VALUE=subprocess.Popen(Befeel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(Kontroll_Wee)]+Bréck_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_Element=selectors.DefaultSelector();CHOOSE_Element.register(Prozess_VALUE.stdout,selectors.EVENT_READ)
            def 받기(Show_VALUE,Laf=0,제한=45):
                끝=time.monotonic()+제한
                while Show_VALUE not in LOG_Rei[Laf:]:
                    if time.monotonic()>끝 or Prozess_VALUE.poll() is not None:raise AssertionError('Missing '+repr(Show_VALUE)+'\n'+LOG_Rei[Laf:].decode('utf-8','replace'))
                    for Tast_VALUE,_ in CHOOSE_Element.select(.1):
                        Daten=Tast_VALUE.fileobj.read(65536)
                        if Daten:LOG_Rei.extend(Daten)
                return LOG_Rei[Laf:].decode('utf-8','replace').replace('\r\n','\n')
            def mailen(Daten):Prozess_VALUE.stdin.write(Daten);Prozess_VALUE.stdin.flush()
            def Shell(SMS):
                SMS=ipTestText(SMS)
                print(mellen_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;Show_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Laf=len(LOG_Rei)
                mailen((SMS+'; echo; echo '+Show_VALUE+'\n').encode())
                bëennegen_Markéierung=('\r\n'+Show_VALUE+'\r\n').encode();받기(bëennegen_Markéierung,Laf)
                bëennegen_positionéieren=LOG_Rei.index(bëennegen_Markéierung,Laf)+len(bëennegen_Markéierung)
                받기(b'jkoros-native> ',bëennegen_positionéieren)
                return LOG_Rei[Laf:].decode('utf-8','replace').replace('\r\n','\n')
            def verifizéieren(SMS,*값들):
                äntweren=Shell(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in äntweren,(SMS,VALUE,äntweren)
                return äntweren
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    Hëllef_VALUE=verifizéieren('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in Alias_VALUE.values():assert 별칭 in Hëllef_VALUE,(별칭,Hëllef_VALUE)
                    verifizéieren(Alias_VALUE['help']+' system','Network / system')
                    verifizéieren('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifizéieren(Alias_VALUE['ipconfig'],'inet 10.0.2.15');verifizéieren('ip addr show','sl0: UP');verifizéieren('ifconfig','sl0: UP')
                    for ongëlteg_Astellungen in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Feeler=verifizéieren('ipconfig set '+ongëlteg_Astellungen+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Feeler,Feeler
                        verifizéieren('ipconfig','inet 10.0.2.15')
                    verifizéieren('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifizéieren(Alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifizéieren('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifizéieren('ip link set dev sl0 down','sl0: DOWN');verifizéieren('ping -c 1 10.0.2.2; echo STATUS=$?','Feeler -100','STATUS=1')
                    verifizéieren('ipconfig up','sl0: UP')
                    verifizéieren(Alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifizéieren('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifizéieren('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifizéieren(Alias_VALUE['route'],'10.0.2.2 sl0')
                    verifizéieren('ftpd start','FTP listening')
                    verifizéieren(Alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');verifizéieren('ss','LISTEN')
                    verifizéieren('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Feeler -16')
                    with ftplib.FTP() as Client_VALUE:
                        Client_VALUE.connect('127.0.0.2',접속번호,timeout=20);Client_VALUE.login();Daten=b'Network address was changed in the guest.\n'
                        Client_VALUE.storbinary('STOR net-state.txt',io.BytesIO(Daten));RECEIVED_Daten=bytearray();Client_VALUE.retrbinary('RETR net-state.txt',RECEIVED_Daten.extend);assert RECEIVED_Daten==Daten;Client_VALUE.delete('net-state.txt')
                    verifizéieren('ftpd stop','FTP stopped');verifizéieren('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    mellen_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(verifizéieren('df','RAM only'));verifizéieren('echo disk-proof > sys-state.txt');후=저장값(verifizéieren(Alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifizéieren('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Späicher_VALUE=verifizéieren(Alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Späicher_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verifizéieren(Alias_VALUE['ps'],'kernel/shell');verifizéieren(Alias_VALUE['uptime'],'seconds')
                    Status_Info=verifizéieren(Alias_VALUE['top']+' -n 2','kernel/shell');assert Status_Info.count('PID SLOT STATE')==2,Status_Info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifizéieren('terminal','TERMINAL READY');Laf=len(LOG_Rei);mailen(b'vi process.txt\n');받기(b'NORMAL',Laf)
                    Laf=len(LOG_Rei);mailen(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Laf)
                    Agab_Lëscht=verifizéieren('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',Agab_Lëscht);assert 찾음 and int(찾음.group(2))>0,Agab_Lëscht
                    verifizéieren('free','EL0 mapped KiB: '+찾음.group(2))
                    Laf=len(LOG_Rei);mailen(b'top\n');받기(b'PID SLOT STATE',Laf);mailen(b'q');받기(b'jkoros-native> ',Laf)
                    # Test a multibyte prefix through the real shell completion path.
                    if Alias_VALUE['df']!='df':
                        Laf=len(LOG_Rei);mailen((Alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Laf);받기(b'jkoros-native> ',Laf)
                    mellen_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as Kontroll_VALUE:
                    Kontroll_VALUE.settimeout(15);Kontroll_VALUE.connect(str(Kontroll_Wee));Stream_VALUE=Kontroll_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    mailen((('poweroff' if 인수.poweroff_only else Alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Evenement=json.loads(Stream_VALUE.readline())
                        if Evenement.get('event')=='SHUTDOWN':break
                    assert Evenement['data']['guest'] and Evenement['data']['reason']=='guest-shutdown',Evenement
                    assert Prozess_VALUE.wait(timeout=15)==0
                    mellen_VALUE['shutdown']=Evenement;mellen_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                mellen_VALUE['network_trace']=Bréck_VALUE.추적기록
                assert 인수.poweroff_only or any(Agab_VALUE['protocol']==1 and Agab_VALUE['direction']=='from_guest' for Agab_VALUE in Bréck_VALUE.추적기록)
                mellen_VALUE['passed']=True
            finally:
                if Prozess_VALUE.poll() is None:os.killpg(Prozess_VALUE.pid,signal.SIGTERM)
                try:Prozess_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Prozess_VALUE.kill();Prozess_VALUE.wait()
                CHOOSE_Element.close();(출력/'serial.log').write_bytes(LOG_Rei);(출력/'report.json').write_text(json.dumps(mellen_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Tast_VALUE:VALUE for Tast_VALUE,VALUE in mellen_VALUE.items() if Tast_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Laf()
