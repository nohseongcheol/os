#!/usr/bin/env python3
"""실제 자체 커널의 IP/ICMP, jamakua_iparülein_ajutuu asakiriaa_ajutuu, 현지어 aluwataaya, 게스트 aju_itaa_akumajiaa 검증."""
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


def 시작():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];설정={};이름표={}
    if 인수.edition:
        나라=인수.edition.resolve();설정=json.loads((나라/'native.json').read_text());이름표=설정['identifiers'];기준=나라/설정['source']/설정['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        epiajatü=나라/'host/qemu'
        if epiajatü.is_file():os.environ['QEMU_AARCH64']=str(epiajatü)
    도구=기준/Path(설정.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def 읽기(이름):
        wopu_a_ttaaleemüin=도구/(이름표.get(이름,이름)+'.py');achikii_ajutuu=importlib.util.spec_from_file_location('test_'+이름,str(wopu_a_ttaaleemüin));모듈=importlib.util.module_from_spec(achikii_ajutuu);achikii_ajutuu.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('실행');망모듈=읽기('통신다리');aluwataaya=getattr(실행모듈,이름표.get('aluwataaya','aluwataaya'));다리형=getattr(망모듈,이름표.get('통신다리','통신다리'))
    anülieeyaa_ajutuu=설정.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ejepüsee_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'도움말'})
    sys.path.insert(0,str(기준/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(기준);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or 기준/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    achikiimaajatü_ajutuu={'passed':False,'country':설정.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    aa_innachikimaajatü_aparatsee=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        aa_inmajia_wopu_a_ttaaleemüin=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Achajaaya_ajutuu:Achajaaya_ajutuu.bind(('127.0.0.1',0));접속번호=Achajaaya_ajutuu.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),epiajatü_ejepüsee='127.0.0.2') as 다리:
            과정=subprocess.Popen(aluwataaya()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(aa_inmajia_wopu_a_ttaaleemüin)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            aapawaa_apüshii=selectors.DefaultSelector();aapawaa_apüshii.register(과정.stdout,selectors.EVENT_READ)
            def 받기(표시,시작=0,제한=45):
                끝=time.monotonic()+제한
                while 표시 not in aa_innachikimaajatü_aparatsee[시작:]:
                    if time.monotonic()>끝 or 과정.poll() is not None:raise AssertionError('Missing '+repr(표시)+'\n'+aa_innachikimaajatü_aparatsee[시작:].decode('utf-8','replace'))
                    for ajüttia_ajutuu,_ in aapawaa_apüshii.select(.1):
                        atijaaya=ajüttia_ajutuu.fileobj.read(65536)
                        if atijaaya:aa_innachikimaajatü_aparatsee.extend(atijaaya)
                return aa_innachikimaajatü_aparatsee[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def ajütaa(atijaaya):과정.stdin.write(atijaaya);과정.stdin.flush()
            def aluwataalapu_u(글):
                글=ipTestText(글)
                print(achikiimaajatü_ajutuu['country'],글,flush=True);차례[0]+=1;표시='__SYSTEM_DONE_'+str(차례[0])+'__';시작=len(aa_innachikimaajatü_aparatsee)
                ajütaa((글+'; echo; echo '+표시+'\n').encode())
                끝표시=('\r\n'+표시+'\r\n').encode();받기(끝표시,시작)
                끝자리=aa_innachikimaajatü_aparatsee.index(끝표시,시작)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return aa_innachikimaajatü_aparatsee[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(글,*값들):
                응답=aluwataalapu_u(글)
                for ajutuu in 값들:assert ipTestText(ajutuu) in 응답,(글,ajutuu,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    akaaliijiaa_ajutuu_8d901cc2=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in anülieeyaa_ajutuu.values():assert 별칭 in akaaliijiaa_ajutuu_8d901cc2,(별칭,akaaliijiaa_ajutuu_8d901cc2)
                    확인(anülieeyaa_ajutuu['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(anülieeyaa_ajutuu['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for 잘못된설정 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ajachitia=확인('ipconfig set '+잘못된설정+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ajachitia,ajachitia
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(anülieeyaa_ajutuu['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','ajachitia -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(anülieeyaa_ajutuu['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(anülieeyaa_ajutuu['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(anülieeyaa_ajutuu['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ajachitia -16')
                    with ftplib.FTP() as matchanta_ajutuu:
                        matchanta_ajutuu.connect('127.0.0.2',접속번호,timeout=20);matchanta_ajutuu.login();atijaaya=b'Network address was changed in the guest.\n'
                        matchanta_ajutuu.storbinary('STOR net-state.txt',io.BytesIO(atijaaya));받은자료=bytearray();matchanta_ajutuu.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==atijaaya;matchanta_ajutuu.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    achikiimaajatü_ajutuu['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(글):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',글);assert 찾음,글;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(anülieeyaa_ajutuu['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(aluwataalapu_u('df'))==전
                    기억=확인(anülieeyaa_ajutuu['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',기억).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    확인(anülieeyaa_ajutuu['ps'],'kernel/shell');확인(anülieeyaa_ajutuu['uptime'],'seconds')
                    현황=확인(anülieeyaa_ajutuu['top']+' -n 2','kernel/shell');assert 현황.count('PID SLOT STATE')==2,현황
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');시작=len(aa_innachikimaajatü_aparatsee);ajütaa(b'vi process.txt\n');받기(b'NORMAL',시작)
                    시작=len(aa_innachikimaajatü_aparatsee);ajütaa(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',시작)
                    목록=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',목록);assert 찾음 and int(찾음.group(2))>0,목록
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    시작=len(aa_innachikimaajatü_aparatsee);ajütaa(b'top\n');받기(b'PID SLOT STATE',시작);ajütaa(b'q');받기(b'jkoros-native> ',시작)
                    # Test a multibyte prefix through the real shell completion path.
                    if anülieeyaa_ajutuu['df']!='df':
                        시작=len(aa_innachikimaajatü_aparatsee);ajütaa((anülieeyaa_ajutuu['df'][:-1]+'\t\n').encode());받기(b'RAM only',시작);받기(b'jkoros-native> ',시작)
                    achikiimaajatü_ajutuu['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as aa_inmajia_ajutuu:
                    aa_inmajia_ajutuu.settimeout(15);aa_inmajia_ajutuu.connect(str(aa_inmajia_wopu_a_ttaaleemüin));palantüsü_ajutuu=aa_inmajia_ajutuu.makefile('rwb');json.loads(palantüsü_ajutuu.readline());palantüsü_ajutuu.write(b'{"execute":"qmp_capabilities"}\n');palantüsü_ajutuu.flush()
                    while 'return' not in json.loads(palantüsü_ajutuu.readline()):pass
                    ajütaa((('poweroff' if 인수.poweroff_only else anülieeyaa_ajutuu['poweroff'])+'\n').encode())
                    while True:
                        kasachiki=json.loads(palantüsü_ajutuu.readline())
                        if kasachiki.get('event')=='SHUTDOWN':break
                    assert kasachiki['data']['guest'] and kasachiki['data']['reason']=='guest-shutdown',kasachiki
                    assert 과정.wait(timeout=15)==0
                    achikiimaajatü_ajutuu['shutdown']=kasachiki;achikiimaajatü_ajutuu['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                achikiimaajatü_ajutuu['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(ekeroliaa_ajutuu['protocol']==1 and ekeroliaa_ajutuu['direction']=='from_guest' for ekeroliaa_ajutuu in 다리.추적기록)
                achikiimaajatü_ajutuu['passed']=True
            finally:
                if 과정.poll() is None:os.killpg(과정.pid,signal.SIGTERM)
                try:과정.wait(timeout=10)
                except subprocess.TimeoutExpired:과정.kill();과정.wait()
                aapawaa_apüshii.close();(출력/'serial.log').write_bytes(aa_innachikimaajatü_aparatsee);(출력/'report.json').write_text(json.dumps(achikiimaajatü_ajutuu,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ajüttia_ajutuu:ajutuu for ajüttia_ajutuu,ajutuu in achikiimaajatü_ajutuu.items() if ajüttia_ajutuu!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':시작()
