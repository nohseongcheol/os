#!/usr/bin/env python3
"""реален_податоци 자체 커널의 IP/ICMP, статус_VALUE прашалник_VALUE, 현지어 Команда, 게스트 Излез_програма потврди."""
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


def Изврши_2():
    анализатор_48ee4b1b=argparse.ArgumentParser();анализатор_48ee4b1b.add_argument('--edition',type=Path);анализатор_48ee4b1b.add_argument('--output',type=Path);анализатор_48ee4b1b.add_argument('--poweroff-only',action='store_true');Аргументи=анализатор_48ee4b1b.parse_args()
    Project_корен=Path(__file__).resolve().parents[1];Подесувања={};име_табела={}
    if Аргументи.edition:
        나라=Аргументи.edition.resolve();Подесувања=json.loads((나라/'native.json').read_text());име_табела=Подесувања['identifiers'];Project_корен=나라/Подесувања['source']/Подесувања['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        вдоми=나라/'host/qemu'
        if вдоми.is_file():os.environ['QEMU_AARCH64']=str(вдоми)
    Алатки=Project_корен/Path(Подесувања.get('runner','Алатки/Изврши_наредба.py')).parent
    sys.path.insert(0,str(Алатки))
    def Читај(Име):
        ПАТЕКА=Алатки/(име_табела.get(Име,Име)+'.py');задача_VALUE_102996da=importlib.util.spec_from_file_location('test_'+Име,str(ПАТЕКА));модул_VALUE=importlib.util.module_from_spec(задача_VALUE_102996da);задача_VALUE_102996da.loader.exec_module(модул_VALUE);return модул_VALUE
    실행모듈=Читај('Изврши_наредба');Мрежа_модул=Читај('Мрежа_мост');Команда=getattr(실행모듈,име_табела.get('Команда','Команда'));мост_TYPE=getattr(Мрежа_модул,име_табела.get('Мрежа_мост','Мрежа_мост'))
    псевдоним_VALUE=Подесувања.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ИП_адреса','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'прикажи_помош'})
    sys.path.insert(0,str(Project_корен/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_корен);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=Аргументи.output or Project_корен/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    извештај_VALUE={'passed':False,'country':Подесувања.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_ред=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        контрола_патека=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));број_на_порта=SEARCH_VALUE.getsockname()[1]
            if not 50000<=број_на_порта<=50007:break
        with мост_TYPE(број_на_порта,зафати=True,гостин_адреса=ipTestText('10.0.2.20'),вдоми_адреса='127.0.0.2') as мост_VALUE:
            Процес_VALUE=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(контрола_патека)]+мост_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_ставка=selectors.DefaultSelector();CHOOSE_ставка.register(Процес_VALUE.stdout,selectors.EVENT_READ)
            def 받기(прикажи_VALUE,Изврши_2=0,제한=45):
                끝=time.monotonic()+제한
                while прикажи_VALUE not in LOG_ред[Изврши_2:]:
                    if time.monotonic()>끝 or Процес_VALUE.poll() is not None:raise AssertionError('Missing '+repr(прикажи_VALUE)+'\n'+LOG_ред[Изврши_2:].decode('utf-8','replace'))
                    for Клуч_VALUE,_ in CHOOSE_ставка.select(.1):
                        податоци=Клуч_VALUE.fileobj.read(65536)
                        if податоци:LOG_ред.extend(податоци)
                return LOG_ред[Изврши_2:].decode('utf-8','replace').replace('\r\n','\n')
            def испрати(податоци):Процес_VALUE.stdin.write(податоци);Процес_VALUE.stdin.flush()
            def обвивка(Текст):
                Текст=ipTestText(Текст)
                print(извештај_VALUE['country'],Текст,flush=True);SEQUENCE_VALUE[0]+=1;прикажи_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Изврши_2=len(LOG_ред)
                испрати((Текст+'; echo; echo '+прикажи_VALUE+'\n').encode())
                끝표시=('\r\n'+прикажи_VALUE+'\r\n').encode();받기(끝표시,Изврши_2)
                крај_позиционирање=LOG_ред.index(끝표시,Изврши_2)+len(끝표시)
                받기(b'jkoros-native> ',крај_позиционирање)
                return LOG_ред[Изврши_2:].decode('utf-8','replace').replace('\r\n','\n')
            def провери(Текст,*값들):
                одговори=обвивка(Текст)
                for VALUE in 값들:assert ipTestText(VALUE) in одговори,(Текст,VALUE,одговори)
                return одговори
            try:
                받기(b'jkoros-native> ')
                if not Аргументи.poweroff_only:
                    помош_VALUE=провери('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in псевдоним_VALUE.values():assert 별칭 in помош_VALUE,(별칭,помош_VALUE)
                    провери(псевдоним_VALUE['help']+' system','Network / system')
                    провери('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    провери(псевдоним_VALUE['ipconfig'],'inet 10.0.2.15');провери('ip addr show','sl0: UP');провери('ifconfig','sl0: UP')
                    for неважечки_Параметри in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ГРЕШКА=провери('ipconfig set '+неважечки_Параметри+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ГРЕШКА,ГРЕШКА
                        провери('ipconfig','inet 10.0.2.15')
                    провери('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    провери(псевдоним_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    провери('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    провери('ip link set dev sl0 down','sl0: DOWN');провери('ping -c 1 10.0.2.2; echo STATUS=$?','ГРЕШКА -100','STATUS=1')
                    провери('ipconfig up','sl0: UP')
                    провери(псевдоним_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    провери('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    провери('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');провери(псевдоним_VALUE['route'],'10.0.2.2 sl0')
                    провери('ftpd start','FTP listening')
                    провери(псевдоним_VALUE['netstat'],'10.0.2.20:21','LISTEN');провери('ss','LISTEN')
                    провери('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ГРЕШКА -16')
                    with ftplib.FTP() as клиент_VALUE:
                        клиент_VALUE.connect('127.0.0.2',број_на_порта,timeout=20);клиент_VALUE.login();податоци=b'Network address was changed in the guest.\n'
                        клиент_VALUE.storbinary('STOR net-state.txt',io.BytesIO(податоци));RECEIVED_податоци=bytearray();клиент_VALUE.retrbinary('RETR net-state.txt',RECEIVED_податоци.extend);assert RECEIVED_податоци==податоци;клиент_VALUE.delete('net-state.txt')
                    провери('ftpd stop','FTP stopped');провери('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    извештај_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Текст):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Текст);assert 찾음,Текст;return tuple(map(int,찾음.groups()))
                    전=저장값(провери('df','RAM only'));провери('echo disk-proof > sys-state.txt');후=저장값(провери(псевдоним_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    провери('rm sys-state.txt');assert 저장값(обвивка('df'))==전
                    Меморија_VALUE=провери(псевдоним_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Меморија_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    провери(псевдоним_VALUE['ps'],'kernel/shell');провери(псевдоним_VALUE['uptime'],'seconds')
                    статус_информации=провери(псевдоним_VALUE['top']+' -n 2','kernel/shell');assert статус_информации.count('PID SLOT STATE')==2,статус_информации
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    провери('terminal','TERMINAL READY');Изврши_2=len(LOG_ред);испрати(b'vi process.txt\n');받기(b'NORMAL',Изврши_2)
                    Изврши_2=len(LOG_ред);испрати(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Изврши_2)
                    внес_Список=провери('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',внес_Список);assert 찾음 and int(찾음.group(2))>0,внес_Список
                    провери('free','EL0 mapped KiB: '+찾음.group(2))
                    Изврши_2=len(LOG_ред);испрати(b'top\n');받기(b'PID SLOT STATE',Изврши_2);испрати(b'q');받기(b'jkoros-native> ',Изврши_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if псевдоним_VALUE['df']!='df':
                        Изврши_2=len(LOG_ред);испрати((псевдоним_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Изврши_2);받기(b'jkoros-native> ',Изврши_2)
                    извештај_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as контрола_VALUE:
                    контрола_VALUE.settimeout(15);контрола_VALUE.connect(str(контрола_патека));Stream_VALUE=контрола_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    испрати((('poweroff' if Аргументи.poweroff_only else псевдоним_VALUE['poweroff'])+'\n').encode())
                    while True:
                        настан=json.loads(Stream_VALUE.readline())
                        if настан.get('event')=='SHUTDOWN':break
                    assert настан['data']['guest'] and настан['data']['reason']=='guest-shutdown',настан
                    assert Процес_VALUE.wait(timeout=15)==0
                    извештај_VALUE['shutdown']=настан;извештај_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                извештај_VALUE['network_trace']=мост_VALUE.трага_LOG
                assert Аргументи.poweroff_only or any(внес_VALUE['protocol']==1 and внес_VALUE['direction']=='from_guest' for внес_VALUE in мост_VALUE.трага_LOG)
                извештај_VALUE['passed']=True
            finally:
                if Процес_VALUE.poll() is None:os.killpg(Процес_VALUE.pid,signal.SIGTERM)
                try:Процес_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Процес_VALUE.kill();Процес_VALUE.wait()
                CHOOSE_ставка.close();(출력/'serial.log').write_bytes(LOG_ред);(출력/'report.json').write_text(json.dumps(извештај_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Клуч_VALUE:VALUE for Клуч_VALUE,VALUE in извештај_VALUE.items() if Клуч_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Изврши_2()
