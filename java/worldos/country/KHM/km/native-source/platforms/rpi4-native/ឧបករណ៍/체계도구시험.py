#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ 자체 커널의 IP/ICMP, ភាព_តំលៃ សំណើ_តំលៃ, 현지어 ពាក្យ_បញ្ជា, 게스트 ចេញ_កម្មវិធី ធ្វើអោយមានសុពលភាព."""
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


def រត់():
    មុខងារ_ញែក_48ee4b1b=argparse.ArgumentParser();មុខងារ_ញែក_48ee4b1b.add_argument('--edition',type=Path);មុខងារ_ញែក_48ee4b1b.add_argument('--output',type=Path);មុខងារ_ញែក_48ee4b1b.add_argument('--poweroff-only',action='store_true');អាគុយម៉ង់=មុខងារ_ញែក_48ee4b1b.parse_args()
    បញ្ចាំង_ឬស=Path(__file__).resolve().parents[1];ការកំណត់={};ឈ្មោះ_តារាង={}
    if អាគុយម៉ង់.edition:
        나라=អាគុយម៉ង់.edition.resolve();ការកំណត់=json.loads((나라/'native.json').read_text());ឈ្មោះ_តារាង=ការកំណត់['identifiers'];បញ្ចាំង_ឬស=나라/ការកំណត់['source']/ការកំណត់['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ហូស=나라/'host/qemu'
        if ហូស.is_file():os.environ['QEMU_AARCH64']=str(ហូស)
    ឧបករណ៍=បញ្ចាំង_ឬស/Path(ការកំណត់.get('runner','ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py')).parent
    sys.path.insert(0,str(ឧបករណ៍))
    def អាន(ឈ្មោះ):
        ផ្លូវ=ឧបករណ៍/(ឈ្មោះ_តារាង.get(ឈ្មោះ,ឈ្មោះ)+'.py');ករណី_តំលៃ=importlib.util.spec_from_file_location('test_'+ឈ្មោះ,str(ផ្លូវ));ម៉ូឌុល_តំលៃ_6d2d8bf4=importlib.util.module_from_spec(ករណី_តំលៃ);ករណី_តំលៃ.loader.exec_module(ម៉ូឌុល_តំលៃ_6d2d8bf4);return ម៉ូឌុល_តំលៃ_6d2d8bf4
    실행모듈=អាន('អនុវត្ត_ពាក្យបញ្ជា');ណិតវឺក_ម៉ូឌុល=អាន('통신다리');ពាក្យ_បញ្ជា=getattr(실행모듈,ឈ្មោះ_តារាង.get('ពាក្យ_បញ្ជា','ពាក្យ_បញ្ជា'));다리형=getattr(ណិតវឺក_ម៉ូឌុល,ឈ្មោះ_តារាង.get('통신다리','통신다리'))
    ផ្លូវកាត់_តំលៃ_0a38607b=ការកំណត់.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'អាសយដ្ឋាន_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'បង្ហាញ_ជំនួយ'})
    sys.path.insert(0,str(បញ្ចាំង_ឬស/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(បញ្ចាំង_ឬស);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    លទ្ធផល=អាគុយម៉ង់.output or បញ្ចាំង_ឬស/'build/verification/system-tools';លទ្ធផល.mkdir(parents=True,exist_ok=True)
    រាយការណ៍_តំលៃ={'passed':False,'country':ការកំណត់.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    កំណត់_ហេតុ_ថត=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        អង្គបញ្ជា_ផ្លូវ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as រុករក_តំលៃ:រុករក_តំលៃ.bind(('127.0.0.1',0));លេខរន្ធ=រុករក_តំលៃ.getsockname()[1]
            if not 50000<=លេខរន្ធ<=50007:break
        with 다리형(លេខរន្ធ,ថត=True,ភ្ញៀវ_អ៊ីម៉ែល=ipTestText('10.0.2.20'),ហូស_អ៊ីម៉ែល='127.0.0.2') as 다리:
            ដំណើរការ_តំលៃ=subprocess.Popen(ពាក្យ_បញ្ជា()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(អង្គបញ្ជា_ផ្លូវ)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ជ្រើសរើស_ធាតុ=selectors.DefaultSelector();ជ្រើសរើស_ធាតុ.register(ដំណើរការ_តំលៃ.stdout,selectors.EVENT_READ)
            def 받기(បង្ហាញ_តំលៃ,រត់=0,제한=45):
                끝=time.monotonic()+제한
                while បង្ហាញ_តំលៃ not in កំណត់_ហេតុ_ថត[រត់:]:
                    if time.monotonic()>끝 or ដំណើរការ_តំលៃ.poll() is not None:raise AssertionError('Missing '+repr(បង្ហាញ_តំលៃ)+'\n'+កំណត់_ហេតុ_ថត[រត់:].decode('utf-8','replace'))
                    for ឃី_តំលៃ,_ in ជ្រើសរើស_ធាតុ.select(.1):
                        ទិន្នន័យ=ឃី_តំលៃ.fileobj.read(65536)
                        if ទិន្នន័យ:កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
                return កំណត់_ហេតុ_ថត[រត់:].decode('utf-8','replace').replace('\r\n','\n')
            def ផ្ញើ(ទិន្នន័យ):ដំណើរការ_តំលៃ.stdin.write(ទិន្នន័យ);ដំណើរការ_តំលៃ.stdin.flush()
            def 셸(អត្ថបទ):
                អត្ថបទ=ipTestText(អត្ថបទ)
                print(រាយការណ៍_តំលៃ['country'],អត្ថបទ,flush=True);차례[0]+=1;បង្ហាញ_តំលៃ='__SYSTEM_DONE_'+str(차례[0])+'__';រត់=len(កំណត់_ហេតុ_ថត)
                ផ្ញើ((អត្ថបទ+'; echo; echo '+បង្ហាញ_តំលៃ+'\n').encode())
                끝표시=('\r\n'+បង្ហាញ_តំលៃ+'\r\n').encode();받기(끝표시,រត់)
                បញ្ចប់_កំណត់ទីតាំង=កំណត់_ហេតុ_ថត.index(끝표시,រត់)+len(끝표시)
                받기(b'jkoros-native> ',បញ្ចប់_កំណត់ទីតាំង)
                return កំណត់_ហេតុ_ថត[រត់:].decode('utf-8','replace').replace('\r\n','\n')
            def ផ្ទៀងផ្ទាត់(អត្ថបទ,*값들):
                ឆ្លើយតប=셸(អត្ថបទ)
                for តំលៃ in 값들:assert ipTestText(តំលៃ) in ឆ្លើយតប,(អត្ថបទ,តំលៃ,ឆ្លើយតប)
                return ឆ្លើយតប
            try:
                받기(b'jkoros-native> ')
                if not អាគុយម៉ង់.poweroff_only:
                    ជំនួយ_តំលៃ=ផ្ទៀងផ្ទាត់('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ផ្លូវកាត់_តំលៃ_0a38607b.values():assert 별칭 in ជំនួយ_តំលៃ,(별칭,ជំនួយ_តំលៃ)
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['help']+' system','Network / system')
                    ផ្ទៀងផ្ទាត់('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['ipconfig'],'inet 10.0.2.15');ផ្ទៀងផ្ទាត់('ip addr show','sl0: UP');ផ្ទៀងផ្ទាត់('ifconfig','sl0: UP')
                    for មិនត្រឹមត្រូវ_ការកំណត់ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        កំហុស=ផ្ទៀងផ្ទាត់('ipconfig set '+មិនត្រឹមត្រូវ_ការកំណត់+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in កំហុស,កំហុស
                        ផ្ទៀងផ្ទាត់('ipconfig','inet 10.0.2.15')
                    ផ្ទៀងផ្ទាត់('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ផ្ទៀងផ្ទាត់('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ផ្ទៀងផ្ទាត់('ip link set dev sl0 down','sl0: DOWN');ផ្ទៀងផ្ទាត់('ping -c 1 10.0.2.2; echo STATUS=$?','កំហុស -100','STATUS=1')
                    ផ្ទៀងផ្ទាត់('ipconfig up','sl0: UP')
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ផ្ទៀងផ្ទាត់('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ផ្ទៀងផ្ទាត់('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['route'],'10.0.2.2 sl0')
                    ផ្ទៀងផ្ទាត់('ftpd start','FTP listening')
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['netstat'],'10.0.2.20:21','LISTEN');ផ្ទៀងផ្ទាត់('ss','LISTEN')
                    ផ្ទៀងផ្ទាត់('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','កំហុស -16')
                    with ftplib.FTP() as អតិថិជន_តំលៃ:
                        អតិថិជន_តំលៃ.connect('127.0.0.2',លេខរន្ធ,timeout=20);អតិថិជន_តំលៃ.login();ទិន្នន័យ=b'Network address was changed in the guest.\n'
                        អតិថិជន_តំលៃ.storbinary('STOR net-state.txt',io.BytesIO(ទិន្នន័យ));받은자료=bytearray();អតិថិជន_តំលៃ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ទិន្នន័យ;អតិថិជន_តំលៃ.delete('net-state.txt')
                    ផ្ទៀងផ្ទាត់('ftpd stop','FTP stopped');ផ្ទៀងផ្ទាត់('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    រាយការណ៍_តំលៃ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(អត្ថបទ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',អត្ថបទ);assert 찾음,អត្ថបទ;return tuple(map(int,찾음.groups()))
                    전=저장값(ផ្ទៀងផ្ទាត់('df','RAM only'));ផ្ទៀងផ្ទាត់('echo disk-proof > sys-state.txt');후=저장값(ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ផ្ទៀងផ្ទាត់('rm sys-state.txt');assert 저장값(셸('df'))==전
                    សតិ_តំលៃ=ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',សតិ_តំលៃ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['ps'],'kernel/shell');ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['uptime'],'seconds')
                    ភាព_ព័ត៌មាន=ផ្ទៀងផ្ទាត់(ផ្លូវកាត់_តំលៃ_0a38607b['top']+' -n 2','kernel/shell');assert ភាព_ព័ត៌មាន.count('PID SLOT STATE')==2,ភាព_ព័ត៌មាន
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ផ្ទៀងផ្ទាត់('terminal','TERMINAL READY');រត់=len(កំណត់_ហេតុ_ថត);ផ្ញើ(b'vi process.txt\n');받기(b'NORMAL',រត់)
                    រត់=len(កំណត់_ហេតុ_ថត);ផ្ញើ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',រត់)
                    ការបញ្ចូល_បញ្ជី=ផ្ទៀងផ្ទាត់('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ការបញ្ចូល_បញ្ជី);assert 찾음 and int(찾음.group(2))>0,ការបញ្ចូល_បញ្ជី
                    ផ្ទៀងផ្ទាត់('free','EL0 mapped KiB: '+찾음.group(2))
                    រត់=len(កំណត់_ហេតុ_ថត);ផ្ញើ(b'top\n');받기(b'PID SLOT STATE',រត់);ផ្ញើ(b'q');받기(b'jkoros-native> ',រត់)
                    # Test a multibyte prefix through the real shell completion path.
                    if ផ្លូវកាត់_តំលៃ_0a38607b['df']!='df':
                        រត់=len(កំណត់_ហេតុ_ថត);ផ្ញើ((ផ្លូវកាត់_តំលៃ_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',រត់);받기(b'jkoros-native> ',រត់)
                    រាយការណ៍_តំលៃ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as អង្គបញ្ជា_តំលៃ:
                    អង្គបញ្ជា_តំលៃ.settimeout(15);អង្គបញ្ជា_តំលៃ.connect(str(អង្គបញ្ជា_ផ្លូវ));ស្ទ្រីម_តំលៃ=អង្គបញ្ជា_តំលៃ.makefile('rwb');json.loads(ស្ទ្រីម_តំលៃ.readline());ស្ទ្រីម_តំលៃ.write(b'{"execute":"qmp_capabilities"}\n');ស្ទ្រីម_តំលៃ.flush()
                    while 'return' not in json.loads(ស្ទ្រីម_តំលៃ.readline()):pass
                    ផ្ញើ((('poweroff' if អាគុយម៉ង់.poweroff_only else ផ្លូវកាត់_តំលៃ_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        ព្រឹត្តិការណ៍=json.loads(ស្ទ្រីម_តំលៃ.readline())
                        if ព្រឹត្តិការណ៍.get('event')=='SHUTDOWN':break
                    assert ព្រឹត្តិការណ៍['data']['guest'] and ព្រឹត្តិការណ៍['data']['reason']=='guest-shutdown',ព្រឹត្តិការណ៍
                    assert ដំណើរការ_តំលៃ.wait(timeout=15)==0
                    រាយការណ៍_តំលៃ['shutdown']=ព្រឹត្តិការណ៍;រាយការណ៍_តំលៃ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                រាយការណ៍_តំលៃ['network_trace']=다리.ត្រេស_កំណត់_ហេតុ
                assert អាគុយម៉ង់.poweroff_only or any(ការបញ្ចូល_តំលៃ['protocol']==1 and ការបញ្ចូល_តំលៃ['direction']=='from_guest' for ការបញ្ចូល_តំលៃ in 다리.ត្រេស_កំណត់_ហេតុ)
                រាយការណ៍_តំលៃ['passed']=True
            finally:
                if ដំណើរការ_តំលៃ.poll() is None:os.killpg(ដំណើរការ_តំលៃ.pid,signal.SIGTERM)
                try:ដំណើរការ_តំលៃ.wait(timeout=10)
                except subprocess.TimeoutExpired:ដំណើរការ_តំលៃ.kill();ដំណើរការ_តំលៃ.wait()
                ជ្រើសរើស_ធាតុ.close();(លទ្ធផល/'serial.log').write_bytes(កំណត់_ហេតុ_ថត);(លទ្ធផល/'report.json').write_text(json.dumps(រាយការណ៍_តំលៃ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ឃី_តំលៃ:តំលៃ for ឃី_តំលៃ,តំលៃ in រាយការណ៍_តំលៃ.items() if ឃី_តំលៃ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':រត់()
