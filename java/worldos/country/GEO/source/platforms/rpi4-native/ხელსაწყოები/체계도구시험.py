#!/usr/bin/env python3
"""რეალური_მონაცემები 자체 커널의 IP/ICMP, სტატუსი_მნიშვნელობა მოთხოვნა_მნიშვნელობა, 현지어 ბრძანება, 게스트 გასვლა_აპი შემოწმება."""
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


def გაშვება():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    პროეცირება_ფესვი=Path(__file__).resolve().parents[1];პარამეტრები={};სახელი_ცხრილი={}
    if 인수.edition:
        나라=인수.edition.resolve();პარამეტრები=json.loads((나라/'native.json').read_text());სახელი_ცხრილი=პარამეტრები['identifiers'];პროეცირება_ფესვი=나라/პარამეტრები['source']/პარამეტრები['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        მასპინძელი=나라/'host/qemu'
        if მასპინძელი.is_file():os.environ['QEMU_AARCH64']=str(მასპინძელი)
    ხელსაწყოები=პროეცირება_ფესვი/Path(პარამეტრები.get('runner','ხელსაწყოები/შესრულება_ბრძანება.py')).parent
    sys.path.insert(0,str(ხელსაწყოები))
    def კითხვა(სახელი):
        გეზი=ხელსაწყოები/(სახელი_ცხრილი.get(სახელი,სახელი)+'.py');დავალება_მნიშვნელობა=importlib.util.spec_from_file_location('test_'+სახელი,str(გეზი));მოდული_მნიშვნელობა=importlib.util.module_from_spec(დავალება_მნიშვნელობა);დავალება_მნიშვნელობა.loader.exec_module(მოდული_მნიშვნელობა);return მოდული_მნიშვნელობა
    실행모듈=კითხვა('შესრულება_ბრძანება');ქსელი_მოდული=კითხვა('ქსელი_ხიდი');ბრძანება=getattr(실행모듈,სახელი_ცხრილი.get('ბრძანება','ბრძანება'));ხიდი_აკრეფა=getattr(ქსელი_მოდული,სახელი_ცხრილი.get('ქსელი_ხიდი','ქსელი_ხიდი'))
    მეტსახელი_მნიშვნელობა=პარამეტრები.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_მისამართი','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ჩვენება_დახმარება'})
    sys.path.insert(0,str(პროეცირება_ფესვი/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(პროეცირება_ფესვი);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or პროეცირება_ფესვი/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    ანგარიში_მნიშვნელობა={'passed':False,'country':პარამეტრები.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ჟურნალი_ჩაწერა=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        მართვა_მდებარეობა=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ძებნა_მნიშვნელობა:ძებნა_მნიშვნელობა.bind(('127.0.0.1',0));접속번호=ძებნა_მნიშვნელობა.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ხიდი_აკრეფა(접속번호,გადაღება=True,სტუმარი_მისამართი=ipTestText('10.0.2.20'),მასპინძელი_მისამართი='127.0.0.2') as ხიდი_მნიშვნელობა:
            პროცესი_მნიშვნელობა=subprocess.Popen(ბრძანება()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(მართვა_მდებარეობა)]+ხიდი_მნიშვნელობა.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            არჩევა_ელემენტი=selectors.DefaultSelector();არჩევა_ელემენტი.register(პროცესი_მნიშვნელობა.stdout,selectors.EVENT_READ)
            def 받기(ჩვენება_მნიშვნელობა,გაშვება=0,제한=45):
                끝=time.monotonic()+제한
                while ჩვენება_მნიშვნელობა not in ჟურნალი_ჩაწერა[გაშვება:]:
                    if time.monotonic()>끝 or პროცესი_მნიშვნელობა.poll() is not None:raise AssertionError('Missing '+repr(ჩვენება_მნიშვნელობა)+'\n'+ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8','replace'))
                    for კლავიში_მნიშვნელობა,_ in არჩევა_ელემენტი.select(.1):
                        მონაცემები=კლავიში_მნიშვნელობა.fileobj.read(65536)
                        if მონაცემები:ჟურნალი_ჩაწერა.extend(მონაცემები)
                return ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8','replace').replace('\r\n','\n')
            def გაგზავნა(მონაცემები):პროცესი_მნიშვნელობა.stdin.write(მონაცემები);პროცესი_მნიშვნელობა.stdin.flush()
            def გარემო(ტექსტი):
                ტექსტი=ipTestText(ტექსტი)
                print(ანგარიში_მნიშვნელობა['country'],ტექსტი,flush=True);차례[0]+=1;ჩვენება_მნიშვნელობა='__SYSTEM_DONE_'+str(차례[0])+'__';გაშვება=len(ჟურნალი_ჩაწერა)
                გაგზავნა((ტექსტი+'; echo; echo '+ჩვენება_მნიშვნელობა+'\n').encode())
                끝표시=('\r\n'+ჩვენება_მნიშვნელობა+'\r\n').encode();받기(끝표시,გაშვება)
                დასასრული_პოზიცია=ჟურნალი_ჩაწერა.index(끝표시,გაშვება)+len(끝표시)
                받기(b'jkoros-native> ',დასასრული_პოზიცია)
                return ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8','replace').replace('\r\n','\n')
            def გადამოწმება(ტექსტი,*값들):
                პასუხი=გარემო(ტექსტი)
                for მნიშვნელობა in 값들:assert ipTestText(მნიშვნელობა) in პასუხი,(ტექსტი,მნიშვნელობა,პასუხი)
                return პასუხი
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    დახმარება_მნიშვნელობა=გადამოწმება('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in მეტსახელი_მნიშვნელობა.values():assert 별칭 in დახმარება_მნიშვნელობა,(별칭,დახმარება_მნიშვნელობა)
                    გადამოწმება(მეტსახელი_მნიშვნელობა['help']+' system','Network / system')
                    გადამოწმება('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    გადამოწმება(მეტსახელი_მნიშვნელობა['ipconfig'],'inet 10.0.2.15');გადამოწმება('ip addr show','sl0: UP');გადამოწმება('ifconfig','sl0: UP')
                    for არასწორი_პარამეტრები in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        შეცდომა=გადამოწმება('ipconfig set '+არასწორი_პარამეტრები+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in შეცდომა,შეცდომა
                        გადამოწმება('ipconfig','inet 10.0.2.15')
                    გადამოწმება('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    გადამოწმება(მეტსახელი_მნიშვნელობა['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    გადამოწმება('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    გადამოწმება('ip link set dev sl0 down','sl0: DOWN');გადამოწმება('ping -c 1 10.0.2.2; echo STATUS=$?','შეცდომა -100','STATUS=1')
                    გადამოწმება('ipconfig up','sl0: UP')
                    გადამოწმება(მეტსახელი_მნიშვნელობა['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    გადამოწმება('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    გადამოწმება('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');გადამოწმება(მეტსახელი_მნიშვნელობა['route'],'10.0.2.2 sl0')
                    გადამოწმება('ftpd start','FTP listening')
                    გადამოწმება(მეტსახელი_მნიშვნელობა['netstat'],'10.0.2.20:21','LISTEN');გადამოწმება('ss','LISTEN')
                    გადამოწმება('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','შეცდომა -16')
                    with ftplib.FTP() as კლიენტი_მნიშვნელობა:
                        კლიენტი_მნიშვნელობა.connect('127.0.0.2',접속번호,timeout=20);კლიენტი_მნიშვნელობა.login();მონაცემები=b'Network address was changed in the guest.\n'
                        კლიენტი_მნიშვნელობა.storbinary('STOR net-state.txt',io.BytesIO(მონაცემები));받은자료=bytearray();კლიენტი_მნიშვნელობა.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==მონაცემები;კლიენტი_მნიშვნელობა.delete('net-state.txt')
                    გადამოწმება('ftpd stop','FTP stopped');გადამოწმება('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ანგარიში_მნიშვნელობა['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ტექსტი):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ტექსტი);assert 찾음,ტექსტი;return tuple(map(int,찾음.groups()))
                    전=저장값(გადამოწმება('df','RAM only'));გადამოწმება('echo disk-proof > sys-state.txt');후=저장값(გადამოწმება(მეტსახელი_მნიშვნელობა['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    გადამოწმება('rm sys-state.txt');assert 저장값(გარემო('df'))==전
                    მეხსიერება_მნიშვნელობა=გადამოწმება(მეტსახელი_მნიშვნელობა['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',მეხსიერება_მნიშვნელობა).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    გადამოწმება(მეტსახელი_მნიშვნელობა['ps'],'kernel/shell');გადამოწმება(მეტსახელი_მნიშვნელობა['uptime'],'seconds')
                    სტატუსი_ინფო=გადამოწმება(მეტსახელი_მნიშვნელობა['top']+' -n 2','kernel/shell');assert სტატუსი_ინფო.count('PID SLOT STATE')==2,სტატუსი_ინფო
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    გადამოწმება('terminal','TERMINAL READY');გაშვება=len(ჟურნალი_ჩაწერა);გაგზავნა(b'vi process.txt\n');받기(b'NORMAL',გაშვება)
                    გაშვება=len(ჟურნალი_ჩაწერა);გაგზავნა(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',გაშვება)
                    შენატანი_სია=გადამოწმება('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',შენატანი_სია);assert 찾음 and int(찾음.group(2))>0,შენატანი_სია
                    გადამოწმება('free','EL0 mapped KiB: '+찾음.group(2))
                    გაშვება=len(ჟურნალი_ჩაწერა);გაგზავნა(b'top\n');받기(b'PID SLOT STATE',გაშვება);გაგზავნა(b'q');받기(b'jkoros-native> ',გაშვება)
                    # Test a multibyte prefix through the real shell completion path.
                    if მეტსახელი_მნიშვნელობა['df']!='df':
                        გაშვება=len(ჟურნალი_ჩაწერა);გაგზავნა((მეტსახელი_მნიშვნელობა['df'][:-1]+'\t\n').encode());받기(b'RAM only',გაშვება);받기(b'jkoros-native> ',გაშვება)
                    ანგარიში_მნიშვნელობა['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as მართვა_მნიშვნელობა:
                    მართვა_მნიშვნელობა.settimeout(15);მართვა_მნიშვნელობა.connect(str(მართვა_მდებარეობა));ნაკადი_მნიშვნელობა=მართვა_მნიშვნელობა.makefile('rwb');json.loads(ნაკადი_მნიშვნელობა.readline());ნაკადი_მნიშვნელობა.write(b'{"execute":"qmp_capabilities"}\n');ნაკადი_მნიშვნელობა.flush()
                    while 'return' not in json.loads(ნაკადი_მნიშვნელობა.readline()):pass
                    გაგზავნა((('poweroff' if 인수.poweroff_only else მეტსახელი_მნიშვნელობა['poweroff'])+'\n').encode())
                    while True:
                        მოვლენა=json.loads(ნაკადი_მნიშვნელობა.readline())
                        if მოვლენა.get('event')=='SHUTDOWN':break
                    assert მოვლენა['data']['guest'] and მოვლენა['data']['reason']=='guest-shutdown',მოვლენა
                    assert პროცესი_მნიშვნელობა.wait(timeout=15)==0
                    ანგარიში_მნიშვნელობა['shutdown']=მოვლენა;ანგარიში_მნიშვნელობა['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ანგარიში_მნიშვნელობა['network_trace']=ხიდი_მნიშვნელობა.추적기록
                assert 인수.poweroff_only or any(შენატანი_მნიშვნელობა['protocol']==1 and შენატანი_მნიშვნელობა['direction']=='from_guest' for შენატანი_მნიშვნელობა in ხიდი_მნიშვნელობა.추적기록)
                ანგარიში_მნიშვნელობა['passed']=True
            finally:
                if პროცესი_მნიშვნელობა.poll() is None:os.killpg(პროცესი_მნიშვნელობა.pid,signal.SIGTERM)
                try:პროცესი_მნიშვნელობა.wait(timeout=10)
                except subprocess.TimeoutExpired:პროცესი_მნიშვნელობა.kill();პროცესი_მნიშვნელობა.wait()
                არჩევა_ელემენტი.close();(출력/'serial.log').write_bytes(ჟურნალი_ჩაწერა);(출력/'report.json').write_text(json.dumps(ანგარიში_მნიშვნელობა,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({კლავიში_მნიშვნელობა:მნიშვნელობა for კლავიში_მნიშვნელობა,მნიშვნელობა in ანგარიში_მნიშვნელობა.items() if კლავიში_მნიშვნელობა!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':გაშვება()
