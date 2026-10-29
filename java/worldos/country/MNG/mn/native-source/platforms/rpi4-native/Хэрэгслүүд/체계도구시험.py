#!/usr/bin/env python3
"""бодит_өгөгдөл 자체 커널의 IP/ICMP, төлөв_утга асуулга_утга, 현지어 Тушаал, 게스트 Гарах_програм баталгаажуулах."""
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


def Ажиллуулах():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Тохиргоо={};нэр_хүснэгт={}
    if 인수.edition:
        나라=인수.edition.resolve();Тохиргоо=json.loads((나라/'native.json').read_text());нэр_хүснэгт=Тохиргоо['identifiers'];기준=나라/Тохиргоо['source']/Тохиргоо['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        хост=나라/'host/qemu'
        if хост.is_file():os.environ['QEMU_AARCH64']=str(хост)
    Хэрэгслүүд=기준/Path(Тохиргоо.get('runner','Хэрэгслүүд/Гүйцэтгэх_команд.py')).parent
    sys.path.insert(0,str(Хэрэгслүүд))
    def Унших(Нэр):
        ЗАМ=Хэрэгслүүд/(нэр_хүснэгт.get(Нэр,Нэр)+'.py');нөхцөл_байдал_утга=importlib.util.spec_from_file_location('test_'+Нэр,str(ЗАМ));모듈=importlib.util.module_from_spec(нөхцөл_байдал_утга);нөхцөл_байдал_утга.loader.exec_module(모듈);return 모듈
    실행모듈=Унших('Гүйцэтгэх_команд');망모듈=Унших('통신다리');Тушаал=getattr(실행모듈,нэр_хүснэгт.get('Тушаал','Тушаал'));다리형=getattr(망모듈,нэр_хүснэгт.get('통신다리','통신다리'))
    нэр_утга=Тохиргоо.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_хаяг','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'үзүүлэх_тусламж'})
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
    출력=인수.output or 기준/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    тайлан_утга_ddf2aaf3={'passed':False,'country':Тохиргоо.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    бичих_мөр_6e8b375a=bytearray();ДАРААЛАЛ_утга=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        хяналт_зам=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Хайх_утга:Хайх_утга.bind(('127.0.0.1',0));접속번호=Хайх_утга.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,авах=True,게스트주소=ipTestText('10.0.2.20'),хост_хаяг='127.0.0.2') as 다리:
            үйл_явц_утга=subprocess.Popen(Тушаал()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(хяналт_зам)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            сонгох_зүйл=selectors.DefaultSelector();сонгох_зүйл.register(үйл_явц_утга.stdout,selectors.EVENT_READ)
            def 받기(үзүүлэх_утга,Ажиллуулах=0,제한=45):
                끝=time.monotonic()+제한
                while үзүүлэх_утга not in бичих_мөр_6e8b375a[Ажиллуулах:]:
                    if time.monotonic()>끝 or үйл_явц_утга.poll() is not None:raise AssertionError('Missing '+repr(үзүүлэх_утга)+'\n'+бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8','replace'))
                    for түлхүүр_утга,_ in сонгох_зүйл.select(.1):
                        өгөгдөл=түлхүүр_утга.fileobj.read(65536)
                        if өгөгдөл:бичих_мөр_6e8b375a.extend(өгөгдөл)
                return бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8','replace').replace('\r\n','\n')
            def илгээх(өгөгдөл):үйл_явц_утга.stdin.write(өгөгдөл);үйл_явц_утга.stdin.flush()
            def бүрхүүл(Бичвэр):
                Бичвэр=ipTestText(Бичвэр)
                print(тайлан_утга_ddf2aaf3['country'],Бичвэр,flush=True);ДАРААЛАЛ_утга[0]+=1;үзүүлэх_утга='__SYSTEM_DONE_'+str(ДАРААЛАЛ_утга[0])+'__';Ажиллуулах=len(бичих_мөр_6e8b375a)
                илгээх((Бичвэр+'; echo; echo '+үзүүлэх_утга+'\n').encode())
                끝표시=('\r\n'+үзүүлэх_утга+'\r\n').encode();받기(끝표시,Ажиллуулах)
                끝자리=бичих_мөр_6e8b375a.index(끝표시,Ажиллуулах)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8','replace').replace('\r\n','\n')
            def шалгах(Бичвэр,*값들):
                хариулах=бүрхүүл(Бичвэр)
                for утга in 값들:assert ipTestText(утга) in хариулах,(Бичвэр,утга,хариулах)
                return хариулах
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    тусламж_утга_8d901cc2=шалгах('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in нэр_утга.values():assert 별칭 in тусламж_утга_8d901cc2,(별칭,тусламж_утга_8d901cc2)
                    шалгах(нэр_утга['help']+' system','Network / system')
                    шалгах('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    шалгах(нэр_утга['ipconfig'],'inet 10.0.2.15');шалгах('ip addr show','sl0: UP');шалгах('ifconfig','sl0: UP')
                    for буруу_Тохиргоо in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Алдаа=шалгах('ipconfig set '+буруу_Тохиргоо+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Алдаа,Алдаа
                        шалгах('ipconfig','inet 10.0.2.15')
                    шалгах('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    шалгах(нэр_утга['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    шалгах('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    шалгах('ip link set dev sl0 down','sl0: DOWN');шалгах('ping -c 1 10.0.2.2; echo STATUS=$?','Алдаа -100','STATUS=1')
                    шалгах('ipconfig up','sl0: UP')
                    шалгах(нэр_утга['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    шалгах('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    шалгах('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');шалгах(нэр_утга['route'],'10.0.2.2 sl0')
                    шалгах('ftpd start','FTP listening')
                    шалгах(нэр_утга['netstat'],'10.0.2.20:21','LISTEN');шалгах('ss','LISTEN')
                    шалгах('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Алдаа -16')
                    with ftplib.FTP() as клиент_утга:
                        клиент_утга.connect('127.0.0.2',접속번호,timeout=20);клиент_утга.login();өгөгдөл=b'Network address was changed in the guest.\n'
                        клиент_утга.storbinary('STOR net-state.txt',io.BytesIO(өгөгдөл));받은자료=bytearray();клиент_утга.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==өгөгдөл;клиент_утга.delete('net-state.txt')
                    шалгах('ftpd stop','FTP stopped');шалгах('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    тайлан_утга_ddf2aaf3['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Бичвэр):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Бичвэр);assert 찾음,Бичвэр;return tuple(map(int,찾음.groups()))
                    전=저장값(шалгах('df','RAM only'));шалгах('echo disk-proof > sys-state.txt');후=저장값(шалгах(нэр_утга['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    шалгах('rm sys-state.txt');assert 저장값(бүрхүүл('df'))==전
                    санах_ой_утга=шалгах(нэр_утга['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',санах_ой_утга).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    шалгах(нэр_утга['ps'],'kernel/shell');шалгах(нэр_утга['uptime'],'seconds')
                    төлөв_мэдээлэл=шалгах(нэр_утга['top']+' -n 2','kernel/shell');assert төлөв_мэдээлэл.count('PID SLOT STATE')==2,төлөв_мэдээлэл
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    шалгах('terminal','TERMINAL READY');Ажиллуулах=len(бичих_мөр_6e8b375a);илгээх(b'vi process.txt\n');받기(b'NORMAL',Ажиллуулах)
                    Ажиллуулах=len(бичих_мөр_6e8b375a);илгээх(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Ажиллуулах)
                    оролт_Жагсаалт=шалгах('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',оролт_Жагсаалт);assert 찾음 and int(찾음.group(2))>0,оролт_Жагсаалт
                    шалгах('free','EL0 mapped KiB: '+찾음.group(2))
                    Ажиллуулах=len(бичих_мөр_6e8b375a);илгээх(b'top\n');받기(b'PID SLOT STATE',Ажиллуулах);илгээх(b'q');받기(b'jkoros-native> ',Ажиллуулах)
                    # Test a multibyte prefix through the real shell completion path.
                    if нэр_утга['df']!='df':
                        Ажиллуулах=len(бичих_мөр_6e8b375a);илгээх((нэр_утга['df'][:-1]+'\t\n').encode());받기(b'RAM only',Ажиллуулах);받기(b'jkoros-native> ',Ажиллуулах)
                    тайлан_утга_ddf2aaf3['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as хяналт_утга:
                    хяналт_утга.settimeout(15);хяналт_утга.connect(str(хяналт_зам));урсгал_утга=хяналт_утга.makefile('rwb');json.loads(урсгал_утга.readline());урсгал_утга.write(b'{"execute":"qmp_capabilities"}\n');урсгал_утга.flush()
                    while 'return' not in json.loads(урсгал_утга.readline()):pass
                    илгээх((('poweroff' if 인수.poweroff_only else нэр_утга['poweroff'])+'\n').encode())
                    while True:
                        үйлдэл=json.loads(урсгал_утга.readline())
                        if үйлдэл.get('event')=='SHUTDOWN':break
                    assert үйлдэл['data']['guest'] and үйлдэл['data']['reason']=='guest-shutdown',үйлдэл
                    assert үйл_явц_утга.wait(timeout=15)==0
                    тайлан_утга_ddf2aaf3['shutdown']=үйлдэл;тайлан_утга_ddf2aaf3['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                тайлан_утга_ddf2aaf3['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(оролт_утга['protocol']==1 and оролт_утга['direction']=='from_guest' for оролт_утга in 다리.추적기록)
                тайлан_утга_ddf2aaf3['passed']=True
            finally:
                if үйл_явц_утга.poll() is None:os.killpg(үйл_явц_утга.pid,signal.SIGTERM)
                try:үйл_явц_утга.wait(timeout=10)
                except subprocess.TimeoutExpired:үйл_явц_утга.kill();үйл_явц_утга.wait()
                сонгох_зүйл.close();(출력/'serial.log').write_bytes(бичих_мөр_6e8b375a);(출력/'report.json').write_text(json.dumps(тайлан_утга_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({түлхүүр_утга:утга for түлхүүр_утга,утга in тайлан_утга_ddf2aaf3.items() if түлхүүр_утга!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Ажиллуулах()
