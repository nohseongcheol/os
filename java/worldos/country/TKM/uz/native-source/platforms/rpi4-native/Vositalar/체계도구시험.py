#!/usr/bin/env python3
"""real_ma_lumotlar 자체 커널의 IP/ICMP, holat_VALUE_e10195a1 so_rov_VALUE, 현지어 Buyruq, 게스트 Chiqish_ilova tasdiqlash."""
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


def Bajarish():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=parser_48ee4b1b.parse_args()
    Project_ildiz=Path(__file__).resolve().parents[1];Moslamalar={};nom_jadval={}
    if 인수.edition:
        나라=인수.edition.resolve();Moslamalar=json.loads((나라/'native.json').read_text());nom_jadval=Moslamalar['identifiers'];Project_ildiz=나라/Moslamalar['source']/Moslamalar['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        tashkilotchi=나라/'host/qemu'
        if tashkilotchi.is_file():os.environ['QEMU_AARCH64']=str(tashkilotchi)
    Vositalar=Project_ildiz/Path(Moslamalar.get('runner','Vositalar/bajarmoq_buyruq.py')).parent
    sys.path.insert(0,str(Vositalar))
    def Oʻqish(Nomi):
        yo_l=Vositalar/(nom_jadval.get(Nomi,Nomi)+'.py');murojaat_VALUE=importlib.util.spec_from_file_location('test_'+Nomi,str(yo_l));modul_VALUE=importlib.util.module_from_spec(murojaat_VALUE);murojaat_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Oʻqish('bajarmoq_buyruq');Tarmoq_modul=Oʻqish('통신다리');Buyruq=getattr(실행모듈,nom_jadval.get('Buyruq','Buyruq'));다리형=getattr(Tarmoq_modul,nom_jadval.get('통신다리','통신다리'))
    yorliq_VALUE_0a38607b=Moslamalar.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_manzil','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ko_rsatmoq_yordam'})
    sys.path.insert(0,str(Project_ildiz/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_ildiz);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or Project_ildiz/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    hisobot_VALUE={'passed':False,'country':Moslamalar.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_satr=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        boshqaruv_yo_l=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Izlash_VALUE:Izlash_VALUE.bind(('127.0.0.1',0));접속번호=Izlash_VALUE.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,olish=True,mehmon_manzil=ipTestText('10.0.2.20'),tashkilotchi_manzil='127.0.0.2') as 다리:
            Jarayon_VALUE=subprocess.Popen(Buyruq()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(boshqaruv_yo_l)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_element=selectors.DefaultSelector();CHOOSE_element.register(Jarayon_VALUE.stdout,selectors.EVENT_READ)
            def 받기(ko_rsatmoq_VALUE,Bajarish=0,제한=45):
                끝=time.monotonic()+제한
                while ko_rsatmoq_VALUE not in LOG_satr[Bajarish:]:
                    if time.monotonic()>끝 or Jarayon_VALUE.poll() is not None:raise AssertionError('Missing '+repr(ko_rsatmoq_VALUE)+'\n'+LOG_satr[Bajarish:].decode('utf-8','replace'))
                    for Kalit_VALUE,_ in CHOOSE_element.select(.1):
                        ma_lumotlar=Kalit_VALUE.fileobj.read(65536)
                        if ma_lumotlar:LOG_satr.extend(ma_lumotlar)
                return LOG_satr[Bajarish:].decode('utf-8','replace').replace('\r\n','\n')
            def yuborish(ma_lumotlar):Jarayon_VALUE.stdin.write(ma_lumotlar);Jarayon_VALUE.stdin.flush()
            def qobiq(Matn):
                Matn=ipTestText(Matn)
                print(hisobot_VALUE['country'],Matn,flush=True);SEQUENCE_VALUE[0]+=1;ko_rsatmoq_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Bajarish=len(LOG_satr)
                yuborish((Matn+'; echo; echo '+ko_rsatmoq_VALUE+'\n').encode())
                끝표시=('\r\n'+ko_rsatmoq_VALUE+'\r\n').encode();받기(끝표시,Bajarish)
                to_xtatmoq_holat=LOG_satr.index(끝표시,Bajarish)+len(끝표시)
                받기(b'jkoros-native> ',to_xtatmoq_holat)
                return LOG_satr[Bajarish:].decode('utf-8','replace').replace('\r\n','\n')
            def tasdiqlamoq(Matn,*값들):
                javob_berish=qobiq(Matn)
                for VALUE in 값들:assert ipTestText(VALUE) in javob_berish,(Matn,VALUE,javob_berish)
                return javob_berish
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    yordam_VALUE=tasdiqlamoq('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in yorliq_VALUE_0a38607b.values():assert 별칭 in yordam_VALUE,(별칭,yordam_VALUE)
                    tasdiqlamoq(yorliq_VALUE_0a38607b['help']+' system','Network / system')
                    tasdiqlamoq('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    tasdiqlamoq(yorliq_VALUE_0a38607b['ipconfig'],'inet 10.0.2.15');tasdiqlamoq('ip addr show','sl0: UP');tasdiqlamoq('ifconfig','sl0: UP')
                    for xato_Sozlamalar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Xato=tasdiqlamoq('ipconfig set '+xato_Sozlamalar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Xato,Xato
                        tasdiqlamoq('ipconfig','inet 10.0.2.15')
                    tasdiqlamoq('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    tasdiqlamoq(yorliq_VALUE_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tasdiqlamoq('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    tasdiqlamoq('ip link set dev sl0 down','sl0: DOWN');tasdiqlamoq('ping -c 1 10.0.2.2; echo STATUS=$?','Xato -100','STATUS=1')
                    tasdiqlamoq('ipconfig up','sl0: UP')
                    tasdiqlamoq(yorliq_VALUE_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    tasdiqlamoq('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tasdiqlamoq('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');tasdiqlamoq(yorliq_VALUE_0a38607b['route'],'10.0.2.2 sl0')
                    tasdiqlamoq('ftpd start','FTP listening')
                    tasdiqlamoq(yorliq_VALUE_0a38607b['netstat'],'10.0.2.20:21','LISTEN');tasdiqlamoq('ss','LISTEN')
                    tasdiqlamoq('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Xato -16')
                    with ftplib.FTP() as mijoz_VALUE:
                        mijoz_VALUE.connect('127.0.0.2',접속번호,timeout=20);mijoz_VALUE.login();ma_lumotlar=b'Network address was changed in the guest.\n'
                        mijoz_VALUE.storbinary('STOR net-state.txt',io.BytesIO(ma_lumotlar));RECEIVED_ma_lumotlar=bytearray();mijoz_VALUE.retrbinary('RETR net-state.txt',RECEIVED_ma_lumotlar.extend);assert RECEIVED_ma_lumotlar==ma_lumotlar;mijoz_VALUE.delete('net-state.txt')
                    tasdiqlamoq('ftpd stop','FTP stopped');tasdiqlamoq('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    hisobot_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Matn):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Matn);assert 찾음,Matn;return tuple(map(int,찾음.groups()))
                    전=저장값(tasdiqlamoq('df','RAM only'));tasdiqlamoq('echo disk-proof > sys-state.txt');후=저장값(tasdiqlamoq(yorliq_VALUE_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    tasdiqlamoq('rm sys-state.txt');assert 저장값(qobiq('df'))==전
                    Xotira_VALUE=tasdiqlamoq(yorliq_VALUE_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Xotira_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    tasdiqlamoq(yorliq_VALUE_0a38607b['ps'],'kernel/shell');tasdiqlamoq(yorliq_VALUE_0a38607b['uptime'],'seconds')
                    holat_ma_lumot=tasdiqlamoq(yorliq_VALUE_0a38607b['top']+' -n 2','kernel/shell');assert holat_ma_lumot.count('PID SLOT STATE')==2,holat_ma_lumot
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    tasdiqlamoq('terminal','TERMINAL READY');Bajarish=len(LOG_satr);yuborish(b'vi process.txt\n');받기(b'NORMAL',Bajarish)
                    Bajarish=len(LOG_satr);yuborish(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Bajarish)
                    kiritish_Ro_yxat=tasdiqlamoq('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',kiritish_Ro_yxat);assert 찾음 and int(찾음.group(2))>0,kiritish_Ro_yxat
                    tasdiqlamoq('free','EL0 mapped KiB: '+찾음.group(2))
                    Bajarish=len(LOG_satr);yuborish(b'top\n');받기(b'PID SLOT STATE',Bajarish);yuborish(b'q');받기(b'jkoros-native> ',Bajarish)
                    # Test a multibyte prefix through the real shell completion path.
                    if yorliq_VALUE_0a38607b['df']!='df':
                        Bajarish=len(LOG_satr);yuborish((yorliq_VALUE_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',Bajarish);받기(b'jkoros-native> ',Bajarish)
                    hisobot_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as boshqaruv_VALUE:
                    boshqaruv_VALUE.settimeout(15);boshqaruv_VALUE.connect(str(boshqaruv_yo_l));oqim_VALUE=boshqaruv_VALUE.makefile('rwb');json.loads(oqim_VALUE.readline());oqim_VALUE.write(b'{"execute":"qmp_capabilities"}\n');oqim_VALUE.flush()
                    while 'return' not in json.loads(oqim_VALUE.readline()):pass
                    yuborish((('poweroff' if 인수.poweroff_only else yorliq_VALUE_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        hodisa=json.loads(oqim_VALUE.readline())
                        if hodisa.get('event')=='SHUTDOWN':break
                    assert hodisa['data']['guest'] and hodisa['data']['reason']=='guest-shutdown',hodisa
                    assert Jarayon_VALUE.wait(timeout=15)==0
                    hisobot_VALUE['shutdown']=hodisa;hisobot_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                hisobot_VALUE['network_trace']=다리.iz_LOG
                assert 인수.poweroff_only or any(kiritish_VALUE['protocol']==1 and kiritish_VALUE['direction']=='from_guest' for kiritish_VALUE in 다리.iz_LOG)
                hisobot_VALUE['passed']=True
            finally:
                if Jarayon_VALUE.poll() is None:os.killpg(Jarayon_VALUE.pid,signal.SIGTERM)
                try:Jarayon_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Jarayon_VALUE.kill();Jarayon_VALUE.wait()
                CHOOSE_element.close();(출력/'serial.log').write_bytes(LOG_satr);(출력/'report.json').write_text(json.dumps(hisobot_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kalit_VALUE:VALUE for Kalit_VALUE,VALUE in hisobot_VALUE.items() if Kalit_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Bajarish()
