#!/usr/bin/env python3
"""실제 자체 커널의 IP/ICMP, 상태 조회, 현지어 Komando, 게스트 종료 검증."""
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


def Ruli():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');Argumentoj=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Agordoj={};이름표={}
    if Argumentoj.edition:
        나라=Argumentoj.edition.resolve();Agordoj=json.loads((나라/'native.json').read_text());이름표=Agordoj['identifiers'];기준=나라/Agordoj['source']/Agordoj['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        호스트=나라/'host/qemu'
        if 호스트.is_file():os.environ['QEMU_AARCH64']=str(호스트)
    도구=기준/Path(Agordoj.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def Lego(Nomo):
        Vojo=도구/(이름표.get(Nomo,Nomo)+'.py');규약=importlib.util.spec_from_file_location('test_'+Nomo,str(Vojo));모듈=importlib.util.module_from_spec(규약);규약.loader.exec_module(모듈);return 모듈
    실행모듈=Lego('실행');망모듈=Lego('통신다리');Komando=getattr(실행모듈,이름표.get('Komando','Komando'));다리형=getattr(망모듈,이름표.get('통신다리','통신다리'))
    별명=Agordoj.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'아이피','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'도움말'})
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
    Eligo=Argumentoj.output or 기준/'build/verification/system-tools';Eligo.mkdir(parents=True,exist_ok=True)
    보고={'passed':False,'country':Agordoj.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    기록=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        제어경로=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as 탐색:탐색.bind(('127.0.0.1',0));접속번호=탐색.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),호스트주소='127.0.0.2') as 다리:
            과정=subprocess.Popen(Komando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(제어경로)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            고르기=selectors.DefaultSelector();고르기.register(과정.stdout,selectors.EVENT_READ)
            def 받기(표시,Ruli=0,제한=45):
                끝=time.monotonic()+제한
                while 표시 not in 기록[Ruli:]:
                    if time.monotonic()>끝 or 과정.poll() is not None:raise AssertionError('Missing '+repr(표시)+'\n'+기록[Ruli:].decode('utf-8','replace'))
                    for 키,_ in 고르기.select(.1):
                        자료=키.fileobj.read(65536)
                        if 자료:기록.extend(자료)
                return 기록[Ruli:].decode('utf-8','replace').replace('\r\n','\n')
            def 보내기(자료):과정.stdin.write(자료);과정.stdin.flush()
            def 셸(Teksto):
                Teksto=ipTestText(Teksto)
                print(보고['country'],Teksto,flush=True);차례[0]+=1;표시='__SYSTEM_DONE_'+str(차례[0])+'__';Ruli=len(기록)
                보내기((Teksto+'; echo; echo '+표시+'\n').encode())
                끝표시=('\r\n'+표시+'\r\n').encode();받기(끝표시,Ruli)
                끝자리=기록.index(끝표시,Ruli)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return 기록[Ruli:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(Teksto,*값들):
                응답=셸(Teksto)
                for 값 in 값들:assert ipTestText(값) in 응답,(Teksto,값,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not Argumentoj.poweroff_only:
                    도움=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in 별명.values():assert 별칭 in 도움,(별칭,도움)
                    확인(별명['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(별명['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for 잘못된설정 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        eraro=확인('ipconfig set '+잘못된설정+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in eraro,eraro
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(별명['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','eraro -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(별명['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(별명['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(별명['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','eraro -16')
                    with ftplib.FTP() as 고객:
                        고객.connect('127.0.0.2',접속번호,timeout=20);고객.login();자료=b'Network address was changed in the guest.\n'
                        고객.storbinary('STOR net-state.txt',io.BytesIO(자료));받은자료=bytearray();고객.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==자료;고객.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    보고['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Teksto):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Teksto);assert 찾음,Teksto;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(별명['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(셸('df'))==전
                    기억=확인(별명['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',기억).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    확인(별명['ps'],'kernel/shell');확인(별명['uptime'],'seconds')
                    현황=확인(별명['top']+' -n 2','kernel/shell');assert 현황.count('PID SLOT STATE')==2,현황
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');Ruli=len(기록);보내기(b'vi process.txt\n');받기(b'NORMAL',Ruli)
                    Ruli=len(기록);보내기(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Ruli)
                    목록=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',목록);assert 찾음 and int(찾음.group(2))>0,목록
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    Ruli=len(기록);보내기(b'top\n');받기(b'PID SLOT STATE',Ruli);보내기(b'q');받기(b'jkoros-native> ',Ruli)
                    # Test a multibyte prefix through the real shell completion path.
                    if 별명['df']!='df':
                        Ruli=len(기록);보내기((별명['df'][:-1]+'\t\n').encode());받기(b'RAM only',Ruli);받기(b'jkoros-native> ',Ruli)
                    보고['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as 제어:
                    제어.settimeout(15);제어.connect(str(제어경로));흐름=제어.makefile('rwb');json.loads(흐름.readline());흐름.write(b'{"execute":"qmp_capabilities"}\n');흐름.flush()
                    while 'return' not in json.loads(흐름.readline()):pass
                    보내기((('poweroff' if Argumentoj.poweroff_only else 별명['poweroff'])+'\n').encode())
                    while True:
                        사건=json.loads(흐름.readline())
                        if 사건.get('event')=='SHUTDOWN':break
                    assert 사건['data']['guest'] and 사건['data']['reason']=='guest-shutdown',사건
                    assert 과정.wait(timeout=15)==0
                    보고['shutdown']=사건;보고['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                보고['network_trace']=다리.추적기록
                assert Argumentoj.poweroff_only or any(항목['protocol']==1 and 항목['direction']=='from_guest' for 항목 in 다리.추적기록)
                보고['passed']=True
            finally:
                if 과정.poll() is None:os.killpg(과정.pid,signal.SIGTERM)
                try:과정.wait(timeout=10)
                except subprocess.TimeoutExpired:과정.kill();과정.wait()
                고르기.close();(Eligo/'serial.log').write_bytes(기록);(Eligo/'report.json').write_text(json.dumps(보고,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({키:값 for 키,값 in 보고.items() if 키!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Ruli()
