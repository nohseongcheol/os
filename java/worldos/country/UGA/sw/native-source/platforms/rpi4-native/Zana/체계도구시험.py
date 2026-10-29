#!/usr/bin/env python3
"""halisi_data 자체 커널의 IP/ICMP, hali_thamani uliza_thamani, 현지어 amri, 게스트 toka_programu hakikisha."""
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


def endesha():
    kichanganuzi_48ee4b1b=argparse.ArgumentParser();kichanganuzi_48ee4b1b.add_argument('--edition',type=Path);kichanganuzi_48ee4b1b.add_argument('--output',type=Path);kichanganuzi_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=kichanganuzi_48ee4b1b.parse_args()
    기준=Path(__file__).resolve().parents[1];Mipangilio={};jina_jedwali={}
    if 인수.edition:
        나라=인수.edition.resolve();Mipangilio=json.loads((나라/'native.json').read_text());jina_jedwali=Mipangilio['identifiers'];기준=나라/Mipangilio['source']/Mipangilio['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        mwenyeji=나라/'host/qemu'
        if mwenyeji.is_file():os.environ['QEMU_AARCH64']=str(mwenyeji)
    Zana=기준/Path(Mipangilio.get('runner','Zana/tekeleza_amri.py')).parent
    sys.path.insert(0,str(Zana))
    def 읽기(Jina):
        njia=Zana/(jina_jedwali.get(Jina,Jina)+'.py');Kazi_thamani=importlib.util.spec_from_file_location('test_'+Jina,str(njia));moduli_thamani=importlib.util.module_from_spec(Kazi_thamani);Kazi_thamani.loader.exec_module(moduli_thamani);return moduli_thamani
    실행모듈=읽기('tekeleza_amri');Mtandao_moduli=읽기('Mtandao_daraja');amri=getattr(실행모듈,jina_jedwali.get('amri','amri'));daraja_aina=getattr(Mtandao_moduli,jina_jedwali.get('Mtandao_daraja','Mtandao_daraja'))
    lakabu_thamani=Mipangilio.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'anwani_ya_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'onyesha_msaada'})
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
    ripoti_thamani={'passed':False,'country':Mipangilio.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    batli_REKODI=bytearray();MFUATANO_thamani=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        udhibiti_njia=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Duhusi_thamani:Duhusi_thamani.bind(('127.0.0.1',0));namba_ya_kituo=Duhusi_thamani.getsockname()[1]
            if not 50000<=namba_ya_kituo<=50007:break
        with daraja_aina(namba_ya_kituo,unasaji=True,mgeni_anwani=ipTestText('10.0.2.20'),mwenyeji_anwani='127.0.0.2') as daraja_thamani:
            Mchakato_thamani=subprocess.Popen(amri()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(udhibiti_njia)]+daraja_thamani.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            chagua_kipengee=selectors.DefaultSelector();chagua_kipengee.register(Mchakato_thamani.stdout,selectors.EVENT_READ)
            def 받기(onyesha_thamani,endesha=0,제한=45):
                끝=time.monotonic()+제한
                while onyesha_thamani not in batli_REKODI[endesha:]:
                    if time.monotonic()>끝 or Mchakato_thamani.poll() is not None:raise AssertionError('Missing '+repr(onyesha_thamani)+'\n'+batli_REKODI[endesha:].decode('utf-8','replace'))
                    for Kitufe_thamani,_ in chagua_kipengee.select(.1):
                        data=Kitufe_thamani.fileobj.read(65536)
                        if data:batli_REKODI.extend(data)
                return batli_REKODI[endesha:].decode('utf-8','replace').replace('\r\n','\n')
            def tuma(data):Mchakato_thamani.stdin.write(data);Mchakato_thamani.stdin.flush()
            def sheli(SMS):
                SMS=ipTestText(SMS)
                print(ripoti_thamani['country'],SMS,flush=True);MFUATANO_thamani[0]+=1;onyesha_thamani='__SYSTEM_DONE_'+str(MFUATANO_thamani[0])+'__';endesha=len(batli_REKODI)
                tuma((SMS+'; echo; echo '+onyesha_thamani+'\n').encode())
                끝표시=('\r\n'+onyesha_thamani+'\r\n').encode();받기(끝표시,endesha)
                끝자리=batli_REKODI.index(끝표시,endesha)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return batli_REKODI[endesha:].decode('utf-8','replace').replace('\r\n','\n')
            def thibitisha(SMS,*값들):
                jibu=sheli(SMS)
                for thamani in 값들:assert ipTestText(thamani) in jibu,(SMS,thamani,jibu)
                return jibu
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    msaada_thamani=thibitisha('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in lakabu_thamani.values():assert 별칭 in msaada_thamani,(별칭,msaada_thamani)
                    thibitisha(lakabu_thamani['help']+' system','Network / system')
                    thibitisha('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    thibitisha(lakabu_thamani['ipconfig'],'inet 10.0.2.15');thibitisha('ip addr show','sl0: UP');thibitisha('ifconfig','sl0: UP')
                    for batili_Mipangilio in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        kosa=thibitisha('ipconfig set '+batili_Mipangilio+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in kosa,kosa
                        thibitisha('ipconfig','inet 10.0.2.15')
                    thibitisha('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    thibitisha(lakabu_thamani['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    thibitisha('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    thibitisha('ip link set dev sl0 down','sl0: DOWN');thibitisha('ping -c 1 10.0.2.2; echo STATUS=$?','kosa -100','STATUS=1')
                    thibitisha('ipconfig up','sl0: UP')
                    thibitisha(lakabu_thamani['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    thibitisha('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    thibitisha('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');thibitisha(lakabu_thamani['route'],'10.0.2.2 sl0')
                    thibitisha('ftpd start','FTP listening')
                    thibitisha(lakabu_thamani['netstat'],'10.0.2.20:21','LISTEN');thibitisha('ss','LISTEN')
                    thibitisha('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','kosa -16')
                    with ftplib.FTP() as teja_thamani:
                        teja_thamani.connect('127.0.0.2',namba_ya_kituo,timeout=20);teja_thamani.login();data=b'Network address was changed in the guest.\n'
                        teja_thamani.storbinary('STOR net-state.txt',io.BytesIO(data));받은자료=bytearray();teja_thamani.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==data;teja_thamani.delete('net-state.txt')
                    thibitisha('ftpd stop','FTP stopped');thibitisha('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ripoti_thamani['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(thibitisha('df','RAM only'));thibitisha('echo disk-proof > sys-state.txt');후=저장값(thibitisha(lakabu_thamani['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    thibitisha('rm sys-state.txt');assert 저장값(sheli('df'))==전
                    kumbukumbu_thamani_603669bd=thibitisha(lakabu_thamani['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',kumbukumbu_thamani_603669bd).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    thibitisha(lakabu_thamani['ps'],'kernel/shell');thibitisha(lakabu_thamani['uptime'],'seconds')
                    hali_maelezo=thibitisha(lakabu_thamani['top']+' -n 2','kernel/shell');assert hali_maelezo.count('PID SLOT STATE')==2,hali_maelezo
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    thibitisha('terminal','TERMINAL READY');endesha=len(batli_REKODI);tuma(b'vi process.txt\n');받기(b'NORMAL',endesha)
                    endesha=len(batli_REKODI);tuma(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',endesha)
                    ingizo_Orodha=thibitisha('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ingizo_Orodha);assert 찾음 and int(찾음.group(2))>0,ingizo_Orodha
                    thibitisha('free','EL0 mapped KiB: '+찾음.group(2))
                    endesha=len(batli_REKODI);tuma(b'top\n');받기(b'PID SLOT STATE',endesha);tuma(b'q');받기(b'jkoros-native> ',endesha)
                    # Test a multibyte prefix through the real shell completion path.
                    if lakabu_thamani['df']!='df':
                        endesha=len(batli_REKODI);tuma((lakabu_thamani['df'][:-1]+'\t\n').encode());받기(b'RAM only',endesha);받기(b'jkoros-native> ',endesha)
                    ripoti_thamani['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as udhibiti_thamani:
                    udhibiti_thamani.settimeout(15);udhibiti_thamani.connect(str(udhibiti_njia));Stream_thamani=udhibiti_thamani.makefile('rwb');json.loads(Stream_thamani.readline());Stream_thamani.write(b'{"execute":"qmp_capabilities"}\n');Stream_thamani.flush()
                    while 'return' not in json.loads(Stream_thamani.readline()):pass
                    tuma((('poweroff' if 인수.poweroff_only else lakabu_thamani['poweroff'])+'\n').encode())
                    while True:
                        tukio=json.loads(Stream_thamani.readline())
                        if tukio.get('event')=='SHUTDOWN':break
                    assert tukio['data']['guest'] and tukio['data']['reason']=='guest-shutdown',tukio
                    assert Mchakato_thamani.wait(timeout=15)==0
                    ripoti_thamani['shutdown']=tukio;ripoti_thamani['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ripoti_thamani['network_trace']=daraja_thamani.idadi_ya_maingizo_mlalo_batli
                assert 인수.poweroff_only or any(ingizo_thamani['protocol']==1 and ingizo_thamani['direction']=='from_guest' for ingizo_thamani in daraja_thamani.idadi_ya_maingizo_mlalo_batli)
                ripoti_thamani['passed']=True
            finally:
                if Mchakato_thamani.poll() is None:os.killpg(Mchakato_thamani.pid,signal.SIGTERM)
                try:Mchakato_thamani.wait(timeout=10)
                except subprocess.TimeoutExpired:Mchakato_thamani.kill();Mchakato_thamani.wait()
                chagua_kipengee.close();(출력/'serial.log').write_bytes(batli_REKODI);(출력/'report.json').write_text(json.dumps(ripoti_thamani,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kitufe_thamani:thamani for Kitufe_thamani,thamani in ripoti_thamani.items() if Kitufe_thamani!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':endesha()
