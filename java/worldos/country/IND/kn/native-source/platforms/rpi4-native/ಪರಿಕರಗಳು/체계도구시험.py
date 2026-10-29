#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ 자체 커널의 IP/ICMP, ಸ್ಥಿತಿ_ಮೌಲ್ಯ ಪ್ರಶ್ನಾವಳಿ_ಮೌಲ್ಯ, 현지어 ಆಜ್ಞೆ, 게스트 ನಿರ್ಗಮನ_ಅಪ್ಲಿ ಸಕ್ರಮೀಕರಿಸು."""
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


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b=argparse.ArgumentParser();ಪಾರ್ಸರ್_48ee4b1b.add_argument('--edition',type=Path);ಪಾರ್ಸರ್_48ee4b1b.add_argument('--output',type=Path);ಪಾರ್ಸರ್_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ಬಿಂಬಿಸು_ಮೂಲ=Path(__file__).resolve().parents[1];ಸಿದ್ಧತೆಗಳು={};ಹೆಸರು_ಕೋಷ್ಟಕ={}
    if 인수.edition:
        나라=인수.edition.resolve();ಸಿದ್ಧತೆಗಳು=json.loads((나라/'native.json').read_text());ಹೆಸರು_ಕೋಷ್ಟಕ=ಸಿದ್ಧತೆಗಳು['identifiers'];ಬಿಂಬಿಸು_ಮೂಲ=나라/ಸಿದ್ಧತೆಗಳು['source']/ಸಿದ್ಧತೆಗಳು['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ಹೋಸ್ಟ್=나라/'host/qemu'
        if ಹೋಸ್ಟ್.is_file():os.environ['QEMU_AARCH64']=str(ಹೋಸ್ಟ್)
    ಪರಿಕರಗಳು=ಬಿಂಬಿಸು_ಮೂಲ/Path(ಸಿದ್ಧತೆಗಳು.get('runner','ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py')).parent
    sys.path.insert(0,str(ಪರಿಕರಗಳು))
    def ಓದು(ಹೆಸರು):
        ಮಾರ್ಗ=ಪರಿಕರಗಳು/(ಹೆಸರು_ಕೋಷ್ಟಕ.get(ಹೆಸರು,ಹೆಸರು)+'.py');ಕೆಲಸ_ಮೌಲ್ಯ=importlib.util.spec_from_file_location('test_'+ಹೆಸರು,str(ಮಾರ್ಗ));ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ=importlib.util.module_from_spec(ಕೆಲಸ_ಮೌಲ್ಯ);ಕೆಲಸ_ಮೌಲ್ಯ.loader.exec_module(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ);return ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ
    실행모듈=ಓದು('ಪೂರೈಸು_ಆದೇಶ');ನೆಟ್_ವರ್ಕ್_ಮಾಡ್ಯೂಲ್=ಓದು('ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ');ಆಜ್ಞೆ=getattr(실행모듈,ಹೆಸರು_ಕೋಷ್ಟಕ.get('ಆಜ್ಞೆ','ಆಜ್ಞೆ'));ಸೇತುವೆ_ಪ್ರಕಾರ=getattr(ನೆಟ್_ವರ್ಕ್_ಮಾಡ್ಯೂಲ್,ಹೆಸರು_ಕೋಷ್ಟಕ.get('ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ','ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ'))
    ಆಲಿಯಾಸ್_ಮೌಲ್ಯ=ಸಿದ್ಧತೆಗಳು.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ವಿಳಾಸ','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ಶೋ_ಸಹಾಯ'})
    sys.path.insert(0,str(ಬಿಂಬಿಸು_ಮೂಲ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ಬಿಂಬಿಸು_ಮೂಲ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ಔಟ್_ಪುಟ್=인수.output or ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/system-tools';ಔಟ್_ಪುಟ್.mkdir(parents=True,exist_ok=True)
    ವರದಿ_ಮೌಲ್ಯ={'passed':False,'country':ಸಿದ್ಧತೆಗಳು.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ಲಾಗ್_ದಾಖಲೆ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ನಿಯಂತ್ರಣ_ಹಾದಿ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ಶೋಧ_ಮೌಲ್ಯ:ಶೋಧ_ಮೌಲ್ಯ.bind(('127.0.0.1',0));ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=ಶೋಧ_ಮೌಲ್ಯ.getsockname()[1]
            if not 50000<=ಪೋರ್ಟ್_ಸಂಖ್ಯೆ<=50007:break
        with ಸೇತುವೆ_ಪ್ರಕಾರ(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ,ಸೆರೆಹಿಡಿ=True,ಅತಿಥಿ_ಇಮೇಲ್=ipTestText('10.0.2.20'),ಹೋಸ್ಟ್_ಇಮೇಲ್='127.0.0.2') as ಸೇತುವೆ_ಮೌಲ್ಯ:
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ=subprocess.Popen(ಆಜ್ಞೆ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ನಿಯಂತ್ರಣ_ಹಾದಿ)]+ಸೇತುವೆ_ಮೌಲ್ಯ.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ಆರಿಸು_ಅಂಶ=selectors.DefaultSelector();ಆರಿಸು_ಅಂಶ.register(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout,selectors.EVENT_READ)
            def 받기(ಶೋ_ಮೌಲ್ಯ,ಚಲಾಯಿಸು_2=0,제한=45):
                끝=time.monotonic()+제한
                while ಶೋ_ಮೌಲ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:]:
                    if time.monotonic()>끝 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:raise AssertionError('Missing '+repr(ಶೋ_ಮೌಲ್ಯ)+'\n'+ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8','replace'))
                    for ಕೀ_ಮೌಲ್ಯ,_ in ಆರಿಸು_ಅಂಶ.select(.1):
                        ಡೇಟಾ=ಕೀ_ಮೌಲ್ಯ.fileobj.read(65536)
                        if ಡೇಟಾ:ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
                return ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ಕಳುಹಿಸಿ(ಡೇಟಾ):ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.write(ಡೇಟಾ);ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.flush()
            def ಶೆಲ್(ಪಠ್ಯ):
                ಪಠ್ಯ=ipTestText(ಪಠ್ಯ)
                print(ವರದಿ_ಮೌಲ್ಯ['country'],ಪಠ್ಯ,flush=True);차례[0]+=1;ಶೋ_ಮೌಲ್ಯ='__SYSTEM_DONE_'+str(차례[0])+'__';ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ((ಪಠ್ಯ+'; echo; echo '+ಶೋ_ಮೌಲ್ಯ+'\n').encode())
                끝표시=('\r\n'+ಶೋ_ಮೌಲ್ಯ+'\r\n').encode();받기(끝표시,ಚಲಾಯಿಸು_2)
                ಅಂತ್ಯಗೊಳಿಸು_ಹುದ್ದೆ=ಲಾಗ್_ದಾಖಲೆ.index(끝표시,ಚಲಾಯಿಸು_2)+len(끝표시)
                받기(b'jkoros-native> ',ಅಂತ್ಯಗೊಳಿಸು_ಹುದ್ದೆ)
                return ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಪಠ್ಯ,*값들):
                ಪ್ರತ್ಯುತ್ತರ=ಶೆಲ್(ಪಠ್ಯ)
                for ಮೌಲ್ಯ in 값들:assert ipTestText(ಮೌಲ್ಯ) in ಪ್ರತ್ಯುತ್ತರ,(ಪಠ್ಯ,ಮೌಲ್ಯ,ಪ್ರತ್ಯುತ್ತರ)
                return ಪ್ರತ್ಯುತ್ತರ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ಸಹಾಯ_ಮೌಲ್ಯ=ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ಆಲಿಯಾಸ್_ಮೌಲ್ಯ.values():assert 별칭 in ಸಹಾಯ_ಮೌಲ್ಯ,(별칭,ಸಹಾಯ_ಮೌಲ್ಯ)
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['help']+' system','Network / system')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['ipconfig'],'inet 10.0.2.15');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ip addr show','sl0: UP');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ifconfig','sl0: UP')
                    for ಅಮಾನ್ಯ_ಸೆಟ್ಟಿಂಗ್ಸ್ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ದೋಷ=ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig set '+ಅಮಾನ್ಯ_ಸೆಟ್ಟಿಂಗ್ಸ್+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ದೋಷ,ದೋಷ
                        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig','inet 10.0.2.15')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ip link set dev sl0 down','sl0: DOWN');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ping -c 1 10.0.2.2; echo STATUS=$?','ದೋಷ -100','STATUS=1')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig up','sl0: UP')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['route'],'10.0.2.2 sl0')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ftpd start','FTP listening')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['netstat'],'10.0.2.20:21','LISTEN');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ss','LISTEN')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ದೋಷ -16')
                    with ftplib.FTP() as ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ:
                        ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ.connect('127.0.0.2',ಪೋರ್ಟ್_ಸಂಖ್ಯೆ,timeout=20);ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ.login();ಡೇಟಾ=b'Network address was changed in the guest.\n'
                        ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ.storbinary('STOR net-state.txt',io.BytesIO(ಡೇಟಾ));받은자료=bytearray();ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ಡೇಟಾ;ಕ್ಲೈಂಟ್_ಮೌಲ್ಯ.delete('net-state.txt')
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ftpd stop','FTP stopped');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ವರದಿ_ಮೌಲ್ಯ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ಪಠ್ಯ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ಪಠ್ಯ);assert 찾음,ಪಠ್ಯ;return tuple(map(int,찾음.groups()))
                    전=저장값(ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('df','RAM only'));ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('echo disk-proof > sys-state.txt');후=저장값(ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('rm sys-state.txt');assert 저장값(ಶೆಲ್('df'))==전
                    ಮೆಮೊರಿ_ಮೌಲ್ಯ=ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ಮೆಮೊರಿ_ಮೌಲ್ಯ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['ps'],'kernel/shell');ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['uptime'],'seconds')
                    ಲಭ್ಯತೆ_ಮಾಹಿತಿ=ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['top']+' -n 2','kernel/shell');assert ಲಭ್ಯತೆ_ಮಾಹಿತಿ.count('PID SLOT STATE')==2,ಲಭ್ಯತೆ_ಮಾಹಿತಿ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('terminal','TERMINAL READY');ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕಳುಹಿಸಿ(b'vi process.txt\n');받기(b'NORMAL',ಚಲಾಯಿಸು_2)
                    ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕಳುಹಿಸಿ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ಚಲಾಯಿಸು_2)
                    ನಮೂದು_ಪಟ್ಟಿ=ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ನಮೂದು_ಪಟ್ಟಿ);assert 찾음 and int(찾음.group(2))>0,ನಮೂದು_ಪಟ್ಟಿ
                    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು('free','EL0 mapped KiB: '+찾음.group(2))
                    ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕಳುಹಿಸಿ(b'top\n');받기(b'PID SLOT STATE',ಚಲಾಯಿಸು_2);ಕಳುಹಿಸಿ(b'q');받기(b'jkoros-native> ',ಚಲಾಯಿಸು_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['df']!='df':
                        ಚಲಾಯಿಸು_2=len(ಲಾಗ್_ದಾಖಲೆ);ಕಳುಹಿಸಿ((ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ಚಲಾಯಿಸು_2);받기(b'jkoros-native> ',ಚಲಾಯಿಸು_2)
                    ವರದಿ_ಮೌಲ್ಯ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ:
                    ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.settimeout(15);ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.connect(str(ನಿಯಂತ್ರಣ_ಹಾದಿ));ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ=ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.makefile('rwb');json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline());ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.write(b'{"execute":"qmp_capabilities"}\n');ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.flush()
                    while 'return' not in json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline()):pass
                    ಕಳುಹಿಸಿ((('poweroff' if 인수.poweroff_only else ಆಲಿಯಾಸ್_ಮೌಲ್ಯ['poweroff'])+'\n').encode())
                    while True:
                        ಸಂಗತಿ=json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                        if ಸಂಗತಿ.get('event')=='SHUTDOWN':break
                    assert ಸಂಗತಿ['data']['guest'] and ಸಂಗತಿ['data']['reason']=='guest-shutdown',ಸಂಗತಿ
                    assert ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=15)==0
                    ವರದಿ_ಮೌಲ್ಯ['shutdown']=ಸಂಗತಿ;ವರದಿ_ಮೌಲ್ಯ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ವರದಿ_ಮೌಲ್ಯ['network_trace']=ಸೇತುವೆ_ಮೌಲ್ಯ.ಟ್ರೇಸ್_ಲಾಗ್
                assert 인수.poweroff_only or any(ನಮೂದು_ಮೌಲ್ಯ['protocol']==1 and ನಮೂದು_ಮೌಲ್ಯ['direction']=='from_guest' for ನಮೂದು_ಮೌಲ್ಯ in ಸೇತುವೆ_ಮೌಲ್ಯ.ಟ್ರೇಸ್_ಲಾಗ್)
                ವರದಿ_ಮೌಲ್ಯ['passed']=True
            finally:
                if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:os.killpg(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.pid,signal.SIGTERM)
                try:ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=10)
                except subprocess.TimeoutExpired:ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill();ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
                ಆರಿಸು_ಅಂಶ.close();(ಔಟ್_ಪುಟ್/'serial.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ);(ಔಟ್_ಪುಟ್/'report.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ಕೀ_ಮೌಲ್ಯ:ಮೌಲ್ಯ for ಕೀ_ಮೌಲ್ಯ,ಮೌಲ್ಯ in ವರದಿ_ಮೌಲ್ಯ.items() if ಕೀ_ಮೌಲ್ಯ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ಚಲಾಯಿಸು_2()
