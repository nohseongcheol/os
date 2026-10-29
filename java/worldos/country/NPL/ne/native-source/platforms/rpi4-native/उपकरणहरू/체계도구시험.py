#!/usr/bin/env python3
"""वास्तविक_लगत निज 커널의 IP/ICMP, स्थिति_मान क्वेरी_मान, 현지어 आदेश, 게스트 बाहिर_जानुहोस्_अनुप्रयोग वैध_गर्नुहोस्."""
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


def चलाउनुहोस्():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');तर्क=해석기.parse_args()
    परियोजना_रूट=Path(__file__).resolve().parents[1];सेटिङ={};नाम_तालिका={}
    if तर्क.edition:
        나라=तर्क.edition.resolve();सेटिङ=json.loads((나라/'native.json').read_text());नाम_तालिका=सेटिङ['identifiers'];परियोजना_रूट=나라/सेटिङ['source']/सेटिङ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        होस्ट=나라/'host/qemu'
        if होस्ट.is_file():os.environ['QEMU_AARCH64']=str(होस्ट)
    उपकरणहरू=परियोजना_रूट/Path(सेटिङ.get('runner','उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py')).parent
    sys.path.insert(0,str(उपकरणहरू))
    def पढनुहोस्(नाम):
        मार्ग=उपकरणहरू/(नाम_तालिका.get(नाम,नाम)+'.py');केस_मान=importlib.util.spec_from_file_location('test_'+नाम,str(मार्ग));मोड्युल_मान=importlib.util.module_from_spec(केस_मान);केस_मान.loader.exec_module(मोड्युल_मान);return मोड्युल_मान
    실행모듈=पढनुहोस्('कार्यान्वयन_गर्नुहोस्_आदेश');सञ्जाल_मोड्युल=पढनुहोस्('सञ्जाल_ब्रिज');आदेश=getattr(실행모듈,नाम_तालिका.get('आदेश','आदेश'));ब्रिज_प्रकार=getattr(सञ्जाल_मोड्युल,नाम_तालिका.get('सञ्जाल_ब्रिज','सञ्जाल_ब्रिज'))
    उपनाम_मान=सेटिङ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'आइपी_ठेगाना','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'शो_मद्दत'})
    sys.path.insert(0,str(परियोजना_रूट/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(परियोजना_रूट);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=तर्क.output or परियोजना_रूट/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    रिपोर्ट_मान={'passed':False,'country':सेटिङ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    लग_रेकर्ड=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        नियन्त्रण_बाटो=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as खोज_मान:खोज_मान.bind(('127.0.0.1',0));접속번호=खोज_मान.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ब्रिज_प्रकार(접속번호,क्यापचर=True,अतिथि_ठेगाना=ipTestText('10.0.2.20'),होस्ट_ठेगाना='127.0.0.2') as ब्रिज_मान:
            प्रक्रिया_मान=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(नियन्त्रण_बाटो)]+ब्रिज_मान.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            छान्नुहोस्_वस्तु=selectors.DefaultSelector();छान्नुहोस्_वस्तु.register(प्रक्रिया_मान.stdout,selectors.EVENT_READ)
            def 받기(शो_मान,चलाउनुहोस्=0,제한=45):
                끝=time.monotonic()+제한
                while शो_मान not in लग_रेकर्ड[चलाउनुहोस्:]:
                    if time.monotonic()>끝 or प्रक्रिया_मान.poll() is not None:raise AssertionError('Missing '+repr(शो_मान)+'\n'+लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8','replace'))
                    for कुञ्जी_मान,_ in छान्नुहोस्_वस्तु.select(.1):
                        लगत=कुञ्जी_मान.fileobj.read(65536)
                        if लगत:लग_रेकर्ड.extend(लगत)
                return लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8','replace').replace('\r\n','\n')
            def पठाउनुहोस्(लगत):प्रक्रिया_मान.stdin.write(लगत);प्रक्रिया_मान.stdin.flush()
            def शेल(पाठ):
                पाठ=ipTestText(पाठ)
                print(रिपोर्ट_मान['country'],पाठ,flush=True);차례[0]+=1;शो_मान='__SYSTEM_DONE_'+str(차례[0])+'__';चलाउनुहोस्=len(लग_रेकर्ड)
                पठाउनुहोस्((पाठ+'; echo; echo '+शो_मान+'\n').encode())
                끝표시=('\r\n'+शो_मान+'\r\n').encode();받기(끝표시,चलाउनुहोस्)
                समाप्त_गर्नुहोस्_राख्नुहोस्=लग_रेकर्ड.index(끝표시,चलाउनुहोस्)+len(끝표시)
                받기(b'jkoros-native> ',समाप्त_गर्नुहोस्_राख्नुहोस्)
                return लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8','replace').replace('\r\n','\n')
            def रुजू_गर्नुहोस्(पाठ,*값들):
                जवाफ_दिनुहोस्=शेल(पाठ)
                for मान in 값들:assert ipTestText(मान) in जवाफ_दिनुहोस्,(पाठ,मान,जवाफ_दिनुहोस्)
                return जवाफ_दिनुहोस्
            try:
                받기(b'jkoros-native> ')
                if not तर्क.poweroff_only:
                    मद्दत_मान=रुजू_गर्नुहोस्('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in उपनाम_मान.values():assert 별칭 in मद्दत_मान,(별칭,मद्दत_मान)
                    रुजू_गर्नुहोस्(उपनाम_मान['help']+' system','Network / system')
                    रुजू_गर्नुहोस्('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    रुजू_गर्नुहोस्(उपनाम_मान['ipconfig'],'inet 10.0.2.15');रुजू_गर्नुहोस्('ip addr show','sl0: UP');रुजू_गर्नुहोस्('ifconfig','sl0: UP')
                    for अवैधानिक_सेटिङहरू in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        त्रुटि=रुजू_गर्नुहोस्('ipconfig set '+अवैधानिक_सेटिङहरू+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in त्रुटि,त्रुटि
                        रुजू_गर्नुहोस्('ipconfig','inet 10.0.2.15')
                    रुजू_गर्नुहोस्('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    रुजू_गर्नुहोस्(उपनाम_मान['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    रुजू_गर्नुहोस्('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    रुजू_गर्नुहोस्('ip link set dev sl0 down','sl0: DOWN');रुजू_गर्नुहोस्('ping -c 1 10.0.2.2; echo STATUS=$?','त्रुटि -100','STATUS=1')
                    रुजू_गर्नुहोस्('ipconfig up','sl0: UP')
                    रुजू_गर्नुहोस्(उपनाम_मान['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    रुजू_गर्नुहोस्('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    रुजू_गर्नुहोस्('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');रुजू_गर्नुहोस्(उपनाम_मान['route'],'10.0.2.2 sl0')
                    रुजू_गर्नुहोस्('ftpd start','FTP listening')
                    रुजू_गर्नुहोस्(उपनाम_मान['netstat'],'10.0.2.20:21','LISTEN');रुजू_गर्नुहोस्('ss','LISTEN')
                    रुजू_गर्नुहोस्('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','त्रुटि -16')
                    with ftplib.FTP() as ग्राहक_मान:
                        ग्राहक_मान.connect('127.0.0.2',접속번호,timeout=20);ग्राहक_मान.login();लगत=b'Network address was changed in the guest.\n'
                        ग्राहक_मान.storbinary('STOR net-state.txt',io.BytesIO(लगत));받은자료=bytearray();ग्राहक_मान.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==लगत;ग्राहक_मान.delete('net-state.txt')
                    रुजू_गर्नुहोस्('ftpd stop','FTP stopped');रुजू_गर्नुहोस्('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    रिपोर्ट_मान['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(पाठ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',पाठ);assert 찾음,पाठ;return tuple(map(int,찾음.groups()))
                    전=저장값(रुजू_गर्नुहोस्('df','RAM only'));रुजू_गर्नुहोस्('echo disk-proof > sys-state.txt');후=저장값(रुजू_गर्नुहोस्(उपनाम_मान['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    रुजू_गर्नुहोस्('rm sys-state.txt');assert 저장값(शेल('df'))==전
                    मेमोरी_मान=रुजू_गर्नुहोस्(उपनाम_मान['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',मेमोरी_मान).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    रुजू_गर्नुहोस्(उपनाम_मान['ps'],'kernel/shell');रुजू_गर्नुहोस्(उपनाम_मान['uptime'],'seconds')
                    स्थिति_जानकारी=रुजू_गर्नुहोस्(उपनाम_मान['top']+' -n 2','kernel/shell');assert स्थिति_जानकारी.count('PID SLOT STATE')==2,स्थिति_जानकारी
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    रुजू_गर्नुहोस्('terminal','TERMINAL READY');चलाउनुहोस्=len(लग_रेकर्ड);पठाउनुहोस्(b'vi process.txt\n');받기(b'NORMAL',चलाउनुहोस्)
                    चलाउनुहोस्=len(लग_रेकर्ड);पठाउनुहोस्(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',चलाउनुहोस्)
                    प्रविष्टि_सूची=रुजू_गर्नुहोस्('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',प्रविष्टि_सूची);assert 찾음 and int(찾음.group(2))>0,प्रविष्टि_सूची
                    रुजू_गर्नुहोस्('free','EL0 mapped KiB: '+찾음.group(2))
                    चलाउनुहोस्=len(लग_रेकर्ड);पठाउनुहोस्(b'top\n');받기(b'PID SLOT STATE',चलाउनुहोस्);पठाउनुहोस्(b'q');받기(b'jkoros-native> ',चलाउनुहोस्)
                    # Test a multibyte prefix through the real shell completion path.
                    if उपनाम_मान['df']!='df':
                        चलाउनुहोस्=len(लग_रेकर्ड);पठाउनुहोस्((उपनाम_मान['df'][:-1]+'\t\n').encode());받기(b'RAM only',चलाउनुहोस्);받기(b'jkoros-native> ',चलाउनुहोस्)
                    रिपोर्ट_मान['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as नियन्त्रण_मान:
                    नियन्त्रण_मान.settimeout(15);नियन्त्रण_मान.connect(str(नियन्त्रण_बाटो));प्रवाह_मान=नियन्त्रण_मान.makefile('rwb');json.loads(प्रवाह_मान.readline());प्रवाह_मान.write(b'{"execute":"qmp_capabilities"}\n');प्रवाह_मान.flush()
                    while 'return' not in json.loads(प्रवाह_मान.readline()):pass
                    पठाउनुहोस्((('poweroff' if तर्क.poweroff_only else उपनाम_मान['poweroff'])+'\n').encode())
                    while True:
                        घटना=json.loads(प्रवाह_मान.readline())
                        if घटना.get('event')=='SHUTDOWN':break
                    assert घटना['data']['guest'] and घटना['data']['reason']=='guest-shutdown',घटना
                    assert प्रक्रिया_मान.wait(timeout=15)==0
                    रिपोर्ट_मान['shutdown']=घटना;रिपोर्ट_मान['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                रिपोर्ट_मान['network_trace']=ब्रिज_मान.추적기록
                assert तर्क.poweroff_only or any(प्रविष्टि_मान['protocol']==1 and प्रविष्टि_मान['direction']=='from_guest' for प्रविष्टि_मान in ब्रिज_मान.추적기록)
                रिपोर्ट_मान['passed']=True
            finally:
                if प्रक्रिया_मान.poll() is None:os.killpg(प्रक्रिया_मान.pid,signal.SIGTERM)
                try:प्रक्रिया_मान.wait(timeout=10)
                except subprocess.TimeoutExpired:प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
                छान्नुहोस्_वस्तु.close();(출력/'serial.log').write_bytes(लग_रेकर्ड);(출력/'report.json').write_text(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({कुञ्जी_मान:मान for कुञ्जी_मान,मान in रिपोर्ट_मान.items() if कुञ्जी_मान!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':चलाउनुहोस्()
