#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা 자체 커널의 IP/ICMP, অৱস্থা_মান কুৱেৰী_মান, 현지어 কমান্ড, 게스트 প্ৰস্থান_এপ্প্ বৈধকৰণ_কৰক."""
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


def সঞ্চালন():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];বৈশিষ্ট্য={};নাম_তালিকা={}
    if 인수.edition:
        나라=인수.edition.resolve();বৈশিষ্ট্য=json.loads((나라/'native.json').read_text());নাম_তালিকা=বৈশিষ্ট্য['identifiers'];기준=나라/বৈশিষ্ট্য['source']/বৈশিষ্ট্য['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        হ_ষ্ট=나라/'host/qemu'
        if হ_ষ্ট.is_file():os.environ['QEMU_AARCH64']=str(হ_ষ্ট)
    সঁজুলিসমূহ=기준/Path(বৈশিষ্ট্য.get('runner','সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py')).parent
    sys.path.insert(0,str(সঁজুলিসমূহ))
    def পড়া(নাম):
        পথ=সঁজুলিসমূহ/(নাম_তালিকা.get(নাম,নাম)+'.py');কেছ_মান=importlib.util.spec_from_file_location('test_'+নাম,str(পথ));মডিউল_মান=importlib.util.module_from_spec(কেছ_মান);কেছ_মান.loader.exec_module(মডিউল_মান);return মডিউল_মান
    실행모듈=পড়া('নিষ্পাদন_আদেশ');নেটৱৰ্ক_মডিউল=পড়া('নেটৱৰ্ক_ব্ৰীজ');কমান্ড=getattr(실행모듈,নাম_তালিকা.get('কমান্ড','কমান্ড'));ব্ৰীজ_প্ৰকাৰ=getattr(নেটৱৰ্ক_মডিউল,নাম_তালিকা.get('নেটৱৰ্ক_ব্ৰীজ','নেটৱৰ্ক_ব্ৰীজ'))
    উপনাম_মান=বৈশিষ্ট্য.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ঠিকনা','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'শ্ব_সহায়'})
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
    নিৰ্গম=인수.output or 기준/'build/verification/system-tools';নিৰ্গম.mkdir(parents=True,exist_ok=True)
    ৰিপ_ৰ্ট_মান={'passed':False,'country':বৈশিষ্ট্য.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    লগ_শাৰী=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        নিয়ন্ত্রণ_পথ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as অনুসন্ধান_মান:অনুসন্ধান_মান.bind(('127.0.0.1',0));접속번호=অনুসন্ধান_মান.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ব্ৰীজ_প্ৰকাৰ(접속번호,কেপচাৰ=True,অতিথি_ঠিকনা=ipTestText('10.0.2.20'),হ_ষ্ট_ঠিকনা='127.0.0.2') as ব্ৰীজ_মান:
            প্ৰক্ৰিয়া_মান=subprocess.Popen(কমান্ড()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(নিয়ন্ত্রণ_পথ)]+ব্ৰীজ_মান.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            পচন্দ_কৰক_আইটেম=selectors.DefaultSelector();পচন্দ_কৰক_আইটেম.register(প্ৰক্ৰিয়া_মান.stdout,selectors.EVENT_READ)
            def 받기(শ্ব_মান,সঞ্চালন=0,제한=45):
                끝=time.monotonic()+제한
                while শ্ব_মান not in লগ_শাৰী[সঞ্চালন:]:
                    if time.monotonic()>끝 or প্ৰক্ৰিয়া_মান.poll() is not None:raise AssertionError('Missing '+repr(শ্ব_মান)+'\n'+লগ_শাৰী[সঞ্চালন:].decode('utf-8','replace'))
                    for কী_মান,_ in পচন্দ_কৰক_আইটেম.select(.1):
                        ডাটা=কী_মান.fileobj.read(65536)
                        if ডাটা:লগ_শাৰী.extend(ডাটা)
                return লগ_শাৰী[সঞ্চালন:].decode('utf-8','replace').replace('\r\n','\n')
            def ই_মেইল_কৰক(ডাটা):প্ৰক্ৰিয়া_মান.stdin.write(ডাটা);প্ৰক্ৰিয়া_মান.stdin.flush()
            def শ্বেল(টেক্সট):
                টেক্সট=ipTestText(টেক্সট)
                print(ৰিপ_ৰ্ট_মান['country'],টেক্সট,flush=True);차례[0]+=1;শ্ব_মান='__SYSTEM_DONE_'+str(차례[0])+'__';সঞ্চালন=len(লগ_শাৰী)
                ই_মেইল_কৰক((টেক্সট+'; echo; echo '+শ্ব_মান+'\n').encode())
                끝표시=('\r\n'+শ্ব_মান+'\r\n').encode();받기(끝표시,সঞ্চালন)
                অন্ত_কৰক_স্থান_সলনি_কৰক=লগ_শাৰী.index(끝표시,সঞ্চালন)+len(끝표시)
                받기(b'jkoros-native> ',অন্ত_কৰক_স্থান_সলনি_কৰক)
                return লগ_শাৰী[সঞ্চালন:].decode('utf-8','replace').replace('\r\n','\n')
            def প্ৰমাণিত_কৰক(টেক্সট,*값들):
                প্ৰত্যুত্তৰ_দিয়ক=শ্বেল(টেক্সট)
                for মান in 값들:assert ipTestText(মান) in প্ৰত্যুত্তৰ_দিয়ক,(টেক্সট,মান,প্ৰত্যুত্তৰ_দিয়ক)
                return প্ৰত্যুত্তৰ_দিয়ক
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    সহায়_মান=প্ৰমাণিত_কৰক('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in উপনাম_মান.values():assert 별칭 in সহায়_মান,(별칭,সহায়_মান)
                    প্ৰমাণিত_কৰক(উপনাম_মান['help']+' system','Network / system')
                    প্ৰমাণিত_কৰক('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    প্ৰমাণিত_কৰক(উপনাম_মান['ipconfig'],'inet 10.0.2.15');প্ৰমাণিত_কৰক('ip addr show','sl0: UP');প্ৰমাণিত_কৰক('ifconfig','sl0: UP')
                    for অবৈধ_ছেটিংছ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ত্ৰুটি=প্ৰমাণিত_কৰক('ipconfig set '+অবৈধ_ছেটিংছ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ত্ৰুটি,ত্ৰুটি
                        প্ৰমাণিত_কৰক('ipconfig','inet 10.0.2.15')
                    প্ৰমাণিত_কৰক('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    প্ৰমাণিত_কৰক(উপনাম_মান['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    প্ৰমাণিত_কৰক('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    প্ৰমাণিত_কৰক('ip link set dev sl0 down','sl0: DOWN');প্ৰমাণিত_কৰক('ping -c 1 10.0.2.2; echo STATUS=$?','ত্ৰুটি -100','STATUS=1')
                    প্ৰমাণিত_কৰক('ipconfig up','sl0: UP')
                    প্ৰমাণিত_কৰক(উপনাম_মান['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    প্ৰমাণিত_কৰক('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    প্ৰমাণিত_কৰক('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');প্ৰমাণিত_কৰক(উপনাম_মান['route'],'10.0.2.2 sl0')
                    প্ৰমাণিত_কৰক('ftpd start','FTP listening')
                    প্ৰমাণিত_কৰক(উপনাম_মান['netstat'],'10.0.2.20:21','LISTEN');প্ৰমাণিত_কৰক('ss','LISTEN')
                    প্ৰমাণিত_কৰক('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ত্ৰুটি -16')
                    with ftplib.FTP() as ক্লায়েণ্ট_মান:
                        ক্লায়েণ্ট_মান.connect('127.0.0.2',접속번호,timeout=20);ক্লায়েণ্ট_মান.login();ডাটা=b'Network address was changed in the guest.\n'
                        ক্লায়েণ্ট_মান.storbinary('STOR net-state.txt',io.BytesIO(ডাটা));받은자료=bytearray();ক্লায়েণ্ট_মান.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ডাটা;ক্লায়েণ্ট_মান.delete('net-state.txt')
                    প্ৰমাণিত_কৰক('ftpd stop','FTP stopped');প্ৰমাণিত_কৰক('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ৰিপ_ৰ্ট_মান['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(টেক্সট):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',টেক্সট);assert 찾음,টেক্সট;return tuple(map(int,찾음.groups()))
                    전=저장값(প্ৰমাণিত_কৰক('df','RAM only'));প্ৰমাণিত_কৰক('echo disk-proof > sys-state.txt');후=저장값(প্ৰমাণিত_কৰক(উপনাম_মান['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    প্ৰমাণিত_কৰক('rm sys-state.txt');assert 저장값(শ্বেল('df'))==전
                    মেম_ৰি_মান=প্ৰমাণিত_কৰক(উপনাম_মান['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',মেম_ৰি_মান).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    প্ৰমাণিত_কৰক(উপনাম_মান['ps'],'kernel/shell');প্ৰমাণিত_কৰক(উপনাম_মান['uptime'],'seconds')
                    অৱস্থা_তথ্য=প্ৰমাণিত_কৰক(উপনাম_মান['top']+' -n 2','kernel/shell');assert অৱস্থা_তথ্য.count('PID SLOT STATE')==2,অৱস্থা_তথ্য
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    প্ৰমাণিত_কৰক('terminal','TERMINAL READY');সঞ্চালন=len(লগ_শাৰী);ই_মেইল_কৰক(b'vi process.txt\n');받기(b'NORMAL',সঞ্চালন)
                    সঞ্চালন=len(লগ_শাৰী);ই_মেইল_কৰক(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',সঞ্চালন)
                    প্রবিষ্ট_সূচী=প্ৰমাণিত_কৰক('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',প্রবিষ্ট_সূচী);assert 찾음 and int(찾음.group(2))>0,প্রবিষ্ট_সূচী
                    প্ৰমাণিত_কৰক('free','EL0 mapped KiB: '+찾음.group(2))
                    সঞ্চালন=len(লগ_শাৰী);ই_মেইল_কৰক(b'top\n');받기(b'PID SLOT STATE',সঞ্চালন);ই_মেইল_কৰক(b'q');받기(b'jkoros-native> ',সঞ্চালন)
                    # Test a multibyte prefix through the real shell completion path.
                    if উপনাম_মান['df']!='df':
                        সঞ্চালন=len(লগ_শাৰী);ই_মেইল_কৰক((উপনাম_মান['df'][:-1]+'\t\n').encode());받기(b'RAM only',সঞ্চালন);받기(b'jkoros-native> ',সঞ্চালন)
                    ৰিপ_ৰ্ট_মান['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as নিয়ন্ত্রণ_মান:
                    নিয়ন্ত্রণ_মান.settimeout(15);নিয়ন্ত্রণ_মান.connect(str(নিয়ন্ত্রণ_পথ));ষ্ট্ৰিম_মান=নিয়ন্ত্রণ_মান.makefile('rwb');json.loads(ষ্ট্ৰিম_মান.readline());ষ্ট্ৰিম_মান.write(b'{"execute":"qmp_capabilities"}\n');ষ্ট্ৰিম_মান.flush()
                    while 'return' not in json.loads(ষ্ট্ৰিম_মান.readline()):pass
                    ই_মেইল_কৰক((('poweroff' if 인수.poweroff_only else উপনাম_মান['poweroff'])+'\n').encode())
                    while True:
                        ইভেণ্ট=json.loads(ষ্ট্ৰিম_মান.readline())
                        if ইভেণ্ট.get('event')=='SHUTDOWN':break
                    assert ইভেণ্ট['data']['guest'] and ইভেণ্ট['data']['reason']=='guest-shutdown',ইভেণ্ট
                    assert প্ৰক্ৰিয়া_মান.wait(timeout=15)==0
                    ৰিপ_ৰ্ট_মান['shutdown']=ইভেণ্ট;ৰিপ_ৰ্ট_মান['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ৰিপ_ৰ্ট_মান['network_trace']=ব্ৰীজ_মান.ট্ৰেচ_লগ
                assert 인수.poweroff_only or any(প্রবিষ্ট_মান['protocol']==1 and প্রবিষ্ট_মান['direction']=='from_guest' for প্রবিষ্ট_মান in ব্ৰীজ_মান.ট্ৰেচ_লগ)
                ৰিপ_ৰ্ট_মান['passed']=True
            finally:
                if প্ৰক্ৰিয়া_মান.poll() is None:os.killpg(প্ৰক্ৰিয়া_মান.pid,signal.SIGTERM)
                try:প্ৰক্ৰিয়া_মান.wait(timeout=10)
                except subprocess.TimeoutExpired:প্ৰক্ৰিয়া_মান.kill();প্ৰক্ৰিয়া_মান.wait()
                পচন্দ_কৰক_আইটেম.close();(নিৰ্গম/'serial.log').write_bytes(লগ_শাৰী);(নিৰ্গম/'report.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({কী_মান:মান for কী_মান,মান in ৰিপ_ৰ্ট_মান.items() if কী_মান!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':সঞ্চালন()
