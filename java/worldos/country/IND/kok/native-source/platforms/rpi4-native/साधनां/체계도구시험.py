#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा 자체 커널의 IP/ICMP, स्थिती_मोल_e10195a1 क्वॅरी_मोल, 현지어 आदेश, 게스트 प्रस्थान_करचें_एप्लिकेशन पुनर्तपासणी_करची_5fb2b747."""
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


def चलोवप():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    प्रॉजॅक्ट_रूट=Path(__file__).resolve().parents[1];मांडावळी={};नांव_तकटो={}
    if 인수.edition:
        나라=인수.edition.resolve();मांडावळी=json.loads((나라/'native.json').read_text());नांव_तकटो=मांडावळी['identifiers'];प्रॉजॅक्ट_रूट=나라/मांडावळी['source']/मांडावळी['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        येजमान=나라/'host/qemu'
        if येजमान.is_file():os.environ['QEMU_AARCH64']=str(येजमान)
    साधनां=प्रॉजॅक्ट_रूट/Path(मांडावळी.get('runner','साधनां/पाळो_दिवचो_आदेश.py')).parent
    sys.path.insert(0,str(साधनां))
    def 읽기(नांव):
        पाथ=साधनां/(नांव_तकटो.get(नांव,नांव)+'.py');काम_मोल=importlib.util.spec_from_file_location('test_'+नांव,str(पाथ));मॉड्यूल_मोल=importlib.util.module_from_spec(काम_मोल);काम_मोल.loader.exec_module(मॉड्यूल_मोल);return मॉड्यूल_मोल
    실행모듈=읽기('पाळो_दिवचो_आदेश');नॅटवर्क_मॉड्यूल=읽기('नॅटवर्क_ब्रिज');आदेश=getattr(실행모듈,नांव_तकटो.get('आदेश','आदेश'));ब्रिज_TYPE=getattr(नॅटवर्क_मॉड्यूल,नांव_तकटो.get('नॅटवर्क_ब्रिज','नॅटवर्क_ब्रिज'))
    आडवाट_मोल_0a38607b=मांडावळी.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_नामो','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'शो_आदार'})
    sys.path.insert(0,str(प्रॉजॅक्ट_रूट/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(प्रॉजॅक्ट_रूट);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or प्रॉजॅक्ट_रूट/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    अहवाल_मोल={'passed':False,'country':मांडावळी.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_नोंद=bytearray();SEQUENCE_मोल=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        नियंत्रण_पाथ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as सोद_मोल:सोद_मोल.bind(('127.0.0.1',0));접속번호=सोद_मोल.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ब्रिज_TYPE(접속번호,कॅप्चर=True,सोयरो_नामो=ipTestText('10.0.2.20'),येजमान_नामो='127.0.0.2') as ब्रिज_मोल:
            प्रक्रिया_मोल=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(नियंत्रण_पाथ)]+ब्रिज_मोल.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_आयटम=selectors.DefaultSelector();CHOOSE_आयटम.register(प्रक्रिया_मोल.stdout,selectors.EVENT_READ)
            def 받기(शो_मोल,चलोवप=0,제한=45):
                끝=time.monotonic()+제한
                while शो_मोल not in LOG_नोंद[चलोवप:]:
                    if time.monotonic()>끝 or प्रक्रिया_मोल.poll() is not None:raise AssertionError('Missing '+repr(शो_मोल)+'\n'+LOG_नोंद[चलोवप:].decode('utf-8','replace'))
                    for की_मोल,_ in CHOOSE_आयटम.select(.1):
                        डेटा=की_मोल.fileobj.read(65536)
                        if डेटा:LOG_नोंद.extend(डेटा)
                return LOG_नोंद[चलोवप:].decode('utf-8','replace').replace('\r\n','\n')
            def धाडचें(डेटा):प्रक्रिया_मोल.stdin.write(डेटा);प्रक्रिया_मोल.stdin.flush()
            def शॅल(SMS):
                SMS=ipTestText(SMS)
                print(अहवाल_मोल['country'],SMS,flush=True);SEQUENCE_मोल[0]+=1;शो_मोल='__SYSTEM_DONE_'+str(SEQUENCE_मोल[0])+'__';चलोवप=len(LOG_नोंद)
                धाडचें((SMS+'; echo; echo '+शो_मोल+'\n').encode())
                끝표시=('\r\n'+शो_मोल+'\r\n').encode();받기(끝표시,चलोवप)
                सोपोवचें_स्थिती=LOG_नोंद.index(끝표시,चलोवप)+len(끝표시)
                받기(b'jkoros-native> ',सोपोवचें_स्थिती)
                return LOG_नोंद[चलोवप:].decode('utf-8','replace').replace('\r\n','\n')
            def पुनर्तपासणी_करची(SMS,*값들):
                जाप_दिवप=शॅल(SMS)
                for मोल in 값들:assert ipTestText(मोल) in जाप_दिवप,(SMS,मोल,जाप_दिवप)
                return जाप_दिवप
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    आदार_मोल=पुनर्तपासणी_करची('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in आडवाट_मोल_0a38607b.values():assert 별칭 in आदार_मोल,(별칭,आदार_मोल)
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['help']+' system','Network / system')
                    पुनर्तपासणी_करची('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['ipconfig'],'inet 10.0.2.15');पुनर्तपासणी_करची('ip addr show','sl0: UP');पुनर्तपासणी_करची('ifconfig','sl0: UP')
                    for अवैध_मांडावळी in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        चूक=पुनर्तपासणी_करची('ipconfig set '+अवैध_मांडावळी+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in चूक,चूक
                        पुनर्तपासणी_करची('ipconfig','inet 10.0.2.15')
                    पुनर्तपासणी_करची('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    पुनर्तपासणी_करची('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    पुनर्तपासणी_करची('ip link set dev sl0 down','sl0: DOWN');पुनर्तपासणी_करची('ping -c 1 10.0.2.2; echo STATUS=$?','चूक -100','STATUS=1')
                    पुनर्तपासणी_करची('ipconfig up','sl0: UP')
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    पुनर्तपासणी_करची('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    पुनर्तपासणी_करची('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['route'],'10.0.2.2 sl0')
                    पुनर्तपासणी_करची('ftpd start','FTP listening')
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['netstat'],'10.0.2.20:21','LISTEN');पुनर्तपासणी_करची('ss','LISTEN')
                    पुनर्तपासणी_करची('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','चूक -16')
                    with ftplib.FTP() as क्लायंट_मोल:
                        क्लायंट_मोल.connect('127.0.0.2',접속번호,timeout=20);क्लायंट_मोल.login();डेटा=b'Network address was changed in the guest.\n'
                        क्लायंट_मोल.storbinary('STOR net-state.txt',io.BytesIO(डेटा));RECEIVED_डेटा=bytearray();क्लायंट_मोल.retrbinary('RETR net-state.txt',RECEIVED_डेटा.extend);assert RECEIVED_डेटा==डेटा;क्लायंट_मोल.delete('net-state.txt')
                    पुनर्तपासणी_करची('ftpd stop','FTP stopped');पुनर्तपासणी_करची('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    अहवाल_मोल['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(पुनर्तपासणी_करची('df','RAM only'));पुनर्तपासणी_करची('echo disk-proof > sys-state.txt');후=저장값(पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    पुनर्तपासणी_करची('rm sys-state.txt');assert 저장값(शॅल('df'))==전
                    मेमरी_मोल=पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',मेमरी_मोल).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['ps'],'kernel/shell');पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['uptime'],'seconds')
                    स्थिती_म्हायती=पुनर्तपासणी_करची(आडवाट_मोल_0a38607b['top']+' -n 2','kernel/shell');assert स्थिती_म्हायती.count('PID SLOT STATE')==2,स्थिती_म्हायती
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    पुनर्तपासणी_करची('terminal','TERMINAL READY');चलोवप=len(LOG_नोंद);धाडचें(b'vi process.txt\n');받기(b'NORMAL',चलोवप)
                    चलोवप=len(LOG_नोंद);धाडचें(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',चलोवप)
                    प्रवेश_सुची=पुनर्तपासणी_करची('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',प्रवेश_सुची);assert 찾음 and int(찾음.group(2))>0,प्रवेश_सुची
                    पुनर्तपासणी_करची('free','EL0 mapped KiB: '+찾음.group(2))
                    चलोवप=len(LOG_नोंद);धाडचें(b'top\n');받기(b'PID SLOT STATE',चलोवप);धाडचें(b'q');받기(b'jkoros-native> ',चलोवप)
                    # Test a multibyte prefix through the real shell completion path.
                    if आडवाट_मोल_0a38607b['df']!='df':
                        चलोवप=len(LOG_नोंद);धाडचें((आडवाट_मोल_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',चलोवप);받기(b'jkoros-native> ',चलोवप)
                    अहवाल_मोल['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as नियंत्रण_मोल:
                    नियंत्रण_मोल.settimeout(15);नियंत्रण_मोल.connect(str(नियंत्रण_पाथ));Stream_मोल=नियंत्रण_मोल.makefile('rwb');json.loads(Stream_मोल.readline());Stream_मोल.write(b'{"execute":"qmp_capabilities"}\n');Stream_मोल.flush()
                    while 'return' not in json.loads(Stream_मोल.readline()):pass
                    धाडचें((('poweroff' if 인수.poweroff_only else आडवाट_मोल_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        प्रसंग=json.loads(Stream_मोल.readline())
                        if प्रसंग.get('event')=='SHUTDOWN':break
                    assert प्रसंग['data']['guest'] and प्रसंग['data']['reason']=='guest-shutdown',प्रसंग
                    assert प्रक्रिया_मोल.wait(timeout=15)==0
                    अहवाल_मोल['shutdown']=प्रसंग;अहवाल_मोल['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                अहवाल_मोल['network_trace']=ब्रिज_मोल.추적기록
                assert 인수.poweroff_only or any(प्रवेश_मोल['protocol']==1 and प्रवेश_मोल['direction']=='from_guest' for प्रवेश_मोल in ब्रिज_मोल.추적기록)
                अहवाल_मोल['passed']=True
            finally:
                if प्रक्रिया_मोल.poll() is None:os.killpg(प्रक्रिया_मोल.pid,signal.SIGTERM)
                try:प्रक्रिया_मोल.wait(timeout=10)
                except subprocess.TimeoutExpired:प्रक्रिया_मोल.kill();प्रक्रिया_मोल.wait()
                CHOOSE_आयटम.close();(출력/'serial.log').write_bytes(LOG_नोंद);(출력/'report.json').write_text(json.dumps(अहवाल_मोल,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({की_मोल:मोल for की_मोल,मोल in अहवाल_मोल.items() if की_मोल!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':चलोवप()
