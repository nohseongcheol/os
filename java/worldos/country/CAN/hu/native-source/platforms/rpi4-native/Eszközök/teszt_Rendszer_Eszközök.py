#!/usr/bin/env python3
"""tényleges_adat saját 커널의 IP/ICMP, Állapot_ÉRTÉK lekérdez_ÉRTÉK, 현지어 Parancs, 게스트 kilép_app ellenőriz."""
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


def Futtatás():
    elemző_48ee4b1b=argparse.ArgumentParser();elemző_48ee4b1b.add_argument('--edition',type=Path);elemző_48ee4b1b.add_argument('--output',type=Path);elemző_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumentumok=elemző_48ee4b1b.parse_args()
    teendő_gyök=Path(__file__).resolve().parents[1];Beállítások={};név_tábla={}
    if Argumentumok.edition:
        Country_ÉRTÉK=Argumentumok.edition.resolve();Beállítások=json.loads((Country_ÉRTÉK/'native.json').read_text());név_tábla=Beállítások['identifiers'];teendő_gyök=Country_ÉRTÉK/Beállítások['source']/Beállítások['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_ÉRTÉK/'native-edition.py'),'check'])
        gazda=Country_ÉRTÉK/'host/qemu'
        if gazda.is_file():os.environ['QEMU_AARCH64']=str(gazda)
    Eszközök=teendő_gyök/Path(Beállítások.get('runner','Eszközök/végrehajt_parancs.py')).parent
    sys.path.insert(0,str(Eszközök))
    def Olvasás(Név):
        ÚTVONAL=Eszközök/(név_tábla.get(Név,Név)+'.py');szerződés_értéke=importlib.util.spec_from_file_location('test_'+Név,str(ÚTVONAL));modul_ÉRTÉK=importlib.util.module_from_spec(szerződés_értéke);szerződés_értéke.loader.exec_module(modul_ÉRTÉK);return modul_ÉRTÉK
    végrehajtás_modul=Olvasás('végrehajt_parancs');hálózat_modul=Olvasás('híd_3de4fe3a');Parancs=getattr(végrehajtás_modul,név_tábla.get('Parancs','Parancs'));híd_beír=getattr(hálózat_modul,név_tábla.get('híd_3de4fe3a','híd_3de4fe3a'))
    alias_ÉRTÉK=Beállítások.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_cím','ping':'teszt_válasz','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'bemutató_súgó'})
    sys.path.insert(0,str(teendő_gyök/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(teendő_gyök);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Kimenet=Argumentumok.output or teendő_gyök/'build/verification/system-tools';Kimenet.mkdir(parents=True,exist_ok=True)
    jelent_ÉRTÉK={'passed':False,'country':Beállítások.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_REKORD=bytearray();szekvencia_ÉRTÉK=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        vezérlő_útvonal=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as keres_ÉRTÉK:keres_ÉRTÉK.bind(('127.0.0.1',0));portszám=keres_ÉRTÉK.getsockname()[1]
            if not 50000<=portszám<=50007:break
        with híd_beír(portszám,kioszt=True,vendég_CÍM=ipTestText('10.0.2.20'),gazda_CÍM='127.0.0.2') as híd_ÉRTÉK:
            folyamat_ÉRTÉK=subprocess.Popen(Parancs()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(vezérlő_útvonal)]+híd_ÉRTÉK.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            VÁLASZT_cikk=selectors.DefaultSelector();VÁLASZT_cikk.register(folyamat_ÉRTÉK.stdout,selectors.EVENT_READ)
            def fogad(bemutató_ÉRTÉK,Futtatás=0,제한=45):
                끝=time.monotonic()+제한
                while bemutató_ÉRTÉK not in LOG_REKORD[Futtatás:]:
                    if time.monotonic()>끝 or folyamat_ÉRTÉK.poll() is not None:raise AssertionError('Missing '+repr(bemutató_ÉRTÉK)+'\n'+LOG_REKORD[Futtatás:].decode('utf-8','replace'))
                    for Kulcs_ÉRTÉK,_ in VÁLASZT_cikk.select(.1):
                        adat=Kulcs_ÉRTÉK.fileobj.read(65536)
                        if adat:LOG_REKORD.extend(adat)
                return LOG_REKORD[Futtatás:].decode('utf-8','replace').replace('\r\n','\n')
            def küld(adat):folyamat_ÉRTÉK.stdin.write(adat);folyamat_ÉRTÉK.stdin.flush()
            def felület(Szöveg):
                Szöveg=ipTestText(Szöveg)
                print(jelent_ÉRTÉK['country'],Szöveg,flush=True);szekvencia_ÉRTÉK[0]+=1;bemutató_ÉRTÉK='__SYSTEM_DONE_'+str(szekvencia_ÉRTÉK[0])+'__';Futtatás=len(LOG_REKORD)
                küld((Szöveg+'; echo; echo '+bemutató_ÉRTÉK+'\n').encode())
                megszüntet_jelölő=('\r\n'+bemutató_ÉRTÉK+'\r\n').encode();fogad(megszüntet_jelölő,Futtatás)
                megszüntet_pozíció=LOG_REKORD.index(megszüntet_jelölő,Futtatás)+len(megszüntet_jelölő)
                fogad(b'jkoros-native> ',megszüntet_pozíció)
                return LOG_REKORD[Futtatás:].decode('utf-8','replace').replace('\r\n','\n')
            def igazol(Szöveg,*값들):
                válasz=felület(Szöveg)
                for ÉRTÉK in 값들:assert ipTestText(ÉRTÉK) in válasz,(Szöveg,ÉRTÉK,válasz)
                return válasz
            try:
                fogad(b'jkoros-native> ')
                if not Argumentumok.poweroff_only:
                    súgó_ÉRTÉK=igazol('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_ÉRTÉK.values():assert 별칭 in súgó_ÉRTÉK,(별칭,súgó_ÉRTÉK)
                    igazol(alias_ÉRTÉK['help']+' system','Network / system')
                    igazol('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    igazol(alias_ÉRTÉK['ipconfig'],'inet 10.0.2.15');igazol('ip addr show','sl0: UP');igazol('ifconfig','sl0: UP')
                    for alaptalan_Gépház in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        HIBA=igazol('ipconfig set '+alaptalan_Gépház+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in HIBA,HIBA
                        igazol('ipconfig','inet 10.0.2.15')
                    igazol('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    igazol(alias_ÉRTÉK['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    igazol('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    igazol('ip link set dev sl0 down','sl0: DOWN');igazol('ping -c 1 10.0.2.2; echo STATUS=$?','HIBA -100','STATUS=1')
                    igazol('ipconfig up','sl0: UP')
                    igazol(alias_ÉRTÉK['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    igazol('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    igazol('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');igazol(alias_ÉRTÉK['route'],'10.0.2.2 sl0')
                    igazol('ftpd start','FTP listening')
                    igazol(alias_ÉRTÉK['netstat'],'10.0.2.20:21','LISTEN');igazol('ss','LISTEN')
                    igazol('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','HIBA -16')
                    with ftplib.FTP() as kliens_ÉRTÉK:
                        kliens_ÉRTÉK.connect('127.0.0.2',portszám,timeout=20);kliens_ÉRTÉK.login();adat=b'Network address was changed in the guest.\n'
                        kliens_ÉRTÉK.storbinary('STOR net-state.txt',io.BytesIO(adat));KAPOTT_adat=bytearray();kliens_ÉRTÉK.retrbinary('RETR net-state.txt',KAPOTT_adat.extend);assert KAPOTT_adat==adat;kliens_ÉRTÉK.delete('net-state.txt')
                    igazol('ftpd stop','FTP stopped');igazol('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    jelent_ÉRTÉK['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Szöveg):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Szöveg);assert 찾음,Szöveg;return tuple(map(int,찾음.groups()))
                    전=저장값(igazol('df','RAM only'));igazol('echo disk-proof > sys-state.txt');후=저장값(igazol(alias_ÉRTÉK['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    igazol('rm sys-state.txt');assert 저장값(felület('df'))==전
                    Memória_ÉRTÉK=igazol(alias_ÉRTÉK['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');mennyiség_ÉRTÉK=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memória_ÉRTÉK).groups()));assert 0<mennyiség_ÉRTÉK[1]<=mennyiség_ÉRTÉK[0] and mennyiség_ÉRTÉK[1]+mennyiség_ÉRTÉK[2]==mennyiség_ÉRTÉK[0]
                    igazol(alias_ÉRTÉK['ps'],'kernel/shell');igazol(alias_ÉRTÉK['uptime'],'seconds')
                    állapot_infó=igazol(alias_ÉRTÉK['top']+' -n 2','kernel/shell');assert állapot_infó.count('PID SLOT STATE')==2,állapot_infó
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    igazol('terminal','TERMINAL READY');Futtatás=len(LOG_REKORD);küld(b'vi process.txt\n');fogad(b'NORMAL',Futtatás)
                    Futtatás=len(LOG_REKORD);küld(bytes([30,2,1,0,0,0,0]));fogad(b'jkoros-native> ',Futtatás)
                    bejegyzés_Lista=igazol('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',bejegyzés_Lista);assert 찾음 and int(찾음.group(2))>0,bejegyzés_Lista
                    igazol('free','EL0 mapped KiB: '+찾음.group(2))
                    Futtatás=len(LOG_REKORD);küld(b'top\n');fogad(b'PID SLOT STATE',Futtatás);küld(b'q');fogad(b'jkoros-native> ',Futtatás)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_ÉRTÉK['df']!='df':
                        Futtatás=len(LOG_REKORD);küld((alias_ÉRTÉK['df'][:-1]+'\t\n').encode());fogad(b'RAM only',Futtatás);fogad(b'jkoros-native> ',Futtatás)
                    jelent_ÉRTÉK['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as vezérlő_ÉRTÉK:
                    vezérlő_ÉRTÉK.settimeout(15);vezérlő_ÉRTÉK.connect(str(vezérlő_útvonal));Stream_ÉRTÉK=vezérlő_ÉRTÉK.makefile('rwb');json.loads(Stream_ÉRTÉK.readline());Stream_ÉRTÉK.write(b'{"execute":"qmp_capabilities"}\n');Stream_ÉRTÉK.flush()
                    while 'return' not in json.loads(Stream_ÉRTÉK.readline()):pass
                    küld((('poweroff' if Argumentumok.poweroff_only else alias_ÉRTÉK['poweroff'])+'\n').encode())
                    while True:
                        Esemény=json.loads(Stream_ÉRTÉK.readline())
                        if Esemény.get('event')=='SHUTDOWN':break
                    assert Esemény['data']['guest'] and Esemény['data']['reason']=='guest-shutdown',Esemény
                    assert folyamat_ÉRTÉK.wait(timeout=15)==0
                    jelent_ÉRTÉK['shutdown']=Esemény;jelent_ÉRTÉK['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                jelent_ÉRTÉK['network_trace']=híd_ÉRTÉK.nyomkövetési_napló
                assert Argumentumok.poweroff_only or any(bejegyzés_ÉRTÉK['protocol']==1 and bejegyzés_ÉRTÉK['direction']=='from_guest' for bejegyzés_ÉRTÉK in híd_ÉRTÉK.nyomkövetési_napló)
                jelent_ÉRTÉK['passed']=True
            finally:
                if folyamat_ÉRTÉK.poll() is None:os.killpg(folyamat_ÉRTÉK.pid,signal.SIGTERM)
                try:folyamat_ÉRTÉK.wait(timeout=10)
                except subprocess.TimeoutExpired:folyamat_ÉRTÉK.kill();folyamat_ÉRTÉK.wait()
                VÁLASZT_cikk.close();(Kimenet/'serial.log').write_bytes(LOG_REKORD);(Kimenet/'report.json').write_text(json.dumps(jelent_ÉRTÉK,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kulcs_ÉRTÉK:ÉRTÉK for Kulcs_ÉRTÉK,ÉRTÉK in jelent_ÉRTÉK.items() if Kulcs_ÉRTÉK!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Futtatás()
