#!/usr/bin/env python3
"""фактично_дані своє 커널의 IP/ICMP, Стан_значення запит_значення, 현지어 команда, 게스트 Вийти_програма затвердити."""
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


def запустити():
    аналізатор_48ee4b1b=argparse.ArgumentParser();аналізатор_48ee4b1b.add_argument('--edition',type=Path);аналізатор_48ee4b1b.add_argument('--output',type=Path);аналізатор_48ee4b1b.add_argument('--poweroff-only',action='store_true');аргументи=аналізатор_48ee4b1b.parse_args()
    Дії_корінь=Path(__file__).resolve().parents[1];Налаштування={};ім_я_таблиця={}
    if аргументи.edition:
        Кантрі_значення=аргументи.edition.resolve();Налаштування=json.loads((Кантрі_значення/'native.json').read_text());ім_я_таблиця=Налаштування['identifiers'];Дії_корінь=Кантрі_значення/Налаштування['source']/Налаштування['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Кантрі_значення/'native-edition.py'),'check'])
        хост=Кантрі_значення/'host/qemu'
        if хост.is_file():os.environ['QEMU_AARCH64']=str(хост)
    інструменти=Дії_корінь/Path(Налаштування.get('runner','інструменти/Виконати_команда.py')).parent
    sys.path.insert(0,str(інструменти))
    def Читання(Назва):
        шлях=інструменти/(ім_я_таблиця.get(Назва,Назва)+'.py');контракт_значення=importlib.util.spec_from_file_location('test_'+Назва,str(шлях));модуль_значення=importlib.util.module_from_spec(контракт_значення);контракт_значення.loader.exec_module(модуль_значення);return модуль_значення
    실행모듈=Читання('Виконати_команда');мережа_модуль=Читання('міст_3de4fe3a');команда=getattr(실행모듈,ім_я_таблиця.get('команда','команда'));міст_Тип=getattr(мережа_модуль,ім_я_таблиця.get('міст_3de4fe3a','міст_3de4fe3a'))
    ярлик_значення_0a38607b=Налаштування.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адреса','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'показати_довідку'})
    sys.path.insert(0,str(Дії_корінь/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Дії_корінь);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Вивід=аргументи.output or Дії_корінь/'build/verification/system-tools';Вивід.mkdir(parents=True,exist_ok=True)
    звіт_значення={'passed':False,'country':Налаштування.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    журнал_запис=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        керування_шлях=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Пошук_значення:Пошук_значення.bind(('127.0.0.1',0));номер_порту=Пошук_значення.getsockname()[1]
            if not 50000<=номер_порту<=50007:break
        with міст_Тип(номер_порту,записувати=True,гість_адреса=ipTestText('10.0.2.20'),хост_адреса='127.0.0.2') as міст_значення:
            процес_значення=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(керування_шлях)]+міст_значення.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            вибирати_елемент=selectors.DefaultSelector();вибирати_елемент.register(процес_значення.stdout,selectors.EVENT_READ)
            def отримувати(показувати_значення,запустити=0,제한=45):
                끝=time.monotonic()+제한
                while показувати_значення not in журнал_запис[запустити:]:
                    if time.monotonic()>끝 or процес_значення.poll() is not None:raise AssertionError('Missing '+repr(показувати_значення)+'\n'+журнал_запис[запустити:].decode('utf-8','replace'))
                    for Ключ_значення,_ in вибирати_елемент.select(.1):
                        дані=Ключ_значення.fileobj.read(65536)
                        if дані:журнал_запис.extend(дані)
                return журнал_запис[запустити:].decode('utf-8','replace').replace('\r\n','\n')
            def надсилати(дані):процес_значення.stdin.write(дані);процес_значення.stdin.flush()
            def оболонка(текст):
                текст=ipTestText(текст)
                print(звіт_значення['country'],текст,flush=True);차례[0]+=1;показувати_значення='__SYSTEM_DONE_'+str(차례[0])+'__';запустити=len(журнал_запис)
                надсилати((текст+'; echo; echo '+показувати_значення+'\n').encode())
                завершити_виклик_маркер=('\r\n'+показувати_значення+'\r\n').encode();отримувати(завершити_виклик_маркер,запустити)
                завершити_виклик_посада=журнал_запис.index(завершити_виклик_маркер,запустити)+len(завершити_виклик_маркер)
                отримувати(b'jkoros-native> ',завершити_виклик_посада)
                return журнал_запис[запустити:].decode('utf-8','replace').replace('\r\n','\n')
            def перевіряти(текст,*값들):
                відповідь=оболонка(текст)
                for значення in 값들:assert ipTestText(значення) in відповідь,(текст,значення,відповідь)
                return відповідь
            try:
                отримувати(b'jkoros-native> ')
                if not аргументи.poweroff_only:
                    довідка_значення=перевіряти('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ярлик_значення_0a38607b.values():assert 별칭 in довідка_значення,(별칭,довідка_значення)
                    перевіряти(ярлик_значення_0a38607b['help']+' system','Network / system')
                    перевіряти('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    перевіряти(ярлик_значення_0a38607b['ipconfig'],'inet 10.0.2.15');перевіряти('ip addr show','sl0: UP');перевіряти('ifconfig','sl0: UP')
                    for недійсний_Настройки in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ПОМИЛКА=перевіряти('ipconfig set '+недійсний_Настройки+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ПОМИЛКА,ПОМИЛКА
                        перевіряти('ipconfig','inet 10.0.2.15')
                    перевіряти('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    перевіряти(ярлик_значення_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    перевіряти('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    перевіряти('ip link set dev sl0 down','sl0: DOWN');перевіряти('ping -c 1 10.0.2.2; echo STATUS=$?','ПОМИЛКА -100','STATUS=1')
                    перевіряти('ipconfig up','sl0: UP')
                    перевіряти(ярлик_значення_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    перевіряти('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    перевіряти('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');перевіряти(ярлик_значення_0a38607b['route'],'10.0.2.2 sl0')
                    перевіряти('ftpd start','FTP listening')
                    перевіряти(ярлик_значення_0a38607b['netstat'],'10.0.2.20:21','LISTEN');перевіряти('ss','LISTEN')
                    перевіряти('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ПОМИЛКА -16')
                    with ftplib.FTP() as клієнт_значення:
                        клієнт_значення.connect('127.0.0.2',номер_порту,timeout=20);клієнт_значення.login();дані=b'Network address was changed in the guest.\n'
                        клієнт_значення.storbinary('STOR net-state.txt',io.BytesIO(дані));받은자료=bytearray();клієнт_значення.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==дані;клієнт_значення.delete('net-state.txt')
                    перевіряти('ftpd stop','FTP stopped');перевіряти('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    звіт_значення['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',текст);assert 찾음,текст;return tuple(map(int,찾음.groups()))
                    전=저장값(перевіряти('df','RAM only'));перевіряти('echo disk-proof > sys-state.txt');후=저장값(перевіряти(ярлик_значення_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    перевіряти('rm sys-state.txt');assert 저장값(оболонка('df'))==전
                    Пам_ять_значення=перевіряти(ярлик_значення_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Пам_ять_значення).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    перевіряти(ярлик_значення_0a38607b['ps'],'kernel/shell');перевіряти(ярлик_значення_0a38607b['uptime'],'seconds')
                    стан_відомості=перевіряти(ярлик_значення_0a38607b['top']+' -n 2','kernel/shell');assert стан_відомості.count('PID SLOT STATE')==2,стан_відомості
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    перевіряти('terminal','TERMINAL READY');запустити=len(журнал_запис);надсилати(b'vi process.txt\n');отримувати(b'NORMAL',запустити)
                    запустити=len(журнал_запис);надсилати(bytes([30,2,1,0,0,0,0]));отримувати(b'jkoros-native> ',запустити)
                    запис_список=перевіряти('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',запис_список);assert 찾음 and int(찾음.group(2))>0,запис_список
                    перевіряти('free','EL0 mapped KiB: '+찾음.group(2))
                    запустити=len(журнал_запис);надсилати(b'top\n');отримувати(b'PID SLOT STATE',запустити);надсилати(b'q');отримувати(b'jkoros-native> ',запустити)
                    # Test a multibyte prefix through the real shell completion path.
                    if ярлик_значення_0a38607b['df']!='df':
                        запустити=len(журнал_запис);надсилати((ярлик_значення_0a38607b['df'][:-1]+'\t\n').encode());отримувати(b'RAM only',запустити);отримувати(b'jkoros-native> ',запустити)
                    звіт_значення['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as керування_значення:
                    керування_значення.settimeout(15);керування_значення.connect(str(керування_шлях));потік_значення=керування_значення.makefile('rwb');json.loads(потік_значення.readline());потік_значення.write(b'{"execute":"qmp_capabilities"}\n');потік_значення.flush()
                    while 'return' not in json.loads(потік_значення.readline()):pass
                    надсилати((('poweroff' if аргументи.poweroff_only else ярлик_значення_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Подія=json.loads(потік_значення.readline())
                        if Подія.get('event')=='SHUTDOWN':break
                    assert Подія['data']['guest'] and Подія['data']['reason']=='guest-shutdown',Подія
                    assert процес_значення.wait(timeout=15)==0
                    звіт_значення['shutdown']=Подія;звіт_значення['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                звіт_значення['network_trace']=міст_значення.журнал_трасування
                assert аргументи.poweroff_only or any(запис_значення_962f286b['protocol']==1 and запис_значення_962f286b['direction']=='from_guest' for запис_значення_962f286b in міст_значення.журнал_трасування)
                звіт_значення['passed']=True
            finally:
                if процес_значення.poll() is None:os.killpg(процес_значення.pid,signal.SIGTERM)
                try:процес_значення.wait(timeout=10)
                except subprocess.TimeoutExpired:процес_значення.kill();процес_значення.wait()
                вибирати_елемент.close();(Вивід/'serial.log').write_bytes(журнал_запис);(Вивід/'report.json').write_text(json.dumps(звіт_значення,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ключ_значення:значення for Ключ_значення,значення in звіт_значення.items() if Ключ_значення!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':запустити()
