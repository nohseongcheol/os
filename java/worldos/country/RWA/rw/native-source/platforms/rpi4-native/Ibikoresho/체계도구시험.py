#!/usr/bin/env python3
"""nyakuri_amakurushingiro 자체 커널의 IP/ICMP, imimerere_agaciro isaba_agaciro, 현지어 Icyo_wifuza, 게스트 gusohoka_porogaramu kwemeza."""
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


def ihuriro():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];Amagenamiterere={};izina_imbonerahamwe={}
    if 인수.edition:
        나라=인수.edition.resolve();Amagenamiterere=json.loads((나라/'native.json').read_text());izina_imbonerahamwe=Amagenamiterere['identifiers'];기준=나라/Amagenamiterere['source']/Amagenamiterere['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        gucumbikira=나라/'host/qemu'
        if gucumbikira.is_file():os.environ['QEMU_AARCH64']=str(gucumbikira)
    Ibikoresho=기준/Path(Amagenamiterere.get('runner','Ibikoresho/gukora_ibwiriza.py')).parent
    sys.path.insert(0,str(Ibikoresho))
    def 읽기(Izina):
        Inzira=Ibikoresho/(izina_imbonerahamwe.get(Izina,Izina)+'.py');ikibazo_agaciro=importlib.util.spec_from_file_location('test_'+Izina,str(Inzira));모듈=importlib.util.module_from_spec(ikibazo_agaciro);ikibazo_agaciro.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('gukora_ibwiriza');망모듈=읽기('통신다리');Icyo_wifuza=getattr(실행모듈,izina_imbonerahamwe.get('Icyo_wifuza','Icyo_wifuza'));다리형=getattr(망모듈,izina_imbonerahamwe.get('통신다리','통신다리'))
    ihinanzira_agaciro_0a38607b=Amagenamiterere.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'Aderesi_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'kugaragaza_ifashayoboro'})
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
    raporo_agaciro={'passed':False,'country':Amagenamiterere.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    kubika_umurongo=bytearray();URUKURIKIRANE_agaciro=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        icunga_inzira=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Gushaka_agaciro:Gushaka_agaciro.bind(('127.0.0.1',0));접속번호=Gushaka_agaciro.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,ishusho_ba7b8054=True,게스트주소=ipTestText('10.0.2.20'),gucumbikira_aderesi='127.0.0.2') as 다리:
            Inzira_agaciro=subprocess.Popen(Icyo_wifuza()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(icunga_inzira)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            guhitamo_igice=selectors.DefaultSelector();guhitamo_igice.register(Inzira_agaciro.stdout,selectors.EVENT_READ)
            def 받기(kugaragaza_agaciro,ihuriro=0,제한=45):
                끝=time.monotonic()+제한
                while kugaragaza_agaciro not in kubika_umurongo[ihuriro:]:
                    if time.monotonic()>끝 or Inzira_agaciro.poll() is not None:raise AssertionError('Missing '+repr(kugaragaza_agaciro)+'\n'+kubika_umurongo[ihuriro:].decode('utf-8','replace'))
                    for buto_agaciro,_ in guhitamo_igice.select(.1):
                        amakurushingiro=buto_agaciro.fileobj.read(65536)
                        if amakurushingiro:kubika_umurongo.extend(amakurushingiro)
                return kubika_umurongo[ihuriro:].decode('utf-8','replace').replace('\r\n','\n')
            def kohereza(amakurushingiro):Inzira_agaciro.stdin.write(amakurushingiro);Inzira_agaciro.stdin.flush()
            def insomamabwiriza(Umwandiko):
                Umwandiko=ipTestText(Umwandiko)
                print(raporo_agaciro['country'],Umwandiko,flush=True);URUKURIKIRANE_agaciro[0]+=1;kugaragaza_agaciro='__SYSTEM_DONE_'+str(URUKURIKIRANE_agaciro[0])+'__';ihuriro=len(kubika_umurongo)
                kohereza((Umwandiko+'; echo; echo '+kugaragaza_agaciro+'\n').encode())
                끝표시=('\r\n'+kugaragaza_agaciro+'\r\n').encode();받기(끝표시,ihuriro)
                끝자리=kubika_umurongo.index(끝표시,ihuriro)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return kubika_umurongo[ihuriro:].decode('utf-8','replace').replace('\r\n','\n')
            def gusuzuma(Umwandiko,*값들):
                gusubiza=insomamabwiriza(Umwandiko)
                for agaciro in 값들:assert ipTestText(agaciro) in gusubiza,(Umwandiko,agaciro,gusubiza)
                return gusubiza
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ifashayoboro_agaciro=gusuzuma('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ihinanzira_agaciro_0a38607b.values():assert 별칭 in ifashayoboro_agaciro,(별칭,ifashayoboro_agaciro)
                    gusuzuma(ihinanzira_agaciro_0a38607b['help']+' system','Network / system')
                    gusuzuma('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    gusuzuma(ihinanzira_agaciro_0a38607b['ipconfig'],'inet 10.0.2.15');gusuzuma('ip addr show','sl0: UP');gusuzuma('ifconfig','sl0: UP')
                    for kitemewe_Amagenamiterere in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        IKOSA=gusuzuma('ipconfig set '+kitemewe_Amagenamiterere+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in IKOSA,IKOSA
                        gusuzuma('ipconfig','inet 10.0.2.15')
                    gusuzuma('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    gusuzuma(ihinanzira_agaciro_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    gusuzuma('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    gusuzuma('ip link set dev sl0 down','sl0: DOWN');gusuzuma('ping -c 1 10.0.2.2; echo STATUS=$?','IKOSA -100','STATUS=1')
                    gusuzuma('ipconfig up','sl0: UP')
                    gusuzuma(ihinanzira_agaciro_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    gusuzuma('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    gusuzuma('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');gusuzuma(ihinanzira_agaciro_0a38607b['route'],'10.0.2.2 sl0')
                    gusuzuma('ftpd start','FTP listening')
                    gusuzuma(ihinanzira_agaciro_0a38607b['netstat'],'10.0.2.20:21','LISTEN');gusuzuma('ss','LISTEN')
                    gusuzuma('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','IKOSA -16')
                    with ftplib.FTP() as umukiriya_agaciro:
                        umukiriya_agaciro.connect('127.0.0.2',접속번호,timeout=20);umukiriya_agaciro.login();amakurushingiro=b'Network address was changed in the guest.\n'
                        umukiriya_agaciro.storbinary('STOR net-state.txt',io.BytesIO(amakurushingiro));받은자료=bytearray();umukiriya_agaciro.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==amakurushingiro;umukiriya_agaciro.delete('net-state.txt')
                    gusuzuma('ftpd stop','FTP stopped');gusuzuma('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    raporo_agaciro['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Umwandiko):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Umwandiko);assert 찾음,Umwandiko;return tuple(map(int,찾음.groups()))
                    전=저장값(gusuzuma('df','RAM only'));gusuzuma('echo disk-proof > sys-state.txt');후=저장값(gusuzuma(ihinanzira_agaciro_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    gusuzuma('rm sys-state.txt');assert 저장값(insomamabwiriza('df'))==전
                    ububiko_agaciro=gusuzuma(ihinanzira_agaciro_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ububiko_agaciro).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    gusuzuma(ihinanzira_agaciro_0a38607b['ps'],'kernel/shell');gusuzuma(ihinanzira_agaciro_0a38607b['uptime'],'seconds')
                    imimerere_amakuru=gusuzuma(ihinanzira_agaciro_0a38607b['top']+' -n 2','kernel/shell');assert imimerere_amakuru.count('PID SLOT STATE')==2,imimerere_amakuru
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    gusuzuma('terminal','TERMINAL READY');ihuriro=len(kubika_umurongo);kohereza(b'vi process.txt\n');받기(b'NORMAL',ihuriro)
                    ihuriro=len(kubika_umurongo);kohereza(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ihuriro)
                    icyinjizwa_Urutonde=gusuzuma('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',icyinjizwa_Urutonde);assert 찾음 and int(찾음.group(2))>0,icyinjizwa_Urutonde
                    gusuzuma('free','EL0 mapped KiB: '+찾음.group(2))
                    ihuriro=len(kubika_umurongo);kohereza(b'top\n');받기(b'PID SLOT STATE',ihuriro);kohereza(b'q');받기(b'jkoros-native> ',ihuriro)
                    # Test a multibyte prefix through the real shell completion path.
                    if ihinanzira_agaciro_0a38607b['df']!='df':
                        ihuriro=len(kubika_umurongo);kohereza((ihinanzira_agaciro_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',ihuriro);받기(b'jkoros-native> ',ihuriro)
                    raporo_agaciro['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as icunga_agaciro:
                    icunga_agaciro.settimeout(15);icunga_agaciro.connect(str(icunga_inzira));Stream_agaciro=icunga_agaciro.makefile('rwb');json.loads(Stream_agaciro.readline());Stream_agaciro.write(b'{"execute":"qmp_capabilities"}\n');Stream_agaciro.flush()
                    while 'return' not in json.loads(Stream_agaciro.readline()):pass
                    kohereza((('poweroff' if 인수.poweroff_only else ihinanzira_agaciro_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        icyabaye=json.loads(Stream_agaciro.readline())
                        if icyabaye.get('event')=='SHUTDOWN':break
                    assert icyabaye['data']['guest'] and icyabaye['data']['reason']=='guest-shutdown',icyabaye
                    assert Inzira_agaciro.wait(timeout=15)==0
                    raporo_agaciro['shutdown']=icyabaye;raporo_agaciro['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                raporo_agaciro['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(icyinjizwa_agaciro['protocol']==1 and icyinjizwa_agaciro['direction']=='from_guest' for icyinjizwa_agaciro in 다리.추적기록)
                raporo_agaciro['passed']=True
            finally:
                if Inzira_agaciro.poll() is None:os.killpg(Inzira_agaciro.pid,signal.SIGTERM)
                try:Inzira_agaciro.wait(timeout=10)
                except subprocess.TimeoutExpired:Inzira_agaciro.kill();Inzira_agaciro.wait()
                guhitamo_igice.close();(출력/'serial.log').write_bytes(kubika_umurongo);(출력/'report.json').write_text(json.dumps(raporo_agaciro,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({buto_agaciro:agaciro for buto_agaciro,agaciro in raporo_agaciro.items() if buto_agaciro!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ihuriro()
