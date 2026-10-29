#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા 자체 커널의 IP/ICMP, સ્થિતિ_મૂલ્ય_e10195a1 ક્વેરી_મૂલ્ય, 현지어 આદેશ, 게스트 પ્રસ્થાન_એપ્લિકેશન માન્ય_કરો."""
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


def ચલાવો_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');દલીલો=해석기.parse_args()
    પ્રોજેક્ટ_રૂટ=Path(__file__).resolve().parents[1];સુયોજના={};નામ_કોષ્ટક={}
    if દલીલો.edition:
        나라=દલીલો.edition.resolve();સુયોજના=json.loads((나라/'native.json').read_text());નામ_કોષ્ટક=સુયોજના['identifiers'];પ્રોજેક્ટ_રૂટ=나라/સુયોજના['source']/સુયોજના['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        હોસ્ટ=나라/'host/qemu'
        if હોસ્ટ.is_file():os.environ['QEMU_AARCH64']=str(હોસ્ટ)
    ઉપકરણો=પ્રોજેક્ટ_રૂટ/Path(સુયોજના.get('runner','ઉપકરણો/અમલ_કરો_આદેશ.py')).parent
    sys.path.insert(0,str(ઉપકરણો))
    def વાંચો(નામ):
        પથ=ઉપકરણો/(નામ_કોષ્ટક.get(નામ,નામ)+'.py');કામ_મૂલ્ય=importlib.util.spec_from_file_location('test_'+નામ,str(પથ));મૉડ્યૂલ_મૂલ્ય=importlib.util.module_from_spec(કામ_મૂલ્ય);કામ_મૂલ્ય.loader.exec_module(મૉડ્યૂલ_મૂલ્ય);return મૉડ્યૂલ_મૂલ્ય
    실행모듈=વાંચો('અમલ_કરો_આદેશ');નેટવર્ક_મૉડ્યૂલ=વાંચો('નેટવર્ક_બ્રિજ');આદેશ=getattr(실행모듈,નામ_કોષ્ટક.get('આદેશ','આદેશ'));બ્રિજ_લખો=getattr(નેટવર્ક_મૉડ્યૂલ,નામ_કોષ્ટક.get('નેટવર્ક_બ્રિજ','નેટવર્ક_બ્રિજ'))
    ઉર્ફ_મૂલ્ય=સુયોજના.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_સરનામું','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'શૉ_મદદ'})
    sys.path.insert(0,str(પ્રોજેક્ટ_રૂટ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(પ્રોજેક્ટ_રૂટ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    આઉટપુટ=દલીલો.output or પ્રોજેક્ટ_રૂટ/'build/verification/system-tools';આઉટપુટ.mkdir(parents=True,exist_ok=True)
    અહેવાલ_મૂલ્ય={'passed':False,'country':સુયોજના.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    લૉગ_પંક્તિ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        નિયંત્રણ_પાથ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as શોધ_મૂલ્ય:શોધ_મૂલ્ય.bind(('127.0.0.1',0));પોર્ટ_નંબર=શોધ_મૂલ્ય.getsockname()[1]
            if not 50000<=પોર્ટ_નંબર<=50007:break
        with બ્રિજ_લખો(પોર્ટ_નંબર,કૅપ્ચર_કરો=True,અતિથિ_સરનામું=ipTestText('10.0.2.20'),હોસ્ટ_સરનામું='127.0.0.2') as બ્રિજ_મૂલ્ય:
            પ્રક્રિયા_મૂલ્ય=subprocess.Popen(આદેશ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(નિયંત્રણ_પાથ)]+બ્રિજ_મૂલ્ય.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            પસંદ_કરો_આઇટમ=selectors.DefaultSelector();પસંદ_કરો_આઇટમ.register(પ્રક્રિયા_મૂલ્ય.stdout,selectors.EVENT_READ)
            def 받기(શૉ_મૂલ્ય,ચલાવો_2=0,제한=45):
                끝=time.monotonic()+제한
                while શૉ_મૂલ્ય not in લૉગ_પંક્તિ[ચલાવો_2:]:
                    if time.monotonic()>끝 or પ્રક્રિયા_મૂલ્ય.poll() is not None:raise AssertionError('Missing '+repr(શૉ_મૂલ્ય)+'\n'+લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8','replace'))
                    for કી_મૂલ્ય,_ in પસંદ_કરો_આઇટમ.select(.1):
                        ડેટા=કી_મૂલ્ય.fileobj.read(65536)
                        if ડેટા:લૉગ_પંક્તિ.extend(ડેટા)
                return લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8','replace').replace('\r\n','\n')
            def મોકલો(ડેટા):પ્રક્રિયા_મૂલ્ય.stdin.write(ડેટા);પ્રક્રિયા_મૂલ્ય.stdin.flush()
            def શેલ(લખાણ):
                લખાણ=ipTestText(લખાણ)
                print(અહેવાલ_મૂલ્ય['country'],લખાણ,flush=True);차례[0]+=1;શૉ_મૂલ્ય='__SYSTEM_DONE_'+str(차례[0])+'__';ચલાવો_2=len(લૉગ_પંક્તિ)
                મોકલો((લખાણ+'; echo; echo '+શૉ_મૂલ્ય+'\n').encode())
                끝표시=('\r\n'+શૉ_મૂલ્ય+'\r\n').encode();받기(끝표시,ચલાવો_2)
                અંત_કરો_સ્થિતિ=લૉગ_પંક્તિ.index(끝표시,ચલાવો_2)+len(끝표시)
                받기(b'jkoros-native> ',અંત_કરો_સ્થિતિ)
                return લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ચકાસવું(લખાણ,*값들):
                જવાબ=શેલ(લખાણ)
                for મૂલ્ય in 값들:assert ipTestText(મૂલ્ય) in જવાબ,(લખાણ,મૂલ્ય,જવાબ)
                return જવાબ
            try:
                받기(b'jkoros-native> ')
                if not દલીલો.poweroff_only:
                    મદદ_મૂલ્ય=ચકાસવું('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ઉર્ફ_મૂલ્ય.values():assert 별칭 in મદદ_મૂલ્ય,(별칭,મદદ_મૂલ્ય)
                    ચકાસવું(ઉર્ફ_મૂલ્ય['help']+' system','Network / system')
                    ચકાસવું('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ચકાસવું(ઉર્ફ_મૂલ્ય['ipconfig'],'inet 10.0.2.15');ચકાસવું('ip addr show','sl0: UP');ચકાસવું('ifconfig','sl0: UP')
                    for અમાન્ય_સેટિંગ્સ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ભૂલ=ચકાસવું('ipconfig set '+અમાન્ય_સેટિંગ્સ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ભૂલ,ભૂલ
                        ચકાસવું('ipconfig','inet 10.0.2.15')
                    ચકાસવું('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ચકાસવું(ઉર્ફ_મૂલ્ય['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ચકાસવું('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ચકાસવું('ip link set dev sl0 down','sl0: DOWN');ચકાસવું('ping -c 1 10.0.2.2; echo STATUS=$?','ભૂલ -100','STATUS=1')
                    ચકાસવું('ipconfig up','sl0: UP')
                    ચકાસવું(ઉર્ફ_મૂલ્ય['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ચકાસવું('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ચકાસવું('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ચકાસવું(ઉર્ફ_મૂલ્ય['route'],'10.0.2.2 sl0')
                    ચકાસવું('ftpd start','FTP listening')
                    ચકાસવું(ઉર્ફ_મૂલ્ય['netstat'],'10.0.2.20:21','LISTEN');ચકાસવું('ss','LISTEN')
                    ચકાસવું('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ભૂલ -16')
                    with ftplib.FTP() as ક્લાયંટ_મૂલ્ય:
                        ક્લાયંટ_મૂલ્ય.connect('127.0.0.2',પોર્ટ_નંબર,timeout=20);ક્લાયંટ_મૂલ્ય.login();ડેટા=b'Network address was changed in the guest.\n'
                        ક્લાયંટ_મૂલ્ય.storbinary('STOR net-state.txt',io.BytesIO(ડેટા));받은자료=bytearray();ક્લાયંટ_મૂલ્ય.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ડેટા;ક્લાયંટ_મૂલ્ય.delete('net-state.txt')
                    ચકાસવું('ftpd stop','FTP stopped');ચકાસવું('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    અહેવાલ_મૂલ્ય['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(લખાણ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',લખાણ);assert 찾음,લખાણ;return tuple(map(int,찾음.groups()))
                    전=저장값(ચકાસવું('df','RAM only'));ચકાસવું('echo disk-proof > sys-state.txt');후=저장값(ચકાસવું(ઉર્ફ_મૂલ્ય['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ચકાસવું('rm sys-state.txt');assert 저장값(શેલ('df'))==전
                    મેમરી_મૂલ્ય=ચકાસવું(ઉર્ફ_મૂલ્ય['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',મેમરી_મૂલ્ય).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ચકાસવું(ઉર્ફ_મૂલ્ય['ps'],'kernel/shell');ચકાસવું(ઉર્ફ_મૂલ્ય['uptime'],'seconds')
                    સ્થિતિ_માહિતી=ચકાસવું(ઉર્ફ_મૂલ્ય['top']+' -n 2','kernel/shell');assert સ્થિતિ_માહિતી.count('PID SLOT STATE')==2,સ્થિતિ_માહિતી
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ચકાસવું('terminal','TERMINAL READY');ચલાવો_2=len(લૉગ_પંક્તિ);મોકલો(b'vi process.txt\n');받기(b'NORMAL',ચલાવો_2)
                    ચલાવો_2=len(લૉગ_પંક્તિ);મોકલો(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ચલાવો_2)
                    પ્રવેશ_સૂચી=ચકાસવું('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',પ્રવેશ_સૂચી);assert 찾음 and int(찾음.group(2))>0,પ્રવેશ_સૂચી
                    ચકાસવું('free','EL0 mapped KiB: '+찾음.group(2))
                    ચલાવો_2=len(લૉગ_પંક્તિ);મોકલો(b'top\n');받기(b'PID SLOT STATE',ચલાવો_2);મોકલો(b'q');받기(b'jkoros-native> ',ચલાવો_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if ઉર્ફ_મૂલ્ય['df']!='df':
                        ચલાવો_2=len(લૉગ_પંક્તિ);મોકલો((ઉર્ફ_મૂલ્ય['df'][:-1]+'\t\n').encode());받기(b'RAM only',ચલાવો_2);받기(b'jkoros-native> ',ચલાવો_2)
                    અહેવાલ_મૂલ્ય['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as નિયંત્રણ_મૂલ્ય:
                    નિયંત્રણ_મૂલ્ય.settimeout(15);નિયંત્રણ_મૂલ્ય.connect(str(નિયંત્રણ_પાથ));સ્ટ્રીમ_મૂલ્ય=નિયંત્રણ_મૂલ્ય.makefile('rwb');json.loads(સ્ટ્રીમ_મૂલ્ય.readline());સ્ટ્રીમ_મૂલ્ય.write(b'{"execute":"qmp_capabilities"}\n');સ્ટ્રીમ_મૂલ્ય.flush()
                    while 'return' not in json.loads(સ્ટ્રીમ_મૂલ્ય.readline()):pass
                    મોકલો((('poweroff' if દલીલો.poweroff_only else ઉર્ફ_મૂલ્ય['poweroff'])+'\n').encode())
                    while True:
                        ઇવેંટ=json.loads(સ્ટ્રીમ_મૂલ્ય.readline())
                        if ઇવેંટ.get('event')=='SHUTDOWN':break
                    assert ઇવેંટ['data']['guest'] and ઇવેંટ['data']['reason']=='guest-shutdown',ઇવેંટ
                    assert પ્રક્રિયા_મૂલ્ય.wait(timeout=15)==0
                    અહેવાલ_મૂલ્ય['shutdown']=ઇવેંટ;અહેવાલ_મૂલ્ય['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                અહેવાલ_મૂલ્ય['network_trace']=બ્રિજ_મૂલ્ય.ટ્રૅસ_લૉગ
                assert દલીલો.poweroff_only or any(પ્રવેશ_મૂલ્ય['protocol']==1 and પ્રવેશ_મૂલ્ય['direction']=='from_guest' for પ્રવેશ_મૂલ્ય in બ્રિજ_મૂલ્ય.ટ્રૅસ_લૉગ)
                અહેવાલ_મૂલ્ય['passed']=True
            finally:
                if પ્રક્રિયા_મૂલ્ય.poll() is None:os.killpg(પ્રક્રિયા_મૂલ્ય.pid,signal.SIGTERM)
                try:પ્રક્રિયા_મૂલ્ય.wait(timeout=10)
                except subprocess.TimeoutExpired:પ્રક્રિયા_મૂલ્ય.kill();પ્રક્રિયા_મૂલ્ય.wait()
                પસંદ_કરો_આઇટમ.close();(આઉટપુટ/'serial.log').write_bytes(લૉગ_પંક્તિ);(આઉટપુટ/'report.json').write_text(json.dumps(અહેવાલ_મૂલ્ય,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({કી_મૂલ્ય:મૂલ્ય for કી_મૂલ્ય,મૂલ્ય in અહેવાલ_મૂલ્ય.items() if કી_મૂલ્ય!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ચલાવો_2()
