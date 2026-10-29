#!/usr/bin/env python3
"""tota_tshedimosetso 자체 커널의 IP/ICMP, kemo_Boleng fenenkolola_Boleng, 현지어 Taelo, 게스트 tswaya_Tiriso netefatsa_5fb2b747."""
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


def dirisa():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Diseting={};leina_lenaneothalo={}
    if 인수.edition:
        나라=인수.edition.resolve();Diseting=json.loads((나라/'native.json').read_text());leina_lenaneothalo=Diseting['identifiers'];기준=나라/Diseting['source']/Diseting['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        pinagare=나라/'host/qemu'
        if pinagare.is_file():os.environ['QEMU_AARCH64']=str(pinagare)
    Thuluse=기준/Path(Diseting.get('runner','Thuluse/diragatsa_Taelo.py')).parent
    sys.path.insert(0,str(Thuluse))
    def 읽기(leina):
        tsela=Thuluse/(leina_lenaneothalo.get(leina,leina)+'.py');konteraka_Boleng=importlib.util.spec_from_file_location('test_'+leina,str(tsela));모듈=importlib.util.module_from_spec(konteraka_Boleng);konteraka_Boleng.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('diragatsa_Taelo');망모듈=읽기('Neteweke_leborogo');Taelo=getattr(실행모듈,leina_lenaneothalo.get('Taelo','Taelo'));leborogo_tlanya=getattr(망모듈,leina_lenaneothalo.get('Neteweke_leborogo','Neteweke_leborogo'))
    Imeile_nngwe_Boleng=Diseting.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_aterese','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'bontsha_thuso'})
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
    pego_Boleng={'passed':False,'country':Diseting.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    rekota_mola=bytearray();TATELANO_Boleng=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        taolo_tsela=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as batla_Boleng:batla_Boleng.bind(('127.0.0.1',0));접속번호=batla_Boleng.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with leborogo_tlanya(접속번호,tshwara=True,moeng_aterese=ipTestText('10.0.2.20'),pinagare_aterese='127.0.0.2') as leborogo_Boleng:
            Thulaganyo_Boleng=subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(taolo_tsela)]+leborogo_Boleng.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            tlhopha_selwana=selectors.DefaultSelector();tlhopha_selwana.register(Thulaganyo_Boleng.stdout,selectors.EVENT_READ)
            def 받기(bontsha_Boleng,dirisa=0,제한=45):
                끝=time.monotonic()+제한
                while bontsha_Boleng not in rekota_mola[dirisa:]:
                    if time.monotonic()>끝 or Thulaganyo_Boleng.poll() is not None:raise AssertionError('Missing '+repr(bontsha_Boleng)+'\n'+rekota_mola[dirisa:].decode('utf-8','replace'))
                    for taetsi_Boleng,_ in tlhopha_selwana.select(.1):
                        tshedimosetso=taetsi_Boleng.fileobj.read(65536)
                        if tshedimosetso:rekota_mola.extend(tshedimosetso)
                return rekota_mola[dirisa:].decode('utf-8','replace').replace('\r\n','\n')
            def romela(tshedimosetso):Thulaganyo_Boleng.stdin.write(tshedimosetso);Thulaganyo_Boleng.stdin.flush()
            def setlhalosataelo(SMS):
                SMS=ipTestText(SMS)
                print(pego_Boleng['country'],SMS,flush=True);TATELANO_Boleng[0]+=1;bontsha_Boleng='__SYSTEM_DONE_'+str(TATELANO_Boleng[0])+'__';dirisa=len(rekota_mola)
                romela((SMS+'; echo; echo '+bontsha_Boleng+'\n').encode())
                끝표시=('\r\n'+bontsha_Boleng+'\r\n').encode();받기(끝표시,dirisa)
                끝자리=rekota_mola.index(끝표시,dirisa)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return rekota_mola[dirisa:].decode('utf-8','replace').replace('\r\n','\n')
            def netefatsa(SMS,*값들):
                araba=setlhalosataelo(SMS)
                for Boleng in 값들:assert ipTestText(Boleng) in araba,(SMS,Boleng,araba)
                return araba
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    thuso_Boleng=netefatsa('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in Imeile_nngwe_Boleng.values():assert 별칭 in thuso_Boleng,(별칭,thuso_Boleng)
                    netefatsa(Imeile_nngwe_Boleng['help']+' system','Network / system')
                    netefatsa('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    netefatsa(Imeile_nngwe_Boleng['ipconfig'],'inet 10.0.2.15');netefatsa('ip addr show','sl0: UP');netefatsa('ifconfig','sl0: UP')
                    for Ga_e_a_siama_Diseting in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        phoso=netefatsa('ipconfig set '+Ga_e_a_siama_Diseting+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in phoso,phoso
                        netefatsa('ipconfig','inet 10.0.2.15')
                    netefatsa('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    netefatsa(Imeile_nngwe_Boleng['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    netefatsa('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    netefatsa('ip link set dev sl0 down','sl0: DOWN');netefatsa('ping -c 1 10.0.2.2; echo STATUS=$?','phoso -100','STATUS=1')
                    netefatsa('ipconfig up','sl0: UP')
                    netefatsa(Imeile_nngwe_Boleng['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    netefatsa('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    netefatsa('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');netefatsa(Imeile_nngwe_Boleng['route'],'10.0.2.2 sl0')
                    netefatsa('ftpd start','FTP listening')
                    netefatsa(Imeile_nngwe_Boleng['netstat'],'10.0.2.20:21','LISTEN');netefatsa('ss','LISTEN')
                    netefatsa('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','phoso -16')
                    with ftplib.FTP() as sedirelwa_Boleng:
                        sedirelwa_Boleng.connect('127.0.0.2',접속번호,timeout=20);sedirelwa_Boleng.login();tshedimosetso=b'Network address was changed in the guest.\n'
                        sedirelwa_Boleng.storbinary('STOR net-state.txt',io.BytesIO(tshedimosetso));받은자료=bytearray();sedirelwa_Boleng.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==tshedimosetso;sedirelwa_Boleng.delete('net-state.txt')
                    netefatsa('ftpd stop','FTP stopped');netefatsa('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    pego_Boleng['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(netefatsa('df','RAM only'));netefatsa('echo disk-proof > sys-state.txt');후=저장값(netefatsa(Imeile_nngwe_Boleng['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    netefatsa('rm sys-state.txt');assert 저장값(setlhalosataelo('df'))==전
                    memori_Boleng=netefatsa(Imeile_nngwe_Boleng['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',memori_Boleng).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    netefatsa(Imeile_nngwe_Boleng['ps'],'kernel/shell');netefatsa(Imeile_nngwe_Boleng['uptime'],'seconds')
                    kemo_tshedimosetso=netefatsa(Imeile_nngwe_Boleng['top']+' -n 2','kernel/shell');assert kemo_tshedimosetso.count('PID SLOT STATE')==2,kemo_tshedimosetso
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    netefatsa('terminal','TERMINAL READY');dirisa=len(rekota_mola);romela(b'vi process.txt\n');받기(b'NORMAL',dirisa)
                    dirisa=len(rekota_mola);romela(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',dirisa)
                    tsenyo_lenaane=netefatsa('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',tsenyo_lenaane);assert 찾음 and int(찾음.group(2))>0,tsenyo_lenaane
                    netefatsa('free','EL0 mapped KiB: '+찾음.group(2))
                    dirisa=len(rekota_mola);romela(b'top\n');받기(b'PID SLOT STATE',dirisa);romela(b'q');받기(b'jkoros-native> ',dirisa)
                    # Test a multibyte prefix through the real shell completion path.
                    if Imeile_nngwe_Boleng['df']!='df':
                        dirisa=len(rekota_mola);romela((Imeile_nngwe_Boleng['df'][:-1]+'\t\n').encode());받기(b'RAM only',dirisa);받기(b'jkoros-native> ',dirisa)
                    pego_Boleng['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as taolo_Boleng:
                    taolo_Boleng.settimeout(15);taolo_Boleng.connect(str(taolo_tsela));moela_Boleng=taolo_Boleng.makefile('rwb');json.loads(moela_Boleng.readline());moela_Boleng.write(b'{"execute":"qmp_capabilities"}\n');moela_Boleng.flush()
                    while 'return' not in json.loads(moela_Boleng.readline()):pass
                    romela((('poweroff' if 인수.poweroff_only else Imeile_nngwe_Boleng['poweroff'])+'\n').encode())
                    while True:
                        tiragalo=json.loads(moela_Boleng.readline())
                        if tiragalo.get('event')=='SHUTDOWN':break
                    assert tiragalo['data']['guest'] and tiragalo['data']['reason']=='guest-shutdown',tiragalo
                    assert Thulaganyo_Boleng.wait(timeout=15)==0
                    pego_Boleng['shutdown']=tiragalo;pego_Boleng['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                pego_Boleng['network_trace']=leborogo_Boleng.palo_tlhakanyo_rekota
                assert 인수.poweroff_only or any(tsenyo_Boleng['protocol']==1 and tsenyo_Boleng['direction']=='from_guest' for tsenyo_Boleng in leborogo_Boleng.palo_tlhakanyo_rekota)
                pego_Boleng['passed']=True
            finally:
                if Thulaganyo_Boleng.poll() is None:os.killpg(Thulaganyo_Boleng.pid,signal.SIGTERM)
                try:Thulaganyo_Boleng.wait(timeout=10)
                except subprocess.TimeoutExpired:Thulaganyo_Boleng.kill();Thulaganyo_Boleng.wait()
                tlhopha_selwana.close();(출력/'serial.log').write_bytes(rekota_mola);(출력/'report.json').write_text(json.dumps(pego_Boleng,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({taetsi_Boleng:Boleng for taetsi_Boleng,Boleng in pego_Boleng.items() if taetsi_Boleng!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':dirisa()
