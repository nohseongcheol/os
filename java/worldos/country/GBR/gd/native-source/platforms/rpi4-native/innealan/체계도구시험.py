#!/usr/bin/env python3
"""dearbh_dàta 자체 커널의 IP/ICMP, cor_VALUE ceist_VALUE, 현지어 àithne, 게스트 fàg_ap dearbh_5fb2b747."""
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


def ruith():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    tilg_freumh=Path(__file__).resolve().parents[1];roghainnean={};ainm_clàr={}
    if 인수.edition:
        나라=인수.edition.resolve();roghainnean=json.loads((나라/'native.json').read_text());ainm_clàr=roghainnean['identifiers'];tilg_freumh=나라/roghainnean['source']/roghainnean['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        òstair=나라/'host/qemu'
        if òstair.is_file():os.environ['QEMU_AARCH64']=str(òstair)
    innealan=tilg_freumh/Path(roghainnean.get('runner','innealan/gnìomhaich_àithne.py')).parent
    sys.path.insert(0,str(innealan))
    def 읽기(Ainm):
        Slighe=innealan/(ainm_clàr.get(Ainm,Ainm)+'.py');cùis_VALUE=importlib.util.spec_from_file_location('test_'+Ainm,str(Slighe));mòideal_VALUE=importlib.util.module_from_spec(cùis_VALUE);cùis_VALUE.loader.exec_module(mòideal_VALUE);return mòideal_VALUE
    실행모듈=읽기('gnìomhaich_àithne');lìonra_mòideal=읽기('lìonra_drochaid');àithne=getattr(실행모듈,ainm_clàr.get('àithne','àithne'));drochaid_TYPE=getattr(lìonra_mòideal,ainm_clàr.get('lìonra_drochaid','lìonra_drochaid'))
    alias_VALUE=roghainnean.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'seòladh_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'show_cuideachadh'})
    sys.path.insert(0,str(tilg_freumh/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(tilg_freumh);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or tilg_freumh/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    aithisg_VALUE={'passed':False,'country':roghainnean.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_ràgh=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        smachd_slighe=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as lorg_VALUE:lorg_VALUE.bind(('127.0.0.1',0));접속번호=lorg_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with drochaid_TYPE(접속번호,glac=True,aoigh_ADDRESS=ipTestText('10.0.2.20'),òstair_ADDRESS='127.0.0.2') as drochaid_VALUE:
            Pròiseas_VALUE=subprocess.Popen(àithne()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(smachd_slighe)]+drochaid_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            tagh_nì=selectors.DefaultSelector();tagh_nì.register(Pròiseas_VALUE.stdout,selectors.EVENT_READ)
            def 받기(show_VALUE,ruith=0,제한=45):
                끝=time.monotonic()+제한
                while show_VALUE not in LOG_ràgh[ruith:]:
                    if time.monotonic()>끝 or Pròiseas_VALUE.poll() is not None:raise AssertionError('Missing '+repr(show_VALUE)+'\n'+LOG_ràgh[ruith:].decode('utf-8','replace'))
                    for Iuchair_VALUE,_ in tagh_nì.select(.1):
                        dàta=Iuchair_VALUE.fileobj.read(65536)
                        if dàta:LOG_ràgh.extend(dàta)
                return LOG_ràgh[ruith:].decode('utf-8','replace').replace('\r\n','\n')
            def cuir(dàta):Pròiseas_VALUE.stdin.write(dàta);Pròiseas_VALUE.stdin.flush()
            def slige(SMS):
                SMS=ipTestText(SMS)
                print(aithisg_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;show_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';ruith=len(LOG_ràgh)
                cuir((SMS+'; echo; echo '+show_VALUE+'\n').encode())
                끝표시=('\r\n'+show_VALUE+'\r\n').encode();받기(끝표시,ruith)
                crìochnaich_suidhich=LOG_ràgh.index(끝표시,ruith)+len(끝표시)
                받기(b'jkoros-native> ',crìochnaich_suidhich)
                return LOG_ràgh[ruith:].decode('utf-8','replace').replace('\r\n','\n')
            def dearbh(SMS,*값들):
                freagair=slige(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in freagair,(SMS,VALUE,freagair)
                return freagair
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    cuideachadh_VALUE=dearbh('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in cuideachadh_VALUE,(별칭,cuideachadh_VALUE)
                    dearbh(alias_VALUE['help']+' system','Network / system')
                    dearbh('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    dearbh(alias_VALUE['ipconfig'],'inet 10.0.2.15');dearbh('ip addr show','sl0: UP');dearbh('ifconfig','sl0: UP')
                    for mì_dhligheach_roghainnean in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Mearachd=dearbh('ipconfig set '+mì_dhligheach_roghainnean+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Mearachd,Mearachd
                        dearbh('ipconfig','inet 10.0.2.15')
                    dearbh('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    dearbh(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    dearbh('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    dearbh('ip link set dev sl0 down','sl0: DOWN');dearbh('ping -c 1 10.0.2.2; echo STATUS=$?','Mearachd -100','STATUS=1')
                    dearbh('ipconfig up','sl0: UP')
                    dearbh(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    dearbh('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    dearbh('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');dearbh(alias_VALUE['route'],'10.0.2.2 sl0')
                    dearbh('ftpd start','FTP listening')
                    dearbh(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');dearbh('ss','LISTEN')
                    dearbh('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Mearachd -16')
                    with ftplib.FTP() as cliant_VALUE:
                        cliant_VALUE.connect('127.0.0.2',접속번호,timeout=20);cliant_VALUE.login();dàta=b'Network address was changed in the guest.\n'
                        cliant_VALUE.storbinary('STOR net-state.txt',io.BytesIO(dàta));RECEIVED_dàta=bytearray();cliant_VALUE.retrbinary('RETR net-state.txt',RECEIVED_dàta.extend);assert RECEIVED_dàta==dàta;cliant_VALUE.delete('net-state.txt')
                    dearbh('ftpd stop','FTP stopped');dearbh('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    aithisg_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(dearbh('df','RAM only'));dearbh('echo disk-proof > sys-state.txt');후=저장값(dearbh(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    dearbh('rm sys-state.txt');assert 저장값(slige('df'))==전
                    cuimhne_VALUE=dearbh(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',cuimhne_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    dearbh(alias_VALUE['ps'],'kernel/shell');dearbh(alias_VALUE['uptime'],'seconds')
                    cor_fios=dearbh(alias_VALUE['top']+' -n 2','kernel/shell');assert cor_fios.count('PID SLOT STATE')==2,cor_fios
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    dearbh('terminal','TERMINAL READY');ruith=len(LOG_ràgh);cuir(b'vi process.txt\n');받기(b'NORMAL',ruith)
                    ruith=len(LOG_ràgh);cuir(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ruith)
                    cur_a_steach_Liosta=dearbh('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',cur_a_steach_Liosta);assert 찾음 and int(찾음.group(2))>0,cur_a_steach_Liosta
                    dearbh('free','EL0 mapped KiB: '+찾음.group(2))
                    ruith=len(LOG_ràgh);cuir(b'top\n');받기(b'PID SLOT STATE',ruith);cuir(b'q');받기(b'jkoros-native> ',ruith)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        ruith=len(LOG_ràgh);cuir((alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',ruith);받기(b'jkoros-native> ',ruith)
                    aithisg_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as smachd_VALUE:
                    smachd_VALUE.settimeout(15);smachd_VALUE.connect(str(smachd_slighe));sruth_VALUE=smachd_VALUE.makefile('rwb');json.loads(sruth_VALUE.readline());sruth_VALUE.write(b'{"execute":"qmp_capabilities"}\n');sruth_VALUE.flush()
                    while 'return' not in json.loads(sruth_VALUE.readline()):pass
                    cuir((('poweroff' if 인수.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        tachartas=json.loads(sruth_VALUE.readline())
                        if tachartas.get('event')=='SHUTDOWN':break
                    assert tachartas['data']['guest'] and tachartas['data']['reason']=='guest-shutdown',tachartas
                    assert Pròiseas_VALUE.wait(timeout=15)==0
                    aithisg_VALUE['shutdown']=tachartas;aithisg_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                aithisg_VALUE['network_trace']=drochaid_VALUE.treus_LOG
                assert 인수.poweroff_only or any(cur_a_steach_VALUE['protocol']==1 and cur_a_steach_VALUE['direction']=='from_guest' for cur_a_steach_VALUE in drochaid_VALUE.treus_LOG)
                aithisg_VALUE['passed']=True
            finally:
                if Pròiseas_VALUE.poll() is None:os.killpg(Pròiseas_VALUE.pid,signal.SIGTERM)
                try:Pròiseas_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Pròiseas_VALUE.kill();Pròiseas_VALUE.wait()
                tagh_nì.close();(출력/'serial.log').write_bytes(LOG_ràgh);(출력/'report.json').write_text(json.dumps(aithisg_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Iuchair_VALUE:VALUE for Iuchair_VALUE,VALUE in aithisg_VALUE.items() if Iuchair_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ruith()
