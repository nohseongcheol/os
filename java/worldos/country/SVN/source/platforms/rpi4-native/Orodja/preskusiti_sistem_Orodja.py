#!/usr/bin/env python3
"""dejanski_podatki lastno 커널의 IP/ICMP, stanje_VALUE poizvedba_VALUE, 현지어 Ukaz, 게스트 Izhod_aplikacija preveriti_veljavnost."""
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


def Zaženi():
    razčlenjevalnik_48ee4b1b=argparse.ArgumentParser();razčlenjevalnik_48ee4b1b.add_argument('--edition',type=Path);razčlenjevalnik_48ee4b1b.add_argument('--output',type=Path);razčlenjevalnik_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumenti=razčlenjevalnik_48ee4b1b.parse_args()
    pobuda_koren=Path(__file__).resolve().parents[1];Nastavitve={};ime_tabela={}
    if Argumenti.edition:
        Country_VALUE=Argumenti.edition.resolve();Nastavitve=json.loads((Country_VALUE/'native.json').read_text());ime_tabela=Nastavitve['identifiers'];pobuda_koren=Country_VALUE/Nastavitve['source']/Nastavitve['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALUE/'native-edition.py'),'check'])
        gostiti=Country_VALUE/'host/qemu'
        if gostiti.is_file():os.environ['QEMU_AARCH64']=str(gostiti)
    Orodja=pobuda_koren/Path(Nastavitve.get('runner','Orodja/Izvedi_ukaz.py')).parent
    sys.path.insert(0,str(Orodja))
    def Branje(Ime):
        POT=Orodja/(ime_tabela.get(Ime,Ime)+'.py');primer_VALUE=importlib.util.spec_from_file_location('test_'+Ime,str(POT));modul_VALUE=importlib.util.module_from_spec(primer_VALUE);primer_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Branje('Izvedi_ukaz');mreža_modul=Branje('most_3de4fe3a');Ukaz=getattr(실행모듈,ime_tabela.get('Ukaz','Ukaz'));most_Tip=getattr(mreža_modul,ime_tabela.get('most_3de4fe3a','most_3de4fe3a'))
    vzdevek_VALUE=Nastavitve.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'naslov_IP','ping':'preskusiti_odziv','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'oddaja_spletna_pomoč'})
    sys.path.insert(0,str(pobuda_koren/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(pobuda_koren);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Izpis=Argumenti.output or pobuda_koren/'build/verification/system-tools';Izpis.mkdir(parents=True,exist_ok=True)
    prijavi_VALUE={'passed':False,'country':Nastavitve.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_zapis=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        nadzor_pot=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Išči_VALUE:Išči_VALUE.bind(('127.0.0.1',0));številka_vrat=Išči_VALUE.getsockname()[1]
            if not 50000<=številka_vrat<=50007:break
        with most_Tip(številka_vrat,snemati=True,gost_naslov=ipTestText('10.0.2.20'),gostiti_naslov='127.0.0.2') as most_VALUE:
            Proces_VALUE=subprocess.Popen(Ukaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(nadzor_pot)]+most_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_element=selectors.DefaultSelector();CHOOSE_element.register(Proces_VALUE.stdout,selectors.EVENT_READ)
            def sprejeti_sprejemati_prejeti_prejemati(oddaja_VALUE_487749b8,Zaženi=0,제한=45):
                끝=time.monotonic()+제한
                while oddaja_VALUE_487749b8 not in LOG_zapis[Zaženi:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:raise AssertionError('Missing '+repr(oddaja_VALUE_487749b8)+'\n'+LOG_zapis[Zaženi:].decode('utf-8','replace'))
                    for Ključ_VALUE,_ in CHOOSE_element.select(.1):
                        podatki=Ključ_VALUE.fileobj.read(65536)
                        if podatki:LOG_zapis.extend(podatki)
                return LOG_zapis[Zaženi:].decode('utf-8','replace').replace('\r\n','\n')
            def poslati(podatki):Proces_VALUE.stdin.write(podatki);Proces_VALUE.stdin.flush()
            def lupina(Besedilo):
                Besedilo=ipTestText(Besedilo)
                print(prijavi_VALUE['country'],Besedilo,flush=True);SEQUENCE_VALUE[0]+=1;oddaja_VALUE_487749b8='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Zaženi=len(LOG_zapis)
                poslati((Besedilo+'; echo; echo '+oddaja_VALUE_487749b8+'\n').encode())
                končati_klic_oznaka=('\r\n'+oddaja_VALUE_487749b8+'\r\n').encode();sprejeti_sprejemati_prejeti_prejemati(končati_klic_oznaka,Zaženi)
                končati_klic_položaj=LOG_zapis.index(končati_klic_oznaka,Zaženi)+len(končati_klic_oznaka)
                sprejeti_sprejemati_prejeti_prejemati(b'jkoros-native> ',končati_klic_položaj)
                return LOG_zapis[Zaženi:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(Besedilo,*값들):
                odgovor=lupina(Besedilo)
                for VALUE in 값들:assert ipTestText(VALUE) in odgovor,(Besedilo,VALUE,odgovor)
                return odgovor
            try:
                sprejeti_sprejemati_prejeti_prejemati(b'jkoros-native> ')
                if not Argumenti.poweroff_only:
                    spletna_pomoč_VALUE=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in vzdevek_VALUE.values():assert 별칭 in spletna_pomoč_VALUE,(별칭,spletna_pomoč_VALUE)
                    확인(vzdevek_VALUE['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(vzdevek_VALUE['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for neveljaven_Nastavitve in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        NAPAKA=확인('ipconfig set '+neveljaven_Nastavitve+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in NAPAKA,NAPAKA
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(vzdevek_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','NAPAKA -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(vzdevek_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(vzdevek_VALUE['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(vzdevek_VALUE['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','NAPAKA -16')
                    with ftplib.FTP() as odjemalec_VALUE:
                        odjemalec_VALUE.connect('127.0.0.2',številka_vrat,timeout=20);odjemalec_VALUE.login();podatki=b'Network address was changed in the guest.\n'
                        odjemalec_VALUE.storbinary('STOR net-state.txt',io.BytesIO(podatki));RECEIVED_podatki=bytearray();odjemalec_VALUE.retrbinary('RETR net-state.txt',RECEIVED_podatki.extend);assert RECEIVED_podatki==podatki;odjemalec_VALUE.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    prijavi_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Besedilo):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Besedilo);assert 찾음,Besedilo;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(vzdevek_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(lupina('df'))==전
                    pomnilnik_VALUE=확인(vzdevek_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',pomnilnik_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    확인(vzdevek_VALUE['ps'],'kernel/shell');확인(vzdevek_VALUE['uptime'],'seconds')
                    stanje_informacije=확인(vzdevek_VALUE['top']+' -n 2','kernel/shell');assert stanje_informacije.count('PID SLOT STATE')==2,stanje_informacije
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');Zaženi=len(LOG_zapis);poslati(b'vi process.txt\n');sprejeti_sprejemati_prejeti_prejemati(b'NORMAL',Zaženi)
                    Zaženi=len(LOG_zapis);poslati(bytes([30,2,1,0,0,0,0]));sprejeti_sprejemati_prejeti_prejemati(b'jkoros-native> ',Zaženi)
                    vnos_Seznam=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',vnos_Seznam);assert 찾음 and int(찾음.group(2))>0,vnos_Seznam
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    Zaženi=len(LOG_zapis);poslati(b'top\n');sprejeti_sprejemati_prejeti_prejemati(b'PID SLOT STATE',Zaženi);poslati(b'q');sprejeti_sprejemati_prejeti_prejemati(b'jkoros-native> ',Zaženi)
                    # Test a multibyte prefix through the real shell completion path.
                    if vzdevek_VALUE['df']!='df':
                        Zaženi=len(LOG_zapis);poslati((vzdevek_VALUE['df'][:-1]+'\t\n').encode());sprejeti_sprejemati_prejeti_prejemati(b'RAM only',Zaženi);sprejeti_sprejemati_prejeti_prejemati(b'jkoros-native> ',Zaženi)
                    prijavi_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as nadzor_VALUE:
                    nadzor_VALUE.settimeout(15);nadzor_VALUE.connect(str(nadzor_pot));tok_VALUE=nadzor_VALUE.makefile('rwb');json.loads(tok_VALUE.readline());tok_VALUE.write(b'{"execute":"qmp_capabilities"}\n');tok_VALUE.flush()
                    while 'return' not in json.loads(tok_VALUE.readline()):pass
                    poslati((('poweroff' if Argumenti.poweroff_only else vzdevek_VALUE['poweroff'])+'\n').encode())
                    while True:
                        dogodek=json.loads(tok_VALUE.readline())
                        if dogodek.get('event')=='SHUTDOWN':break
                    assert dogodek['data']['guest'] and dogodek['data']['reason']=='guest-shutdown',dogodek
                    assert Proces_VALUE.wait(timeout=15)==0
                    prijavi_VALUE['shutdown']=dogodek;prijavi_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                prijavi_VALUE['network_trace']=most_VALUE.dnevnik_sledenja
                assert Argumenti.poweroff_only or any(vnos_VALUE['protocol']==1 and vnos_VALUE['direction']=='from_guest' for vnos_VALUE in most_VALUE.dnevnik_sledenja)
                prijavi_VALUE['passed']=True
            finally:
                if Proces_VALUE.poll() is None:os.killpg(Proces_VALUE.pid,signal.SIGTERM)
                try:Proces_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
                CHOOSE_element.close();(Izpis/'serial.log').write_bytes(LOG_zapis);(Izpis/'report.json').write_text(json.dumps(prijavi_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Ključ_VALUE:VALUE for Ključ_VALUE,VALUE in prijavi_VALUE.items() if Ključ_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Zaženi()
