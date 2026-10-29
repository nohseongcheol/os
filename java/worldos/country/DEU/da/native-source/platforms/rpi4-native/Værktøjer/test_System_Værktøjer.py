#!/usr/bin/env python3
"""faktisk_data eget 커널의 IP/ICMP, status_VÆRDI forespørge_VÆRDI, 현지어 Kommando, 게스트 Afslut_app bekræfte_5fb2b747."""
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


def Kør_2():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumenter=parser_48ee4b1b.parse_args()
    To_do_rod=Path(__file__).resolve().parents[1];Indstillinger={};navn_tabel={}
    if Argumenter.edition:
        Country_VÆRDI=Argumenter.edition.resolve();Indstillinger=json.loads((Country_VÆRDI/'native.json').read_text());navn_tabel=Indstillinger['identifiers'];To_do_rod=Country_VÆRDI/Indstillinger['source']/Indstillinger['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VÆRDI/'native-edition.py'),'check'])
        vært=Country_VÆRDI/'host/qemu'
        if vært.is_file():os.environ['QEMU_AARCH64']=str(vært)
    Værktøjer=To_do_rod/Path(Indstillinger.get('runner','Værktøjer/Udfør_kommando.py')).parent
    sys.path.insert(0,str(Værktøjer))
    def Læse(Navn):
        Sti=Værktøjer/(navn_tabel.get(Navn,Navn)+'.py');kontraktværdi=importlib.util.spec_from_file_location('test_'+Navn,str(Sti));modul_VÆRDI=importlib.util.module_from_spec(kontraktværdi);kontraktværdi.loader.exec_module(modul_VÆRDI);return modul_VÆRDI
    udførelse_modul=Læse('Udfør_kommando');netværk_modul=Læse('bro_3de4fe3a');Kommando=getattr(udførelse_modul,navn_tabel.get('Kommando','Kommando'));bro_Type=getattr(netværk_modul,navn_tabel.get('bro_3de4fe3a','bro_3de4fe3a'))
    alias_VÆRDI_0a38607b=Indstillinger.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresse','ping':'test_svar','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'vise_hjælp'})
    sys.path.insert(0,str(To_do_rod/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(To_do_rod);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Udgang=Argumenter.output or To_do_rod/'build/verification/system-tools';Udgang.mkdir(parents=True,exist_ok=True)
    rapport_VÆRDI={'passed':False,'country':Indstillinger.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_post=bytearray();SEKVENS_VÆRDI=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrol_sti=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SØG_VÆRDI:SØG_VÆRDI.bind(('127.0.0.1',0));portnummer=SØG_VÆRDI.getsockname()[1]
            if not 50000<=portnummer<=50007:break
        with bro_Type(portnummer,optage=True,gæst_mail=ipTestText('10.0.2.20'),vært_mail='127.0.0.2') as bro_VÆRDI:
            Proces_VÆRDI=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrol_sti)]+bro_VÆRDI.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            VÆLG_vare=selectors.DefaultSelector();VÆLG_vare.register(Proces_VÆRDI.stdout,selectors.EVENT_READ)
            def modtage(vise_VÆRDI,Kør_2=0,제한=45):
                끝=time.monotonic()+제한
                while vise_VÆRDI not in LOG_post[Kør_2:]:
                    if time.monotonic()>끝 or Proces_VÆRDI.poll() is not None:raise AssertionError('Missing '+repr(vise_VÆRDI)+'\n'+LOG_post[Kør_2:].decode('utf-8','replace'))
                    for tast_VÆRDI,_ in VÆLG_vare.select(.1):
                        data=tast_VÆRDI.fileobj.read(65536)
                        if data:LOG_post.extend(data)
                return LOG_post[Kør_2:].decode('utf-8','replace').replace('\r\n','\n')
            def maile(data):Proces_VÆRDI.stdin.write(data);Proces_VÆRDI.stdin.flush()
            def Shell(Tekst):
                Tekst=ipTestText(Tekst)
                print(rapport_VÆRDI['country'],Tekst,flush=True);SEKVENS_VÆRDI[0]+=1;vise_VÆRDI='__SYSTEM_DONE_'+str(SEKVENS_VÆRDI[0])+'__';Kør_2=len(LOG_post)
                maile((Tekst+'; echo; echo '+vise_VÆRDI+'\n').encode())
                afslutte_et_opkald_mærke=('\r\n'+vise_VÆRDI+'\r\n').encode();modtage(afslutte_et_opkald_mærke,Kør_2)
                afslutte_et_opkald_placere=LOG_post.index(afslutte_et_opkald_mærke,Kør_2)+len(afslutte_et_opkald_mærke)
                modtage(b'jkoros-native> ',afslutte_et_opkald_placere)
                return LOG_post[Kør_2:].decode('utf-8','replace').replace('\r\n','\n')
            def bekræfte(Tekst,*값들):
                svar=Shell(Tekst)
                for VÆRDI in 값들:assert ipTestText(VÆRDI) in svar,(Tekst,VÆRDI,svar)
                return svar
            try:
                modtage(b'jkoros-native> ')
                if not Argumenter.poweroff_only:
                    hjælp_VÆRDI=bekræfte('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VÆRDI_0a38607b.values():assert 별칭 in hjælp_VÆRDI,(별칭,hjælp_VÆRDI)
                    bekræfte(alias_VÆRDI_0a38607b['help']+' system','Network / system')
                    bekræfte('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    bekræfte(alias_VÆRDI_0a38607b['ipconfig'],'inet 10.0.2.15');bekræfte('ip addr show','sl0: UP');bekræfte('ifconfig','sl0: UP')
                    for ugyldig_Indstillinger in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        fejl=bekræfte('ipconfig set '+ugyldig_Indstillinger+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in fejl,fejl
                        bekræfte('ipconfig','inet 10.0.2.15')
                    bekræfte('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    bekræfte(alias_VÆRDI_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bekræfte('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    bekræfte('ip link set dev sl0 down','sl0: DOWN');bekræfte('ping -c 1 10.0.2.2; echo STATUS=$?','fejl -100','STATUS=1')
                    bekræfte('ipconfig up','sl0: UP')
                    bekræfte(alias_VÆRDI_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    bekræfte('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    bekræfte('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');bekræfte(alias_VÆRDI_0a38607b['route'],'10.0.2.2 sl0')
                    bekræfte('ftpd start','FTP listening')
                    bekræfte(alias_VÆRDI_0a38607b['netstat'],'10.0.2.20:21','LISTEN');bekræfte('ss','LISTEN')
                    bekræfte('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','fejl -16')
                    with ftplib.FTP() as klient_VÆRDI:
                        klient_VÆRDI.connect('127.0.0.2',portnummer,timeout=20);klient_VÆRDI.login();data=b'Network address was changed in the guest.\n'
                        klient_VÆRDI.storbinary('STOR net-state.txt',io.BytesIO(data));MODTAGET_VED_UDLØB_data=bytearray();klient_VÆRDI.retrbinary('RETR net-state.txt',MODTAGET_VED_UDLØB_data.extend);assert MODTAGET_VED_UDLØB_data==data;klient_VÆRDI.delete('net-state.txt')
                    bekræfte('ftpd stop','FTP stopped');bekræfte('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    rapport_VÆRDI['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(bekræfte('df','RAM only'));bekræfte('echo disk-proof > sys-state.txt');후=저장값(bekræfte(alias_VÆRDI_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    bekræfte('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Hukommelse_VÆRDI=bekræfte(alias_VÆRDI_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');antal_VÆRDI=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Hukommelse_VÆRDI).groups()));assert 0<antal_VÆRDI[1]<=antal_VÆRDI[0] and antal_VÆRDI[1]+antal_VÆRDI[2]==antal_VÆRDI[0]
                    bekræfte(alias_VÆRDI_0a38607b['ps'],'kernel/shell');bekræfte(alias_VÆRDI_0a38607b['uptime'],'seconds')
                    status_info=bekræfte(alias_VÆRDI_0a38607b['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    bekræfte('terminal','TERMINAL READY');Kør_2=len(LOG_post);maile(b'vi process.txt\n');modtage(b'NORMAL',Kør_2)
                    Kør_2=len(LOG_post);maile(bytes([30,2,1,0,0,0,0]));modtage(b'jkoros-native> ',Kør_2)
                    post_Liste=bekræfte('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',post_Liste);assert 찾음 and int(찾음.group(2))>0,post_Liste
                    bekræfte('free','EL0 mapped KiB: '+찾음.group(2))
                    Kør_2=len(LOG_post);maile(b'top\n');modtage(b'PID SLOT STATE',Kør_2);maile(b'q');modtage(b'jkoros-native> ',Kør_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VÆRDI_0a38607b['df']!='df':
                        Kør_2=len(LOG_post);maile((alias_VÆRDI_0a38607b['df'][:-1]+'\t\n').encode());modtage(b'RAM only',Kør_2);modtage(b'jkoros-native> ',Kør_2)
                    rapport_VÆRDI['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrol_VÆRDI:
                    kontrol_VÆRDI.settimeout(15);kontrol_VÆRDI.connect(str(kontrol_sti));strøm_VÆRDI=kontrol_VÆRDI.makefile('rwb');json.loads(strøm_VÆRDI.readline());strøm_VÆRDI.write(b'{"execute":"qmp_capabilities"}\n');strøm_VÆRDI.flush()
                    while 'return' not in json.loads(strøm_VÆRDI.readline()):pass
                    maile((('poweroff' if Argumenter.poweroff_only else alias_VÆRDI_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        hændelse=json.loads(strøm_VÆRDI.readline())
                        if hændelse.get('event')=='SHUTDOWN':break
                    assert hændelse['data']['guest'] and hændelse['data']['reason']=='guest-shutdown',hændelse
                    assert Proces_VÆRDI.wait(timeout=15)==0
                    rapport_VÆRDI['shutdown']=hændelse;rapport_VÆRDI['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                rapport_VÆRDI['network_trace']=bro_VÆRDI.sporingslogfil
                assert Argumenter.poweroff_only or any(post_VÆRDI_962f286b['protocol']==1 and post_VÆRDI_962f286b['direction']=='from_guest' for post_VÆRDI_962f286b in bro_VÆRDI.sporingslogfil)
                rapport_VÆRDI['passed']=True
            finally:
                if Proces_VÆRDI.poll() is None:os.killpg(Proces_VÆRDI.pid,signal.SIGTERM)
                try:Proces_VÆRDI.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VÆRDI.kill();Proces_VÆRDI.wait()
                VÆLG_vare.close();(Udgang/'serial.log').write_bytes(LOG_post);(Udgang/'report.json').write_text(json.dumps(rapport_VÆRDI,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tast_VÆRDI:VÆRDI for tast_VÆRDI,VÆRDI in rapport_VÆRDI.items() if tast_VÆRDI!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Kør_2()
