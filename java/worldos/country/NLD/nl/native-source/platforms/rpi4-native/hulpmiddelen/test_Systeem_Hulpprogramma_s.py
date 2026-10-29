#!/usr/bin/env python3
"""werkelijk_gegevens Eigen 커널의 IP/ICMP, Status_WAARDE query_WAARDE, 현지어 opdracht, 게스트 Einde_app valideren."""
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


def starten():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumenten=parser_48ee4b1b.parse_args()
    Taken_wortel=Path(__file__).resolve().parents[1];Instellingen={};naam_tabel={}
    if argumenten.edition:
        Country_WAARDE=argumenten.edition.resolve();Instellingen=json.loads((Country_WAARDE/'native.json').read_text());naam_tabel=Instellingen['identifiers'];Taken_wortel=Country_WAARDE/Instellingen['source']/Instellingen['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_WAARDE/'native-edition.py'),'check'])
        host=Country_WAARDE/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    hulpmiddelen=Taken_wortel/Path(Instellingen.get('runner','hulpmiddelen/Uitvoeren_opdracht.py')).parent
    sys.path.insert(0,str(hulpmiddelen))
    def Lezen(Naam):
        pad=hulpmiddelen/(naam_tabel.get(Naam,Naam)+'.py');contractwaarde=importlib.util.spec_from_file_location('test_'+Naam,str(pad));module_WAARDE=importlib.util.module_from_spec(contractwaarde);contractwaarde.loader.exec_module(module_WAARDE);return module_WAARDE
    uitvoerbewerking_module=Lezen('Uitvoeren_opdracht');net_module=Lezen('brug_3de4fe3a');opdracht=getattr(uitvoerbewerking_module,naam_tabel.get('opdracht','opdracht'));brug_TYPE=getattr(net_module,naam_tabel.get('brug_3de4fe3a','brug_3de4fe3a'))
    alias_WAARDE_0a38607b=Instellingen.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adres','ping':'test_reactie','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'hulp_tonen'})
    sys.path.insert(0,str(Taken_wortel/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Taken_wortel);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    tekstuitvoer=argumenten.output or Taken_wortel/'build/verification/system-tools';tekstuitvoer.mkdir(parents=True,exist_ok=True)
    Rapport_WAARDE={'passed':False,'country':Instellingen.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();REEKS_WAARDE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        controle_pad=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Search_WAARDE:Search_WAARDE.bind(('127.0.0.1',0));poortnummer=Search_WAARDE.getsockname()[1]
            if not 50000<=poortnummer<=50007:break
        with brug_TYPE(poortnummer,Capture=True,gast_ADRES=ipTestText('10.0.2.20'),host_ADRES='127.0.0.2') as brug_WAARDE:
            Proces_WAARDE=subprocess.Popen(opdracht()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(controle_pad)]+brug_WAARDE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            KIEZEN_item=selectors.DefaultSelector();KIEZEN_item.register(Proces_WAARDE.stdout,selectors.EVENT_READ)
            def ontvangen(weergeven_WAARDE,starten=0,제한=45):
                끝=time.monotonic()+제한
                while weergeven_WAARDE not in LOG_RECORD[starten:]:
                    if time.monotonic()>끝 or Proces_WAARDE.poll() is not None:raise AssertionError('Missing '+repr(weergeven_WAARDE)+'\n'+LOG_RECORD[starten:].decode('utf-8','replace'))
                    for toets_WAARDE,_ in KIEZEN_item.select(.1):
                        gegevens=toets_WAARDE.fileobj.read(65536)
                        if gegevens:LOG_RECORD.extend(gegevens)
                return LOG_RECORD[starten:].decode('utf-8','replace').replace('\r\n','\n')
            def e_mailen(gegevens):Proces_WAARDE.stdin.write(gegevens);Proces_WAARDE.stdin.flush()
            def Shell(tekst):
                tekst=ipTestText(tekst)
                print(Rapport_WAARDE['country'],tekst,flush=True);REEKS_WAARDE[0]+=1;weergeven_WAARDE='__SYSTEM_DONE_'+str(REEKS_WAARDE[0])+'__';starten=len(LOG_RECORD)
                e_mailen((tekst+'; echo; echo '+weergeven_WAARDE+'\n').encode())
                beëindigen_markering=('\r\n'+weergeven_WAARDE+'\r\n').encode();ontvangen(beëindigen_markering,starten)
                beëindigen_functie=LOG_RECORD.index(beëindigen_markering,starten)+len(beëindigen_markering)
                ontvangen(b'jkoros-native> ',beëindigen_functie)
                return LOG_RECORD[starten:].decode('utf-8','replace').replace('\r\n','\n')
            def bevestigen(tekst,*값들):
                reactie=Shell(tekst)
                for WAARDE in 값들:assert ipTestText(WAARDE) in reactie,(tekst,WAARDE,reactie)
                return reactie
            try:
                ontvangen(b'jkoros-native> ')
                if not argumenten.poweroff_only:
                    help_WAARDE=bevestigen('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_WAARDE_0a38607b.values():assert 별칭 in help_WAARDE,(별칭,help_WAARDE)
                    bevestigen(alias_WAARDE_0a38607b['help']+' system','Network / system')
                    bevestigen('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    bevestigen(alias_WAARDE_0a38607b['ipconfig'],'inet 10.0.2.15');bevestigen('ip addr show','sl0: UP');bevestigen('ifconfig','sl0: UP')
                    for nietig_Instellingen in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        fout=bevestigen('ipconfig set '+nietig_Instellingen+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in fout,fout
                        bevestigen('ipconfig','inet 10.0.2.15')
                    bevestigen('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    bevestigen(alias_WAARDE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bevestigen('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    bevestigen('ip link set dev sl0 down','sl0: DOWN');bevestigen('ping -c 1 10.0.2.2; echo STATUS=$?','fout -100','STATUS=1')
                    bevestigen('ipconfig up','sl0: UP')
                    bevestigen(alias_WAARDE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    bevestigen('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bevestigen('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');bevestigen(alias_WAARDE_0a38607b['route'],'10.0.2.2 sl0')
                    bevestigen('ftpd start','FTP listening')
                    bevestigen(alias_WAARDE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');bevestigen('ss','LISTEN')
                    bevestigen('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','fout -16')
                    with ftplib.FTP() as client_WAARDE:
                        client_WAARDE.connect('127.0.0.2',poortnummer,timeout=20);client_WAARDE.login();gegevens=b'Network address was changed in the guest.\n'
                        client_WAARDE.storbinary('STOR net-state.txt',io.BytesIO(gegevens));OPBRENGST_gegevens=bytearray();client_WAARDE.retrbinary('RETR net-state.txt',OPBRENGST_gegevens.extend);assert OPBRENGST_gegevens==gegevens;client_WAARDE.delete('net-state.txt')
                    bevestigen('ftpd stop','FTP stopped');bevestigen('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Rapport_WAARDE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',tekst);assert 찾음,tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(bevestigen('df','RAM only'));bevestigen('echo disk-proof > sys-state.txt');후=저장값(bevestigen(alias_WAARDE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    bevestigen('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Geheugen_WAARDE=bevestigen(alias_WAARDE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');hoeveelheid_WAARDE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Geheugen_WAARDE).groups()));assert 0<hoeveelheid_WAARDE[1]<=hoeveelheid_WAARDE[0] and hoeveelheid_WAARDE[1]+hoeveelheid_WAARDE[2]==hoeveelheid_WAARDE[0]
                    bevestigen(alias_WAARDE_0a38607b['ps'],'kernel/shell');bevestigen(alias_WAARDE_0a38607b['uptime'],'seconds')
                    status_info=bevestigen(alias_WAARDE_0a38607b['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    bevestigen('terminal','TERMINAL READY');starten=len(LOG_RECORD);e_mailen(b'vi process.txt\n');ontvangen(b'NORMAL',starten)
                    starten=len(LOG_RECORD);e_mailen(bytes([30,2,1,0,0,0,0]));ontvangen(b'jkoros-native> ',starten)
                    invoer_Lijst_f07b3200=bevestigen('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',invoer_Lijst_f07b3200);assert 찾음 and int(찾음.group(2))>0,invoer_Lijst_f07b3200
                    bevestigen('free','EL0 mapped KiB: '+찾음.group(2))
                    starten=len(LOG_RECORD);e_mailen(b'top\n');ontvangen(b'PID SLOT STATE',starten);e_mailen(b'q');ontvangen(b'jkoros-native> ',starten)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_WAARDE_0a38607b['df']!='df':
                        starten=len(LOG_RECORD);e_mailen((alias_WAARDE_0a38607b['df'][:-1]+'\t\n').encode());ontvangen(b'RAM only',starten);ontvangen(b'jkoros-native> ',starten)
                    Rapport_WAARDE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as controle_WAARDE:
                    controle_WAARDE.settimeout(15);controle_WAARDE.connect(str(controle_pad));Stream_WAARDE=controle_WAARDE.makefile('rwb');json.loads(Stream_WAARDE.readline());Stream_WAARDE.write(b'{"execute":"qmp_capabilities"}\n');Stream_WAARDE.flush()
                    while 'return' not in json.loads(Stream_WAARDE.readline()):pass
                    e_mailen((('poweroff' if argumenten.poweroff_only else alias_WAARDE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Gebeurtenis=json.loads(Stream_WAARDE.readline())
                        if Gebeurtenis.get('event')=='SHUTDOWN':break
                    assert Gebeurtenis['data']['guest'] and Gebeurtenis['data']['reason']=='guest-shutdown',Gebeurtenis
                    assert Proces_WAARDE.wait(timeout=15)==0
                    Rapport_WAARDE['shutdown']=Gebeurtenis;Rapport_WAARDE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Rapport_WAARDE['network_trace']=brug_WAARDE.traceerlogboek
                assert argumenten.poweroff_only or any(invoer_WAARDE_962f286b['protocol']==1 and invoer_WAARDE_962f286b['direction']=='from_guest' for invoer_WAARDE_962f286b in brug_WAARDE.traceerlogboek)
                Rapport_WAARDE['passed']=True
            finally:
                if Proces_WAARDE.poll() is None:os.killpg(Proces_WAARDE.pid,signal.SIGTERM)
                try:Proces_WAARDE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_WAARDE.kill();Proces_WAARDE.wait()
                KIEZEN_item.close();(tekstuitvoer/'serial.log').write_bytes(LOG_RECORD);(tekstuitvoer/'report.json').write_text(json.dumps(Rapport_WAARDE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({toets_WAARDE:WAARDE for toets_WAARDE,WAARDE in Rapport_WAARDE.items() if toets_WAARDE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':starten()
