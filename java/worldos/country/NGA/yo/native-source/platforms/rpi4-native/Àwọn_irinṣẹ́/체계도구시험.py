#!/usr/bin/env python3
"""gangan_détà 자체 커널의 IP/ICMP, ipò_iye aṣèbéèré_iye, 현지어 Àṣẹ, 게스트 jáde_àtòjọ_ètò ìfọwọ́síìwé."""
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


def Rọ́ọ̀nù():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Àwọn_ààtò={};orúkọ_atọ́ka={}
    if 인수.edition:
        나라=인수.edition.resolve();Àwọn_ààtò=json.loads((나라/'native.json').read_text());orúkọ_atọ́ka=Àwọn_ààtò['identifiers'];기준=나라/Àwọn_ààtò['source']/Àwọn_ààtò['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        olùpèsè=나라/'host/qemu'
        if olùpèsè.is_file():os.environ['QEMU_AARCH64']=str(olùpèsè)
    Àwọn_irinṣẹ́=기준/Path(Àwọn_ààtò.get('runner','Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py')).parent
    sys.path.insert(0,str(Àwọn_irinṣẹ́))
    def Kàá(Orúkọ):
        ọ̀nà=Àwọn_irinṣẹ́/(orúkọ_atọ́ka.get(Orúkọ,Orúkọ)+'.py');iṣẹ́_iye=importlib.util.spec_from_file_location('test_'+Orúkọ,str(ọ̀nà));모듈=importlib.util.module_from_spec(iṣẹ́_iye);iṣẹ́_iye.loader.exec_module(모듈);return 모듈
    실행모듈=Kàá('ṣiṣẹ́_àṣẹ');망모듈=Kàá('Alásopọ̀_afará');Àṣẹ=getattr(실행모듈,orúkọ_atọ́ka.get('Àṣẹ','Àṣẹ'));afará_irú=getattr(망모듈,orúkọ_atọ́ka.get('Alásopọ̀_afará','Alásopọ̀_afará'))
    àbùjá_iye_0a38607b=Àwọn_ààtò.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'àdírẹ́ẹ̀sì_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ṣàfihàn_ìrànwọ́'})
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
    ìjábọ̀_iye={'passed':False,'country':Àwọn_ààtò.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    àkọsílẹ̀_ìṣe_ìlà_ìbú=bytearray();ÀTẸ̀LÉRA_iye=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ìdarí_ọ̀nà=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as wákiri_iye:wákiri_iye.bind(('127.0.0.1',0));접속번호=wákiri_iye.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with afará_irú(접속번호,gbàwòránsílẹ̀=True,àlejò_àdírẹ́ẹ̀sì=ipTestText('10.0.2.20'),olùpèsè_àdírẹ́ẹ̀sì='127.0.0.2') as afará_iye:
            Ìlànà_iye=subprocess.Popen(Àṣẹ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ìdarí_ọ̀nà)]+afará_iye.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            yan_wúnrẹ̀n=selectors.DefaultSelector();yan_wúnrẹ̀n.register(Ìlànà_iye.stdout,selectors.EVENT_READ)
            def 받기(ṣàfihàn_iye,Rọ́ọ̀nù=0,제한=45):
                끝=time.monotonic()+제한
                while ṣàfihàn_iye not in àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:]:
                    if time.monotonic()>끝 or Ìlànà_iye.poll() is not None:raise AssertionError('Missing '+repr(ṣàfihàn_iye)+'\n'+àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8','replace'))
                    for bọ́tìnnì_iye,_ in yan_wúnrẹ̀n.select(.1):
                        détà=bọ́tìnnì_iye.fileobj.read(65536)
                        if détà:àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
                return àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8','replace').replace('\r\n','\n')
            def í_meèlì(détà):Ìlànà_iye.stdin.write(détà);Ìlànà_iye.stdin.flush()
            def ṣẹ́ẹ̀lì(SMS):
                SMS=ipTestText(SMS)
                print(ìjábọ̀_iye['country'],SMS,flush=True);ÀTẸ̀LÉRA_iye[0]+=1;ṣàfihàn_iye='__SYSTEM_DONE_'+str(ÀTẸ̀LÉRA_iye[0])+'__';Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì((SMS+'; echo; echo '+ṣàfihàn_iye+'\n').encode())
                끝표시=('\r\n'+ṣàfihàn_iye+'\r\n').encode();받기(끝표시,Rọ́ọ̀nù)
                끝자리=àkọsílẹ̀_ìṣe_ìlà_ìbú.index(끝표시,Rọ́ọ̀nù)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8','replace').replace('\r\n','\n')
            def ridájú(SMS,*값들):
                Fèsì=ṣẹ́ẹ̀lì(SMS)
                for iye in 값들:assert ipTestText(iye) in Fèsì,(SMS,iye,Fèsì)
                return Fèsì
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ìrànwọ́_iye=ridájú('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in àbùjá_iye_0a38607b.values():assert 별칭 in ìrànwọ́_iye,(별칭,ìrànwọ́_iye)
                    ridájú(àbùjá_iye_0a38607b['help']+' system','Network / system')
                    ridájú('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ridájú(àbùjá_iye_0a38607b['ipconfig'],'inet 10.0.2.15');ridájú('ip addr show','sl0: UP');ridájú('ifconfig','sl0: UP')
                    for aláìbẹgbẹmu_Àwọn_ààtò in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        àṣìṣe=ridájú('ipconfig set '+aláìbẹgbẹmu_Àwọn_ààtò+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in àṣìṣe,àṣìṣe
                        ridájú('ipconfig','inet 10.0.2.15')
                    ridájú('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ridájú(àbùjá_iye_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ridájú('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ridájú('ip link set dev sl0 down','sl0: DOWN');ridájú('ping -c 1 10.0.2.2; echo STATUS=$?','àṣìṣe -100','STATUS=1')
                    ridájú('ipconfig up','sl0: UP')
                    ridájú(àbùjá_iye_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ridájú('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ridájú('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ridájú(àbùjá_iye_0a38607b['route'],'10.0.2.2 sl0')
                    ridájú('ftpd start','FTP listening')
                    ridájú(àbùjá_iye_0a38607b['netstat'],'10.0.2.20:21','LISTEN');ridájú('ss','LISTEN')
                    ridájú('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','àṣìṣe -16')
                    with ftplib.FTP() as aṣojú_iye:
                        aṣojú_iye.connect('127.0.0.2',접속번호,timeout=20);aṣojú_iye.login();détà=b'Network address was changed in the guest.\n'
                        aṣojú_iye.storbinary('STOR net-state.txt',io.BytesIO(détà));받은자료=bytearray();aṣojú_iye.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==détà;aṣojú_iye.delete('net-state.txt')
                    ridájú('ftpd stop','FTP stopped');ridájú('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ìjábọ̀_iye['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(ridájú('df','RAM only'));ridájú('echo disk-proof > sys-state.txt');후=저장값(ridájú(àbùjá_iye_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ridájú('rm sys-state.txt');assert 저장값(ṣẹ́ẹ̀lì('df'))==전
                    ibi_ìpamọ́_iye=ridájú(àbùjá_iye_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ibi_ìpamọ́_iye).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ridájú(àbùjá_iye_0a38607b['ps'],'kernel/shell');ridájú(àbùjá_iye_0a38607b['uptime'],'seconds')
                    ipò_Ìwífún=ridájú(àbùjá_iye_0a38607b['top']+' -n 2','kernel/shell');assert ipò_Ìwífún.count('PID SLOT STATE')==2,ipò_Ìwífún
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ridájú('terminal','TERMINAL READY');Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);í_meèlì(b'vi process.txt\n');받기(b'NORMAL',Rọ́ọ̀nù)
                    Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);í_meèlì(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Rọ́ọ̀nù)
                    ìgbéwọlé_Àtòkọ=ridájú('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ìgbéwọlé_Àtòkọ);assert 찾음 and int(찾음.group(2))>0,ìgbéwọlé_Àtòkọ
                    ridájú('free','EL0 mapped KiB: '+찾음.group(2))
                    Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);í_meèlì(b'top\n');받기(b'PID SLOT STATE',Rọ́ọ̀nù);í_meèlì(b'q');받기(b'jkoros-native> ',Rọ́ọ̀nù)
                    # Test a multibyte prefix through the real shell completion path.
                    if àbùjá_iye_0a38607b['df']!='df':
                        Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);í_meèlì((àbùjá_iye_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Rọ́ọ̀nù);받기(b'jkoros-native> ',Rọ́ọ̀nù)
                    ìjábọ̀_iye['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ìdarí_iye:
                    ìdarí_iye.settimeout(15);ìdarí_iye.connect(str(ìdarí_ọ̀nà));Stream_iye=ìdarí_iye.makefile('rwb');json.loads(Stream_iye.readline());Stream_iye.write(b'{"execute":"qmp_capabilities"}\n');Stream_iye.flush()
                    while 'return' not in json.loads(Stream_iye.readline()):pass
                    í_meèlì((('poweroff' if 인수.poweroff_only else àbùjá_iye_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        ìgbéṣẹ̀=json.loads(Stream_iye.readline())
                        if ìgbéṣẹ̀.get('event')=='SHUTDOWN':break
                    assert ìgbéṣẹ̀['data']['guest'] and ìgbéṣẹ̀['data']['reason']=='guest-shutdown',ìgbéṣẹ̀
                    assert Ìlànà_iye.wait(timeout=15)==0
                    ìjábọ̀_iye['shutdown']=ìgbéṣẹ̀;ìjábọ̀_iye['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ìjábọ̀_iye['network_trace']=afará_iye.àròpọ̀_mátirísì_adọ́gbaníhà_àkọsílẹ̀_ìṣe
                assert 인수.poweroff_only or any(ìgbéwọlé_iye['protocol']==1 and ìgbéwọlé_iye['direction']=='from_guest' for ìgbéwọlé_iye in afará_iye.àròpọ̀_mátirísì_adọ́gbaníhà_àkọsílẹ̀_ìṣe)
                ìjábọ̀_iye['passed']=True
            finally:
                if Ìlànà_iye.poll() is None:os.killpg(Ìlànà_iye.pid,signal.SIGTERM)
                try:Ìlànà_iye.wait(timeout=10)
                except subprocess.TimeoutExpired:Ìlànà_iye.kill();Ìlànà_iye.wait()
                yan_wúnrẹ̀n.close();(출력/'serial.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú);(출력/'report.json').write_text(json.dumps(ìjábọ̀_iye,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({bọ́tìnnì_iye:iye for bọ́tìnnì_iye,iye in ìjábọ̀_iye.items() if bọ́tìnnì_iye!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Rọ́ọ̀nù()
