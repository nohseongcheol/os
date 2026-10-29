#!/usr/bin/env python3
"""තථ්_ය_දත්ත 자체 커널의 IP/ICMP, තත්වය_අගය විමසුම_අගය, 현지어 විධානය, 게스트 පිටවීම_යෙදු වලංගු_කරන්න."""
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


def ක්_රියාත්මක_කරන්න_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');විස්තාරක=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];සැකසුම්={};නම_වගුව={}
    if විස්තාරක.edition:
        나라=විස්තාරක.edition.resolve();සැකසුම්=json.loads((나라/'native.json').read_text());නම_වගුව=සැකසුම්['identifiers'];기준=나라/සැකසුම්['source']/සැකසුම්['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ධාරකය=나라/'host/qemu'
        if ධාරකය.is_file():os.environ['QEMU_AARCH64']=str(ධාරකය)
    මෙවලම්=기준/Path(සැකසුම්.get('runner','මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py')).parent
    sys.path.insert(0,str(මෙවලම්))
    def කියවීම(නම):
        මාර්_ගය=මෙවලම්/(නම_වගුව.get(නම,නම)+'.py');කාරණය_අගය=importlib.util.spec_from_file_location('test_'+නම,str(මාර්_ගය));모듈=importlib.util.module_from_spec(කාරණය_අගය);කාරණය_අගය.loader.exec_module(모듈);return 모듈
    실행모듈=කියවීම('ක්_රියාත්මක_කරන්න_විධානය');망모듈=කියවීම('ජාලය_පාලම');විධානය=getattr(실행모듈,නම_වගුව.get('විධානය','විධානය'));පාලම_ටයිප්_කරන්න=getattr(망모듈,නම_වගුව.get('ජාලය_පාලම','ජාලය_පාලම'))
    කෙටිමඟ_අගය_0a38607b=සැකසුම්.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_යොමුව','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'දර්ශනය_උදව්ව'})
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
    출력=විස්තාරක.output or 기준/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    වාර්තාව_අගය={'passed':False,'country':සැකසුම්.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ලොගය_පේළිය=bytearray();අනුක්_රමය_අගය=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        පාලකය_පෙත=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as සෙවීම_අගය:සෙවීම_අගය.bind(('127.0.0.1',0));접속번호=සෙවීම_අගය.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with පාලම_ටයිප්_කරන්න(접속번호,ග්_රහණය=True,අමුත්තා_යොමුව=ipTestText('10.0.2.20'),ධාරකය_යොමුව='127.0.0.2') as පාලම_අගය:
            ක්_රියාවලිය_අගය=subprocess.Popen(විධානය()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(පාලකය_පෙත)]+පාලම_අගය.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            තෝරන්න_අයිතමය=selectors.DefaultSelector();තෝරන්න_අයිතමය.register(ක්_රියාවලිය_අගය.stdout,selectors.EVENT_READ)
            def 받기(දර්ශනය_අගය,ක්_රියාත්මක_කරන්න_2=0,제한=45):
                끝=time.monotonic()+제한
                while දර්ශනය_අගය not in ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:]:
                    if time.monotonic()>끝 or ක්_රියාවලිය_අගය.poll() is not None:raise AssertionError('Missing '+repr(දර්ශනය_අගය)+'\n'+ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8','replace'))
                    for යතුර_අගය,_ in තෝරන්න_අයිතමය.select(.1):
                        දත්ත=යතුර_අගය.fileobj.read(65536)
                        if දත්ත:ලොගය_පේළිය.extend(දත්ත)
                return ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ඊමේල්(දත්ත):ක්_රියාවලිය_අගය.stdin.write(දත්ත);ක්_රියාවලිය_අගය.stdin.flush()
            def කවචය(පෙළ):
                පෙළ=ipTestText(පෙළ)
                print(වාර්තාව_අගය['country'],පෙළ,flush=True);අනුක්_රමය_අගය[0]+=1;දර්ශනය_අගය='__SYSTEM_DONE_'+str(අනුක්_රමය_අගය[0])+'__';ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය)
                ඊමේල්((පෙළ+'; echo; echo '+දර්ශනය_අගය+'\n').encode())
                끝표시=('\r\n'+දර්ශනය_අගය+'\r\n').encode();받기(끝표시,ක්_රියාත්මක_කරන්න_2)
                끝자리=ලොගය_පේළිය.index(끝표시,ක්_රියාත්මක_කරන්න_2)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8','replace').replace('\r\n','\n')
            def තහවුරු_කරන්න(පෙළ,*값들):
                පිළිතුරු_දෙන්න=කවචය(පෙළ)
                for අගය in 값들:assert ipTestText(අගය) in පිළිතුරු_දෙන්න,(පෙළ,අගය,පිළිතුරු_දෙන්න)
                return පිළිතුරු_දෙන්න
            try:
                받기(b'jkoros-native> ')
                if not විස්තාරක.poweroff_only:
                    උදව්ව_අගය=තහවුරු_කරන්න('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in කෙටිමඟ_අගය_0a38607b.values():assert 별칭 in උදව්ව_අගය,(별칭,උදව්ව_අගය)
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['help']+' system','Network / system')
                    තහවුරු_කරන්න('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['ipconfig'],'inet 10.0.2.15');තහවුරු_කරන්න('ip addr show','sl0: UP');තහවුරු_කරන්න('ifconfig','sl0: UP')
                    for අවලංගු_පසුතල in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        දෝෂය=තහවුරු_කරන්න('ipconfig set '+අවලංගු_පසුතල+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in දෝෂය,දෝෂය
                        තහවුරු_කරන්න('ipconfig','inet 10.0.2.15')
                    තහවුරු_කරන්න('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    තහවුරු_කරන්න('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    තහවුරු_කරන්න('ip link set dev sl0 down','sl0: DOWN');තහවුරු_කරන්න('ping -c 1 10.0.2.2; echo STATUS=$?','දෝෂය -100','STATUS=1')
                    තහවුරු_කරන්න('ipconfig up','sl0: UP')
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    තහවුරු_කරන්න('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    තහවුරු_කරන්න('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['route'],'10.0.2.2 sl0')
                    තහවුරු_කරන්න('ftpd start','FTP listening')
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['netstat'],'10.0.2.20:21','LISTEN');තහවුරු_කරන්න('ss','LISTEN')
                    තහවුරු_කරන්න('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','දෝෂය -16')
                    with ftplib.FTP() as සේවාලාභීයා_අගය:
                        සේවාලාභීයා_අගය.connect('127.0.0.2',접속번호,timeout=20);සේවාලාභීයා_අගය.login();දත්ත=b'Network address was changed in the guest.\n'
                        සේවාලාභීයා_අගය.storbinary('STOR net-state.txt',io.BytesIO(දත්ත));받은자료=bytearray();සේවාලාභීයා_අගය.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==දත්ත;සේවාලාභීයා_අගය.delete('net-state.txt')
                    තහවුරු_කරන්න('ftpd stop','FTP stopped');තහවුරු_කරන්න('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    වාර්තාව_අගය['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(පෙළ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',පෙළ);assert 찾음,පෙළ;return tuple(map(int,찾음.groups()))
                    전=저장값(තහවුරු_කරන්න('df','RAM only'));තහවුරු_කරන්න('echo disk-proof > sys-state.txt');후=저장값(තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    තහවුරු_කරන්න('rm sys-state.txt');assert 저장값(කවචය('df'))==전
                    මතකය_අගය=තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',මතකය_අගය).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['ps'],'kernel/shell');තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['uptime'],'seconds')
                    තත්වය_තතු=තහවුරු_කරන්න(කෙටිමඟ_අගය_0a38607b['top']+' -n 2','kernel/shell');assert තත්වය_තතු.count('PID SLOT STATE')==2,තත්වය_තතු
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    තහවුරු_කරන්න('terminal','TERMINAL READY');ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ඊමේල්(b'vi process.txt\n');받기(b'NORMAL',ක්_රියාත්මක_කරන්න_2)
                    ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ඊමේල්(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ක්_රියාත්මක_කරන්න_2)
                    පිවිසුම_ලැයිස්තුව=තහවුරු_කරන්න('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',පිවිසුම_ලැයිස්තුව);assert 찾음 and int(찾음.group(2))>0,පිවිසුම_ලැයිස්තුව
                    තහවුරු_කරන්න('free','EL0 mapped KiB: '+찾음.group(2))
                    ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ඊමේල්(b'top\n');받기(b'PID SLOT STATE',ක්_රියාත්මක_කරන්න_2);ඊමේල්(b'q');받기(b'jkoros-native> ',ක්_රියාත්මක_කරන්න_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if කෙටිමඟ_අගය_0a38607b['df']!='df':
                        ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ඊමේල්((කෙටිමඟ_අගය_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',ක්_රියාත්මක_කරන්න_2);받기(b'jkoros-native> ',ක්_රියාත්මක_කරන්න_2)
                    වාර්තාව_අගය['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as පාලකය_අගය:
                    පාලකය_අගය.settimeout(15);පාලකය_අගය.connect(str(පාලකය_පෙත));දහර_අගය=පාලකය_අගය.makefile('rwb');json.loads(දහර_අගය.readline());දහර_අගය.write(b'{"execute":"qmp_capabilities"}\n');දහර_අගය.flush()
                    while 'return' not in json.loads(දහර_අගය.readline()):pass
                    ඊමේල්((('poweroff' if විස්තාරක.poweroff_only else කෙටිමඟ_අගය_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        සිදුවීම=json.loads(දහර_අගය.readline())
                        if සිදුවීම.get('event')=='SHUTDOWN':break
                    assert සිදුවීම['data']['guest'] and සිදුවීම['data']['reason']=='guest-shutdown',සිදුවීම
                    assert ක්_රියාවලිය_අගය.wait(timeout=15)==0
                    වාර්තාව_අගය['shutdown']=සිදුවීම;වාර්තාව_අගය['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                වාර්තාව_අගය['network_trace']=පාලම_අගය.추적기록
                assert විස්තාරක.poweroff_only or any(පිවිසුම_අගය['protocol']==1 and පිවිසුම_අගය['direction']=='from_guest' for පිවිසුම_අගය in පාලම_අගය.추적기록)
                වාර්තාව_අගය['passed']=True
            finally:
                if ක්_රියාවලිය_අගය.poll() is None:os.killpg(ක්_රියාවලිය_අගය.pid,signal.SIGTERM)
                try:ක්_රියාවලිය_අගය.wait(timeout=10)
                except subprocess.TimeoutExpired:ක්_රියාවලිය_අගය.kill();ක්_රියාවලිය_අගය.wait()
                තෝරන්න_අයිතමය.close();(출력/'serial.log').write_bytes(ලොගය_පේළිය);(출력/'report.json').write_text(json.dumps(වාර්තාව_අගය,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({යතුර_අගය:අගය for යතුර_අගය,අගය in වාර්තාව_අගය.items() if යතුර_අගය!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
