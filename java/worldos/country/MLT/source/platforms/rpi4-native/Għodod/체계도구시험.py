#!/usr/bin/env python3
"""attwali_data 자체 커널의 IP/ICMP, stat_VALUE query_VALUE, 현지어 kmand, 게스트 Ħruġ_programm vvalida."""
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


def serje():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    pprojetta_għerq=Path(__file__).resolve().parents[1];Settings={};isem_tabella={}
    if 인수.edition:
        나라=인수.edition.resolve();Settings=json.loads((나라/'native.json').read_text());isem_tabella=Settings['identifiers'];pprojetta_għerq=나라/Settings['source']/Settings['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        host=나라/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    Għodod=pprojetta_għerq/Path(Settings.get('runner','Għodod/eżegwixxa_kmand.py')).parent
    sys.path.insert(0,str(Għodod))
    def 읽기(isem):
        mogħdija=Għodod/(isem_tabella.get(isem,isem)+'.py');każ_VALUE=importlib.util.spec_from_file_location('test_'+isem,str(mogħdija));modulu_VALUE=importlib.util.module_from_spec(każ_VALUE);każ_VALUE.loader.exec_module(modulu_VALUE);return modulu_VALUE
    실행모듈=읽기('eżegwixxa_kmand');netwerk_modulu=읽기('netwerk_pont');kmand=getattr(실행모듈,isem_tabella.get('kmand','kmand'));pont_TYPE=getattr(netwerk_modulu,isem_tabella.get('netwerk_pont','netwerk_pont'))
    alias_VALUE=Settings.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'indirizz_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'wera_għajnuna'})
    sys.path.insert(0,str(pprojetta_għerq/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(pprojetta_għerq);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or pprojetta_għerq/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    rapport_VALUE={'passed':False,'country':Settings.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontroll_mogħdija=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));접속번호=SEARCH_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with pont_TYPE(접속번호,iġbed=True,mistieden_ADDRESS=ipTestText('10.0.2.20'),host_ADDRESS='127.0.0.2') as pont_VALUE:
            Proċess_VALUE=subprocess.Popen(kmand()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontroll_mogħdija)]+pont_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_element=selectors.DefaultSelector();CHOOSE_element.register(Proċess_VALUE.stdout,selectors.EVENT_READ)
            def 받기(wera_VALUE_487749b8,serje=0,제한=45):
                끝=time.monotonic()+제한
                while wera_VALUE_487749b8 not in LOG_RECORD[serje:]:
                    if time.monotonic()>끝 or Proċess_VALUE.poll() is not None:raise AssertionError('Missing '+repr(wera_VALUE_487749b8)+'\n'+LOG_RECORD[serje:].decode('utf-8','replace'))
                    for tast_VALUE,_ in CHOOSE_element.select(.1):
                        data=tast_VALUE.fileobj.read(65536)
                        if data:LOG_RECORD.extend(data)
                return LOG_RECORD[serje:].decode('utf-8','replace').replace('\r\n','\n')
            def bagħat(data):Proċess_VALUE.stdin.write(data);Proċess_VALUE.stdin.flush()
            def shell(SMS):
                SMS=ipTestText(SMS)
                print(rapport_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;wera_VALUE_487749b8='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';serje=len(LOG_RECORD)
                bagħat((SMS+'; echo; echo '+wera_VALUE_487749b8+'\n').encode())
                끝표시=('\r\n'+wera_VALUE_487749b8+'\r\n').encode();받기(끝표시,serje)
                ttermina_pożizzjoni=LOG_RECORD.index(끝표시,serje)+len(끝표시)
                받기(b'jkoros-native> ',ttermina_pożizzjoni)
                return LOG_RECORD[serje:].decode('utf-8','replace').replace('\r\n','\n')
            def vverifika(SMS,*값들):
                wieġeb=shell(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in wieġeb,(SMS,VALUE,wieġeb)
                return wieġeb
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    għajnuna_VALUE=vverifika('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in għajnuna_VALUE,(별칭,għajnuna_VALUE)
                    vverifika(alias_VALUE['help']+' system','Network / system')
                    vverifika('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    vverifika(alias_VALUE['ipconfig'],'inet 10.0.2.15');vverifika('ip addr show','sl0: UP');vverifika('ifconfig','sl0: UP')
                    for invalidu_Settings in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        żball=vverifika('ipconfig set '+invalidu_Settings+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in żball,żball
                        vverifika('ipconfig','inet 10.0.2.15')
                    vverifika('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    vverifika(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    vverifika('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    vverifika('ip link set dev sl0 down','sl0: DOWN');vverifika('ping -c 1 10.0.2.2; echo STATUS=$?','żball -100','STATUS=1')
                    vverifika('ipconfig up','sl0: UP')
                    vverifika(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    vverifika('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    vverifika('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');vverifika(alias_VALUE['route'],'10.0.2.2 sl0')
                    vverifika('ftpd start','FTP listening')
                    vverifika(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');vverifika('ss','LISTEN')
                    vverifika('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','żball -16')
                    with ftplib.FTP() as klijent_VALUE:
                        klijent_VALUE.connect('127.0.0.2',접속번호,timeout=20);klijent_VALUE.login();data=b'Network address was changed in the guest.\n'
                        klijent_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();klijent_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;klijent_VALUE.delete('net-state.txt')
                    vverifika('ftpd stop','FTP stopped');vverifika('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    rapport_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(vverifika('df','RAM only'));vverifika('echo disk-proof > sys-state.txt');후=저장값(vverifika(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    vverifika('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memorja_VALUE=vverifika(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memorja_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    vverifika(alias_VALUE['ps'],'kernel/shell');vverifika(alias_VALUE['uptime'],'seconds')
                    stat_informazzjoni=vverifika(alias_VALUE['top']+' -n 2','kernel/shell');assert stat_informazzjoni.count('PID SLOT STATE')==2,stat_informazzjoni
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    vverifika('terminal','TERMINAL READY');serje=len(LOG_RECORD);bagħat(b'vi process.txt\n');받기(b'NORMAL',serje)
                    serje=len(LOG_RECORD);bagħat(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',serje)
                    entrata_Lista=vverifika('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',entrata_Lista);assert 찾음 and int(찾음.group(2))>0,entrata_Lista
                    vverifika('free','EL0 mapped KiB: '+찾음.group(2))
                    serje=len(LOG_RECORD);bagħat(b'top\n');받기(b'PID SLOT STATE',serje);bagħat(b'q');받기(b'jkoros-native> ',serje)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        serje=len(LOG_RECORD);bagħat((alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',serje);받기(b'jkoros-native> ',serje)
                    rapport_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontroll_VALUE:
                    kontroll_VALUE.settimeout(15);kontroll_VALUE.connect(str(kontroll_mogħdija));Stream_VALUE=kontroll_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    bagħat((('poweroff' if 인수.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        avveniment=json.loads(Stream_VALUE.readline())
                        if avveniment.get('event')=='SHUTDOWN':break
                    assert avveniment['data']['guest'] and avveniment['data']['reason']=='guest-shutdown',avveniment
                    assert Proċess_VALUE.wait(timeout=15)==0
                    rapport_VALUE['shutdown']=avveniment;rapport_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                rapport_VALUE['network_trace']=pont_VALUE.traċċar_LOG
                assert 인수.poweroff_only or any(entrata_VALUE['protocol']==1 and entrata_VALUE['direction']=='from_guest' for entrata_VALUE in pont_VALUE.traċċar_LOG)
                rapport_VALUE['passed']=True
            finally:
                if Proċess_VALUE.poll() is None:os.killpg(Proċess_VALUE.pid,signal.SIGTERM)
                try:Proċess_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proċess_VALUE.kill();Proċess_VALUE.wait()
                CHOOSE_element.close();(출력/'serial.log').write_bytes(LOG_RECORD);(출력/'report.json').write_text(json.dumps(rapport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tast_VALUE:VALUE for tast_VALUE,VALUE in rapport_VALUE.items() if tast_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':serje()
