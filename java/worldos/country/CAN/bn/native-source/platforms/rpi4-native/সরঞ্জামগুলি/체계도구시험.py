#!/usr/bin/env python3
"""প্রকৃত_ডাটা নিজ 커널의 IP/ICMP, অবস্হা_মান জিজ্ঞাসা_মান, 현지어 আদেশ, 게스트 প্রস্থান_অ্যাপ বৈধ_করুন."""
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


def চালনা():
    পার্সার_48ee4b1b=argparse.ArgumentParser();পার্সার_48ee4b1b.add_argument('--edition',type=Path);পার্সার_48ee4b1b.add_argument('--output',type=Path);পার্সার_48ee4b1b.add_argument('--poweroff-only',action='store_true');আর্গুমেন্ট_তালিকা=পার্সার_48ee4b1b.parse_args()
    প্রকল্প_মূল=Path(__file__).resolve().parents[1];সেটিংস={};নাম_সারণি={}
    if আর্গুমেন্ট_তালিকা.edition:
        나라=আর্গুমেন্ট_তালিকা.edition.resolve();সেটিংস=json.loads((나라/'native.json').read_text());নাম_সারণি=সেটিংস['identifiers'];প্রকল্প_মূল=나라/সেটিংস['source']/সেটিংস['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        হোস্ট=나라/'host/qemu'
        if হোস্ট.is_file():os.environ['QEMU_AARCH64']=str(হোস্ট)
    সরঞ্জামগুলি=প্রকল্প_মূল/Path(সেটিংস.get('runner','সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py')).parent
    sys.path.insert(0,str(সরঞ্জামগুলি))
    def পড়া(নাম):
        পথ_2=সরঞ্জামগুলি/(নাম_সারণি.get(নাম,নাম)+'.py');কাজ_মান=importlib.util.spec_from_file_location('test_'+নাম,str(পথ_2));মডিউল_মান=importlib.util.module_from_spec(কাজ_মান);কাজ_মান.loader.exec_module(মডিউল_মান);return মডিউল_মান
    실행모듈=পড়া('কার্যকর_করুন_আদেশ');নেটওয়ার্ক_মডিউল=পড়া('নেটওয়ার্ক_ব্রিজ');আদেশ=getattr(실행모듈,নাম_সারণি.get('আদেশ','আদেশ'));ব্রিজ_টাইপ_করুন=getattr(নেটওয়ার্ক_মডিউল,নাম_সারণি.get('নেটওয়ার্ক_ব্রিজ','নেটওয়ার্ক_ব্রিজ'))
    ওরফে_মান=সেটিংস.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ঠিকানা','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'সহায়তা_দেখানো'})
    sys.path.insert(0,str(প্রকল্প_মূল/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(প্রকল্প_মূল);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    নির্গম=আর্গুমেন্ট_তালিকা.output or প্রকল্প_মূল/'build/verification/system-tools';নির্গম.mkdir(parents=True,exist_ok=True)
    রিপোর্ট_মান={'passed':False,'country':সেটিংস.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    লগ_সারি=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        নিয়ন্ত্রণ_পথ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as দেখুন_মান:দেখুন_মান.bind(('127.0.0.1',0));পোর্ট_নম্বর=দেখুন_মান.getsockname()[1]
            if not 50000<=পোর্ট_নম্বর<=50007:break
        with ব্রিজ_টাইপ_করুন(পোর্ট_নম্বর,ক্যাপচার=True,অতিথি_ইমেইল=ipTestText('10.0.2.20'),হোস্ট_ইমেইল='127.0.0.2') as ব্রিজ_মান:
            প্রসেসর_মান=subprocess.Popen(আদেশ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(নিয়ন্ত্রণ_পথ)]+ব্রিজ_মান.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            চয়ন_করা_দফা=selectors.DefaultSelector();চয়ন_করা_দফা.register(প্রসেসর_মান.stdout,selectors.EVENT_READ)
            def 받기(শো_মান,চালনা=0,제한=45):
                끝=time.monotonic()+제한
                while শো_মান not in লগ_সারি[চালনা:]:
                    if time.monotonic()>끝 or প্রসেসর_মান.poll() is not None:raise AssertionError('Missing '+repr(শো_মান)+'\n'+লগ_সারি[চালনা:].decode('utf-8','replace'))
                    for কী_মান,_ in চয়ন_করা_দফা.select(.1):
                        ডাটা=কী_মান.fileobj.read(65536)
                        if ডাটা:লগ_সারি.extend(ডাটা)
                return লগ_সারি[চালনা:].decode('utf-8','replace').replace('\r\n','\n')
            def পাঠান(ডাটা):প্রসেসর_মান.stdin.write(ডাটা);প্রসেসর_মান.stdin.flush()
            def শেল(পাঠ):
                পাঠ=ipTestText(পাঠ)
                print(রিপোর্ট_মান['country'],পাঠ,flush=True);차례[0]+=1;শো_মান='__SYSTEM_DONE_'+str(차례[0])+'__';চালনা=len(লগ_সারি)
                পাঠান((পাঠ+'; echo; echo '+শো_মান+'\n').encode())
                끝표시=('\r\n'+শো_মান+'\r\n').encode();받기(끝표시,চালনা)
                শেষ_করা_পদ=লগ_সারি.index(끝표시,চালনা)+len(끝표시)
                받기(b'jkoros-native> ',শেষ_করা_পদ)
                return লগ_সারি[চালনা:].decode('utf-8','replace').replace('\r\n','\n')
            def যাচাই_করা(পাঠ,*값들):
                উত্তর_দিন=শেল(পাঠ)
                for মান in 값들:assert ipTestText(মান) in উত্তর_দিন,(পাঠ,মান,উত্তর_দিন)
                return উত্তর_দিন
            try:
                받기(b'jkoros-native> ')
                if not আর্গুমেন্ট_তালিকা.poweroff_only:
                    সহায়তা_মান=যাচাই_করা('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ওরফে_মান.values():assert 별칭 in সহায়তা_মান,(별칭,সহায়তা_মান)
                    যাচাই_করা(ওরফে_মান['help']+' system','Network / system')
                    যাচাই_করা('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    যাচাই_করা(ওরফে_মান['ipconfig'],'inet 10.0.2.15');যাচাই_করা('ip addr show','sl0: UP');যাচাই_করা('ifconfig','sl0: UP')
                    for অবৈধ_সেটিংস in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ত্রুটি=যাচাই_করা('ipconfig set '+অবৈধ_সেটিংস+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ত্রুটি,ত্রুটি
                        যাচাই_করা('ipconfig','inet 10.0.2.15')
                    যাচাই_করা('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    যাচাই_করা(ওরফে_মান['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    যাচাই_করা('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    যাচাই_করা('ip link set dev sl0 down','sl0: DOWN');যাচাই_করা('ping -c 1 10.0.2.2; echo STATUS=$?','ত্রুটি -100','STATUS=1')
                    যাচাই_করা('ipconfig up','sl0: UP')
                    যাচাই_করা(ওরফে_মান['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    যাচাই_করা('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    যাচাই_করা('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');যাচাই_করা(ওরফে_মান['route'],'10.0.2.2 sl0')
                    যাচাই_করা('ftpd start','FTP listening')
                    যাচাই_করা(ওরফে_মান['netstat'],'10.0.2.20:21','LISTEN');যাচাই_করা('ss','LISTEN')
                    যাচাই_করা('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ত্রুটি -16')
                    with ftplib.FTP() as গ্রাহক_মান:
                        গ্রাহক_মান.connect('127.0.0.2',পোর্ট_নম্বর,timeout=20);গ্রাহক_মান.login();ডাটা=b'Network address was changed in the guest.\n'
                        গ্রাহক_মান.storbinary('STOR net-state.txt',io.BytesIO(ডাটা));받은자료=bytearray();গ্রাহক_মান.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ডাটা;গ্রাহক_মান.delete('net-state.txt')
                    যাচাই_করা('ftpd stop','FTP stopped');যাচাই_করা('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    রিপোর্ট_মান['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(পাঠ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',পাঠ);assert 찾음,পাঠ;return tuple(map(int,찾음.groups()))
                    전=저장값(যাচাই_করা('df','RAM only'));যাচাই_করা('echo disk-proof > sys-state.txt');후=저장값(যাচাই_করা(ওরফে_মান['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    যাচাই_করা('rm sys-state.txt');assert 저장값(শেল('df'))==전
                    মেমরি_মান=যাচাই_করা(ওরফে_মান['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',মেমরি_মান).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    যাচাই_করা(ওরফে_মান['ps'],'kernel/shell');যাচাই_করা(ওরফে_মান['uptime'],'seconds')
                    অবস্থা_তথ্য=যাচাই_করা(ওরফে_মান['top']+' -n 2','kernel/shell');assert অবস্থা_তথ্য.count('PID SLOT STATE')==2,অবস্থা_তথ্য
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    যাচাই_করা('terminal','TERMINAL READY');চালনা=len(লগ_সারি);পাঠান(b'vi process.txt\n');받기(b'NORMAL',চালনা)
                    চালনা=len(লগ_সারি);পাঠান(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',চালনা)
                    ভুক্তি_তালিকা=যাচাই_করা('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ভুক্তি_তালিকা);assert 찾음 and int(찾음.group(2))>0,ভুক্তি_তালিকা
                    যাচাই_করা('free','EL0 mapped KiB: '+찾음.group(2))
                    চালনা=len(লগ_সারি);পাঠান(b'top\n');받기(b'PID SLOT STATE',চালনা);পাঠান(b'q');받기(b'jkoros-native> ',চালনা)
                    # Test a multibyte prefix through the real shell completion path.
                    if ওরফে_মান['df']!='df':
                        চালনা=len(লগ_সারি);পাঠান((ওরফে_মান['df'][:-1]+'\t\n').encode());받기(b'RAM only',চালনা);받기(b'jkoros-native> ',চালনা)
                    রিপোর্ট_মান['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as নিয়ন্ত্রণ_মান:
                    নিয়ন্ত্রণ_মান.settimeout(15);নিয়ন্ত্রণ_মান.connect(str(নিয়ন্ত্রণ_পথ));প্রবাহ_মান=নিয়ন্ত্রণ_মান.makefile('rwb');json.loads(প্রবাহ_মান.readline());প্রবাহ_মান.write(b'{"execute":"qmp_capabilities"}\n');প্রবাহ_মান.flush()
                    while 'return' not in json.loads(প্রবাহ_মান.readline()):pass
                    পাঠান((('poweroff' if আর্গুমেন্ট_তালিকা.poweroff_only else ওরফে_মান['poweroff'])+'\n').encode())
                    while True:
                        ঘটনা=json.loads(প্রবাহ_মান.readline())
                        if ঘটনা.get('event')=='SHUTDOWN':break
                    assert ঘটনা['data']['guest'] and ঘটনা['data']['reason']=='guest-shutdown',ঘটনা
                    assert প্রসেসর_মান.wait(timeout=15)==0
                    রিপোর্ট_মান['shutdown']=ঘটনা;রিপোর্ট_মান['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                রিপোর্ট_মান['network_trace']=ব্রিজ_মান.ট্রেস_লগ
                assert আর্গুমেন্ট_তালিকা.poweroff_only or any(ভুক্তি_মান['protocol']==1 and ভুক্তি_মান['direction']=='from_guest' for ভুক্তি_মান in ব্রিজ_মান.ট্রেস_লগ)
                রিপোর্ট_মান['passed']=True
            finally:
                if প্রসেসর_মান.poll() is None:os.killpg(প্রসেসর_মান.pid,signal.SIGTERM)
                try:প্রসেসর_মান.wait(timeout=10)
                except subprocess.TimeoutExpired:প্রসেসর_মান.kill();প্রসেসর_মান.wait()
                চয়ন_করা_দফা.close();(নির্গম/'serial.log').write_bytes(লগ_সারি);(নির্গম/'report.json').write_text(json.dumps(রিপোর্ট_মান,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({কী_মান:মান for কী_মান,মান in রিপোর্ট_মান.items() if কী_মান!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':চালনা()
