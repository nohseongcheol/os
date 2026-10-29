#!/usr/bin/env python3
"""нақты_деректер 자체 커널의 IP/ICMP, күй_мән сұрау_мән, 현지어 Команда, 게스트 Шығу_бағдарлама тексеру_5fb2b747."""
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


def Орындау_2():
    талдау_құралы_48ee4b1b=argparse.ArgumentParser();талдау_құралы_48ee4b1b.add_argument('--edition',type=Path);талдау_құралы_48ee4b1b.add_argument('--output',type=Path);талдау_құралы_48ee4b1b.add_argument('--poweroff-only',action='store_true');Аргументтер=талдау_құралы_48ee4b1b.parse_args()
    жоба_түбір=Path(__file__).resolve().parents[1];Баптаулар={};аты_кесте={}
    if Аргументтер.edition:
        나라=Аргументтер.edition.resolve();Баптаулар=json.loads((나라/'native.json').read_text());аты_кесте=Баптаулар['identifiers'];жоба_түбір=나라/Баптаулар['source']/Баптаулар['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        орналастыру=나라/'host/qemu'
        if орналастыру.is_file():os.environ['QEMU_AARCH64']=str(орналастыру)
    Құралдар=жоба_түбір/Path(Баптаулар.get('runner','Құралдар/орындау_пәрмен.py')).parent
    sys.path.insert(0,str(Құралдар))
    def Оқу(Аты):
        Жол_2=Құралдар/(аты_кесте.get(Аты,Аты)+'.py');іс_мән=importlib.util.spec_from_file_location('test_'+Аты,str(Жол_2));модуль_мән=importlib.util.module_from_spec(іс_мән);іс_мән.loader.exec_module(модуль_мән);return модуль_мән
    실행모듈=Оқу('орындау_пәрмен');желі_модуль=Оқу('желі_көпір');Команда=getattr(실행모듈,аты_кесте.get('Команда','Команда'));көпір_Түрі=getattr(желі_модуль,аты_кесте.get('желі_көпір','желі_көпір'))
    таңбаша_мән_0a38607b=Баптаулар.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_мекенжайы','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'көрсету_анықтама'})
    sys.path.insert(0,str(жоба_түбір/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(жоба_түбір);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Шығысы=Аргументтер.output or жоба_түбір/'build/verification/system-tools';Шығысы.mkdir(parents=True,exist_ok=True)
    есеп_мән={'passed':False,'country':Баптаулар.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    журнал_жол=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        Басқару_жол=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Іздеу_мән:Іздеу_мән.bind(('127.0.0.1',0));порт_нөмірі=Іздеу_мән.getsockname()[1]
            if not 50000<=порт_нөмірі<=50007:break
        with көпір_Түрі(порт_нөмірі,түсіру=True,қонақ_мекенжай=ipTestText('10.0.2.20'),орналастыру_мекенжай='127.0.0.2') as көпір_мән:
            Процесс_мән=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(Басқару_жол)]+көпір_мән.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            таңдау_элемент=selectors.DefaultSelector();таңдау_элемент.register(Процесс_мән.stdout,selectors.EVENT_READ)
            def 받기(көрсету_мән,Орындау_2=0,제한=45):
                끝=time.monotonic()+제한
                while көрсету_мән not in журнал_жол[Орындау_2:]:
                    if time.monotonic()>끝 or Процесс_мән.poll() is not None:raise AssertionError('Missing '+repr(көрсету_мән)+'\n'+журнал_жол[Орындау_2:].decode('utf-8','replace'))
                    for Кілт_мән,_ in таңдау_элемент.select(.1):
                        деректер=Кілт_мән.fileobj.read(65536)
                        if деректер:журнал_жол.extend(деректер)
                return журнал_жол[Орындау_2:].decode('utf-8','replace').replace('\r\n','\n')
            def жіберу(деректер):Процесс_мән.stdin.write(деректер);Процесс_мән.stdin.flush()
            def қоршам(Мәтін):
                Мәтін=ipTestText(Мәтін)
                print(есеп_мән['country'],Мәтін,flush=True);차례[0]+=1;көрсету_мән='__SYSTEM_DONE_'+str(차례[0])+'__';Орындау_2=len(журнал_жол)
                жіберу((Мәтін+'; echo; echo '+көрсету_мән+'\n').encode())
                끝표시=('\r\n'+көрсету_мән+'\r\n').encode();받기(끝표시,Орындау_2)
                тоқтату_лауазым=журнал_жол.index(끝표시,Орындау_2)+len(끝표시)
                받기(b'jkoros-native> ',тоқтату_лауазым)
                return журнал_жол[Орындау_2:].decode('utf-8','replace').replace('\r\n','\n')
            def тексеру(Мәтін,*값들):
                жауап=қоршам(Мәтін)
                for мән in 값들:assert ipTestText(мән) in жауап,(Мәтін,мән,жауап)
                return жауап
            try:
                받기(b'jkoros-native> ')
                if not Аргументтер.poweroff_only:
                    анықтама_мән=тексеру('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in таңбаша_мән_0a38607b.values():assert 별칭 in анықтама_мән,(별칭,анықтама_мән)
                    тексеру(таңбаша_мән_0a38607b['help']+' system','Network / system')
                    тексеру('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    тексеру(таңбаша_мән_0a38607b['ipconfig'],'inet 10.0.2.15');тексеру('ip addr show','sl0: UP');тексеру('ifconfig','sl0: UP')
                    for дұрыс_емес_Параметрлер in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Қате=тексеру('ipconfig set '+дұрыс_емес_Параметрлер+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Қате,Қате
                        тексеру('ipconfig','inet 10.0.2.15')
                    тексеру('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    тексеру(таңбаша_мән_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тексеру('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    тексеру('ip link set dev sl0 down','sl0: DOWN');тексеру('ping -c 1 10.0.2.2; echo STATUS=$?','Қате -100','STATUS=1')
                    тексеру('ipconfig up','sl0: UP')
                    тексеру(таңбаша_мән_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    тексеру('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тексеру('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');тексеру(таңбаша_мән_0a38607b['route'],'10.0.2.2 sl0')
                    тексеру('ftpd start','FTP listening')
                    тексеру(таңбаша_мән_0a38607b['netstat'],'10.0.2.20:21','LISTEN');тексеру('ss','LISTEN')
                    тексеру('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Қате -16')
                    with ftplib.FTP() as клиент_мән:
                        клиент_мән.connect('127.0.0.2',порт_нөмірі,timeout=20);клиент_мән.login();деректер=b'Network address was changed in the guest.\n'
                        клиент_мән.storbinary('STOR net-state.txt',io.BytesIO(деректер));받은자료=bytearray();клиент_мән.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==деректер;клиент_мән.delete('net-state.txt')
                    тексеру('ftpd stop','FTP stopped');тексеру('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    есеп_мән['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Мәтін):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Мәтін);assert 찾음,Мәтін;return tuple(map(int,찾음.groups()))
                    전=저장값(тексеру('df','RAM only'));тексеру('echo disk-proof > sys-state.txt');후=저장값(тексеру(таңбаша_мән_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    тексеру('rm sys-state.txt');assert 저장값(қоршам('df'))==전
                    Жад_мән=тексеру(таңбаша_мән_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Жад_мән).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    тексеру(таңбаша_мән_0a38607b['ps'],'kernel/shell');тексеру(таңбаша_мән_0a38607b['uptime'],'seconds')
                    күй_ақпарат=тексеру(таңбаша_мән_0a38607b['top']+' -n 2','kernel/shell');assert күй_ақпарат.count('PID SLOT STATE')==2,күй_ақпарат
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    тексеру('terminal','TERMINAL READY');Орындау_2=len(журнал_жол);жіберу(b'vi process.txt\n');받기(b'NORMAL',Орындау_2)
                    Орындау_2=len(журнал_жол);жіберу(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Орындау_2)
                    енгізу_Тізім=тексеру('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',енгізу_Тізім);assert 찾음 and int(찾음.group(2))>0,енгізу_Тізім
                    тексеру('free','EL0 mapped KiB: '+찾음.group(2))
                    Орындау_2=len(журнал_жол);жіберу(b'top\n');받기(b'PID SLOT STATE',Орындау_2);жіберу(b'q');받기(b'jkoros-native> ',Орындау_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if таңбаша_мән_0a38607b['df']!='df':
                        Орындау_2=len(журнал_жол);жіберу((таңбаша_мән_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Орындау_2);받기(b'jkoros-native> ',Орындау_2)
                    есеп_мән['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as Басқару_мән:
                    Басқару_мән.settimeout(15);Басқару_мән.connect(str(Басқару_жол));ағым_мән=Басқару_мән.makefile('rwb');json.loads(ағым_мән.readline());ағым_мән.write(b'{"execute":"qmp_capabilities"}\n');ағым_мән.flush()
                    while 'return' not in json.loads(ағым_мән.readline()):pass
                    жіберу((('poweroff' if Аргументтер.poweroff_only else таңбаша_мән_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Оқиға=json.loads(ағым_мән.readline())
                        if Оқиға.get('event')=='SHUTDOWN':break
                    assert Оқиға['data']['guest'] and Оқиға['data']['reason']=='guest-shutdown',Оқиға
                    assert Процесс_мән.wait(timeout=15)==0
                    есеп_мән['shutdown']=Оқиға;есеп_мән['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                есеп_мән['network_trace']=көпір_мән.трассалау_журналы
                assert Аргументтер.poweroff_only or any(енгізу_мән['protocol']==1 and енгізу_мән['direction']=='from_guest' for енгізу_мән in көпір_мән.трассалау_журналы)
                есеп_мән['passed']=True
            finally:
                if Процесс_мән.poll() is None:os.killpg(Процесс_мән.pid,signal.SIGTERM)
                try:Процесс_мән.wait(timeout=10)
                except subprocess.TimeoutExpired:Процесс_мән.kill();Процесс_мән.wait()
                таңдау_элемент.close();(Шығысы/'serial.log').write_bytes(журнал_жол);(Шығысы/'report.json').write_text(json.dumps(есеп_мән,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Кілт_мән:мән for Кілт_мән,мән in есеп_мән.items() if Кілт_мән!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Орындау_2()
