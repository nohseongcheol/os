#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 자체 커널의 IP/ICMP, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ ᎠᏛᏛᎲᏍᎩ_ᏧᎬᏩᎶᏗᏯ, 현지어 ᎤᏁᏤᎸᎩ, 게스트 ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ ᎪᎯᏳᏙᏗ."""
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


def ᎠᎢᏎᏍᏗ():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];ᏕᎦᎧᎲᎢ={};ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ={}
    if 인수.edition:
        나라=인수.edition.resolve();ᏕᎦᎧᎲᎢ=json.loads((나라/'native.json').read_text());ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ=ᏕᎦᎧᎲᎢ['identifiers'];기준=나라/ᏕᎦᎧᎲᎢ['source']/ᏕᎦᎧᎲᎢ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ᎠᏁᏢᏍᎩ=나라/'host/qemu'
        if ᎠᏁᏢᏍᎩ.is_file():os.environ['QEMU_AARCH64']=str(ᎠᏁᏢᏍᎩ)
    도구=기준/Path(ᏕᎦᎧᎲᎢ.get('runner','도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py')).parent
    sys.path.insert(0,str(도구))
    def 읽기(ᏚᏙᎥᎢ):
        ᎠᏍᏓᏩᏛᏍᏗ=도구/(ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ.get(ᏚᏙᎥᎢ,ᏚᏙᎥᎢ)+'.py');ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ=importlib.util.spec_from_file_location('test_'+ᏚᏙᎥᎢ,str(ᎠᏍᏓᏩᏛᏍᏗ));모듈=importlib.util.module_from_spec(ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ);ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ');망모듈=읽기('통신다리');ᎤᏁᏤᎸᎩ=getattr(실행모듈,ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ.get('ᎤᏁᏤᎸᎩ','ᎤᏁᏤᎸᎩ'));다리형=getattr(망모듈,ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ.get('통신다리','통신다리'))
    ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b=ᏕᎦᎧᎲᎢ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ᏍᎩᎪᏩᏛᏓ_ᎠᏍᏕᎸᏗᎢ'})
    sys.path.insert(0,str(기준/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(기준);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or 기준/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ={'passed':False,'country':ᏕᎦᎧᎲᎢ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ:ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.1',0));접속번호=ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ipTestText('10.0.2.20'),ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ='127.0.0.2') as 다리:
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ=subprocess.Popen(ᎤᏁᏤᎸᎩ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ=selectors.DefaultSelector();ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout,selectors.EVENT_READ)
            def 받기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ,ᎠᎢᏎᏍᏗ=0,제한=45):
                끝=time.monotonic()+제한
                while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:]:
                    if time.monotonic()>끝 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None:raise AssertionError('Missing '+repr(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ)+'\n'+ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8','replace'))
                    for ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ,_ in ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.select(.1):
                        ᎦᏟᏌᏅᎯ=ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ.fileobj.read(65536)
                        if ᎦᏟᏌᏅᎯ:ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
                return ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8','replace').replace('\r\n','\n')
            def ᏫᎦᏅᏗ(ᎦᏟᏌᏅᎯ):ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.write(ᎦᏟᏌᏅᎯ);ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.flush()
            def ᎤᏯᏍᎦ(ᎠᎪᎵᏰᏗ):
                ᎠᎪᎵᏰᏗ=ipTestText(ᎠᎪᎵᏰᏗ)
                print(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['country'],ᎠᎪᎵᏰᏗ,flush=True);차례[0]+=1;ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ='__SYSTEM_DONE_'+str(차례[0])+'__';ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ((ᎠᎪᎵᏰᏗ+'; echo; echo '+ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ+'\n').encode())
                끝표시=('\r\n'+ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ+'\r\n').encode();받기(끝표시,ᎠᎢᏎᏍᏗ)
                끝자리=ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.index(끝표시,ᎠᎢᏎᏍᏗ)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8','replace').replace('\r\n','\n')
            def ᎰᎯᏳᏓ(ᎠᎪᎵᏰᏗ,*값들):
                응답=ᎤᏯᏍᎦ(ᎠᎪᎵᏰᏗ)
                for ᏧᎬᏩᎶᏗᏯ in 값들:assert ipTestText(ᏧᎬᏩᎶᏗᏯ) in 응답,(ᎠᎪᎵᏰᏗ,ᏧᎬᏩᎶᏗᏯ,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ᎠᏍᏕᎸᏗᎢ_ᏧᎬᏩᎶᏗᏯ=ᎰᎯᏳᏓ('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b.values():assert 별칭 in ᎠᏍᏕᎸᏗᎢ_ᏧᎬᏩᎶᏗᏯ,(별칭,ᎠᏍᏕᎸᏗᎢ_ᏧᎬᏩᎶᏗᏯ)
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['help']+' system','Network / system')
                    ᎰᎯᏳᏓ('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['ipconfig'],'inet 10.0.2.15');ᎰᎯᏳᏓ('ip addr show','sl0: UP');ᎰᎯᏳᏓ('ifconfig','sl0: UP')
                    for ᏂᏓᏓᏂᎸᎬᎾ_ᏕᎦᎧᎲᎢ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ᎦᎵᏓᏍᏔᏅ=ᎰᎯᏳᏓ('ipconfig set '+ᏂᏓᏓᏂᎸᎬᎾ_ᏕᎦᎧᎲᎢ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ᎦᎵᏓᏍᏔᏅ,ᎦᎵᏓᏍᏔᏅ
                        ᎰᎯᏳᏓ('ipconfig','inet 10.0.2.15')
                    ᎰᎯᏳᏓ('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ᎰᎯᏳᏓ('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ᎰᎯᏳᏓ('ip link set dev sl0 down','sl0: DOWN');ᎰᎯᏳᏓ('ping -c 1 10.0.2.2; echo STATUS=$?','ᎦᎵᏓᏍᏔᏅ -100','STATUS=1')
                    ᎰᎯᏳᏓ('ipconfig up','sl0: UP')
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ᎰᎯᏳᏓ('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ᎰᎯᏳᏓ('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['route'],'10.0.2.2 sl0')
                    ᎰᎯᏳᏓ('ftpd start','FTP listening')
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['netstat'],'10.0.2.20:21','LISTEN');ᎰᎯᏳᏓ('ss','LISTEN')
                    ᎰᎯᏳᏓ('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ᎦᎵᏓᏍᏔᏅ -16')
                    with ftplib.FTP() as ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ:
                        ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.connect('127.0.0.2',접속번호,timeout=20);ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.login();ᎦᏟᏌᏅᎯ=b'Network address was changed in the guest.\n'
                        ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.storbinary('STOR net-state.txt',io.BytesIO(ᎦᏟᏌᏅᎯ));받은자료=bytearray();ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ᎦᏟᏌᏅᎯ;ᎠᏥᏍᏕᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ.delete('net-state.txt')
                    ᎰᎯᏳᏓ('ftpd stop','FTP stopped');ᎰᎯᏳᏓ('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ᎠᎪᎵᏰᏗ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ᎠᎪᎵᏰᏗ);assert 찾음,ᎠᎪᎵᏰᏗ;return tuple(map(int,찾음.groups()))
                    전=저장값(ᎰᎯᏳᏓ('df','RAM only'));ᎰᎯᏳᏓ('echo disk-proof > sys-state.txt');후=저장값(ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ᎰᎯᏳᏓ('rm sys-state.txt');assert 저장값(ᎤᏯᏍᎦ('df'))==전
                    ᎠᏅᏓᏗᏍᏙ_ᏧᎬᏩᎶᏗᏯ=ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ᎠᏅᏓᏗᏍᏙ_ᏧᎬᏩᎶᏗᏯ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['ps'],'kernel/shell');ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['uptime'],'seconds')
                    ᏄᏍᏗᏓᏅ_ᎧᏃᎮᏢᎥᏍᎩ=ᎰᎯᏳᏓ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['top']+' -n 2','kernel/shell');assert ᏄᏍᏗᏓᏅ_ᎧᏃᎮᏢᎥᏍᎩ.count('PID SLOT STATE')==2,ᏄᏍᏗᏓᏅ_ᎧᏃᎮᏢᎥᏍᎩ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ᎰᎯᏳᏓ('terminal','TERMINAL READY');ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᏫᎦᏅᏗ(b'vi process.txt\n');받기(b'NORMAL',ᎠᎢᏎᏍᏗ)
                    ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᏫᎦᏅᏗ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ᎠᎢᏎᏍᏗ)
                    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ=ᎰᎯᏳᏓ('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ);assert 찾음 and int(찾음.group(2))>0,Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ
                    ᎰᎯᏳᏓ('free','EL0 mapped KiB: '+찾음.group(2))
                    ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᏫᎦᏅᏗ(b'top\n');받기(b'PID SLOT STATE',ᎠᎢᏎᏍᏗ);ᏫᎦᏅᏗ(b'q');받기(b'jkoros-native> ',ᎠᎢᏎᏍᏗ)
                    # Test a multibyte prefix through the real shell completion path.
                    if ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['df']!='df':
                        ᎠᎢᏎᏍᏗ=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);ᏫᎦᏅᏗ((ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',ᎠᎢᏎᏍᏗ);받기(b'jkoros-native> ',ᎠᎢᏎᏍᏗ)
                    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ:
                    ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.settimeout(15);ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.connect(str(ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ));ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ=ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.makefile('rwb');json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline());ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.write(b'{"execute":"qmp_capabilities"}\n');ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.flush()
                    while 'return' not in json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline()):pass
                    ᏫᎦᏅᏗ((('poweroff' if 인수.poweroff_only else ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ=json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                        if ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.get('event')=='SHUTDOWN':break
                    assert ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ['data']['guest'] and ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ['data']['reason']=='guest-shutdown',ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ
                    assert ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=15)==0
                    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['shutdown']=ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ;ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['protocol']==1 and Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['direction']=='from_guest' for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 다리.추적기록)
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed']=True
            finally:
                if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:os.killpg(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.pid,signal.SIGTERM)
                try:ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=10)
                except subprocess.TimeoutExpired:ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill();ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
                ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.close();(출력/'serial.log').write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);(출력/'report.json').write_text(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ:ᏧᎬᏩᎶᏗᏯ for ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ,ᏧᎬᏩᎶᏗᏯ in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ.items() if ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ᎠᎢᏎᏍᏗ()
