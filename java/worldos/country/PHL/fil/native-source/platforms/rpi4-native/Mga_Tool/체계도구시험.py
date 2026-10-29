#!/usr/bin/env python3
"""totoo_data 자체 커널의 IP/ICMP, katayuan_VALUE query_VALUE, 현지어 utos, 게스트 Paglabas_app patunayan."""
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


def run():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=parser_48ee4b1b.parse_args()
    Project_root=Path(__file__).resolve().parents[1];Mga_Setting={};pangalan_talahanayan={}
    if 인수.edition:
        나라=인수.edition.resolve();Mga_Setting=json.loads((나라/'native.json').read_text());pangalan_talahanayan=Mga_Setting['identifiers'];Project_root=나라/Mga_Setting['source']/Mga_Setting['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        host=나라/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    Mga_Tool=Project_root/Path(Mga_Setting.get('runner','Mga_Tool/Mag_execute_utos.py')).parent
    sys.path.insert(0,str(Mga_Tool))
    def 읽기(pangalan):
        path=Mga_Tool/(pangalan_talahanayan.get(pangalan,pangalan)+'.py');kaso_VALUE=importlib.util.spec_from_file_location('test_'+pangalan,str(path));module_VALUE=importlib.util.module_from_spec(kaso_VALUE);kaso_VALUE.loader.exec_module(module_VALUE);return module_VALUE
    실행모듈=읽기('Mag_execute_utos');Network_module=읽기('Network_bridge');utos=getattr(실행모듈,pangalan_talahanayan.get('utos','utos'));bridge_TYPE=getattr(Network_module,pangalan_talahanayan.get('Network_bridge','Network_bridge'))
    alyas_VALUE=Mga_Setting.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_address','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ipakita_tulong'})
    sys.path.insert(0,str(Project_root/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_root);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or Project_root/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    ulat_VALUE={'passed':False,'country':Mga_Setting.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_hanay=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        control_path=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));numero_ng_port=SEARCH_VALUE.getsockname()[1]
            if not 50000<=numero_ng_port<=50007:break
        with bridge_TYPE(numero_ng_port,mag_capture=True,bisita_email=ipTestText('10.0.2.20'),host_email='127.0.0.2') as bridge_VALUE:
            Proseso_VALUE=subprocess.Popen(utos()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(control_path)]+bridge_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_item=selectors.DefaultSelector();CHOOSE_item.register(Proseso_VALUE.stdout,selectors.EVENT_READ)
            def 받기(ipakita_VALUE,run=0,제한=45):
                끝=time.monotonic()+제한
                while ipakita_VALUE not in LOG_hanay[run:]:
                    if time.monotonic()>끝 or Proseso_VALUE.poll() is not None:raise AssertionError('Missing '+repr(ipakita_VALUE)+'\n'+LOG_hanay[run:].decode('utf-8','replace'))
                    for key_VALUE,_ in CHOOSE_item.select(.1):
                        data=key_VALUE.fileobj.read(65536)
                        if data:LOG_hanay.extend(data)
                return LOG_hanay[run:].decode('utf-8','replace').replace('\r\n','\n')
            def i_email(data):Proseso_VALUE.stdin.write(data);Proseso_VALUE.stdin.flush()
            def shell(SMS):
                SMS=ipTestText(SMS)
                print(ulat_VALUE['country'],SMS,flush=True);SEQUENCE_VALUE[0]+=1;ipakita_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';run=len(LOG_hanay)
                i_email((SMS+'; echo; echo '+ipakita_VALUE+'\n').encode())
                끝표시=('\r\n'+ipakita_VALUE+'\r\n').encode();받기(끝표시,run)
                tapusin_posisyon=LOG_hanay.index(끝표시,run)+len(끝표시)
                받기(b'jkoros-native> ',tapusin_posisyon)
                return LOG_hanay[run:].decode('utf-8','replace').replace('\r\n','\n')
            def tiyakin_kumpirmahin(SMS,*값들):
                tumugon=shell(SMS)
                for VALUE in 값들:assert ipTestText(VALUE) in tumugon,(SMS,VALUE,tumugon)
                return tumugon
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    tulong_VALUE=tiyakin_kumpirmahin('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alyas_VALUE.values():assert 별칭 in tulong_VALUE,(별칭,tulong_VALUE)
                    tiyakin_kumpirmahin(alyas_VALUE['help']+' system','Network / system')
                    tiyakin_kumpirmahin('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    tiyakin_kumpirmahin(alyas_VALUE['ipconfig'],'inet 10.0.2.15');tiyakin_kumpirmahin('ip addr show','sl0: UP');tiyakin_kumpirmahin('ifconfig','sl0: UP')
                    for hindi_tama_Mga_Setting in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        error=tiyakin_kumpirmahin('ipconfig set '+hindi_tama_Mga_Setting+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in error,error
                        tiyakin_kumpirmahin('ipconfig','inet 10.0.2.15')
                    tiyakin_kumpirmahin('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    tiyakin_kumpirmahin(alyas_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tiyakin_kumpirmahin('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    tiyakin_kumpirmahin('ip link set dev sl0 down','sl0: DOWN');tiyakin_kumpirmahin('ping -c 1 10.0.2.2; echo STATUS=$?','error -100','STATUS=1')
                    tiyakin_kumpirmahin('ipconfig up','sl0: UP')
                    tiyakin_kumpirmahin(alyas_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    tiyakin_kumpirmahin('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tiyakin_kumpirmahin('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');tiyakin_kumpirmahin(alyas_VALUE['route'],'10.0.2.2 sl0')
                    tiyakin_kumpirmahin('ftpd start','FTP listening')
                    tiyakin_kumpirmahin(alyas_VALUE['netstat'],'10.0.2.20:21','LISTEN');tiyakin_kumpirmahin('ss','LISTEN')
                    tiyakin_kumpirmahin('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','error -16')
                    with ftplib.FTP() as client_VALUE:
                        client_VALUE.connect('127.0.0.2',numero_ng_port,timeout=20);client_VALUE.login();data=b'Network address was changed in the guest.\n'
                        client_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();client_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;client_VALUE.delete('net-state.txt')
                    tiyakin_kumpirmahin('ftpd stop','FTP stopped');tiyakin_kumpirmahin('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ulat_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(tiyakin_kumpirmahin('df','RAM only'));tiyakin_kumpirmahin('echo disk-proof > sys-state.txt');후=저장값(tiyakin_kumpirmahin(alyas_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    tiyakin_kumpirmahin('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memory_VALUE=tiyakin_kumpirmahin(alyas_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memory_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    tiyakin_kumpirmahin(alyas_VALUE['ps'],'kernel/shell');tiyakin_kumpirmahin(alyas_VALUE['uptime'],'seconds')
                    katayuan_impormasyon=tiyakin_kumpirmahin(alyas_VALUE['top']+' -n 2','kernel/shell');assert katayuan_impormasyon.count('PID SLOT STATE')==2,katayuan_impormasyon
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    tiyakin_kumpirmahin('terminal','TERMINAL READY');run=len(LOG_hanay);i_email(b'vi process.txt\n');받기(b'NORMAL',run)
                    run=len(LOG_hanay);i_email(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',run)
                    pagpasok_list=tiyakin_kumpirmahin('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',pagpasok_list);assert 찾음 and int(찾음.group(2))>0,pagpasok_list
                    tiyakin_kumpirmahin('free','EL0 mapped KiB: '+찾음.group(2))
                    run=len(LOG_hanay);i_email(b'top\n');받기(b'PID SLOT STATE',run);i_email(b'q');받기(b'jkoros-native> ',run)
                    # Test a multibyte prefix through the real shell completion path.
                    if alyas_VALUE['df']!='df':
                        run=len(LOG_hanay);i_email((alyas_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',run);받기(b'jkoros-native> ',run)
                    ulat_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as control_VALUE:
                    control_VALUE.settimeout(15);control_VALUE.connect(str(control_path));Stream_VALUE=control_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    i_email((('poweroff' if 인수.poweroff_only else alyas_VALUE['poweroff'])+'\n').encode())
                    while True:
                        kaganapan=json.loads(Stream_VALUE.readline())
                        if kaganapan.get('event')=='SHUTDOWN':break
                    assert kaganapan['data']['guest'] and kaganapan['data']['reason']=='guest-shutdown',kaganapan
                    assert Proseso_VALUE.wait(timeout=15)==0
                    ulat_VALUE['shutdown']=kaganapan;ulat_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ulat_VALUE['network_trace']=bridge_VALUE.trace_LOG
                assert 인수.poweroff_only or any(pagpasok_VALUE['protocol']==1 and pagpasok_VALUE['direction']=='from_guest' for pagpasok_VALUE in bridge_VALUE.trace_LOG)
                ulat_VALUE['passed']=True
            finally:
                if Proseso_VALUE.poll() is None:os.killpg(Proseso_VALUE.pid,signal.SIGTERM)
                try:Proseso_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proseso_VALUE.kill();Proseso_VALUE.wait()
                CHOOSE_item.close();(출력/'serial.log').write_bytes(LOG_hanay);(출력/'report.json').write_text(json.dumps(ulat_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key_VALUE:VALUE for key_VALUE,VALUE in ulat_VALUE.items() if key_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':run()
