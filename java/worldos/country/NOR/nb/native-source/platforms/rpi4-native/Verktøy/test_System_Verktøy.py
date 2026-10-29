#!/usr/bin/env python3
"""faktisk_data eget 커널의 IP/ICMP, status_VERDI spørre_VERDI, 현지어 Kommando, 게스트 Utgang_app bekrefte_5fb2b747."""
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


def Kjør_2():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumenter=parser_48ee4b1b.parse_args()
    speile_rot=Path(__file__).resolve().parents[1];Innstillinger={};navn_tabell={}
    if Argumenter.edition:
        Country_VERDI=Argumenter.edition.resolve();Innstillinger=json.loads((Country_VERDI/'native.json').read_text());navn_tabell=Innstillinger['identifiers'];speile_rot=Country_VERDI/Innstillinger['source']/Innstillinger['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VERDI/'native-edition.py'),'check'])
        vert=Country_VERDI/'host/qemu'
        if vert.is_file():os.environ['QEMU_AARCH64']=str(vert)
    Verktøy=speile_rot/Path(Innstillinger.get('runner','Verktøy/Utfør_kommando.py')).parent
    sys.path.insert(0,str(Verktøy))
    def Les(Navn):
        Sti=Verktøy/(navn_tabell.get(Navn,Navn)+'.py');kontraktverdi=importlib.util.spec_from_file_location('test_'+Navn,str(Sti));modul_VERDI=importlib.util.module_from_spec(kontraktverdi);kontraktverdi.loader.exec_module(modul_VERDI);return modul_VERDI
    kjøring_modul=Les('Utfør_kommando');nettverk_modul=Les('bro_3de4fe3a');Kommando=getattr(kjøring_modul,navn_tabell.get('Kommando','Kommando'));bro_Type=getattr(nettverk_modul,navn_tabell.get('bro_3de4fe3a','bro_3de4fe3a'))
    alias_VERDI_0a38607b=Innstillinger.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresse','ping':'test_svar','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'vise_hjelp'})
    sys.path.insert(0,str(speile_rot/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(speile_rot);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Utgang=Argumenter.output or speile_rot/'build/verification/system-tools';Utgang.mkdir(parents=True,exist_ok=True)
    rapport_VERDI={'passed':False,'country':Innstillinger.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_POST=bytearray();SEKVENS_VERDI=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontroll_bane=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SØK_VERDI:SØK_VERDI.bind(('127.0.0.1',0));portnummer=SØK_VERDI.getsockname()[1]
            if not 50000<=portnummer<=50007:break
        with bro_Type(portnummer,hente=True,gjest_e_post=ipTestText('10.0.2.20'),vert_e_post='127.0.0.2') as bro_VERDI:
            Prosess_VERDI=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontroll_bane)]+bro_VERDI.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            VELG_vare=selectors.DefaultSelector();VELG_vare.register(Prosess_VERDI.stdout,selectors.EVENT_READ)
            def motta(vise_VERDI_487749b8,Kjør_2=0,제한=45):
                끝=time.monotonic()+제한
                while vise_VERDI_487749b8 not in LOG_POST[Kjør_2:]:
                    if time.monotonic()>끝 or Prosess_VERDI.poll() is not None:raise AssertionError('Missing '+repr(vise_VERDI_487749b8)+'\n'+LOG_POST[Kjør_2:].decode('utf-8','replace'))
                    for tast_VERDI,_ in VELG_vare.select(.1):
                        data=tast_VERDI.fileobj.read(65536)
                        if data:LOG_POST.extend(data)
                return LOG_POST[Kjør_2:].decode('utf-8','replace').replace('\r\n','\n')
            def sende(data):Prosess_VERDI.stdin.write(data);Prosess_VERDI.stdin.flush()
            def Shell(Tekst):
                Tekst=ipTestText(Tekst)
                print(rapport_VERDI['country'],Tekst,flush=True);SEKVENS_VERDI[0]+=1;vise_VERDI_487749b8='__SYSTEM_DONE_'+str(SEKVENS_VERDI[0])+'__';Kjør_2=len(LOG_POST)
                sende((Tekst+'; echo; echo '+vise_VERDI_487749b8+'\n').encode())
                avslutte_en_samtale_tusj=('\r\n'+vise_VERDI_487749b8+'\r\n').encode();motta(avslutte_en_samtale_tusj,Kjør_2)
                avslutte_en_samtale_plassere=LOG_POST.index(avslutte_en_samtale_tusj,Kjør_2)+len(avslutte_en_samtale_tusj)
                motta(b'jkoros-native> ',avslutte_en_samtale_plassere)
                return LOG_POST[Kjør_2:].decode('utf-8','replace').replace('\r\n','\n')
            def bekrefte(Tekst,*값들):
                svar=Shell(Tekst)
                for VERDI in 값들:assert ipTestText(VERDI) in svar,(Tekst,VERDI,svar)
                return svar
            try:
                motta(b'jkoros-native> ')
                if not Argumenter.poweroff_only:
                    hjelp_VERDI=bekrefte('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VERDI_0a38607b.values():assert 별칭 in hjelp_VERDI,(별칭,hjelp_VERDI)
                    bekrefte(alias_VERDI_0a38607b['help']+' system','Network / system')
                    bekrefte('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    bekrefte(alias_VERDI_0a38607b['ipconfig'],'inet 10.0.2.15');bekrefte('ip addr show','sl0: UP');bekrefte('ifconfig','sl0: UP')
                    for ugyldig_Innstillinger in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        feil=bekrefte('ipconfig set '+ugyldig_Innstillinger+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in feil,feil
                        bekrefte('ipconfig','inet 10.0.2.15')
                    bekrefte('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    bekrefte(alias_VERDI_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bekrefte('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    bekrefte('ip link set dev sl0 down','sl0: DOWN');bekrefte('ping -c 1 10.0.2.2; echo STATUS=$?','feil -100','STATUS=1')
                    bekrefte('ipconfig up','sl0: UP')
                    bekrefte(alias_VERDI_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    bekrefte('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bekrefte('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');bekrefte(alias_VERDI_0a38607b['route'],'10.0.2.2 sl0')
                    bekrefte('ftpd start','FTP listening')
                    bekrefte(alias_VERDI_0a38607b['netstat'],'10.0.2.20:21','LISTEN');bekrefte('ss','LISTEN')
                    bekrefte('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','feil -16')
                    with ftplib.FTP() as klient_VERDI:
                        klient_VERDI.connect('127.0.0.2',portnummer,timeout=20);klient_VERDI.login();data=b'Network address was changed in the guest.\n'
                        klient_VERDI.storbinary('STOR net-state.txt',io.BytesIO(data));MOTTATT_AVKAST_data=bytearray();klient_VERDI.retrbinary('RETR net-state.txt',MOTTATT_AVKAST_data.extend);assert MOTTATT_AVKAST_data==data;klient_VERDI.delete('net-state.txt')
                    bekrefte('ftpd stop','FTP stopped');bekrefte('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    rapport_VERDI['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(bekrefte('df','RAM only'));bekrefte('echo disk-proof > sys-state.txt');후=저장값(bekrefte(alias_VERDI_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    bekrefte('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Minne_VERDI=bekrefte(alias_VERDI_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');antall_VERDI=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Minne_VERDI).groups()));assert 0<antall_VERDI[1]<=antall_VERDI[0] and antall_VERDI[1]+antall_VERDI[2]==antall_VERDI[0]
                    bekrefte(alias_VERDI_0a38607b['ps'],'kernel/shell');bekrefte(alias_VERDI_0a38607b['uptime'],'seconds')
                    status_info=bekrefte(alias_VERDI_0a38607b['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    bekrefte('terminal','TERMINAL READY');Kjør_2=len(LOG_POST);sende(b'vi process.txt\n');motta(b'NORMAL',Kjør_2)
                    Kjør_2=len(LOG_POST);sende(bytes([30,2,1,0,0,0,0]));motta(b'jkoros-native> ',Kjør_2)
                    oppføring_Liste=bekrefte('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',oppføring_Liste);assert 찾음 and int(찾음.group(2))>0,oppføring_Liste
                    bekrefte('free','EL0 mapped KiB: '+찾음.group(2))
                    Kjør_2=len(LOG_POST);sende(b'top\n');motta(b'PID SLOT STATE',Kjør_2);sende(b'q');motta(b'jkoros-native> ',Kjør_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VERDI_0a38607b['df']!='df':
                        Kjør_2=len(LOG_POST);sende((alias_VERDI_0a38607b['df'][:-1]+'\t\n').encode());motta(b'RAM only',Kjør_2);motta(b'jkoros-native> ',Kjør_2)
                    rapport_VERDI['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontroll_VERDI:
                    kontroll_VERDI.settimeout(15);kontroll_VERDI.connect(str(kontroll_bane));strøm_VERDI=kontroll_VERDI.makefile('rwb');json.loads(strøm_VERDI.readline());strøm_VERDI.write(b'{"execute":"qmp_capabilities"}\n');strøm_VERDI.flush()
                    while 'return' not in json.loads(strøm_VERDI.readline()):pass
                    sende((('poweroff' if Argumenter.poweroff_only else alias_VERDI_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Hendelse=json.loads(strøm_VERDI.readline())
                        if Hendelse.get('event')=='SHUTDOWN':break
                    assert Hendelse['data']['guest'] and Hendelse['data']['reason']=='guest-shutdown',Hendelse
                    assert Prosess_VERDI.wait(timeout=15)==0
                    rapport_VERDI['shutdown']=Hendelse;rapport_VERDI['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                rapport_VERDI['network_trace']=bro_VERDI.sporingslogg
                assert Argumenter.poweroff_only or any(oppføring_VERDI['protocol']==1 and oppføring_VERDI['direction']=='from_guest' for oppføring_VERDI in bro_VERDI.sporingslogg)
                rapport_VERDI['passed']=True
            finally:
                if Prosess_VERDI.poll() is None:os.killpg(Prosess_VERDI.pid,signal.SIGTERM)
                try:Prosess_VERDI.wait(timeout=10)
                except subprocess.TimeoutExpired:Prosess_VERDI.kill();Prosess_VERDI.wait()
                VELG_vare.close();(Utgang/'serial.log').write_bytes(LOG_POST);(Utgang/'report.json').write_text(json.dumps(rapport_VERDI,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tast_VERDI:VERDI for tast_VERDI,VERDI in rapport_VERDI.items() if tast_VERDI!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Kjør_2()
