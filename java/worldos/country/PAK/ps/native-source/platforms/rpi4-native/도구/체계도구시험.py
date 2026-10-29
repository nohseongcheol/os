#!/usr/bin/env python3
"""실제 자체 커널의 IP/ICMP, انکړ_ارزښت پوښتنه_ارزښت, 현지어 بولۍ, 게스트 وتون_کاريال 검증."""
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


def ځغلول():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];امستنې={};이름표={}
    if 인수.edition:
        나라=인수.edition.resolve();امستنې=json.loads((나라/'native.json').read_text());이름표=امستنې['identifiers'];기준=나라/امستنې['source']/امستنې['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        کوربه=나라/'host/qemu'
        if کوربه.is_file():os.environ['QEMU_AARCH64']=str(کوربه)
    도구=기준/Path(امستنې.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def لوستل(نوم):
        يونلور=도구/(이름표.get(نوم,نوم)+'.py');کیس_ارزښت=importlib.util.spec_from_file_location('test_'+نوم,str(يونلور));모듈=importlib.util.module_from_spec(کیس_ارزښت);کیس_ارزښت.loader.exec_module(모듈);return 모듈
    실행모듈=لوستل('실행');망모듈=لوستل('통신다리');بولۍ=getattr(실행모듈,이름표.get('بولۍ','بولۍ'));다리형=getattr(망모듈,이름표.get('통신다리','통신다리'))
    لنډلار_ارزښت_0a38607b=امستنې.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_پته','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'도움말'})
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
    راپور_ارزښت={'passed':False,'country':امستنې.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    خبرال_کیل=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        مهار_يونلور=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as پلټل_ارزښت:پلټل_ارزښت.bind(('127.0.0.1',0));접속번호=پلټل_ارزښت.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),کوربه_پته='127.0.0.2') as 다리:
            과정=subprocess.Popen(بولۍ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(مهار_يونلور)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            چڼل_توک=selectors.DefaultSelector();چڼل_توک.register(과정.stdout,selectors.EVENT_READ)
            def 받기(표시,ځغلول=0,제한=45):
                끝=time.monotonic()+제한
                while 표시 not in خبرال_کیل[ځغلول:]:
                    if time.monotonic()>끝 or 과정.poll() is not None:raise AssertionError('Missing '+repr(표시)+'\n'+خبرال_کیل[ځغلول:].decode('utf-8','replace'))
                    for کيلي_ارزښت,_ in چڼل_توک.select(.1):
                        اومتوک=کيلي_ارزښت.fileobj.read(65536)
                        if اومتوک:خبرال_کیل.extend(اومتوک)
                return خبرال_کیل[ځغلول:].decode('utf-8','replace').replace('\r\n','\n')
            def استول(اومتوک):과정.stdin.write(اومتوک);과정.stdin.flush()
            def سیپۍ(ليکنه):
                ليکنه=ipTestText(ليکنه)
                print(راپور_ارزښت['country'],ليکنه,flush=True);차례[0]+=1;표시='__SYSTEM_DONE_'+str(차례[0])+'__';ځغلول=len(خبرال_کیل)
                استول((ليکنه+'; echo; echo '+표시+'\n').encode())
                끝표시=('\r\n'+표시+'\r\n').encode();받기(끝표시,ځغلول)
                끝자리=خبرال_کیل.index(끝표시,ځغلول)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return خبرال_کیل[ځغلول:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(ليکنه,*값들):
                응답=سیپۍ(ليکنه)
                for ارزښت in 값들:assert ipTestText(ارزښت) in 응답,(ليکنه,ارزښت,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    مرسته_ارزښت=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in لنډلار_ارزښت_0a38607b.values():assert 별칭 in مرسته_ارزښت,(별칭,مرسته_ارزښت)
                    확인(لنډلار_ارزښت_0a38607b['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(لنډلار_ارزښت_0a38607b['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for 잘못된설정 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        تېروتنه=확인('ipconfig set '+잘못된설정+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in تېروتنه,تېروتنه
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(لنډلار_ارزښت_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','تېروتنه -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(لنډلار_ارزښت_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(لنډلار_ارزښت_0a38607b['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(لنډلار_ارزښت_0a38607b['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','تېروتنه -16')
                    with ftplib.FTP() as پېرن_ارزښت:
                        پېرن_ارزښت.connect('127.0.0.2',접속번호,timeout=20);پېرن_ارزښت.login();اومتوک=b'Network address was changed in the guest.\n'
                        پېرن_ارزښت.storbinary('STOR net-state.txt',io.BytesIO(اومتوک));받은자료=bytearray();پېرن_ارزښت.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==اومتوک;پېرن_ارزښت.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    راپور_ارزښت['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ليکنه):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ليکنه);assert 찾음,ليکنه;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(لنډلار_ارزښت_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(سیپۍ('df'))==전
                    기억=확인(لنډلار_ارزښت_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',기억).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    확인(لنډلار_ارزښت_0a38607b['ps'],'kernel/shell');확인(لنډلار_ارزښت_0a38607b['uptime'],'seconds')
                    현황=확인(لنډلار_ارزښت_0a38607b['top']+' -n 2','kernel/shell');assert 현황.count('PID SLOT STATE')==2,현황
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');ځغلول=len(خبرال_کیل);استول(b'vi process.txt\n');받기(b'NORMAL',ځغلول)
                    ځغلول=len(خبرال_کیل);استول(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ځغلول)
                    목록=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',목록);assert 찾음 and int(찾음.group(2))>0,목록
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    ځغلول=len(خبرال_کیل);استول(b'top\n');받기(b'PID SLOT STATE',ځغلول);استول(b'q');받기(b'jkoros-native> ',ځغلول)
                    # Test a multibyte prefix through the real shell completion path.
                    if لنډلار_ارزښت_0a38607b['df']!='df':
                        ځغلول=len(خبرال_کیل);استول((لنډلار_ارزښت_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',ځغلول);받기(b'jkoros-native> ',ځغلول)
                    راپور_ارزښت['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as مهار_ارزښت:
                    مهار_ارزښت.settimeout(15);مهار_ارزښت.connect(str(مهار_يونلور));بهنګ_ارزښت=مهار_ارزښت.makefile('rwb');json.loads(بهنګ_ارزښت.readline());بهنګ_ارزښت.write(b'{"execute":"qmp_capabilities"}\n');بهنګ_ارزښت.flush()
                    while 'return' not in json.loads(بهنګ_ارزښت.readline()):pass
                    استول((('poweroff' if 인수.poweroff_only else لنډلار_ارزښت_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        پېښه=json.loads(بهنګ_ارزښت.readline())
                        if پېښه.get('event')=='SHUTDOWN':break
                    assert پېښه['data']['guest'] and پېښه['data']['reason']=='guest-shutdown',پېښه
                    assert 과정.wait(timeout=15)==0
                    راپور_ارزښت['shutdown']=پېښه;راپور_ارزښت['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                راپور_ارزښت['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(ننوت_ارزښت['protocol']==1 and ننوت_ارزښت['direction']=='from_guest' for ننوت_ارزښت in 다리.추적기록)
                راپور_ارزښت['passed']=True
            finally:
                if 과정.poll() is None:os.killpg(과정.pid,signal.SIGTERM)
                try:과정.wait(timeout=10)
                except subprocess.TimeoutExpired:과정.kill();과정.wait()
                چڼل_توک.close();(출력/'serial.log').write_bytes(خبرال_کیل);(출력/'report.json').write_text(json.dumps(راپور_ارزښت,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({کيلي_ارزښت:ارزښت for کيلي_ارزښت,ارزښت in راپور_ارزښت.items() if کيلي_ارزښت!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ځغلول()
