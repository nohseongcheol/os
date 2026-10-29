#!/usr/bin/env python3
"""фактический_данные свой 커널의 IP/ICMP, Состояние_ЗНАЧЕН запрос_ЗНАЧЕН, 현지어 команда, 게스트 Выход_программа проверить."""
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


def запустить():
    анализатор_48ee4b1b=argparse.ArgumentParser();анализатор_48ee4b1b.add_argument('--edition',type=Path);анализатор_48ee4b1b.add_argument('--output',type=Path);анализатор_48ee4b1b.add_argument('--poweroff-only',action='store_true');аргументы=анализатор_48ee4b1b.parse_args()
    задача_корень=Path(__file__).resolve().parents[1];Настройки={};имя_таблица={}
    if аргументы.edition:
        кантри_ЗНАЧЕН=аргументы.edition.resolve();Настройки=json.loads((кантри_ЗНАЧЕН/'native.json').read_text());имя_таблица=Настройки['identifiers'];задача_корень=кантри_ЗНАЧЕН/Настройки['source']/Настройки['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(кантри_ЗНАЧЕН/'native-edition.py'),'check'])
        узел=кантри_ЗНАЧЕН/'host/qemu'
        if узел.is_file():os.environ['QEMU_AARCH64']=str(узел)
    инструменты=задача_корень/Path(Настройки.get('runner','инструменты/실행.py')).parent
    sys.path.insert(0,str(инструменты))
    def Чтение(Название):
        путь=инструменты/(имя_таблица.get(Название,Название)+'.py');сумма_контракта=importlib.util.spec_from_file_location('test_'+Название,str(путь));модуль_ЗНАЧЕН=importlib.util.module_from_spec(сумма_контракта);сумма_контракта.loader.exec_module(модуль_ЗНАЧЕН);return модуль_ЗНАЧЕН
    выполнение_модуль=Чтение('실행');сеть_модуль=Чтение('мост_3de4fe3a');команда=getattr(выполнение_модуль,имя_таблица.get('команда','команда'));мост_ТИП=getattr(сеть_модуль,имя_таблица.get('мост_3de4fe3a','мост_3de4fe3a'))
    ярлык_ЗНАЧЕН_0a38607b=Настройки.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адрес','ping':'тест_ответ','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'показать_справку'})
    sys.path.insert(0,str(задача_корень/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(задача_корень);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    текстовыйВывод=аргументы.output or задача_корень/'build/verification/system-tools';текстовыйВывод.mkdir(parents=True,exist_ok=True)
    Отчет_ЗНАЧЕН={'passed':False,'country':Настройки.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_ЗАПИСЬ=bytearray();ПОСЛЕД_ЗНАЧЕН=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        управление_путь=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ПОИСК_ЗНАЧЕН:ПОИСК_ЗНАЧЕН.bind(('127.0.0.1',0));номер_порта=ПОИСК_ЗНАЧЕН.getsockname()[1]
            if not 50000<=номер_порта<=50007:break
        with мост_ТИП(номер_порта,Сбор=True,гость_АДРЕС=ipTestText('10.0.2.20'),адрес_узла='127.0.0.2') as мост_ЗНАЧЕН:
            Процесс_ЗНАЧЕН=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(управление_путь)]+мост_ЗНАЧЕН.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ВЫБОР_товар=selectors.DefaultSelector();ВЫБОР_товар.register(Процесс_ЗНАЧЕН.stdout,selectors.EVENT_READ)
            def получить(выпуск_ЗНАЧЕН,запустить=0,제한=45):
                끝=time.monotonic()+제한
                while выпуск_ЗНАЧЕН not in LOG_ЗАПИСЬ[запустить:]:
                    if time.monotonic()>끝 or Процесс_ЗНАЧЕН.poll() is not None:raise AssertionError('Missing '+repr(выпуск_ЗНАЧЕН)+'\n'+LOG_ЗАПИСЬ[запустить:].decode('utf-8','replace'))
                    for Ключ_ЗНАЧЕН,_ in ВЫБОР_товар.select(.1):
                        данные=Ключ_ЗНАЧЕН.fileobj.read(65536)
                        if данные:LOG_ЗАПИСЬ.extend(данные)
                return LOG_ЗАПИСЬ[запустить:].decode('utf-8','replace').replace('\r\n','\n')
            def написать(данные):Процесс_ЗНАЧЕН.stdin.write(данные);Процесс_ЗНАЧЕН.stdin.flush()
            def оболочка(текст):
                текст=ipTestText(текст)
                print(Отчет_ЗНАЧЕН['country'],текст,flush=True);ПОСЛЕД_ЗНАЧЕН[0]+=1;выпуск_ЗНАЧЕН='__SYSTEM_DONE_'+str(ПОСЛЕД_ЗНАЧЕН[0])+'__';запустить=len(LOG_ЗАПИСЬ)
                написать((текст+'; echo; echo '+выпуск_ЗНАЧЕН+'\n').encode())
                элемент_метка=('\r\n'+выпуск_ЗНАЧЕН+'\r\n').encode();получить(элемент_метка,запустить)
                элемент_позиция=LOG_ЗАПИСЬ.index(элемент_метка,запустить)+len(элемент_метка)
                получить(b'jkoros-native> ',элемент_позиция)
                return LOG_ЗАПИСЬ[запустить:].decode('utf-8','replace').replace('\r\n','\n')
            def проверять(текст,*값들):
                ответ=оболочка(текст)
                for ЗНАЧЕН in 값들:assert ipTestText(ЗНАЧЕН) in ответ,(текст,ЗНАЧЕН,ответ)
                return ответ
            try:
                получить(b'jkoros-native> ')
                if not аргументы.poweroff_only:
                    справка_ЗНАЧЕН=проверять('help system','ipconfig','ping','ps','top','df','poweroff')
                    for слово_для_замены_имя in ярлык_ЗНАЧЕН_0a38607b.values():assert слово_для_замены_имя in справка_ЗНАЧЕН,(слово_для_замены_имя,справка_ЗНАЧЕН)
                    проверять(ярлык_ЗНАЧЕН_0a38607b['help']+' system','Network / system')
                    проверять('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    проверять(ярлык_ЗНАЧЕН_0a38607b['ipconfig'],'inet 10.0.2.15');проверять('ip addr show','sl0: UP');проверять('ifconfig','sl0: UP')
                    for неверный_Настройки in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ошибка=проверять('ipconfig set '+неверный_Настройки+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ошибка,ошибка
                        проверять('ipconfig','inet 10.0.2.15')
                    проверять('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    проверять(ярлык_ЗНАЧЕН_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    проверять('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    проверять('ip link set dev sl0 down','sl0: DOWN');проверять('ping -c 1 10.0.2.2; echo STATUS=$?','ошибка -100','STATUS=1')
                    проверять('ipconfig up','sl0: UP')
                    проверять(ярлык_ЗНАЧЕН_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    проверять('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    проверять('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');проверять(ярлык_ЗНАЧЕН_0a38607b['route'],'10.0.2.2 sl0')
                    проверять('ftpd start','FTP listening')
                    проверять(ярлык_ЗНАЧЕН_0a38607b['netstat'],'10.0.2.20:21','LISTEN');проверять('ss','LISTEN')
                    проверять('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ошибка -16')
                    with ftplib.FTP() as клиент_ЗНАЧЕН:
                        клиент_ЗНАЧЕН.connect('127.0.0.2',номер_порта,timeout=20);клиент_ЗНАЧЕН.login();данные=b'Network address was changed in the guest.\n'
                        клиент_ЗНАЧЕН.storbinary('STOR net-state.txt',io.BytesIO(данные));ПОЛУЧЕНО_данные=bytearray();клиент_ЗНАЧЕН.retrbinary('RETR net-state.txt',ПОЛУЧЕНО_данные.extend);assert ПОЛУЧЕНО_данные==данные;клиент_ЗНАЧЕН.delete('net-state.txt')
                    проверять('ftpd stop','FTP stopped');проверять('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Отчет_ЗНАЧЕН['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',текст);assert 찾음,текст;return tuple(map(int,찾음.groups()))
                    전=저장값(проверять('df','RAM only'));проверять('echo disk-proof > sys-state.txt');후=저장값(проверять(ярлык_ЗНАЧЕН_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    проверять('rm sys-state.txt');assert 저장값(оболочка('df'))==전
                    Память_ЗНАЧЕН=проверять(ярлык_ЗНАЧЕН_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');количество_ЗНАЧЕН=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Память_ЗНАЧЕН).groups()));assert 0<количество_ЗНАЧЕН[1]<=количество_ЗНАЧЕН[0] and количество_ЗНАЧЕН[1]+количество_ЗНАЧЕН[2]==количество_ЗНАЧЕН[0]
                    проверять(ярлык_ЗНАЧЕН_0a38607b['ps'],'kernel/shell');проверять(ярлык_ЗНАЧЕН_0a38607b['uptime'],'seconds')
                    статус_сведения=проверять(ярлык_ЗНАЧЕН_0a38607b['top']+' -n 2','kernel/shell');assert статус_сведения.count('PID SLOT STATE')==2,статус_сведения
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    проверять('terminal','TERMINAL READY');запустить=len(LOG_ЗАПИСЬ);написать(b'vi process.txt\n');получить(b'NORMAL',запустить)
                    запустить=len(LOG_ЗАПИСЬ);написать(bytes([30,2,1,0,0,0,0]));получить(b'jkoros-native> ',запустить)
                    ввод_Список=проверять('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ввод_Список);assert 찾음 and int(찾음.group(2))>0,ввод_Список
                    проверять('free','EL0 mapped KiB: '+찾음.group(2))
                    запустить=len(LOG_ЗАПИСЬ);написать(b'top\n');получить(b'PID SLOT STATE',запустить);написать(b'q');получить(b'jkoros-native> ',запустить)
                    # Test a multibyte prefix through the real shell completion path.
                    if ярлык_ЗНАЧЕН_0a38607b['df']!='df':
                        запустить=len(LOG_ЗАПИСЬ);написать((ярлык_ЗНАЧЕН_0a38607b['df'][:-1]+'\t\n').encode());получить(b'RAM only',запустить);получить(b'jkoros-native> ',запустить)
                    Отчет_ЗНАЧЕН['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as управление_ЗНАЧЕН:
                    управление_ЗНАЧЕН.settimeout(15);управление_ЗНАЧЕН.connect(str(управление_путь));поток_ЗНАЧЕН=управление_ЗНАЧЕН.makefile('rwb');json.loads(поток_ЗНАЧЕН.readline());поток_ЗНАЧЕН.write(b'{"execute":"qmp_capabilities"}\n');поток_ЗНАЧЕН.flush()
                    while 'return' not in json.loads(поток_ЗНАЧЕН.readline()):pass
                    написать((('poweroff' if аргументы.poweroff_only else ярлык_ЗНАЧЕН_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Событие=json.loads(поток_ЗНАЧЕН.readline())
                        if Событие.get('event')=='SHUTDOWN':break
                    assert Событие['data']['guest'] and Событие['data']['reason']=='guest-shutdown',Событие
                    assert Процесс_ЗНАЧЕН.wait(timeout=15)==0
                    Отчет_ЗНАЧЕН['shutdown']=Событие;Отчет_ЗНАЧЕН['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Отчет_ЗНАЧЕН['network_trace']=мост_ЗНАЧЕН.журнал_трассировки
                assert аргументы.poweroff_only or any(ввод_ЗНАЧЕН['protocol']==1 and ввод_ЗНАЧЕН['direction']=='from_guest' for ввод_ЗНАЧЕН in мост_ЗНАЧЕН.журнал_трассировки)
                Отчет_ЗНАЧЕН['passed']=True
            finally:
                if Процесс_ЗНАЧЕН.poll() is None:os.killpg(Процесс_ЗНАЧЕН.pid,signal.SIGTERM)
                try:Процесс_ЗНАЧЕН.wait(timeout=10)
                except subprocess.TimeoutExpired:Процесс_ЗНАЧЕН.kill();Процесс_ЗНАЧЕН.wait()
                ВЫБОР_товар.close();(текстовыйВывод/'serial.log').write_bytes(LOG_ЗАПИСЬ);(текстовыйВывод/'report.json').write_text(json.dumps(Отчет_ЗНАЧЕН,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ключ_ЗНАЧЕН:ЗНАЧЕН for Ключ_ЗНАЧЕН,ЗНАЧЕН in Отчет_ЗНАЧЕН.items() if Ключ_ЗНАЧЕН!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':запустить()
