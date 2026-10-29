#!/usr/bin/env python3
"""tegelik_andmed oma 커널의 IP/ICMP, Olek_VALUE päring_VALUE, 현지어 Käsk, 게스트 Välju_programm valideerima."""
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


def Käivita_2():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumendid=parser_48ee4b1b.parse_args()
    Project_juur=Path(__file__).resolve().parents[1];Seaded={};nimetus_tabel={}
    if Argumendid.edition:
        Kantri_VALUE=Argumendid.edition.resolve();Seaded=json.loads((Kantri_VALUE/'native.json').read_text());nimetus_tabel=Seaded['identifiers'];Project_juur=Kantri_VALUE/Seaded['source']/Seaded['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Kantri_VALUE/'native-edition.py'),'check'])
        host=Kantri_VALUE/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    Tööriistad=Project_juur/Path(Seaded.get('runner','Tööriistad/Täida_käsk.py')).parent
    sys.path.insert(0,str(Tööriistad))
    def Lugemine(Nimi_2):
        RADA=Tööriistad/(nimetus_tabel.get(Nimi_2,Nimi_2)+'.py');lepingu_väärtus=importlib.util.spec_from_file_location('test_'+Nimi_2,str(RADA));moodul_VALUE=importlib.util.module_from_spec(lepingu_väärtus);lepingu_väärtus.loader.exec_module(moodul_VALUE);return moodul_VALUE
    실행모듈=Lugemine('Täida_käsk');võrk_moodul=Lugemine('sild_3de4fe3a');Käsk=getattr(실행모듈,nimetus_tabel.get('Käsk','Käsk'));sild_TYPE=getattr(võrk_moodul,nimetus_tabel.get('sild_3de4fe3a','sild_3de4fe3a'))
    otsetee_VALUE_0a38607b=Seaded.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_aadress','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'saade_spikker'})
    sys.path.insert(0,str(Project_juur/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_juur);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Väljund=Argumendid.output or Project_juur/'build/verification/system-tools';Väljund.mkdir(parents=True,exist_ok=True)
    aruanne_VALUE={'passed':False,'country':Seaded.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_kirje=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        meede_tee=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Otsi_VALUE:Otsi_VALUE.bind(('127.0.0.1',0));pordinumber=Otsi_VALUE.getsockname()[1]
            if not 50000<=pordinumber<=50007:break
        with sild_TYPE(pordinumber,hõivama=True,külaline_ADDRESS=ipTestText('10.0.2.20'),host_ADDRESS='127.0.0.2') as sild_VALUE:
            Joonis_VALUE=subprocess.Popen(Käsk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(meede_tee)]+sild_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_kaup=selectors.DefaultSelector();CHOOSE_kaup.register(Joonis_VALUE.stdout,selectors.EVENT_READ)
            def saama(saade_VALUE,Käivita_2=0,제한=45):
                끝=time.monotonic()+제한
                while saade_VALUE not in LOG_kirje[Käivita_2:]:
                    if time.monotonic()>끝 or Joonis_VALUE.poll() is not None:raise AssertionError('Missing '+repr(saade_VALUE)+'\n'+LOG_kirje[Käivita_2:].decode('utf-8','replace'))
                    for Võti_VALUE,_ in CHOOSE_kaup.select(.1):
                        andmed=Võti_VALUE.fileobj.read(65536)
                        if andmed:LOG_kirje.extend(andmed)
                return LOG_kirje[Käivita_2:].decode('utf-8','replace').replace('\r\n','\n')
            def saatma(andmed):Joonis_VALUE.stdin.write(andmed);Joonis_VALUE.stdin.flush()
            def kest(Tekst):
                Tekst=ipTestText(Tekst)
                print(aruanne_VALUE['country'],Tekst,flush=True);SEQUENCE_VALUE[0]+=1;saade_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Käivita_2=len(LOG_kirje)
                saatma((Tekst+'; echo; echo '+saade_VALUE+'\n').encode())
                lõpeta_kõne_marker=('\r\n'+saade_VALUE+'\r\n').encode();saama(lõpeta_kõne_marker,Käivita_2)
                lõpeta_kõne_ametikoht=LOG_kirje.index(lõpeta_kõne_marker,Käivita_2)+len(lõpeta_kõne_marker)
                saama(b'jkoros-native> ',lõpeta_kõne_ametikoht)
                return LOG_kirje[Käivita_2:].decode('utf-8','replace').replace('\r\n','\n')
            def kinnitama(Tekst,*값들):
                vastus=kest(Tekst)
                for VALUE in 값들:assert ipTestText(VALUE) in vastus,(Tekst,VALUE,vastus)
                return vastus
            try:
                saama(b'jkoros-native> ')
                if not Argumendid.poweroff_only:
                    spikker_VALUE=kinnitama('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in otsetee_VALUE_0a38607b.values():assert 별칭 in spikker_VALUE,(별칭,spikker_VALUE)
                    kinnitama(otsetee_VALUE_0a38607b['help']+' system','Network / system')
                    kinnitama('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    kinnitama(otsetee_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');kinnitama('ip addr show','sl0: UP');kinnitama('ifconfig','sl0: UP')
                    for kehtetu_Sätted in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        VIGA=kinnitama('ipconfig set '+kehtetu_Sätted+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in VIGA,VIGA
                        kinnitama('ipconfig','inet 10.0.2.15')
                    kinnitama('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    kinnitama(otsetee_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    kinnitama('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    kinnitama('ip link set dev sl0 down','sl0: DOWN');kinnitama('ping -c 1 10.0.2.2; echo STATUS=$?','VIGA -100','STATUS=1')
                    kinnitama('ipconfig up','sl0: UP')
                    kinnitama(otsetee_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    kinnitama('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    kinnitama('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');kinnitama(otsetee_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    kinnitama('ftpd start','FTP listening')
                    kinnitama(otsetee_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');kinnitama('ss','LISTEN')
                    kinnitama('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','VIGA -16')
                    with ftplib.FTP() as klient_VALUE:
                        klient_VALUE.connect('127.0.0.2',pordinumber,timeout=20);klient_VALUE.login();andmed=b'Network address was changed in the guest.\n'
                        klient_VALUE.storbinary('STOR net-state.txt',io.BytesIO(andmed));RECEIVED_andmed=bytearray();klient_VALUE.retrbinary('RETR net-state.txt',RECEIVED_andmed.extend);assert RECEIVED_andmed==andmed;klient_VALUE.delete('net-state.txt')
                    kinnitama('ftpd stop','FTP stopped');kinnitama('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    aruanne_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Tekst):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Tekst);assert 찾음,Tekst;return tuple(map(int,찾음.groups()))
                    전=저장값(kinnitama('df','RAM only'));kinnitama('echo disk-proof > sys-state.txt');후=저장값(kinnitama(otsetee_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    kinnitama('rm sys-state.txt');assert 저장값(kest('df'))==전
                    Mälu_VALUE=kinnitama(otsetee_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');kogus_VALUE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Mälu_VALUE).groups()));assert 0<kogus_VALUE[1]<=kogus_VALUE[0] and kogus_VALUE[1]+kogus_VALUE[2]==kogus_VALUE[0]
                    kinnitama(otsetee_VALUE_0a38607b['ps'],'kernel/shell');kinnitama(otsetee_VALUE_0a38607b['uptime'],'seconds')
                    olek_teave=kinnitama(otsetee_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert olek_teave.count('PID SLOT STATE')==2,olek_teave
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    kinnitama('terminal','TERMINAL READY');Käivita_2=len(LOG_kirje);saatma(b'vi process.txt\n');saama(b'NORMAL',Käivita_2)
                    Käivita_2=len(LOG_kirje);saatma(bytes([30,2,1,0,0,0,0]));saama(b'jkoros-native> ',Käivita_2)
                    kirje_Loend=kinnitama('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',kirje_Loend);assert 찾음 and int(찾음.group(2))>0,kirje_Loend
                    kinnitama('free','EL0 mapped KiB: '+찾음.group(2))
                    Käivita_2=len(LOG_kirje);saatma(b'top\n');saama(b'PID SLOT STATE',Käivita_2);saatma(b'q');saama(b'jkoros-native> ',Käivita_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if otsetee_VALUE_0a38607b['df']!='df':
                        Käivita_2=len(LOG_kirje);saatma((otsetee_VALUE_0a38607b['df'][:-1]+'\t\n').encode());saama(b'RAM only',Käivita_2);saama(b'jkoros-native> ',Käivita_2)
                    aruanne_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as meede_VALUE:
                    meede_VALUE.settimeout(15);meede_VALUE.connect(str(meede_tee));voog_VALUE=meede_VALUE.makefile('rwb');json.loads(voog_VALUE.readline());voog_VALUE.write(b'{"execute":"qmp_capabilities"}\n');voog_VALUE.flush()
                    while 'return' not in json.loads(voog_VALUE.readline()):pass
                    saatma((('poweroff' if Argumendid.poweroff_only else otsetee_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Sündmus=json.loads(voog_VALUE.readline())
                        if Sündmus.get('event')=='SHUTDOWN':break
                    assert Sündmus['data']['guest'] and Sündmus['data']['reason']=='guest-shutdown',Sündmus
                    assert Joonis_VALUE.wait(timeout=15)==0
                    aruanne_VALUE['shutdown']=Sündmus;aruanne_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                aruanne_VALUE['network_trace']=sild_VALUE.jälituslogi
                assert Argumendid.poweroff_only or any(kirje_VALUE['protocol']==1 and kirje_VALUE['direction']=='from_guest' for kirje_VALUE in sild_VALUE.jälituslogi)
                aruanne_VALUE['passed']=True
            finally:
                if Joonis_VALUE.poll() is None:os.killpg(Joonis_VALUE.pid,signal.SIGTERM)
                try:Joonis_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Joonis_VALUE.kill();Joonis_VALUE.wait()
                CHOOSE_kaup.close();(Väljund/'serial.log').write_bytes(LOG_kirje);(Väljund/'report.json').write_text(json.dumps(aruanne_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Võti_VALUE:VALUE for Võti_VALUE,VALUE in aruanne_VALUE.items() if Võti_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Käivita_2()
