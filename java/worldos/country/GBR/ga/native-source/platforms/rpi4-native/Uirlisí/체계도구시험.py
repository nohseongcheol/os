#!/usr/bin/env python3
"""iarbhír_sonraí 자체 커널의 IP/ICMP, staid_VALUE iarratas_VALUE, 현지어 Ordú, 게스트 scoir_clár bailíochtaigh."""
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


def Rith_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');Argóintí=해석기.parse_args()
    teilgean_fréamh=Path(__file__).resolve().parents[1];Socruithe={};ainm_tábla={}
    if Argóintí.edition:
        나라=Argóintí.edition.resolve();Socruithe=json.loads((나라/'native.json').read_text());ainm_tábla=Socruithe['identifiers'];teilgean_fréamh=나라/Socruithe['source']/Socruithe['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        óstach=나라/'host/qemu'
        if óstach.is_file():os.environ['QEMU_AARCH64']=str(óstach)
    Uirlisí=teilgean_fréamh/Path(Socruithe.get('runner','Uirlisí/Rith_ordú.py')).parent
    sys.path.insert(0,str(Uirlisí))
    def Léigh(Ainm):
        CONAIR=Uirlisí/(ainm_tábla.get(Ainm,Ainm)+'.py');cás_VALUE=importlib.util.spec_from_file_location('test_'+Ainm,str(CONAIR));modúl_VALUE=importlib.util.module_from_spec(cás_VALUE);cás_VALUE.loader.exec_module(modúl_VALUE);return modúl_VALUE
    실행모듈=Léigh('Rith_ordú');Líonra_modúl=Léigh('Líonra_traschóiritheoir');Ordú=getattr(실행모듈,ainm_tábla.get('Ordú','Ordú'));traschóiritheoir_TYPE=getattr(Líonra_modúl,ainm_tábla.get('Líonra_traschóiritheoir','Líonra_traschóiritheoir'))
    ailias_VALUE=Socruithe.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'seoladh_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'seó_cabhair'})
    sys.path.insert(0,str(teilgean_fréamh/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(teilgean_fréamh);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Aschur=Argóintí.output or teilgean_fréamh/'build/verification/system-tools';Aschur.mkdir(parents=True,exist_ok=True)
    tuairisc_VALUE={'passed':False,'country':Socruithe.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_ró=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        rialú_cosán=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));uimhir_phoirt=SEARCH_VALUE.getsockname()[1]
            if not 50000<=uimhir_phoirt<=50007:break
        with traschóiritheoir_TYPE(uimhir_phoirt,taifead=True,aoi_ADDRESS=ipTestText('10.0.2.20'),óstach_ADDRESS='127.0.0.2') as traschóiritheoir_VALUE:
            Próiseas_VALUE=subprocess.Popen(Ordú()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(rialú_cosán)]+traschóiritheoir_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_mír=selectors.DefaultSelector();CHOOSE_mír.register(Próiseas_VALUE.stdout,selectors.EVENT_READ)
            def 받기(seó_VALUE,Rith_2=0,제한=45):
                끝=time.monotonic()+제한
                while seó_VALUE not in LOG_ró[Rith_2:]:
                    if time.monotonic()>끝 or Próiseas_VALUE.poll() is not None:raise AssertionError('Missing '+repr(seó_VALUE)+'\n'+LOG_ró[Rith_2:].decode('utf-8','replace'))
                    for eochair_VALUE,_ in CHOOSE_mír.select(.1):
                        sonraí=eochair_VALUE.fileobj.read(65536)
                        if sonraí:LOG_ró.extend(sonraí)
                return LOG_ró[Rith_2:].decode('utf-8','replace').replace('\r\n','\n')
            def seol(sonraí):Próiseas_VALUE.stdin.write(sonraí);Próiseas_VALUE.stdin.flush()
            def blaosc(Téacs):
                Téacs=ipTestText(Téacs)
                print(tuairisc_VALUE['country'],Téacs,flush=True);SEQUENCE_VALUE[0]+=1;seó_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Rith_2=len(LOG_ró)
                seol((Téacs+'; echo; echo '+seó_VALUE+'\n').encode())
                끝표시=('\r\n'+seó_VALUE+'\r\n').encode();받기(끝표시,Rith_2)
                cuir_deireadh_le_suíomh=LOG_ró.index(끝표시,Rith_2)+len(끝표시)
                받기(b'jkoros-native> ',cuir_deireadh_le_suíomh)
                return LOG_ró[Rith_2:].decode('utf-8','replace').replace('\r\n','\n')
            def fíoraigh(Téacs,*값들):
                freagair=blaosc(Téacs)
                for VALUE in 값들:assert ipTestText(VALUE) in freagair,(Téacs,VALUE,freagair)
                return freagair
            try:
                받기(b'jkoros-native> ')
                if not Argóintí.poweroff_only:
                    cabhair_VALUE=fíoraigh('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ailias_VALUE.values():assert 별칭 in cabhair_VALUE,(별칭,cabhair_VALUE)
                    fíoraigh(ailias_VALUE['help']+' system','Network / system')
                    fíoraigh('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    fíoraigh(ailias_VALUE['ipconfig'],'inet 10.0.2.15');fíoraigh('ip addr show','sl0: UP');fíoraigh('ifconfig','sl0: UP')
                    for neamhbhailí_Socruithe in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ERREÁID=fíoraigh('ipconfig set '+neamhbhailí_Socruithe+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ERREÁID,ERREÁID
                        fíoraigh('ipconfig','inet 10.0.2.15')
                    fíoraigh('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    fíoraigh(ailias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    fíoraigh('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    fíoraigh('ip link set dev sl0 down','sl0: DOWN');fíoraigh('ping -c 1 10.0.2.2; echo STATUS=$?','ERREÁID -100','STATUS=1')
                    fíoraigh('ipconfig up','sl0: UP')
                    fíoraigh(ailias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    fíoraigh('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    fíoraigh('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');fíoraigh(ailias_VALUE['route'],'10.0.2.2 sl0')
                    fíoraigh('ftpd start','FTP listening')
                    fíoraigh(ailias_VALUE['netstat'],'10.0.2.20:21','LISTEN');fíoraigh('ss','LISTEN')
                    fíoraigh('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ERREÁID -16')
                    with ftplib.FTP() as cliant_VALUE:
                        cliant_VALUE.connect('127.0.0.2',uimhir_phoirt,timeout=20);cliant_VALUE.login();sonraí=b'Network address was changed in the guest.\n'
                        cliant_VALUE.storbinary('STOR net-state.txt',io.BytesIO(sonraí));RECEIVED_sonraí=bytearray();cliant_VALUE.retrbinary('RETR net-state.txt',RECEIVED_sonraí.extend);assert RECEIVED_sonraí==sonraí;cliant_VALUE.delete('net-state.txt')
                    fíoraigh('ftpd stop','FTP stopped');fíoraigh('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    tuairisc_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Téacs):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Téacs);assert 찾음,Téacs;return tuple(map(int,찾음.groups()))
                    전=저장값(fíoraigh('df','RAM only'));fíoraigh('echo disk-proof > sys-state.txt');후=저장값(fíoraigh(ailias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    fíoraigh('rm sys-state.txt');assert 저장값(blaosc('df'))==전
                    Cuimhne_VALUE=fíoraigh(ailias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Cuimhne_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    fíoraigh(ailias_VALUE['ps'],'kernel/shell');fíoraigh(ailias_VALUE['uptime'],'seconds')
                    staid_faisnéis=fíoraigh(ailias_VALUE['top']+' -n 2','kernel/shell');assert staid_faisnéis.count('PID SLOT STATE')==2,staid_faisnéis
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    fíoraigh('terminal','TERMINAL READY');Rith_2=len(LOG_ró);seol(b'vi process.txt\n');받기(b'NORMAL',Rith_2)
                    Rith_2=len(LOG_ró);seol(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Rith_2)
                    iontráil_Liosta=fíoraigh('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',iontráil_Liosta);assert 찾음 and int(찾음.group(2))>0,iontráil_Liosta
                    fíoraigh('free','EL0 mapped KiB: '+찾음.group(2))
                    Rith_2=len(LOG_ró);seol(b'top\n');받기(b'PID SLOT STATE',Rith_2);seol(b'q');받기(b'jkoros-native> ',Rith_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if ailias_VALUE['df']!='df':
                        Rith_2=len(LOG_ró);seol((ailias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Rith_2);받기(b'jkoros-native> ',Rith_2)
                    tuairisc_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as rialú_VALUE:
                    rialú_VALUE.settimeout(15);rialú_VALUE.connect(str(rialú_cosán));sruth_VALUE=rialú_VALUE.makefile('rwb');json.loads(sruth_VALUE.readline());sruth_VALUE.write(b'{"execute":"qmp_capabilities"}\n');sruth_VALUE.flush()
                    while 'return' not in json.loads(sruth_VALUE.readline()):pass
                    seol((('poweroff' if Argóintí.poweroff_only else ailias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        ócáid=json.loads(sruth_VALUE.readline())
                        if ócáid.get('event')=='SHUTDOWN':break
                    assert ócáid['data']['guest'] and ócáid['data']['reason']=='guest-shutdown',ócáid
                    assert Próiseas_VALUE.wait(timeout=15)==0
                    tuairisc_VALUE['shutdown']=ócáid;tuairisc_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                tuairisc_VALUE['network_trace']=traschóiritheoir_VALUE.rian_LOG
                assert Argóintí.poweroff_only or any(iontráil_VALUE['protocol']==1 and iontráil_VALUE['direction']=='from_guest' for iontráil_VALUE in traschóiritheoir_VALUE.rian_LOG)
                tuairisc_VALUE['passed']=True
            finally:
                if Próiseas_VALUE.poll() is None:os.killpg(Próiseas_VALUE.pid,signal.SIGTERM)
                try:Próiseas_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Próiseas_VALUE.kill();Próiseas_VALUE.wait()
                CHOOSE_mír.close();(Aschur/'serial.log').write_bytes(LOG_ró);(Aschur/'report.json').write_text(json.dumps(tuairisc_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({eochair_VALUE:VALUE for eochair_VALUE,VALUE in tuairisc_VALUE.items() if eochair_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Rith_2()
