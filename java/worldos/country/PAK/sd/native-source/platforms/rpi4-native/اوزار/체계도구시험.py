#!/usr/bin/env python3
"""اصلي_ڪوائف 자체 커널의 IP/ICMP, حالت_قدر سوال_قدر, 현지어 حڪم, 게스트 خارج_ڪريو_ائپ ڪارگر_ڪريو."""
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


def هلائڻ():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];سيٽنگون={};نالو_جدول={}
    if 인수.edition:
        나라=인수.edition.resolve();سيٽنگون=json.loads((나라/'native.json').read_text());نالو_جدول=سيٽنگون['identifiers'];기준=나라/سيٽنگون['source']/سيٽنگون['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        مهمان=나라/'host/qemu'
        if مهمان.is_file():os.environ['QEMU_AARCH64']=str(مهمان)
    اوزار=기준/Path(سيٽنگون.get('runner','اوزار/تعميل_ڪرڻ_حڪم.py')).parent
    sys.path.insert(0,str(اوزار))
    def 읽기(نالو):
        راههه=اوزار/(نالو_جدول.get(نالو,نالو)+'.py');حالت_قدر_102996da=importlib.util.spec_from_file_location('test_'+نالو,str(راههه));모듈=importlib.util.module_from_spec(حالت_قدر_102996da);حالت_قدر_102996da.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('تعميل_ڪرڻ_حڪم');망모듈=읽기('통신다리');حڪم=getattr(실행모듈,نالو_جدول.get('حڪم','حڪم'));다리형=getattr(망모듈,نالو_جدول.get('통신다리','통신다리'))
    عرف_قدر=سيٽنگون.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'پتو_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'نمائش_ڪريو_مدد'})
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
    رپورٽ_قدر={'passed':False,'country':سيٽنگون.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    لاگ_صف=bytearray();ترتيب_قدر_e9fa7815=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ڪنٽرول_راههه=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ڳولا_قدر:ڳولا_قدر.bind(('127.0.0.1',0));접속번호=ڳولا_قدر.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,ڪيپچر=True,게스트주소=ipTestText('10.0.2.20'),مهمان_پتو='127.0.0.2') as 다리:
            عمل_قدر=subprocess.Popen(حڪم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ڪنٽرول_راههه)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            چونڊ_ڪريو_شي=selectors.DefaultSelector();چونڊ_ڪريو_شي.register(عمل_قدر.stdout,selectors.EVENT_READ)
            def 받기(نمائش_ڪريو_قدر,هلائڻ=0,제한=45):
                끝=time.monotonic()+제한
                while نمائش_ڪريو_قدر not in لاگ_صف[هلائڻ:]:
                    if time.monotonic()>끝 or عمل_قدر.poll() is not None:raise AssertionError('Missing '+repr(نمائش_ڪريو_قدر)+'\n'+لاگ_صف[هلائڻ:].decode('utf-8','replace'))
                    for ڪليد_قدر,_ in چونڊ_ڪريو_شي.select(.1):
                        ڪوائف=ڪليد_قدر.fileobj.read(65536)
                        if ڪوائف:لاگ_صف.extend(ڪوائف)
                return لاگ_صف[هلائڻ:].decode('utf-8','replace').replace('\r\n','\n')
            def اي_ميل(ڪوائف):عمل_قدر.stdin.write(ڪوائف);عمل_قدر.stdin.flush()
            def شيل(متن):
                متن=ipTestText(متن)
                print(رپورٽ_قدر['country'],متن,flush=True);ترتيب_قدر_e9fa7815[0]+=1;نمائش_ڪريو_قدر='__SYSTEM_DONE_'+str(ترتيب_قدر_e9fa7815[0])+'__';هلائڻ=len(لاگ_صف)
                اي_ميل((متن+'; echo; echo '+نمائش_ڪريو_قدر+'\n').encode())
                끝표시=('\r\n'+نمائش_ڪريو_قدر+'\r\n').encode();받기(끝표시,هلائڻ)
                끝자리=لاگ_صف.index(끝표시,هلائڻ)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return لاگ_صف[هلائڻ:].decode('utf-8','replace').replace('\r\n','\n')
            def تصديق_ڪريو(متن,*값들):
                جواب_ڏيو=شيل(متن)
                for قدر in 값들:assert ipTestText(قدر) in جواب_ڏيو,(متن,قدر,جواب_ڏيو)
                return جواب_ڏيو
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    مدد_قدر=تصديق_ڪريو('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in عرف_قدر.values():assert 별칭 in مدد_قدر,(별칭,مدد_قدر)
                    تصديق_ڪريو(عرف_قدر['help']+' system','Network / system')
                    تصديق_ڪريو('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    تصديق_ڪريو(عرف_قدر['ipconfig'],'inet 10.0.2.15');تصديق_ڪريو('ip addr show','sl0: UP');تصديق_ڪريو('ifconfig','sl0: UP')
                    for ناجائز_سيٽنگون in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        نقص=تصديق_ڪريو('ipconfig set '+ناجائز_سيٽنگون+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in نقص,نقص
                        تصديق_ڪريو('ipconfig','inet 10.0.2.15')
                    تصديق_ڪريو('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    تصديق_ڪريو(عرف_قدر['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصديق_ڪريو('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    تصديق_ڪريو('ip link set dev sl0 down','sl0: DOWN');تصديق_ڪريو('ping -c 1 10.0.2.2; echo STATUS=$?','نقص -100','STATUS=1')
                    تصديق_ڪريو('ipconfig up','sl0: UP')
                    تصديق_ڪريو(عرف_قدر['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    تصديق_ڪريو('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصديق_ڪريو('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');تصديق_ڪريو(عرف_قدر['route'],'10.0.2.2 sl0')
                    تصديق_ڪريو('ftpd start','FTP listening')
                    تصديق_ڪريو(عرف_قدر['netstat'],'10.0.2.20:21','LISTEN');تصديق_ڪريو('ss','LISTEN')
                    تصديق_ڪريو('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','نقص -16')
                    with ftplib.FTP() as گراهڪ_قدر:
                        گراهڪ_قدر.connect('127.0.0.2',접속번호,timeout=20);گراهڪ_قدر.login();ڪوائف=b'Network address was changed in the guest.\n'
                        گراهڪ_قدر.storbinary('STOR net-state.txt',io.BytesIO(ڪوائف));받은자료=bytearray();گراهڪ_قدر.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ڪوائف;گراهڪ_قدر.delete('net-state.txt')
                    تصديق_ڪريو('ftpd stop','FTP stopped');تصديق_ڪريو('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    رپورٽ_قدر['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(متن):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',متن);assert 찾음,متن;return tuple(map(int,찾음.groups()))
                    전=저장값(تصديق_ڪريو('df','RAM only'));تصديق_ڪريو('echo disk-proof > sys-state.txt');후=저장값(تصديق_ڪريو(عرف_قدر['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    تصديق_ڪريو('rm sys-state.txt');assert 저장값(شيل('df'))==전
                    ميموري_قدر=تصديق_ڪريو(عرف_قدر['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ميموري_قدر).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    تصديق_ڪريو(عرف_قدر['ps'],'kernel/shell');تصديق_ڪريو(عرف_قدر['uptime'],'seconds')
                    حالت_معلومات=تصديق_ڪريو(عرف_قدر['top']+' -n 2','kernel/shell');assert حالت_معلومات.count('PID SLOT STATE')==2,حالت_معلومات
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    تصديق_ڪريو('terminal','TERMINAL READY');هلائڻ=len(لاگ_صف);اي_ميل(b'vi process.txt\n');받기(b'NORMAL',هلائڻ)
                    هلائڻ=len(لاگ_صف);اي_ميل(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',هلائڻ)
                    داخلا_فهرست=تصديق_ڪريو('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',داخلا_فهرست);assert 찾음 and int(찾음.group(2))>0,داخلا_فهرست
                    تصديق_ڪريو('free','EL0 mapped KiB: '+찾음.group(2))
                    هلائڻ=len(لاگ_صف);اي_ميل(b'top\n');받기(b'PID SLOT STATE',هلائڻ);اي_ميل(b'q');받기(b'jkoros-native> ',هلائڻ)
                    # Test a multibyte prefix through the real shell completion path.
                    if عرف_قدر['df']!='df':
                        هلائڻ=len(لاگ_صف);اي_ميل((عرف_قدر['df'][:-1]+'\t\n').encode());받기(b'RAM only',هلائڻ);받기(b'jkoros-native> ',هلائڻ)
                    رپورٽ_قدر['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ڪنٽرول_قدر:
                    ڪنٽرول_قدر.settimeout(15);ڪنٽرول_قدر.connect(str(ڪنٽرول_راههه));اسٽريم_قدر=ڪنٽرول_قدر.makefile('rwb');json.loads(اسٽريم_قدر.readline());اسٽريم_قدر.write(b'{"execute":"qmp_capabilities"}\n');اسٽريم_قدر.flush()
                    while 'return' not in json.loads(اسٽريم_قدر.readline()):pass
                    اي_ميل((('poweroff' if 인수.poweroff_only else عرف_قدر['poweroff'])+'\n').encode())
                    while True:
                        واقعو=json.loads(اسٽريم_قدر.readline())
                        if واقعو.get('event')=='SHUTDOWN':break
                    assert واقعو['data']['guest'] and واقعو['data']['reason']=='guest-shutdown',واقعو
                    assert عمل_قدر.wait(timeout=15)==0
                    رپورٽ_قدر['shutdown']=واقعو;رپورٽ_قدر['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                رپورٽ_قدر['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(داخلا_قدر['protocol']==1 and داخلا_قدر['direction']=='from_guest' for داخلا_قدر in 다리.추적기록)
                رپورٽ_قدر['passed']=True
            finally:
                if عمل_قدر.poll() is None:os.killpg(عمل_قدر.pid,signal.SIGTERM)
                try:عمل_قدر.wait(timeout=10)
                except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
                چونڊ_ڪريو_شي.close();(출력/'serial.log').write_bytes(لاگ_صف);(출력/'report.json').write_text(json.dumps(رپورٽ_قدر,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ڪليد_قدر:قدر for ڪليد_قدر,قدر in رپورٽ_قدر.items() if ڪليد_قدر!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':هلائڻ()
