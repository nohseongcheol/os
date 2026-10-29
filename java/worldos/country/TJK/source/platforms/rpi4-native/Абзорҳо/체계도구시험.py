#!/usr/bin/env python3
"""воқеӣ_иттилоот 자체 커널의 IP/ICMP, вазъият_қимат ковиш_қимат, 현지어 фармон, 게스트 Баромад_барнома санҷидани_эътибор."""
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


def порча():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Танзимот={};ном_ҷадвал={}
    if 인수.edition:
        나라=인수.edition.resolve();Танзимот=json.loads((나라/'native.json').read_text());ном_ҷадвал=Танзимот['identifiers'];기준=나라/Танзимот['source']/Танзимот['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        мизбон=나라/'host/qemu'
        if мизбон.is_file():os.environ['QEMU_AARCH64']=str(мизбон)
    Абзорҳо=기준/Path(Танзимот.get('runner','Абзорҳо/иҷро_кардан_фармон.py')).parent
    sys.path.insert(0,str(Абзорҳо))
    def Хондан(Ном):
        масир=Абзорҳо/(ном_ҷадвал.get(Ном,Ном)+'.py');кор_қимат=importlib.util.spec_from_file_location('test_'+Ном,str(масир));모듈=importlib.util.module_from_spec(кор_қимат);кор_қимат.loader.exec_module(모듈);return 모듈
    실행모듈=Хондан('иҷро_кардан_фармон');망모듈=Хондан('Шабака_кӯпрук');фармон=getattr(실행모듈,ном_ҷадвал.get('фармон','фармон'));кӯпрук_навъ=getattr(망모듈,ном_ҷадвал.get('Шабака_кӯпрук','Шабака_кӯпрук'))
    миёнбур_қимат_0a38607b=Танзимот.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'суроғаи_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'намоиш_додан_кӯмак'})
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
    гузориш_қимат={'passed':False,'country':Танзимот.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    сабт_кардан_сабт=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        идоракунӣ_масир=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ҷустан_қимат:ҷустан_қимат.bind(('127.0.0.1',0));접속번호=ҷустан_қимат.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with кӯпрук_навъ(접속번호,акс_гирифтан=True,меҳмон_суроға=ipTestText('10.0.2.20'),мизбон_суроға='127.0.0.2') as кӯпрук_қимат:
            Раванд_қимат=subprocess.Popen(фармон()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(идоракунӣ_масир)]+кӯпрук_қимат.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            интихоб_кардан_объект=selectors.DefaultSelector();интихоб_кардан_объект.register(Раванд_қимат.stdout,selectors.EVENT_READ)
            def 받기(намоиш_додан_қимат,порча=0,제한=45):
                끝=time.monotonic()+제한
                while намоиш_додан_қимат not in сабт_кардан_сабт[порча:]:
                    if time.monotonic()>끝 or Раванд_қимат.poll() is not None:raise AssertionError('Missing '+repr(намоиш_додан_қимат)+'\n'+сабт_кардан_сабт[порча:].decode('utf-8','replace'))
                    for калид_қимат,_ in интихоб_кардан_объект.select(.1):
                        иттилоот=калид_қимат.fileobj.read(65536)
                        if иттилоот:сабт_кардан_сабт.extend(иттилоот)
                return сабт_кардан_сабт[порча:].decode('utf-8','replace').replace('\r\n','\n')
            def фиристодан(иттилоот):Раванд_қимат.stdin.write(иттилоот);Раванд_қимат.stdin.flush()
            def восит(Матн):
                Матн=ipTestText(Матн)
                print(гузориш_қимат['country'],Матн,flush=True);차례[0]+=1;намоиш_додан_қимат='__SYSTEM_DONE_'+str(차례[0])+'__';порча=len(сабт_кардан_сабт)
                фиристодан((Матн+'; echo; echo '+намоиш_додан_қимат+'\n').encode())
                끝표시=('\r\n'+намоиш_додан_қимат+'\r\n').encode();받기(끝표시,порча)
                끝자리=сабт_кардан_сабт.index(끝표시,порча)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return сабт_кардан_сабт[порча:].decode('utf-8','replace').replace('\r\n','\n')
            def тасдиқ_кардан(Матн,*값들):
                ҷавоб_додан=восит(Матн)
                for қимат in 값들:assert ipTestText(қимат) in ҷавоб_додан,(Матн,қимат,ҷавоб_додан)
                return ҷавоб_додан
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    кӯмак_қимат=тасдиқ_кардан('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in миёнбур_қимат_0a38607b.values():assert 별칭 in кӯмак_қимат,(별칭,кӯмак_қимат)
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['help']+' system','Network / system')
                    тасдиқ_кардан('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['ipconfig'],'inet 10.0.2.15');тасдиқ_кардан('ip addr show','sl0: UP');тасдиқ_кардан('ifconfig','sl0: UP')
                    for беэътибор_Танзимот in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Хато=тасдиқ_кардан('ipconfig set '+беэътибор_Танзимот+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Хато,Хато
                        тасдиқ_кардан('ipconfig','inet 10.0.2.15')
                    тасдиқ_кардан('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тасдиқ_кардан('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    тасдиқ_кардан('ip link set dev sl0 down','sl0: DOWN');тасдиқ_кардан('ping -c 1 10.0.2.2; echo STATUS=$?','Хато -100','STATUS=1')
                    тасдиқ_кардан('ipconfig up','sl0: UP')
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    тасдиқ_кардан('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    тасдиқ_кардан('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');тасдиқ_кардан(миёнбур_қимат_0a38607b['route'],'10.0.2.2 sl0')
                    тасдиқ_кардан('ftpd start','FTP listening')
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['netstat'],'10.0.2.20:21','LISTEN');тасдиқ_кардан('ss','LISTEN')
                    тасдиқ_кардан('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Хато -16')
                    with ftplib.FTP() as муштарӣ_қимат:
                        муштарӣ_қимат.connect('127.0.0.2',접속번호,timeout=20);муштарӣ_қимат.login();иттилоот=b'Network address was changed in the guest.\n'
                        муштарӣ_қимат.storbinary('STOR net-state.txt',io.BytesIO(иттилоот));받은자료=bytearray();муштарӣ_қимат.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==иттилоот;муштарӣ_қимат.delete('net-state.txt')
                    тасдиқ_кардан('ftpd stop','FTP stopped');тасдиқ_кардан('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    гузориш_қимат['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Матн):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Матн);assert 찾음,Матн;return tuple(map(int,찾음.groups()))
                    전=저장값(тасдиқ_кардан('df','RAM only'));тасдиқ_кардан('echo disk-proof > sys-state.txt');후=저장값(тасдиқ_кардан(миёнбур_қимат_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    тасдиқ_кардан('rm sys-state.txt');assert 저장값(восит('df'))==전
                    ҳофиза_қимат=тасдиқ_кардан(миёнбур_қимат_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ҳофиза_қимат).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    тасдиқ_кардан(миёнбур_қимат_0a38607b['ps'],'kernel/shell');тасдиқ_кардан(миёнбур_қимат_0a38607b['uptime'],'seconds')
                    вазъият_маълумот=тасдиқ_кардан(миёнбур_қимат_0a38607b['top']+' -n 2','kernel/shell');assert вазъият_маълумот.count('PID SLOT STATE')==2,вазъият_маълумот
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    тасдиқ_кардан('terminal','TERMINAL READY');порча=len(сабт_кардан_сабт);фиристодан(b'vi process.txt\n');받기(b'NORMAL',порча)
                    порча=len(сабт_кардан_сабт);фиристодан(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',порча)
                    ворида_Рӯйхат=тасдиқ_кардан('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ворида_Рӯйхат);assert 찾음 and int(찾음.group(2))>0,ворида_Рӯйхат
                    тасдиқ_кардан('free','EL0 mapped KiB: '+찾음.group(2))
                    порча=len(сабт_кардан_сабт);фиристодан(b'top\n');받기(b'PID SLOT STATE',порча);фиристодан(b'q');받기(b'jkoros-native> ',порча)
                    # Test a multibyte prefix through the real shell completion path.
                    if миёнбур_қимат_0a38607b['df']!='df':
                        порча=len(сабт_кардан_сабт);фиристодан((миёнбур_қимат_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',порча);받기(b'jkoros-native> ',порча)
                    гузориш_қимат['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as идоракунӣ_қимат:
                    идоракунӣ_қимат.settimeout(15);идоракунӣ_қимат.connect(str(идоракунӣ_масир));ҷараён_қимат=идоракунӣ_қимат.makefile('rwb');json.loads(ҷараён_қимат.readline());ҷараён_қимат.write(b'{"execute":"qmp_capabilities"}\n');ҷараён_қимат.flush()
                    while 'return' not in json.loads(ҷараён_қимат.readline()):pass
                    фиристодан((('poweroff' if 인수.poweroff_only else миёнбур_қимат_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        рӯйдод=json.loads(ҷараён_қимат.readline())
                        if рӯйдод.get('event')=='SHUTDOWN':break
                    assert рӯйдод['data']['guest'] and рӯйдод['data']['reason']=='guest-shutdown',рӯйдод
                    assert Раванд_қимат.wait(timeout=15)==0
                    гузориш_қимат['shutdown']=рӯйдод;гузориш_қимат['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                гузориш_қимат['network_trace']=кӯпрук_қимат.추적기록
                assert 인수.poweroff_only or any(ворида_қимат['protocol']==1 and ворида_қимат['direction']=='from_guest' for ворида_қимат in кӯпрук_қимат.추적기록)
                гузориш_қимат['passed']=True
            finally:
                if Раванд_қимат.poll() is None:os.killpg(Раванд_қимат.pid,signal.SIGTERM)
                try:Раванд_қимат.wait(timeout=10)
                except subprocess.TimeoutExpired:Раванд_қимат.kill();Раванд_қимат.wait()
                интихоб_кардан_объект.close();(출력/'serial.log').write_bytes(сабт_кардан_сабт);(출력/'report.json').write_text(json.dumps(гузориш_қимат,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({калид_қимат:қимат for калид_қимат,қимат in гузориш_қимат.items() if калид_қимат!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':порча()
