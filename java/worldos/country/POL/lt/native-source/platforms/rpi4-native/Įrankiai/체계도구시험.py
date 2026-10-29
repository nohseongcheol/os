#!/usr/bin/env python3
"""faktinis_duomenys savas 커널의 IP/ICMP, Būsena_VALUE užklausa_VALUE, 현지어 Komanda, 게스트 Baigti_programa_086bb533 tikrinti."""
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


def Paleisti():
    analizatorius_48ee4b1b=argparse.ArgumentParser();analizatorius_48ee4b1b.add_argument('--edition',type=Path);analizatorius_48ee4b1b.add_argument('--output',type=Path);analizatorius_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumentai=analizatorius_48ee4b1b.parse_args()
    Project_šaknis=Path(__file__).resolve().parents[1];Nustatymai={};pavadinimas_lentelė={}
    if Argumentai.edition:
        Kantri_VALUE=Argumentai.edition.resolve();Nustatymai=json.loads((Kantri_VALUE/'native.json').read_text());pavadinimas_lentelė=Nustatymai['identifiers'];Project_šaknis=Kantri_VALUE/Nustatymai['source']/Nustatymai['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Kantri_VALUE/'native-edition.py'),'check'])
        organizuoti=Kantri_VALUE/'host/qemu'
        if organizuoti.is_file():os.environ['QEMU_AARCH64']=str(organizuoti)
    Įrankiai=Project_šaknis/Path(Nustatymai.get('runner','Įrankiai/Vykdyti_komanda.py')).parent
    sys.path.insert(0,str(Įrankiai))
    def Skaitymas(Pavadinimas_2):
        KELIAS=Įrankiai/(pavadinimas_lentelė.get(Pavadinimas_2,Pavadinimas_2)+'.py');sutarties_vertė=importlib.util.spec_from_file_location('test_'+Pavadinimas_2,str(KELIAS));modulis_VALUE=importlib.util.module_from_spec(sutarties_vertė);sutarties_vertė.loader.exec_module(modulis_VALUE);return modulis_VALUE
    실행모듈=Skaitymas('Vykdyti_komanda');tinklas_modulis=Skaitymas('tiltas_3de4fe3a');Komanda=getattr(실행모듈,pavadinimas_lentelė.get('Komanda','Komanda'));tiltas_TYPE=getattr(tinklas_modulis,pavadinimas_lentelė.get('tiltas_3de4fe3a','tiltas_3de4fe3a'))
    nuoroda_VALUE_0a38607b=Nustatymai.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresas','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'laida_žinynas'})
    sys.path.insert(0,str(Project_šaknis/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_šaknis);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Išvestis=Argumentai.output or Project_šaknis/'build/verification/system-tools';Išvestis.mkdir(parents=True,exist_ok=True)
    pranešti_VALUE={'passed':False,'country':Nustatymai.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        valdymas_kelias=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Ieška_VALUE:Ieška_VALUE.bind(('127.0.0.1',0));prievado_numeris=Ieška_VALUE.getsockname()[1]
            if not 50000<=prievado_numeris<=50007:break
        with tiltas_TYPE(prievado_numeris,įrašyti=True,svečias_ADDRESS=ipTestText('10.0.2.20'),organizuoti_ADDRESS='127.0.0.2') as tiltas_VALUE:
            Procesas_VALUE=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(valdymas_kelias)]+tiltas_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_prekė=selectors.DefaultSelector();CHOOSE_prekė.register(Procesas_VALUE.stdout,selectors.EVENT_READ)
            def gauti(laida_VALUE,Paleisti=0,제한=45):
                끝=time.monotonic()+제한
                while laida_VALUE not in LOG_RECORD[Paleisti:]:
                    if time.monotonic()>끝 or Procesas_VALUE.poll() is not None:raise AssertionError('Missing '+repr(laida_VALUE)+'\n'+LOG_RECORD[Paleisti:].decode('utf-8','replace'))
                    for Raktas_VALUE,_ in CHOOSE_prekė.select(.1):
                        duomenys=Raktas_VALUE.fileobj.read(65536)
                        if duomenys:LOG_RECORD.extend(duomenys)
                return LOG_RECORD[Paleisti:].decode('utf-8','replace').replace('\r\n','\n')
            def siųsti(duomenys):Procesas_VALUE.stdin.write(duomenys);Procesas_VALUE.stdin.flush()
            def apvalkalas(Tekstas):
                Tekstas=ipTestText(Tekstas)
                print(pranešti_VALUE['country'],Tekstas,flush=True);SEQUENCE_VALUE[0]+=1;laida_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Paleisti=len(LOG_RECORD)
                siųsti((Tekstas+'; echo; echo '+laida_VALUE+'\n').encode())
                baigti_pokalbį_žymeklis=('\r\n'+laida_VALUE+'\r\n').encode();gauti(baigti_pokalbį_žymeklis,Paleisti)
                baigti_pokalbį_padėtis=LOG_RECORD.index(baigti_pokalbį_žymeklis,Paleisti)+len(baigti_pokalbį_žymeklis)
                gauti(b'jkoros-native> ',baigti_pokalbį_padėtis)
                return LOG_RECORD[Paleisti:].decode('utf-8','replace').replace('\r\n','\n')
            def patvirtinti(Tekstas,*값들):
                atsakyti=apvalkalas(Tekstas)
                for VALUE in 값들:assert ipTestText(VALUE) in atsakyti,(Tekstas,VALUE,atsakyti)
                return atsakyti
            try:
                gauti(b'jkoros-native> ')
                if not Argumentai.poweroff_only:
                    žinynas_VALUE=patvirtinti('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in nuoroda_VALUE_0a38607b.values():assert 별칭 in žinynas_VALUE,(별칭,žinynas_VALUE)
                    patvirtinti(nuoroda_VALUE_0a38607b['help']+' system','Network / system')
                    patvirtinti('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    patvirtinti(nuoroda_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');patvirtinti('ip addr show','sl0: UP');patvirtinti('ifconfig','sl0: UP')
                    for neleistinas_Parametrai in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        KLAIDA=patvirtinti('ipconfig set '+neleistinas_Parametrai+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in KLAIDA,KLAIDA
                        patvirtinti('ipconfig','inet 10.0.2.15')
                    patvirtinti('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    patvirtinti(nuoroda_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    patvirtinti('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    patvirtinti('ip link set dev sl0 down','sl0: DOWN');patvirtinti('ping -c 1 10.0.2.2; echo STATUS=$?','KLAIDA -100','STATUS=1')
                    patvirtinti('ipconfig up','sl0: UP')
                    patvirtinti(nuoroda_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    patvirtinti('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    patvirtinti('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');patvirtinti(nuoroda_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    patvirtinti('ftpd start','FTP listening')
                    patvirtinti(nuoroda_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');patvirtinti('ss','LISTEN')
                    patvirtinti('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','KLAIDA -16')
                    with ftplib.FTP() as klientas_VALUE:
                        klientas_VALUE.connect('127.0.0.2',prievado_numeris,timeout=20);klientas_VALUE.login();duomenys=b'Network address was changed in the guest.\n'
                        klientas_VALUE.storbinary('STOR net-state.txt',io.BytesIO(duomenys));RECEIVED_duomenys=bytearray();klientas_VALUE.retrbinary('RETR net-state.txt',RECEIVED_duomenys.extend);assert RECEIVED_duomenys==duomenys;klientas_VALUE.delete('net-state.txt')
                    patvirtinti('ftpd stop','FTP stopped');patvirtinti('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    pranešti_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekstas):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekstas);assert 찾음,Tekstas;return tuple(map(int,찾음.groups()))
                    전=저장값(patvirtinti('df','RAM only'));patvirtinti('echo disk-proof > sys-state.txt');후=저장값(patvirtinti(nuoroda_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    patvirtinti('rm sys-state.txt');assert 저장값(apvalkalas('df'))==전
                    atmintis_VALUE=patvirtinti(nuoroda_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');kiekis_VALUE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',atmintis_VALUE).groups()));assert 0<kiekis_VALUE[1]<=kiekis_VALUE[0] and kiekis_VALUE[1]+kiekis_VALUE[2]==kiekis_VALUE[0]
                    patvirtinti(nuoroda_VALUE_0a38607b['ps'],'kernel/shell');patvirtinti(nuoroda_VALUE_0a38607b['uptime'],'seconds')
                    būsena_informacija=patvirtinti(nuoroda_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert būsena_informacija.count('PID SLOT STATE')==2,būsena_informacija
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    patvirtinti('terminal','TERMINAL READY');Paleisti=len(LOG_RECORD);siųsti(b'vi process.txt\n');gauti(b'NORMAL',Paleisti)
                    Paleisti=len(LOG_RECORD);siųsti(bytes([30,2,1,0,0,0,0]));gauti(b'jkoros-native> ',Paleisti)
                    įrašas_Sąrašas=patvirtinti('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',įrašas_Sąrašas);assert 찾음 and int(찾음.group(2))>0,įrašas_Sąrašas
                    patvirtinti('free','EL0 mapped KiB: '+찾음.group(2))
                    Paleisti=len(LOG_RECORD);siųsti(b'top\n');gauti(b'PID SLOT STATE',Paleisti);siųsti(b'q');gauti(b'jkoros-native> ',Paleisti)
                    # Test a multibyte prefix through the real shell completion path.
                    if nuoroda_VALUE_0a38607b['df']!='df':
                        Paleisti=len(LOG_RECORD);siųsti((nuoroda_VALUE_0a38607b['df'][:-1]+'\t\n').encode());gauti(b'RAM only',Paleisti);gauti(b'jkoros-native> ',Paleisti)
                    pranešti_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as valdymas_VALUE:
                    valdymas_VALUE.settimeout(15);valdymas_VALUE.connect(str(valdymas_kelias));Stream_VALUE=valdymas_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    siųsti((('poweroff' if Argumentai.poweroff_only else nuoroda_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Įvykis=json.loads(Stream_VALUE.readline())
                        if Įvykis.get('event')=='SHUTDOWN':break
                    assert Įvykis['data']['guest'] and Įvykis['data']['reason']=='guest-shutdown',Įvykis
                    assert Procesas_VALUE.wait(timeout=15)==0
                    pranešti_VALUE['shutdown']=Įvykis;pranešti_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                pranešti_VALUE['network_trace']=tiltas_VALUE.sekimo_žurnalas
                assert Argumentai.poweroff_only or any(įrašas_VALUE['protocol']==1 and įrašas_VALUE['direction']=='from_guest' for įrašas_VALUE in tiltas_VALUE.sekimo_žurnalas)
                pranešti_VALUE['passed']=True
            finally:
                if Procesas_VALUE.poll() is None:os.killpg(Procesas_VALUE.pid,signal.SIGTERM)
                try:Procesas_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Procesas_VALUE.kill();Procesas_VALUE.wait()
                CHOOSE_prekė.close();(Išvestis/'serial.log').write_bytes(LOG_RECORD);(Išvestis/'report.json').write_text(json.dumps(pranešti_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Raktas_VALUE:VALUE for Raktas_VALUE,VALUE in pranešti_VALUE.items() if Raktas_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Paleisti()
