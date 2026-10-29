#!/usr/bin/env python3
"""raun_gögn eigin 커널의 IP/ICMP, staða_VALUE_e10195a1 fyrirspurn_VALUE, 현지어 Skipun, 게스트 loka_forrit staðfesta."""
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


def Keyra_2():
    þáttari_48ee4b1b=argparse.ArgumentParser();þáttari_48ee4b1b.add_argument('--edition',type=Path);þáttari_48ee4b1b.add_argument('--output',type=Path);þáttari_48ee4b1b.add_argument('--poweroff-only',action='store_true');Viðföng=þáttari_48ee4b1b.parse_args()
    verk_rót=Path(__file__).resolve().parents[1];Stillingar={};heiti_tafla={}
    if Viðföng.edition:
        나라=Viðföng.edition.resolve();Stillingar=json.loads((나라/'native.json').read_text());heiti_tafla=Stillingar['identifiers'];verk_rót=나라/Stillingar['source']/Stillingar['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        hýsa=나라/'host/qemu'
        if hýsa.is_file():os.environ['QEMU_AARCH64']=str(hýsa)
    Verkfæri=verk_rót/Path(Stillingar.get('runner','Verkfæri/keyra_skipun.py')).parent
    sys.path.insert(0,str(Verkfæri))
    def Lestur(Heiti):
        SLÓÐ=Verkfæri/(heiti_tafla.get(Heiti,Heiti)+'.py');samningsvirði=importlib.util.spec_from_file_location('test_'+Heiti,str(SLÓÐ));eining_VALUE_6d2d8bf4=importlib.util.module_from_spec(samningsvirði);samningsvirði.loader.exec_module(eining_VALUE_6d2d8bf4);return eining_VALUE_6d2d8bf4
    실행모듈=Lestur('keyra_skipun');Net_eining=Lestur('Net_brú');Skipun=getattr(실행모듈,heiti_tafla.get('Skipun','Skipun'));brú_TYPE=getattr(Net_eining,heiti_tafla.get('Net_brú','Net_brú'))
    samnefni_VALUE=Stillingar.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_tala','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'sýna_hjálp'})
    sys.path.insert(0,str(verk_rót/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(verk_rót);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    úttak=Viðföng.output or verk_rót/'build/verification/system-tools';úttak.mkdir(parents=True,exist_ok=True)
    skrá_VALUE_ddf2aaf3={'passed':False,'country':Stillingar.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_lína=bytearray();SEQUENCE_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        stýring_slóð=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Leit_VALUE:Leit_VALUE.bind(('127.0.0.1',0));tengisnúmer=Leit_VALUE.getsockname()[1]
            if not 50000<=tengisnúmer<=50007:break
        with brú_TYPE(tengisnúmer,fanga=True,gestur_slóð=ipTestText('10.0.2.20'),hýsa_slóð='127.0.0.2') as brú_VALUE:
            Ferli_VALUE=subprocess.Popen(Skipun()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(stýring_slóð)]+brú_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            velja_vara=selectors.DefaultSelector();velja_vara.register(Ferli_VALUE.stdout,selectors.EVENT_READ)
            def 받기(sýna_VALUE,Keyra_2=0,제한=45):
                끝=time.monotonic()+제한
                while sýna_VALUE not in LOG_lína[Keyra_2:]:
                    if time.monotonic()>끝 or Ferli_VALUE.poll() is not None:raise AssertionError('Missing '+repr(sýna_VALUE)+'\n'+LOG_lína[Keyra_2:].decode('utf-8','replace'))
                    for Lykill_VALUE,_ in velja_vara.select(.1):
                        gögn=Lykill_VALUE.fileobj.read(65536)
                        if gögn:LOG_lína.extend(gögn)
                return LOG_lína[Keyra_2:].decode('utf-8','replace').replace('\r\n','\n')
            def senda(gögn):Ferli_VALUE.stdin.write(gögn);Ferli_VALUE.stdin.flush()
            def skel(Texti):
                Texti=ipTestText(Texti)
                print(skrá_VALUE_ddf2aaf3['country'],Texti,flush=True);SEQUENCE_VALUE[0]+=1;sýna_VALUE='__SYSTEM_DONE_'+str(SEQUENCE_VALUE[0])+'__';Keyra_2=len(LOG_lína)
                senda((Texti+'; echo; echo '+sýna_VALUE+'\n').encode())
                끝표시=('\r\n'+sýna_VALUE+'\r\n').encode();받기(끝표시,Keyra_2)
                ljúka_staða=LOG_lína.index(끝표시,Keyra_2)+len(끝표시)
                받기(b'jkoros-native> ',ljúka_staða)
                return LOG_lína[Keyra_2:].decode('utf-8','replace').replace('\r\n','\n')
            def sannprófa(Texti,*값들):
                svara=skel(Texti)
                for VALUE in 값들:assert ipTestText(VALUE) in svara,(Texti,VALUE,svara)
                return svara
            try:
                받기(b'jkoros-native> ')
                if not Viðföng.poweroff_only:
                    hjálp_VALUE=sannprófa('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in samnefni_VALUE.values():assert 별칭 in hjálp_VALUE,(별칭,hjálp_VALUE)
                    sannprófa(samnefni_VALUE['help']+' system','Network / system')
                    sannprófa('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    sannprófa(samnefni_VALUE['ipconfig'],'inet 10.0.2.15');sannprófa('ip addr show','sl0: UP');sannprófa('ifconfig','sl0: UP')
                    for ógilt_Stillingar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        Villa=sannprófa('ipconfig set '+ógilt_Stillingar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in Villa,Villa
                        sannprófa('ipconfig','inet 10.0.2.15')
                    sannprófa('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    sannprófa(samnefni_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    sannprófa('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    sannprófa('ip link set dev sl0 down','sl0: DOWN');sannprófa('ping -c 1 10.0.2.2; echo STATUS=$?','Villa -100','STATUS=1')
                    sannprófa('ipconfig up','sl0: UP')
                    sannprófa(samnefni_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    sannprófa('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    sannprófa('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');sannprófa(samnefni_VALUE['route'],'10.0.2.2 sl0')
                    sannprófa('ftpd start','FTP listening')
                    sannprófa(samnefni_VALUE['netstat'],'10.0.2.20:21','LISTEN');sannprófa('ss','LISTEN')
                    sannprófa('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','Villa -16')
                    with ftplib.FTP() as biðlari_VALUE:
                        biðlari_VALUE.connect('127.0.0.2',tengisnúmer,timeout=20);biðlari_VALUE.login();gögn=b'Network address was changed in the guest.\n'
                        biðlari_VALUE.storbinary('STOR net-state.txt',io.BytesIO(gögn));RECEIVED_gögn=bytearray();biðlari_VALUE.retrbinary('RETR net-state.txt',RECEIVED_gögn.extend);assert RECEIVED_gögn==gögn;biðlari_VALUE.delete('net-state.txt')
                    sannprófa('ftpd stop','FTP stopped');sannprófa('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    skrá_VALUE_ddf2aaf3['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Texti):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Texti);assert 찾음,Texti;return tuple(map(int,찾음.groups()))
                    전=저장값(sannprófa('df','RAM only'));sannprófa('echo disk-proof > sys-state.txt');후=저장값(sannprófa(samnefni_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    sannprófa('rm sys-state.txt');assert 저장값(skel('df'))==전
                    Minni_VALUE=sannprófa(samnefni_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');magn_VALUE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Minni_VALUE).groups()));assert 0<magn_VALUE[1]<=magn_VALUE[0] and magn_VALUE[1]+magn_VALUE[2]==magn_VALUE[0]
                    sannprófa(samnefni_VALUE['ps'],'kernel/shell');sannprófa(samnefni_VALUE['uptime'],'seconds')
                    staða_uppl=sannprófa(samnefni_VALUE['top']+' -n 2','kernel/shell');assert staða_uppl.count('PID SLOT STATE')==2,staða_uppl
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    sannprófa('terminal','TERMINAL READY');Keyra_2=len(LOG_lína);senda(b'vi process.txt\n');받기(b'NORMAL',Keyra_2)
                    Keyra_2=len(LOG_lína);senda(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Keyra_2)
                    færsla_Listi=sannprófa('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',færsla_Listi);assert 찾음 and int(찾음.group(2))>0,færsla_Listi
                    sannprófa('free','EL0 mapped KiB: '+찾음.group(2))
                    Keyra_2=len(LOG_lína);senda(b'top\n');받기(b'PID SLOT STATE',Keyra_2);senda(b'q');받기(b'jkoros-native> ',Keyra_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if samnefni_VALUE['df']!='df':
                        Keyra_2=len(LOG_lína);senda((samnefni_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Keyra_2);받기(b'jkoros-native> ',Keyra_2)
                    skrá_VALUE_ddf2aaf3['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as stýring_VALUE:
                    stýring_VALUE.settimeout(15);stýring_VALUE.connect(str(stýring_slóð));Stream_VALUE=stýring_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    senda((('poweroff' if Viðföng.poweroff_only else samnefni_VALUE['poweroff'])+'\n').encode())
                    while True:
                        atvik=json.loads(Stream_VALUE.readline())
                        if atvik.get('event')=='SHUTDOWN':break
                    assert atvik['data']['guest'] and atvik['data']['reason']=='guest-shutdown',atvik
                    assert Ferli_VALUE.wait(timeout=15)==0
                    skrá_VALUE_ddf2aaf3['shutdown']=atvik;skrá_VALUE_ddf2aaf3['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                skrá_VALUE_ddf2aaf3['network_trace']=brú_VALUE.spor_LOG
                assert Viðföng.poweroff_only or any(færsla_VALUE['protocol']==1 and færsla_VALUE['direction']=='from_guest' for færsla_VALUE in brú_VALUE.spor_LOG)
                skrá_VALUE_ddf2aaf3['passed']=True
            finally:
                if Ferli_VALUE.poll() is None:os.killpg(Ferli_VALUE.pid,signal.SIGTERM)
                try:Ferli_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Ferli_VALUE.kill();Ferli_VALUE.wait()
                velja_vara.close();(úttak/'serial.log').write_bytes(LOG_lína);(úttak/'report.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Lykill_VALUE:VALUE for Lykill_VALUE,VALUE in skrá_VALUE_ddf2aaf3.items() if Lykill_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Keyra_2()
