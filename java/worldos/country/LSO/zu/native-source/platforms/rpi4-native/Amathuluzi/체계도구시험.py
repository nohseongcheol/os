#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane 자체 커널의 IP/ICMP, isimo_inani umbuzo_inani, 현지어 Umlayelo, 게스트 phuma_i_app qinisekisa."""
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


def Sebenzisa():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Izinhlelo={};igama_ithebula={}
    if 인수.edition:
        나라=인수.edition.resolve();Izinhlelo=json.loads((나라/'native.json').read_text());igama_ithebula=Izinhlelo['identifiers'];기준=나라/Izinhlelo['source']/Izinhlelo['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        singatha=나라/'host/qemu'
        if singatha.is_file():os.environ['QEMU_AARCH64']=str(singatha)
    Amathuluzi=기준/Path(Izinhlelo.get('runner','Amathuluzi/yenza_umyalo.py')).parent
    sys.path.insert(0,str(Amathuluzi))
    def Funda(Igama):
        Indlela_2=Amathuluzi/(igama_ithebula.get(Igama,Igama)+'.py');udaba_inani=importlib.util.spec_from_file_location('test_'+Igama,str(Indlela_2));모듈=importlib.util.module_from_spec(udaba_inani);udaba_inani.loader.exec_module(모듈);return 모듈
    실행모듈=Funda('yenza_umyalo');망모듈=Funda('iNethiwekhi_ibhuloho');Umlayelo=getattr(실행모듈,igama_ithebula.get('Umlayelo','Umlayelo'));ibhuloho_thayipha=getattr(망모듈,igama_ithebula.get('iNethiwekhi_ibhuloho','iNethiwekhi_ibhuloho'))
    isibizo_inani=Izinhlelo.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ikheli_le_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'khombisa_usizo'})
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
    umbiko_inani={'passed':False,'country':Izinhlelo.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    loga_umugqa=bytearray();UKULANDELANA_inani=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        isilawuli_umzila=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Bheka_inani:Bheka_inani.bind(('127.0.0.1',0));접속번호=Bheka_inani.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ibhuloho_thayipha(접속번호,thwebula=True,isivakashi_ikheli=ipTestText('10.0.2.20'),singatha_ikheli='127.0.0.2') as ibhuloho_inani:
            Inqubo_inani=subprocess.Popen(Umlayelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(isilawuli_umzila)]+ibhuloho_inani.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            khetha_utho=selectors.DefaultSelector();khetha_utho.register(Inqubo_inani.stdout,selectors.EVENT_READ)
            def 받기(khombisa_inani,Sebenzisa=0,제한=45):
                끝=time.monotonic()+제한
                while khombisa_inani not in loga_umugqa[Sebenzisa:]:
                    if time.monotonic()>끝 or Inqubo_inani.poll() is not None:raise AssertionError('Missing '+repr(khombisa_inani)+'\n'+loga_umugqa[Sebenzisa:].decode('utf-8','replace'))
                    for inkomba_inani,_ in khetha_utho.select(.1):
                        imininingwane=inkomba_inani.fileobj.read(65536)
                        if imininingwane:loga_umugqa.extend(imininingwane)
                return loga_umugqa[Sebenzisa:].decode('utf-8','replace').replace('\r\n','\n')
            def Thumela(imininingwane):Inqubo_inani.stdin.write(imininingwane);Inqubo_inani.stdin.flush()
            def isihumushi_miyalelo(Itekisi):
                Itekisi=ipTestText(Itekisi)
                print(umbiko_inani['country'],Itekisi,flush=True);UKULANDELANA_inani[0]+=1;khombisa_inani='__SYSTEM_DONE_'+str(UKULANDELANA_inani[0])+'__';Sebenzisa=len(loga_umugqa)
                Thumela((Itekisi+'; echo; echo '+khombisa_inani+'\n').encode())
                끝표시=('\r\n'+khombisa_inani+'\r\n').encode();받기(끝표시,Sebenzisa)
                끝자리=loga_umugqa.index(끝표시,Sebenzisa)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return loga_umugqa[Sebenzisa:].decode('utf-8','replace').replace('\r\n','\n')
            def qiniseka(Itekisi,*값들):
                phendula=isihumushi_miyalelo(Itekisi)
                for inani in 값들:assert ipTestText(inani) in phendula,(Itekisi,inani,phendula)
                return phendula
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    usizo_inani=qiniseka('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in isibizo_inani.values():assert 별칭 in usizo_inani,(별칭,usizo_inani)
                    qiniseka(isibizo_inani['help']+' system','Network / system')
                    qiniseka('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    qiniseka(isibizo_inani['ipconfig'],'inet 10.0.2.15');qiniseka('ip addr show','sl0: UP');qiniseka('ifconfig','sl0: UP')
                    for akusikho_Amasethingi in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Iphutha=qiniseka('ipconfig set '+akusikho_Amasethingi+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Iphutha,Iphutha
                        qiniseka('ipconfig','inet 10.0.2.15')
                    qiniseka('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    qiniseka(isibizo_inani['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    qiniseka('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    qiniseka('ip link set dev sl0 down','sl0: DOWN');qiniseka('ping -c 1 10.0.2.2; echo STATUS=$?','Iphutha -100','STATUS=1')
                    qiniseka('ipconfig up','sl0: UP')
                    qiniseka(isibizo_inani['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    qiniseka('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    qiniseka('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');qiniseka(isibizo_inani['route'],'10.0.2.2 sl0')
                    qiniseka('ftpd start','FTP listening')
                    qiniseka(isibizo_inani['netstat'],'10.0.2.20:21','LISTEN');qiniseka('ss','LISTEN')
                    qiniseka('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Iphutha -16')
                    with ftplib.FTP() as iklayenti_inani:
                        iklayenti_inani.connect('127.0.0.2',접속번호,timeout=20);iklayenti_inani.login();imininingwane=b'Network address was changed in the guest.\n'
                        iklayenti_inani.storbinary('STOR net-state.txt',io.BytesIO(imininingwane));받은자료=bytearray();iklayenti_inani.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==imininingwane;iklayenti_inani.delete('net-state.txt')
                    qiniseka('ftpd stop','FTP stopped');qiniseka('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    umbiko_inani['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Itekisi):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Itekisi);assert 찾음,Itekisi;return tuple(map(int,찾음.groups()))
                    전=저장값(qiniseka('df','RAM only'));qiniseka('echo disk-proof > sys-state.txt');후=저장값(qiniseka(isibizo_inani['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    qiniseka('rm sys-state.txt');assert 저장값(isihumushi_miyalelo('df'))==전
                    inkumbulo_inani=qiniseka(isibizo_inani['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',inkumbulo_inani).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    qiniseka(isibizo_inani['ps'],'kernel/shell');qiniseka(isibizo_inani['uptime'],'seconds')
                    isimo_ulwazi=qiniseka(isibizo_inani['top']+' -n 2','kernel/shell');assert isimo_ulwazi.count('PID SLOT STATE')==2,isimo_ulwazi
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    qiniseka('terminal','TERMINAL READY');Sebenzisa=len(loga_umugqa);Thumela(b'vi process.txt\n');받기(b'NORMAL',Sebenzisa)
                    Sebenzisa=len(loga_umugqa);Thumela(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Sebenzisa)
                    okufakwayo_Uhlu=qiniseka('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',okufakwayo_Uhlu);assert 찾음 and int(찾음.group(2))>0,okufakwayo_Uhlu
                    qiniseka('free','EL0 mapped KiB: '+찾음.group(2))
                    Sebenzisa=len(loga_umugqa);Thumela(b'top\n');받기(b'PID SLOT STATE',Sebenzisa);Thumela(b'q');받기(b'jkoros-native> ',Sebenzisa)
                    # Test a multibyte prefix through the real shell completion path.
                    if isibizo_inani['df']!='df':
                        Sebenzisa=len(loga_umugqa);Thumela((isibizo_inani['df'][:-1]+'\t\n').encode());받기(b'RAM only',Sebenzisa);받기(b'jkoros-native> ',Sebenzisa)
                    umbiko_inani['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as isilawuli_inani:
                    isilawuli_inani.settimeout(15);isilawuli_inani.connect(str(isilawuli_umzila));Stream_inani=isilawuli_inani.makefile('rwb');json.loads(Stream_inani.readline());Stream_inani.write(b'{"execute":"qmp_capabilities"}\n');Stream_inani.flush()
                    while 'return' not in json.loads(Stream_inani.readline()):pass
                    Thumela((('poweroff' if 인수.poweroff_only else isibizo_inani['poweroff'])+'\n').encode())
                    while True:
                        isigameko=json.loads(Stream_inani.readline())
                        if isigameko.get('event')=='SHUTDOWN':break
                    assert isigameko['data']['guest'] and isigameko['data']['reason']=='guest-shutdown',isigameko
                    assert Inqubo_inani.wait(timeout=15)==0
                    umbiko_inani['shutdown']=isigameko;umbiko_inani['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                umbiko_inani['network_trace']=ibhuloho_inani.ithreyisi_loga
                assert 인수.poweroff_only or any(okufakwayo_inani['protocol']==1 and okufakwayo_inani['direction']=='from_guest' for okufakwayo_inani in ibhuloho_inani.ithreyisi_loga)
                umbiko_inani['passed']=True
            finally:
                if Inqubo_inani.poll() is None:os.killpg(Inqubo_inani.pid,signal.SIGTERM)
                try:Inqubo_inani.wait(timeout=10)
                except subprocess.TimeoutExpired:Inqubo_inani.kill();Inqubo_inani.wait()
                khetha_utho.close();(출력/'serial.log').write_bytes(loga_umugqa);(출력/'report.json').write_text(json.dumps(umbiko_inani,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({inkomba_inani:inani for inkomba_inani,inani in umbiko_inani.items() if inkomba_inani!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Sebenzisa()
