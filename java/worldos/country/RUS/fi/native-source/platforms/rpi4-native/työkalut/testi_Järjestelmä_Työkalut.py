#!/usr/bin/env python3
"""todellinen_data oma 커널의 IP/ICMP, Tila_ARVO kysely_ARVO, 현지어 komento, 게스트 Lopeta_ohjelma vahvista."""
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


def Suorita_2():
    jäsennin_48ee4b1b=argparse.ArgumentParser();jäsennin_48ee4b1b.add_argument('--edition',type=Path);jäsennin_48ee4b1b.add_argument('--output',type=Path);jäsennin_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumentit=jäsennin_48ee4b1b.parse_args()
    aloite_juuri=Path(__file__).resolve().parents[1];Asetukset={};nimi_taulukko={}
    if argumentit.edition:
        country_ARVO=argumentit.edition.resolve();Asetukset=json.loads((country_ARVO/'native.json').read_text());nimi_taulukko=Asetukset['identifiers'];aloite_juuri=country_ARVO/Asetukset['source']/Asetukset['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(country_ARVO/'native-edition.py'),'check'])
        isäntä=country_ARVO/'host/qemu'
        if isäntä.is_file():os.environ['QEMU_AARCH64']=str(isäntä)
    työkalut=aloite_juuri/Path(Asetukset.get('runner','työkalut/Suorita_komento.py')).parent
    sys.path.insert(0,str(työkalut))
    def Luku(Nimi):
        polku_2=työkalut/(nimi_taulukko.get(Nimi,Nimi)+'.py');sopimuksen_arvo=importlib.util.spec_from_file_location('test_'+Nimi,str(polku_2));moduuli_ARVO=importlib.util.module_from_spec(sopimuksen_arvo);sopimuksen_arvo.loader.exec_module(moduuli_ARVO);return moduuli_ARVO
    suoritus_moduuli=Luku('Suorita_komento');verkko_moduuli=Luku('silta_3de4fe3a');komento=getattr(suoritus_moduuli,nimi_taulukko.get('komento','komento'));silta_TYYPPI=getattr(verkko_moduuli,nimi_taulukko.get('silta_3de4fe3a','silta_3de4fe3a'))
    alias_ARVO=Asetukset.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_osoite','ping':'testi_vastaus','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'näytä_ohje'})
    sys.path.insert(0,str(aloite_juuri/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(aloite_juuri);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    tulostuspaikka=argumentit.output or aloite_juuri/'build/verification/system-tools';tulostuspaikka.mkdir(parents=True,exist_ok=True)
    raportti_ARVO={'passed':False,'country':Asetukset.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_TIETUE=bytearray();JONO_ARVO=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ohjain_polku=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Hae_ARVO:Hae_ARVO.bind(('127.0.0.1',0));portin_numero=Hae_ARVO.getsockname()[1]
            if not 50000<=portin_numero<=50007:break
        with silta_TYYPPI(portin_numero,siepata=True,vieras_OSOITE=ipTestText('10.0.2.20'),isäntä_OSOITE='127.0.0.2') as silta_ARVO:
            prosessi_ARVO=subprocess.Popen(komento()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ohjain_polku)]+silta_ARVO.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            valita_kohde=selectors.DefaultSelector();valita_kohde.register(prosessi_ARVO.stdout,selectors.EVENT_READ)
            def saada(näyttää_ARVO,Suorita_2=0,제한=45):
                끝=time.monotonic()+제한
                while näyttää_ARVO not in LOG_TIETUE[Suorita_2:]:
                    if time.monotonic()>끝 or prosessi_ARVO.poll() is not None:raise AssertionError('Missing '+repr(näyttää_ARVO)+'\n'+LOG_TIETUE[Suorita_2:].decode('utf-8','replace'))
                    for Avain_ARVO,_ in valita_kohde.select(.1):
                        data=Avain_ARVO.fileobj.read(65536)
                        if data:LOG_TIETUE.extend(data)
                return LOG_TIETUE[Suorita_2:].decode('utf-8','replace').replace('\r\n','\n')
            def lähettää(data):prosessi_ARVO.stdin.write(data);prosessi_ARVO.stdin.flush()
            def liittymä(teksti):
                teksti=ipTestText(teksti)
                print(raportti_ARVO['country'],teksti,flush=True);JONO_ARVO[0]+=1;näyttää_ARVO='__SYSTEM_DONE_'+str(JONO_ARVO[0])+'__';Suorita_2=len(LOG_TIETUE)
                lähettää((teksti+'; echo; echo '+näyttää_ARVO+'\n').encode())
                lopettaa_puhelu_merkintä=('\r\n'+näyttää_ARVO+'\r\n').encode();saada(lopettaa_puhelu_merkintä,Suorita_2)
                lopettaa_puhelu_toimi=LOG_TIETUE.index(lopettaa_puhelu_merkintä,Suorita_2)+len(lopettaa_puhelu_merkintä)
                saada(b'jkoros-native> ',lopettaa_puhelu_toimi)
                return LOG_TIETUE[Suorita_2:].decode('utf-8','replace').replace('\r\n','\n')
            def tarkistaa(teksti,*값들):
                palaute=liittymä(teksti)
                for ARVO in 값들:assert ipTestText(ARVO) in palaute,(teksti,ARVO,palaute)
                return palaute
            try:
                saada(b'jkoros-native> ')
                if not argumentit.poweroff_only:
                    ohje_ARVO=tarkistaa('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_ARVO.values():assert 별칭 in ohje_ARVO,(별칭,ohje_ARVO)
                    tarkistaa(alias_ARVO['help']+' system','Network / system')
                    tarkistaa('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    tarkistaa(alias_ARVO['ipconfig'],'inet 10.0.2.15');tarkistaa('ip addr show','sl0: UP');tarkistaa('ifconfig','sl0: UP')
                    for pätemätön_Asetukset in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        VIRHE=tarkistaa('ipconfig set '+pätemätön_Asetukset+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in VIRHE,VIRHE
                        tarkistaa('ipconfig','inet 10.0.2.15')
                    tarkistaa('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    tarkistaa(alias_ARVO['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tarkistaa('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    tarkistaa('ip link set dev sl0 down','sl0: DOWN');tarkistaa('ping -c 1 10.0.2.2; echo STATUS=$?','VIRHE -100','STATUS=1')
                    tarkistaa('ipconfig up','sl0: UP')
                    tarkistaa(alias_ARVO['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    tarkistaa('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tarkistaa('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');tarkistaa(alias_ARVO['route'],'10.0.2.2 sl0')
                    tarkistaa('ftpd start','FTP listening')
                    tarkistaa(alias_ARVO['netstat'],'10.0.2.20:21','LISTEN');tarkistaa('ss','LISTEN')
                    tarkistaa('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','VIRHE -16')
                    with ftplib.FTP() as asiakas_ARVO:
                        asiakas_ARVO.connect('127.0.0.2',portin_numero,timeout=20);asiakas_ARVO.login();data=b'Network address was changed in the guest.\n'
                        asiakas_ARVO.storbinary('STOR net-state.txt',io.BytesIO(data));SAATU_HINTA_data=bytearray();asiakas_ARVO.retrbinary('RETR net-state.txt',SAATU_HINTA_data.extend);assert SAATU_HINTA_data==data;asiakas_ARVO.delete('net-state.txt')
                    tarkistaa('ftpd stop','FTP stopped');tarkistaa('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    raportti_ARVO['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(teksti):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',teksti);assert 찾음,teksti;return tuple(map(int,찾음.groups()))
                    전=저장값(tarkistaa('df','RAM only'));tarkistaa('echo disk-proof > sys-state.txt');후=저장값(tarkistaa(alias_ARVO['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    tarkistaa('rm sys-state.txt');assert 저장값(liittymä('df'))==전
                    Muisti_ARVO=tarkistaa(alias_ARVO['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');määrä_ARVO=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Muisti_ARVO).groups()));assert 0<määrä_ARVO[1]<=määrä_ARVO[0] and määrä_ARVO[1]+määrä_ARVO[2]==määrä_ARVO[0]
                    tarkistaa(alias_ARVO['ps'],'kernel/shell');tarkistaa(alias_ARVO['uptime'],'seconds')
                    tila_info=tarkistaa(alias_ARVO['top']+' -n 2','kernel/shell');assert tila_info.count('PID SLOT STATE')==2,tila_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    tarkistaa('terminal','TERMINAL READY');Suorita_2=len(LOG_TIETUE);lähettää(b'vi process.txt\n');saada(b'NORMAL',Suorita_2)
                    Suorita_2=len(LOG_TIETUE);lähettää(bytes([30,2,1,0,0,0,0]));saada(b'jkoros-native> ',Suorita_2)
                    merkintä_luettelo=tarkistaa('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',merkintä_luettelo);assert 찾음 and int(찾음.group(2))>0,merkintä_luettelo
                    tarkistaa('free','EL0 mapped KiB: '+찾음.group(2))
                    Suorita_2=len(LOG_TIETUE);lähettää(b'top\n');saada(b'PID SLOT STATE',Suorita_2);lähettää(b'q');saada(b'jkoros-native> ',Suorita_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_ARVO['df']!='df':
                        Suorita_2=len(LOG_TIETUE);lähettää((alias_ARVO['df'][:-1]+'\t\n').encode());saada(b'RAM only',Suorita_2);saada(b'jkoros-native> ',Suorita_2)
                    raportti_ARVO['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ohjain_ARVO:
                    ohjain_ARVO.settimeout(15);ohjain_ARVO.connect(str(ohjain_polku));virta_ARVO=ohjain_ARVO.makefile('rwb');json.loads(virta_ARVO.readline());virta_ARVO.write(b'{"execute":"qmp_capabilities"}\n');virta_ARVO.flush()
                    while 'return' not in json.loads(virta_ARVO.readline()):pass
                    lähettää((('poweroff' if argumentit.poweroff_only else alias_ARVO['poweroff'])+'\n').encode())
                    while True:
                        Tapahtuma=json.loads(virta_ARVO.readline())
                        if Tapahtuma.get('event')=='SHUTDOWN':break
                    assert Tapahtuma['data']['guest'] and Tapahtuma['data']['reason']=='guest-shutdown',Tapahtuma
                    assert prosessi_ARVO.wait(timeout=15)==0
                    raportti_ARVO['shutdown']=Tapahtuma;raportti_ARVO['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                raportti_ARVO['network_trace']=silta_ARVO.tapahtumaloki
                assert argumentit.poweroff_only or any(merkintä_ARVO_962f286b['protocol']==1 and merkintä_ARVO_962f286b['direction']=='from_guest' for merkintä_ARVO_962f286b in silta_ARVO.tapahtumaloki)
                raportti_ARVO['passed']=True
            finally:
                if prosessi_ARVO.poll() is None:os.killpg(prosessi_ARVO.pid,signal.SIGTERM)
                try:prosessi_ARVO.wait(timeout=10)
                except subprocess.TimeoutExpired:prosessi_ARVO.kill();prosessi_ARVO.wait()
                valita_kohde.close();(tulostuspaikka/'serial.log').write_bytes(LOG_TIETUE);(tulostuspaikka/'report.json').write_text(json.dumps(raportti_ARVO,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Avain_ARVO:ARVO for Avain_ARVO,ARVO in raportti_ARVO.items() if Avain_ARVO!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Suorita_2()
