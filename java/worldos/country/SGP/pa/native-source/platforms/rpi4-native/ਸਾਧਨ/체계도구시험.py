#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ 자체 커널의 IP/ICMP, ਸਥਿਤੀ_ਕੀਮਤ ਪੜਤਾਲ_ਕੀਮਤ, 현지어 ਕਮਾਂਡ, 게스트 ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼ ਪ੍ਰਮਾਣਿਤ."""
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


def ਚਲਾਓ_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');ਆਰਗੂਮੈਂਟ=해석기.parse_args()
    ਪ੍ਰੋਜੈਕਟ_ਰੂਟ=Path(__file__).resolve().parents[1];ਸੈਟਿੰਗ={};ਨਾਮ_ਤਾਲਿਕਾ={}
    if ਆਰਗੂਮੈਂਟ.edition:
        나라=ਆਰਗੂਮੈਂਟ.edition.resolve();ਸੈਟਿੰਗ=json.loads((나라/'native.json').read_text());ਨਾਮ_ਤਾਲਿਕਾ=ਸੈਟਿੰਗ['identifiers'];ਪ੍ਰੋਜੈਕਟ_ਰੂਟ=나라/ਸੈਟਿੰਗ['source']/ਸੈਟਿੰਗ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ਹੋਸਟ=나라/'host/qemu'
        if ਹੋਸਟ.is_file():os.environ['QEMU_AARCH64']=str(ਹੋਸਟ)
    ਸਾਧਨ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/Path(ਸੈਟਿੰਗ.get('runner','ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py')).parent
    sys.path.insert(0,str(ਸਾਧਨ))
    def ਪੜ੍ਹਨ(ਨਾਂ):
        ਮਾਰਗ=ਸਾਧਨ/(ਨਾਮ_ਤਾਲਿਕਾ.get(ਨਾਂ,ਨਾਂ)+'.py');ਕੰਮ_ਕੀਮਤ=importlib.util.spec_from_file_location('test_'+ਨਾਂ,str(ਮਾਰਗ));ਮੌਡਿਉਲ_ਕੀਮਤ=importlib.util.module_from_spec(ਕੰਮ_ਕੀਮਤ);ਕੰਮ_ਕੀਮਤ.loader.exec_module(ਮੌਡਿਉਲ_ਕੀਮਤ);return ਮੌਡਿਉਲ_ਕੀਮਤ
    실행모듈=ਪੜ੍ਹਨ('ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼');ਨੈਟਵਰਕ_ਮੌਡਿਉਲ=ਪੜ੍ਹਨ('ਨੈਟਵਰਕ_ਬਰਿਜ');ਕਮਾਂਡ=getattr(실행모듈,ਨਾਮ_ਤਾਲਿਕਾ.get('ਕਮਾਂਡ','ਕਮਾਂਡ'));ਬਰਿਜ_ਟਾਈਪ_ਕਰੋ=getattr(ਨੈਟਵਰਕ_ਮੌਡਿਉਲ,ਨਾਮ_ਤਾਲਿਕਾ.get('ਨੈਟਵਰਕ_ਬਰਿਜ','ਨੈਟਵਰਕ_ਬਰਿਜ'))
    ਉਪਨਾਮ_ਕੀਮਤ=ਸੈਟਿੰਗ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ਪਤਾ','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ਸ਼ੋਅ_ਮਦਦ'})
    sys.path.insert(0,str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ਆਉਟਪੁੱਟ=ਆਰਗੂਮੈਂਟ.output or ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/system-tools';ਆਉਟਪੁੱਟ.mkdir(parents=True,exist_ok=True)
    ਵਿਵਰਨ_ਕੀਮਤ={'passed':False,'country':ਸੈਟਿੰਗ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ਲੌਗ_ਕਤਾਰ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ਨਿਯੰਤਰਣ_ਰਸਤਾ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ਖੋਜ_ਕੀਮਤ:ਖੋਜ_ਕੀਮਤ.bind(('127.0.0.1',0));접속번호=ਖੋਜ_ਕੀਮਤ.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ਬਰਿਜ_ਟਾਈਪ_ਕਰੋ(접속번호,ਪਕੜਨਾ=True,ਗੈਸਟ_ਪਤਾ=ipTestText('10.0.2.20'),ਹੋਸਟ_ਪਤਾ='127.0.0.2') as ਬਰਿਜ_ਕੀਮਤ:
            ਕਾਰਵਾਈ_ਕੀਮਤ=subprocess.Popen(ਕਮਾਂਡ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ਨਿਯੰਤਰਣ_ਰਸਤਾ)]+ਬਰਿਜ_ਕੀਮਤ.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ਚੁਣੋ_ਆਇਟਮ=selectors.DefaultSelector();ਚੁਣੋ_ਆਇਟਮ.register(ਕਾਰਵਾਈ_ਕੀਮਤ.stdout,selectors.EVENT_READ)
            def 받기(ਸ਼ੋਅ_ਕੀਮਤ,ਚਲਾਓ_2=0,제한=45):
                끝=time.monotonic()+제한
                while ਸ਼ੋਅ_ਕੀਮਤ not in ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:]:
                    if time.monotonic()>끝 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:raise AssertionError('Missing '+repr(ਸ਼ੋਅ_ਕੀਮਤ)+'\n'+ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8','replace'))
                    for ਕੀ_ਕੀਮਤ,_ in ਚੁਣੋ_ਆਇਟਮ.select(.1):
                        ਸਮੱਗਰੀ=ਕੀ_ਕੀਮਤ.fileobj.read(65536)
                        if ਸਮੱਗਰੀ:ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
                return ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ਈਮੇਲ(ਸਮੱਗਰੀ):ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.write(ਸਮੱਗਰੀ);ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.flush()
            def ਸ਼ੈਲ(ਟੈਕਸਟ):
                ਟੈਕਸਟ=ipTestText(ਟੈਕਸਟ)
                print(ਵਿਵਰਨ_ਕੀਮਤ['country'],ਟੈਕਸਟ,flush=True);차례[0]+=1;ਸ਼ੋਅ_ਕੀਮਤ='__SYSTEM_DONE_'+str(차례[0])+'__';ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ((ਟੈਕਸਟ+'; echo; echo '+ਸ਼ੋਅ_ਕੀਮਤ+'\n').encode())
                끝표시=('\r\n'+ਸ਼ੋਅ_ਕੀਮਤ+'\r\n').encode();받기(끝표시,ਚਲਾਓ_2)
                ਅੰਤ_ਸਥਿਤੀ_ਬਦਲੋ=ਲੌਗ_ਕਤਾਰ.index(끝표시,ਚਲਾਓ_2)+len(끝표시)
                받기(b'jkoros-native> ',ਅੰਤ_ਸਥਿਤੀ_ਬਦਲੋ)
                return ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ਤਸਦੀਕ(ਟੈਕਸਟ,*값들):
                ਜਵਾਬ_ਦਿਓ=ਸ਼ੈਲ(ਟੈਕਸਟ)
                for ਕੀਮਤ in 값들:assert ipTestText(ਕੀਮਤ) in ਜਵਾਬ_ਦਿਓ,(ਟੈਕਸਟ,ਕੀਮਤ,ਜਵਾਬ_ਦਿਓ)
                return ਜਵਾਬ_ਦਿਓ
            try:
                받기(b'jkoros-native> ')
                if not ਆਰਗੂਮੈਂਟ.poweroff_only:
                    ਮਦਦ_ਕੀਮਤ=ਤਸਦੀਕ('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ਉਪਨਾਮ_ਕੀਮਤ.values():assert 별칭 in ਮਦਦ_ਕੀਮਤ,(별칭,ਮਦਦ_ਕੀਮਤ)
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['help']+' system','Network / system')
                    ਤਸਦੀਕ('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['ipconfig'],'inet 10.0.2.15');ਤਸਦੀਕ('ip addr show','sl0: UP');ਤਸਦੀਕ('ifconfig','sl0: UP')
                    for ਅਯੋਗ_ਸੈਟਿੰਗਾਂ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ਗਲਤੀ=ਤਸਦੀਕ('ipconfig set '+ਅਯੋਗ_ਸੈਟਿੰਗਾਂ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ਗਲਤੀ,ਗਲਤੀ
                        ਤਸਦੀਕ('ipconfig','inet 10.0.2.15')
                    ਤਸਦੀਕ('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ਤਸਦੀਕ('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ਤਸਦੀਕ('ip link set dev sl0 down','sl0: DOWN');ਤਸਦੀਕ('ping -c 1 10.0.2.2; echo STATUS=$?','ਗਲਤੀ -100','STATUS=1')
                    ਤਸਦੀਕ('ipconfig up','sl0: UP')
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ਤਸਦੀਕ('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ਤਸਦੀਕ('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['route'],'10.0.2.2 sl0')
                    ਤਸਦੀਕ('ftpd start','FTP listening')
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['netstat'],'10.0.2.20:21','LISTEN');ਤਸਦੀਕ('ss','LISTEN')
                    ਤਸਦੀਕ('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ਗਲਤੀ -16')
                    with ftplib.FTP() as ਗਾਹਕ_ਕੀਮਤ:
                        ਗਾਹਕ_ਕੀਮਤ.connect('127.0.0.2',접속번호,timeout=20);ਗਾਹਕ_ਕੀਮਤ.login();ਸਮੱਗਰੀ=b'Network address was changed in the guest.\n'
                        ਗਾਹਕ_ਕੀਮਤ.storbinary('STOR net-state.txt',io.BytesIO(ਸਮੱਗਰੀ));받은자료=bytearray();ਗਾਹਕ_ਕੀਮਤ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ਸਮੱਗਰੀ;ਗਾਹਕ_ਕੀਮਤ.delete('net-state.txt')
                    ਤਸਦੀਕ('ftpd stop','FTP stopped');ਤਸਦੀਕ('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ਟੈਕਸਟ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ਟੈਕਸਟ);assert 찾음,ਟੈਕਸਟ;return tuple(map(int,찾음.groups()))
                    전=저장값(ਤਸਦੀਕ('df','RAM only'));ਤਸਦੀਕ('echo disk-proof > sys-state.txt');후=저장값(ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ਤਸਦੀਕ('rm sys-state.txt');assert 저장값(ਸ਼ੈਲ('df'))==전
                    ਮੈਮਰੀ_ਕੀਮਤ=ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ਮੈਮਰੀ_ਕੀਮਤ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['ps'],'kernel/shell');ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['uptime'],'seconds')
                    ਸਥਿਤੀ_ਜਾਣਕਾਰੀ=ਤਸਦੀਕ(ਉਪਨਾਮ_ਕੀਮਤ['top']+' -n 2','kernel/shell');assert ਸਥਿਤੀ_ਜਾਣਕਾਰੀ.count('PID SLOT STATE')==2,ਸਥਿਤੀ_ਜਾਣਕਾਰੀ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ਤਸਦੀਕ('terminal','TERMINAL READY');ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਈਮੇਲ(b'vi process.txt\n');받기(b'NORMAL',ਚਲਾਓ_2)
                    ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਈਮੇਲ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ਚਲਾਓ_2)
                    ਦਾਖਲਾ_ਸੂਚੀ=ਤਸਦੀਕ('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ਦਾਖਲਾ_ਸੂਚੀ);assert 찾음 and int(찾음.group(2))>0,ਦਾਖਲਾ_ਸੂਚੀ
                    ਤਸਦੀਕ('free','EL0 mapped KiB: '+찾음.group(2))
                    ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਈਮੇਲ(b'top\n');받기(b'PID SLOT STATE',ਚਲਾਓ_2);ਈਮੇਲ(b'q');받기(b'jkoros-native> ',ਚਲਾਓ_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if ਉਪਨਾਮ_ਕੀਮਤ['df']!='df':
                        ਚਲਾਓ_2=len(ਲੌਗ_ਕਤਾਰ);ਈਮੇਲ((ਉਪਨਾਮ_ਕੀਮਤ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ਚਲਾਓ_2);받기(b'jkoros-native> ',ਚਲਾਓ_2)
                    ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ਨਿਯੰਤਰਣ_ਕੀਮਤ:
                    ਨਿਯੰਤਰਣ_ਕੀਮਤ.settimeout(15);ਨਿਯੰਤਰਣ_ਕੀਮਤ.connect(str(ਨਿਯੰਤਰਣ_ਰਸਤਾ));ਸਟ੍ਰੀਮ_ਕੀਮਤ=ਨਿਯੰਤਰਣ_ਕੀਮਤ.makefile('rwb');json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline());ਸਟ੍ਰੀਮ_ਕੀਮਤ.write(b'{"execute":"qmp_capabilities"}\n');ਸਟ੍ਰੀਮ_ਕੀਮਤ.flush()
                    while 'return' not in json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline()):pass
                    ਈਮੇਲ((('poweroff' if ਆਰਗੂਮੈਂਟ.poweroff_only else ਉਪਨਾਮ_ਕੀਮਤ['poweroff'])+'\n').encode())
                    while True:
                        ਇਵੈਂਟ=json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                        if ਇਵੈਂਟ.get('event')=='SHUTDOWN':break
                    assert ਇਵੈਂਟ['data']['guest'] and ਇਵੈਂਟ['data']['reason']=='guest-shutdown',ਇਵੈਂਟ
                    assert ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=15)==0
                    ਵਿਵਰਨ_ਕੀਮਤ['shutdown']=ਇਵੈਂਟ;ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ਵਿਵਰਨ_ਕੀਮਤ['network_trace']=ਬਰਿਜ_ਕੀਮਤ.ਟਰੇਸ_ਲੌਗ
                assert ਆਰਗੂਮੈਂਟ.poweroff_only or any(ਦਾਖਲਾ_ਕੀਮਤ['protocol']==1 and ਦਾਖਲਾ_ਕੀਮਤ['direction']=='from_guest' for ਦਾਖਲਾ_ਕੀਮਤ in ਬਰਿਜ_ਕੀਮਤ.ਟਰੇਸ_ਲੌਗ)
                ਵਿਵਰਨ_ਕੀਮਤ['passed']=True
            finally:
                if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:os.killpg(ਕਾਰਵਾਈ_ਕੀਮਤ.pid,signal.SIGTERM)
                try:ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=10)
                except subprocess.TimeoutExpired:ਕਾਰਵਾਈ_ਕੀਮਤ.kill();ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
                ਚੁਣੋ_ਆਇਟਮ.close();(ਆਉਟਪੁੱਟ/'serial.log').write_bytes(ਲੌਗ_ਕਤਾਰ);(ਆਉਟਪੁੱਟ/'report.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ਕੀ_ਕੀਮਤ:ਕੀਮਤ for ਕੀ_ਕੀਮਤ,ਕੀਮਤ in ਵਿਵਰਨ_ਕੀਮਤ.items() if ਕੀ_ਕੀਮਤ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ਚਲਾਓ_2()
