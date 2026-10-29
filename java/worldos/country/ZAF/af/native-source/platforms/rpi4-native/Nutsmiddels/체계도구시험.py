#!/usr/bin/env python3
"""werklik_data 자체 커널의 IP/ICMP, stand_VALUE navraag_VALUE, 현지어 Opdrag, 게스트 Verlaat_program valideer."""
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


def Loop():
    ontleder_48ee4b1b=argparse.ArgumentParser();ontleder_48ee4b1b.add_argument('--edition',type=Path);ontleder_48ee4b1b.add_argument('--output',type=Path);ontleder_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=ontleder_48ee4b1b.parse_args()
    Project_wortel=Path(__file__).resolve().parents[1];Instellings={};naam_tabel={}
    if 인수.edition:
        나라=인수.edition.resolve();Instellings=json.loads((나라/'native.json').read_text());naam_tabel=Instellings['identifiers'];Project_wortel=나라/Instellings['source']/Instellings['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        hou=나라/'host/qemu'
        if hou.is_file():os.environ['QEMU_AARCH64']=str(hou)
    Nutsmiddels=Project_wortel/Path(Instellings.get('runner','Nutsmiddels/uitvoer_bevel.py')).parent
    sys.path.insert(0,str(Nutsmiddels))
    def Lees(Naam):
        Pad=Nutsmiddels/(naam_tabel.get(Naam,Naam)+'.py');saak_VALUE=importlib.util.spec_from_file_location('test_'+Naam,str(Pad));module_VALUE=importlib.util.module_from_spec(saak_VALUE);saak_VALUE.loader.exec_module(module_VALUE);return module_VALUE
    실행모듈=Lees('uitvoer_bevel');Netwerk_module=Lees('Netwerk_brug');Opdrag=getattr(실행모듈,naam_tabel.get('Opdrag','Opdrag'));brug_TYPE=getattr(Netwerk_module,naam_tabel.get('Netwerk_brug','Netwerk_brug'))
    alias_VALUE=Instellings.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adres','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'wys_hulp'})
    sys.path.insert(0,str(Project_wortel/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_wortel);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Afvoer=인수.output or Project_wortel/'build/verification/system-tools';Afvoer.mkdir(parents=True,exist_ok=True)
    verslag_VALUE={'passed':False,'country':Instellings.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_ry=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrole_pad=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Soek_VALUE:Soek_VALUE.bind(('127.0.0.1',0));접속번호=Soek_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with brug_TYPE(접속번호,lê_vas=True,gas_adres=ipTestText('10.0.2.20'),hou_adres='127.0.0.2') as brug_VALUE:
            Proses_VALUE=subprocess.Popen(Opdrag()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrole_pad)]+brug_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            kies_item=selectors.DefaultSelector();kies_item.register(Proses_VALUE.stdout,selectors.EVENT_READ)
            def 받기(wys_VALUE,Loop=0,제한=45):
                끝=time.monotonic()+제한
                while wys_VALUE not in LOG_ry[Loop:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:raise AssertionError('Missing '+repr(wys_VALUE)+'\n'+LOG_ry[Loop:].decode('utf-8','replace'))
                    for Sleutel_VALUE,_ in kies_item.select(.1):
                        data=Sleutel_VALUE.fileobj.read(65536)
                        if data:LOG_ry.extend(data)
                return LOG_ry[Loop:].decode('utf-8','replace').replace('\r\n','\n')
            def e_pos(data):Proses_VALUE.stdin.write(data);Proses_VALUE.stdin.flush()
            def dop(Teks):
                Teks=ipTestText(Teks)
                print(verslag_VALUE['country'],Teks,flush=True);SEQUENCE_VALUE[0]+=1;wys_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Loop=len(LOG_ry)
                e_pos((Teks+'; echo; echo '+wys_VALUE+'\n').encode())
                끝표시=('\r\n'+wys_VALUE+'\r\n').encode();받기(끝표시,Loop)
                beëindig_plaas=LOG_ry.index(끝표시,Loop)+len(끝표시)
                받기(b'jkoros-native> ',beëindig_plaas)
                return LOG_ry[Loop:].decode('utf-8','replace').replace('\r\n','\n')
            def verifieer(Teks,*값들):
                antwoord=dop(Teks)
                for VALUE in 값들:assert ipTestText(VALUE) in antwoord,(Teks,VALUE,antwoord)
                return antwoord
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    hulp_VALUE=verifieer('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in hulp_VALUE,(별칭,hulp_VALUE)
                    verifieer(alias_VALUE['help']+' system','Network / system')
                    verifieer('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifieer(alias_VALUE['ipconfig'],'inet 10.0.2.15');verifieer('ip addr show','sl0: UP');verifieer('ifconfig','sl0: UP')
                    for ongeldig_Instellings in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Fout=verifieer('ipconfig set '+ongeldig_Instellings+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Fout,Fout
                        verifieer('ipconfig','inet 10.0.2.15')
                    verifieer('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifieer(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifieer('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifieer('ip link set dev sl0 down','sl0: DOWN');verifieer('ping -c 1 10.0.2.2; echo STATUS=$?','Fout -100','STATUS=1')
                    verifieer('ipconfig up','sl0: UP')
                    verifieer(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifieer('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifieer('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifieer(alias_VALUE['route'],'10.0.2.2 sl0')
                    verifieer('ftpd start','FTP listening')
                    verifieer(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');verifieer('ss','LISTEN')
                    verifieer('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Fout -16')
                    with ftplib.FTP() as kliënt_VALUE:
                        kliënt_VALUE.connect('127.0.0.2',접속번호,timeout=20);kliënt_VALUE.login();data=b'Network address was changed in the guest.\n'
                        kliënt_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();kliënt_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;kliënt_VALUE.delete('net-state.txt')
                    verifieer('ftpd stop','FTP stopped');verifieer('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    verslag_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Teks):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Teks);assert 찾음,Teks;return tuple(map(int,찾음.groups()))
                    전=저장값(verifieer('df','RAM only'));verifieer('echo disk-proof > sys-state.txt');후=저장값(verifieer(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifieer('rm sys-state.txt');assert 저장값(dop('df'))==전
                    Geheue_VALUE=verifieer(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Geheue_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verifieer(alias_VALUE['ps'],'kernel/shell');verifieer(alias_VALUE['uptime'],'seconds')
                    stand_inligting=verifieer(alias_VALUE['top']+' -n 2','kernel/shell');assert stand_inligting.count('PID SLOT STATE')==2,stand_inligting
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifieer('terminal','TERMINAL READY');Loop=len(LOG_ry);e_pos(b'vi process.txt\n');받기(b'NORMAL',Loop)
                    Loop=len(LOG_ry);e_pos(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Loop)
                    inskrywing_Lys=verifieer('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',inskrywing_Lys);assert 찾음 and int(찾음.group(2))>0,inskrywing_Lys
                    verifieer('free','EL0 mapped KiB: '+찾음.group(2))
                    Loop=len(LOG_ry);e_pos(b'top\n');받기(b'PID SLOT STATE',Loop);e_pos(b'q');받기(b'jkoros-native> ',Loop)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        Loop=len(LOG_ry);e_pos((alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Loop);받기(b'jkoros-native> ',Loop)
                    verslag_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrole_VALUE:
                    kontrole_VALUE.settimeout(15);kontrole_VALUE.connect(str(kontrole_pad));Stream_VALUE=kontrole_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    e_pos((('poweroff' if 인수.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        gebeurtenis=json.loads(Stream_VALUE.readline())
                        if gebeurtenis.get('event')=='SHUTDOWN':break
                    assert gebeurtenis['data']['guest'] and gebeurtenis['data']['reason']=='guest-shutdown',gebeurtenis
                    assert Proses_VALUE.wait(timeout=15)==0
                    verslag_VALUE['shutdown']=gebeurtenis;verslag_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                verslag_VALUE['network_trace']=brug_VALUE.spoor_LOG
                assert 인수.poweroff_only or any(inskrywing_VALUE['protocol']==1 and inskrywing_VALUE['direction']=='from_guest' for inskrywing_VALUE in brug_VALUE.spoor_LOG)
                verslag_VALUE['passed']=True
            finally:
                if Proses_VALUE.poll() is None:os.killpg(Proses_VALUE.pid,signal.SIGTERM)
                try:Proses_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
                kies_item.close();(Afvoer/'serial.log').write_bytes(LOG_ry);(Afvoer/'report.json').write_text(json.dumps(verslag_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Sleutel_VALUE:VALUE for Sleutel_VALUE,VALUE in verslag_VALUE.items() if Sleutel_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Loop()
