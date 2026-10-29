#!/usr/bin/env python3
"""liteew_mbir 자체 커널의 IP/ICMP, nekkin_xëyma laaj_xëyma, 현지어 ndigel, 게스트 Génn_jëfekaay wéral."""
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


def daw():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Jekkal_yi={};tur_àlluwa={}
    if 인수.edition:
        나라=인수.edition.resolve();Jekkal_yi=json.loads((나라/'native.json').read_text());tur_àlluwa=Jekkal_yi['identifiers'];기준=나라/Jekkal_yi['source']/Jekkal_yi['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        dalal=나라/'host/qemu'
        if dalal.is_file():os.environ['QEMU_AARCH64']=str(dalal)
    Jumtukaay_yi=기준/Path(Jekkal_yi.get('runner','Jumtukaay_yi/def_ndigel.py')).parent
    sys.path.insert(0,str(Jumtukaay_yi))
    def 읽기(tur_253d1510):
        Yoonu_jëmale=Jumtukaay_yi/(tur_àlluwa.get(tur_253d1510,tur_253d1510)+'.py');ay_xëyma=importlib.util.spec_from_file_location('test_'+tur_253d1510,str(Yoonu_jëmale));모듈=importlib.util.module_from_spec(ay_xëyma);ay_xëyma.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('def_ndigel');망모듈=읽기('mbaal_poŋ');ndigel=getattr(실행모듈,tur_àlluwa.get('ndigel','ndigel'));poŋ_xeet=getattr(망모듈,tur_àlluwa.get('mbaal_poŋ','mbaal_poŋ'))
    Teggi_xëyma_0a38607b=Jekkal_yi.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'dëkkuwaayu_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'féeñal_ndimbal'})
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
    tënk_xëyma={'passed':False,'country':Jekkal_yi.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    làq_Dënk=bytearray();SEQUENCE_xëyma=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        Saytu_doxinu_ordinateur_Yoonu_jëmale=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Wut_xëyma:Wut_xëyma.bind(('127.0.0.1',0));접속번호=Wut_xëyma.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with poŋ_xeet(접속번호,jël=True,gan_dëkkuwaay=ipTestText('10.0.2.20'),dalal_dëkkuwaay='127.0.0.2') as poŋ_xëyma:
            yokkute_xëyma=subprocess.Popen(ndigel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(Saytu_doxinu_ordinateur_Yoonu_jëmale)]+poŋ_xëyma.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            Tànn_ëmbeef=selectors.DefaultSelector();Tànn_ëmbeef.register(yokkute_xëyma.stdout,selectors.EVENT_READ)
            def 받기(féeñal_xëyma,daw=0,제한=45):
                끝=time.monotonic()+제한
                while féeñal_xëyma not in làq_Dënk[daw:]:
                    if time.monotonic()>끝 or yokkute_xëyma.poll() is not None:raise AssertionError('Missing '+repr(féeñal_xëyma)+'\n'+làq_Dënk[daw:].decode('utf-8','replace'))
                    for kër_xëyma,_ in Tànn_ëmbeef.select(.1):
                        mbir=kër_xëyma.fileobj.read(65536)
                        if mbir:làq_Dënk.extend(mbir)
                return làq_Dënk[daw:].decode('utf-8','replace').replace('\r\n','\n')
            def Yónnee(mbir):yokkute_xëyma.stdin.write(mbir);yokkute_xëyma.stdin.flush()
            def Wëreef(Tekst):
                Tekst=ipTestText(Tekst)
                print(tënk_xëyma['country'],Tekst,flush=True);SEQUENCE_xëyma[0]+=1;féeñal_xëyma='__SYSTEM_DONE_'+str(SEQUENCE_xëyma[0])+'__';daw=len(làq_Dënk)
                Yónnee((Tekst+'; echo; echo '+féeñal_xëyma+'\n').encode())
                끝표시=('\r\n'+féeñal_xëyma+'\r\n').encode();받기(끝표시,daw)
                끝자리=làq_Dënk.index(끝표시,daw)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return làq_Dënk[daw:].decode('utf-8','replace').replace('\r\n','\n')
            def luñutu(Tekst,*값들):
                tontu=Wëreef(Tekst)
                for xëyma in 값들:assert ipTestText(xëyma) in tontu,(Tekst,xëyma,tontu)
                return tontu
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ndimbal_xëyma=luñutu('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in Teggi_xëyma_0a38607b.values():assert 별칭 in ndimbal_xëyma,(별칭,ndimbal_xëyma)
                    luñutu(Teggi_xëyma_0a38607b['help']+' system','Network / system')
                    luñutu('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    luñutu(Teggi_xëyma_0a38607b['ipconfig'],'inet 10.0.2.15');luñutu('ip addr show','sl0: UP');luñutu('ifconfig','sl0: UP')
                    for baaxul_Jekkal_yi in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        njumte=luñutu('ipconfig set '+baaxul_Jekkal_yi+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in njumte,njumte
                        luñutu('ipconfig','inet 10.0.2.15')
                    luñutu('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    luñutu(Teggi_xëyma_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    luñutu('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    luñutu('ip link set dev sl0 down','sl0: DOWN');luñutu('ping -c 1 10.0.2.2; echo STATUS=$?','njumte -100','STATUS=1')
                    luñutu('ipconfig up','sl0: UP')
                    luñutu(Teggi_xëyma_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    luñutu('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    luñutu('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');luñutu(Teggi_xëyma_0a38607b['route'],'10.0.2.2 sl0')
                    luñutu('ftpd start','FTP listening')
                    luñutu(Teggi_xëyma_0a38607b['netstat'],'10.0.2.20:21','LISTEN');luñutu('ss','LISTEN')
                    luñutu('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','njumte -16')
                    with ftplib.FTP() as lëkkalekat_xëyma:
                        lëkkalekat_xëyma.connect('127.0.0.2',접속번호,timeout=20);lëkkalekat_xëyma.login();mbir=b'Network address was changed in the guest.\n'
                        lëkkalekat_xëyma.storbinary('STOR net-state.txt',io.BytesIO(mbir));받은자료=bytearray();lëkkalekat_xëyma.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==mbir;lëkkalekat_xëyma.delete('net-state.txt')
                    luñutu('ftpd stop','FTP stopped');luñutu('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    tënk_xëyma['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(luñutu('df','RAM only'));luñutu('echo disk-proof > sys-state.txt');후=저장값(luñutu(Teggi_xëyma_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    luñutu('rm sys-state.txt');assert 저장값(Wëreef('df'))==전
                    fatlekookaay_xëyma=luñutu(Teggi_xëyma_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',fatlekookaay_xëyma).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    luñutu(Teggi_xëyma_0a38607b['ps'],'kernel/shell');luñutu(Teggi_xëyma_0a38607b['uptime'],'seconds')
                    nekkin_yëglë=luñutu(Teggi_xëyma_0a38607b['top']+' -n 2','kernel/shell');assert nekkin_yëglë.count('PID SLOT STATE')==2,nekkin_yëglë
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    luñutu('terminal','TERMINAL READY');daw=len(làq_Dënk);Yónnee(b'vi process.txt\n');받기(b'NORMAL',daw)
                    daw=len(làq_Dënk);Yónnee(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',daw)
                    dugal_xabaar_lim=luñutu('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',dugal_xabaar_lim);assert 찾음 and int(찾음.group(2))>0,dugal_xabaar_lim
                    luñutu('free','EL0 mapped KiB: '+찾음.group(2))
                    daw=len(làq_Dënk);Yónnee(b'top\n');받기(b'PID SLOT STATE',daw);Yónnee(b'q');받기(b'jkoros-native> ',daw)
                    # Test a multibyte prefix through the real shell completion path.
                    if Teggi_xëyma_0a38607b['df']!='df':
                        daw=len(làq_Dënk);Yónnee((Teggi_xëyma_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',daw);받기(b'jkoros-native> ',daw)
                    tënk_xëyma['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as Saytu_doxinu_ordinateur_xëyma:
                    Saytu_doxinu_ordinateur_xëyma.settimeout(15);Saytu_doxinu_ordinateur_xëyma.connect(str(Saytu_doxinu_ordinateur_Yoonu_jëmale));dawal_xëyma=Saytu_doxinu_ordinateur_xëyma.makefile('rwb');json.loads(dawal_xëyma.readline());dawal_xëyma.write(b'{"execute":"qmp_capabilities"}\n');dawal_xëyma.flush()
                    while 'return' not in json.loads(dawal_xëyma.readline()):pass
                    Yónnee((('poweroff' if 인수.poweroff_only else Teggi_xëyma_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        xewxew=json.loads(dawal_xëyma.readline())
                        if xewxew.get('event')=='SHUTDOWN':break
                    assert xewxew['data']['guest'] and xewxew['data']['reason']=='guest-shutdown',xewxew
                    assert yokkute_xëyma.wait(timeout=15)==0
                    tënk_xëyma['shutdown']=xewxew;tënk_xëyma['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                tënk_xëyma['network_trace']=poŋ_xëyma.추적기록
                assert 인수.poweroff_only or any(dugal_xabaar_xëyma['protocol']==1 and dugal_xabaar_xëyma['direction']=='from_guest' for dugal_xabaar_xëyma in poŋ_xëyma.추적기록)
                tënk_xëyma['passed']=True
            finally:
                if yokkute_xëyma.poll() is None:os.killpg(yokkute_xëyma.pid,signal.SIGTERM)
                try:yokkute_xëyma.wait(timeout=10)
                except subprocess.TimeoutExpired:yokkute_xëyma.kill();yokkute_xëyma.wait()
                Tànn_ëmbeef.close();(출력/'serial.log').write_bytes(làq_Dënk);(출력/'report.json').write_text(json.dumps(tënk_xëyma,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({kër_xëyma:xëyma for kër_xëyma,xëyma in tënk_xëyma.items() if kër_xëyma!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':daw()
