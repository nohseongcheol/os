#!/usr/bin/env python3
"""ڕاستەکی_دەیتا 자체 커널의 IP/ICMP, دۆخ_نرخ پرس_نرخ, 현지어 فەرمان, 게스트 بزربوون_بەرنامە ڕەوایی."""
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


def ڕادان():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];ڕێكبەندەكان={};ناو_خشتە={}
    if 인수.edition:
        나라=인수.edition.resolve();ڕێكبەندەكان=json.loads((나라/'native.json').read_text());ناو_خشتە=ڕێكبەندەكان['identifiers'];기준=나라/ڕێكبەندەكان['source']/ڕێكبەندەكان['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        جێدەر=나라/'host/qemu'
        if جێدەر.is_file():os.environ['QEMU_AARCH64']=str(جێدەر)
    ئامرازەکان=기준/Path(ڕێكبەندەكان.get('runner','ئامرازەکان/جێبەجێکردن_فەرمان.py')).parent
    sys.path.insert(0,str(ئامرازەکان))
    def 읽기(ناو):
        گوزەر=ئامرازەکان/(ناو_خشتە.get(ناو,ناو)+'.py');ئەرک_نرخ=importlib.util.spec_from_file_location('test_'+ناو,str(گوزەر));모듈=importlib.util.module_from_spec(ئەرک_نرخ);ئەرک_نرخ.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('جێبەجێکردن_فەرمان');망모듈=읽기('통신다리');فەرمان=getattr(실행모듈,ناو_خشتە.get('فەرمان','فەرمان'));다리형=getattr(망모듈,ناو_خشتە.get('통신다리','통신다리'))
    نازناو_نرخ=ڕێكبەندەكان.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ناونیشانی_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'نیشاندان_ڕێنوێنی'})
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
    ڕاپۆرت_نرخ={'passed':False,'country':ڕێكبەندەكان.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    تۆمار_ڕزن=bytearray();زنجیره_نرخ=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        کۆنترۆڵ_گوزەر=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as گەڕان_نرخ:گەڕان_نرخ.bind(('127.0.0.1',0));접속번호=گەڕان_نرخ.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,تۆمارکردن=True,게스트주소=ipTestText('10.0.2.20'),جێدەر_ناونیشان='127.0.0.2') as 다리:
            پرۆسە_نرخ=subprocess.Popen(فەرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(کۆنترۆڵ_گوزەر)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            هەڵبژاردن_ئایتم=selectors.DefaultSelector();هەڵبژاردن_ئایتم.register(پرۆسە_نرخ.stdout,selectors.EVENT_READ)
            def 받기(نیشاندان_نرخ,ڕادان=0,제한=45):
                끝=time.monotonic()+제한
                while نیشاندان_نرخ not in تۆمار_ڕزن[ڕادان:]:
                    if time.monotonic()>끝 or پرۆسە_نرخ.poll() is not None:raise AssertionError('Missing '+repr(نیشاندان_نرخ)+'\n'+تۆمار_ڕزن[ڕادان:].decode('utf-8','replace'))
                    for کلیل_نرخ,_ in هەڵبژاردن_ئایتم.select(.1):
                        دەیتا=کلیل_نرخ.fileobj.read(65536)
                        if دەیتا:تۆمار_ڕزن.extend(دەیتا)
                return تۆمار_ڕزن[ڕادان:].decode('utf-8','replace').replace('\r\n','\n')
            def ناردن(دەیتا):پرۆسە_نرخ.stdin.write(دەیتا);پرۆسە_نرخ.stdin.flush()
            def توێکڵ(دەق):
                دەق=ipTestText(دەق)
                print(ڕاپۆرت_نرخ['country'],دەق,flush=True);زنجیره_نرخ[0]+=1;نیشاندان_نرخ='__SYSTEM_DONE_'+str(زنجیره_نرخ[0])+'__';ڕادان=len(تۆمار_ڕزن)
                ناردن((دەق+'; echo; echo '+نیشاندان_نرخ+'\n').encode())
                끝표시=('\r\n'+نیشاندان_نرخ+'\r\n').encode();받기(끝표시,ڕادان)
                끝자리=تۆمار_ڕزن.index(끝표시,ڕادان)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return تۆمار_ڕزن[ڕادان:].decode('utf-8','replace').replace('\r\n','\n')
            def سەلماندن(دەق,*값들):
                وەڵامدانەوه=توێکڵ(دەق)
                for نرخ in 값들:assert ipTestText(نرخ) in وەڵامدانەوه,(دەق,نرخ,وەڵامدانەوه)
                return وەڵامدانەوه
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ڕێنوێنی_نرخ=سەلماندن('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in نازناو_نرخ.values():assert 별칭 in ڕێنوێنی_نرخ,(별칭,ڕێنوێنی_نرخ)
                    سەلماندن(نازناو_نرخ['help']+' system','Network / system')
                    سەلماندن('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    سەلماندن(نازناو_نرخ['ipconfig'],'inet 10.0.2.15');سەلماندن('ip addr show','sl0: UP');سەلماندن('ifconfig','sl0: UP')
                    for بێبایەخ_ڕێكبەندەكان in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        هەڵە=سەلماندن('ipconfig set '+بێبایەخ_ڕێكبەندەكان+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in هەڵە,هەڵە
                        سەلماندن('ipconfig','inet 10.0.2.15')
                    سەلماندن('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    سەلماندن(نازناو_نرخ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    سەلماندن('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    سەلماندن('ip link set dev sl0 down','sl0: DOWN');سەلماندن('ping -c 1 10.0.2.2; echo STATUS=$?','هەڵە -100','STATUS=1')
                    سەلماندن('ipconfig up','sl0: UP')
                    سەلماندن(نازناو_نرخ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    سەلماندن('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    سەلماندن('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');سەلماندن(نازناو_نرخ['route'],'10.0.2.2 sl0')
                    سەلماندن('ftpd start','FTP listening')
                    سەلماندن(نازناو_نرخ['netstat'],'10.0.2.20:21','LISTEN');سەلماندن('ss','LISTEN')
                    سەلماندن('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','هەڵە -16')
                    with ftplib.FTP() as کلایەنت_نرخ:
                        کلایەنت_نرخ.connect('127.0.0.2',접속번호,timeout=20);کلایەنت_نرخ.login();دەیتا=b'Network address was changed in the guest.\n'
                        کلایەنت_نرخ.storbinary('STOR net-state.txt',io.BytesIO(دەیتا));받은자료=bytearray();کلایەنت_نرخ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==دەیتا;کلایەنت_نرخ.delete('net-state.txt')
                    سەلماندن('ftpd stop','FTP stopped');سەلماندن('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ڕاپۆرت_نرخ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(دەق):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',دەق);assert 찾음,دەق;return tuple(map(int,찾음.groups()))
                    전=저장값(سەلماندن('df','RAM only'));سەلماندن('echo disk-proof > sys-state.txt');후=저장값(سەلماندن(نازناو_نرخ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    سەلماندن('rm sys-state.txt');assert 저장값(توێکڵ('df'))==전
                    بیرگە_نرخ=سەلماندن(نازناو_نرخ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',بیرگە_نرخ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    سەلماندن(نازناو_نرخ['ps'],'kernel/shell');سەلماندن(نازناو_نرخ['uptime'],'seconds')
                    دۆخ_زانیاری=سەلماندن(نازناو_نرخ['top']+' -n 2','kernel/shell');assert دۆخ_زانیاری.count('PID SLOT STATE')==2,دۆخ_زانیاری
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    سەلماندن('terminal','TERMINAL READY');ڕادان=len(تۆمار_ڕزن);ناردن(b'vi process.txt\n');받기(b'NORMAL',ڕادان)
                    ڕادان=len(تۆمار_ڕزن);ناردن(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ڕادان)
                    تێنووسین_لیست=سەلماندن('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',تێنووسین_لیست);assert 찾음 and int(찾음.group(2))>0,تێنووسین_لیست
                    سەلماندن('free','EL0 mapped KiB: '+찾음.group(2))
                    ڕادان=len(تۆمار_ڕزن);ناردن(b'top\n');받기(b'PID SLOT STATE',ڕادان);ناردن(b'q');받기(b'jkoros-native> ',ڕادان)
                    # Test a multibyte prefix through the real shell completion path.
                    if نازناو_نرخ['df']!='df':
                        ڕادان=len(تۆمار_ڕزن);ناردن((نازناو_نرخ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ڕادان);받기(b'jkoros-native> ',ڕادان)
                    ڕاپۆرت_نرخ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as کۆنترۆڵ_نرخ:
                    کۆنترۆڵ_نرخ.settimeout(15);کۆنترۆڵ_نرخ.connect(str(کۆنترۆڵ_گوزەر));Stream_نرخ=کۆنترۆڵ_نرخ.makefile('rwb');json.loads(Stream_نرخ.readline());Stream_نرخ.write(b'{"execute":"qmp_capabilities"}\n');Stream_نرخ.flush()
                    while 'return' not in json.loads(Stream_نرخ.readline()):pass
                    ناردن((('poweroff' if 인수.poweroff_only else نازناو_نرخ['poweroff'])+'\n').encode())
                    while True:
                        پێشهات=json.loads(Stream_نرخ.readline())
                        if پێشهات.get('event')=='SHUTDOWN':break
                    assert پێشهات['data']['guest'] and پێشهات['data']['reason']=='guest-shutdown',پێشهات
                    assert پرۆسە_نرخ.wait(timeout=15)==0
                    ڕاپۆرت_نرخ['shutdown']=پێشهات;ڕاپۆرت_نرخ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ڕاپۆرت_نرخ['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(تێنووسین_نرخ['protocol']==1 and تێنووسین_نرخ['direction']=='from_guest' for تێنووسین_نرخ in 다리.추적기록)
                ڕاپۆرت_نرخ['passed']=True
            finally:
                if پرۆسە_نرخ.poll() is None:os.killpg(پرۆسە_نرخ.pid,signal.SIGTERM)
                try:پرۆسە_نرخ.wait(timeout=10)
                except subprocess.TimeoutExpired:پرۆسە_نرخ.kill();پرۆسە_نرخ.wait()
                هەڵبژاردن_ئایتم.close();(출력/'serial.log').write_bytes(تۆمار_ڕزن);(출력/'report.json').write_text(json.dumps(ڕاپۆرت_نرخ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({کلیل_نرخ:نرخ for کلیل_نرخ,نرخ in ڕاپۆرت_نرخ.items() if کلیل_نرخ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ڕادان()
