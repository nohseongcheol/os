#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ 자체 커널의 IP/ICMP, ደረጃ_ዋጋ ሕቶ_ዋጋ, 현지어 ትእዛዝ, 게스트 ውጻእ_መተግበሪ አረጋግፅ."""
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


def ኣኺድ():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];ኣቀማምጣታት={};ሽም_ሰሌዳ={}
    if 인수.edition:
        나라=인수.edition.resolve();ኣቀማምጣታት=json.loads((나라/'native.json').read_text());ሽም_ሰሌዳ=ኣቀማምጣታት['identifiers'];기준=나라/ኣቀማምጣታት['source']/ኣቀማምጣታት['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        አዐንግድ=나라/'host/qemu'
        if አዐንግድ.is_file():os.environ['QEMU_AARCH64']=str(አዐንግድ)
    መሳርሒታት=기준/Path(ኣቀማምጣታት.get('runner','መሳርሒታት/ተግብር_ትእዛዝ.py')).parent
    sys.path.insert(0,str(መሳርሒታት))
    def 읽기(ሽም):
        መገዲ=መሳርሒታት/(ሽም_ሰሌዳ.get(ሽም,ሽም)+'.py');ዕዮ_ዋጋ_102996da=importlib.util.spec_from_file_location('test_'+ሽም,str(መገዲ));모듈=importlib.util.module_from_spec(ዕዮ_ዋጋ_102996da);ዕዮ_ዋጋ_102996da.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('ተግብር_ትእዛዝ');망모듈=읽기('통신다리');ትእዛዝ=getattr(실행모듈,ሽም_ሰሌዳ.get('ትእዛዝ','ትእዛዝ'));다리형=getattr(망모듈,ሽም_ሰሌዳ.get('통신다리','통신다리'))
    ሳጓ_ዋጋ=ኣቀማምጣታት.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ኣድራሻ','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ኣርእይ_ሓገዝ'})
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
    ጸብጻብ_ዋጋ={'passed':False,'country':ኣቀማምጣታት.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ምዝጉብ_ሪጋ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ቁጽጽር_መገዲ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as አለሻ_ዋጋ:አለሻ_ዋጋ.bind(('127.0.0.1',0));접속번호=አለሻ_ዋጋ.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,ቕረጽ=True,게스트주소=ipTestText('10.0.2.20'),አዐንግድ_ኣድራሻ='127.0.0.2') as 다리:
            መስርሕ_ዋጋ=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ቁጽጽር_መገዲ)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ምረጽ_ውልቀ_ነገር=selectors.DefaultSelector();ምረጽ_ውልቀ_ነገር.register(መስርሕ_ዋጋ.stdout,selectors.EVENT_READ)
            def 받기(ኣርእይ_ዋጋ,ኣኺድ=0,제한=45):
                끝=time.monotonic()+제한
                while ኣርእይ_ዋጋ not in ምዝጉብ_ሪጋ[ኣኺድ:]:
                    if time.monotonic()>끝 or መስርሕ_ዋጋ.poll() is not None:raise AssertionError('Missing '+repr(ኣርእይ_ዋጋ)+'\n'+ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8','replace'))
                    for መፍትሕ_ዋጋ,_ in ምረጽ_ውልቀ_ነገር.select(.1):
                        ሓበሬታ=መፍትሕ_ዋጋ.fileobj.read(65536)
                        if ሓበሬታ:ምዝጉብ_ሪጋ.extend(ሓበሬታ)
                return ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8','replace').replace('\r\n','\n')
            def ለኣኽ(ሓበሬታ):መስርሕ_ዋጋ.stdin.write(ሓበሬታ);መስርሕ_ዋጋ.stdin.flush()
            def ሽፋን(ጽሑፍ):
                ጽሑፍ=ipTestText(ጽሑፍ)
                print(ጸብጻብ_ዋጋ['country'],ጽሑፍ,flush=True);차례[0]+=1;ኣርእይ_ዋጋ='__SYSTEM_DONE_'+str(차례[0])+'__';ኣኺድ=len(ምዝጉብ_ሪጋ)
                ለኣኽ((ጽሑፍ+'; echo; echo '+ኣርእይ_ዋጋ+'\n').encode())
                끝표시=('\r\n'+ኣርእይ_ዋጋ+'\r\n').encode();받기(끝표시,ኣኺድ)
                끝자리=ምዝጉብ_ሪጋ.index(끝표시,ኣኺድ)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8','replace').replace('\r\n','\n')
            def ኣረጋግጽ(ጽሑፍ,*값들):
                መልስ=ሽፋን(ጽሑፍ)
                for ዋጋ in 값들:assert ipTestText(ዋጋ) in መልስ,(ጽሑፍ,ዋጋ,መልስ)
                return መልስ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ሓገዝ_ዋጋ_8d901cc2=ኣረጋግጽ('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ሳጓ_ዋጋ.values():assert 별칭 in ሓገዝ_ዋጋ_8d901cc2,(별칭,ሓገዝ_ዋጋ_8d901cc2)
                    ኣረጋግጽ(ሳጓ_ዋጋ['help']+' system','Network / system')
                    ኣረጋግጽ('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ኣረጋግጽ(ሳጓ_ዋጋ['ipconfig'],'inet 10.0.2.15');ኣረጋግጽ('ip addr show','sl0: UP');ኣረጋግጽ('ifconfig','sl0: UP')
                    for ዘይቅቡል_ኣቀማምጣታት in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ጌጋ=ኣረጋግጽ('ipconfig set '+ዘይቅቡል_ኣቀማምጣታት+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ጌጋ,ጌጋ
                        ኣረጋግጽ('ipconfig','inet 10.0.2.15')
                    ኣረጋግጽ('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ኣረጋግጽ(ሳጓ_ዋጋ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ኣረጋግጽ('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ኣረጋግጽ('ip link set dev sl0 down','sl0: DOWN');ኣረጋግጽ('ping -c 1 10.0.2.2; echo STATUS=$?','ጌጋ -100','STATUS=1')
                    ኣረጋግጽ('ipconfig up','sl0: UP')
                    ኣረጋግጽ(ሳጓ_ዋጋ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ኣረጋግጽ('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ኣረጋግጽ('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ኣረጋግጽ(ሳጓ_ዋጋ['route'],'10.0.2.2 sl0')
                    ኣረጋግጽ('ftpd start','FTP listening')
                    ኣረጋግጽ(ሳጓ_ዋጋ['netstat'],'10.0.2.20:21','LISTEN');ኣረጋግጽ('ss','LISTEN')
                    ኣረጋግጽ('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ጌጋ -16')
                    with ftplib.FTP() as ዓሚል_ዋጋ:
                        ዓሚል_ዋጋ.connect('127.0.0.2',접속번호,timeout=20);ዓሚል_ዋጋ.login();ሓበሬታ=b'Network address was changed in the guest.\n'
                        ዓሚል_ዋጋ.storbinary('STOR net-state.txt',io.BytesIO(ሓበሬታ));받은자료=bytearray();ዓሚል_ዋጋ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ሓበሬታ;ዓሚል_ዋጋ.delete('net-state.txt')
                    ኣረጋግጽ('ftpd stop','FTP stopped');ኣረጋግጽ('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ጸብጻብ_ዋጋ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ጽሑፍ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ጽሑፍ);assert 찾음,ጽሑፍ;return tuple(map(int,찾음.groups()))
                    전=저장값(ኣረጋግጽ('df','RAM only'));ኣረጋግጽ('echo disk-proof > sys-state.txt');후=저장값(ኣረጋግጽ(ሳጓ_ዋጋ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ኣረጋግጽ('rm sys-state.txt');assert 저장값(ሽፋን('df'))==전
                    ማህደር_ዝኽረት_ዋጋ=ኣረጋግጽ(ሳጓ_ዋጋ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ማህደር_ዝኽረት_ዋጋ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ኣረጋግጽ(ሳጓ_ዋጋ['ps'],'kernel/shell');ኣረጋግጽ(ሳጓ_ዋጋ['uptime'],'seconds')
                    ደረጃ_ሓበሬታ=ኣረጋግጽ(ሳጓ_ዋጋ['top']+' -n 2','kernel/shell');assert ደረጃ_ሓበሬታ.count('PID SLOT STATE')==2,ደረጃ_ሓበሬታ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ኣረጋግጽ('terminal','TERMINAL READY');ኣኺድ=len(ምዝጉብ_ሪጋ);ለኣኽ(b'vi process.txt\n');받기(b'NORMAL',ኣኺድ)
                    ኣኺድ=len(ምዝጉብ_ሪጋ);ለኣኽ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ኣኺድ)
                    ምእታው_ዝርዝር=ኣረጋግጽ('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ምእታው_ዝርዝር);assert 찾음 and int(찾음.group(2))>0,ምእታው_ዝርዝር
                    ኣረጋግጽ('free','EL0 mapped KiB: '+찾음.group(2))
                    ኣኺድ=len(ምዝጉብ_ሪጋ);ለኣኽ(b'top\n');받기(b'PID SLOT STATE',ኣኺድ);ለኣኽ(b'q');받기(b'jkoros-native> ',ኣኺድ)
                    # Test a multibyte prefix through the real shell completion path.
                    if ሳጓ_ዋጋ['df']!='df':
                        ኣኺድ=len(ምዝጉብ_ሪጋ);ለኣኽ((ሳጓ_ዋጋ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ኣኺድ);받기(b'jkoros-native> ',ኣኺድ)
                    ጸብጻብ_ዋጋ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ቁጽጽር_ዋጋ:
                    ቁጽጽር_ዋጋ.settimeout(15);ቁጽጽር_ዋጋ.connect(str(ቁጽጽር_መገዲ));ወሓዚ_ዋጋ=ቁጽጽር_ዋጋ.makefile('rwb');json.loads(ወሓዚ_ዋጋ.readline());ወሓዚ_ዋጋ.write(b'{"execute":"qmp_capabilities"}\n');ወሓዚ_ዋጋ.flush()
                    while 'return' not in json.loads(ወሓዚ_ዋጋ.readline()):pass
                    ለኣኽ((('poweroff' if 인수.poweroff_only else ሳጓ_ዋጋ['poweroff'])+'\n').encode())
                    while True:
                        ፍጻመ=json.loads(ወሓዚ_ዋጋ.readline())
                        if ፍጻመ.get('event')=='SHUTDOWN':break
                    assert ፍጻመ['data']['guest'] and ፍጻመ['data']['reason']=='guest-shutdown',ፍጻመ
                    assert መስርሕ_ዋጋ.wait(timeout=15)==0
                    ጸብጻብ_ዋጋ['shutdown']=ፍጻመ;ጸብጻብ_ዋጋ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ጸብጻብ_ዋጋ['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(ምእታው_ዋጋ['protocol']==1 and ምእታው_ዋጋ['direction']=='from_guest' for ምእታው_ዋጋ in 다리.추적기록)
                ጸብጻብ_ዋጋ['passed']=True
            finally:
                if መስርሕ_ዋጋ.poll() is None:os.killpg(መስርሕ_ዋጋ.pid,signal.SIGTERM)
                try:መስርሕ_ዋጋ.wait(timeout=10)
                except subprocess.TimeoutExpired:መስርሕ_ዋጋ.kill();መስርሕ_ዋጋ.wait()
                ምረጽ_ውልቀ_ነገር.close();(출력/'serial.log').write_bytes(ምዝጉብ_ሪጋ);(출력/'report.json').write_text(json.dumps(ጸብጻብ_ዋጋ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({መፍትሕ_ዋጋ:ዋጋ for መፍትሕ_ዋጋ,ዋጋ in ጸብጻብ_ዋጋ.items() if መፍትሕ_ዋጋ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ኣኺድ()
