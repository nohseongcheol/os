#!/usr/bin/env python3
"""laatii_keɓe 자체 커널의 IP/ICMP, ngonka_njaru ɗaɓɓal_njaru, 현지어 ginol, 게스트 yaltude_tafirde 검증."""
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


def huutoraade():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];설정={};innde_taabal={}
    if 인수.edition:
        나라=인수.edition.resolve();설정=json.loads((나라/'native.json').read_text());innde_taabal=설정['identifiers'];기준=나라/설정['source']/설정['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        njaatigi=나라/'host/qemu'
        if njaatigi.is_file():os.environ['QEMU_AARCH64']=str(njaatigi)
    도구=기준/Path(설정.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def 읽기(innde):
        laawol=도구/(innde_taabal.get(innde,innde)+'.py');haaju_njaru=importlib.util.spec_from_file_location('test_'+innde,str(laawol));모듈=importlib.util.module_from_spec(haaju_njaru);haaju_njaru.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('실행');망모듈=읽기('통신다리');ginol=getattr(실행모듈,innde_taabal.get('ginol','ginol'));다리형=getattr(망모듈,innde_taabal.get('통신다리','통신다리'))
    alias_njaru=설정.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ñiiɓirde_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'hollirde_ballal'})
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
    ciimtol_njaru={'passed':False,'country':설정.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    suurnal_winndande=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        yuurnitorde_laawol=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as njiilawu_njaru:njiilawu_njaru.bind(('127.0.0.1',0));접속번호=njiilawu_njaru.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),njaatigi_ñiiɓirde='127.0.0.2') as 다리:
            Yuɓɓo_golle_njaru=subprocess.Popen(ginol()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(yuurnitorde_laawol)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            labaade_geɗal=selectors.DefaultSelector();labaade_geɗal.register(Yuɓɓo_golle_njaru.stdout,selectors.EVENT_READ)
            def 받기(hollirde_njaru,huutoraade=0,제한=45):
                끝=time.monotonic()+제한
                while hollirde_njaru not in suurnal_winndande[huutoraade:]:
                    if time.monotonic()>끝 or Yuɓɓo_golle_njaru.poll() is not None:raise AssertionError('Missing '+repr(hollirde_njaru)+'\n'+suurnal_winndande[huutoraade:].decode('utf-8','replace'))
                    for kelal_njaru,_ in labaade_geɗal.select(.1):
                        keɓe=kelal_njaru.fileobj.read(65536)
                        if keɓe:suurnal_winndande.extend(keɓe)
                return suurnal_winndande[huutoraade:].decode('utf-8','replace').replace('\r\n','\n')
            def neldude(keɓe):Yuɓɓo_golle_njaru.stdin.write(keɓe);Yuɓɓo_golle_njaru.stdin.flush()
            def laalagal(binndi):
                binndi=ipTestText(binndi)
                print(ciimtol_njaru['country'],binndi,flush=True);차례[0]+=1;hollirde_njaru='__SYSTEM_DONE_'+str(차례[0])+'__';huutoraade=len(suurnal_winndande)
                neldude((binndi+'; echo; echo '+hollirde_njaru+'\n').encode())
                끝표시=('\r\n'+hollirde_njaru+'\r\n').encode();받기(끝표시,huutoraade)
                끝자리=suurnal_winndande.index(끝표시,huutoraade)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return suurnal_winndande[huutoraade:].decode('utf-8','replace').replace('\r\n','\n')
            def ƴeewtaade(binndi,*값들):
                응답=laalagal(binndi)
                for njaru in 값들:assert ipTestText(njaru) in 응답,(binndi,njaru,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ballal_njaru=ƴeewtaade('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_njaru.values():assert 별칭 in ballal_njaru,(별칭,ballal_njaru)
                    ƴeewtaade(alias_njaru['help']+' system','Network / system')
                    ƴeewtaade('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ƴeewtaade(alias_njaru['ipconfig'],'inet 10.0.2.15');ƴeewtaade('ip addr show','sl0: UP');ƴeewtaade('ifconfig','sl0: UP')
                    for 잘못된설정 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        juumre=ƴeewtaade('ipconfig set '+잘못된설정+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in juumre,juumre
                        ƴeewtaade('ipconfig','inet 10.0.2.15')
                    ƴeewtaade('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ƴeewtaade(alias_njaru['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ƴeewtaade('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ƴeewtaade('ip link set dev sl0 down','sl0: DOWN');ƴeewtaade('ping -c 1 10.0.2.2; echo STATUS=$?','juumre -100','STATUS=1')
                    ƴeewtaade('ipconfig up','sl0: UP')
                    ƴeewtaade(alias_njaru['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ƴeewtaade('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ƴeewtaade('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ƴeewtaade(alias_njaru['route'],'10.0.2.2 sl0')
                    ƴeewtaade('ftpd start','FTP listening')
                    ƴeewtaade(alias_njaru['netstat'],'10.0.2.20:21','LISTEN');ƴeewtaade('ss','LISTEN')
                    ƴeewtaade('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','juumre -16')
                    with ftplib.FTP() as kiliyaan_njaru:
                        kiliyaan_njaru.connect('127.0.0.2',접속번호,timeout=20);kiliyaan_njaru.login();keɓe=b'Network address was changed in the guest.\n'
                        kiliyaan_njaru.storbinary('STOR net-state.txt',io.BytesIO(keɓe));받은자료=bytearray();kiliyaan_njaru.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==keɓe;kiliyaan_njaru.delete('net-state.txt')
                    ƴeewtaade('ftpd stop','FTP stopped');ƴeewtaade('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ciimtol_njaru['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(binndi):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',binndi);assert 찾음,binndi;return tuple(map(int,찾음.groups()))
                    전=저장값(ƴeewtaade('df','RAM only'));ƴeewtaade('echo disk-proof > sys-state.txt');후=저장값(ƴeewtaade(alias_njaru['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ƴeewtaade('rm sys-state.txt');assert 저장값(laalagal('df'))==전
                    teskordu_njaru=ƴeewtaade(alias_njaru['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',teskordu_njaru).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ƴeewtaade(alias_njaru['ps'],'kernel/shell');ƴeewtaade(alias_njaru['uptime'],'seconds')
                    ngonka_kumpital=ƴeewtaade(alias_njaru['top']+' -n 2','kernel/shell');assert ngonka_kumpital.count('PID SLOT STATE')==2,ngonka_kumpital
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ƴeewtaade('terminal','TERMINAL READY');huutoraade=len(suurnal_winndande);neldude(b'vi process.txt\n');받기(b'NORMAL',huutoraade)
                    huutoraade=len(suurnal_winndande);neldude(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',huutoraade)
                    naatnugol_Doggol=ƴeewtaade('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',naatnugol_Doggol);assert 찾음 and int(찾음.group(2))>0,naatnugol_Doggol
                    ƴeewtaade('free','EL0 mapped KiB: '+찾음.group(2))
                    huutoraade=len(suurnal_winndande);neldude(b'top\n');받기(b'PID SLOT STATE',huutoraade);neldude(b'q');받기(b'jkoros-native> ',huutoraade)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_njaru['df']!='df':
                        huutoraade=len(suurnal_winndande);neldude((alias_njaru['df'][:-1]+'\t\n').encode());받기(b'RAM only',huutoraade);받기(b'jkoros-native> ',huutoraade)
                    ciimtol_njaru['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as yuurnitorde_njaru:
                    yuurnitorde_njaru.settimeout(15);yuurnitorde_njaru.connect(str(yuurnitorde_laawol));waraango_njaru=yuurnitorde_njaru.makefile('rwb');json.loads(waraango_njaru.readline());waraango_njaru.write(b'{"execute":"qmp_capabilities"}\n');waraango_njaru.flush()
                    while 'return' not in json.loads(waraango_njaru.readline()):pass
                    neldude((('poweroff' if 인수.poweroff_only else alias_njaru['poweroff'])+'\n').encode())
                    while True:
                        saɗteende=json.loads(waraango_njaru.readline())
                        if saɗteende.get('event')=='SHUTDOWN':break
                    assert saɗteende['data']['guest'] and saɗteende['data']['reason']=='guest-shutdown',saɗteende
                    assert Yuɓɓo_golle_njaru.wait(timeout=15)==0
                    ciimtol_njaru['shutdown']=saɗteende;ciimtol_njaru['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ciimtol_njaru['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(naatnugol_njaru['protocol']==1 and naatnugol_njaru['direction']=='from_guest' for naatnugol_njaru in 다리.추적기록)
                ciimtol_njaru['passed']=True
            finally:
                if Yuɓɓo_golle_njaru.poll() is None:os.killpg(Yuɓɓo_golle_njaru.pid,signal.SIGTERM)
                try:Yuɓɓo_golle_njaru.wait(timeout=10)
                except subprocess.TimeoutExpired:Yuɓɓo_golle_njaru.kill();Yuɓɓo_golle_njaru.wait()
                labaade_geɗal.close();(출력/'serial.log').write_bytes(suurnal_winndande);(출력/'report.json').write_text(json.dumps(ciimtol_njaru,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({kelal_njaru:njaru for kelal_njaru,njaru in ciimtol_njaru.items() if kelal_njaru!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':huutoraade()
