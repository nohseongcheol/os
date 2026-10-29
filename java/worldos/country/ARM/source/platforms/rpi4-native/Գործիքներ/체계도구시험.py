#!/usr/bin/env python3
"""իրական_տվյալ 자체 커널의 IP/ICMP, վիճակ_արժեք հարցում_արժեք, 현지어 Հրահանգ, 게스트 Ելք_ծրագիր վավերացնել."""
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


def Գործարկել():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    արձակել_արմատ=Path(__file__).resolve().parents[1];Նախընտրանքներ={};անուն_աղյուսակ={}
    if 인수.edition:
        나라=인수.edition.resolve();Նախընտրանքներ=json.loads((나라/'native.json').read_text());անուն_աղյուսակ=Նախընտրանքներ['identifiers'];արձակել_արմատ=나라/Նախընտրանքներ['source']/Նախընտրանքներ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        հոստ=나라/'host/qemu'
        if հոստ.is_file():os.environ['QEMU_AARCH64']=str(հոստ)
    Գործիքներ=արձակել_արմատ/Path(Նախընտրանքներ.get('runner','Գործիքներ/կատարել_հրաման.py')).parent
    sys.path.insert(0,str(Գործիքներ))
    def Ընթերցում(Անուն):
        Ճանապարհ=Գործիքներ/(անուն_աղյուսակ.get(Անուն,Անուն)+'.py');գործ_արժեք=importlib.util.spec_from_file_location('test_'+Անուն,str(Ճանապարհ));հանգույց_արժեք_6d2d8bf4=importlib.util.module_from_spec(գործ_արժեք);գործ_արժեք.loader.exec_module(հանգույց_արժեք_6d2d8bf4);return հանգույց_արժեք_6d2d8bf4
    실행모듈=Ընթերցում('կատարել_հրաման');Ցանց_հանգույց=Ընթերցում('Ցանց_կամուրջ');Հրահանգ=getattr(실행모듈,անուն_աղյուսակ.get('Հրահանգ','Հրահանգ'));կամուրջ_մուտքագրել=getattr(Ցանց_հանգույց,անուն_աղյուսակ.get('Ցանց_կամուրջ','Ցանց_կամուրջ'))
    այլանուն_արժեք=Նախընտրանքներ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_հասցե','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ցուցադրել_օգնություն'})
    sys.path.insert(0,str(արձակել_արմատ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(արձակել_արմատ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Ելք=인수.output or արձակել_արմատ/'build/verification/system-tools';Ելք.mkdir(parents=True,exist_ok=True)
    զեկույց_արժեք={'passed':False,'country':Նախընտրանքներ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    մատյան_տող=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        հսկում_ուղի=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as որոնել_արժեք:որոնել_արժեք.bind(('127.0.0.1',0));접속번호=որոնել_արժեք.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with կամուրջ_մուտքագրել(접속번호,նկարահանել=True,հյուր_հասցե=ipTestText('10.0.2.20'),հոստ_հասցե='127.0.0.2') as կամուրջ_արժեք:
            Ընթացք_արժեք=subprocess.Popen(Հրահանգ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(հսկում_ուղի)]+կամուրջ_արժեք.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ընտրել_միավոր=selectors.DefaultSelector();ընտրել_միավոր.register(Ընթացք_արժեք.stdout,selectors.EVENT_READ)
            def 받기(ցուցադրել_արժեք,Գործարկել=0,제한=45):
                끝=time.monotonic()+제한
                while ցուցադրել_արժեք not in մատյան_տող[Գործարկել:]:
                    if time.monotonic()>끝 or Ընթացք_արժեք.poll() is not None:raise AssertionError('Missing '+repr(ցուցադրել_արժեք)+'\n'+մատյան_տող[Գործարկել:].decode('utf-8','replace'))
                    for ստեղն_արժեք,_ in ընտրել_միավոր.select(.1):
                        տվյալ=ստեղն_արժեք.fileobj.read(65536)
                        if տվյալ:մատյան_տող.extend(տվյալ)
                return մատյան_տող[Գործարկել:].decode('utf-8','replace').replace('\r\n','\n')
            def ուղարկել(տվյալ):Ընթացք_արժեք.stdin.write(տվյալ);Ընթացք_արժեք.stdin.flush()
            def խեցի(Տեքստ):
                Տեքստ=ipTestText(Տեքստ)
                print(զեկույց_արժեք['country'],Տեքստ,flush=True);차례[0]+=1;ցուցադրել_արժեք='__SYSTEM_DONE_'+str(차례[0])+'__';Գործարկել=len(մատյան_տող)
                ուղարկել((Տեքստ+'; echo; echo '+ցուցադրել_արժեք+'\n').encode())
                끝표시=('\r\n'+ցուցադրել_արժեք+'\r\n').encode();받기(끝표시,Գործարկել)
                վերջացնել_դիրք=մատյան_տող.index(끝표시,Գործարկել)+len(끝표시)
                받기(b'jkoros-native> ',վերջացնել_դիրք)
                return մատյան_տող[Գործարկել:].decode('utf-8','replace').replace('\r\n','\n')
            def հաստատել(Տեքստ,*값들):
                պատասխանել=խեցի(Տեքստ)
                for արժեք in 값들:assert ipTestText(արժեք) in պատասխանել,(Տեքստ,արժեք,պատասխանել)
                return պատասխանել
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    օգնություն_արժեք=հաստատել('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in այլանուն_արժեք.values():assert 별칭 in օգնություն_արժեք,(별칭,օգնություն_արժեք)
                    հաստատել(այլանուն_արժեք['help']+' system','Network / system')
                    հաստատել('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    հաստատել(այլանուն_արժեք['ipconfig'],'inet 10.0.2.15');հաստատել('ip addr show','sl0: UP');հաստատել('ifconfig','sl0: UP')
                    for անվավեր_Կարգավորումներ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Սխալ=հաստատել('ipconfig set '+անվավեր_Կարգավորումներ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Սխալ,Սխալ
                        հաստատել('ipconfig','inet 10.0.2.15')
                    հաստատել('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    հաստատել(այլանուն_արժեք['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    հաստատել('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    հաստատել('ip link set dev sl0 down','sl0: DOWN');հաստատել('ping -c 1 10.0.2.2; echo STATUS=$?','Սխալ -100','STATUS=1')
                    հաստատել('ipconfig up','sl0: UP')
                    հաստատել(այլանուն_արժեք['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    հաստատել('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    հաստատել('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');հաստատել(այլանուն_արժեք['route'],'10.0.2.2 sl0')
                    հաստատել('ftpd start','FTP listening')
                    հաստատել(այլանուն_արժեք['netstat'],'10.0.2.20:21','LISTEN');հաստատել('ss','LISTEN')
                    հաստատել('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Սխալ -16')
                    with ftplib.FTP() as սպասառու_արժեք:
                        սպասառու_արժեք.connect('127.0.0.2',접속번호,timeout=20);սպասառու_արժեք.login();տվյալ=b'Network address was changed in the guest.\n'
                        սպասառու_արժեք.storbinary('STOR net-state.txt',io.BytesIO(տվյալ));받은자료=bytearray();սպասառու_արժեք.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==տվյալ;սպասառու_արժեք.delete('net-state.txt')
                    հաստատել('ftpd stop','FTP stopped');հաստատել('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    զեկույց_արժեք['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Տեքստ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Տեքստ);assert 찾음,Տեքստ;return tuple(map(int,찾음.groups()))
                    전=저장값(հաստատել('df','RAM only'));հաստատել('echo disk-proof > sys-state.txt');후=저장값(հաստատել(այլանուն_արժեք['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    հաստատել('rm sys-state.txt');assert 저장값(խեցի('df'))==전
                    Հիշողություն_արժեք=հաստատել(այլանուն_արժեք['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Հիշողություն_արժեք).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    հաստատել(այլանուն_արժեք['ps'],'kernel/shell');հաստատել(այլանուն_արժեք['uptime'],'seconds')
                    վիճակ_տեղեկություն=հաստատել(այլանուն_արժեք['top']+' -n 2','kernel/shell');assert վիճակ_տեղեկություն.count('PID SLOT STATE')==2,վիճակ_տեղեկություն
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    հաստատել('terminal','TERMINAL READY');Գործարկել=len(մատյան_տող);ուղարկել(b'vi process.txt\n');받기(b'NORMAL',Գործարկել)
                    Գործարկել=len(մատյան_տող);ուղարկել(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Գործարկել)
                    մուտքագրում_Ցուցակ=հաստատել('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',մուտքագրում_Ցուցակ);assert 찾음 and int(찾음.group(2))>0,մուտքագրում_Ցուցակ
                    հաստատել('free','EL0 mapped KiB: '+찾음.group(2))
                    Գործարկել=len(մատյան_տող);ուղարկել(b'top\n');받기(b'PID SLOT STATE',Գործարկել);ուղարկել(b'q');받기(b'jkoros-native> ',Գործարկել)
                    # Test a multibyte prefix through the real shell completion path.
                    if այլանուն_արժեք['df']!='df':
                        Գործարկել=len(մատյան_տող);ուղարկել((այլանուն_արժեք['df'][:-1]+'\t\n').encode());받기(b'RAM only',Գործարկել);받기(b'jkoros-native> ',Գործարկել)
                    զեկույց_արժեք['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as հսկում_արժեք:
                    հսկում_արժեք.settimeout(15);հսկում_արժեք.connect(str(հսկում_ուղի));հոսք_արժեք=հսկում_արժեք.makefile('rwb');json.loads(հոսք_արժեք.readline());հոսք_արժեք.write(b'{"execute":"qmp_capabilities"}\n');հոսք_արժեք.flush()
                    while 'return' not in json.loads(հոսք_արժեք.readline()):pass
                    ուղարկել((('poweroff' if 인수.poweroff_only else այլանուն_արժեք['poweroff'])+'\n').encode())
                    while True:
                        միջոցառում=json.loads(հոսք_արժեք.readline())
                        if միջոցառում.get('event')=='SHUTDOWN':break
                    assert միջոցառում['data']['guest'] and միջոցառում['data']['reason']=='guest-shutdown',միջոցառում
                    assert Ընթացք_արժեք.wait(timeout=15)==0
                    զեկույց_արժեք['shutdown']=միջոցառում;զեկույց_արժեք['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                զեկույց_արժեք['network_trace']=կամուրջ_արժեք.추적기록
                assert 인수.poweroff_only or any(մուտքագրում_արժեք['protocol']==1 and մուտքագրում_արժեք['direction']=='from_guest' for մուտքագրում_արժեք in կամուրջ_արժեք.추적기록)
                զեկույց_արժեք['passed']=True
            finally:
                if Ընթացք_արժեք.poll() is None:os.killpg(Ընթացք_արժեք.pid,signal.SIGTERM)
                try:Ընթացք_արժեք.wait(timeout=10)
                except subprocess.TimeoutExpired:Ընթացք_արժեք.kill();Ընթացք_արժեք.wait()
                ընտրել_միավոր.close();(Ելք/'serial.log').write_bytes(մատյան_տող);(Ելք/'report.json').write_text(json.dumps(զեկույց_արժեք,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ստեղն_արժեք:արժեք for ստեղն_արժեք,արժեք in զեկույց_արժեք.items() if ստեղն_արժեք!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Գործարկել()
