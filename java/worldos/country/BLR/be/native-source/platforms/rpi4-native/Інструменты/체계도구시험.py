#!/usr/bin/env python3
"""фактычны_дадзеныя 자체 커널의 IP/ICMP, стан_значэнне запыт_значэнне, 현지어 Загад, 게스트 Выхад_праграма праверыць_5fb2b747."""
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


def Выканаць():
    аналізатар_48ee4b1b=argparse.ArgumentParser();аналізатар_48ee4b1b.add_argument('--edition',type=Path);аналізатар_48ee4b1b.add_argument('--output',type=Path);аналізатар_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=аналізатар_48ee4b1b.parse_args()
    기준=Path(__file__).resolve().parents[1];Усталёўкі={};імя_табліца={}
    if 인수.edition:
        나라=인수.edition.resolve();Усталёўкі=json.loads((나라/'native.json').read_text());імя_табліца=Усталёўкі['identifiers'];기준=나라/Усталёўкі['source']/Усталёўкі['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        вузел=나라/'host/qemu'
        if вузел.is_file():os.environ['QEMU_AARCH64']=str(вузел)
    Інструменты=기준/Path(Усталёўкі.get('runner','Інструменты/выканаць_каманда.py')).parent
    sys.path.insert(0,str(Інструменты))
    def Чытанне(Назва):
        ШЛЯХ=Інструменты/(імя_табліца.get(Назва,Назва)+'.py');зварот_значэнне=importlib.util.spec_from_file_location('test_'+Назва,str(ШЛЯХ));модуль_значэнне=importlib.util.module_from_spec(зварот_значэнне);зварот_значэнне.loader.exec_module(модуль_значэнне);return модуль_значэнне
    실행모듈=Чытанне('выканаць_каманда');Сетка_модуль=Чытанне('Сетка_мост');Загад=getattr(실행모듈,імя_табліца.get('Загад','Загад'));мост_друкаваць=getattr(Сетка_модуль,імя_табліца.get('Сетка_мост','Сетка_мост'))
    ярлык_значэнне_0a38607b=Усталёўкі.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адрас','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'паказаць_даведка'})
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
    Выхад=인수.output or 기준/'build/verification/system-tools';Выхад.mkdir(parents=True,exist_ok=True)
    справаздача_значэнне={'passed':False,'country':Усталёўкі.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    журнал_запіс=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        кіраванне_шлях=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Пошук_значэнне:Пошук_значэнне.bind(('127.0.0.1',0));нумар_порта=Пошук_значэнне.getsockname()[1]
            if not 50000<=нумар_порта<=50007:break
        with мост_друкаваць(нумар_порта,зняць=True,госць_адрас=ipTestText('10.0.2.20'),вузел_адрас='127.0.0.2') as мост_значэнне:
            Працэс_значэнне=subprocess.Popen(Загад()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(кіраванне_шлях)]+мост_значэнне.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            выбіраць_элемент=selectors.DefaultSelector();выбіраць_элемент.register(Працэс_значэнне.stdout,selectors.EVENT_READ)
            def 받기(паказаць_значэнне,Выканаць=0,제한=45):
                끝=time.monotonic()+제한
                while паказаць_значэнне not in журнал_запіс[Выканаць:]:
                    if time.monotonic()>끝 or Працэс_значэнне.poll() is not None:raise AssertionError('Missing '+repr(паказаць_значэнне)+'\n'+журнал_запіс[Выканаць:].decode('utf-8','replace'))
                    for клавіша_значэнне,_ in выбіраць_элемент.select(.1):
                        дадзеныя=клавіша_значэнне.fileobj.read(65536)
                        if дадзеныя:журнал_запіс.extend(дадзеныя)
                return журнал_запіс[Выканаць:].decode('utf-8','replace').replace('\r\n','\n')
            def адправіць(дадзеныя):Працэс_значэнне.stdin.write(дадзеныя);Працэс_значэнне.stdin.flush()
            def абалонка(Тэкст):
                Тэкст=ipTestText(Тэкст)
                print(справаздача_значэнне['country'],Тэкст,flush=True);차례[0]+=1;паказаць_значэнне='__SYSTEM_DONE_'+str(차례[0])+'__';Выканаць=len(журнал_запіс)
                адправіць((Тэкст+'; echo; echo '+паказаць_значэнне+'\n').encode())
                끝표시=('\r\n'+паказаць_значэнне+'\r\n').encode();받기(끝표시,Выканаць)
                끝자리=журнал_запіс.index(끝표시,Выканаць)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return журнал_запіс[Выканаць:].decode('utf-8','replace').replace('\r\n','\n')
            def праверыць(Тэкст,*값들):
                адказаць=абалонка(Тэкст)
                for значэнне in 값들:assert ipTestText(значэнне) in адказаць,(Тэкст,значэнне,адказаць)
                return адказаць
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    даведка_значэнне=праверыць('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ярлык_значэнне_0a38607b.values():assert 별칭 in даведка_значэнне,(별칭,даведка_значэнне)
                    праверыць(ярлык_значэнне_0a38607b['help']+' system','Network / system')
                    праверыць('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    праверыць(ярлык_значэнне_0a38607b['ipconfig'],'inet 10.0.2.15');праверыць('ip addr show','sl0: UP');праверыць('ifconfig','sl0: UP')
                    for памылковы_Налады in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ПАМЫЛКА=праверыць('ipconfig set '+памылковы_Налады+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ПАМЫЛКА,ПАМЫЛКА
                        праверыць('ipconfig','inet 10.0.2.15')
                    праверыць('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    праверыць(ярлык_значэнне_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    праверыць('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    праверыць('ip link set dev sl0 down','sl0: DOWN');праверыць('ping -c 1 10.0.2.2; echo STATUS=$?','ПАМЫЛКА -100','STATUS=1')
                    праверыць('ipconfig up','sl0: UP')
                    праверыць(ярлык_значэнне_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    праверыць('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    праверыць('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');праверыць(ярлык_значэнне_0a38607b['route'],'10.0.2.2 sl0')
                    праверыць('ftpd start','FTP listening')
                    праверыць(ярлык_значэнне_0a38607b['netstat'],'10.0.2.20:21','LISTEN');праверыць('ss','LISTEN')
                    праверыць('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ПАМЫЛКА -16')
                    with ftplib.FTP() as кліент_значэнне:
                        кліент_значэнне.connect('127.0.0.2',нумар_порта,timeout=20);кліент_значэнне.login();дадзеныя=b'Network address was changed in the guest.\n'
                        кліент_значэнне.storbinary('STOR net-state.txt',io.BytesIO(дадзеныя));받은자료=bytearray();кліент_значэнне.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==дадзеныя;кліент_значэнне.delete('net-state.txt')
                    праверыць('ftpd stop','FTP stopped');праверыць('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    справаздача_значэнне['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Тэкст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Тэкст);assert 찾음,Тэкст;return tuple(map(int,찾음.groups()))
                    전=저장값(праверыць('df','RAM only'));праверыць('echo disk-proof > sys-state.txt');후=저장값(праверыць(ярлык_значэнне_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    праверыць('rm sys-state.txt');assert 저장값(абалонка('df'))==전
                    памяць_значэнне=праверыць(ярлык_значэнне_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',памяць_значэнне).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    праверыць(ярлык_значэнне_0a38607b['ps'],'kernel/shell');праверыць(ярлык_значэнне_0a38607b['uptime'],'seconds')
                    стан_звесткі=праверыць(ярлык_значэнне_0a38607b['top']+' -n 2','kernel/shell');assert стан_звесткі.count('PID SLOT STATE')==2,стан_звесткі
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    праверыць('terminal','TERMINAL READY');Выканаць=len(журнал_запіс);адправіць(b'vi process.txt\n');받기(b'NORMAL',Выканаць)
                    Выканаць=len(журнал_запіс);адправіць(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Выканаць)
                    увядзенне_Спіс=праверыць('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',увядзенне_Спіс);assert 찾음 and int(찾음.group(2))>0,увядзенне_Спіс
                    праверыць('free','EL0 mapped KiB: '+찾음.group(2))
                    Выканаць=len(журнал_запіс);адправіць(b'top\n');받기(b'PID SLOT STATE',Выканаць);адправіць(b'q');받기(b'jkoros-native> ',Выканаць)
                    # Test a multibyte prefix through the real shell completion path.
                    if ярлык_значэнне_0a38607b['df']!='df':
                        Выканаць=len(журнал_запіс);адправіць((ярлык_значэнне_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Выканаць);받기(b'jkoros-native> ',Выканаць)
                    справаздача_значэнне['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as кіраванне_значэнне:
                    кіраванне_значэнне.settimeout(15);кіраванне_значэнне.connect(str(кіраванне_шлях));паток_значэнне=кіраванне_значэнне.makefile('rwb');json.loads(паток_значэнне.readline());паток_значэнне.write(b'{"execute":"qmp_capabilities"}\n');паток_значэнне.flush()
                    while 'return' not in json.loads(паток_значэнне.readline()):pass
                    адправіць((('poweroff' if 인수.poweroff_only else ярлык_значэнне_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Падзея=json.loads(паток_значэнне.readline())
                        if Падзея.get('event')=='SHUTDOWN':break
                    assert Падзея['data']['guest'] and Падзея['data']['reason']=='guest-shutdown',Падзея
                    assert Працэс_значэнне.wait(timeout=15)==0
                    справаздача_значэнне['shutdown']=Падзея;справаздача_значэнне['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                справаздача_значэнне['network_trace']=мост_значэнне.след_журнал
                assert 인수.poweroff_only or any(увядзенне_значэнне['protocol']==1 and увядзенне_значэнне['direction']=='from_guest' for увядзенне_значэнне in мост_значэнне.след_журнал)
                справаздача_значэнне['passed']=True
            finally:
                if Працэс_значэнне.poll() is None:os.killpg(Працэс_значэнне.pid,signal.SIGTERM)
                try:Працэс_значэнне.wait(timeout=10)
                except subprocess.TimeoutExpired:Працэс_значэнне.kill();Працэс_значэнне.wait()
                выбіраць_элемент.close();(Выхад/'serial.log').write_bytes(журнал_запіс);(Выхад/'report.json').write_text(json.dumps(справаздача_значэнне,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({клавіша_значэнне:значэнне for клавіша_значэнне,значэнне in справаздача_значэнне.items() if клавіша_значэнне!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Выканаць()
