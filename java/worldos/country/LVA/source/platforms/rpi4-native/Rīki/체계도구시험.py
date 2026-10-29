#!/usr/bin/env python3
"""faktisks_dati savs 커널의 IP/ICMP, Statuss_VALUE vaicāt_VALUE, 현지어 Komanda, 게스트 Iziet_programma validēt."""
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


def Palaist():
    parsētājs_48ee4b1b=argparse.ArgumentParser();parsētājs_48ee4b1b.add_argument('--edition',type=Path);parsētājs_48ee4b1b.add_argument('--output',type=Path);parsētājs_48ee4b1b.add_argument('--poweroff-only',action='store_true');Parametri=parsētājs_48ee4b1b.parse_args()
    Project_sakne=Path(__file__).resolve().parents[1];Uzstādījumi={};nosaukums_tabula={}
    if Parametri.edition:
        Kantri_VALUE=Parametri.edition.resolve();Uzstādījumi=json.loads((Kantri_VALUE/'native.json').read_text());nosaukums_tabula=Uzstādījumi['identifiers'];Project_sakne=Kantri_VALUE/Uzstādījumi['source']/Uzstādījumi['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Kantri_VALUE/'native-edition.py'),'check'])
        viesot=Kantri_VALUE/'host/qemu'
        if viesot.is_file():os.environ['QEMU_AARCH64']=str(viesot)
    Rīki=Project_sakne/Path(Uzstādījumi.get('runner','Rīki/Izpildīt_komanda.py')).parent
    sys.path.insert(0,str(Rīki))
    def Lasīt(Nosaukums):
        CEĻŠ=Rīki/(nosaukums_tabula.get(Nosaukums,Nosaukums)+'.py');līguma_vērtība=importlib.util.spec_from_file_location('test_'+Nosaukums,str(CEĻŠ));modulis_VALUE=importlib.util.module_from_spec(līguma_vērtība);līguma_vērtība.loader.exec_module(modulis_VALUE);return modulis_VALUE
    실행모듈=Lasīt('Izpildīt_komanda');tīkls_modulis=Lasīt('tilts_3de4fe3a');Komanda=getattr(실행모듈,nosaukums_tabula.get('Komanda','Komanda'));tilts_TYPE=getattr(tīkls_modulis,nosaukums_tabula.get('tilts_3de4fe3a','tilts_3de4fe3a'))
    saīsne_VALUE_0a38607b=Uzstādījumi.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adrese','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'rādīt_palīdzība'})
    sys.path.insert(0,str(Project_sakne/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_sakne);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Izvade=Parametri.output or Project_sakne/'build/verification/system-tools';Izvade.mkdir(parents=True,exist_ok=True)
    ziņot_VALUE={'passed':False,'country':Uzstādījumi.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        vadība_ceļš=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Meklēt_VALUE:Meklēt_VALUE.bind(('127.0.0.1',0));porta_numurs=Meklēt_VALUE.getsockname()[1]
            if not 50000<=porta_numurs<=50007:break
        with tilts_TYPE(porta_numurs,tvert=True,viesis_adrese=ipTestText('10.0.2.20'),viesot_adrese='127.0.0.2') as tilts_VALUE:
            Process_VALUE=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(vadība_ceļš)]+tilts_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_krājums=selectors.DefaultSelector();CHOOSE_krājums.register(Process_VALUE.stdout,selectors.EVENT_READ)
            def saņemt(rādīt_VALUE,Palaist=0,제한=45):
                끝=time.monotonic()+제한
                while rādīt_VALUE not in LOG_RECORD[Palaist:]:
                    if time.monotonic()>끝 or Process_VALUE.poll() is not None:raise AssertionError('Missing '+repr(rādīt_VALUE)+'\n'+LOG_RECORD[Palaist:].decode('utf-8','replace'))
                    for Atslēga_VALUE,_ in CHOOSE_krājums.select(.1):
                        dati=Atslēga_VALUE.fileobj.read(65536)
                        if dati:LOG_RECORD.extend(dati)
                return LOG_RECORD[Palaist:].decode('utf-8','replace').replace('\r\n','\n')
            def sūtīt(dati):Process_VALUE.stdin.write(dati);Process_VALUE.stdin.flush()
            def čaula(Teksts):
                Teksts=ipTestText(Teksts)
                print(ziņot_VALUE['country'],Teksts,flush=True);SEQUENCE_VALUE[0]+=1;rādīt_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Palaist=len(LOG_RECORD)
                sūtīt((Teksts+'; echo; echo '+rādīt_VALUE+'\n').encode())
                beigt_zvanu_marķieris=('\r\n'+rādīt_VALUE+'\r\n').encode();saņemt(beigt_zvanu_marķieris,Palaist)
                beigt_zvanu_amats=LOG_RECORD.index(beigt_zvanu_marķieris,Palaist)+len(beigt_zvanu_marķieris)
                saņemt(b'jkoros-native> ',beigt_zvanu_amats)
                return LOG_RECORD[Palaist:].decode('utf-8','replace').replace('\r\n','\n')
            def verificēt(Teksts,*값들):
                atbilde=čaula(Teksts)
                for VALUE in 값들:assert ipTestText(VALUE) in atbilde,(Teksts,VALUE,atbilde)
                return atbilde
            try:
                saņemt(b'jkoros-native> ')
                if not Parametri.poweroff_only:
                    palīdzība_VALUE=verificēt('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in saīsne_VALUE_0a38607b.values():assert 별칭 in palīdzība_VALUE,(별칭,palīdzība_VALUE)
                    verificēt(saīsne_VALUE_0a38607b['help']+' system','Network / system')
                    verificēt('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificēt(saīsne_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');verificēt('ip addr show','sl0: UP');verificēt('ifconfig','sl0: UP')
                    for nederīgs_Iestatījumi in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Kļūda=verificēt('ipconfig set '+nederīgs_Iestatījumi+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Kļūda,Kļūda
                        verificēt('ipconfig','inet 10.0.2.15')
                    verificēt('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificēt(saīsne_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificēt('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificēt('ip link set dev sl0 down','sl0: DOWN');verificēt('ping -c 1 10.0.2.2; echo STATUS=$?','Kļūda -100','STATUS=1')
                    verificēt('ipconfig up','sl0: UP')
                    verificēt(saīsne_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificēt('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificēt('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificēt(saīsne_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    verificēt('ftpd start','FTP listening')
                    verificēt(saīsne_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');verificēt('ss','LISTEN')
                    verificēt('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Kļūda -16')
                    with ftplib.FTP() as klients_VALUE:
                        klients_VALUE.connect('127.0.0.2',porta_numurs,timeout=20);klients_VALUE.login();dati=b'Network address was changed in the guest.\n'
                        klients_VALUE.storbinary('STOR net-state.txt',io.BytesIO(dati));RECEIVED_dati=bytearray();klients_VALUE.retrbinary('RETR net-state.txt',RECEIVED_dati.extend);assert RECEIVED_dati==dati;klients_VALUE.delete('net-state.txt')
                    verificēt('ftpd stop','FTP stopped');verificēt('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ziņot_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Teksts):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Teksts);assert 찾음,Teksts;return tuple(map(int,찾음.groups()))
                    전=저장값(verificēt('df','RAM only'));verificēt('echo disk-proof > sys-state.txt');후=저장값(verificēt(saīsne_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verificēt('rm sys-state.txt');assert 저장값(čaula('df'))==전
                    atmiņa_VALUE=verificēt(saīsne_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');daudzums_VALUE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',atmiņa_VALUE).groups()));assert 0<daudzums_VALUE[1]<=daudzums_VALUE[0] and daudzums_VALUE[1]+daudzums_VALUE[2]==daudzums_VALUE[0]
                    verificēt(saīsne_VALUE_0a38607b['ps'],'kernel/shell');verificēt(saīsne_VALUE_0a38607b['uptime'],'seconds')
                    statuss_informācija=verificēt(saīsne_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert statuss_informācija.count('PID SLOT STATE')==2,statuss_informācija
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificēt('terminal','TERMINAL READY');Palaist=len(LOG_RECORD);sūtīt(b'vi process.txt\n');saņemt(b'NORMAL',Palaist)
                    Palaist=len(LOG_RECORD);sūtīt(bytes([30,2,1,0,0,0,0]));saņemt(b'jkoros-native> ',Palaist)
                    ievade_Saraksts=verificēt('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ievade_Saraksts);assert 찾음 and int(찾음.group(2))>0,ievade_Saraksts
                    verificēt('free','EL0 mapped KiB: '+찾음.group(2))
                    Palaist=len(LOG_RECORD);sūtīt(b'top\n');saņemt(b'PID SLOT STATE',Palaist);sūtīt(b'q');saņemt(b'jkoros-native> ',Palaist)
                    # Test a multibyte prefix through the real shell completion path.
                    if saīsne_VALUE_0a38607b['df']!='df':
                        Palaist=len(LOG_RECORD);sūtīt((saīsne_VALUE_0a38607b['df'][:-1]+'\t\n').encode());saņemt(b'RAM only',Palaist);saņemt(b'jkoros-native> ',Palaist)
                    ziņot_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as vadība_VALUE:
                    vadība_VALUE.settimeout(15);vadība_VALUE.connect(str(vadība_ceļš));Stream_VALUE=vadība_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    sūtīt((('poweroff' if Parametri.poweroff_only else saīsne_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Notikums=json.loads(Stream_VALUE.readline())
                        if Notikums.get('event')=='SHUTDOWN':break
                    assert Notikums['data']['guest'] and Notikums['data']['reason']=='guest-shutdown',Notikums
                    assert Process_VALUE.wait(timeout=15)==0
                    ziņot_VALUE['shutdown']=Notikums;ziņot_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ziņot_VALUE['network_trace']=tilts_VALUE.trasēšanas_žurnāls
                assert Parametri.poweroff_only or any(ievade_VALUE['protocol']==1 and ievade_VALUE['direction']=='from_guest' for ievade_VALUE in tilts_VALUE.trasēšanas_žurnāls)
                ziņot_VALUE['passed']=True
            finally:
                if Process_VALUE.poll() is None:os.killpg(Process_VALUE.pid,signal.SIGTERM)
                try:Process_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Process_VALUE.kill();Process_VALUE.wait()
                CHOOSE_krājums.close();(Izvade/'serial.log').write_bytes(LOG_RECORD);(Izvade/'report.json').write_text(json.dumps(ziņot_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Atslēga_VALUE:VALUE for Atslēga_VALUE,VALUE in ziņot_VALUE.items() if Atslēga_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Palaist()
