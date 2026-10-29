#!/usr/bin/env python3
"""действителен_данни 자체 커널의 IP/ICMP, Състояние_стойност заявка_стойност, 현지어 Команда, 게스트 Изход_програма проверка."""
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


def Стартиране():
    анализатор_48ee4b1b=argparse.ArgumentParser();анализатор_48ee4b1b.add_argument('--edition',type=Path);анализатор_48ee4b1b.add_argument('--output',type=Path);анализатор_48ee4b1b.add_argument('--poweroff-only',action='store_true');Параметри=анализатор_48ee4b1b.parse_args()
    проект_корен=Path(__file__).resolve().parents[1];Настройки={};препратка_към_клетка_таблица={}
    if Параметри.edition:
        кънтри_стойност=Параметри.edition.resolve();Настройки=json.loads((кънтри_стойност/'native.json').read_text());препратка_към_клетка_таблица=Настройки['identifiers'];проект_корен=кънтри_стойност/Настройки['source']/Настройки['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(кънтри_стойност/'native-edition.py'),'check'])
        хост=кънтри_стойност/'host/qemu'
        if хост.is_file():os.environ['QEMU_AARCH64']=str(хост)
    Инструменти=проект_корен/Path(Настройки.get('runner','Инструменти/изпълнявам_команда.py')).parent
    sys.path.insert(0,str(Инструменти))
    def Четене(Име):
        ПЪТ=Инструменти/(препратка_към_клетка_таблица.get(Име,Име)+'.py');случай_стойност=importlib.util.spec_from_file_location('test_'+Име,str(ПЪТ));модул_стойност=importlib.util.module_from_spec(случай_стойност);случай_стойност.loader.exec_module(модул_стойност);return модул_стойност
    실행모듈=Четене('изпълнявам_команда');мрежа_модул=Четене('мост_3de4fe3a');Команда=getattr(실행모듈,препратка_към_клетка_таблица.get('Команда','Команда'));мост_Тип=getattr(мрежа_модул,препратка_към_клетка_таблица.get('мост_3de4fe3a','мост_3de4fe3a'))
    пряк_път_стойност_0a38607b=Настройки.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адрес','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'показвам_помощ'})
    sys.path.insert(0,str(проект_корен/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(проект_корен);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Изход=Параметри.output or проект_корен/'build/verification/system-tools';Изход.mkdir(parents=True,exist_ok=True)
    отчет_стойност={'passed':False,'country':Настройки.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    регистрирам_запис=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        контрол_път=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as търся_стойност:търся_стойност.bind(('127.0.0.1',0));номер_на_порт=търся_стойност.getsockname()[1]
            if not 50000<=номер_на_порт<=50007:break
        with мост_Тип(номер_на_порт,заснемам=True,гост_адрес=ipTestText('10.0.2.20'),хост_адрес='127.0.0.2') as мост_стойност:
            Процес_стойност=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(контрол_път)]+мост_стойност.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            избирам_артикул=selectors.DefaultSelector();избирам_артикул.register(Процес_стойност.stdout,selectors.EVENT_READ)
            def получавам(показвам_стойност,Стартиране=0,제한=45):
                끝=time.monotonic()+제한
                while показвам_стойност not in регистрирам_запис[Стартиране:]:
                    if time.monotonic()>끝 or Процес_стойност.poll() is not None:raise AssertionError('Missing '+repr(показвам_стойност)+'\n'+регистрирам_запис[Стартиране:].decode('utf-8','replace'))
                    for Ключ_стойност,_ in избирам_артикул.select(.1):
                        данни=Ключ_стойност.fileobj.read(65536)
                        if данни:регистрирам_запис.extend(данни)
                return регистрирам_запис[Стартиране:].decode('utf-8','replace').replace('\r\n','\n')
            def изпращам(данни):Процес_стойност.stdin.write(данни);Процес_стойност.stdin.flush()
            def обвивка(Текст):
                Текст=ipTestText(Текст)
                print(отчет_стойност['country'],Текст,flush=True);차례[0]+=1;показвам_стойност='__SYSTEM_DONE_'+str(차례[0])+'__';Стартиране=len(регистрирам_запис)
                изпращам((Текст+'; echo; echo '+показвам_стойност+'\n').encode())
                прекратяване_на_повикването_маркер=('\r\n'+показвам_стойност+'\r\n').encode();получавам(прекратяване_на_повикването_маркер,Стартиране)
                прекратяване_на_повикването_позиция=регистрирам_запис.index(прекратяване_на_повикването_маркер,Стартиране)+len(прекратяване_на_повикването_маркер)
                получавам(b'jkoros-native> ',прекратяване_на_повикването_позиция)
                return регистрирам_запис[Стартиране:].decode('utf-8','replace').replace('\r\n','\n')
            def проверявам(Текст,*값들):
                отговор=обвивка(Текст)
                for стойност in 값들:assert ipTestText(стойност) in отговор,(Текст,стойност,отговор)
                return отговор
            try:
                получавам(b'jkoros-native> ')
                if not Параметри.poweroff_only:
                    помощ_стойност=проверявам('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in пряк_път_стойност_0a38607b.values():assert 별칭 in помощ_стойност,(별칭,помощ_стойност)
                    проверявам(пряк_път_стойност_0a38607b['help']+' system','Network / system')
                    проверявам('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    проверявам(пряк_път_стойност_0a38607b['ipconfig'],'inet 10.0.2.15');проверявам('ip addr show','sl0: UP');проверявам('ifconfig','sl0: UP')
                    for невалиден_Настройки in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ГРЕШКА=проверявам('ipconfig set '+невалиден_Настройки+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ГРЕШКА,ГРЕШКА
                        проверявам('ipconfig','inet 10.0.2.15')
                    проверявам('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    проверявам(пряк_път_стойност_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    проверявам('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    проверявам('ip link set dev sl0 down','sl0: DOWN');проверявам('ping -c 1 10.0.2.2; echo STATUS=$?','ГРЕШКА -100','STATUS=1')
                    проверявам('ipconfig up','sl0: UP')
                    проверявам(пряк_път_стойност_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    проверявам('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    проверявам('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');проверявам(пряк_път_стойност_0a38607b['route'],'10.0.2.2 sl0')
                    проверявам('ftpd start','FTP listening')
                    проверявам(пряк_път_стойност_0a38607b['netstat'],'10.0.2.20:21','LISTEN');проверявам('ss','LISTEN')
                    проверявам('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ГРЕШКА -16')
                    with ftplib.FTP() as клиент_стойност:
                        клиент_стойност.connect('127.0.0.2',номер_на_порт,timeout=20);клиент_стойност.login();данни=b'Network address was changed in the guest.\n'
                        клиент_стойност.storbinary('STOR net-state.txt',io.BytesIO(данни));받은자료=bytearray();клиент_стойност.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==данни;клиент_стойност.delete('net-state.txt')
                    проверявам('ftpd stop','FTP stopped');проверявам('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    отчет_стойност['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Текст);assert 찾음,Текст;return tuple(map(int,찾음.groups()))
                    전=저장값(проверявам('df','RAM only'));проверявам('echo disk-proof > sys-state.txt');후=저장값(проверявам(пряк_път_стойност_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    проверявам('rm sys-state.txt');assert 저장값(обвивка('df'))==전
                    Памет_стойност=проверявам(пряк_път_стойност_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Памет_стойност).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    проверявам(пряк_път_стойност_0a38607b['ps'],'kernel/shell');проверявам(пряк_път_стойност_0a38607b['uptime'],'seconds')
                    статус_инфо=проверявам(пряк_път_стойност_0a38607b['top']+' -n 2','kernel/shell');assert статус_инфо.count('PID SLOT STATE')==2,статус_инфо
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    проверявам('terminal','TERMINAL READY');Стартиране=len(регистрирам_запис);изпращам(b'vi process.txt\n');получавам(b'NORMAL',Стартиране)
                    Стартиране=len(регистрирам_запис);изпращам(bytes([30,2,1,0,0,0,0]));получавам(b'jkoros-native> ',Стартиране)
                    запис_Списък=проверявам('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',запис_Списък);assert 찾음 and int(찾음.group(2))>0,запис_Списък
                    проверявам('free','EL0 mapped KiB: '+찾음.group(2))
                    Стартиране=len(регистрирам_запис);изпращам(b'top\n');получавам(b'PID SLOT STATE',Стартиране);изпращам(b'q');получавам(b'jkoros-native> ',Стартиране)
                    # Test a multibyte prefix through the real shell completion path.
                    if пряк_път_стойност_0a38607b['df']!='df':
                        Стартиране=len(регистрирам_запис);изпращам((пряк_път_стойност_0a38607b['df'][:-1]+'\t\n').encode());получавам(b'RAM only',Стартиране);получавам(b'jkoros-native> ',Стартиране)
                    отчет_стойност['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as контрол_стойност:
                    контрол_стойност.settimeout(15);контрол_стойност.connect(str(контрол_път));поток_стойност=контрол_стойност.makefile('rwb');json.loads(поток_стойност.readline());поток_стойност.write(b'{"execute":"qmp_capabilities"}\n');поток_стойност.flush()
                    while 'return' not in json.loads(поток_стойност.readline()):pass
                    изпращам((('poweroff' if Параметри.poweroff_only else пряк_път_стойност_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Събитие=json.loads(поток_стойност.readline())
                        if Събитие.get('event')=='SHUTDOWN':break
                    assert Събитие['data']['guest'] and Събитие['data']['reason']=='guest-shutdown',Събитие
                    assert Процес_стойност.wait(timeout=15)==0
                    отчет_стойност['shutdown']=Събитие;отчет_стойност['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                отчет_стойност['network_trace']=мост_стойност.регистрационен_файл_за_проследяванията
                assert Параметри.poweroff_only or any(запис_стойност['protocol']==1 and запис_стойност['direction']=='from_guest' for запис_стойност in мост_стойност.регистрационен_файл_за_проследяванията)
                отчет_стойност['passed']=True
            finally:
                if Процес_стойност.poll() is None:os.killpg(Процес_стойност.pid,signal.SIGTERM)
                try:Процес_стойност.wait(timeout=10)
                except subprocess.TimeoutExpired:Процес_стойност.kill();Процес_стойност.wait()
                избирам_артикул.close();(Изход/'serial.log').write_bytes(регистрирам_запис);(Изход/'report.json').write_text(json.dumps(отчет_стойност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ключ_стойност:стойност for Ключ_стойност,стойност in отчет_стойност.items() if Ключ_стойност!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Стартиране()
