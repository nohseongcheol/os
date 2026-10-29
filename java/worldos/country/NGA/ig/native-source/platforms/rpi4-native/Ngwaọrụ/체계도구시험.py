#!/usr/bin/env python3
"""ǹdịnezie_datà 자체 커널의 IP/ICMP, ọnọdụ_valuu mgbaajụjụ_valuu, 현지어 Ntiiwu, 게스트 pụọ_app mee_ịbanihe."""
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


def Bido():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Mwube={};akara_ahà_tebùl={}
    if 인수.edition:
        나라=인수.edition.resolve();Mwube=json.loads((나라/'native.json').read_text());akara_ahà_tebùl=Mwube['identifiers'];기준=나라/Mwube['source']/Mwube['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        usu=나라/'host/qemu'
        if usu.is_file():os.environ['QEMU_AARCH64']=str(usu)
    Ngwaọrụ=기준/Path(Mwube.get('runner','Ngwaọrụ/mee_nnyemiwu.py')).parent
    sys.path.insert(0,str(Ngwaọrụ))
    def Wepụta_ọzi(Aha):
        ụzọ_ozi=Ngwaọrụ/(akara_ahà_tebùl.get(Aha,Aha)+'.py');ngō_valuu=importlib.util.spec_from_file_location('test_'+Aha,str(ụzọ_ozi));모듈=importlib.util.module_from_spec(ngō_valuu);ngō_valuu.loader.exec_module(모듈);return 모듈
    실행모듈=Wepụta_ọzi('mee_nnyemiwu');망모듈=Wepụta_ọzi('통신다리');Ntiiwu=getattr(실행모듈,akara_ahà_tebùl.get('Ntiiwu','Ntiiwu'));다리형=getattr(망모듈,akara_ahà_tebùl.get('통신다리','통신다리'))
    ahaọzọ_valuu=Mwube.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adreèsì_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'gòsi_ènyèmaka'})
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
    akụkọ_valuu={'passed':False,'country':Mwube.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ndekọ_NDEKỌ=bytearray();NSOTANSO_valuu=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        njizi_ụzọ_ozi=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Chọọ_valuu:Chọọ_valuu.bind(('127.0.0.1',0));접속번호=Chọọ_valuu.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,See=True,게스트주소=ipTestText('10.0.2.20'),usu_àdreèsì='127.0.0.2') as 다리:
            ùsòrò_valuu_6712bde7=subprocess.Popen(Ntiiwu()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(njizi_ụzọ_ozi)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            họrọ_ihe=selectors.DefaultSelector();họrọ_ihe.register(ùsòrò_valuu_6712bde7.stdout,selectors.EVENT_READ)
            def 받기(gòsi_valuu,Bido=0,제한=45):
                끝=time.monotonic()+제한
                while gòsi_valuu not in ndekọ_NDEKỌ[Bido:]:
                    if time.monotonic()>끝 or ùsòrò_valuu_6712bde7.poll() is not None:raise AssertionError('Missing '+repr(gòsi_valuu)+'\n'+ndekọ_NDEKỌ[Bido:].decode('utf-8','replace'))
                    for ọtụgwo_valuu,_ in họrọ_ihe.select(.1):
                        datà=ọtụgwo_valuu.fileobj.read(65536)
                        if datà:ndekọ_NDEKỌ.extend(datà)
                return ndekọ_NDEKỌ[Bido:].decode('utf-8','replace').replace('\r\n','\n')
            def zìga(datà):ùsòrò_valuu_6712bde7.stdin.write(datà);ùsòrò_valuu_6712bde7.stdin.flush()
            def nkọwannyemiwu(SMS):
                SMS=ipTestText(SMS)
                print(akụkọ_valuu['country'],SMS,flush=True);NSOTANSO_valuu[0]+=1;gòsi_valuu='__SYSTEM_DONE_'+str(NSOTANSO_valuu[0])+'__';Bido=len(ndekọ_NDEKỌ)
                zìga((SMS+'; echo; echo '+gòsi_valuu+'\n').encode())
                끝표시=('\r\n'+gòsi_valuu+'\r\n').encode();받기(끝표시,Bido)
                끝자리=ndekọ_NDEKỌ.index(끝표시,Bido)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return ndekọ_NDEKỌ[Bido:].decode('utf-8','replace').replace('\r\n','\n')
            def nkwàdo_eziokwū(SMS,*값들):
                nzaghachi=nkọwannyemiwu(SMS)
                for valuu in 값들:assert ipTestText(valuu) in nzaghachi,(SMS,valuu,nzaghachi)
                return nzaghachi
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ènyèmaka_valuu=nkwàdo_eziokwū('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ahaọzọ_valuu.values():assert 별칭 in ènyèmaka_valuu,(별칭,ènyèmaka_valuu)
                    nkwàdo_eziokwū(ahaọzọ_valuu['help']+' system','Network / system')
                    nkwàdo_eziokwū('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    nkwàdo_eziokwū(ahaọzọ_valuu['ipconfig'],'inet 10.0.2.15');nkwàdo_eziokwū('ip addr show','sl0: UP');nkwàdo_eziokwū('ifconfig','sl0: UP')
                    for abànihe_Mwube in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        mmejọ=nkwàdo_eziokwū('ipconfig set '+abànihe_Mwube+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in mmejọ,mmejọ
                        nkwàdo_eziokwū('ipconfig','inet 10.0.2.15')
                    nkwàdo_eziokwū('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    nkwàdo_eziokwū(ahaọzọ_valuu['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    nkwàdo_eziokwū('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    nkwàdo_eziokwū('ip link set dev sl0 down','sl0: DOWN');nkwàdo_eziokwū('ping -c 1 10.0.2.2; echo STATUS=$?','mmejọ -100','STATUS=1')
                    nkwàdo_eziokwū('ipconfig up','sl0: UP')
                    nkwàdo_eziokwū(ahaọzọ_valuu['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    nkwàdo_eziokwū('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    nkwàdo_eziokwū('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');nkwàdo_eziokwū(ahaọzọ_valuu['route'],'10.0.2.2 sl0')
                    nkwàdo_eziokwū('ftpd start','FTP listening')
                    nkwàdo_eziokwū(ahaọzọ_valuu['netstat'],'10.0.2.20:21','LISTEN');nkwàdo_eziokwū('ss','LISTEN')
                    nkwàdo_eziokwū('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','mmejọ -16')
                    with ftplib.FTP() as klayènt_valuu:
                        klayènt_valuu.connect('127.0.0.2',접속번호,timeout=20);klayènt_valuu.login();datà=b'Network address was changed in the guest.\n'
                        klayènt_valuu.storbinary('STOR net-state.txt',io.BytesIO(datà));받은자료=bytearray();klayènt_valuu.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==datà;klayènt_valuu.delete('net-state.txt')
                    nkwàdo_eziokwū('ftpd stop','FTP stopped');nkwàdo_eziokwū('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    akụkọ_valuu['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(nkwàdo_eziokwū('df','RAM only'));nkwàdo_eziokwū('echo disk-proof > sys-state.txt');후=저장값(nkwàdo_eziokwū(ahaọzọ_valuu['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    nkwàdo_eziokwū('rm sys-state.txt');assert 저장값(nkọwannyemiwu('df'))==전
                    memọrị_valuu=nkwàdo_eziokwū(ahaọzọ_valuu['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',memọrị_valuu).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    nkwàdo_eziokwū(ahaọzọ_valuu['ps'],'kernel/shell');nkwàdo_eziokwū(ahaọzọ_valuu['uptime'],'seconds')
                    ọnọdụ_ozi=nkwàdo_eziokwū(ahaọzọ_valuu['top']+' -n 2','kernel/shell');assert ọnọdụ_ozi.count('PID SLOT STATE')==2,ọnọdụ_ozi
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    nkwàdo_eziokwū('terminal','TERMINAL READY');Bido=len(ndekọ_NDEKỌ);zìga(b'vi process.txt\n');받기(b'NORMAL',Bido)
                    Bido=len(ndekọ_NDEKỌ);zìga(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Bido)
                    ndebà_ndepụta=nkwàdo_eziokwū('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ndebà_ndepụta);assert 찾음 and int(찾음.group(2))>0,ndebà_ndepụta
                    nkwàdo_eziokwū('free','EL0 mapped KiB: '+찾음.group(2))
                    Bido=len(ndekọ_NDEKỌ);zìga(b'top\n');받기(b'PID SLOT STATE',Bido);zìga(b'q');받기(b'jkoros-native> ',Bido)
                    # Test a multibyte prefix through the real shell completion path.
                    if ahaọzọ_valuu['df']!='df':
                        Bido=len(ndekọ_NDEKỌ);zìga((ahaọzọ_valuu['df'][:-1]+'\t\n').encode());받기(b'RAM only',Bido);받기(b'jkoros-native> ',Bido)
                    akụkọ_valuu['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as njizi_valuu:
                    njizi_valuu.settimeout(15);njizi_valuu.connect(str(njizi_ụzọ_ozi));agịrị_valuu=njizi_valuu.makefile('rwb');json.loads(agịrị_valuu.readline());agịrị_valuu.write(b'{"execute":"qmp_capabilities"}\n');agịrị_valuu.flush()
                    while 'return' not in json.loads(agịrị_valuu.readline()):pass
                    zìga((('poweroff' if 인수.poweroff_only else ahaọzọ_valuu['poweroff'])+'\n').encode())
                    while True:
                        mmèrème=json.loads(agịrị_valuu.readline())
                        if mmèrème.get('event')=='SHUTDOWN':break
                    assert mmèrème['data']['guest'] and mmèrème['data']['reason']=='guest-shutdown',mmèrème
                    assert ùsòrò_valuu_6712bde7.wait(timeout=15)==0
                    akụkọ_valuu['shutdown']=mmèrème;akụkọ_valuu['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                akụkọ_valuu['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(ndebà_valuu['protocol']==1 and ndebà_valuu['direction']=='from_guest' for ndebà_valuu in 다리.추적기록)
                akụkọ_valuu['passed']=True
            finally:
                if ùsòrò_valuu_6712bde7.poll() is None:os.killpg(ùsòrò_valuu_6712bde7.pid,signal.SIGTERM)
                try:ùsòrò_valuu_6712bde7.wait(timeout=10)
                except subprocess.TimeoutExpired:ùsòrò_valuu_6712bde7.kill();ùsòrò_valuu_6712bde7.wait()
                họrọ_ihe.close();(출력/'serial.log').write_bytes(ndekọ_NDEKỌ);(출력/'report.json').write_text(json.dumps(akụkọ_valuu,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ọtụgwo_valuu:valuu for ọtụgwo_valuu,valuu in akụkọ_valuu.items() if ọtụgwo_valuu!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Bido()
