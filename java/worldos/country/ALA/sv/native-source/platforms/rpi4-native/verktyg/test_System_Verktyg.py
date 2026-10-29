#!/usr/bin/env python3
"""verklig_data eget 커널의 IP/ICMP, status_värde fråga_värde, 현지어 kommando, 게스트 Utgång_app validera."""
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


def Kör():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');argument=parser_48ee4b1b.parse_args()
    åtgärd_rot=Path(__file__).resolve().parents[1];Inställningar={};namn_tabell={}
    if argument.edition:
        Country_värde=argument.edition.resolve();Inställningar=json.loads((Country_värde/'native.json').read_text());namn_tabell=Inställningar['identifiers'];åtgärd_rot=Country_värde/Inställningar['source']/Inställningar['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_värde/'native-edition.py'),'check'])
        värd=Country_värde/'host/qemu'
        if värd.is_file():os.environ['QEMU_AARCH64']=str(värd)
    verktyg=åtgärd_rot/Path(Inställningar.get('runner','verktyg/köra_kommando.py')).parent
    sys.path.insert(0,str(verktyg))
    def Läs(Namn):
        sökväg_2=verktyg/(namn_tabell.get(Namn,Namn)+'.py');kontraktsvärde=importlib.util.spec_from_file_location('test_'+Namn,str(sökväg_2));modul_värde=importlib.util.module_from_spec(kontraktsvärde);kontraktsvärde.loader.exec_module(modul_värde);return modul_värde
    körning_modul=Läs('köra_kommando');nätverk_modul=Läs('brygga_3de4fe3a');kommando=getattr(körning_modul,namn_tabell.get('kommando','kommando'));brygga_Typ=getattr(nätverk_modul,namn_tabell.get('brygga_3de4fe3a','brygga_3de4fe3a'))
    alias_värde_0a38607b=Inställningar.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adress','ping':'test_svar','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'visa_hjälp'})
    sys.path.insert(0,str(åtgärd_rot/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(åtgärd_rot);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    utmatningsposition=argument.output or åtgärd_rot/'build/verification/system-tools';utmatningsposition.mkdir(parents=True,exist_ok=True)
    Rapport_värde={'passed':False,'country':Inställningar.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_POST=bytearray();SEKVENS_värde=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontroll_väg=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SÖK_värde:SÖK_värde.bind(('127.0.0.1',0));portnummer=SÖK_värde.getsockname()[1]
            if not 50000<=portnummer<=50007:break
        with brygga_Typ(portnummer,Capture=True,gäst_ADRESS=ipTestText('10.0.2.20'),värd_ADRESS='127.0.0.2') as brygga_värde:
            Process_värde=subprocess.Popen(kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontroll_väg)]+brygga_värde.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            VÄLJ_objekt=selectors.DefaultSelector();VÄLJ_objekt.register(Process_värde.stdout,selectors.EVENT_READ)
            def få(visa_värde,Kör=0,제한=45):
                끝=time.monotonic()+제한
                while visa_värde not in LOG_POST[Kör:]:
                    if time.monotonic()>끝 or Process_värde.poll() is not None:raise AssertionError('Missing '+repr(visa_värde)+'\n'+LOG_POST[Kör:].decode('utf-8','replace'))
                    for Nyckel_värde,_ in VÄLJ_objekt.select(.1):
                        data=Nyckel_värde.fileobj.read(65536)
                        if data:LOG_POST.extend(data)
                return LOG_POST[Kör:].decode('utf-8','replace').replace('\r\n','\n')
            def skicka(data):Process_värde.stdin.write(data);Process_värde.stdin.flush()
            def Shell(text):
                text=ipTestText(text)
                print(Rapport_värde['country'],text,flush=True);SEKVENS_värde[0]+=1;visa_värde='__SYSTEM_DONE_'+str(SEKVENS_värde[0])+'__';Kör=len(LOG_POST)
                skicka((text+'; echo; echo '+visa_värde+'\n').encode())
                avsluta_markör=('\r\n'+visa_värde+'\r\n').encode();få(avsluta_markör,Kör)
                avsluta_placera=LOG_POST.index(avsluta_markör,Kör)+len(avsluta_markör)
                få(b'jkoros-native> ',avsluta_placera)
                return LOG_POST[Kör:].decode('utf-8','replace').replace('\r\n','\n')
            def verifiera(text,*값들):
                svara=Shell(text)
                for värde in 값들:assert ipTestText(värde) in svara,(text,värde,svara)
                return svara
            try:
                få(b'jkoros-native> ')
                if not argument.poweroff_only:
                    hjälp_värde=verifiera('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_värde_0a38607b.values():assert 별칭 in hjälp_värde,(별칭,hjälp_värde)
                    verifiera(alias_värde_0a38607b['help']+' system','Network / system')
                    verifiera('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verifiera(alias_värde_0a38607b['ipconfig'],'inet 10.0.2.15');verifiera('ip addr show','sl0: UP');verifiera('ifconfig','sl0: UP')
                    for ogiltig_Inställningar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        fel=verifiera('ipconfig set '+ogiltig_Inställningar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in fel,fel
                        verifiera('ipconfig','inet 10.0.2.15')
                    verifiera('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verifiera(alias_värde_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifiera('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verifiera('ip link set dev sl0 down','sl0: DOWN');verifiera('ping -c 1 10.0.2.2; echo STATUS=$?','fel -100','STATUS=1')
                    verifiera('ipconfig up','sl0: UP')
                    verifiera(alias_värde_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verifiera('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verifiera('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verifiera(alias_värde_0a38607b['route'],'10.0.2.2 sl0')
                    verifiera('ftpd start','FTP listening')
                    verifiera(alias_värde_0a38607b['netstat'],'10.0.2.20:21','LISTEN');verifiera('ss','LISTEN')
                    verifiera('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','fel -16')
                    with ftplib.FTP() as klient_värde:
                        klient_värde.connect('127.0.0.2',portnummer,timeout=20);klient_värde.login();data=b'Network address was changed in the guest.\n'
                        klient_värde.storbinary('STOR net-state.txt',io.BytesIO(data));BELOPP_data=bytearray();klient_värde.retrbinary('RETR net-state.txt',BELOPP_data.extend);assert BELOPP_data==data;klient_värde.delete('net-state.txt')
                    verifiera('ftpd stop','FTP stopped');verifiera('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Rapport_värde['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(text):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',text);assert 찾음,text;return tuple(map(int,찾음.groups()))
                    전=저장값(verifiera('df','RAM only'));verifiera('echo disk-proof > sys-state.txt');후=저장값(verifiera(alias_värde_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verifiera('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Minne_värde=verifiera(alias_värde_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');kvantitet_värde=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Minne_värde).groups()));assert 0<kvantitet_värde[1]<=kvantitet_värde[0] and kvantitet_värde[1]+kvantitet_värde[2]==kvantitet_värde[0]
                    verifiera(alias_värde_0a38607b['ps'],'kernel/shell');verifiera(alias_värde_0a38607b['uptime'],'seconds')
                    status_info=verifiera(alias_värde_0a38607b['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verifiera('terminal','TERMINAL READY');Kör=len(LOG_POST);skicka(b'vi process.txt\n');få(b'NORMAL',Kör)
                    Kör=len(LOG_POST);skicka(bytes([30,2,1,0,0,0,0]));få(b'jkoros-native> ',Kör)
                    post_ange=verifiera('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',post_ange);assert 찾음 and int(찾음.group(2))>0,post_ange
                    verifiera('free','EL0 mapped KiB: '+찾음.group(2))
                    Kör=len(LOG_POST);skicka(b'top\n');få(b'PID SLOT STATE',Kör);skicka(b'q');få(b'jkoros-native> ',Kör)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_värde_0a38607b['df']!='df':
                        Kör=len(LOG_POST);skicka((alias_värde_0a38607b['df'][:-1]+'\t\n').encode());få(b'RAM only',Kör);få(b'jkoros-native> ',Kör)
                    Rapport_värde['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontroll_värde:
                    kontroll_värde.settimeout(15);kontroll_värde.connect(str(kontroll_väg));flöde_värde=kontroll_värde.makefile('rwb');json.loads(flöde_värde.readline());flöde_värde.write(b'{"execute":"qmp_capabilities"}\n');flöde_värde.flush()
                    while 'return' not in json.loads(flöde_värde.readline()):pass
                    skicka((('poweroff' if argument.poweroff_only else alias_värde_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Händelse=json.loads(flöde_värde.readline())
                        if Händelse.get('event')=='SHUTDOWN':break
                    assert Händelse['data']['guest'] and Händelse['data']['reason']=='guest-shutdown',Händelse
                    assert Process_värde.wait(timeout=15)==0
                    Rapport_värde['shutdown']=Händelse;Rapport_värde['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Rapport_värde['network_trace']=brygga_värde.spårningslogg
                assert argument.poweroff_only or any(post_värde['protocol']==1 and post_värde['direction']=='from_guest' for post_värde in brygga_värde.spårningslogg)
                Rapport_värde['passed']=True
            finally:
                if Process_värde.poll() is None:os.killpg(Process_värde.pid,signal.SIGTERM)
                try:Process_värde.wait(timeout=10)
                except subprocess.TimeoutExpired:Process_värde.kill();Process_värde.wait()
                VÄLJ_objekt.close();(utmatningsposition/'serial.log').write_bytes(LOG_POST);(utmatningsposition/'report.json').write_text(json.dumps(Rapport_värde,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Nyckel_värde:värde for Nyckel_värde,värde in Rapport_värde.items() if Nyckel_värde!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Kör()
