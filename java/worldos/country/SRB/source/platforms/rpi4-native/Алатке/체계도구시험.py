#!/usr/bin/env python3
"""стваран_подаци 자체 커널의 IP/ICMP, стање_вриједност упит_вриједност, 현지어 Наредба, 게스트 Излаз_програм потврдити_5fb2b747."""
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


def Покрени():
    анализатор_48ee4b1b=argparse.ArgumentParser();анализатор_48ee4b1b.add_argument('--edition',type=Path);анализатор_48ee4b1b.add_argument('--output',type=Path);анализатор_48ee4b1b.add_argument('--poweroff-only',action='store_true');Аргументи=анализатор_48ee4b1b.parse_args()
    пројектовати_корен=Path(__file__).resolve().parents[1];Поставке={};име_табела={}
    if Аргументи.edition:
        나라=Аргументи.edition.resolve();Поставке=json.loads((나라/'native.json').read_text());име_табела=Поставке['identifiers'];пројектовати_корен=나라/Поставке['source']/Поставке['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        хост=나라/'host/qemu'
        if хост.is_file():os.environ['QEMU_AARCH64']=str(хост)
    Алатке=пројектовати_корен/Path(Поставке.get('runner','Алатке/Изврши_команда.py')).parent
    sys.path.insert(0,str(Алатке))
    def Чита(Назив):
        ПУТАЊА=Алатке/(име_табела.get(Назив,Назив)+'.py');случај_вриједност=importlib.util.spec_from_file_location('test_'+Назив,str(ПУТАЊА));модул_вриједност=importlib.util.module_from_spec(случај_вриједност);случај_вриједност.loader.exec_module(модул_вриједност);return модул_вриједност
    실행모듈=Чита('Изврши_команда');Мрежа_модул=Чита('Мрежа_мост');Наредба=getattr(실행모듈,име_табела.get('Наредба','Наредба'));мост_тип=getattr(Мрежа_модул,име_табела.get('Мрежа_мост','Мрежа_мост'))
    пречица_вриједност_0a38607b=Поставке.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_адреса','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'емисија_помоћ'})
    sys.path.insert(0,str(пројектовати_корен/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(пројектовати_корен);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Излаз=Аргументи.output or пројектовати_корен/'build/verification/system-tools';Излаз.mkdir(parents=True,exist_ok=True)
    извештај_вриједност={'passed':False,'country':Поставке.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    евиденција_ред=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        контрола_пут=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as тражити_вриједност:тражити_вриједност.bind(('127.0.0.1',0));број_порта=тражити_вриједност.getsockname()[1]
            if not 50000<=број_порта<=50007:break
        with мост_тип(број_порта,снимити=True,гост_адреса=ipTestText('10.0.2.20'),хост_адреса='127.0.0.2') as мост_вриједност:
            Процес_вриједност=subprocess.Popen(Наредба()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(контрола_пут)]+мост_вриједност.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            изабрати_ставка=selectors.DefaultSelector();изабрати_ставка.register(Процес_вриједност.stdout,selectors.EVENT_READ)
            def 받기(емисија_вриједност,Покрени=0,제한=45):
                끝=time.monotonic()+제한
                while емисија_вриједност not in евиденција_ред[Покрени:]:
                    if time.monotonic()>끝 or Процес_вриједност.poll() is not None:raise AssertionError('Missing '+repr(емисија_вриједност)+'\n'+евиденција_ред[Покрени:].decode('utf-8','replace'))
                    for Кључ_вриједност,_ in изабрати_ставка.select(.1):
                        подаци=Кључ_вриједност.fileobj.read(65536)
                        if подаци:евиденција_ред.extend(подаци)
                return евиденција_ред[Покрени:].decode('utf-8','replace').replace('\r\n','\n')
            def послати(подаци):Процес_вриједност.stdin.write(подаци);Процес_вриједност.stdin.flush()
            def љуска(Текст):
                Текст=ipTestText(Текст)
                print(извештај_вриједност['country'],Текст,flush=True);차례[0]+=1;емисија_вриједност='__SYSTEM_DONE_'+str(차례[0])+'__';Покрени=len(евиденција_ред)
                послати((Текст+'; echo; echo '+емисија_вриједност+'\n').encode())
                끝표시=('\r\n'+емисија_вриједност+'\r\n').encode();받기(끝표시,Покрени)
                завршити_позиција=евиденција_ред.index(끝표시,Покрени)+len(끝표시)
                받기(b'jkoros-native> ',завршити_позиција)
                return евиденција_ред[Покрени:].decode('utf-8','replace').replace('\r\n','\n')
            def потврдити(Текст,*값들):
                одговор=љуска(Текст)
                for вриједност in 값들:assert ipTestText(вриједност) in одговор,(Текст,вриједност,одговор)
                return одговор
            try:
                받기(b'jkoros-native> ')
                if not Аргументи.poweroff_only:
                    помоћ_вриједност=потврдити('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in пречица_вриједност_0a38607b.values():assert 별칭 in помоћ_вриједност,(별칭,помоћ_вриједност)
                    потврдити(пречица_вриједност_0a38607b['help']+' system','Network / system')
                    потврдити('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    потврдити(пречица_вриједност_0a38607b['ipconfig'],'inet 10.0.2.15');потврдити('ip addr show','sl0: UP');потврдити('ifconfig','sl0: UP')
                    for неважеће_Поставке in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ГРЕШКА=потврдити('ipconfig set '+неважеће_Поставке+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ГРЕШКА,ГРЕШКА
                        потврдити('ipconfig','inet 10.0.2.15')
                    потврдити('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    потврдити(пречица_вриједност_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    потврдити('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    потврдити('ip link set dev sl0 down','sl0: DOWN');потврдити('ping -c 1 10.0.2.2; echo STATUS=$?','ГРЕШКА -100','STATUS=1')
                    потврдити('ipconfig up','sl0: UP')
                    потврдити(пречица_вриједност_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    потврдити('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    потврдити('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');потврдити(пречица_вриједност_0a38607b['route'],'10.0.2.2 sl0')
                    потврдити('ftpd start','FTP listening')
                    потврдити(пречица_вриједност_0a38607b['netstat'],'10.0.2.20:21','LISTEN');потврдити('ss','LISTEN')
                    потврдити('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ГРЕШКА -16')
                    with ftplib.FTP() as клијент_вриједност:
                        клијент_вриједност.connect('127.0.0.2',број_порта,timeout=20);клијент_вриједност.login();подаци=b'Network address was changed in the guest.\n'
                        клијент_вриједност.storbinary('STOR net-state.txt',io.BytesIO(подаци));받은자료=bytearray();клијент_вриједност.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==подаци;клијент_вриједност.delete('net-state.txt')
                    потврдити('ftpd stop','FTP stopped');потврдити('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    извештај_вриједност['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Текст);assert 찾음,Текст;return tuple(map(int,찾음.groups()))
                    전=저장값(потврдити('df','RAM only'));потврдити('echo disk-proof > sys-state.txt');후=저장값(потврдити(пречица_вриједност_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    потврдити('rm sys-state.txt');assert 저장값(љуска('df'))==전
                    Меморија_вриједност=потврдити(пречица_вриједност_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Меморија_вриједност).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    потврдити(пречица_вриједност_0a38607b['ps'],'kernel/shell');потврдити(пречица_вриједност_0a38607b['uptime'],'seconds')
                    стање_информација=потврдити(пречица_вриједност_0a38607b['top']+' -n 2','kernel/shell');assert стање_информација.count('PID SLOT STATE')==2,стање_информација
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    потврдити('terminal','TERMINAL READY');Покрени=len(евиденција_ред);послати(b'vi process.txt\n');받기(b'NORMAL',Покрени)
                    Покрени=len(евиденција_ред);послати(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Покрени)
                    унос_Листа=потврдити('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',унос_Листа);assert 찾음 and int(찾음.group(2))>0,унос_Листа
                    потврдити('free','EL0 mapped KiB: '+찾음.group(2))
                    Покрени=len(евиденција_ред);послати(b'top\n');받기(b'PID SLOT STATE',Покрени);послати(b'q');받기(b'jkoros-native> ',Покрени)
                    # Test a multibyte prefix through the real shell completion path.
                    if пречица_вриједност_0a38607b['df']!='df':
                        Покрени=len(евиденција_ред);послати((пречица_вриједност_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Покрени);받기(b'jkoros-native> ',Покрени)
                    извештај_вриједност['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as контрола_вриједност:
                    контрола_вриједност.settimeout(15);контрола_вриједност.connect(str(контрола_пут));ток_вриједност=контрола_вриједност.makefile('rwb');json.loads(ток_вриједност.readline());ток_вриједност.write(b'{"execute":"qmp_capabilities"}\n');ток_вриједност.flush()
                    while 'return' not in json.loads(ток_вриједност.readline()):pass
                    послати((('poweroff' if Аргументи.poweroff_only else пречица_вриједност_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Догађај=json.loads(ток_вриједност.readline())
                        if Догађај.get('event')=='SHUTDOWN':break
                    assert Догађај['data']['guest'] and Догађај['data']['reason']=='guest-shutdown',Догађај
                    assert Процес_вриједност.wait(timeout=15)==0
                    извештај_вриједност['shutdown']=Догађај;извештај_вриједност['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                извештај_вриједност['network_trace']=мост_вриједност.траг_евиденција
                assert Аргументи.poweroff_only or any(унос_вриједност['protocol']==1 and унос_вриједност['direction']=='from_guest' for унос_вриједност in мост_вриједност.траг_евиденција)
                извештај_вриједност['passed']=True
            finally:
                if Процес_вриједност.poll() is None:os.killpg(Процес_вриједност.pid,signal.SIGTERM)
                try:Процес_вриједност.wait(timeout=10)
                except subprocess.TimeoutExpired:Процес_вриједност.kill();Процес_вриједност.wait()
                изабрати_ставка.close();(Излаз/'serial.log').write_bytes(евиденција_ред);(Излаз/'report.json').write_text(json.dumps(извештај_вриједност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Кључ_вриједност:вриједност for Кључ_вриједност,вриједност in извештај_вриједност.items() if Кључ_вриједност!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Покрени()
