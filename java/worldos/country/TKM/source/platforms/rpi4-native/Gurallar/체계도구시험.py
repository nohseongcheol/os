#!/usr/bin/env python3
"""hakyky_maglumat 자체 커널의 IP/ICMP, ýagdaý_baha talap_baha, 현지어 buýruk, 게스트 çyk_programma tassykla."""
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


def Bitir():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Düzümler={};at_tablisa={}
    if 인수.edition:
        나라=인수.edition.resolve();Düzümler=json.loads((나라/'native.json').read_text());at_tablisa=Düzümler['identifiers'];기준=나라/Düzümler['source']/Düzümler['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        esasy=나라/'host/qemu'
        if esasy.is_file():os.environ['QEMU_AARCH64']=str(esasy)
    Gurallar=기준/Path(Düzümler.get('runner','Gurallar/ýerine_ýetir_buýruk.py')).parent
    sys.path.insert(0,str(Gurallar))
    def Oka(Ad):
        Ýol=Gurallar/(at_tablisa.get(Ad,Ad)+'.py');ýumuş_baha_102996da=importlib.util.spec_from_file_location('test_'+Ad,str(Ýol));모듈=importlib.util.module_from_spec(ýumuş_baha_102996da);ýumuş_baha_102996da.loader.exec_module(모듈);return 모듈
    실행모듈=Oka('ýerine_ýetir_buýruk');망모듈=Oka('통신다리');buýruk=getattr(실행모듈,at_tablisa.get('buýruk','buýruk'));다리형=getattr(망모듈,at_tablisa.get('통신다리','통신다리'))
    lakam_baha=Düzümler.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_salgy','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'görkez_kömek'})
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
    hasabat_baha={'passed':False,'country':Düzümler.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    hasaba_alyş_setir=bytearray();SEQUENCE_baha=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        dolandyryş_ýol=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as gözle_baha:gözle_baha.bind(('127.0.0.1',0));접속번호=gözle_baha.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,düşüriş=True,게스트주소=ipTestText('10.0.2.20'),esasy_salgy='127.0.0.2') as 다리:
            Proses_baha=subprocess.Popen(buýruk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(dolandyryş_ýol)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            saýlap_al_element=selectors.DefaultSelector();saýlap_al_element.register(Proses_baha.stdout,selectors.EVENT_READ)
            def 받기(görkez_baha_487749b8,Bitir=0,제한=45):
                끝=time.monotonic()+제한
                while görkez_baha_487749b8 not in hasaba_alyş_setir[Bitir:]:
                    if time.monotonic()>끝 or Proses_baha.poll() is not None:raise AssertionError('Missing '+repr(görkez_baha_487749b8)+'\n'+hasaba_alyş_setir[Bitir:].decode('utf-8','replace'))
                    for açar_baha,_ in saýlap_al_element.select(.1):
                        maglumat=açar_baha.fileobj.read(65536)
                        if maglumat:hasaba_alyş_setir.extend(maglumat)
                return hasaba_alyş_setir[Bitir:].decode('utf-8','replace').replace('\r\n','\n')
            def iber(maglumat):Proses_baha.stdin.write(maglumat);Proses_baha.stdin.flush()
            def gabyjak(Metin):
                Metin=ipTestText(Metin)
                print(hasabat_baha['country'],Metin,flush=True);SEQUENCE_baha[0]+=1;görkez_baha_487749b8='__SYSTEM_DONE_'+str(SEQUENCE_baha[0])+'__';Bitir=len(hasaba_alyş_setir)
                iber((Metin+'; echo; echo '+görkez_baha_487749b8+'\n').encode())
                끝표시=('\r\n'+görkez_baha_487749b8+'\r\n').encode();받기(끝표시,Bitir)
                끝자리=hasaba_alyş_setir.index(끝표시,Bitir)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return hasaba_alyş_setir[Bitir:].decode('utf-8','replace').replace('\r\n','\n')
            def barla(Metin,*값들):
                jogap_bermek=gabyjak(Metin)
                for baha in 값들:assert ipTestText(baha) in jogap_bermek,(Metin,baha,jogap_bermek)
                return jogap_bermek
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    kömek_baha=barla('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in lakam_baha.values():assert 별칭 in kömek_baha,(별칭,kömek_baha)
                    barla(lakam_baha['help']+' system','Network / system')
                    barla('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    barla(lakam_baha['ipconfig'],'inet 10.0.2.15');barla('ip addr show','sl0: UP');barla('ifconfig','sl0: UP')
                    for nädogry_Sazlamalar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Hata=barla('ipconfig set '+nädogry_Sazlamalar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Hata,Hata
                        barla('ipconfig','inet 10.0.2.15')
                    barla('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    barla(lakam_baha['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    barla('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    barla('ip link set dev sl0 down','sl0: DOWN');barla('ping -c 1 10.0.2.2; echo STATUS=$?','Hata -100','STATUS=1')
                    barla('ipconfig up','sl0: UP')
                    barla(lakam_baha['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    barla('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    barla('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');barla(lakam_baha['route'],'10.0.2.2 sl0')
                    barla('ftpd start','FTP listening')
                    barla(lakam_baha['netstat'],'10.0.2.20:21','LISTEN');barla('ss','LISTEN')
                    barla('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Hata -16')
                    with ftplib.FTP() as müşderi_baha:
                        müşderi_baha.connect('127.0.0.2',접속번호,timeout=20);müşderi_baha.login();maglumat=b'Network address was changed in the guest.\n'
                        müşderi_baha.storbinary('STOR net-state.txt',io.BytesIO(maglumat));받은자료=bytearray();müşderi_baha.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==maglumat;müşderi_baha.delete('net-state.txt')
                    barla('ftpd stop','FTP stopped');barla('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    hasabat_baha['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Metin):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Metin);assert 찾음,Metin;return tuple(map(int,찾음.groups()))
                    전=저장값(barla('df','RAM only'));barla('echo disk-proof > sys-state.txt');후=저장값(barla(lakam_baha['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    barla('rm sys-state.txt');assert 저장값(gabyjak('df'))==전
                    ýat_baha=barla(lakam_baha['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ýat_baha).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    barla(lakam_baha['ps'],'kernel/shell');barla(lakam_baha['uptime'],'seconds')
                    ýagdaý_maglumat=barla(lakam_baha['top']+' -n 2','kernel/shell');assert ýagdaý_maglumat.count('PID SLOT STATE')==2,ýagdaý_maglumat
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    barla('terminal','TERMINAL READY');Bitir=len(hasaba_alyş_setir);iber(b'vi process.txt\n');받기(b'NORMAL',Bitir)
                    Bitir=len(hasaba_alyş_setir);iber(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Bitir)
                    girizmeklik_Sanaw=barla('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',girizmeklik_Sanaw);assert 찾음 and int(찾음.group(2))>0,girizmeklik_Sanaw
                    barla('free','EL0 mapped KiB: '+찾음.group(2))
                    Bitir=len(hasaba_alyş_setir);iber(b'top\n');받기(b'PID SLOT STATE',Bitir);iber(b'q');받기(b'jkoros-native> ',Bitir)
                    # Test a multibyte prefix through the real shell completion path.
                    if lakam_baha['df']!='df':
                        Bitir=len(hasaba_alyş_setir);iber((lakam_baha['df'][:-1]+'\t\n').encode());받기(b'RAM only',Bitir);받기(b'jkoros-native> ',Bitir)
                    hasabat_baha['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as dolandyryş_baha:
                    dolandyryş_baha.settimeout(15);dolandyryş_baha.connect(str(dolandyryş_ýol));Stream_baha=dolandyryş_baha.makefile('rwb');json.loads(Stream_baha.readline());Stream_baha.write(b'{"execute":"qmp_capabilities"}\n');Stream_baha.flush()
                    while 'return' not in json.loads(Stream_baha.readline()):pass
                    iber((('poweroff' if 인수.poweroff_only else lakam_baha['poweroff'])+'\n').encode())
                    while True:
                        waka=json.loads(Stream_baha.readline())
                        if waka.get('event')=='SHUTDOWN':break
                    assert waka['data']['guest'] and waka['data']['reason']=='guest-shutdown',waka
                    assert Proses_baha.wait(timeout=15)==0
                    hasabat_baha['shutdown']=waka;hasabat_baha['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                hasabat_baha['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(girizmeklik_baha['protocol']==1 and girizmeklik_baha['direction']=='from_guest' for girizmeklik_baha in 다리.추적기록)
                hasabat_baha['passed']=True
            finally:
                if Proses_baha.poll() is None:os.killpg(Proses_baha.pid,signal.SIGTERM)
                try:Proses_baha.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_baha.kill();Proses_baha.wait()
                saýlap_al_element.close();(출력/'serial.log').write_bytes(hasaba_alyş_setir);(출력/'report.json').write_text(json.dumps(hasabat_baha,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({açar_baha:baha for açar_baha,baha in hasabat_baha.items() if açar_baha!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Bitir()
