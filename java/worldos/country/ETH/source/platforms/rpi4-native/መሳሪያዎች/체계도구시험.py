#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ 자체 커널의 IP/ICMP, ዞን_እሴት መጠይቅ_እሴት, 현지어 ትእዛዝ, 게스트 ውጣ_ፕሮግራም ትክክለኛነት_አረጋግጥ."""
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


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b=argparse.ArgumentParser();አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--edition',type=Path);አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--output',type=Path);አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    አሳይ_ስር=Path(__file__).resolve().parents[1];ማሰናጃዎች={};ስም_ሰንጠረዥ={}
    if 인수.edition:
        나라=인수.edition.resolve();ማሰናጃዎች=json.loads((나라/'native.json').read_text());ስም_ሰንጠረዥ=ማሰናጃዎች['identifiers'];አሳይ_ስር=나라/ማሰናጃዎች['source']/ማሰናጃዎች['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        አዘጋጅ_b78e430d=나라/'host/qemu'
        if አዘጋጅ_b78e430d.is_file():os.environ['QEMU_AARCH64']=str(አዘጋጅ_b78e430d)
    መሳሪያዎች=አሳይ_ስር/Path(ማሰናጃዎች.get('runner','መሳሪያዎች/ፈጽም_ትእዛዝ.py')).parent
    sys.path.insert(0,str(መሳሪያዎች))
    def ማንበቢያ(ስም):
        መተላለፊያ=መሳሪያዎች/(ስም_ሰንጠረዥ.get(ስም,ስም)+'.py');ስራ_እሴት_102996da=importlib.util.spec_from_file_location('test_'+ስም,str(መተላለፊያ));ሞጁል_እሴት=importlib.util.module_from_spec(ስራ_እሴት_102996da);ስራ_እሴት_102996da.loader.exec_module(ሞጁል_እሴት);return ሞጁል_እሴት
    실행모듈=ማንበቢያ('ፈጽም_ትእዛዝ');መረብ_ሞጁል=ማንበቢያ('መረብ_ድልድይ');ትእዛዝ=getattr(실행모듈,ስም_ሰንጠረዥ.get('ትእዛዝ','ትእዛዝ'));ድልድይ_ተይብ=getattr(መረብ_ሞጁል,ስም_ሰንጠረዥ.get('መረብ_ድልድይ','መረብ_ድልድይ'))
    አቋራጭ_እሴት_0a38607b=ማሰናጃዎች.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_አድራሻ','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'አሳይ_እገዛ'})
    sys.path.insert(0,str(አሳይ_ስር/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(አሳይ_ስር);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ውጤት=인수.output or አሳይ_ስር/'build/verification/system-tools';ውጤት.mkdir(parents=True,exist_ok=True)
    ዘገባ_እሴት={'passed':False,'country':ማሰናጃዎች.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    መዝግብ_ረድፍ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ቁጥጥር_ዱካ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ፈልግ_እሴት:ፈልግ_እሴት.bind(('127.0.0.1',0));የወደብ_ቁጥር=ፈልግ_እሴት.getsockname()[1]
            if not 50000<=የወደብ_ቁጥር<=50007:break
        with ድልድይ_ተይብ(የወደብ_ቁጥር,መያዝ=True,እንግዳ_አድራሻ=ipTestText('10.0.2.20'),አዘጋጅ_አድራሻ='127.0.0.2') as ድልድይ_እሴት:
            ሂደት_እሴት=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ቁጥጥር_ዱካ)]+ድልድይ_እሴት.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ምረጥ_ንጥል_ነገር=selectors.DefaultSelector();ምረጥ_ንጥል_ነገር.register(ሂደት_እሴት.stdout,selectors.EVENT_READ)
            def 받기(አሳይ_እሴት,ማስኬጃ=0,제한=45):
                끝=time.monotonic()+제한
                while አሳይ_እሴት not in መዝግብ_ረድፍ[ማስኬጃ:]:
                    if time.monotonic()>끝 or ሂደት_እሴት.poll() is not None:raise AssertionError('Missing '+repr(አሳይ_እሴት)+'\n'+መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8','replace'))
                    for ቁልፍ_እሴት,_ in ምረጥ_ንጥል_ነገር.select(.1):
                        ውሂብ=ቁልፍ_እሴት.fileobj.read(65536)
                        if ውሂብ:መዝግብ_ረድፍ.extend(ውሂብ)
                return መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8','replace').replace('\r\n','\n')
            def ላክ(ውሂብ):ሂደት_እሴት.stdin.write(ውሂብ);ሂደት_እሴት.stdin.flush()
            def ሼል(ጽሁፍ):
                ጽሁፍ=ipTestText(ጽሁፍ)
                print(ዘገባ_እሴት['country'],ጽሁፍ,flush=True);차례[0]+=1;አሳይ_እሴት='__SYSTEM_DONE_'+str(차례[0])+'__';ማስኬጃ=len(መዝግብ_ረድፍ)
                ላክ((ጽሁፍ+'; echo; echo '+አሳይ_እሴት+'\n').encode())
                끝표시=('\r\n'+አሳይ_እሴት+'\r\n').encode();받기(끝표시,ማስኬጃ)
                ጨርስ_በቦታ_አስቀመጠ=መዝግብ_ረድፍ.index(끝표시,ማስኬጃ)+len(끝표시)
                받기(b'jkoros-native> ',ጨርስ_በቦታ_አስቀመጠ)
                return መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8','replace').replace('\r\n','\n')
            def አረጋግጥ(ጽሁፍ,*값들):
                መልስ=ሼል(ጽሁፍ)
                for እሴት in 값들:assert ipTestText(እሴት) in መልስ,(ጽሁፍ,እሴት,መልስ)
                return መልስ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    እገዛ_እሴት=አረጋግጥ('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in አቋራጭ_እሴት_0a38607b.values():assert 별칭 in እገዛ_እሴት,(별칭,እገዛ_እሴት)
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['help']+' system','Network / system')
                    አረጋግጥ('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['ipconfig'],'inet 10.0.2.15');አረጋግጥ('ip addr show','sl0: UP');አረጋግጥ('ifconfig','sl0: UP')
                    for ልክ_ያልኾነ_ቅንብሮች in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ስህተት=አረጋግጥ('ipconfig set '+ልክ_ያልኾነ_ቅንብሮች+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ስህተት,ስህተት
                        አረጋግጥ('ipconfig','inet 10.0.2.15')
                    አረጋግጥ('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    አረጋግጥ('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    አረጋግጥ('ip link set dev sl0 down','sl0: DOWN');አረጋግጥ('ping -c 1 10.0.2.2; echo STATUS=$?','ስህተት -100','STATUS=1')
                    አረጋግጥ('ipconfig up','sl0: UP')
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    አረጋግጥ('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    አረጋግጥ('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');አረጋግጥ(አቋራጭ_እሴት_0a38607b['route'],'10.0.2.2 sl0')
                    አረጋግጥ('ftpd start','FTP listening')
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['netstat'],'10.0.2.20:21','LISTEN');አረጋግጥ('ss','LISTEN')
                    አረጋግጥ('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ስህተት -16')
                    with ftplib.FTP() as ተገልጋይ_እሴት:
                        ተገልጋይ_እሴት.connect('127.0.0.2',የወደብ_ቁጥር,timeout=20);ተገልጋይ_እሴት.login();ውሂብ=b'Network address was changed in the guest.\n'
                        ተገልጋይ_እሴት.storbinary('STOR net-state.txt',io.BytesIO(ውሂብ));받은자료=bytearray();ተገልጋይ_እሴት.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ውሂብ;ተገልጋይ_እሴት.delete('net-state.txt')
                    አረጋግጥ('ftpd stop','FTP stopped');አረጋግጥ('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ዘገባ_እሴት['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ጽሁፍ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ጽሁፍ);assert 찾음,ጽሁፍ;return tuple(map(int,찾음.groups()))
                    전=저장값(አረጋግጥ('df','RAM only'));አረጋግጥ('echo disk-proof > sys-state.txt');후=저장값(አረጋግጥ(አቋራጭ_እሴት_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    አረጋግጥ('rm sys-state.txt');assert 저장값(ሼል('df'))==전
                    ማስቀመጫ_እሴት=አረጋግጥ(አቋራጭ_እሴት_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ማስቀመጫ_እሴት).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    አረጋግጥ(አቋራጭ_እሴት_0a38607b['ps'],'kernel/shell');አረጋግጥ(አቋራጭ_እሴት_0a38607b['uptime'],'seconds')
                    ዞን_መረጃ=አረጋግጥ(አቋራጭ_እሴት_0a38607b['top']+' -n 2','kernel/shell');assert ዞን_መረጃ.count('PID SLOT STATE')==2,ዞን_መረጃ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    አረጋግጥ('terminal','TERMINAL READY');ማስኬጃ=len(መዝግብ_ረድፍ);ላክ(b'vi process.txt\n');받기(b'NORMAL',ማስኬጃ)
                    ማስኬጃ=len(መዝግብ_ረድፍ);ላክ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ማስኬጃ)
                    ምዝግብ_ዝርዝር=አረጋግጥ('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ምዝግብ_ዝርዝር);assert 찾음 and int(찾음.group(2))>0,ምዝግብ_ዝርዝር
                    አረጋግጥ('free','EL0 mapped KiB: '+찾음.group(2))
                    ማስኬጃ=len(መዝግብ_ረድፍ);ላክ(b'top\n');받기(b'PID SLOT STATE',ማስኬጃ);ላክ(b'q');받기(b'jkoros-native> ',ማስኬጃ)
                    # Test a multibyte prefix through the real shell completion path.
                    if አቋራጭ_እሴት_0a38607b['df']!='df':
                        ማስኬጃ=len(መዝግብ_ረድፍ);ላክ((አቋራጭ_እሴት_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',ማስኬጃ);받기(b'jkoros-native> ',ማስኬጃ)
                    ዘገባ_እሴት['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ቁጥጥር_እሴት:
                    ቁጥጥር_እሴት.settimeout(15);ቁጥጥር_እሴት.connect(str(ቁጥጥር_ዱካ));ልቀቅ_እሴት=ቁጥጥር_እሴት.makefile('rwb');json.loads(ልቀቅ_እሴት.readline());ልቀቅ_እሴት.write(b'{"execute":"qmp_capabilities"}\n');ልቀቅ_እሴት.flush()
                    while 'return' not in json.loads(ልቀቅ_እሴት.readline()):pass
                    ላክ((('poweroff' if 인수.poweroff_only else አቋራጭ_እሴት_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        ፍጻሜ=json.loads(ልቀቅ_እሴት.readline())
                        if ፍጻሜ.get('event')=='SHUTDOWN':break
                    assert ፍጻሜ['data']['guest'] and ፍጻሜ['data']['reason']=='guest-shutdown',ፍጻሜ
                    assert ሂደት_እሴት.wait(timeout=15)==0
                    ዘገባ_እሴት['shutdown']=ፍጻሜ;ዘገባ_እሴት['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ዘገባ_እሴት['network_trace']=ድልድይ_እሴት.ዱካ_መዝግብ
                assert 인수.poweroff_only or any(ምዝግብ_እሴት['protocol']==1 and ምዝግብ_እሴት['direction']=='from_guest' for ምዝግብ_እሴት in ድልድይ_እሴት.ዱካ_መዝግብ)
                ዘገባ_እሴት['passed']=True
            finally:
                if ሂደት_እሴት.poll() is None:os.killpg(ሂደት_እሴት.pid,signal.SIGTERM)
                try:ሂደት_እሴት.wait(timeout=10)
                except subprocess.TimeoutExpired:ሂደት_እሴት.kill();ሂደት_እሴት.wait()
                ምረጥ_ንጥል_ነገር.close();(ውጤት/'serial.log').write_bytes(መዝግብ_ረድፍ);(ውጤት/'report.json').write_text(json.dumps(ዘገባ_እሴት,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ቁልፍ_እሴት:እሴት for ቁልፍ_እሴት,እሴት in ዘገባ_እሴት.items() if ቁልፍ_እሴት!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ማስኬጃ()
