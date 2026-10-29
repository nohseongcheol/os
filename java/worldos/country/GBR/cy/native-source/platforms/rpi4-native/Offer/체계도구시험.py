#!/usr/bin/env python3
"""go_iawn_data 자체 커널의 IP/ICMP, cyflwr_VALUE ymholiad_VALUE, 현지어 Gorchymyn, 게스트 gadael_Rhaglen dilysu_5fb2b747."""
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


def Gweithredu_2():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    prosiect_gwraidd=Path(__file__).resolve().parents[1];Gosodiadau={};enw_tabl={}
    if 인수.edition:
        나라=인수.edition.resolve();Gosodiadau=json.loads((나라/'native.json').read_text());enw_tabl=Gosodiadau['identifiers'];prosiect_gwraidd=나라/Gosodiadau['source']/Gosodiadau['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        lletya=나라/'host/qemu'
        if lletya.is_file():os.environ['QEMU_AARCH64']=str(lletya)
    Offer=prosiect_gwraidd/Path(Gosodiadau.get('runner','Offer/Gweithredu_gorchymyn.py')).parent
    sys.path.insert(0,str(Offer))
    def Darllen(Enw):
        LLWYBR=Offer/(enw_tabl.get(Enw,Enw)+'.py');tasg_VALUE=importlib.util.spec_from_file_location('test_'+Enw,str(LLWYBR));modiwl_VALUE=importlib.util.module_from_spec(tasg_VALUE);tasg_VALUE.loader.exec_module(modiwl_VALUE);return modiwl_VALUE
    실행모듈=Darllen('Gweithredu_gorchymyn');Rhwydwaith_modiwl=Darllen('Rhwydwaith_pont');Gorchymyn=getattr(실행모듈,enw_tabl.get('Gorchymyn','Gorchymyn'));pont_TYPE=getattr(Rhwydwaith_modiwl,enw_tabl.get('Rhwydwaith_pont','Rhwydwaith_pont'))
    enw_arall_VALUE=Gosodiadau.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'cyfeiriad_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'sioe_help'})
    sys.path.insert(0,str(prosiect_gwraidd/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(prosiect_gwraidd);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Allbwn=인수.output or prosiect_gwraidd/'build/verification/system-tools';Allbwn.mkdir(parents=True,exist_ok=True)
    adrodd_VALUE={'passed':False,'country':Gosodiadau.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_rhes=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        rheoli_llwybr=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));rhif_porth=SEARCH_VALUE.getsockname()[1]
            if not 50000<=rhif_porth<=50007:break
        with pont_TYPE(rhif_porth,recordio=True,gwestai_ADDRESS=ipTestText('10.0.2.20'),lletya_ADDRESS='127.0.0.2') as pont_VALUE:
            Proses_VALUE=subprocess.Popen(Gorchymyn()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(rheoli_llwybr)]+pont_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            dewis_eitem=selectors.DefaultSelector();dewis_eitem.register(Proses_VALUE.stdout,selectors.EVENT_READ)
            def 받기(sioe_VALUE,Gweithredu_2=0,제한=45):
                끝=time.monotonic()+제한
                while sioe_VALUE not in LOG_rhes[Gweithredu_2:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:raise AssertionError('Missing '+repr(sioe_VALUE)+'\n'+LOG_rhes[Gweithredu_2:].decode('utf-8','replace'))
                    for bysell_VALUE,_ in dewis_eitem.select(.1):
                        data=bysell_VALUE.fileobj.read(65536)
                        if data:LOG_rhes.extend(data)
                return LOG_rhes[Gweithredu_2:].decode('utf-8','replace').replace('\r\n','\n')
            def anfon(data):Proses_VALUE.stdin.write(data);Proses_VALUE.stdin.flush()
            def cragen(Testun):
                Testun=ipTestText(Testun)
                print(adrodd_VALUE['country'],Testun,flush=True);SEQUENCE_VALUE[0]+=1;sioe_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Gweithredu_2=len(LOG_rhes)
                anfon((Testun+'; echo; echo '+sioe_VALUE+'\n').encode())
                끝표시=('\r\n'+sioe_VALUE+'\r\n').encode();받기(끝표시,Gweithredu_2)
                gorffen_safle=LOG_rhes.index(끝표시,Gweithredu_2)+len(끝표시)
                받기(b'jkoros-native> ',gorffen_safle)
                return LOG_rhes[Gweithredu_2:].decode('utf-8','replace').replace('\r\n','\n')
            def dilysu(Testun,*값들):
                ateb=cragen(Testun)
                for VALUE in 값들:assert ipTestText(VALUE) in ateb,(Testun,VALUE,ateb)
                return ateb
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    help_VALUE=dilysu('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in enw_arall_VALUE.values():assert 별칭 in help_VALUE,(별칭,help_VALUE)
                    dilysu(enw_arall_VALUE['help']+' system','Network / system')
                    dilysu('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    dilysu(enw_arall_VALUE['ipconfig'],'inet 10.0.2.15');dilysu('ip addr show','sl0: UP');dilysu('ifconfig','sl0: UP')
                    for annilys_Gosodiadau in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Gwall=dilysu('ipconfig set '+annilys_Gosodiadau+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Gwall,Gwall
                        dilysu('ipconfig','inet 10.0.2.15')
                    dilysu('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    dilysu(enw_arall_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    dilysu('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    dilysu('ip link set dev sl0 down','sl0: DOWN');dilysu('ping -c 1 10.0.2.2; echo STATUS=$?','Gwall -100','STATUS=1')
                    dilysu('ipconfig up','sl0: UP')
                    dilysu(enw_arall_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    dilysu('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    dilysu('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');dilysu(enw_arall_VALUE['route'],'10.0.2.2 sl0')
                    dilysu('ftpd start','FTP listening')
                    dilysu(enw_arall_VALUE['netstat'],'10.0.2.20:21','LISTEN');dilysu('ss','LISTEN')
                    dilysu('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Gwall -16')
                    with ftplib.FTP() as cleient_VALUE:
                        cleient_VALUE.connect('127.0.0.2',rhif_porth,timeout=20);cleient_VALUE.login();data=b'Network address was changed in the guest.\n'
                        cleient_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();cleient_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;cleient_VALUE.delete('net-state.txt')
                    dilysu('ftpd stop','FTP stopped');dilysu('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    adrodd_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Testun):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Testun);assert 찾음,Testun;return tuple(map(int,찾음.groups()))
                    전=저장값(dilysu('df','RAM only'));dilysu('echo disk-proof > sys-state.txt');후=저장값(dilysu(enw_arall_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    dilysu('rm sys-state.txt');assert 저장값(cragen('df'))==전
                    Cof_VALUE=dilysu(enw_arall_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Cof_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    dilysu(enw_arall_VALUE['ps'],'kernel/shell');dilysu(enw_arall_VALUE['uptime'],'seconds')
                    cyflwr_gwybodaeth=dilysu(enw_arall_VALUE['top']+' -n 2','kernel/shell');assert cyflwr_gwybodaeth.count('PID SLOT STATE')==2,cyflwr_gwybodaeth
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    dilysu('terminal','TERMINAL READY');Gweithredu_2=len(LOG_rhes);anfon(b'vi process.txt\n');받기(b'NORMAL',Gweithredu_2)
                    Gweithredu_2=len(LOG_rhes);anfon(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Gweithredu_2)
                    cofnod_Rhestr=dilysu('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',cofnod_Rhestr);assert 찾음 and int(찾음.group(2))>0,cofnod_Rhestr
                    dilysu('free','EL0 mapped KiB: '+찾음.group(2))
                    Gweithredu_2=len(LOG_rhes);anfon(b'top\n');받기(b'PID SLOT STATE',Gweithredu_2);anfon(b'q');받기(b'jkoros-native> ',Gweithredu_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if enw_arall_VALUE['df']!='df':
                        Gweithredu_2=len(LOG_rhes);anfon((enw_arall_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Gweithredu_2);받기(b'jkoros-native> ',Gweithredu_2)
                    adrodd_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as rheoli_VALUE:
                    rheoli_VALUE.settimeout(15);rheoli_VALUE.connect(str(rheoli_llwybr));ffrwd_VALUE=rheoli_VALUE.makefile('rwb');json.loads(ffrwd_VALUE.readline());ffrwd_VALUE.write(b'{"execute":"qmp_capabilities"}\n');ffrwd_VALUE.flush()
                    while 'return' not in json.loads(ffrwd_VALUE.readline()):pass
                    anfon((('poweroff' if 인수.poweroff_only else enw_arall_VALUE['poweroff'])+'\n').encode())
                    while True:
                        digwyddiad=json.loads(ffrwd_VALUE.readline())
                        if digwyddiad.get('event')=='SHUTDOWN':break
                    assert digwyddiad['data']['guest'] and digwyddiad['data']['reason']=='guest-shutdown',digwyddiad
                    assert Proses_VALUE.wait(timeout=15)==0
                    adrodd_VALUE['shutdown']=digwyddiad;adrodd_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                adrodd_VALUE['network_trace']=pont_VALUE.olrhain_LOG
                assert 인수.poweroff_only or any(cofnod_VALUE['protocol']==1 and cofnod_VALUE['direction']=='from_guest' for cofnod_VALUE in pont_VALUE.olrhain_LOG)
                adrodd_VALUE['passed']=True
            finally:
                if Proses_VALUE.poll() is None:os.killpg(Proses_VALUE.pid,signal.SIGTERM)
                try:Proses_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
                dewis_eitem.close();(Allbwn/'serial.log').write_bytes(LOG_rhes);(Allbwn/'report.json').write_text(json.dumps(adrodd_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({bysell_VALUE:VALUE for bysell_VALUE,VALUE in adrodd_VALUE.items() if bysell_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Gweithredu_2()
