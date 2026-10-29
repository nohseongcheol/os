#!/usr/bin/env python3
"""skutečný_data vlastní 커널의 IP/ICMP, Stav_HODNOTA dotaz_HODNOTA, 현지어 příkaz, 게스트 Konec_program ověřit_5fb2b747."""
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


def Spustit_2():
    analyzátor_48ee4b1b=argparse.ArgumentParser();analyzátor_48ee4b1b.add_argument('--edition',type=Path);analyzátor_48ee4b1b.add_argument('--output',type=Path);analyzátor_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumenty=analyzátor_48ee4b1b.parse_args()
    akce_kořen=Path(__file__).resolve().parents[1];Nastavení={};název_tabulka={}
    if argumenty.edition:
        Country_HODNOTA=argumenty.edition.resolve();Nastavení=json.loads((Country_HODNOTA/'native.json').read_text());název_tabulka=Nastavení['identifiers'];akce_kořen=Country_HODNOTA/Nastavení['source']/Nastavení['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_HODNOTA/'native-edition.py'),'check'])
        hostit=Country_HODNOTA/'host/qemu'
        if hostit.is_file():os.environ['QEMU_AARCH64']=str(hostit)
    nástroje=akce_kořen/Path(Nastavení.get('runner','nástroje/Provést_příkaz.py')).parent
    sys.path.insert(0,str(nástroje))
    def Čtení(Název):
        cesta_2=nástroje/(název_tabulka.get(Název,Název)+'.py');hodnota_smlouvy=importlib.util.spec_from_file_location('test_'+Název,str(cesta_2));modul_HODNOTA=importlib.util.module_from_spec(hodnota_smlouvy);hodnota_smlouvy.loader.exec_module(modul_HODNOTA);return modul_HODNOTA
    spuštění_modul=Čtení('Provést_příkaz');síť_modul=Čtení('most_3de4fe3a');příkaz=getattr(spuštění_modul,název_tabulka.get('příkaz','příkaz'));most_TYP=getattr(síť_modul,název_tabulka.get('most_3de4fe3a','most_3de4fe3a'))
    alias_HODNOTA=Nastavení.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresa','ping':'test_odpověď','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'zobrazit_nápovědu'})
    sys.path.insert(0,str(akce_kořen/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(akce_kořen);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    výstupní_pozice=argumenty.output or akce_kořen/'build/verification/system-tools';výstupní_pozice.mkdir(parents=True,exist_ok=True)
    Zpráva_HODNOTA={'passed':False,'country':Nastavení.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOGZ_ZÁZNAM=bytearray();SEQUENCE_HODNOTA=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        řízení_cesta=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as HLEDAT_HODNOTA:HLEDAT_HODNOTA.bind(('127.0.0.1',0));číslo_portu=HLEDAT_HODNOTA.getsockname()[1]
            if not 50000<=číslo_portu<=50007:break
        with most_TYP(číslo_portu,čerpat=True,host_ODKAZ=ipTestText('10.0.2.20'),hostit_ODKAZ='127.0.0.2') as most_HODNOTA:
            Proces_HODNOTA=subprocess.Popen(příkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(řízení_cesta)]+most_HODNOTA.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ZVOLIT_zboží=selectors.DefaultSelector();ZVOLIT_zboží.register(Proces_HODNOTA.stdout,selectors.EVENT_READ)
            def dostat(zobrazit_HODNOTA,Spustit_2=0,제한=45):
                끝=time.monotonic()+제한
                while zobrazit_HODNOTA not in LOGZ_ZÁZNAM[Spustit_2:]:
                    if time.monotonic()>끝 or Proces_HODNOTA.poll() is not None:raise AssertionError('Missing '+repr(zobrazit_HODNOTA)+'\n'+LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8','replace'))
                    for Klíč_HODNOTA,_ in ZVOLIT_zboží.select(.1):
                        data=Klíč_HODNOTA.fileobj.read(65536)
                        if data:LOGZ_ZÁZNAM.extend(data)
                return LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8','replace').replace('\r\n','\n')
            def poslat(data):Proces_HODNOTA.stdin.write(data);Proces_HODNOTA.stdin.flush()
            def prostředí(text):
                text=ipTestText(text)
                print(Zpráva_HODNOTA['country'],text,flush=True);SEQUENCE_HODNOTA[0]+=1;zobrazit_HODNOTA='__SYSTEM_DONE_'+str(SEQUENCE_HODNOTA[0])+'__';Spustit_2=len(LOGZ_ZÁZNAM)
                poslat((text+'; echo; echo '+zobrazit_HODNOTA+'\n').encode())
                konec_značka=('\r\n'+zobrazit_HODNOTA+'\r\n').encode();dostat(konec_značka,Spustit_2)
                konec_pozice=LOGZ_ZÁZNAM.index(konec_značka,Spustit_2)+len(konec_značka)
                dostat(b'jkoros-native> ',konec_pozice)
                return LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ověřit(text,*값들):
                odezva=prostředí(text)
                for HODNOTA in 값들:assert ipTestText(HODNOTA) in odezva,(text,HODNOTA,odezva)
                return odezva
            try:
                dostat(b'jkoros-native> ')
                if not argumenty.poweroff_only:
                    nápověda_HODNOTA=ověřit('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_HODNOTA.values():assert 별칭 in nápověda_HODNOTA,(별칭,nápověda_HODNOTA)
                    ověřit(alias_HODNOTA['help']+' system','Network / system')
                    ověřit('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ověřit(alias_HODNOTA['ipconfig'],'inet 10.0.2.15');ověřit('ip addr show','sl0: UP');ověřit('ifconfig','sl0: UP')
                    for neplatný_Nastavení in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        chyba=ověřit('ipconfig set '+neplatný_Nastavení+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in chyba,chyba
                        ověřit('ipconfig','inet 10.0.2.15')
                    ověřit('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ověřit(alias_HODNOTA['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ověřit('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ověřit('ip link set dev sl0 down','sl0: DOWN');ověřit('ping -c 1 10.0.2.2; echo STATUS=$?','chyba -100','STATUS=1')
                    ověřit('ipconfig up','sl0: UP')
                    ověřit(alias_HODNOTA['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ověřit('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ověřit('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ověřit(alias_HODNOTA['route'],'10.0.2.2 sl0')
                    ověřit('ftpd start','FTP listening')
                    ověřit(alias_HODNOTA['netstat'],'10.0.2.20:21','LISTEN');ověřit('ss','LISTEN')
                    ověřit('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','chyba -16')
                    with ftplib.FTP() as klient_HODNOTA:
                        klient_HODNOTA.connect('127.0.0.2',číslo_portu,timeout=20);klient_HODNOTA.login();data=b'Network address was changed in the guest.\n'
                        klient_HODNOTA.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();klient_HODNOTA.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;klient_HODNOTA.delete('net-state.txt')
                    ověřit('ftpd stop','FTP stopped');ověřit('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Zpráva_HODNOTA['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(text):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',text);assert 찾음,text;return tuple(map(int,찾음.groups()))
                    전=저장값(ověřit('df','RAM only'));ověřit('echo disk-proof > sys-state.txt');후=저장값(ověřit(alias_HODNOTA['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ověřit('rm sys-state.txt');assert 저장값(prostředí('df'))==전
                    Paměť_HODNOTA=ověřit(alias_HODNOTA['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');množství_HODNOTA=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Paměť_HODNOTA).groups()));assert 0<množství_HODNOTA[1]<=množství_HODNOTA[0] and množství_HODNOTA[1]+množství_HODNOTA[2]==množství_HODNOTA[0]
                    ověřit(alias_HODNOTA['ps'],'kernel/shell');ověřit(alias_HODNOTA['uptime'],'seconds')
                    stav_informace=ověřit(alias_HODNOTA['top']+' -n 2','kernel/shell');assert stav_informace.count('PID SLOT STATE')==2,stav_informace
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ověřit('terminal','TERMINAL READY');Spustit_2=len(LOGZ_ZÁZNAM);poslat(b'vi process.txt\n');dostat(b'NORMAL',Spustit_2)
                    Spustit_2=len(LOGZ_ZÁZNAM);poslat(bytes([30,2,1,0,0,0,0]));dostat(b'jkoros-native> ',Spustit_2)
                    položka_Seznam=ověřit('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',položka_Seznam);assert 찾음 and int(찾음.group(2))>0,položka_Seznam
                    ověřit('free','EL0 mapped KiB: '+찾음.group(2))
                    Spustit_2=len(LOGZ_ZÁZNAM);poslat(b'top\n');dostat(b'PID SLOT STATE',Spustit_2);poslat(b'q');dostat(b'jkoros-native> ',Spustit_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_HODNOTA['df']!='df':
                        Spustit_2=len(LOGZ_ZÁZNAM);poslat((alias_HODNOTA['df'][:-1]+'\t\n').encode());dostat(b'RAM only',Spustit_2);dostat(b'jkoros-native> ',Spustit_2)
                    Zpráva_HODNOTA['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as řízení_HODNOTA:
                    řízení_HODNOTA.settimeout(15);řízení_HODNOTA.connect(str(řízení_cesta));tok_HODNOTA=řízení_HODNOTA.makefile('rwb');json.loads(tok_HODNOTA.readline());tok_HODNOTA.write(b'{"execute":"qmp_capabilities"}\n');tok_HODNOTA.flush()
                    while 'return' not in json.loads(tok_HODNOTA.readline()):pass
                    poslat((('poweroff' if argumenty.poweroff_only else alias_HODNOTA['poweroff'])+'\n').encode())
                    while True:
                        Události=json.loads(tok_HODNOTA.readline())
                        if Události.get('event')=='SHUTDOWN':break
                    assert Události['data']['guest'] and Události['data']['reason']=='guest-shutdown',Události
                    assert Proces_HODNOTA.wait(timeout=15)==0
                    Zpráva_HODNOTA['shutdown']=Události;Zpráva_HODNOTA['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Zpráva_HODNOTA['network_trace']=most_HODNOTA.protokol_trasování
                assert argumenty.poweroff_only or any(položka_HODNOTA['protocol']==1 and položka_HODNOTA['direction']=='from_guest' for položka_HODNOTA in most_HODNOTA.protokol_trasování)
                Zpráva_HODNOTA['passed']=True
            finally:
                if Proces_HODNOTA.poll() is None:os.killpg(Proces_HODNOTA.pid,signal.SIGTERM)
                try:Proces_HODNOTA.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_HODNOTA.kill();Proces_HODNOTA.wait()
                ZVOLIT_zboží.close();(výstupní_pozice/'serial.log').write_bytes(LOGZ_ZÁZNAM);(výstupní_pozice/'report.json').write_text(json.dumps(Zpráva_HODNOTA,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Klíč_HODNOTA:HODNOTA for Klíč_HODNOTA,HODNOTA in Zpráva_HODNOTA.items() if Klíč_HODNOTA!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Spustit_2()
