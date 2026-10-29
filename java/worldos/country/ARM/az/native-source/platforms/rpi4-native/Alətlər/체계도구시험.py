#!/usr/bin/env python3
"""faktiki_verilənlər 자체 커널의 IP/ICMP, vəziyyət_VALUE sorğu_VALUE, 현지어 Əmr, 게스트 Çıxış_proqram təsdiqlə."""
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


def İcra_Et():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=parser_48ee4b1b.parse_args()
    Project_kök=Path(__file__).resolve().parents[1];Sazlama={};ad_cədvəl={}
    if 인수.edition:
        나라=인수.edition.resolve();Sazlama=json.loads((나라/'native.json').read_text());ad_cədvəl=Sazlama['identifiers'];Project_kök=나라/Sazlama['source']/Sazlama['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        host=나라/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    Alətlər=Project_kök/Path(Sazlama.get('runner','Alətlər/icra_etmək_əmr.py')).parent
    sys.path.insert(0,str(Alətlər))
    def Oxuma(Ad):
        Cığır=Alətlər/(ad_cədvəl.get(Ad,Ad)+'.py');müqavilə_VALUE=importlib.util.spec_from_file_location('test_'+Ad,str(Cığır));modul_VALUE=importlib.util.module_from_spec(müqavilə_VALUE);müqavilə_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Oxuma('icra_etmək_əmr');Şəbəkə_modul=Oxuma('Şəbəkə_körpü');Əmr=getattr(실행모듈,ad_cədvəl.get('Əmr','Əmr'));körpü_TYPE=getattr(Şəbəkə_modul,ad_cədvəl.get('Şəbəkə_körpü','Şəbəkə_körpü'))
    qısayol_VALUE_0a38607b=Sazlama.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_ünvan','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'göstərmək_kömək'})
    sys.path.insert(0,str(Project_kök/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_kök);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or Project_kök/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    hesabat_VALUE={'passed':False,'country':Sazlama.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_yaz=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        nəzarət_yol=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as SEARCH_VALUE:SEARCH_VALUE.bind(('127.0.0.1',0));접속번호=SEARCH_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with körpü_TYPE(접속번호,çəkmək=True,qonaq_ünvan=ipTestText('10.0.2.20'),host_ünvan='127.0.0.2') as körpü_VALUE:
            Proses_VALUE=subprocess.Popen(Əmr()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(nəzarət_yol)]+körpü_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_element=selectors.DefaultSelector();CHOOSE_element.register(Proses_VALUE.stdout,selectors.EVENT_READ)
            def 받기(göstərmək_VALUE,İcra_Et=0,제한=45):
                끝=time.monotonic()+제한
                while göstərmək_VALUE not in LOG_yaz[İcra_Et:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:raise AssertionError('Missing '+repr(göstərmək_VALUE)+'\n'+LOG_yaz[İcra_Et:].decode('utf-8','replace'))
                    for Açar_VALUE,_ in CHOOSE_element.select(.1):
                        verilənlər=Açar_VALUE.fileobj.read(65536)
                        if verilənlər:LOG_yaz.extend(verilənlər)
                return LOG_yaz[İcra_Et:].decode('utf-8','replace').replace('\r\n','\n')
            def göndərmək(verilənlər):Proses_VALUE.stdin.write(verilənlər);Proses_VALUE.stdin.flush()
            def örtük(Mətn):
                Mətn=ipTestText(Mətn)
                print(hesabat_VALUE['country'],Mətn,flush=True);SEQUENCE_VALUE[0]+=1;göstərmək_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';İcra_Et=len(LOG_yaz)
                göndərmək((Mətn+'; echo; echo '+göstərmək_VALUE+'\n').encode())
                끝표시=('\r\n'+göstərmək_VALUE+'\r\n').encode();받기(끝표시,İcra_Et)
                bitirmək_yerinə_qoymaq=LOG_yaz.index(끝표시,İcra_Et)+len(끝표시)
                받기(b'jkoros-native> ',bitirmək_yerinə_qoymaq)
                return LOG_yaz[İcra_Et:].decode('utf-8','replace').replace('\r\n','\n')
            def yoxlamaq(Mətn,*값들):
                cavab=örtük(Mətn)
                for VALUE in 값들:assert ipTestText(VALUE) in cavab,(Mətn,VALUE,cavab)
                return cavab
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    kömək_VALUE=yoxlamaq('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in qısayol_VALUE_0a38607b.values():assert 별칭 in kömək_VALUE,(별칭,kömək_VALUE)
                    yoxlamaq(qısayol_VALUE_0a38607b['help']+' system','Network / system')
                    yoxlamaq('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    yoxlamaq(qısayol_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');yoxlamaq('ip addr show','sl0: UP');yoxlamaq('ifconfig','sl0: UP')
                    for yanlış_Parametrlər in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        XƏTA=yoxlamaq('ipconfig set '+yanlış_Parametrlər+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in XƏTA,XƏTA
                        yoxlamaq('ipconfig','inet 10.0.2.15')
                    yoxlamaq('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    yoxlamaq(qısayol_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    yoxlamaq('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    yoxlamaq('ip link set dev sl0 down','sl0: DOWN');yoxlamaq('ping -c 1 10.0.2.2; echo STATUS=$?','XƏTA -100','STATUS=1')
                    yoxlamaq('ipconfig up','sl0: UP')
                    yoxlamaq(qısayol_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    yoxlamaq('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    yoxlamaq('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');yoxlamaq(qısayol_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    yoxlamaq('ftpd start','FTP listening')
                    yoxlamaq(qısayol_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');yoxlamaq('ss','LISTEN')
                    yoxlamaq('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','XƏTA -16')
                    with ftplib.FTP() as müştəri_VALUE:
                        müştəri_VALUE.connect('127.0.0.2',접속번호,timeout=20);müştəri_VALUE.login();verilənlər=b'Network address was changed in the guest.\n'
                        müştəri_VALUE.storbinary('STOR net-state.txt',io.BytesIO(verilənlər));RECEIVED_verilənlər=bytearray();müştəri_VALUE.retrbinary('RETR net-state.txt',RECEIVED_verilənlər.extend);assert RECEIVED_verilənlər==verilənlər;müştəri_VALUE.delete('net-state.txt')
                    yoxlamaq('ftpd stop','FTP stopped');yoxlamaq('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    hesabat_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Mətn):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Mətn);assert 찾음,Mətn;return tuple(map(int,찾음.groups()))
                    전=저장값(yoxlamaq('df','RAM only'));yoxlamaq('echo disk-proof > sys-state.txt');후=저장값(yoxlamaq(qısayol_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    yoxlamaq('rm sys-state.txt');assert 저장값(örtük('df'))==전
                    Yaddaş_VALUE=yoxlamaq(qısayol_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Yaddaş_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    yoxlamaq(qısayol_VALUE_0a38607b['ps'],'kernel/shell');yoxlamaq(qısayol_VALUE_0a38607b['uptime'],'seconds')
                    vəziyyət_məlumat=yoxlamaq(qısayol_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert vəziyyət_məlumat.count('PID SLOT STATE')==2,vəziyyət_məlumat
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    yoxlamaq('terminal','TERMINAL READY');İcra_Et=len(LOG_yaz);göndərmək(b'vi process.txt\n');받기(b'NORMAL',İcra_Et)
                    İcra_Et=len(LOG_yaz);göndərmək(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',İcra_Et)
                    daxiletmə_Siyahı=yoxlamaq('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',daxiletmə_Siyahı);assert 찾음 and int(찾음.group(2))>0,daxiletmə_Siyahı
                    yoxlamaq('free','EL0 mapped KiB: '+찾음.group(2))
                    İcra_Et=len(LOG_yaz);göndərmək(b'top\n');받기(b'PID SLOT STATE',İcra_Et);göndərmək(b'q');받기(b'jkoros-native> ',İcra_Et)
                    # Test a multibyte prefix through the real shell completion path.
                    if qısayol_VALUE_0a38607b['df']!='df':
                        İcra_Et=len(LOG_yaz);göndərmək((qısayol_VALUE_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',İcra_Et);받기(b'jkoros-native> ',İcra_Et)
                    hesabat_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as nəzarət_VALUE:
                    nəzarət_VALUE.settimeout(15);nəzarət_VALUE.connect(str(nəzarət_yol));axın_VALUE=nəzarət_VALUE.makefile('rwb');json.loads(axın_VALUE.readline());axın_VALUE.write(b'{"execute":"qmp_capabilities"}\n');axın_VALUE.flush()
                    while 'return' not in json.loads(axın_VALUE.readline()):pass
                    göndərmək((('poweroff' if 인수.poweroff_only else qısayol_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        hadisə=json.loads(axın_VALUE.readline())
                        if hadisə.get('event')=='SHUTDOWN':break
                    assert hadisə['data']['guest'] and hadisə['data']['reason']=='guest-shutdown',hadisə
                    assert Proses_VALUE.wait(timeout=15)==0
                    hesabat_VALUE['shutdown']=hadisə;hesabat_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                hesabat_VALUE['network_trace']=körpü_VALUE.iz_LOG
                assert 인수.poweroff_only or any(daxiletmə_VALUE['protocol']==1 and daxiletmə_VALUE['direction']=='from_guest' for daxiletmə_VALUE in körpü_VALUE.iz_LOG)
                hesabat_VALUE['passed']=True
            finally:
                if Proses_VALUE.poll() is None:os.killpg(Proses_VALUE.pid,signal.SIGTERM)
                try:Proses_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
                CHOOSE_element.close();(출력/'serial.log').write_bytes(LOG_yaz);(출력/'report.json').write_text(json.dumps(hesabat_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Açar_VALUE:VALUE for Açar_VALUE,VALUE in hesabat_VALUE.items() if Açar_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':İcra_Et()
