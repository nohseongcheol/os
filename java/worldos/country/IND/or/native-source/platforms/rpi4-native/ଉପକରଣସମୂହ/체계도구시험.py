#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା 자체 커널의 IP/ICMP, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 ଜିଜ୍ଞାସା_ମୂଲ୍ୟ, 현지어 ନିର୍ଦ୍ଦେଶ, 게스트 ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ ବୈଧକରଣ."""
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


def ଚଳାନ୍ତୁ():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍=Path(__file__).resolve().parents[1];ବିନ୍ଯାସ={};ନାମ_ସାରଣୀ={}
    if 인수.edition:
        나라=인수.edition.resolve();ବିନ୍ଯାସ=json.loads((나라/'native.json').read_text());ନାମ_ସାରଣୀ=ବିନ୍ଯାସ['identifiers'];ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍=나라/ବିନ୍ଯାସ['source']/ବିନ୍ଯାସ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ଆୟୋଜକ=나라/'host/qemu'
        if ଆୟୋଜକ.is_file():os.environ['QEMU_AARCH64']=str(ଆୟୋଜକ)
    ଉପକରଣସମୂହ=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/Path(ବିନ୍ଯାସ.get('runner','ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py')).parent
    sys.path.insert(0,str(ଉପକରଣସମୂହ))
    def ପଢନ୍ତୁ(ନାମ):
        ପଥ=ଉପକରଣସମୂହ/(ନାମ_ସାରଣୀ.get(ନାମ,ନାମ)+'.py');କର୍ମ_ମୂଲ୍ୟ=importlib.util.spec_from_file_location('test_'+ନାମ,str(ପଥ));ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ=importlib.util.module_from_spec(କର୍ମ_ମୂଲ୍ୟ);କର୍ମ_ମୂଲ୍ୟ.loader.exec_module(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ);return ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ
    실행모듈=ପଢନ୍ତୁ('ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ');ନେଟ୍_ୱାର୍କ୍_ମଡ୍ୟୁଲ୍=ପଢନ୍ତୁ('ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍');ନିର୍ଦ୍ଦେଶ=getattr(실행모듈,ନାମ_ସାରଣୀ.get('ନିର୍ଦ୍ଦେଶ','ନିର୍ଦ୍ଦେଶ'));ବ୍ରିଜ୍_ଟାଇପ୍_କରିବା=getattr(ନେଟ୍_ୱାର୍କ୍_ମଡ୍ୟୁଲ୍,ନାମ_ସାରଣୀ.get('ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍','ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍'))
    ଛଦ୍ମନାମ_ମୂଲ୍ୟ=ବିନ୍ଯାସ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ଠିକଣା','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ପ୍ରଦର୍ଶନ_କରିବା_ସହାୟତା'})
    sys.path.insert(0,str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ନିର୍ଗମ=인수.output or ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/system-tools';ନିର୍ଗମ.mkdir(parents=True,exist_ok=True)
    ରିପୋର୍ଟ_ମୂଲ୍ୟ={'passed':False,'country':ବିନ୍ଯାସ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ଲଗ୍_ଧାଡ଼ି=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ନିୟନ୍ତ୍ରଣ_ପଥ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ସନ୍ଧାନ_ମୂଲ୍ୟ:ସନ୍ଧାନ_ମୂଲ୍ୟ.bind(('127.0.0.1',0));ପୋର୍ଟ୍_ନମ୍ଵର୍=ସନ୍ଧାନ_ମୂଲ୍ୟ.getsockname()[1]
            if not 50000<=ପୋର୍ଟ୍_ନମ୍ଵର୍<=50007:break
        with ବ୍ରିଜ୍_ଟାଇପ୍_କରିବା(ପୋର୍ଟ୍_ନମ୍ଵର୍,କ୍ୟାପଚର୍_କରିବା=True,ଅତିଥି_ଠିକଣା=ipTestText('10.0.2.20'),ଆୟୋଜକ_ଠିକଣା='127.0.0.2') as ବ୍ରିଜ୍_ମୂଲ୍ୟ:
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ=subprocess.Popen(ନିର୍ଦ୍ଦେଶ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ନିୟନ୍ତ୍ରଣ_ପଥ)]+ବ୍ରିଜ୍_ମୂଲ୍ୟ.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ମନୋନୟନ_ଆଇଟମ୍=selectors.DefaultSelector();ମନୋନୟନ_ଆଇଟମ୍.register(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout,selectors.EVENT_READ)
            def 받기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ,ଚଳାନ୍ତୁ=0,제한=45):
                끝=time.monotonic()+제한
                while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:]:
                    if time.monotonic()>끝 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:raise AssertionError('Missing '+repr(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ)+'\n'+ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8','replace'))
                    for କୀ_ମୂଲ୍ୟ,_ in ମନୋନୟନ_ଆଇଟମ୍.select(.1):
                        ଡାଟା=କୀ_ମୂଲ୍ୟ.fileobj.read(65536)
                        if ଡାଟା:ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
                return ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8','replace').replace('\r\n','\n')
            def ପଠାନ୍ତୁ(ଡାଟା):ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.write(ଡାଟା);ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.flush()
            def ଖୋଳ(ପାଠ୍ଯ):
                ପାଠ୍ଯ=ipTestText(ପାଠ୍ଯ)
                print(ରିପୋର୍ଟ_ମୂଲ୍ୟ['country'],ପାଠ୍ଯ,flush=True);차례[0]+=1;ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ='__SYSTEM_DONE_'+str(차례[0])+'__';ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ((ପାଠ୍ଯ+'; echo; echo '+ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ+'\n').encode())
                끝표시=('\r\n'+ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ+'\r\n').encode();받기(끝표시,ଚଳାନ୍ତୁ)
                ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି=ଲଗ୍_ଧାଡ଼ି.index(끝표시,ଚଳାନ୍ତୁ)+len(끝표시)
                받기(b'jkoros-native> ',ଶେଷ_କରନ୍ତୁ_ସ୍ଥିତି)
                return ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8','replace').replace('\r\n','\n')
            def ଯାଞ୍ଚ୍_କରିବା(ପାଠ୍ଯ,*값들):
                ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ=ଖୋଳ(ପାଠ୍ଯ)
                for ମୂଲ୍ୟ in 값들:assert ipTestText(ମୂଲ୍ୟ) in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ,(ପାଠ୍ଯ,ମୂଲ୍ୟ,ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ)
                return ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ସହାୟତା_ମୂଲ୍ୟ=ଯାଞ୍ଚ୍_କରିବା('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ଛଦ୍ମନାମ_ମୂଲ୍ୟ.values():assert 별칭 in ସହାୟତା_ମୂଲ୍ୟ,(별칭,ସହାୟତା_ମୂଲ୍ୟ)
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['help']+' system','Network / system')
                    ଯାଞ୍ଚ୍_କରିବା('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['ipconfig'],'inet 10.0.2.15');ଯାଞ୍ଚ୍_କରିବା('ip addr show','sl0: UP');ଯାଞ୍ଚ୍_କରିବା('ifconfig','sl0: UP')
                    for ଅବୈଧ_ସେଟିଂସ୍ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ତ୍ରୁଟି=ଯାଞ୍ଚ୍_କରିବା('ipconfig set '+ଅବୈଧ_ସେଟିଂସ୍+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ତ୍ରୁଟି,ତ୍ରୁଟି
                        ଯାଞ୍ଚ୍_କରିବା('ipconfig','inet 10.0.2.15')
                    ଯାଞ୍ଚ୍_କରିବା('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ଯାଞ୍ଚ୍_କରିବା('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ଯାଞ୍ଚ୍_କରିବା('ip link set dev sl0 down','sl0: DOWN');ଯାଞ୍ଚ୍_କରିବା('ping -c 1 10.0.2.2; echo STATUS=$?','ତ୍ରୁଟି -100','STATUS=1')
                    ଯାଞ୍ଚ୍_କରିବା('ipconfig up','sl0: UP')
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ଯାଞ୍ଚ୍_କରିବା('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ଯାଞ୍ଚ୍_କରିବା('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['route'],'10.0.2.2 sl0')
                    ଯାଞ୍ଚ୍_କରିବା('ftpd start','FTP listening')
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['netstat'],'10.0.2.20:21','LISTEN');ଯାଞ୍ଚ୍_କରିବା('ss','LISTEN')
                    ଯାଞ୍ଚ୍_କରିବା('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ତ୍ରୁଟି -16')
                    with ftplib.FTP() as କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ:
                        କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ.connect('127.0.0.2',ପୋର୍ଟ୍_ନମ୍ଵର୍,timeout=20);କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ.login();ଡାଟା=b'Network address was changed in the guest.\n'
                        କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ.storbinary('STOR net-state.txt',io.BytesIO(ଡାଟା));받은자료=bytearray();କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ଡାଟା;କ୍ଲାଏଣ୍ଟ_ମୂଲ୍ୟ.delete('net-state.txt')
                    ଯାଞ୍ଚ୍_କରିବା('ftpd stop','FTP stopped');ଯାଞ୍ଚ୍_କରିବା('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ପାଠ୍ଯ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ପାଠ୍ଯ);assert 찾음,ପାଠ୍ଯ;return tuple(map(int,찾음.groups()))
                    전=저장값(ଯାଞ୍ଚ୍_କରିବା('df','RAM only'));ଯାଞ୍ଚ୍_କରିବା('echo disk-proof > sys-state.txt');후=저장값(ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ଯାଞ୍ଚ୍_କରିବା('rm sys-state.txt');assert 저장값(ଖୋଳ('df'))==전
                    ମୋମରୀ_ମୂଲ୍ୟ=ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ମୋମରୀ_ମୂଲ୍ୟ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['ps'],'kernel/shell');ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['uptime'],'seconds')
                    ସ୍ଥିତି_ସୂଚନା=ଯାଞ୍ଚ୍_କରିବା(ଛଦ୍ମନାମ_ମୂଲ୍ୟ['top']+' -n 2','kernel/shell');assert ସ୍ଥିତି_ସୂଚନା.count('PID SLOT STATE')==2,ସ୍ଥିତି_ସୂଚନା
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ଯାଞ୍ଚ୍_କରିବା('terminal','TERMINAL READY');ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);ପଠାନ୍ତୁ(b'vi process.txt\n');받기(b'NORMAL',ଚଳାନ୍ତୁ)
                    ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);ପଠାନ୍ତୁ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ଚଳାନ୍ତୁ)
                    ଏଣ୍ଟ୍ରି_ତାଲିକା=ଯାଞ୍ଚ୍_କରିବା('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ଏଣ୍ଟ୍ରି_ତାଲିକା);assert 찾음 and int(찾음.group(2))>0,ଏଣ୍ଟ୍ରି_ତାଲିକା
                    ଯାଞ୍ଚ୍_କରିବା('free','EL0 mapped KiB: '+찾음.group(2))
                    ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);ପଠାନ୍ତୁ(b'top\n');받기(b'PID SLOT STATE',ଚଳାନ୍ତୁ);ପଠାନ୍ତୁ(b'q');받기(b'jkoros-native> ',ଚଳାନ୍ତୁ)
                    # Test a multibyte prefix through the real shell completion path.
                    if ଛଦ୍ମନାମ_ମୂଲ୍ୟ['df']!='df':
                        ଚଳାନ୍ତୁ=len(ଲଗ୍_ଧାଡ଼ି);ପଠାନ୍ତୁ((ଛଦ୍ମନାମ_ମୂଲ୍ୟ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ଚଳାନ୍ତୁ);받기(b'jkoros-native> ',ଚଳାନ୍ତୁ)
                    ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ:
                    ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.settimeout(15);ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.connect(str(ନିୟନ୍ତ୍ରଣ_ପଥ));ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ=ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.makefile('rwb');json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline());ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.write(b'{"execute":"qmp_capabilities"}\n');ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.flush()
                    while 'return' not in json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline()):pass
                    ପଠାନ୍ତୁ((('poweroff' if 인수.poweroff_only else ଛଦ୍ମନାମ_ମୂଲ୍ୟ['poweroff'])+'\n').encode())
                    while True:
                        ଘଟଣା=json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                        if ଘଟଣା.get('event')=='SHUTDOWN':break
                    assert ଘଟଣା['data']['guest'] and ଘଟଣା['data']['reason']=='guest-shutdown',ଘଟଣା
                    assert ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=15)==0
                    ରିପୋର୍ଟ_ମୂଲ୍ୟ['shutdown']=ଘଟଣା;ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['network_trace']=ବ୍ରିଜ୍_ମୂଲ୍ୟ.ଚିହ୍ନଟ_ଲଗ୍
                assert 인수.poweroff_only or any(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['protocol']==1 and ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['direction']=='from_guest' for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ବ୍ରିଜ୍_ମୂଲ୍ୟ.ଚିହ୍ନଟ_ଲଗ୍)
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed']=True
            finally:
                if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:os.killpg(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.pid,signal.SIGTERM)
                try:ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=10)
                except subprocess.TimeoutExpired:ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill();ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
                ମନୋନୟନ_ଆଇଟମ୍.close();(ନିର୍ଗମ/'serial.log').write_bytes(ଲଗ୍_ଧାଡ଼ି);(ନିର୍ଗମ/'report.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({କୀ_ମୂଲ୍ୟ:ମୂଲ୍ୟ for କୀ_ମୂଲ୍ୟ,ମୂଲ୍ୟ in ରିପୋର୍ଟ_ମୂଲ୍ୟ.items() if କୀ_ମୂଲ୍ୟ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ଚଳାନ୍ତୁ()
