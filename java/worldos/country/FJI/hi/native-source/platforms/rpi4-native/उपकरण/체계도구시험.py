#!/usr/bin/env python3
"""वास्तविक_डेटा निज 커널의 IP/ICMP, अवस्था_मान क्वेरी_मान, 현지어 आदेश, 게스트 निर्गमन_ऐप मान्य_करें."""
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


def चलाएँ():
    पार्सर_48ee4b1b=argparse.ArgumentParser();पार्सर_48ee4b1b.add_argument('--edition',type=Path);पार्सर_48ee4b1b.add_argument('--output',type=Path);पार्सर_48ee4b1b.add_argument('--poweroff-only',action='store_true');तर्क=पार्सर_48ee4b1b.parse_args()
    प्रोजेक्ट_करें_मूल=Path(__file__).resolve().parents[1];विन्यास={};नाम_तालिका={}
    if तर्क.edition:
        कंट्री_मान=तर्क.edition.resolve();विन्यास=json.loads((कंट्री_मान/'native.json').read_text());नाम_तालिका=विन्यास['identifiers'];प्रोजेक्ट_करें_मूल=कंट्री_मान/विन्यास['source']/विन्यास['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(कंट्री_मान/'native-edition.py'),'check'])
        आयोजक=कंट्री_मान/'host/qemu'
        if आयोजक.is_file():os.environ['QEMU_AARCH64']=str(आयोजक)
    उपकरण=प्रोजेक्ट_करें_मूल/Path(विन्यास.get('runner','उपकरण/निष्पादित_करें_आदेश.py')).parent
    sys.path.insert(0,str(उपकरण))
    def पढ़ें(नाम):
        पथ=उपकरण/(नाम_तालिका.get(नाम,नाम)+'.py');मामला_मान=importlib.util.spec_from_file_location('test_'+नाम,str(पथ));मॉड्यूल_मान=importlib.util.module_from_spec(मामला_मान);मामला_मान.loader.exec_module(मॉड्यूल_मान);return मॉड्यूल_मान
    실행모듈=पढ़ें('निष्पादित_करें_आदेश');नेटवर्क_मॉड्यूल=पढ़ें('ब्रिज_3de4fe3a');आदेश=getattr(실행모듈,नाम_तालिका.get('आदेश','आदेश'));ब्रिज_लिखें=getattr(नेटवर्क_मॉड्यूल,नाम_तालिका.get('ब्रिज_3de4fe3a','ब्रिज_3de4fe3a'))
    उपनाम_मान=विन्यास.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_पता','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'सहायता_दिखाना'})
    sys.path.insert(0,str(प्रोजेक्ट_करें_मूल/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(प्रोजेक्ट_करें_मूल);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    निर्गम=तर्क.output or प्रोजेक्ट_करें_मूल/'build/verification/system-tools';निर्गम.mkdir(parents=True,exist_ok=True)
    रिपोर्ट_मान={'passed':False,'country':विन्यास.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    लॉग_रिकॉर्ड=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        नियंत्रण_पथ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as खोज_मान:खोज_मान.bind(('127.0.0.1',0));पोर्ट_संख्या=खोज_मान.getsockname()[1]
            if not 50000<=पोर्ट_संख्या<=50007:break
        with ब्रिज_लिखें(पोर्ट_संख्या,कैप्चर_करें=True,अतिथि_पता=ipTestText('10.0.2.20'),आयोजक_पता='127.0.0.2') as ब्रिज_मान:
            प्रक्रिया_मान=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(नियंत्रण_पथ)]+ब्रिज_मान.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            चुनें_आइटम=selectors.DefaultSelector();चुनें_आइटम.register(प्रक्रिया_मान.stdout,selectors.EVENT_READ)
            def 받기(शो_मान,चलाएँ=0,제한=45):
                끝=time.monotonic()+제한
                while शो_मान not in लॉग_रिकॉर्ड[चलाएँ:]:
                    if time.monotonic()>끝 or प्रक्रिया_मान.poll() is not None:raise AssertionError('Missing '+repr(शो_मान)+'\n'+लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8','replace'))
                    for कुंजी_मान,_ in चुनें_आइटम.select(.1):
                        आँकड़े=कुंजी_मान.fileobj.read(65536)
                        if आँकड़े:लॉग_रिकॉर्ड.extend(आँकड़े)
                return लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8','replace').replace('\r\n','\n')
            def भेजें(आँकड़े):प्रक्रिया_मान.stdin.write(आँकड़े);प्रक्रिया_मान.stdin.flush()
            def शेल(पाठ):
                पाठ=ipTestText(पाठ)
                print(रिपोर्ट_मान['country'],पाठ,flush=True);차례[0]+=1;शो_मान='__SYSTEM_DONE_'+str(차례[0])+'__';चलाएँ=len(लॉग_रिकॉर्ड)
                भेजें((पाठ+'; echo; echo '+शो_मान+'\n').encode())
                समाप्त_करें_मार्कर=('\r\n'+शो_मान+'\r\n').encode();받기(समाप्त_करें_मार्कर,चलाएँ)
                समाप्त_करें_पद=लॉग_रिकॉर्ड.index(समाप्त_करें_मार्कर,चलाएँ)+len(समाप्त_करें_मार्कर)
                받기(b'jkoros-native> ',समाप्त_करें_पद)
                return लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8','replace').replace('\r\n','\n')
            def सत्यापित_करें(पाठ,*값들):
                उत्तर=शेल(पाठ)
                for मान in 값들:assert ipTestText(मान) in उत्तर,(पाठ,मान,उत्तर)
                return उत्तर
            try:
                받기(b'jkoros-native> ')
                if not तर्क.poweroff_only:
                    मदद_मान=सत्यापित_करें('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in उपनाम_मान.values():assert 별칭 in मदद_मान,(별칭,मदद_मान)
                    सत्यापित_करें(उपनाम_मान['help']+' system','Network / system')
                    सत्यापित_करें('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    सत्यापित_करें(उपनाम_मान['ipconfig'],'inet 10.0.2.15');सत्यापित_करें('ip addr show','sl0: UP');सत्यापित_करें('ifconfig','sl0: UP')
                    for अमान्य_सेटिंग in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        त्रुटि=सत्यापित_करें('ipconfig set '+अमान्य_सेटिंग+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in त्रुटि,त्रुटि
                        सत्यापित_करें('ipconfig','inet 10.0.2.15')
                    सत्यापित_करें('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    सत्यापित_करें(उपनाम_मान['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    सत्यापित_करें('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    सत्यापित_करें('ip link set dev sl0 down','sl0: DOWN');सत्यापित_करें('ping -c 1 10.0.2.2; echo STATUS=$?','त्रुटि -100','STATUS=1')
                    सत्यापित_करें('ipconfig up','sl0: UP')
                    सत्यापित_करें(उपनाम_मान['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    सत्यापित_करें('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    सत्यापित_करें('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');सत्यापित_करें(उपनाम_मान['route'],'10.0.2.2 sl0')
                    सत्यापित_करें('ftpd start','FTP listening')
                    सत्यापित_करें(उपनाम_मान['netstat'],'10.0.2.20:21','LISTEN');सत्यापित_करें('ss','LISTEN')
                    सत्यापित_करें('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','त्रुटि -16')
                    with ftplib.FTP() as क्लायंट_मान:
                        क्लायंट_मान.connect('127.0.0.2',पोर्ट_संख्या,timeout=20);क्लायंट_मान.login();आँकड़े=b'Network address was changed in the guest.\n'
                        क्लायंट_मान.storbinary('STOR net-state.txt',io.BytesIO(आँकड़े));받은자료=bytearray();क्लायंट_मान.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==आँकड़े;क्लायंट_मान.delete('net-state.txt')
                    सत्यापित_करें('ftpd stop','FTP stopped');सत्यापित_करें('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    रिपोर्ट_मान['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(पाठ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',पाठ);assert 찾음,पाठ;return tuple(map(int,찾음.groups()))
                    전=저장값(सत्यापित_करें('df','RAM only'));सत्यापित_करें('echo disk-proof > sys-state.txt');후=저장값(सत्यापित_करें(उपनाम_मान['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    सत्यापित_करें('rm sys-state.txt');assert 저장값(शेल('df'))==전
                    मेमोरी_मान=सत्यापित_करें(उपनाम_मान['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',मेमोरी_मान).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    सत्यापित_करें(उपनाम_मान['ps'],'kernel/shell');सत्यापित_करें(उपनाम_मान['uptime'],'seconds')
                    स्थिति_जानकारी=सत्यापित_करें(उपनाम_मान['top']+' -n 2','kernel/shell');assert स्थिति_जानकारी.count('PID SLOT STATE')==2,स्थिति_जानकारी
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    सत्यापित_करें('terminal','TERMINAL READY');चलाएँ=len(लॉग_रिकॉर्ड);भेजें(b'vi process.txt\n');받기(b'NORMAL',चलाएँ)
                    चलाएँ=len(लॉग_रिकॉर्ड);भेजें(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',चलाएँ)
                    एन्ट्री_सूची=सत्यापित_करें('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',एन्ट्री_सूची);assert 찾음 and int(찾음.group(2))>0,एन्ट्री_सूची
                    सत्यापित_करें('free','EL0 mapped KiB: '+찾음.group(2))
                    चलाएँ=len(लॉग_रिकॉर्ड);भेजें(b'top\n');받기(b'PID SLOT STATE',चलाएँ);भेजें(b'q');받기(b'jkoros-native> ',चलाएँ)
                    # Test a multibyte prefix through the real shell completion path.
                    if उपनाम_मान['df']!='df':
                        चलाएँ=len(लॉग_रिकॉर्ड);भेजें((उपनाम_मान['df'][:-1]+'\t\n').encode());받기(b'RAM only',चलाएँ);받기(b'jkoros-native> ',चलाएँ)
                    रिपोर्ट_मान['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as नियंत्रण_मान:
                    नियंत्रण_मान.settimeout(15);नियंत्रण_मान.connect(str(नियंत्रण_पथ));स्ट्रीम_मान=नियंत्रण_मान.makefile('rwb');json.loads(स्ट्रीम_मान.readline());स्ट्रीम_मान.write(b'{"execute":"qmp_capabilities"}\n');स्ट्रीम_मान.flush()
                    while 'return' not in json.loads(स्ट्रीम_मान.readline()):pass
                    भेजें((('poweroff' if तर्क.poweroff_only else उपनाम_मान['poweroff'])+'\n').encode())
                    while True:
                        घटना=json.loads(स्ट्रीम_मान.readline())
                        if घटना.get('event')=='SHUTDOWN':break
                    assert घटना['data']['guest'] and घटना['data']['reason']=='guest-shutdown',घटना
                    assert प्रक्रिया_मान.wait(timeout=15)==0
                    रिपोर्ट_मान['shutdown']=घटना;रिपोर्ट_मान['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                रिपोर्ट_मान['network_trace']=ब्रिज_मान.ट्रेस_लॉग
                assert तर्क.poweroff_only or any(एन्ट्री_मान['protocol']==1 and एन्ट्री_मान['direction']=='from_guest' for एन्ट्री_मान in ब्रिज_मान.ट्रेस_लॉग)
                रिपोर्ट_मान['passed']=True
            finally:
                if प्रक्रिया_मान.poll() is None:os.killpg(प्रक्रिया_मान.pid,signal.SIGTERM)
                try:प्रक्रिया_मान.wait(timeout=10)
                except subprocess.TimeoutExpired:प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
                चुनें_आइटम.close();(निर्गम/'serial.log').write_bytes(लॉग_रिकॉर्ड);(निर्गम/'report.json').write_text(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({कुंजी_मान:मान for कुंजी_मान,मान in रिपोर्ट_मान.items() if कुंजी_मान!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':चलाएँ()
