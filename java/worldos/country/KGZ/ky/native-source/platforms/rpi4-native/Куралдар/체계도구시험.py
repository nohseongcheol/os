#!/usr/bin/env python3
"""актуалдуу_берилмелер 자체 커널의 IP/ICMP, абал_маани сурам_маани, 현지어 Команда, 게스트 Чыгуу_програм жарактуулугун_текшерүү."""
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


def Жүргүзүү():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Орнотуулар={};аты_жадыбал={}
    if 인수.edition:
        나라=인수.edition.resolve();Орнотуулар=json.loads((나라/'native.json').read_text());аты_жадыбал=Орнотуулар['identifiers'];기준=나라/Орнотуулар['source']/Орнотуулар['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        кабылдоо=나라/'host/qemu'
        if кабылдоо.is_file():os.environ['QEMU_AARCH64']=str(кабылдоо)
    Куралдар=기준/Path(Орнотуулар.get('runner','Куралдар/аткаруу_буйрук.py')).parent
    sys.path.insert(0,str(Куралдар))
    def Окуу(Аты):
        ЖОЛ=Куралдар/(аты_жадыбал.get(Аты,Аты)+'.py');иш_маани=importlib.util.spec_from_file_location('test_'+Аты,str(ЖОЛ));모듈=importlib.util.module_from_spec(иш_маани);иш_маани.loader.exec_module(모듈);return 모듈
    실행모듈=Окуу('аткаруу_буйрук');망모듈=Окуу('통신다리');Команда=getattr(실행모듈,аты_жадыбал.get('Команда','Команда'));다리형=getattr(망모듈,аты_жадыбал.get('통신다리','통신다리'))
    жашырын_ат_маани=Орнотуулар.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_дарек','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'көрсөтүү_жардам'})
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
    Чыгыш=인수.output or 기준/'build/verification/system-tools';Чыгыш.mkdir(parents=True,exist_ok=True)
    отчет_маани_ddf2aaf3={'passed':False,'country':Орнотуулар.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    жазуу_катар=bytearray();ЫРААТТУУЛУК_маани=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        башкаруу_жол=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Издөө_маани:Издөө_маани.bind(('127.0.0.1',0));접속번호=Издөө_маани.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,тартуу_жаздыруу=True,게스트주소=ipTestText('10.0.2.20'),кабылдоо_дарек='127.0.0.2') as 다리:
            Процесс_маани=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(башкаруу_жол)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            тандоо_элемент=selectors.DefaultSelector();тандоо_элемент.register(Процесс_маани.stdout,selectors.EVENT_READ)
            def 받기(көрсөтүү_маани,Жүргүзүү=0,제한=45):
                끝=time.monotonic()+제한
                while көрсөтүү_маани not in жазуу_катар[Жүргүзүү:]:
                    if time.monotonic()>끝 or Процесс_маани.poll() is not None:raise AssertionError('Missing '+repr(көрсөтүү_маани)+'\n'+жазуу_катар[Жүргүзүү:].decode('utf-8','replace'))
                    for ачкыч_маани,_ in тандоо_элемент.select(.1):
                        берилмелер=ачкыч_маани.fileobj.read(65536)
                        if берилмелер:жазуу_катар.extend(берилмелер)
                return жазуу_катар[Жүргүзүү:].decode('utf-8','replace').replace('\r\n','\n')
            def жөнөтүү(берилмелер):Процесс_маани.stdin.write(берилмелер);Процесс_маани.stdin.flush()
            def сырты(Текст):
                Текст=ipTestText(Текст)
                print(отчет_маани_ddf2aaf3['country'],Текст,flush=True);ЫРААТТУУЛУК_маани[0]+=1;көрсөтүү_маани='__SYSTEM_DONE_'+str(ЫРААТТУУЛУК_маани[0])+'__';Жүргүзүү=len(жазуу_катар)
                жөнөтүү((Текст+'; echo; echo '+көрсөтүү_маани+'\n').encode())
                끝표시=('\r\n'+көрсөтүү_маани+'\r\n').encode();받기(끝표시,Жүргүзүү)
                끝자리=жазуу_катар.index(끝표시,Жүргүзүү)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return жазуу_катар[Жүргүзүү:].decode('utf-8','replace').replace('\r\n','\n')
            def тууралыгын_аныктоо(Текст,*값들):
                жооп_берүү=сырты(Текст)
                for маани in 값들:assert ipTestText(маани) in жооп_берүү,(Текст,маани,жооп_берүү)
                return жооп_берүү
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    жардам_маани=тууралыгын_аныктоо('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in жашырын_ат_маани.values():assert 별칭 in жардам_маани,(별칭,жардам_маани)
                    тууралыгын_аныктоо(жашырын_ат_маани['help']+' system','Network / system')
                    тууралыгын_аныктоо('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    тууралыгын_аныктоо(жашырын_ат_маани['ipconfig'],'inet 10.0.2.15');тууралыгын_аныктоо('ip addr show','sl0: UP');тууралыгын_аныктоо('ifconfig','sl0: UP')
                    for бузук_Орнотуулар in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Ката=тууралыгын_аныктоо('ipconfig set '+бузук_Орнотуулар+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Ката,Ката
                        тууралыгын_аныктоо('ipconfig','inet 10.0.2.15')
                    тууралыгын_аныктоо('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    тууралыгын_аныктоо(жашырын_ат_маани['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тууралыгын_аныктоо('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    тууралыгын_аныктоо('ip link set dev sl0 down','sl0: DOWN');тууралыгын_аныктоо('ping -c 1 10.0.2.2; echo STATUS=$?','Ката -100','STATUS=1')
                    тууралыгын_аныктоо('ipconfig up','sl0: UP')
                    тууралыгын_аныктоо(жашырын_ат_маани['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    тууралыгын_аныктоо('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тууралыгын_аныктоо('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');тууралыгын_аныктоо(жашырын_ат_маани['route'],'10.0.2.2 sl0')
                    тууралыгын_аныктоо('ftpd start','FTP listening')
                    тууралыгын_аныктоо(жашырын_ат_маани['netstat'],'10.0.2.20:21','LISTEN');тууралыгын_аныктоо('ss','LISTEN')
                    тууралыгын_аныктоо('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Ката -16')
                    with ftplib.FTP() as керектөөчү_маани:
                        керектөөчү_маани.connect('127.0.0.2',접속번호,timeout=20);керектөөчү_маани.login();берилмелер=b'Network address was changed in the guest.\n'
                        керектөөчү_маани.storbinary('STOR net-state.txt',io.BytesIO(берилмелер));받은자료=bytearray();керектөөчү_маани.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==берилмелер;керектөөчү_маани.delete('net-state.txt')
                    тууралыгын_аныктоо('ftpd stop','FTP stopped');тууралыгын_аныктоо('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    отчет_маани_ddf2aaf3['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Текст);assert 찾음,Текст;return tuple(map(int,찾음.groups()))
                    전=저장값(тууралыгын_аныктоо('df','RAM only'));тууралыгын_аныктоо('echo disk-proof > sys-state.txt');후=저장값(тууралыгын_аныктоо(жашырын_ат_маани['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    тууралыгын_аныктоо('rm sys-state.txt');assert 저장값(сырты('df'))==전
                    эс_маани=тууралыгын_аныктоо(жашырын_ат_маани['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',эс_маани).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    тууралыгын_аныктоо(жашырын_ат_маани['ps'],'kernel/shell');тууралыгын_аныктоо(жашырын_ат_маани['uptime'],'seconds')
                    абал_маалымат=тууралыгын_аныктоо(жашырын_ат_маани['top']+' -n 2','kernel/shell');assert абал_маалымат.count('PID SLOT STATE')==2,абал_маалымат
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    тууралыгын_аныктоо('terminal','TERMINAL READY');Жүргүзүү=len(жазуу_катар);жөнөтүү(b'vi process.txt\n');받기(b'NORMAL',Жүргүзүү)
                    Жүргүзүү=len(жазуу_катар);жөнөтүү(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Жүргүзүү)
                    киргизме_жазуу_Тизме=тууралыгын_аныктоо('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',киргизме_жазуу_Тизме);assert 찾음 and int(찾음.group(2))>0,киргизме_жазуу_Тизме
                    тууралыгын_аныктоо('free','EL0 mapped KiB: '+찾음.group(2))
                    Жүргүзүү=len(жазуу_катар);жөнөтүү(b'top\n');받기(b'PID SLOT STATE',Жүргүзүү);жөнөтүү(b'q');받기(b'jkoros-native> ',Жүргүзүү)
                    # Test a multibyte prefix through the real shell completion path.
                    if жашырын_ат_маани['df']!='df':
                        Жүргүзүү=len(жазуу_катар);жөнөтүү((жашырын_ат_маани['df'][:-1]+'\t\n').encode());받기(b'RAM only',Жүргүзүү);받기(b'jkoros-native> ',Жүргүзүү)
                    отчет_маани_ddf2aaf3['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as башкаруу_маани:
                    башкаруу_маани.settimeout(15);башкаруу_маани.connect(str(башкаруу_жол));агым_маани=башкаруу_маани.makefile('rwb');json.loads(агым_маани.readline());агым_маани.write(b'{"execute":"qmp_capabilities"}\n');агым_маани.flush()
                    while 'return' not in json.loads(агым_маани.readline()):pass
                    жөнөтүү((('poweroff' if 인수.poweroff_only else жашырын_ат_маани['poweroff'])+'\n').encode())
                    while True:
                        окуя=json.loads(агым_маани.readline())
                        if окуя.get('event')=='SHUTDOWN':break
                    assert окуя['data']['guest'] and окуя['data']['reason']=='guest-shutdown',окуя
                    assert Процесс_маани.wait(timeout=15)==0
                    отчет_маани_ddf2aaf3['shutdown']=окуя;отчет_маани_ddf2aaf3['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                отчет_маани_ddf2aaf3['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(киргизме_жазуу_маани['protocol']==1 and киргизме_жазуу_маани['direction']=='from_guest' for киргизме_жазуу_маани in 다리.추적기록)
                отчет_маани_ddf2aaf3['passed']=True
            finally:
                if Процесс_маани.poll() is None:os.killpg(Процесс_маани.pid,signal.SIGTERM)
                try:Процесс_маани.wait(timeout=10)
                except subprocess.TimeoutExpired:Процесс_маани.kill();Процесс_маани.wait()
                тандоо_элемент.close();(Чыгыш/'serial.log').write_bytes(жазуу_катар);(Чыгыш/'report.json').write_text(json.dumps(отчет_маани_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ачкыч_маани:маани for ачкыч_маани,маани in отчет_маани_ddf2aaf3.items() if ачкыч_маани!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Жүргүзүү()
