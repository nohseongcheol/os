#!/usr/bin/env python3
"""aktual_të_dhëna 자체 커널의 IP/ICMP, status_VALUE pyetja_VALUE, 현지어 Komanda, 게스트 dal_program vlerësoj."""
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


def Ekzekuto():
    analizues_48ee4b1b=argparse.ArgumentParser();analizues_48ee4b1b.add_argument('--edition',type=Path);analizues_48ee4b1b.add_argument('--output',type=Path);analizues_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumente=analizues_48ee4b1b.parse_args()
    Project_rrënjë=Path(__file__).resolve().parents[1];Rregullime={};emër_tabelë={}
    if Argumente.edition:
        나라=Argumente.edition.resolve();Rregullime=json.loads((나라/'native.json').read_text());emër_tabelë=Rregullime['identifiers'];Project_rrënjë=나라/Rregullime['source']/Rregullime['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        pritës=나라/'host/qemu'
        if pritës.is_file():os.environ['QEMU_AARCH64']=str(pritës)
    Mjete=Project_rrënjë/Path(Rregullime.get('runner','Mjete/zbatoj_komandë.py')).parent
    sys.path.insert(0,str(Mjete))
    def Leximi(Emër):
        POZICIONI=Mjete/(emër_tabelë.get(Emër,Emër)+'.py');punë_VALUE=importlib.util.spec_from_file_location('test_'+Emër,str(POZICIONI));modul_VALUE=importlib.util.module_from_spec(punë_VALUE);punë_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Leximi('zbatoj_komandë');rrjet_modul=Leximi('rrjet_urë');Komanda=getattr(실행모듈,emër_tabelë.get('Komanda','Komanda'));urë_TYPE=getattr(rrjet_modul,emër_tabelë.get('rrjet_urë','rrjet_urë'))
    pseudonim_VALUE=Rregullime.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'Adresa_e_IP_së','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'shfaq_ndihmë'})
    sys.path.insert(0,str(Project_rrënjë/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_rrënjë);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=Argumente.output or Project_rrënjë/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    raport_VALUE={'passed':False,'country':Rregullime.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontroll_shteg=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Kërkim_VALUE:Kërkim_VALUE.bind(('127.0.0.1',0));numri_i_portës=Kërkim_VALUE.getsockname()[1]
            if not 50000<=numri_i_portës<=50007:break
        with urë_TYPE(numri_i_portës,kap=True,i_ftuar_email=ipTestText('10.0.2.20'),pritës_email='127.0.0.2') as urë_VALUE:
            Proces_VALUE=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontroll_shteg)]+urë_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_njësi=selectors.DefaultSelector();CHOOSE_njësi.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def 받기(shfaq_VALUE,Ekzekuto=0,제한=45):
                끝=time.monotonic()+제한
                while shfaq_VALUE not in LOG_RECORD[Ekzekuto:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(shfaq_VALUE)+'\n'+LOG_RECORD[Ekzekuto:].decode('utf-8','replace'))
                    for tast_VALUE,_ in CHOOSE_njësi.select(.1):
                        të_dhëna=tast_VALUE.fileobj.read(65536)
                        if të_dhëna:LOG_RECORD.extend(të_dhëna)
                return LOG_RECORD[Ekzekuto:].decode('utf-8','replace').replace('\r\n','\n')
            def dërgoj(të_dhëna):Proces_VALUE.stdin.write(të_dhëna);Proces_VALUE.stdin.flush()
            def pasues(Teksti):
                Teksti=ipTestText(Teksti)
                print(raport_VALUE['country'],Teksti,flush=True);SEQUENCE_VALUE[0]+=1;shfaq_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Ekzekuto=len(LOG_RECORD)
                dërgoj((Teksti+'; echo; echo '+shfaq_VALUE+'\n').encode())
                끝표시=('\r\n'+shfaq_VALUE+'\r\n').encode();받기(끝표시,Ekzekuto)
                mbaroj_pozicioni=LOG_RECORD.index(끝표시,Ekzekuto)+len(끝표시)
                받기(b'jkoros-native> ',mbaroj_pozicioni)
                return LOG_RECORD[Ekzekuto:].decode('utf-8','replace').replace('\r\n','\n')
            def verifikoj(Teksti,*값들):
                replikë=pasues(Teksti)
                for VALUE in 값들:assert ipTestText(VALUE) in replikë,(Teksti,VALUE,replikë)
                return replikë
            try:
                받기(b'jkoros-native> ')
                if not Argumente.poweroff_only:
                    ndihmë_VALUE=verifikoj('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in pseudonim_VALUE.values():assert 별칭 in ndihmë_VALUE,(별칭,ndihmë_VALUE)
                    verifikoj(pseudonim_VALUE['help']+' system','Network / system')
                    verifikoj('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifikoj(pseudonim_VALUE['ipconfig'],'inet 10.0.2.15');verifikoj('ip addr show','sl0: UP');verifikoj('ifconfig','sl0: UP')
                    for i_pavlefshëm_cilësimet in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        GABIM=verifikoj('ipconfig set '+i_pavlefshëm_cilësimet+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in GABIM,GABIM
                        verifikoj('ipconfig','inet 10.0.2.15')
                    verifikoj('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifikoj(pseudonim_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifikoj('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifikoj('ip link set dev sl0 down','sl0: DOWN');verifikoj('ping -c 1 10.0.2.2; echo STATUS=$?','GABIM -100','STATUS=1')
                    verifikoj('ipconfig up','sl0: UP')
                    verifikoj(pseudonim_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifikoj('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifikoj('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifikoj(pseudonim_VALUE['route'],'10.0.2.2 sl0')
                    verifikoj('ftpd start','FTP listening')
                    verifikoj(pseudonim_VALUE['netstat'],'10.0.2.20:21','LISTEN');verifikoj('ss','LISTEN')
                    verifikoj('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','GABIM -16')
                    with ftplib.FTP() as klient_VALUE:
                        klient_VALUE.connect('127.0.0.2',numri_i_portës,timeout=20);klient_VALUE.login();të_dhëna=b'Network address was changed in the guest.\n'
                        klient_VALUE.storbinary('STOR net-state.txt',io.BytesIO(të_dhëna));RECEIVED_të_dhëna=bytearray();klient_VALUE.retrbinary('RETR net-state.txt',RECEIVED_të_dhëna.extend);assert RECEIVED_të_dhëna==të_dhëna;klient_VALUE.delete('net-state.txt')
                    verifikoj('ftpd stop','FTP stopped');verifikoj('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    raport_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Teksti):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Teksti);assert 찾음,Teksti;return tuple(map(int,찾음.groups()))
                    전=저장값(verifikoj('df','RAM only'));verifikoj('echo disk-proof > sys-state.txt');후=저장값(verifikoj(pseudonim_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifikoj('rm sys-state.txt');assert 저장값(pasues('df'))==전
                    Memorie_VALUE=verifikoj(pseudonim_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorie_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verifikoj(pseudonim_VALUE['ps'],'kernel/shell');verifikoj(pseudonim_VALUE['uptime'],'seconds')
                    status_informacion=verifikoj(pseudonim_VALUE['top']+' -n 2','kernel/shell');assert status_informacion.count('PID SLOT STATE')==2,status_informacion
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifikoj('terminal','TERMINAL READY');Ekzekuto=len(LOG_RECORD);dërgoj(b'vi process.txt\n');받기(b'NORMAL',Ekzekuto)
                    Ekzekuto=len(LOG_RECORD);dërgoj(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Ekzekuto)
                    futje_Listë=verifikoj('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',futje_Listë);assert 찾음 and int(찾음.group(2))>0,futje_Listë
                    verifikoj('free','EL0 mapped KiB: '+찾음.group(2))
                    Ekzekuto=len(LOG_RECORD);dërgoj(b'top\n');받기(b'PID SLOT STATE',Ekzekuto);dërgoj(b'q');받기(b'jkoros-native> ',Ekzekuto)
                    # Test a multibyte prefix through the real shell completion path.
                    if pseudonim_VALUE['df']!='df':
                        Ekzekuto=len(LOG_RECORD);dërgoj((pseudonim_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Ekzekuto);받기(b'jkoros-native> ',Ekzekuto)
                    raport_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontroll_VALUE:
                    kontroll_VALUE.settimeout(15);kontroll_VALUE.connect(str(kontroll_shteg));Stream_VALUE=kontroll_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    dërgoj((('poweroff' if Argumente.poweroff_only else pseudonim_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Ngjarje=json.loads(Stream_VALUE.readline())
                        if Ngjarje.get('event')=='SHUTDOWN':break
                    assert Ngjarje['data']['guest'] and Ngjarje['data']['reason']=='guest-shutdown',Ngjarje
                    assert Proces_VALUE.wait(timeout=15)==0
                    raport_VALUE['shutdown']=Ngjarje;raport_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                raport_VALUE['network_trace']=urë_VALUE.gjurmë_LOG
                assert Argumente.poweroff_only or any(futje_VALUE['protocol']==1 and futje_VALUE['direction']=='from_guest' for futje_VALUE in urë_VALUE.gjurmë_LOG)
                raport_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                CHOOSE_njësi.close();(출력/'serial.log').write_bytes(LOG_RECORD);(출력/'report.json').write_text(json.dumps(raport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tast_VALUE:VALUE for tast_VALUE,VALUE in raport_VALUE.items() if tast_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Ekzekuto()
