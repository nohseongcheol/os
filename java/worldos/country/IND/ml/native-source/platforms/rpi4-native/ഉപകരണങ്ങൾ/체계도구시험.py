#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ 자체 커널의 IP/ICMP, അവസ്ഥ_മൂല്യം ചോദ്യം_മൂല്യം, 현지어 ആജ്ഞ, 게스트 പുറത്തുകടക്കൽ_പ്രോഗ്രാം സാധൂകരിക്കുക."""
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


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b=argparse.ArgumentParser();പാഴ്_സർ_48ee4b1b.add_argument('--edition',type=Path);പാഴ്_സർ_48ee4b1b.add_argument('--output',type=Path);പാഴ്_സർ_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=പാഴ്_സർ_48ee4b1b.parse_args()
    പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം=Path(__file__).resolve().parents[1];സജ്ജീകരണം={};നാ_മം_పట్టిక={}
    if 인수.edition:
        나라=인수.edition.resolve();സജ്ജീകരണം=json.loads((나라/'native.json').read_text());നാ_മം_పట్టిక=സജ്ജീകരണം['identifiers'];പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം=나라/സജ്ജീകരണം['source']/സജ്ജീകരണം['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ഹോസ്റ്റ്=나라/'host/qemu'
        if ഹോസ്റ്റ്.is_file():os.environ['QEMU_AARCH64']=str(ഹോസ്റ്റ്)
    ഉപകരണങ്ങൾ=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/Path(സജ്ജീകരണം.get('runner','ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py')).parent
    sys.path.insert(0,str(ഉപകരണങ്ങൾ))
    def വായന(പേരു്):
        വഴി=ഉപകരണങ്ങൾ/(നാ_മം_పట్టిక.get(പേരു്,പേരു്)+'.py');കേസ്_മൂല്യം=importlib.util.spec_from_file_location('test_'+പേരു്,str(വഴി));മൊഡ്യൂൾ_മൂല്യം=importlib.util.module_from_spec(കേസ്_മൂല്യം);കേസ്_മൂല്യം.loader.exec_module(മൊഡ്യൂൾ_മൂല്യം);return മൊഡ്യൂൾ_മൂല്യം
    실행모듈=വായന('നടപ്പാക്കുക_കമാന്_ഡ്');നെറ്റ്_വർക്ക്_മൊഡ്യൂൾ=വായന('നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്');ആജ്ഞ=getattr(실행모듈,നാ_മം_పట్టిక.get('ആജ്ഞ','ആജ്ഞ'));ബ്രിഡ്_ജ്_ടൈപ്പ്_ചെയ്യുക=getattr(നെറ്റ്_വർക്ക്_മൊഡ്യൂൾ,നാ_മം_పట్టిక.get('നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്','നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്'))
    അപരനാമം_മൂല്യം=സജ്ജീകരണം.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_വിലാസം','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'പ്രദർശനം_സഹായം'})
    sys.path.insert(0,str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ഫലം=인수.output or പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/system-tools';ഫലം.mkdir(parents=True,exist_ok=True)
    నివేదిక_മൂല്യം={'passed':False,'country':സജ്ജീകരണം.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ലോഗ്_രേഖ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        നിയന്ത്രണം_പാത=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as തിരയൽ_മൂല്യം:തിരയൽ_മൂല്യം.bind(('127.0.0.1',0));പോര്_ട്ട്_നമ്പര്=തിരയൽ_മൂല്യം.getsockname()[1]
            if not 50000<=പോര്_ട്ട്_നമ്പര്<=50007:break
        with ബ്രിഡ്_ജ്_ടൈപ്പ്_ചെയ്യുക(പോര്_ട്ട്_നമ്പര്,ക്യാപ്_ചർ_ചെയ്യുക=True,അതിഥി_ഇമെയിൽ=ipTestText('10.0.2.20'),ഹോസ്റ്റ്_ഇമെയിൽ='127.0.0.2') as ബ്രിഡ്_ജ്_മൂല്യം:
            പ്രോസസ്_മൂല്യം=subprocess.Popen(ആജ്ഞ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(നിയന്ത്രണം_പാത)]+ബ്രിഡ്_ജ്_മൂല്യം.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            നോക്കിയെടുക്കുക_ഇനം=selectors.DefaultSelector();നോക്കിയെടുക്കുക_ഇനം.register(പ്രോസസ്_മൂല്യം.stdout,selectors.EVENT_READ)
            def 받기(പ്രദർശനം_മൂല്യം,നടപ്പിലാക്കുക=0,제한=45):
                끝=time.monotonic()+제한
                while പ്രദർശനം_മൂല്യം not in ലോഗ്_രേഖ[നടപ്പിലാക്കുക:]:
                    if time.monotonic()>끝 or പ്രോസസ്_മൂല്യം.poll() is not None:raise AssertionError('Missing '+repr(പ്രദർശനം_മൂല്യം)+'\n'+ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8','replace'))
                    for കീ_മൂല്യം,_ in നോക്കിയെടുക്കുക_ഇനം.select(.1):
                        ഡാറ്റാ=കീ_മൂല്യം.fileobj.read(65536)
                        if ഡാറ്റാ:ലോഗ്_രേഖ.extend(ഡാറ്റാ)
                return ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8','replace').replace('\r\n','\n')
            def അയയ്ക്കുക(ഡാറ്റാ):പ്രോസസ്_മൂല്യം.stdin.write(ഡാറ്റാ);പ്രോസസ്_മൂല്യം.stdin.flush()
            def ഷെല്(പദാവലി):
                പദാവലി=ipTestText(പദാവലി)
                print(నివేదిక_മൂല്യം['country'],പദാവലി,flush=True);차례[0]+=1;പ്രദർശനം_മൂല്യം='__SYSTEM_DONE_'+str(차례[0])+'__';നടപ്പിലാക്കുക=len(ലോഗ്_രേഖ)
                അയയ്ക്കുക((പദാവലി+'; echo; echo '+പ്രദർശനം_മൂല്യം+'\n').encode())
                끝표시=('\r\n'+പ്രദർശനം_മൂല്യം+'\r\n').encode();받기(끝표시,നടപ്പിലാക്കുക)
                അവസാനിപ്പിക്കുക_പദവി=ലോഗ്_രേഖ.index(끝표시,നടപ്പിലാക്കുക)+len(끝표시)
                받기(b'jkoros-native> ',അവസാനിപ്പിക്കുക_പദവി)
                return ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8','replace').replace('\r\n','\n')
            def പരിശോധിക്കുക(പദാവലി,*값들):
                മറുപടി_നൽകുക=ഷെല്(പദാവലി)
                for മൂല്യം in 값들:assert ipTestText(മൂല്യം) in മറുപടി_നൽകുക,(പദാവലി,മൂല്യം,മറുപടി_നൽകുക)
                return മറുപടി_നൽകുക
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    സഹായം_മൂല്യം=പരിശോധിക്കുക('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in അപരനാമം_മൂല്യം.values():assert 별칭 in സഹായം_മൂല്യം,(별칭,സഹായം_മൂല്യം)
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['help']+' system','Network / system')
                    പരിശോധിക്കുക('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['ipconfig'],'inet 10.0.2.15');പരിശോധിക്കുക('ip addr show','sl0: UP');പരിശോധിക്കുക('ifconfig','sl0: UP')
                    for അസാധുവായ_ക്രമീകരണം in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        പിശക്=പരിശോധിക്കുക('ipconfig set '+അസാധുവായ_ക്രമീകരണം+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in പിശക്,പിശക്
                        പരിശോധിക്കുക('ipconfig','inet 10.0.2.15')
                    പരിശോധിക്കുക('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    പരിശോധിക്കുക('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    പരിശോധിക്കുക('ip link set dev sl0 down','sl0: DOWN');പരിശോധിക്കുക('ping -c 1 10.0.2.2; echo STATUS=$?','പിശക് -100','STATUS=1')
                    പരിശോധിക്കുക('ipconfig up','sl0: UP')
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    പരിശോധിക്കുക('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    പരിശോധിക്കുക('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');പരിശോധിക്കുക(അപരനാമം_മൂല്യം['route'],'10.0.2.2 sl0')
                    പരിശോധിക്കുക('ftpd start','FTP listening')
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['netstat'],'10.0.2.20:21','LISTEN');പരിശോധിക്കുക('ss','LISTEN')
                    പരിശോധിക്കുക('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','പിശക് -16')
                    with ftplib.FTP() as ക്ലയന്_റ്_മൂല്യം:
                        ക്ലയന്_റ്_മൂല്യം.connect('127.0.0.2',പോര്_ട്ട്_നമ്പര്,timeout=20);ക്ലയന്_റ്_മൂല്യം.login();ഡാറ്റാ=b'Network address was changed in the guest.\n'
                        ക്ലയന്_റ്_മൂല്യം.storbinary('STOR net-state.txt',io.BytesIO(ഡാറ്റാ));받은자료=bytearray();ക്ലയന്_റ്_മൂല്യം.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ഡാറ്റാ;ക്ലയന്_റ്_മൂല്യം.delete('net-state.txt')
                    പരിശോധിക്കുക('ftpd stop','FTP stopped');പരിശോധിക്കുക('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    నివేదిక_മൂല്യം['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(പദാവലി):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',പദാവലി);assert 찾음,പദാവലി;return tuple(map(int,찾음.groups()))
                    전=저장값(പരിശോധിക്കുക('df','RAM only'));പരിശോധിക്കുക('echo disk-proof > sys-state.txt');후=저장값(പരിശോധിക്കുക(അപരനാമം_മൂല്യം['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    പരിശോധിക്കുക('rm sys-state.txt');assert 저장값(ഷെല്('df'))==전
                    മെമ്മറി_മൂല്യം=പരിശോധിക്കുക(അപരനാമം_മൂല്യം['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',മെമ്മറി_മൂല്യം).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    പരിശോധിക്കുക(അപരനാമം_മൂല്യം['ps'],'kernel/shell');പരിശോധിക്കുക(അപരനാമം_മൂല്യം['uptime'],'seconds')
                    അവസ്ഥ_വിവരം=പരിശോധിക്കുക(അപരനാമം_മൂല്യം['top']+' -n 2','kernel/shell');assert അവസ്ഥ_വിവരം.count('PID SLOT STATE')==2,അവസ്ഥ_വിവരം
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    പരിശോധിക്കുക('terminal','TERMINAL READY');നടപ്പിലാക്കുക=len(ലോഗ്_രേഖ);അയയ്ക്കുക(b'vi process.txt\n');받기(b'NORMAL',നടപ്പിലാക്കുക)
                    നടപ്പിലാക്കുക=len(ലോഗ്_രേഖ);അയയ്ക്കുക(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',നടപ്പിലാക്കുക)
                    എന്_ട്രി_ലിസ്റ്റ്=പരിശോധിക്കുക('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',എന്_ട്രി_ലിസ്റ്റ്);assert 찾음 and int(찾음.group(2))>0,എന്_ട്രി_ലിസ്റ്റ്
                    പരിശോധിക്കുക('free','EL0 mapped KiB: '+찾음.group(2))
                    നടപ്പിലാക്കുക=len(ലോഗ്_രേഖ);അയയ്ക്കുക(b'top\n');받기(b'PID SLOT STATE',നടപ്പിലാക്കുക);അയയ്ക്കുക(b'q');받기(b'jkoros-native> ',നടപ്പിലാക്കുക)
                    # Test a multibyte prefix through the real shell completion path.
                    if അപരനാമം_മൂല്യം['df']!='df':
                        നടപ്പിലാക്കുക=len(ലോഗ്_രേഖ);അയയ്ക്കുക((അപരനാമം_മൂല്യം['df'][:-1]+'\t\n').encode());받기(b'RAM only',നടപ്പിലാക്കുക);받기(b'jkoros-native> ',നടപ്പിലാക്കുക)
                    నివేదిక_മൂല്യം['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as നിയന്ത്രണം_മൂല്യം:
                    നിയന്ത്രണം_മൂല്യം.settimeout(15);നിയന്ത്രണം_മൂല്യം.connect(str(നിയന്ത്രണം_പാത));സ്ട്രീം_മൂല്യം=നിയന്ത്രണം_മൂല്യം.makefile('rwb');json.loads(സ്ട്രീം_മൂല്യം.readline());സ്ട്രീം_മൂല്യം.write(b'{"execute":"qmp_capabilities"}\n');സ്ട്രീം_മൂല്യം.flush()
                    while 'return' not in json.loads(സ്ട്രീം_മൂല്യം.readline()):pass
                    അയയ്ക്കുക((('poweroff' if 인수.poweroff_only else അപരനാമം_മൂല്യം['poweroff'])+'\n').encode())
                    while True:
                        ഇവന്റ്=json.loads(സ്ട്രീം_മൂല്യം.readline())
                        if ഇവന്റ്.get('event')=='SHUTDOWN':break
                    assert ഇവന്റ്['data']['guest'] and ഇവന്റ്['data']['reason']=='guest-shutdown',ഇവന്റ്
                    assert പ്രോസസ്_മൂല്യം.wait(timeout=15)==0
                    నివేదిక_മൂല്യം['shutdown']=ഇവന്റ്;నివేదిక_മൂല്യം['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                నివేదిక_മൂല്യം['network_trace']=ബ്രിഡ്_ജ്_മൂല്യം.ട്രെയ്സ്_ലോഗ്
                assert 인수.poweroff_only or any(എന്_ട്രി_മൂല്യം['protocol']==1 and എന്_ട്രി_മൂല്യം['direction']=='from_guest' for എന്_ട്രി_മൂല്യം in ബ്രിഡ്_ജ്_മൂല്യം.ട്രെയ്സ്_ലോഗ്)
                నివేదిక_മൂല്യം['passed']=True
            finally:
                if പ്രോസസ്_മൂല്യം.poll() is None:os.killpg(പ്രോസസ്_മൂല്യം.pid,signal.SIGTERM)
                try:പ്രോസസ്_മൂല്യം.wait(timeout=10)
                except subprocess.TimeoutExpired:പ്രോസസ്_മൂല്യം.kill();പ്രോസസ്_മൂല്യം.wait()
                നോക്കിയെടുക്കുക_ഇനം.close();(ഫലം/'serial.log').write_bytes(ലോഗ്_രേഖ);(ഫലം/'report.json').write_text(json.dumps(నివేదిక_മൂല്യം,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({കീ_മൂല്യം:മൂല്യം for കീ_മൂല്യം,മൂല്യം in నివేదిక_മൂല്യം.items() if കീ_മൂല്യം!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':നടപ്പിലാക്കുക()
