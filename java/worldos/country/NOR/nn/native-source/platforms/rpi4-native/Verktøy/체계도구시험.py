#!/usr/bin/env python3
"""faktisk_data 자체 커널의 IP/ICMP, status_VALUE spørjing_VALUE, 현지어 Kommando, 게스트 Utgang_app bekrefte."""
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


def Køyr_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');Argument=해석기.parse_args()
    spegle_rot=Path(__file__).resolve().parents[1];Innstillingar={};namn_tabell={}
    if Argument.edition:
        나라=Argument.edition.resolve();Innstillingar=json.loads((나라/'native.json').read_text());namn_tabell=Innstillingar['identifiers'];spegle_rot=나라/Innstillingar['source']/Innstillingar['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        vert=나라/'host/qemu'
        if vert.is_file():os.environ['QEMU_AARCH64']=str(vert)
    Verktøy=spegle_rot/Path(Innstillingar.get('runner','Verktøy/Utfør_kommando.py')).parent
    sys.path.insert(0,str(Verktøy))
    def Les(Namn):
        STIGE=Verktøy/(namn_tabell.get(Namn,Namn)+'.py');sak_VALUE=importlib.util.spec_from_file_location('test_'+Namn,str(STIGE));modul_VALUE=importlib.util.module_from_spec(sak_VALUE);sak_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Les('Utfør_kommando');Nettverk_modul=Les('Nettverk_bru');Kommando=getattr(실행모듈,namn_tabell.get('Kommando','Kommando'));bru_TYPE=getattr(Nettverk_modul,namn_tabell.get('Nettverk_bru','Nettverk_bru'))
    alias_VALUE=Innstillingar.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresse','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'vise_hjelp'})
    sys.path.insert(0,str(spegle_rot/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(spegle_rot);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Utdata=Argument.output or spegle_rot/'build/verification/system-tools';Utdata.mkdir(parents=True,exist_ok=True)
    rapport_VALUE={'passed':False,'country':Innstillingar.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_rad=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        styring_bane=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Søk_VALUE:Søk_VALUE.bind(('127.0.0.1',0));portnummer=Søk_VALUE.getsockname()[1]
            if not 50000<=portnummer<=50007:break
        with bru_TYPE(portnummer,ta_opp=True,gjest_ADDRESS=ipTestText('10.0.2.20'),vert_ADDRESS='127.0.0.2') as bru_VALUE:
            Prosess_VALUE=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(styring_bane)]+bru_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            velje_vare=selectors.DefaultSelector();velje_vare.register(Prosess_VALUE.stdout,selectors.EVENT_READ)
            def 받기(vise_VALUE_487749b8,Køyr_2=0,제한=45):
                끝=time.monotonic()+제한
                while vise_VALUE_487749b8 not in LOG_rad[Køyr_2:]:
                    if time.monotonic()>끝 or Prosess_VALUE.poll() is not None:raise AssertionError('Missing '+repr(vise_VALUE_487749b8)+'\n'+LOG_rad[Køyr_2:].decode('utf-8','replace'))
                    for tast_VALUE,_ in velje_vare.select(.1):
                        data=tast_VALUE.fileobj.read(65536)
                        if data:LOG_rad.extend(data)
                return LOG_rad[Køyr_2:].decode('utf-8','replace').replace('\r\n','\n')
            def sende(data):Prosess_VALUE.stdin.write(data);Prosess_VALUE.stdin.flush()
            def grensesnitt(Tekst):
                Tekst=ipTestText(Tekst)
                print(rapport_VALUE['country'],Tekst,flush=True);SEQUENCE_VALUE[0]+=1;vise_VALUE_487749b8='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Køyr_2=len(LOG_rad)
                sende((Tekst+'; echo; echo '+vise_VALUE_487749b8+'\n').encode())
                끝표시=('\r\n'+vise_VALUE_487749b8+'\r\n').encode();받기(끝표시,Køyr_2)
                avslutte_plassere=LOG_rad.index(끝표시,Køyr_2)+len(끝표시)
                받기(b'jkoros-native> ',avslutte_plassere)
                return LOG_rad[Køyr_2:].decode('utf-8','replace').replace('\r\n','\n')
            def stadfeste(Tekst,*값들):
                svare=grensesnitt(Tekst)
                for VALUE in 값들:assert ipTestText(VALUE) in svare,(Tekst,VALUE,svare)
                return svare
            try:
                받기(b'jkoros-native> ')
                if not Argument.poweroff_only:
                    hjelp_VALUE=stadfeste('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in hjelp_VALUE,(별칭,hjelp_VALUE)
                    stadfeste(alias_VALUE['help']+' system','Network / system')
                    stadfeste('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    stadfeste(alias_VALUE['ipconfig'],'inet 10.0.2.15');stadfeste('ip addr show','sl0: UP');stadfeste('ifconfig','sl0: UP')
                    for ugyldig_Innstillingar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        FEIL=stadfeste('ipconfig set '+ugyldig_Innstillingar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in FEIL,FEIL
                        stadfeste('ipconfig','inet 10.0.2.15')
                    stadfeste('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    stadfeste(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    stadfeste('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    stadfeste('ip link set dev sl0 down','sl0: DOWN');stadfeste('ping -c 1 10.0.2.2; echo STATUS=$?','FEIL -100','STATUS=1')
                    stadfeste('ipconfig up','sl0: UP')
                    stadfeste(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    stadfeste('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    stadfeste('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');stadfeste(alias_VALUE['route'],'10.0.2.2 sl0')
                    stadfeste('ftpd start','FTP listening')
                    stadfeste(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');stadfeste('ss','LISTEN')
                    stadfeste('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','FEIL -16')
                    with ftplib.FTP() as klient_VALUE:
                        klient_VALUE.connect('127.0.0.2',portnummer,timeout=20);klient_VALUE.login();data=b'Network address was changed in the guest.\n'
                        klient_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();klient_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;klient_VALUE.delete('net-state.txt')
                    stadfeste('ftpd stop','FTP stopped');stadfeste('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    rapport_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(stadfeste('df','RAM only'));stadfeste('echo disk-proof > sys-state.txt');후=저장값(stadfeste(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    stadfeste('rm sys-state.txt');assert 저장값(grensesnitt('df'))==전
                    Minne_VALUE=stadfeste(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Minne_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    stadfeste(alias_VALUE['ps'],'kernel/shell');stadfeste(alias_VALUE['uptime'],'seconds')
                    merkje_informasjon=stadfeste(alias_VALUE['top']+' -n 2','kernel/shell');assert merkje_informasjon.count('PID SLOT STATE')==2,merkje_informasjon
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    stadfeste('terminal','TERMINAL READY');Køyr_2=len(LOG_rad);sende(b'vi process.txt\n');받기(b'NORMAL',Køyr_2)
                    Køyr_2=len(LOG_rad);sende(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Køyr_2)
                    oppføring_Liste=stadfeste('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',oppføring_Liste);assert 찾음 and int(찾음.group(2))>0,oppføring_Liste
                    stadfeste('free','EL0 mapped KiB: '+찾음.group(2))
                    Køyr_2=len(LOG_rad);sende(b'top\n');받기(b'PID SLOT STATE',Køyr_2);sende(b'q');받기(b'jkoros-native> ',Køyr_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        Køyr_2=len(LOG_rad);sende((alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Køyr_2);받기(b'jkoros-native> ',Køyr_2)
                    rapport_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as styring_VALUE:
                    styring_VALUE.settimeout(15);styring_VALUE.connect(str(styring_bane));Stream_VALUE=styring_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    sende((('poweroff' if Argument.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Hending=json.loads(Stream_VALUE.readline())
                        if Hending.get('event')=='SHUTDOWN':break
                    assert Hending['data']['guest'] and Hending['data']['reason']=='guest-shutdown',Hending
                    assert Prosess_VALUE.wait(timeout=15)==0
                    rapport_VALUE['shutdown']=Hending;rapport_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                rapport_VALUE['network_trace']=bru_VALUE.spor_LOG
                assert Argument.poweroff_only or any(oppføring_VALUE['protocol']==1 and oppføring_VALUE['direction']=='from_guest' for oppføring_VALUE in bru_VALUE.spor_LOG)
                rapport_VALUE['passed']=True
            finally:
                if Prosess_VALUE.poll() is None:os.killpg(Prosess_VALUE.pid,signal.SIGTERM)
                try:Prosess_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Prosess_VALUE.kill();Prosess_VALUE.wait()
                velje_vare.close();(Utdata/'serial.log').write_bytes(LOG_rad);(Utdata/'report.json').write_text(json.dumps(rapport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tast_VALUE:VALUE for tast_VALUE,VALUE in rapport_VALUE.items() if tast_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Køyr_2()
