#!/usr/bin/env python3
"""rzeczywisty_dane własny 커널의 IP/ICMP, Stan_WARTOŚĆ zapytanie_WARTOŚĆ, 현지어 polecenie, 게스트 wyjść_program walidować."""
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


def Uruchom_2():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumenty=parser_48ee4b1b.parse_args()
    Project_korzeń=Path(__file__).resolve().parents[1];Ustawienia={};nazwa_tabela={}
    if argumenty.edition:
        Country_WARTOŚĆ=argumenty.edition.resolve();Ustawienia=json.loads((Country_WARTOŚĆ/'native.json').read_text());nazwa_tabela=Ustawienia['identifiers'];Project_korzeń=Country_WARTOŚĆ/Ustawienia['source']/Ustawienia['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_WARTOŚĆ/'native-edition.py'),'check'])
        host=Country_WARTOŚĆ/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    narzędzia=Project_korzeń/Path(Ustawienia.get('runner','narzędzia/Wykonaj_polecenie.py')).parent
    sys.path.insert(0,str(narzędzia))
    def Odczyt(Nazwa):
        ścieżka_2=narzędzia/(nazwa_tabela.get(Nazwa,Nazwa)+'.py');wartość_kontraktu=importlib.util.spec_from_file_location('test_'+Nazwa,str(ścieżka_2));moduł_WARTOŚĆ=importlib.util.module_from_spec(wartość_kontraktu);wartość_kontraktu.loader.exec_module(moduł_WARTOŚĆ);return moduł_WARTOŚĆ
    wykonanie_moduł=Odczyt('Wykonaj_polecenie');sieć_moduł=Odczyt('mostek_3de4fe3a');polecenie=getattr(wykonanie_moduł,nazwa_tabela.get('polecenie','polecenie'));mostek_TYP=getattr(sieć_moduł,nazwa_tabela.get('mostek_3de4fe3a','mostek_3de4fe3a'))
    alias_WARTOŚĆ=Ustawienia.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adres_IP','ping':'test_odpowiedź','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'pokaż_pomoc'})
    sys.path.insert(0,str(Project_korzeń/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_korzeń);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    pozycja_wyjścia=argumenty.output or Project_korzeń/'build/verification/system-tools';pozycja_wyjścia.mkdir(parents=True,exist_ok=True)
    Raport_WARTOŚĆ={'passed':False,'country':Ustawienia.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_zapis=bytearray();SEKWENCJA_WARTOŚĆ=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrola_ścieżka=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Search_WARTOŚĆ:Search_WARTOŚĆ.bind(('127.0.0.1',0));numer_portu=Search_WARTOŚĆ.getsockname()[1]
            if not 50000<=numer_portu<=50007:break
        with mostek_TYP(numer_portu,Capture=True,gość_ADRES=ipTestText('10.0.2.20'),host_ADRES='127.0.0.2') as mostek_WARTOŚĆ:
            Proces_WARTOŚĆ=subprocess.Popen(polecenie()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrola_ścieżka)]+mostek_WARTOŚĆ.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            WYBIERZ_towar=selectors.DefaultSelector();WYBIERZ_towar.register(Proces_WARTOŚĆ.stdout,selectors.EVENT_READ)
            def odbierać(program_WARTOŚĆ,Uruchom_2=0,제한=45):
                끝=time.monotonic()+제한
                while program_WARTOŚĆ not in LOG_zapis[Uruchom_2:]:
                    if time.monotonic()>끝 or Proces_WARTOŚĆ.poll() is not None:raise AssertionError('Missing '+repr(program_WARTOŚĆ)+'\n'+LOG_zapis[Uruchom_2:].decode('utf-8','replace'))
                    for Klucz_WARTOŚĆ,_ in WYBIERZ_towar.select(.1):
                        dane=Klucz_WARTOŚĆ.fileobj.read(65536)
                        if dane:LOG_zapis.extend(dane)
                return LOG_zapis[Uruchom_2:].decode('utf-8','replace').replace('\r\n','\n')
            def wysłać(dane):Proces_WARTOŚĆ.stdin.write(dane);Proces_WARTOŚĆ.stdin.flush()
            def powłoka(tekst):
                tekst=ipTestText(tekst)
                print(Raport_WARTOŚĆ['country'],tekst,flush=True);SEKWENCJA_WARTOŚĆ[0]+=1;program_WARTOŚĆ='__SYSTEM_DONE_'+str(SEKWENCJA_WARTOŚĆ[0])+'__';Uruchom_2=len(LOG_zapis)
                wysłać((tekst+'; echo; echo '+program_WARTOŚĆ+'\n').encode())
                Koniec_pisak=('\r\n'+program_WARTOŚĆ+'\r\n').encode();odbierać(Koniec_pisak,Uruchom_2)
                Koniec_stanowisko=LOG_zapis.index(Koniec_pisak,Uruchom_2)+len(Koniec_pisak)
                odbierać(b'jkoros-native> ',Koniec_stanowisko)
                return LOG_zapis[Uruchom_2:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(tekst,*값들):
                odpowiedź=powłoka(tekst)
                for WARTOŚĆ in 값들:assert ipTestText(WARTOŚĆ) in odpowiedź,(tekst,WARTOŚĆ,odpowiedź)
                return odpowiedź
            try:
                odbierać(b'jkoros-native> ')
                if not argumenty.poweroff_only:
                    pomoc_WARTOŚĆ=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_WARTOŚĆ.values():assert 별칭 in pomoc_WARTOŚĆ,(별칭,pomoc_WARTOŚĆ)
                    확인(alias_WARTOŚĆ['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(alias_WARTOŚĆ['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for nieważny_Ustawienia in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        błąd=확인('ipconfig set '+nieważny_Ustawienia+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in błąd,błąd
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(alias_WARTOŚĆ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','błąd -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(alias_WARTOŚĆ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(alias_WARTOŚĆ['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(alias_WARTOŚĆ['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','błąd -16')
                    with ftplib.FTP() as klient_WARTOŚĆ:
                        klient_WARTOŚĆ.connect('127.0.0.2',numer_portu,timeout=20);klient_WARTOŚĆ.login();dane=b'Network address was changed in the guest.\n'
                        klient_WARTOŚĆ.storbinary('STOR net-state.txt',io.BytesIO(dane));KWOTA_WYKUP_dane=bytearray();klient_WARTOŚĆ.retrbinary('RETR net-state.txt',KWOTA_WYKUP_dane.extend);assert KWOTA_WYKUP_dane==dane;klient_WARTOŚĆ.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Raport_WARTOŚĆ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',tekst);assert 찾음,tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(alias_WARTOŚĆ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(powłoka('df'))==전
                    Pamięć_WARTOŚĆ=확인(alias_WARTOŚĆ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');ilość_WARTOŚĆ=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Pamięć_WARTOŚĆ).groups()));assert 0<ilość_WARTOŚĆ[1]<=ilość_WARTOŚĆ[0] and ilość_WARTOŚĆ[1]+ilość_WARTOŚĆ[2]==ilość_WARTOŚĆ[0]
                    확인(alias_WARTOŚĆ['ps'],'kernel/shell');확인(alias_WARTOŚĆ['uptime'],'seconds')
                    stan_informacje=확인(alias_WARTOŚĆ['top']+' -n 2','kernel/shell');assert stan_informacje.count('PID SLOT STATE')==2,stan_informacje
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');Uruchom_2=len(LOG_zapis);wysłać(b'vi process.txt\n');odbierać(b'NORMAL',Uruchom_2)
                    Uruchom_2=len(LOG_zapis);wysłać(bytes([30,2,1,0,0,0,0]));odbierać(b'jkoros-native> ',Uruchom_2)
                    wpis_Lista=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',wpis_Lista);assert 찾음 and int(찾음.group(2))>0,wpis_Lista
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    Uruchom_2=len(LOG_zapis);wysłać(b'top\n');odbierać(b'PID SLOT STATE',Uruchom_2);wysłać(b'q');odbierać(b'jkoros-native> ',Uruchom_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_WARTOŚĆ['df']!='df':
                        Uruchom_2=len(LOG_zapis);wysłać((alias_WARTOŚĆ['df'][:-1]+'\t\n').encode());odbierać(b'RAM only',Uruchom_2);odbierać(b'jkoros-native> ',Uruchom_2)
                    Raport_WARTOŚĆ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrola_WARTOŚĆ:
                    kontrola_WARTOŚĆ.settimeout(15);kontrola_WARTOŚĆ.connect(str(kontrola_ścieżka));Stream_WARTOŚĆ=kontrola_WARTOŚĆ.makefile('rwb');json.loads(Stream_WARTOŚĆ.readline());Stream_WARTOŚĆ.write(b'{"execute":"qmp_capabilities"}\n');Stream_WARTOŚĆ.flush()
                    while 'return' not in json.loads(Stream_WARTOŚĆ.readline()):pass
                    wysłać((('poweroff' if argumenty.poweroff_only else alias_WARTOŚĆ['poweroff'])+'\n').encode())
                    while True:
                        Wydarzenie=json.loads(Stream_WARTOŚĆ.readline())
                        if Wydarzenie.get('event')=='SHUTDOWN':break
                    assert Wydarzenie['data']['guest'] and Wydarzenie['data']['reason']=='guest-shutdown',Wydarzenie
                    assert Proces_WARTOŚĆ.wait(timeout=15)==0
                    Raport_WARTOŚĆ['shutdown']=Wydarzenie;Raport_WARTOŚĆ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Raport_WARTOŚĆ['network_trace']=mostek_WARTOŚĆ.dziennik_śledzenia
                assert argumenty.poweroff_only or any(wpis_WARTOŚĆ['protocol']==1 and wpis_WARTOŚĆ['direction']=='from_guest' for wpis_WARTOŚĆ in mostek_WARTOŚĆ.dziennik_śledzenia)
                Raport_WARTOŚĆ['passed']=True
            finally:
                if Proces_WARTOŚĆ.poll() is None:os.killpg(Proces_WARTOŚĆ.pid,signal.SIGTERM)
                try:Proces_WARTOŚĆ.wait(timeout=10)
                except subprocess.TimeoutExpired:Proces_WARTOŚĆ.kill();Proces_WARTOŚĆ.wait()
                WYBIERZ_towar.close();(pozycja_wyjścia/'serial.log').write_bytes(LOG_zapis);(pozycja_wyjścia/'report.json').write_text(json.dumps(Raport_WARTOŚĆ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Klucz_WARTOŚĆ:WARTOŚĆ for Klucz_WARTOŚĆ,WARTOŚĆ in Raport_WARTOŚĆ.items() if Klucz_WARTOŚĆ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Uruchom_2()
