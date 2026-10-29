#!/usr/bin/env python3
"""стваран_подаци 자체 커널의 IP/ICMP, стање_вриједност упит_вриједност, 현지어 команда, 게스트 изаћи_програм овјерити."""
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


def 시작():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Подешавања={};назив_табела={}
    if 인수.edition:
        나라=인수.edition.resolve();Подешавања=json.loads((나라/'native.json').read_text());назив_табела=Подешавања['identifiers'];기준=나라/Подешавања['source']/Подешавања['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        хост_рачунар=나라/'host/qemu'
        if хост_рачунар.is_file():os.environ['QEMU_AARCH64']=str(хост_рачунар)
    도구=기준/Path(Подешавања.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def 읽기(назив):
        пут=도구/(назив_табела.get(назив,назив)+'.py');Уговор_вриједност=importlib.util.spec_from_file_location('test_'+назив,str(пут));모듈=importlib.util.module_from_spec(Уговор_вриједност);Уговор_вриједност.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('실행');망모듈=읽기('통신다리');команда=getattr(실행모듈,назив_табела.get('команда','команда'));다리형=getattr(망모듈,назив_табела.get('통신다리','통신다리'))
    пречица_вриједност_0a38607b=Подешавања.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адреса','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'приказати_помоћ'})
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
    извјештај_вриједност={'passed':False,'country':Подешавања.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    дневник_рада_ред=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        контрола_пут=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as тражити_вриједност:тражити_вриједност.bind(('127.0.0.1',0));접속번호=тражити_вриједност.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),хост_рачунар_адреса='127.0.0.2') as 다리:
            процес_вриједност=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(контрола_пут)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            изабрати_ставка=selectors.DefaultSelector();изабрати_ставка.register(процес_вриједност.stdout,selectors.EVENT_READ)
            def 받기(приказати_вриједност,시작=0,제한=45):
                끝=time.monotonic()+제한
                while приказати_вриједност not in дневник_рада_ред[시작:]:
                    if time.monotonic()>끝 or процес_вриједност.poll() is not None:raise AssertionError('Missing '+repr(приказати_вриједност)+'\n'+дневник_рада_ред[시작:].decode('utf-8','replace'))
                    for кључ_вриједност,_ in изабрати_ставка.select(.1):
                        подаци=кључ_вриједност.fileobj.read(65536)
                        if подаци:дневник_рада_ред.extend(подаци)
                return дневник_рада_ред[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def послати(подаци):процес_вриједност.stdin.write(подаци);процес_вриједност.stdin.flush()
            def љуска(текст):
                текст=ipTestText(текст)
                print(извјештај_вриједност['country'],текст,flush=True);차례[0]+=1;приказати_вриједност='__SYSTEM_DONE_'+str(차례[0])+'__';시작=len(дневник_рада_ред)
                послати((текст+'; echo; echo '+приказати_вриједност+'\n').encode())
                끝표시=('\r\n'+приказати_вриједност+'\r\n').encode();받기(끝표시,시작)
                끝자리=дневник_рада_ред.index(끝표시,시작)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return дневник_рада_ред[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def потврдити(текст,*값들):
                응답=љуска(текст)
                for вриједност in 값들:assert ipTestText(вриједност) in 응답,(текст,вриједност,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    помоћ_вриједност=потврдити('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in пречица_вриједност_0a38607b.values():assert 별칭 in помоћ_вриједност,(별칭,помоћ_вриједност)
                    потврдити(пречица_вриједност_0a38607b['help']+' system','Network / system')
                    потврдити('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    потврдити(пречица_вриједност_0a38607b['ipconfig'],'inet 10.0.2.15');потврдити('ip addr show','sl0: UP');потврдити('ifconfig','sl0: UP')
                    for Неважећи_Подешавања in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        грешка=потврдити('ipconfig set '+Неважећи_Подешавања+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in грешка,грешка
                        потврдити('ipconfig','inet 10.0.2.15')
                    потврдити('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    потврдити(пречица_вриједност_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    потврдити('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    потврдити('ip link set dev sl0 down','sl0: DOWN');потврдити('ping -c 1 10.0.2.2; echo STATUS=$?','грешка -100','STATUS=1')
                    потврдити('ipconfig up','sl0: UP')
                    потврдити(пречица_вриједност_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    потврдити('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    потврдити('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');потврдити(пречица_вриједност_0a38607b['route'],'10.0.2.2 sl0')
                    потврдити('ftpd start','FTP listening')
                    потврдити(пречица_вриједност_0a38607b['netstat'],'10.0.2.20:21','LISTEN');потврдити('ss','LISTEN')
                    потврдити('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','грешка -16')
                    with ftplib.FTP() as клијент_вриједност:
                        клијент_вриједност.connect('127.0.0.2',접속번호,timeout=20);клијент_вриједност.login();подаци=b'Network address was changed in the guest.\n'
                        клијент_вриједност.storbinary('STOR net-state.txt',io.BytesIO(подаци));받은자료=bytearray();клијент_вриједност.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==подаци;клијент_вриједност.delete('net-state.txt')
                    потврдити('ftpd stop','FTP stopped');потврдити('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    извјештај_вриједност['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',текст);assert 찾음,текст;return tuple(map(int,찾음.groups()))
                    전=저장값(потврдити('df','RAM only'));потврдити('echo disk-proof > sys-state.txt');후=저장값(потврдити(пречица_вриједност_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    потврдити('rm sys-state.txt');assert 저장값(љуска('df'))==전
                    меморија_вриједност=потврдити(пречица_вриједност_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',меморија_вриједност).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    потврдити(пречица_вриједност_0a38607b['ps'],'kernel/shell');потврдити(пречица_вриједност_0a38607b['uptime'],'seconds')
                    стање_информација=потврдити(пречица_вриједност_0a38607b['top']+' -n 2','kernel/shell');assert стање_информација.count('PID SLOT STATE')==2,стање_информација
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    потврдити('terminal','TERMINAL READY');시작=len(дневник_рада_ред);послати(b'vi process.txt\n');받기(b'NORMAL',시작)
                    시작=len(дневник_рада_ред);послати(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',시작)
                    унос_списак=потврдити('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',унос_списак);assert 찾음 and int(찾음.group(2))>0,унос_списак
                    потврдити('free','EL0 mapped KiB: '+찾음.group(2))
                    시작=len(дневник_рада_ред);послати(b'top\n');받기(b'PID SLOT STATE',시작);послати(b'q');받기(b'jkoros-native> ',시작)
                    # Test a multibyte prefix through the real shell completion path.
                    if пречица_вриједност_0a38607b['df']!='df':
                        시작=len(дневник_рада_ред);послати((пречица_вриједност_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',시작);받기(b'jkoros-native> ',시작)
                    извјештај_вриједност['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as контрола_вриједност:
                    контрола_вриједност.settimeout(15);контрола_вриједност.connect(str(контрола_пут));ток_вриједност=контрола_вриједност.makefile('rwb');json.loads(ток_вриједност.readline());ток_вриједност.write(b'{"execute":"qmp_capabilities"}\n');ток_вриједност.flush()
                    while 'return' not in json.loads(ток_вриједност.readline()):pass
                    послати((('poweroff' if 인수.poweroff_only else пречица_вриједност_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        догађај=json.loads(ток_вриједност.readline())
                        if догађај.get('event')=='SHUTDOWN':break
                    assert догађај['data']['guest'] and догађај['data']['reason']=='guest-shutdown',догађај
                    assert процес_вриједност.wait(timeout=15)==0
                    извјештај_вриједност['shutdown']=догађај;извјештај_вриједност['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                извјештај_вриједност['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(унос_вриједност['protocol']==1 and унос_вриједност['direction']=='from_guest' for унос_вриједност in 다리.추적기록)
                извјештај_вриједност['passed']=True
            finally:
                if процес_вриједност.poll() is None:os.killpg(процес_вриједност.pid,signal.SIGTERM)
                try:процес_вриједност.wait(timeout=10)
                except subprocess.TimeoutExpired:процес_вриједност.kill();процес_вриједност.wait()
                изабрати_ставка.close();(출력/'serial.log').write_bytes(дневник_рада_ред);(출력/'report.json').write_text(json.dumps(извјештај_вриједност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({кључ_вриједност:вриједност for кључ_вриједност,вриједност in извјештај_вриједност.items() if кључ_вриједност!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':시작()
