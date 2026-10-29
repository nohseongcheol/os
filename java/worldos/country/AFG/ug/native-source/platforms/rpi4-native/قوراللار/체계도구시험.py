#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات 자체 커널의 IP/ICMP, ھالەت_قىممىتى تەكشۈرۈش_قىممىتى, 현지어 بۇيرۇق, 게스트 چىقىش_ئەپ دەلىللەش."""
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


def ئىجرا_قىل_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');ئۆزگەرگۈچىلەر=해석기.parse_args()
    كۆرسىتىش_يىلتىز=Path(__file__).resolve().parents[1];تەڭشەكلەر={};نامى_جەدۋەل={}
    if ئۆزگەرگۈچىلەر.edition:
        나라=ئۆزگەرگۈچىلەر.edition.resolve();تەڭشەكلەر=json.loads((나라/'native.json').read_text());نامى_جەدۋەل=تەڭشەكلەر['identifiers'];كۆرسىتىش_يىلتىز=나라/تەڭشەكلەر['source']/تەڭشەكلەر['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        باقار=나라/'host/qemu'
        if باقار.is_file():os.environ['QEMU_AARCH64']=str(باقار)
    قوراللار=كۆرسىتىش_يىلتىز/Path(تەڭشەكلەر.get('runner','قوراللار/ئىجرا_قىلىش_بۇيرۇق.py')).parent
    sys.path.insert(0,str(قوراللار))
    def ئوقۇ(ئاتى):
        يول=قوراللار/(نامى_جەدۋەل.get(ئاتى,ئاتى)+'.py');خىزمەت_قىممىتى=importlib.util.spec_from_file_location('test_'+ئاتى,str(يول));بۆلەك_قىممىتى_6d2d8bf4=importlib.util.module_from_spec(خىزمەت_قىممىتى);خىزمەت_قىممىتى.loader.exec_module(بۆلەك_قىممىتى_6d2d8bf4);return بۆلەك_قىممىتى_6d2d8bf4
    실행모듈=ئوقۇ('ئىجرا_قىلىش_بۇيرۇق');تور_بۆلەك=ئوقۇ('تور_كۆۋرۈك');بۇيرۇق=getattr(실행모듈,نامى_جەدۋەل.get('بۇيرۇق','بۇيرۇق'));كۆۋرۈك_تىپ=getattr(تور_بۆلەك,نامى_جەدۋەل.get('تور_كۆۋرۈك','تور_كۆۋرۈك'))
    باشقا_نام_قىممىتى=تەڭشەكلەر.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ئادرېسى','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'كۆرسەتمەك_ياردەم'})
    sys.path.insert(0,str(كۆرسىتىش_يىلتىز/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(كۆرسىتىش_يىلتىز);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    چىقار=ئۆزگەرگۈچىلەر.output or كۆرسىتىش_يىلتىز/'build/verification/system-tools';چىقار.mkdir(parents=True,exist_ok=True)
    خەۋەر_قىممىتى={'passed':False,'country':تەڭشەكلەر.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    خاتىرە_قۇر=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        كونترول_يول=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ئىزدەش_قىممىتى:ئىزدەش_قىممىتى.bind(('127.0.0.1',0));접속번호=ئىزدەش_قىممىتى.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with كۆۋرۈك_تىپ(접속번호,تۇتۇش=True,مېھمان_ئادرېس=ipTestText('10.0.2.20'),باقار_ئادرېس='127.0.0.2') as كۆۋرۈك_قىممىتى:
            جەريان_قىممىتى=subprocess.Popen(بۇيرۇق()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(كونترول_يول)]+كۆۋرۈك_قىممىتى.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            تاللىماق_تۈر=selectors.DefaultSelector();تاللىماق_تۈر.register(جەريان_قىممىتى.stdout,selectors.EVENT_READ)
            def 받기(كۆرسەتمەك_قىممىتى,ئىجرا_قىل_2=0,제한=45):
                끝=time.monotonic()+제한
                while كۆرسەتمەك_قىممىتى not in خاتىرە_قۇر[ئىجرا_قىل_2:]:
                    if time.monotonic()>끝 or جەريان_قىممىتى.poll() is not None:raise AssertionError('Missing '+repr(كۆرسەتمەك_قىممىتى)+'\n'+خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8','replace'))
                    for ئاچقۇچ_قىممىتى,_ in تاللىماق_تۈر.select(.1):
                        مەلۇمات=ئاچقۇچ_قىممىتى.fileobj.read(65536)
                        if مەلۇمات:خاتىرە_قۇر.extend(مەلۇمات)
                return خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ئەۋەتمەك(مەلۇمات):جەريان_قىممىتى.stdin.write(مەلۇمات);جەريان_قىممىتى.stdin.flush()
            def قاپ(تېكىست):
                تېكىست=ipTestText(تېكىست)
                print(خەۋەر_قىممىتى['country'],تېكىست,flush=True);차례[0]+=1;كۆرسەتمەك_قىممىتى='__SYSTEM_DONE_'+str(차례[0])+'__';ئىجرا_قىل_2=len(خاتىرە_قۇر)
                ئەۋەتمەك((تېكىست+'; echo; echo '+كۆرسەتمەك_قىممىتى+'\n').encode())
                끝표시=('\r\n'+كۆرسەتمەك_قىممىتى+'\r\n').encode();받기(끝표시,ئىجرا_قىل_2)
                تاماملىماق_ئورۇنلاشتۇرۇش=خاتىرە_قۇر.index(끝표시,ئىجرا_قىل_2)+len(끝표시)
                받기(b'jkoros-native> ',تاماملىماق_ئورۇنلاشتۇرۇش)
                return خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8','replace').replace('\r\n','\n')
            def دەلىللىمەك(تېكىست,*값들):
                جاۋابلاش=قاپ(تېكىست)
                for قىممىتى in 값들:assert ipTestText(قىممىتى) in جاۋابلاش,(تېكىست,قىممىتى,جاۋابلاش)
                return جاۋابلاش
            try:
                받기(b'jkoros-native> ')
                if not ئۆزگەرگۈچىلەر.poweroff_only:
                    ياردەم_قىممىتى=دەلىللىمەك('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in باشقا_نام_قىممىتى.values():assert 별칭 in ياردەم_قىممىتى,(별칭,ياردەم_قىممىتى)
                    دەلىللىمەك(باشقا_نام_قىممىتى['help']+' system','Network / system')
                    دەلىللىمەك('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    دەلىللىمەك(باشقا_نام_قىممىتى['ipconfig'],'inet 10.0.2.15');دەلىللىمەك('ip addr show','sl0: UP');دەلىللىمەك('ifconfig','sl0: UP')
                    for ئۈنۈمسىز_تەڭشەك in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        خاتالىق=دەلىللىمەك('ipconfig set '+ئۈنۈمسىز_تەڭشەك+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in خاتالىق,خاتالىق
                        دەلىللىمەك('ipconfig','inet 10.0.2.15')
                    دەلىللىمەك('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    دەلىللىمەك(باشقا_نام_قىممىتى['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    دەلىللىمەك('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    دەلىللىمەك('ip link set dev sl0 down','sl0: DOWN');دەلىللىمەك('ping -c 1 10.0.2.2; echo STATUS=$?','خاتالىق -100','STATUS=1')
                    دەلىللىمەك('ipconfig up','sl0: UP')
                    دەلىللىمەك(باشقا_نام_قىممىتى['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    دەلىللىمەك('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    دەلىللىمەك('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');دەلىللىمەك(باشقا_نام_قىممىتى['route'],'10.0.2.2 sl0')
                    دەلىللىمەك('ftpd start','FTP listening')
                    دەلىللىمەك(باشقا_نام_قىممىتى['netstat'],'10.0.2.20:21','LISTEN');دەلىللىمەك('ss','LISTEN')
                    دەلىللىمەك('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','خاتالىق -16')
                    with ftplib.FTP() as ئابۇنىتېر_قىممىتى:
                        ئابۇنىتېر_قىممىتى.connect('127.0.0.2',접속번호,timeout=20);ئابۇنىتېر_قىممىتى.login();مەلۇمات=b'Network address was changed in the guest.\n'
                        ئابۇنىتېر_قىممىتى.storbinary('STOR net-state.txt',io.BytesIO(مەلۇمات));받은자료=bytearray();ئابۇنىتېر_قىممىتى.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==مەلۇمات;ئابۇنىتېر_قىممىتى.delete('net-state.txt')
                    دەلىللىمەك('ftpd stop','FTP stopped');دەلىللىمەك('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    خەۋەر_قىممىتى['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(تېكىست):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',تېكىست);assert 찾음,تېكىست;return tuple(map(int,찾음.groups()))
                    전=저장값(دەلىللىمەك('df','RAM only'));دەلىللىمەك('echo disk-proof > sys-state.txt');후=저장값(دەلىللىمەك(باشقا_نام_قىممىتى['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    دەلىللىمەك('rm sys-state.txt');assert 저장값(قاپ('df'))==전
                    ساقلىغۇچ_قىممىتى=دەلىللىمەك(باشقا_نام_قىممىتى['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ساقلىغۇچ_قىممىتى).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    دەلىللىمەك(باشقا_نام_قىممىتى['ps'],'kernel/shell');دەلىللىمەك(باشقا_نام_قىممىتى['uptime'],'seconds')
                    بىكار_ئۇچۇر=دەلىللىمەك(باشقا_نام_قىممىتى['top']+' -n 2','kernel/shell');assert بىكار_ئۇچۇر.count('PID SLOT STATE')==2,بىكار_ئۇچۇر
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    دەلىللىمەك('terminal','TERMINAL READY');ئىجرا_قىل_2=len(خاتىرە_قۇر);ئەۋەتمەك(b'vi process.txt\n');받기(b'NORMAL',ئىجرا_قىل_2)
                    ئىجرا_قىل_2=len(خاتىرە_قۇر);ئەۋەتمەك(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ئىجرا_قىل_2)
                    كىرگۈزۈش_تىزىم=دەلىللىمەك('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',كىرگۈزۈش_تىزىم);assert 찾음 and int(찾음.group(2))>0,كىرگۈزۈش_تىزىم
                    دەلىللىمەك('free','EL0 mapped KiB: '+찾음.group(2))
                    ئىجرا_قىل_2=len(خاتىرە_قۇر);ئەۋەتمەك(b'top\n');받기(b'PID SLOT STATE',ئىجرا_قىل_2);ئەۋەتمەك(b'q');받기(b'jkoros-native> ',ئىجرا_قىل_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if باشقا_نام_قىممىتى['df']!='df':
                        ئىجرا_قىل_2=len(خاتىرە_قۇر);ئەۋەتمەك((باشقا_نام_قىممىتى['df'][:-1]+'\t\n').encode());받기(b'RAM only',ئىجرا_قىل_2);받기(b'jkoros-native> ',ئىجرا_قىل_2)
                    خەۋەر_قىممىتى['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as كونترول_قىممىتى:
                    كونترول_قىممىتى.settimeout(15);كونترول_قىممىتى.connect(str(كونترول_يول));ئېقىم_قىممىتى=كونترول_قىممىتى.makefile('rwb');json.loads(ئېقىم_قىممىتى.readline());ئېقىم_قىممىتى.write(b'{"execute":"qmp_capabilities"}\n');ئېقىم_قىممىتى.flush()
                    while 'return' not in json.loads(ئېقىم_قىممىتى.readline()):pass
                    ئەۋەتمەك((('poweroff' if ئۆزگەرگۈچىلەر.poweroff_only else باشقا_نام_قىممىتى['poweroff'])+'\n').encode())
                    while True:
                        ھادىسە=json.loads(ئېقىم_قىممىتى.readline())
                        if ھادىسە.get('event')=='SHUTDOWN':break
                    assert ھادىسە['data']['guest'] and ھادىسە['data']['reason']=='guest-shutdown',ھادىسە
                    assert جەريان_قىممىتى.wait(timeout=15)==0
                    خەۋەر_قىممىتى['shutdown']=ھادىسە;خەۋەر_قىممىتى['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                خەۋەر_قىممىتى['network_trace']=كۆۋرۈك_قىممىتى.추적기록
                assert ئۆزگەرگۈچىلەر.poweroff_only or any(كىرگۈزۈش_قىممىتى['protocol']==1 and كىرگۈزۈش_قىممىتى['direction']=='from_guest' for كىرگۈزۈش_قىممىتى in كۆۋرۈك_قىممىتى.추적기록)
                خەۋەر_قىممىتى['passed']=True
            finally:
                if جەريان_قىممىتى.poll() is None:os.killpg(جەريان_قىممىتى.pid,signal.SIGTERM)
                try:جەريان_قىممىتى.wait(timeout=10)
                except subprocess.TimeoutExpired:جەريان_قىممىتى.kill();جەريان_قىممىتى.wait()
                تاللىماق_تۈر.close();(چىقار/'serial.log').write_bytes(خاتىرە_قۇر);(چىقار/'report.json').write_text(json.dumps(خەۋەر_قىممىتى,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ئاچقۇچ_قىممىتى:قىممىتى for ئاچقۇچ_قىممىتى,قىممىتى in خەۋەر_قىممىتى.items() if ئاچقۇچ_قىممىتى!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ئىجرا_قىل_2()
