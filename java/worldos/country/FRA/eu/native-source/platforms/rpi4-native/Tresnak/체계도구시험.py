#!/usr/bin/env python3
"""benetako_datuak 자체 커널의 IP/ICMP, Egoera_balio kontsulta_balio, 현지어 Komandoa, 게스트 irten_aplik baliozkotu."""
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


def Exekutatu_2():
    analizatzaile_48ee4b1b=argparse.ArgumentParser();analizatzaile_48ee4b1b.add_argument('--edition',type=Path);analizatzaile_48ee4b1b.add_argument('--output',type=Path);analizatzaile_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumentuak=analizatzaile_48ee4b1b.parse_args()
    Project_erro=Path(__file__).resolve().parents[1];Ezarpenak={};izen_taula={}
    if Argumentuak.edition:
        나라=Argumentuak.edition.resolve();Ezarpenak=json.loads((나라/'native.json').read_text());izen_taula=Ezarpenak['identifiers'];Project_erro=나라/Ezarpenak['source']/Ezarpenak['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        Ostalari=나라/'host/qemu'
        if Ostalari.is_file():os.environ['QEMU_AARCH64']=str(Ostalari)
    Tresnak=Project_erro/Path(Ezarpenak.get('runner','Tresnak/exekutatu_komando.py')).parent
    sys.path.insert(0,str(Tresnak))
    def Irakurri(Izena):
        Bide_izena=Tresnak/(izen_taula.get(Izena,Izena)+'.py');kasu_balio=importlib.util.spec_from_file_location('test_'+Izena,str(Bide_izena));modulu_balio=importlib.util.module_from_spec(kasu_balio);kasu_balio.loader.exec_module(modulu_balio);return modulu_balio
    실행모듈=Irakurri('exekutatu_komando');sare_modulu=Irakurri('sare_zubi');Komandoa=getattr(실행모듈,izen_taula.get('Komandoa','Komandoa'));zubi_MOTA=getattr(sare_modulu,izen_taula.get('sare_zubi','sare_zubi'))
    alias_balio=Ezarpenak.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_helbide','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'erakutsi_laguntza'})
    sys.path.insert(0,str(Project_erro/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_erro);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Irteera=Argumentuak.output or Project_erro/'build/verification/system-tools';Irteera.mkdir(parents=True,exist_ok=True)
    txosten_balio={'passed':False,'country':Ezarpenak.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_marka=bytearray();SEKUENTZIA_balio=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrol_bide_izen=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as BILATU_balio:BILATU_balio.bind(('127.0.0.1',0));ataka_zenbaki=BILATU_balio.getsockname()[1]
            if not 50000<=ataka_zenbaki<=50007:break
        with zubi_MOTA(ataka_zenbaki,atera_ba7b8054=True,gonbidatu_helbide=ipTestText('10.0.2.20'),Ostalari_helbide='127.0.0.2') as zubi_balio:
            prozesu_balio=subprocess.Popen(Komandoa()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrol_bide_izen)]+zubi_balio.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            AUKERATU_elementu=selectors.DefaultSelector();AUKERATU_elementu.register(prozesu_balio.stdout,selectors.EVENT_READ)
            def 받기(erakutsi_balio,Exekutatu_2=0,제한=45):
                끝=time.monotonic()+제한
                while erakutsi_balio not in LOG_marka[Exekutatu_2:]:
                    if time.monotonic()>끝 or prozesu_balio.poll() is not None:raise AssertionError('Missing '+repr(erakutsi_balio)+'\n'+LOG_marka[Exekutatu_2:].decode('utf-8','replace'))
                    for gako_balio,_ in AUKERATU_elementu.select(.1):
                        datuak=gako_balio.fileobj.read(65536)
                        if datuak:LOG_marka.extend(datuak)
                return LOG_marka[Exekutatu_2:].decode('utf-8','replace').replace('\r\n','\n')
            def bidali(datuak):prozesu_balio.stdin.write(datuak);prozesu_balio.stdin.flush()
            def shell(Testua):
                Testua=ipTestText(Testua)
                print(txosten_balio['country'],Testua,flush=True);SEKUENTZIA_balio[0]+=1;erakutsi_balio='__SYSTEM_DONE_'+str(SEKUENTZIA_balio[0])+'__';Exekutatu_2=len(LOG_marka)
                bidali((Testua+'; echo; echo '+erakutsi_balio+'\n').encode())
                끝표시=('\r\n'+erakutsi_balio+'\r\n').encode();받기(끝표시,Exekutatu_2)
                amaitu_kargu=LOG_marka.index(끝표시,Exekutatu_2)+len(끝표시)
                받기(b'jkoros-native> ',amaitu_kargu)
                return LOG_marka[Exekutatu_2:].decode('utf-8','replace').replace('\r\n','\n')
            def egiaztatu(Testua,*값들):
                erantzun=shell(Testua)
                for balio in 값들:assert ipTestText(balio) in erantzun,(Testua,balio,erantzun)
                return erantzun
            try:
                받기(b'jkoros-native> ')
                if not Argumentuak.poweroff_only:
                    laguntza_balio=egiaztatu('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_balio.values():assert 별칭 in laguntza_balio,(별칭,laguntza_balio)
                    egiaztatu(alias_balio['help']+' system','Network / system')
                    egiaztatu('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    egiaztatu(alias_balio['ipconfig'],'inet 10.0.2.15');egiaztatu('ip addr show','sl0: UP');egiaztatu('ifconfig','sl0: UP')
                    for baliogabe_Ezarpenak in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        errorea=egiaztatu('ipconfig set '+baliogabe_Ezarpenak+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in errorea,errorea
                        egiaztatu('ipconfig','inet 10.0.2.15')
                    egiaztatu('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    egiaztatu(alias_balio['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    egiaztatu('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    egiaztatu('ip link set dev sl0 down','sl0: DOWN');egiaztatu('ping -c 1 10.0.2.2; echo STATUS=$?','errorea -100','STATUS=1')
                    egiaztatu('ipconfig up','sl0: UP')
                    egiaztatu(alias_balio['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    egiaztatu('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    egiaztatu('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');egiaztatu(alias_balio['route'],'10.0.2.2 sl0')
                    egiaztatu('ftpd start','FTP listening')
                    egiaztatu(alias_balio['netstat'],'10.0.2.20:21','LISTEN');egiaztatu('ss','LISTEN')
                    egiaztatu('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','errorea -16')
                    with ftplib.FTP() as bezero_balio:
                        bezero_balio.connect('127.0.0.2',ataka_zenbaki,timeout=20);bezero_balio.login();datuak=b'Network address was changed in the guest.\n'
                        bezero_balio.storbinary('STOR net-state.txt',io.BytesIO(datuak));RECEIVED_datuak=bytearray();bezero_balio.retrbinary('RETR net-state.txt',RECEIVED_datuak.extend);assert RECEIVED_datuak==datuak;bezero_balio.delete('net-state.txt')
                    egiaztatu('ftpd stop','FTP stopped');egiaztatu('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    txosten_balio['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Testua):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Testua);assert 찾음,Testua;return tuple(map(int,찾음.groups()))
                    전=저장값(egiaztatu('df','RAM only'));egiaztatu('echo disk-proof > sys-state.txt');후=저장값(egiaztatu(alias_balio['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    egiaztatu('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memoria_balio=egiaztatu(alias_balio['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memoria_balio).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    egiaztatu(alias_balio['ps'],'kernel/shell');egiaztatu(alias_balio['uptime'],'seconds')
                    egoera_info=egiaztatu(alias_balio['top']+' -n 2','kernel/shell');assert egoera_info.count('PID SLOT STATE')==2,egoera_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    egiaztatu('terminal','TERMINAL READY');Exekutatu_2=len(LOG_marka);bidali(b'vi process.txt\n');받기(b'NORMAL',Exekutatu_2)
                    Exekutatu_2=len(LOG_marka);bidali(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Exekutatu_2)
                    sarrera_Zerrenda=egiaztatu('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',sarrera_Zerrenda);assert 찾음 and int(찾음.group(2))>0,sarrera_Zerrenda
                    egiaztatu('free','EL0 mapped KiB: '+찾음.group(2))
                    Exekutatu_2=len(LOG_marka);bidali(b'top\n');받기(b'PID SLOT STATE',Exekutatu_2);bidali(b'q');받기(b'jkoros-native> ',Exekutatu_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_balio['df']!='df':
                        Exekutatu_2=len(LOG_marka);bidali((alias_balio['df'][:-1]+'\t\n').encode());받기(b'RAM only',Exekutatu_2);받기(b'jkoros-native> ',Exekutatu_2)
                    txosten_balio['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrol_balio:
                    kontrol_balio.settimeout(15);kontrol_balio.connect(str(kontrol_bide_izen));Stream_balio=kontrol_balio.makefile('rwb');json.loads(Stream_balio.readline());Stream_balio.write(b'{"execute":"qmp_capabilities"}\n');Stream_balio.flush()
                    while 'return' not in json.loads(Stream_balio.readline()):pass
                    bidali((('poweroff' if Argumentuak.poweroff_only else alias_balio['poweroff'])+'\n').encode())
                    while True:
                        Gertaera=json.loads(Stream_balio.readline())
                        if Gertaera.get('event')=='SHUTDOWN':break
                    assert Gertaera['data']['guest'] and Gertaera['data']['reason']=='guest-shutdown',Gertaera
                    assert prozesu_balio.wait(timeout=15)==0
                    txosten_balio['shutdown']=Gertaera;txosten_balio['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                txosten_balio['network_trace']=zubi_balio.balio_diagonalen_batura_LOG
                assert Argumentuak.poweroff_only or any(sarrera_balio['protocol']==1 and sarrera_balio['direction']=='from_guest' for sarrera_balio in zubi_balio.balio_diagonalen_batura_LOG)
                txosten_balio['passed']=True
            finally:
                if prozesu_balio.poll() is None:os.killpg(prozesu_balio.pid,signal.SIGTERM)
                try:prozesu_balio.wait(timeout=10)
                except subprocess.TimeoutExpired:prozesu_balio.kill();prozesu_balio.wait()
                AUKERATU_elementu.close();(Irteera/'serial.log').write_bytes(LOG_marka);(Irteera/'report.json').write_text(json.dumps(txosten_balio,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({gako_balio:balio for gako_balio,balio in txosten_balio.items() if gako_balio!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Exekutatu_2()
