#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani 자체 커널의 IP/ICMP, Matsayi_Daraja Matantanci_Daraja, 현지어 Umarni, 게스트 Mafita_Shiri inganta."""
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


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b=argparse.ArgumentParser();tatsar_manhaja_48ee4b1b.add_argument('--edition',type=Path);tatsar_manhaja_48ee4b1b.add_argument('--output',type=Path);tatsar_manhaja_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=tatsar_manhaja_48ee4b1b.parse_args()
    기준=Path(__file__).resolve().parents[1];Saituna={};Suna_tebur={}
    if 인수.edition:
        나라=인수.edition.resolve();Saituna=json.loads((나라/'native.json').read_text());Suna_tebur=Saituna['identifiers'];기준=나라/Saituna['source']/Saituna['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        sauka=나라/'host/qemu'
        if sauka.is_file():os.environ['QEMU_AARCH64']=str(sauka)
    Kaya=기준/Path(Saituna.get('runner','Kaya/gudanar_Umarni.py')).parent
    sys.path.insert(0,str(Kaya))
    def Yi_Karatu(Suna):
        Hanyar_shiga=Kaya/(Suna_tebur.get(Suna,Suna)+'.py');Kes_Daraja=importlib.util.spec_from_file_location('test_'+Suna,str(Hanyar_shiga));shiri_Daraja=importlib.util.module_from_spec(Kes_Daraja);Kes_Daraja.loader.exec_module(shiri_Daraja);return shiri_Daraja
    실행모듈=Yi_Karatu('gudanar_Umarni');Hanyar_sadarwa_shiri=Yi_Karatu('통신다리');Umarni=getattr(실행모듈,Suna_tebur.get('Umarni','Umarni'));다리형=getattr(Hanyar_sadarwa_shiri,Suna_tebur.get('통신다리','통신다리'))
    alias_Daraja=Saituna.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adireshin_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'Nuna_Taimako'})
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
    Rahoto_Daraja={'passed':False,'country':Saituna.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    logu_naɗa=bytearray();JERI_Daraja=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        masarrafa_Hanyar_shiga=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Leko_Daraja:Leko_Daraja.bind(('127.0.0.1',0));lambar_kafa=Leko_Daraja.getsockname()[1]
            if not 50000<=lambar_kafa<=50007:break
        with 다리형(lambar_kafa,ɗauka=True,baƙo_imel=ipTestText('10.0.2.20'),sauka_imel='127.0.0.2') as 다리:
            haryar_aikin_na_ura_Daraja=subprocess.Popen(Umarni()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(masarrafa_Hanyar_shiga)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            bayyana_ra_ayinka_abu=selectors.DefaultSelector();bayyana_ra_ayinka_abu.register(haryar_aikin_na_ura_Daraja.stdout,selectors.EVENT_READ)
            def 받기(Nuna_Daraja,Tafiyar_da=0,제한=45):
                끝=time.monotonic()+제한
                while Nuna_Daraja not in logu_naɗa[Tafiyar_da:]:
                    if time.monotonic()>끝 or haryar_aikin_na_ura_Daraja.poll() is not None:raise AssertionError('Missing '+repr(Nuna_Daraja)+'\n'+logu_naɗa[Tafiyar_da:].decode('utf-8','replace'))
                    for Makulli_Daraja,_ in bayyana_ra_ayinka_abu.select(.1):
                        Tarin_bayani=Makulli_Daraja.fileobj.read(65536)
                        if Tarin_bayani:logu_naɗa.extend(Tarin_bayani)
                return logu_naɗa[Tafiyar_da:].decode('utf-8','replace').replace('\r\n','\n')
            def Aika(Tarin_bayani):haryar_aikin_na_ura_Daraja.stdin.write(Tarin_bayani);haryar_aikin_na_ura_Daraja.stdin.flush()
            def Mai_fayyace_umani(SMS):
                SMS=ipTestText(SMS)
                print(Rahoto_Daraja['country'],SMS,flush=True);JERI_Daraja[0]+=1;Nuna_Daraja='__SYSTEM_DONE_'+str(JERI_Daraja[0])+'__';Tafiyar_da=len(logu_naɗa)
                Aika((SMS+'; echo; echo '+Nuna_Daraja+'\n').encode())
                끝표시=('\r\n'+Nuna_Daraja+'\r\n').encode();받기(끝표시,Tafiyar_da)
                끝자리=logu_naɗa.index(끝표시,Tafiyar_da)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return logu_naɗa[Tafiyar_da:].decode('utf-8','replace').replace('\r\n','\n')
            def Tabbatar_da(SMS,*값들):
                mayar_da_martani=Mai_fayyace_umani(SMS)
                for Daraja in 값들:assert ipTestText(Daraja) in mayar_da_martani,(SMS,Daraja,mayar_da_martani)
                return mayar_da_martani
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    Taimako_Daraja=Tabbatar_da('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_Daraja.values():assert 별칭 in Taimako_Daraja,(별칭,Taimako_Daraja)
                    Tabbatar_da(alias_Daraja['help']+' system','Network / system')
                    Tabbatar_da('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    Tabbatar_da(alias_Daraja['ipconfig'],'inet 10.0.2.15');Tabbatar_da('ip addr show','sl0: UP');Tabbatar_da('ifconfig','sl0: UP')
                    for mara_ƙarfi_Saituna in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Kuskure=Tabbatar_da('ipconfig set '+mara_ƙarfi_Saituna+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Kuskure,Kuskure
                        Tabbatar_da('ipconfig','inet 10.0.2.15')
                    Tabbatar_da('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    Tabbatar_da(alias_Daraja['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    Tabbatar_da('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    Tabbatar_da('ip link set dev sl0 down','sl0: DOWN');Tabbatar_da('ping -c 1 10.0.2.2; echo STATUS=$?','Kuskure -100','STATUS=1')
                    Tabbatar_da('ipconfig up','sl0: UP')
                    Tabbatar_da(alias_Daraja['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    Tabbatar_da('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    Tabbatar_da('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');Tabbatar_da(alias_Daraja['route'],'10.0.2.2 sl0')
                    Tabbatar_da('ftpd start','FTP listening')
                    Tabbatar_da(alias_Daraja['netstat'],'10.0.2.20:21','LISTEN');Tabbatar_da('ss','LISTEN')
                    Tabbatar_da('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Kuskure -16')
                    with ftplib.FTP() as abokin_hulda_Daraja:
                        abokin_hulda_Daraja.connect('127.0.0.2',lambar_kafa,timeout=20);abokin_hulda_Daraja.login();Tarin_bayani=b'Network address was changed in the guest.\n'
                        abokin_hulda_Daraja.storbinary('STOR net-state.txt',io.BytesIO(Tarin_bayani));받은자료=bytearray();abokin_hulda_Daraja.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==Tarin_bayani;abokin_hulda_Daraja.delete('net-state.txt')
                    Tabbatar_da('ftpd stop','FTP stopped');Tabbatar_da('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Rahoto_Daraja['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(Tabbatar_da('df','RAM only'));Tabbatar_da('echo disk-proof > sys-state.txt');후=저장값(Tabbatar_da(alias_Daraja['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    Tabbatar_da('rm sys-state.txt');assert 저장값(Mai_fayyace_umani('df'))==전
                    Mahardatar_kwamfuta_Daraja=Tabbatar_da(alias_Daraja['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Mahardatar_kwamfuta_Daraja).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    Tabbatar_da(alias_Daraja['ps'],'kernel/shell');Tabbatar_da(alias_Daraja['uptime'],'seconds')
                    samuwa_bayani=Tabbatar_da(alias_Daraja['top']+' -n 2','kernel/shell');assert samuwa_bayani.count('PID SLOT STATE')==2,samuwa_bayani
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    Tabbatar_da('terminal','TERMINAL READY');Tafiyar_da=len(logu_naɗa);Aika(b'vi process.txt\n');받기(b'NORMAL',Tafiyar_da)
                    Tafiyar_da=len(logu_naɗa);Aika(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Tafiyar_da)
                    Mashigar_bayanai_Jeri=Tabbatar_da('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',Mashigar_bayanai_Jeri);assert 찾음 and int(찾음.group(2))>0,Mashigar_bayanai_Jeri
                    Tabbatar_da('free','EL0 mapped KiB: '+찾음.group(2))
                    Tafiyar_da=len(logu_naɗa);Aika(b'top\n');받기(b'PID SLOT STATE',Tafiyar_da);Aika(b'q');받기(b'jkoros-native> ',Tafiyar_da)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_Daraja['df']!='df':
                        Tafiyar_da=len(logu_naɗa);Aika((alias_Daraja['df'][:-1]+'\t\n').encode());받기(b'RAM only',Tafiyar_da);받기(b'jkoros-native> ',Tafiyar_da)
                    Rahoto_Daraja['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as masarrafa_Daraja:
                    masarrafa_Daraja.settimeout(15);masarrafa_Daraja.connect(str(masarrafa_Hanyar_shiga));watsuwa_Daraja=masarrafa_Daraja.makefile('rwb');json.loads(watsuwa_Daraja.readline());watsuwa_Daraja.write(b'{"execute":"qmp_capabilities"}\n');watsuwa_Daraja.flush()
                    while 'return' not in json.loads(watsuwa_Daraja.readline()):pass
                    Aika((('poweroff' if 인수.poweroff_only else alias_Daraja['poweroff'])+'\n').encode())
                    while True:
                        Faruwa=json.loads(watsuwa_Daraja.readline())
                        if Faruwa.get('event')=='SHUTDOWN':break
                    assert Faruwa['data']['guest'] and Faruwa['data']['reason']=='guest-shutdown',Faruwa
                    assert haryar_aikin_na_ura_Daraja.wait(timeout=15)==0
                    Rahoto_Daraja['shutdown']=Faruwa;Rahoto_Daraja['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Rahoto_Daraja['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(Mashigar_bayanai_Daraja['protocol']==1 and Mashigar_bayanai_Daraja['direction']=='from_guest' for Mashigar_bayanai_Daraja in 다리.추적기록)
                Rahoto_Daraja['passed']=True
            finally:
                if haryar_aikin_na_ura_Daraja.poll() is None:os.killpg(haryar_aikin_na_ura_Daraja.pid,signal.SIGTERM)
                try:haryar_aikin_na_ura_Daraja.wait(timeout=10)
                except subprocess.TimeoutExpired:haryar_aikin_na_ura_Daraja.kill();haryar_aikin_na_ura_Daraja.wait()
                bayyana_ra_ayinka_abu.close();(출력/'serial.log').write_bytes(logu_naɗa);(출력/'report.json').write_text(json.dumps(Rahoto_Daraja,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Makulli_Daraja:Daraja for Makulli_Daraja,Daraja in Rahoto_Daraja.items() if Makulli_Daraja!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Tafiyar_da()
