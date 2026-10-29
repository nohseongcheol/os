#!/usr/bin/env python3
"""వాస్తవ_డేటా 자체 커널의 IP/ICMP, స్థితి_మూల్యం ప్రశ్న_మూల్యం, 현지어 ఆదేశము, 게스트 నిష్క్రమణ_అనువర్తనం నిర్థారీకరించు."""
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


def నడుపుము():
    పార్సర్_48ee4b1b=argparse.ArgumentParser();పార్సర్_48ee4b1b.add_argument('--edition',type=Path);పార్సర్_48ee4b1b.add_argument('--output',type=Path);పార్సర్_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=పార్సర్_48ee4b1b.parse_args()
    ప్రొజెక్ట్_మూలం=Path(__file__).resolve().parents[1];అమరికలు={};పేరు_పట్టిక={}
    if 인수.edition:
        나라=인수.edition.resolve();అమరికలు=json.loads((나라/'native.json').read_text());పేరు_పట్టిక=అమరికలు['identifiers'];ప్రొజెక్ట్_మూలం=나라/అమరికలు['source']/అమరికలు['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        హోస్ట్=나라/'host/qemu'
        if హోస్ట్.is_file():os.environ['QEMU_AARCH64']=str(హోస్ట్)
    ఉపకరణాలు=ప్రొజెక్ట్_మూలం/Path(అమరికలు.get('runner','ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py')).parent
    sys.path.insert(0,str(ఉపకరణాలు))
    def చదువు(పేరు):
        పాత్=ఉపకరణాలు/(పేరు_పట్టిక.get(పేరు,పేరు)+'.py');పని_మూల్యం_102996da=importlib.util.spec_from_file_location('test_'+పేరు,str(పాత్));మాడ్యూల్_మూల్యం=importlib.util.module_from_spec(పని_మూల్యం_102996da);పని_మూల్యం_102996da.loader.exec_module(మాడ్యూల్_మూల్యం);return మాడ్యూల్_మూల్యం
    실행모듈=చదువు('అమలు_చేయి_ఆదేశం');నెట్_వర్క్_మాడ్యూల్=చదువు('నెట్_వర్క్_బ్రిడ్జ్');ఆదేశము=getattr(실행모듈,పేరు_పట్టిక.get('ఆదేశము','ఆదేశము'));బ్రిడ్జ్_టైప్_చేయండి=getattr(నెట్_వర్క్_మాడ్యూల్,పేరు_పట్టిక.get('నెట్_వర్క్_బ్రిడ్జ్','నెట్_వర్క్_బ్రిడ్జ్'))
    మారుపేరు_మూల్యం=అమరికలు.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_చిరునామా','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'చూపించు_సహాయం'})
    sys.path.insert(0,str(ప్రొజెక్ట్_మూలం/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ప్రొజెక్ట్_మూలం);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    అవుట్పుట్=인수.output or ప్రొజెక్ట్_మూలం/'build/verification/system-tools';అవుట్పుట్.mkdir(parents=True,exist_ok=True)
    నివేదిక_మూల్యం={'passed':False,'country':అమరికలు.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    లాగ్_వరుస=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        నియంత్రణ_పథం=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as శోధన_మూల్యం:శోధన_మూల్యం.bind(('127.0.0.1',0));పోర్ట్_సంఖ్య=శోధన_మూల్యం.getsockname()[1]
            if not 50000<=పోర్ట్_సంఖ్య<=50007:break
        with బ్రిడ్జ్_టైప్_చేయండి(పోర్ట్_సంఖ్య,సంగ్రహణ=True,అతిథి_ఇమెయిల్=ipTestText('10.0.2.20'),హోస్ట్_ఇమెయిల్='127.0.0.2') as బ్రిడ్జ్_మూల్యం:
            విధానం_మూల్యం=subprocess.Popen(ఆదేశము()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(నియంత్రణ_పథం)]+బ్రిడ్జ్_మూల్యం.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ఎంచు_అంశం=selectors.DefaultSelector();ఎంచు_అంశం.register(విధానం_మూల్యం.stdout,selectors.EVENT_READ)
            def 받기(చూపించు_మూల్యం,నడుపుము=0,제한=45):
                끝=time.monotonic()+제한
                while చూపించు_మూల్యం not in లాగ్_వరుస[నడుపుము:]:
                    if time.monotonic()>끝 or విధానం_మూల్యం.poll() is not None:raise AssertionError('Missing '+repr(చూపించు_మూల్యం)+'\n'+లాగ్_వరుస[నడుపుము:].decode('utf-8','replace'))
                    for కీ_మూల్యం,_ in ఎంచు_అంశం.select(.1):
                        డేటా=కీ_మూల్యం.fileobj.read(65536)
                        if డేటా:లాగ్_వరుస.extend(డేటా)
                return లాగ్_వరుస[నడుపుము:].decode('utf-8','replace').replace('\r\n','\n')
            def పంపు(డేటా):విధానం_మూల్యం.stdin.write(డేటా);విధానం_మూల్యం.stdin.flush()
            def షెల్(పాఠ్యము):
                పాఠ్యము=ipTestText(పాఠ్యము)
                print(నివేదిక_మూల్యం['country'],పాఠ్యము,flush=True);차례[0]+=1;చూపించు_మూల్యం='__SYSTEM_DONE_'+str(차례[0])+'__';నడుపుము=len(లాగ్_వరుస)
                పంపు((పాఠ్యము+'; echo; echo '+చూపించు_మూల్యం+'\n').encode())
                끝표시=('\r\n'+చూపించు_మూల్యం+'\r\n').encode();받기(끝표시,నడుపుము)
                ముగించు_స్థాయి=లాగ్_వరుస.index(끝표시,నడుపుము)+len(끝표시)
                받기(b'jkoros-native> ',ముగించు_స్థాయి)
                return లాగ్_వరుస[నడుపుము:].decode('utf-8','replace').replace('\r\n','\n')
            def సరిచూడు(పాఠ్యము,*값들):
                ప్రత్యుత్తరం_ఇవ్వు=షెల్(పాఠ్యము)
                for మూల్యం in 값들:assert ipTestText(మూల్యం) in ప్రత్యుత్తరం_ఇవ్వు,(పాఠ్యము,మూల్యం,ప్రత్యుత్తరం_ఇవ్వు)
                return ప్రత్యుత్తరం_ఇవ్వు
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    సహాయం_మూల్యం=సరిచూడు('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in మారుపేరు_మూల్యం.values():assert 별칭 in సహాయం_మూల్యం,(별칭,సహాయం_మూల్యం)
                    సరిచూడు(మారుపేరు_మూల్యం['help']+' system','Network / system')
                    సరిచూడు('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    సరిచూడు(మారుపేరు_మూల్యం['ipconfig'],'inet 10.0.2.15');సరిచూడు('ip addr show','sl0: UP');సరిచూడు('ifconfig','sl0: UP')
                    for చెల్లని_సెట్టింగ్_లు in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        దోషం=సరిచూడు('ipconfig set '+చెల్లని_సెట్టింగ్_లు+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in దోషం,దోషం
                        సరిచూడు('ipconfig','inet 10.0.2.15')
                    సరిచూడు('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    సరిచూడు(మారుపేరు_మూల్యం['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    సరిచూడు('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    సరిచూడు('ip link set dev sl0 down','sl0: DOWN');సరిచూడు('ping -c 1 10.0.2.2; echo STATUS=$?','దోషం -100','STATUS=1')
                    సరిచూడు('ipconfig up','sl0: UP')
                    సరిచూడు(మారుపేరు_మూల్యం['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    సరిచూడు('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    సరిచూడు('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');సరిచూడు(మారుపేరు_మూల్యం['route'],'10.0.2.2 sl0')
                    సరిచూడు('ftpd start','FTP listening')
                    సరిచూడు(మారుపేరు_మూల్యం['netstat'],'10.0.2.20:21','LISTEN');సరిచూడు('ss','LISTEN')
                    సరిచూడు('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','దోషం -16')
                    with ftplib.FTP() as క్లయింట్_మూల్యం:
                        క్లయింట్_మూల్యం.connect('127.0.0.2',పోర్ట్_సంఖ్య,timeout=20);క్లయింట్_మూల్యం.login();డేటా=b'Network address was changed in the guest.\n'
                        క్లయింట్_మూల్యం.storbinary('STOR net-state.txt',io.BytesIO(డేటా));받은자료=bytearray();క్లయింట్_మూల్యం.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==డేటా;క్లయింట్_మూల్యం.delete('net-state.txt')
                    సరిచూడు('ftpd stop','FTP stopped');సరిచూడు('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    నివేదిక_మూల్యం['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(పాఠ్యము):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',పాఠ్యము);assert 찾음,పాఠ్యము;return tuple(map(int,찾음.groups()))
                    전=저장값(సరిచూడు('df','RAM only'));సరిచూడు('echo disk-proof > sys-state.txt');후=저장값(సరిచూడు(మారుపేరు_మూల్యం['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    సరిచూడు('rm sys-state.txt');assert 저장값(షెల్('df'))==전
                    మెమరీ_మూల్యం=సరిచూడు(మారుపేరు_మూల్యం['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',మెమరీ_మూల్యం).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    సరిచూడు(మారుపేరు_మూల్యం['ps'],'kernel/shell');సరిచూడు(మారుపేరు_మూల్యం['uptime'],'seconds')
                    లభ్యత_సమాచారం=సరిచూడు(మారుపేరు_మూల్యం['top']+' -n 2','kernel/shell');assert లభ్యత_సమాచారం.count('PID SLOT STATE')==2,లభ్యత_సమాచారం
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    సరిచూడు('terminal','TERMINAL READY');నడుపుము=len(లాగ్_వరుస);పంపు(b'vi process.txt\n');받기(b'NORMAL',నడుపుము)
                    నడుపుము=len(లాగ్_వరుస);పంపు(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',నడుపుము)
                    ప్రవేశం_జాబితా=సరిచూడు('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ప్రవేశం_జాబితా);assert 찾음 and int(찾음.group(2))>0,ప్రవేశం_జాబితా
                    సరిచూడు('free','EL0 mapped KiB: '+찾음.group(2))
                    నడుపుము=len(లాగ్_వరుస);పంపు(b'top\n');받기(b'PID SLOT STATE',నడుపుము);పంపు(b'q');받기(b'jkoros-native> ',నడుపుము)
                    # Test a multibyte prefix through the real shell completion path.
                    if మారుపేరు_మూల్యం['df']!='df':
                        నడుపుము=len(లాగ్_వరుస);పంపు((మారుపేరు_మూల్యం['df'][:-1]+'\t\n').encode());받기(b'RAM only',నడుపుము);받기(b'jkoros-native> ',నడుపుము)
                    నివేదిక_మూల్యం['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as నియంత్రణ_మూల్యం:
                    నియంత్రణ_మూల్యం.settimeout(15);నియంత్రణ_మూల్యం.connect(str(నియంత్రణ_పథం));ధార_మూల్యం=నియంత్రణ_మూల్యం.makefile('rwb');json.loads(ధార_మూల్యం.readline());ధార_మూల్యం.write(b'{"execute":"qmp_capabilities"}\n');ధార_మూల్యం.flush()
                    while 'return' not in json.loads(ధార_మూల్యం.readline()):pass
                    పంపు((('poweroff' if 인수.poweroff_only else మారుపేరు_మూల్యం['poweroff'])+'\n').encode())
                    while True:
                        ఈవెంట్=json.loads(ధార_మూల్యం.readline())
                        if ఈవెంట్.get('event')=='SHUTDOWN':break
                    assert ఈవెంట్['data']['guest'] and ఈవెంట్['data']['reason']=='guest-shutdown',ఈవెంట్
                    assert విధానం_మూల్యం.wait(timeout=15)==0
                    నివేదిక_మూల్యం['shutdown']=ఈవెంట్;నివేదిక_మూల్యం['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                నివేదిక_మూల్యం['network_trace']=బ్రిడ్జ్_మూల్యం.జాడ_లాగ్
                assert 인수.poweroff_only or any(ప్రవేశం_మూల్యం['protocol']==1 and ప్రవేశం_మూల్యం['direction']=='from_guest' for ప్రవేశం_మూల్యం in బ్రిడ్జ్_మూల్యం.జాడ_లాగ్)
                నివేదిక_మూల్యం['passed']=True
            finally:
                if విధానం_మూల్యం.poll() is None:os.killpg(విధానం_మూల్యం.pid,signal.SIGTERM)
                try:విధానం_మూల్యం.wait(timeout=10)
                except subprocess.TimeoutExpired:విధానం_మూల్యం.kill();విధానం_మూల్యం.wait()
                ఎంచు_అంశం.close();(అవుట్పుట్/'serial.log').write_bytes(లాగ్_వరుస);(అవుట్పుట్/'report.json').write_text(json.dumps(నివేదిక_మూల్యం,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({కీ_మూల్యం:మూల్యం for కీ_మూల్యం,మూల్యం in నివేదిక_మూల్యం.items() if కీ_మూల్యం!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':నడుపుము()
