#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo 자체 커널의 IP/ICMP, imo_ixabiso umbuzo_ixabiso, 현지어 Umyalelo, 게스트 phuma_inkqubo qinisekisa."""
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


def Phumeza():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Imimiselo={};igama_itheyibhile={}
    if 인수.edition:
        나라=인수.edition.resolve();Imimiselo=json.loads((나라/'native.json').read_text());igama_itheyibhile=Imimiselo['identifiers'];기준=나라/Imimiselo['source']/Imimiselo['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        umsingathi=나라/'host/qemu'
        if umsingathi.is_file():os.environ['QEMU_AARCH64']=str(umsingathi)
    Izixhobo=기준/Path(Imimiselo.get('runner','Izixhobo/ukwenza_umyalelo.py')).parent
    sys.path.insert(0,str(Izixhobo))
    def Funda(Igama):
        INDLELA=Izixhobo/(igama_itheyibhile.get(Igama,Igama)+'.py');isiganeko_ixabiso=importlib.util.spec_from_file_location('test_'+Igama,str(INDLELA));모듈=importlib.util.module_from_spec(isiganeko_ixabiso);isiganeko_ixabiso.loader.exec_module(모듈);return 모듈
    실행모듈=Funda('ukwenza_umyalelo');망모듈=Funda('Inethiwekhi_ibhulorho');Umyalelo=getattr(실행모듈,igama_itheyibhile.get('Umyalelo','Umyalelo'));ibhulorho_uhlobo=getattr(망모듈,igama_itheyibhile.get('Inethiwekhi_ibhulorho','Inethiwekhi_ibhulorho'))
    isinqumleli_ixabiso_0a38607b=Imimiselo.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'idilesi_ye_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'bonisa_uncedo'})
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
    ingxelo_ixabiso_ddf2aaf3={'passed':False,'country':Imimiselo.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ilog_umqolo=bytearray();ULANDELELWANO_ixabiso=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        isilawuli_indlela=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Khangela_ixabiso:Khangela_ixabiso.bind(('127.0.0.1',0));접속번호=Khangela_ixabiso.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with ibhulorho_uhlobo(접속번호,bamba=True,undwendwe_idilesi=ipTestText('10.0.2.20'),umsingathi_idilesi='127.0.0.2') as ibhulorho_ixabiso:
            Inkqubo_ixabiso=subprocess.Popen(Umyalelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(isilawuli_indlela)]+ibhulorho_ixabiso.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            khetha_into=selectors.DefaultSelector();khetha_into.register(Inkqubo_ixabiso.stdout,selectors.EVENT_READ)
            def 받기(bonisa_ixabiso,Phumeza=0,제한=45):
                끝=time.monotonic()+제한
                while bonisa_ixabiso not in ilog_umqolo[Phumeza:]:
                    if time.monotonic()>끝 or Inkqubo_ixabiso.poll() is not None:raise AssertionError('Missing '+repr(bonisa_ixabiso)+'\n'+ilog_umqolo[Phumeza:].decode('utf-8','replace'))
                    for iqhosha_ixabiso,_ in khetha_into.select(.1):
                        iingcombolo=iqhosha_ixabiso.fileobj.read(65536)
                        if iingcombolo:ilog_umqolo.extend(iingcombolo)
                return ilog_umqolo[Phumeza:].decode('utf-8','replace').replace('\r\n','\n')
            def thumela(iingcombolo):Inkqubo_ixabiso.stdin.write(iingcombolo);Inkqubo_ixabiso.stdin.flush()
            def isiniki_myalelo(Umbhalo):
                Umbhalo=ipTestText(Umbhalo)
                print(ingxelo_ixabiso_ddf2aaf3['country'],Umbhalo,flush=True);ULANDELELWANO_ixabiso[0]+=1;bonisa_ixabiso='__SYSTEM_DONE_'+str(ULANDELELWANO_ixabiso[0])+'__';Phumeza=len(ilog_umqolo)
                thumela((Umbhalo+'; echo; echo '+bonisa_ixabiso+'\n').encode())
                끝표시=('\r\n'+bonisa_ixabiso+'\r\n').encode();받기(끝표시,Phumeza)
                끝자리=ilog_umqolo.index(끝표시,Phumeza)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return ilog_umqolo[Phumeza:].decode('utf-8','replace').replace('\r\n','\n')
            def ngqinisisa(Umbhalo,*값들):
                phendula=isiniki_myalelo(Umbhalo)
                for ixabiso in 값들:assert ipTestText(ixabiso) in phendula,(Umbhalo,ixabiso,phendula)
                return phendula
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    uncedo_ixabiso=ngqinisisa('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in isinqumleli_ixabiso_0a38607b.values():assert 별칭 in uncedo_ixabiso,(별칭,uncedo_ixabiso)
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['help']+' system','Network / system')
                    ngqinisisa('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['ipconfig'],'inet 10.0.2.15');ngqinisisa('ip addr show','sl0: UP');ngqinisisa('ifconfig','sl0: UP')
                    for ayisebenzi_Iisetingi in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Impazamo=ngqinisisa('ipconfig set '+ayisebenzi_Iisetingi+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Impazamo,Impazamo
                        ngqinisisa('ipconfig','inet 10.0.2.15')
                    ngqinisisa('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ngqinisisa('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ngqinisisa('ip link set dev sl0 down','sl0: DOWN');ngqinisisa('ping -c 1 10.0.2.2; echo STATUS=$?','Impazamo -100','STATUS=1')
                    ngqinisisa('ipconfig up','sl0: UP')
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ngqinisisa('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ngqinisisa('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ngqinisisa(isinqumleli_ixabiso_0a38607b['route'],'10.0.2.2 sl0')
                    ngqinisisa('ftpd start','FTP listening')
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['netstat'],'10.0.2.20:21','LISTEN');ngqinisisa('ss','LISTEN')
                    ngqinisisa('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Impazamo -16')
                    with ftplib.FTP() as iklayenti_ixabiso:
                        iklayenti_ixabiso.connect('127.0.0.2',접속번호,timeout=20);iklayenti_ixabiso.login();iingcombolo=b'Network address was changed in the guest.\n'
                        iklayenti_ixabiso.storbinary('STOR net-state.txt',io.BytesIO(iingcombolo));받은자료=bytearray();iklayenti_ixabiso.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==iingcombolo;iklayenti_ixabiso.delete('net-state.txt')
                    ngqinisisa('ftpd stop','FTP stopped');ngqinisisa('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ingxelo_ixabiso_ddf2aaf3['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Umbhalo):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Umbhalo);assert 찾음,Umbhalo;return tuple(map(int,찾음.groups()))
                    전=저장값(ngqinisisa('df','RAM only'));ngqinisisa('echo disk-proof > sys-state.txt');후=저장값(ngqinisisa(isinqumleli_ixabiso_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ngqinisisa('rm sys-state.txt');assert 저장값(isiniki_myalelo('df'))==전
                    imemori_ixabiso=ngqinisisa(isinqumleli_ixabiso_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',imemori_ixabiso).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ngqinisisa(isinqumleli_ixabiso_0a38607b['ps'],'kernel/shell');ngqinisisa(isinqumleli_ixabiso_0a38607b['uptime'],'seconds')
                    imo_ingcaciso=ngqinisisa(isinqumleli_ixabiso_0a38607b['top']+' -n 2','kernel/shell');assert imo_ingcaciso.count('PID SLOT STATE')==2,imo_ingcaciso
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ngqinisisa('terminal','TERMINAL READY');Phumeza=len(ilog_umqolo);thumela(b'vi process.txt\n');받기(b'NORMAL',Phumeza)
                    Phumeza=len(ilog_umqolo);thumela(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Phumeza)
                    ufako_nkcukacha_uludwe=ngqinisisa('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ufako_nkcukacha_uludwe);assert 찾음 and int(찾음.group(2))>0,ufako_nkcukacha_uludwe
                    ngqinisisa('free','EL0 mapped KiB: '+찾음.group(2))
                    Phumeza=len(ilog_umqolo);thumela(b'top\n');받기(b'PID SLOT STATE',Phumeza);thumela(b'q');받기(b'jkoros-native> ',Phumeza)
                    # Test a multibyte prefix through the real shell completion path.
                    if isinqumleli_ixabiso_0a38607b['df']!='df':
                        Phumeza=len(ilog_umqolo);thumela((isinqumleli_ixabiso_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Phumeza);받기(b'jkoros-native> ',Phumeza)
                    ingxelo_ixabiso_ddf2aaf3['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as isilawuli_ixabiso:
                    isilawuli_ixabiso.settimeout(15);isilawuli_ixabiso.connect(str(isilawuli_indlela));Stream_ixabiso=isilawuli_ixabiso.makefile('rwb');json.loads(Stream_ixabiso.readline());Stream_ixabiso.write(b'{"execute":"qmp_capabilities"}\n');Stream_ixabiso.flush()
                    while 'return' not in json.loads(Stream_ixabiso.readline()):pass
                    thumela((('poweroff' if 인수.poweroff_only else isinqumleli_ixabiso_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        umcimbi=json.loads(Stream_ixabiso.readline())
                        if umcimbi.get('event')=='SHUTDOWN':break
                    assert umcimbi['data']['guest'] and umcimbi['data']['reason']=='guest-shutdown',umcimbi
                    assert Inkqubo_ixabiso.wait(timeout=15)==0
                    ingxelo_ixabiso_ddf2aaf3['shutdown']=umcimbi;ingxelo_ixabiso_ddf2aaf3['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ingxelo_ixabiso_ddf2aaf3['network_trace']=ibhulorho_ixabiso.ithreyisi_ilog
                assert 인수.poweroff_only or any(ufako_nkcukacha_ixabiso['protocol']==1 and ufako_nkcukacha_ixabiso['direction']=='from_guest' for ufako_nkcukacha_ixabiso in ibhulorho_ixabiso.ithreyisi_ilog)
                ingxelo_ixabiso_ddf2aaf3['passed']=True
            finally:
                if Inkqubo_ixabiso.poll() is None:os.killpg(Inkqubo_ixabiso.pid,signal.SIGTERM)
                try:Inkqubo_ixabiso.wait(timeout=10)
                except subprocess.TimeoutExpired:Inkqubo_ixabiso.kill();Inkqubo_ixabiso.wait()
                khetha_into.close();(출력/'serial.log').write_bytes(ilog_umqolo);(출력/'report.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({iqhosha_ixabiso:ixabiso for iqhosha_ixabiso,ixabiso in ingxelo_ixabiso_ddf2aaf3.items() if iqhosha_ixabiso!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Phumeza()
