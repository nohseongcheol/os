#!/usr/bin/env python3
"""tūturu_raraunga 자체 커널의 IP/ICMP, tūnga_uara uiui_uara, 현지어 tono, 게스트 Putaatu_kaupapa whakamana."""
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


def whakahaere():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    whakaatu_pūtake=Path(__file__).resolve().parents[1];Ngā_Tautuhinga={};ingoa_ripanga={}
    if 인수.edition:
        나라=인수.edition.resolve();Ngā_Tautuhinga=json.loads((나라/'native.json').read_text());ingoa_ripanga=Ngā_Tautuhinga['identifiers'];whakaatu_pūtake=나라/Ngā_Tautuhinga['source']/Ngā_Tautuhinga['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        taurima=나라/'host/qemu'
        if taurima.is_file():os.environ['QEMU_AARCH64']=str(taurima)
    Ngā_Utauta=whakaatu_pūtake/Path(Ngā_Tautuhinga.get('runner','Ngā_Utauta/kawe_tono.py')).parent
    sys.path.insert(0,str(Ngā_Utauta))
    def Pānuitia(Ingoa):
        ara=Ngā_Utauta/(ingoa_ripanga.get(Ingoa,Ingoa)+'.py');kēhi_uara=importlib.util.spec_from_file_location('test_'+Ingoa,str(ara));kōwae_uara=importlib.util.module_from_spec(kēhi_uara);kēhi_uara.loader.exec_module(kōwae_uara);return kōwae_uara
    실행모듈=Pānuitia('kawe_tono');whatunga_kōwae=Pānuitia('whatunga_arawhata');tono=getattr(실행모듈,ingoa_ripanga.get('tono','tono'));arawhata_TYPE=getattr(whatunga_kōwae,ingoa_ripanga.get('whatunga_arawhata','whatunga_arawhata'))
    ingoakē_uara=Ngā_Tautuhinga.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'wāhitau_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'whakaatu_āwhina'})
    sys.path.insert(0,str(whakaatu_pūtake/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(whakaatu_pūtake);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or whakaatu_pūtake/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    pūrongo_uara={'passed':False,'country':Ngā_Tautuhinga.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_RECORD=bytearray();SEQUENCE_uara=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        mana_ara=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Rapu_uara:Rapu_uara.bind(('127.0.0.1',0));접속번호=Rapu_uara.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with arawhata_TYPE(접속번호,hopu=True,manuhiri_ADDRESS=ipTestText('10.0.2.20'),taurima_ADDRESS='127.0.0.2') as arawhata_uara:
            Hātepe_uara=subprocess.Popen(tono()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(mana_ara)]+arawhata_uara.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            CHOOSE_tuemi=selectors.DefaultSelector();CHOOSE_tuemi.register(Hātepe_uara.stdout,selectors.EVENT_READ)
            def 받기(whakaatu_uara,whakahaere=0,제한=45):
                끝=time.monotonic()+제한
                while whakaatu_uara not in LOG_RECORD[whakahaere:]:
                    if time.monotonic()>끝 or Hātepe_uara.poll() is not None:raise AssertionError('Missing '+repr(whakaatu_uara)+'\n'+LOG_RECORD[whakahaere:].decode('utf-8','replace'))
                    for kī_uara,_ in CHOOSE_tuemi.select(.1):
                        raraunga=kī_uara.fileobj.read(65536)
                        if raraunga:LOG_RECORD.extend(raraunga)
                return LOG_RECORD[whakahaere:].decode('utf-8','replace').replace('\r\n','\n')
            def tuku(raraunga):Hātepe_uara.stdin.write(raraunga);Hātepe_uara.stdin.flush()
            def anga(Ngā_kupu):
                Ngā_kupu=ipTestText(Ngā_kupu)
                print(pūrongo_uara['country'],Ngā_kupu,flush=True);SEQUENCE_uara[0]+=1;whakaatu_uara='__SYSTEM_DONE_'+str(SEQUENCE_uara[0])+'__';whakahaere=len(LOG_RECORD)
                tuku((Ngā_kupu+'; echo; echo '+whakaatu_uara+'\n').encode())
                끝표시=('\r\n'+whakaatu_uara+'\r\n').encode();받기(끝표시,whakahaere)
                mutu_tūranga=LOG_RECORD.index(끝표시,whakahaere)+len(끝표시)
                받기(b'jkoros-native> ',mutu_tūranga)
                return LOG_RECORD[whakahaere:].decode('utf-8','replace').replace('\r\n','\n')
            def manatoko(Ngā_kupu,*값들):
                whakautu=anga(Ngā_kupu)
                for uara in 값들:assert ipTestText(uara) in whakautu,(Ngā_kupu,uara,whakautu)
                return whakautu
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    āwhina_uara=manatoko('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ingoakē_uara.values():assert 별칭 in āwhina_uara,(별칭,āwhina_uara)
                    manatoko(ingoakē_uara['help']+' system','Network / system')
                    manatoko('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    manatoko(ingoakē_uara['ipconfig'],'inet 10.0.2.15');manatoko('ip addr show','sl0: UP');manatoko('ifconfig','sl0: UP')
                    for muhu_Ngā_Tautuhinga in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Pōhēhē=manatoko('ipconfig set '+muhu_Ngā_Tautuhinga+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Pōhēhē,Pōhēhē
                        manatoko('ipconfig','inet 10.0.2.15')
                    manatoko('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    manatoko(ingoakē_uara['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    manatoko('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    manatoko('ip link set dev sl0 down','sl0: DOWN');manatoko('ping -c 1 10.0.2.2; echo STATUS=$?','Pōhēhē -100','STATUS=1')
                    manatoko('ipconfig up','sl0: UP')
                    manatoko(ingoakē_uara['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    manatoko('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    manatoko('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');manatoko(ingoakē_uara['route'],'10.0.2.2 sl0')
                    manatoko('ftpd start','FTP listening')
                    manatoko(ingoakē_uara['netstat'],'10.0.2.20:21','LISTEN');manatoko('ss','LISTEN')
                    manatoko('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Pōhēhē -16')
                    with ftplib.FTP() as kiritaki_uara:
                        kiritaki_uara.connect('127.0.0.2',접속번호,timeout=20);kiritaki_uara.login();raraunga=b'Network address was changed in the guest.\n'
                        kiritaki_uara.storbinary('STOR net-state.txt',io.BytesIO(raraunga));RECEIVED_raraunga=bytearray();kiritaki_uara.retrbinary('RETR net-state.txt',RECEIVED_raraunga.extend);assert RECEIVED_raraunga==raraunga;kiritaki_uara.delete('net-state.txt')
                    manatoko('ftpd stop','FTP stopped');manatoko('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    pūrongo_uara['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Ngā_kupu):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Ngā_kupu);assert 찾음,Ngā_kupu;return tuple(map(int,찾음.groups()))
                    전=저장값(manatoko('df','RAM only'));manatoko('echo disk-proof > sys-state.txt');후=저장값(manatoko(ingoakē_uara['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    manatoko('rm sys-state.txt');assert 저장값(anga('df'))==전
                    Pūmahara_uara=manatoko(ingoakē_uara['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Pūmahara_uara).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    manatoko(ingoakē_uara['ps'],'kernel/shell');manatoko(ingoakē_uara['uptime'],'seconds')
                    tūnga_mōhiohio=manatoko(ingoakē_uara['top']+' -n 2','kernel/shell');assert tūnga_mōhiohio.count('PID SLOT STATE')==2,tūnga_mōhiohio
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    manatoko('terminal','TERMINAL READY');whakahaere=len(LOG_RECORD);tuku(b'vi process.txt\n');받기(b'NORMAL',whakahaere)
                    whakahaere=len(LOG_RECORD);tuku(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',whakahaere)
                    tāurunga_Rārangi=manatoko('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',tāurunga_Rārangi);assert 찾음 and int(찾음.group(2))>0,tāurunga_Rārangi
                    manatoko('free','EL0 mapped KiB: '+찾음.group(2))
                    whakahaere=len(LOG_RECORD);tuku(b'top\n');받기(b'PID SLOT STATE',whakahaere);tuku(b'q');받기(b'jkoros-native> ',whakahaere)
                    # Test a multibyte prefix through the real shell completion path.
                    if ingoakē_uara['df']!='df':
                        whakahaere=len(LOG_RECORD);tuku((ingoakē_uara['df'][:-1]+'\t\n').encode());받기(b'RAM only',whakahaere);받기(b'jkoros-native> ',whakahaere)
                    pūrongo_uara['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as mana_uara:
                    mana_uara.settimeout(15);mana_uara.connect(str(mana_ara));roma_uara=mana_uara.makefile('rwb');json.loads(roma_uara.readline());roma_uara.write(b'{"execute":"qmp_capabilities"}\n');roma_uara.flush()
                    while 'return' not in json.loads(roma_uara.readline()):pass
                    tuku((('poweroff' if 인수.poweroff_only else ingoakē_uara['poweroff'])+'\n').encode())
                    while True:
                        hui=json.loads(roma_uara.readline())
                        if hui.get('event')=='SHUTDOWN':break
                    assert hui['data']['guest'] and hui['data']['reason']=='guest-shutdown',hui
                    assert Hātepe_uara.wait(timeout=15)==0
                    pūrongo_uara['shutdown']=hui;pūrongo_uara['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                pūrongo_uara['network_trace']=arawhata_uara.tapeke_hauroki_LOG
                assert 인수.poweroff_only or any(tāurunga_uara['protocol']==1 and tāurunga_uara['direction']=='from_guest' for tāurunga_uara in arawhata_uara.tapeke_hauroki_LOG)
                pūrongo_uara['passed']=True
            finally:
                if Hātepe_uara.poll() is None:os.killpg(Hātepe_uara.pid,signal.SIGTERM)
                try:Hātepe_uara.wait(timeout=10)
                except subprocess.TimeoutExpired:Hātepe_uara.kill();Hātepe_uara.wait()
                CHOOSE_tuemi.close();(출력/'serial.log').write_bytes(LOG_RECORD);(출력/'report.json').write_text(json.dumps(pūrongo_uara,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({kī_uara:uara for kī_uara,uara in pūrongo_uara.items() if kī_uara!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':whakahaere()
