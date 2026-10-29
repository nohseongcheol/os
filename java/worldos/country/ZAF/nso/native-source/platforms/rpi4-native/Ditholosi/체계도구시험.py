#!/usr/bin/env python3
"""kgonthe_data 자체 커널의 IP/ICMP, boemo_boleng kwiri_boleng, 현지어 Taelo, 게스트 Etšwa_tirišo kgonthiša_5fb2b747."""
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


def Diriša():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Dipeakanyo={};leina_tafola={}
    if 인수.edition:
        나라=인수.edition.resolve();Dipeakanyo=json.loads((나라/'native.json').read_text());leina_tafola=Dipeakanyo['identifiers'];기준=나라/Dipeakanyo['source']/Dipeakanyo['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        go_nea_ditirelo=나라/'host/qemu'
        if go_nea_ditirelo.is_file():os.environ['QEMU_AARCH64']=str(go_nea_ditirelo)
    Ditholosi=기준/Path(Dipeakanyo.get('runner','Ditholosi/phethagatša_taelo.py')).parent
    sys.path.insert(0,str(Ditholosi))
    def Bala(Leina):
        Tsejana=Ditholosi/(leina_tafola.get(Leina,Leina)+'.py');taba_boleng=importlib.util.spec_from_file_location('test_'+Leina,str(Tsejana));모듈=importlib.util.module_from_spec(taba_boleng);taba_boleng.loader.exec_module(모듈);return 모듈
    실행모듈=Bala('phethagatša_taelo');망모듈=Bala('Netweke_kgokaganyo');Taelo=getattr(실행모듈,leina_tafola.get('Taelo','Taelo'));kgokaganyo_thaepa=getattr(망모듈,leina_tafola.get('Netweke_kgokaganyo','Netweke_kgokaganyo'))
    aliase_boleng=Dipeakanyo.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'atrese_ya_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'bontšha_thušo'})
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
    pego_boleng={'passed':False,'country':Dipeakanyo.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    pego_rei=bytearray();TATELANO_boleng=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        taolo_tsela=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Nyaka_boleng:Nyaka_boleng.bind(('127.0.0.1',0));접속번호=Nyaka_boleng.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with kgokaganyo_thaepa(접속번호,tšea=True,moeng_atrese=ipTestText('10.0.2.20'),go_nea_ditirelo_atrese='127.0.0.2') as kgokaganyo_boleng_982037b1:
            tiragalo_boleng=subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(taolo_tsela)]+kgokaganyo_boleng_982037b1.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            kgetha_aetheme=selectors.DefaultSelector();kgetha_aetheme.register(tiragalo_boleng.stdout,selectors.EVENT_READ)
            def 받기(bontšha_boleng,Diriša=0,제한=45):
                끝=time.monotonic()+제한
                while bontšha_boleng not in pego_rei[Diriša:]:
                    if time.monotonic()>끝 or tiragalo_boleng.poll() is not None:raise AssertionError('Missing '+repr(bontšha_boleng)+'\n'+pego_rei[Diriša:].decode('utf-8','replace'))
                    for khii_boleng,_ in kgetha_aetheme.select(.1):
                        data=khii_boleng.fileobj.read(65536)
                        if data:pego_rei.extend(data)
                return pego_rei[Diriša:].decode('utf-8','replace').replace('\r\n','\n')
            def Romela(data):tiragalo_boleng.stdin.write(data);tiragalo_boleng.stdin.flush()
            def šele(Sengwalwa):
                Sengwalwa=ipTestText(Sengwalwa)
                print(pego_boleng['country'],Sengwalwa,flush=True);TATELANO_boleng[0]+=1;bontšha_boleng='__SYSTEM_DONE_'+str(TATELANO_boleng[0])+'__';Diriša=len(pego_rei)
                Romela((Sengwalwa+'; echo; echo '+bontšha_boleng+'\n').encode())
                끝표시=('\r\n'+bontšha_boleng+'\r\n').encode();받기(끝표시,Diriša)
                끝자리=pego_rei.index(끝표시,Diriša)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return pego_rei[Diriša:].decode('utf-8','replace').replace('\r\n','\n')
            def kgonthiša(Sengwalwa,*값들):
                fetola=šele(Sengwalwa)
                for boleng in 값들:assert ipTestText(boleng) in fetola,(Sengwalwa,boleng,fetola)
                return fetola
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    thušo_boleng=kgonthiša('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in aliase_boleng.values():assert 별칭 in thušo_boleng,(별칭,thušo_boleng)
                    kgonthiša(aliase_boleng['help']+' system','Network / system')
                    kgonthiša('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    kgonthiša(aliase_boleng['ipconfig'],'inet 10.0.2.15');kgonthiša('ip addr show','sl0: UP');kgonthiša('ifconfig','sl0: UP')
                    for ye_e_phošagetšego_Dipeakanyo in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Phošo=kgonthiša('ipconfig set '+ye_e_phošagetšego_Dipeakanyo+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Phošo,Phošo
                        kgonthiša('ipconfig','inet 10.0.2.15')
                    kgonthiša('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    kgonthiša(aliase_boleng['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    kgonthiša('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    kgonthiša('ip link set dev sl0 down','sl0: DOWN');kgonthiša('ping -c 1 10.0.2.2; echo STATUS=$?','Phošo -100','STATUS=1')
                    kgonthiša('ipconfig up','sl0: UP')
                    kgonthiša(aliase_boleng['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    kgonthiša('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    kgonthiša('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');kgonthiša(aliase_boleng['route'],'10.0.2.2 sl0')
                    kgonthiša('ftpd start','FTP listening')
                    kgonthiša(aliase_boleng['netstat'],'10.0.2.20:21','LISTEN');kgonthiša('ss','LISTEN')
                    kgonthiša('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Phošo -16')
                    with ftplib.FTP() as klaente_boleng:
                        klaente_boleng.connect('127.0.0.2',접속번호,timeout=20);klaente_boleng.login();data=b'Network address was changed in the guest.\n'
                        klaente_boleng.storbinary('STOR net-state.txt',io.BytesIO(data));받은자료=bytearray();klaente_boleng.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==data;klaente_boleng.delete('net-state.txt')
                    kgonthiša('ftpd stop','FTP stopped');kgonthiša('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    pego_boleng['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Sengwalwa):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Sengwalwa);assert 찾음,Sengwalwa;return tuple(map(int,찾음.groups()))
                    전=저장값(kgonthiša('df','RAM only'));kgonthiša('echo disk-proof > sys-state.txt');후=저장값(kgonthiša(aliase_boleng['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    kgonthiša('rm sys-state.txt');assert 저장값(šele('df'))==전
                    memori_boleng=kgonthiša(aliase_boleng['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',memori_boleng).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    kgonthiša(aliase_boleng['ps'],'kernel/shell');kgonthiša(aliase_boleng['uptime'],'seconds')
                    boemo_tshedimošo=kgonthiša(aliase_boleng['top']+' -n 2','kernel/shell');assert boemo_tshedimošo.count('PID SLOT STATE')==2,boemo_tshedimošo
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    kgonthiša('terminal','TERMINAL READY');Diriša=len(pego_rei);Romela(b'vi process.txt\n');받기(b'NORMAL',Diriša)
                    Diriša=len(pego_rei);Romela(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Diriša)
                    go_tsenya_tshedimošo_Lenaneo=kgonthiša('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',go_tsenya_tshedimošo_Lenaneo);assert 찾음 and int(찾음.group(2))>0,go_tsenya_tshedimošo_Lenaneo
                    kgonthiša('free','EL0 mapped KiB: '+찾음.group(2))
                    Diriša=len(pego_rei);Romela(b'top\n');받기(b'PID SLOT STATE',Diriša);Romela(b'q');받기(b'jkoros-native> ',Diriša)
                    # Test a multibyte prefix through the real shell completion path.
                    if aliase_boleng['df']!='df':
                        Diriša=len(pego_rei);Romela((aliase_boleng['df'][:-1]+'\t\n').encode());받기(b'RAM only',Diriša);받기(b'jkoros-native> ',Diriša)
                    pego_boleng['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as taolo_boleng:
                    taolo_boleng.settimeout(15);taolo_boleng.connect(str(taolo_tsela));Stream_boleng=taolo_boleng.makefile('rwb');json.loads(Stream_boleng.readline());Stream_boleng.write(b'{"execute":"qmp_capabilities"}\n');Stream_boleng.flush()
                    while 'return' not in json.loads(Stream_boleng.readline()):pass
                    Romela((('poweroff' if 인수.poweroff_only else aliase_boleng['poweroff'])+'\n').encode())
                    while True:
                        tiragalo=json.loads(Stream_boleng.readline())
                        if tiragalo.get('event')=='SHUTDOWN':break
                    assert tiragalo['data']['guest'] and tiragalo['data']['reason']=='guest-shutdown',tiragalo
                    assert tiragalo_boleng.wait(timeout=15)==0
                    pego_boleng['shutdown']=tiragalo;pego_boleng['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                pego_boleng['network_trace']=kgokaganyo_boleng_982037b1.latišiša_pego
                assert 인수.poweroff_only or any(go_tsenya_tshedimošo_boleng['protocol']==1 and go_tsenya_tshedimošo_boleng['direction']=='from_guest' for go_tsenya_tshedimošo_boleng in kgokaganyo_boleng_982037b1.latišiša_pego)
                pego_boleng['passed']=True
            finally:
                if tiragalo_boleng.poll() is None:os.killpg(tiragalo_boleng.pid,signal.SIGTERM)
                try:tiragalo_boleng.wait(timeout=10)
                except subprocess.TimeoutExpired:tiragalo_boleng.kill();tiragalo_boleng.wait()
                kgetha_aetheme.close();(출력/'serial.log').write_bytes(pego_rei);(출력/'report.json').write_text(json.dumps(pego_boleng,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({khii_boleng:boleng for khii_boleng,boleng in pego_boleng.items() if khii_boleng!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Diriša()
