#!/usr/bin/env python3
"""фактик_мәгълүмат 자체 커널의 IP/ICMP, халәт_VALUE таләп_VALUE, 현지어 команда, 게스트 Чыгу_кушымта тикшерү."""
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


def эшләтү():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    экранга_җибәрү_тамыр=Path(__file__).resolve().parents[1];Caylaw={};исем_таблица={}
    if 인수.edition:
        나라=인수.edition.resolve();Caylaw=json.loads((나라/'native.json').read_text());исем_таблица=Caylaw['identifiers'];экранга_җибәрү_тамыр=나라/Caylaw['source']/Caylaw['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        хост=나라/'host/qemu'
        if хост.is_file():os.environ['QEMU_AARCH64']=str(хост)
    Кораллар=экранга_җибәрү_тамыр/Path(Caylaw.get('runner','Кораллар/үтәргә_команда.py')).parent
    sys.path.insert(0,str(Кораллар))
    def 읽기(исем):
        Yul=Кораллар/(исем_таблица.get(исем,исем)+'.py');бирем_VALUE_102996da=importlib.util.spec_from_file_location('test_'+исем,str(Yul));модуль_VALUE=importlib.util.module_from_spec(бирем_VALUE_102996da);бирем_VALUE_102996da.loader.exec_module(модуль_VALUE);return модуль_VALUE
    실행모듈=읽기('үтәргә_команда');Челтәр_модуль=읽기('Челтәр_күпер');команда=getattr(실행모듈,исем_таблица.get('команда','команда'));күпер_TYPE=getattr(Челтәр_модуль,исем_таблица.get('Челтәр_күпер','Челтәр_күпер'))
    ярлык_VALUE_0a38607b=Caylaw.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адрес','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'күрсәтү_ярдәм'})
    sys.path.insert(0,str(экранга_җибәрү_тамыр/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(экранга_җибәрү_тамыр);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or экранга_җибәрү_тамыр/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    отчет_VALUE={'passed':False,'country':Caylaw.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_юл=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        идарә_юл=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Эзләү_VALUE:Эзләү_VALUE.bind(('127.0.0.1',0));접속번호=Эзләү_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with күпер_TYPE(접속번호,яздыру=True,кунак_адрес=ipTestText('10.0.2.20'),хост_адрес='127.0.0.2') as күпер_VALUE:
            Процесс_VALUE=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(идарә_юл)]+күпер_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_элемент=selectors.DefaultSelector();CHOOSE_элемент.register(Процесс_VALUE.stdout,selectors.EVENT_READ)
            def 받기(күрсәтү_VALUE,эшләтү=0,제한=45):
                끝=time.monotonic()+제한
                while күрсәтү_VALUE not in LOG_юл[эшләтү:]:
                    if time.monotonic()>끝 or Процесс_VALUE.poll() is not None:raise AssertionError('Missing '+repr(күрсәтү_VALUE)+'\n'+LOG_юл[эшләтү:].decode('utf-8','replace'))
                    for ачкыч_VALUE,_ in CHOOSE_элемент.select(.1):
                        мәгълүмат=ачкыч_VALUE.fileobj.read(65536)
                        if мәгълүмат:LOG_юл.extend(мәгълүмат)
                return LOG_юл[эшләтү:].decode('utf-8','replace').replace('\r\n','\n')
            def җибәрү(мәгълүмат):Процесс_VALUE.stdin.write(мәгълүмат);Процесс_VALUE.stdin.flush()
            def тышча(Mäten):
                Mäten=ipTestText(Mäten)
                print(отчет_VALUE['country'],Mäten,flush=True);SEQUENCE_VALUE[0]+=1;күрсәтү_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';эшләтү=len(LOG_юл)
                җибәрү((Mäten+'; echo; echo '+күрсәтү_VALUE+'\n').encode())
                끝표시=('\r\n'+күрсәтү_VALUE+'\r\n').encode();받기(끝표시,эшләтү)
                тәмамлау_урнаштыру=LOG_юл.index(끝표시,эшләтү)+len(끝표시)
                받기(b'jkoros-native> ',тәмамлау_урнаштыру)
                return LOG_юл[эшләтү:].decode('utf-8','replace').replace('\r\n','\n')
            def раслау(Mäten,*값들):
                җавап_бирү=тышча(Mäten)
                for VALUE in 값들:assert ipTestText(VALUE) in җавап_бирү,(Mäten,VALUE,җавап_бирү)
                return җавап_бирү
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ярдәм_VALUE_8d901cc2=раслау('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ярлык_VALUE_0a38607b.values():assert 별칭 in ярдәм_VALUE_8d901cc2,(별칭,ярдәм_VALUE_8d901cc2)
                    раслау(ярлык_VALUE_0a38607b['help']+' system','Network / system')
                    раслау('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    раслау(ярлык_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');раслау('ip addr show','sl0: UP');раслау('ifconfig','sl0: UP')
                    for дөрес_булмаган_Параметрлар in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Хата=раслау('ipconfig set '+дөрес_булмаган_Параметрлар+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Хата,Хата
                        раслау('ipconfig','inet 10.0.2.15')
                    раслау('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    раслау(ярлык_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    раслау('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    раслау('ip link set dev sl0 down','sl0: DOWN');раслау('ping -c 1 10.0.2.2; echo STATUS=$?','Хата -100','STATUS=1')
                    раслау('ipconfig up','sl0: UP')
                    раслау(ярлык_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    раслау('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    раслау('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');раслау(ярлык_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    раслау('ftpd start','FTP listening')
                    раслау(ярлык_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');раслау('ss','LISTEN')
                    раслау('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Хата -16')
                    with ftplib.FTP() as клиент_VALUE:
                        клиент_VALUE.connect('127.0.0.2',접속번호,timeout=20);клиент_VALUE.login();мәгълүмат=b'Network address was changed in the guest.\n'
                        клиент_VALUE.storbinary('STOR net-state.txt',io.BytesIO(мәгълүмат));RECEIVED_мәгълүмат=bytearray();клиент_VALUE.retrbinary('RETR net-state.txt',RECEIVED_мәгълүмат.extend);assert RECEIVED_мәгълүмат==мәгълүмат;клиент_VALUE.delete('net-state.txt')
                    раслау('ftpd stop','FTP stopped');раслау('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    отчет_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Mäten):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Mäten);assert 찾음,Mäten;return tuple(map(int,찾음.groups()))
                    전=저장값(раслау('df','RAM only'));раслау('echo disk-proof > sys-state.txt');후=저장값(раслау(ярлык_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    раслау('rm sys-state.txt');assert 저장값(тышча('df'))==전
                    Хәтер_VALUE=раслау(ярлык_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Хәтер_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    раслау(ярлык_VALUE_0a38607b['ps'],'kernel/shell');раслау(ярлык_VALUE_0a38607b['uptime'],'seconds')
                    халәт_мәгълүмат=раслау(ярлык_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert халәт_мәгълүмат.count('PID SLOT STATE')==2,халәт_мәгълүмат
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    раслау('terminal','TERMINAL READY');эшләтү=len(LOG_юл);җибәрү(b'vi process.txt\n');받기(b'NORMAL',эшләтү)
                    эшләтү=len(LOG_юл);җибәрү(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',эшләтү)
                    кертү_Исемлек=раслау('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',кертү_Исемлек);assert 찾음 and int(찾음.group(2))>0,кертү_Исемлек
                    раслау('free','EL0 mapped KiB: '+찾음.group(2))
                    эшләтү=len(LOG_юл);җибәрү(b'top\n');받기(b'PID SLOT STATE',эшләтү);җибәрү(b'q');받기(b'jkoros-native> ',эшләтү)
                    # Test a multibyte prefix through the real shell completion path.
                    if ярлык_VALUE_0a38607b['df']!='df':
                        эшләтү=len(LOG_юл);җибәрү((ярлык_VALUE_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',эшләтү);받기(b'jkoros-native> ',эшләтү)
                    отчет_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as идарә_VALUE:
                    идарә_VALUE.settimeout(15);идарә_VALUE.connect(str(идарә_юл));агым_VALUE=идарә_VALUE.makefile('rwb');json.loads(агым_VALUE.readline());агым_VALUE.write(b'{"execute":"qmp_capabilities"}\n');агым_VALUE.flush()
                    while 'return' not in json.loads(агым_VALUE.readline()):pass
                    җибәрү((('poweroff' if 인수.poweroff_only else ярлык_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        вакыйга=json.loads(агым_VALUE.readline())
                        if вакыйга.get('event')=='SHUTDOWN':break
                    assert вакыйга['data']['guest'] and вакыйга['data']['reason']=='guest-shutdown',вакыйга
                    assert Процесс_VALUE.wait(timeout=15)==0
                    отчет_VALUE['shutdown']=вакыйга;отчет_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                отчет_VALUE['network_trace']=күпер_VALUE.추적기록
                assert 인수.poweroff_only or any(кертү_VALUE['protocol']==1 and кертү_VALUE['direction']=='from_guest' for кертү_VALUE in күпер_VALUE.추적기록)
                отчет_VALUE['passed']=True
            finally:
                if Процесс_VALUE.poll() is None:os.killpg(Процесс_VALUE.pid,signal.SIGTERM)
                try:Процесс_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Процесс_VALUE.kill();Процесс_VALUE.wait()
                CHOOSE_элемент.close();(출력/'serial.log').write_bytes(LOG_юл);(출력/'report.json').write_text(json.dumps(отчет_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ачкыч_VALUE:VALUE for ачкыч_VALUE,VALUE in отчет_VALUE.items() if ачкыч_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':эшләтү()
