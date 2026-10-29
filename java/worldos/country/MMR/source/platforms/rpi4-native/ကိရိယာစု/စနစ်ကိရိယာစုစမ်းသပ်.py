#!/usr/bin/env python3
"""တကယ့်ဒေတာ ကိုယ်ပိုင် 커널의 IP/ICMP, အခြေအနေတန်ဖိုး 조회, 현지어 အမိန့်, 게스트 ထွက်ပရိုဂရမ် မှန်ကန်ကြောင်းစစ်."""
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


def လုပ်ဆောင်():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');အချက်များ=해석기.parse_args()
    စီမံကိန်းအမြစ်=Path(__file__).resolve().parents[1];သတ်မှတ်ချက်={};အမည်ဇယား={}
    if အချက်များ.edition:
        နိုင်ငံတန်ဖိုး=အချက်များ.edition.resolve();သတ်မှတ်ချက်=json.loads((နိုင်ငံတန်ဖိုး/'native.json').read_text());အမည်ဇယား=သတ်မှတ်ချက်['identifiers'];စီမံကိန်းအမြစ်=နိုင်ငံတန်ဖိုး/သတ်မှတ်ချက်['source']/သတ်မှတ်ချက်['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(နိုင်ငံတန်ဖိုး/'native-edition.py'),'check'])
        အိမ်ရှင်=နိုင်ငံတန်ဖိုး/'host/qemu'
        if အိမ်ရှင်.is_file():os.environ['QEMU_AARCH64']=str(အိမ်ရှင်)
    ကိရိယာစု=စီမံကိန်းအမြစ်/Path(သတ်မှတ်ချက်.get('runner','ကိရိယာစု/စက်မောင်း.py')).parent
    sys.path.insert(0,str(ကိရိယာစု))
    def ဖတ်(အမည်):
        လမ်း=ကိရိယာစု/(အမည်ဇယား.get(အမည်,အမည်)+'.py');သဘောတူစည်းမျဉ်းတန်ဖိုး=importlib.util.spec_from_file_location('test_'+အမည်,str(လမ်း));မော်ဂျူးတန်ဖိုး=importlib.util.module_from_spec(သဘောတူစည်းမျဉ်းတန်ဖိုး);သဘောတူစည်းမျဉ်းတန်ဖိုး.loader.exec_module(မော်ဂျူးတန်ဖိုး);return မော်ဂျူးတန်ဖိုး
    လုပ်ဆောင်မှုမော်ဂျူး=ဖတ်('စက်မောင်း');ကွန်ရက်အစိတ်အပိုင်း=ဖတ်('ကွန်ရက်တံတား');အမိန့်=getattr(လုပ်ဆောင်မှုမော်ဂျူး,အမည်ဇယား.get('အမိန့်','အမိန့်'));တံတားအမျိုးပုံစံ=getattr(ကွန်ရက်အစိတ်အပိုင်း,အမည်ဇယား.get('ကွန်ရက်တံတား','ကွန်ရက်တံတား'))
    별명=သတ်မှတ်ချက်.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IPလိပ်စာ','ping':'တုံ့ပြန်စမ်းသပ်','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'စက်ပိတ်','help':'အကူအညီပြသ'})
    sys.path.insert(0,str(စီမံကိန်းအမြစ်/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(စီမံကိန်းအမြစ်);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    အထွက်=အချက်များ.output or စီမံကိန်းအမြစ်/'build/verification/system-tools';အထွက်.mkdir(parents=True,exist_ok=True)
    အစီရင်ခံစာတန်ဖိုး={'passed':False,'country':သတ်မှတ်ချက်.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    မှတ်တမ်းမှတ်တမ်းတစ်ခု=bytearray();အစဉ်လိုက်တန်ဖိုး=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as ယာယီတန်ဖိုး:
        ထိန်းချုပ်လမ်းကြောင်း=Path(ယာယီတန်ဖိုး)/'qmp.sock'
        while True:
            with socket.socket() as တန်ဖိုးရှာဖွေ:တန်ဖိုးရှာဖွေ.bind(('127.0.0.1',0));ဆက်သွယ်ပေါက်ကိန်း=တန်ဖိုးရှာဖွေ.getsockname()[1]
            if not 50000<=ဆက်သွယ်ပေါက်ကိန်း<=50007:break
        with တံတားအမျိုးပုံစံ(ဆက်သွယ်ပေါက်ကိန်း,포착여부=True,ဧည့်သည်လိပ်စာ=ipTestText('10.0.2.20'),အိမ်ရှင်လိပ်စာ='127.0.0.2') as တံတားတန်ဖိုး:
            လုပ်ငန်းစဉ်=subprocess.Popen(အမိန့်()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ထိန်းချုပ်လမ်းကြောင်း)]+တံတားတန်ဖိုး.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ရွေးအချက်အလက်တစ်ခု=selectors.DefaultSelector();ရွေးအချက်အလက်တစ်ခု.register(လုပ်ငန်းစဉ်.stdout,selectors.EVENT_READ)
            def လက်ခံ(တန်ဖိုးပြသ,လုပ်ဆောင်=0,ကန့်သတ်ချက်တန်ဖိုး=45):
                အဆုံး=time.monotonic()+ကန့်သတ်ချက်တန်ဖိုး
                while တန်ဖိုးပြသ not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:]:
                    if time.monotonic()>အဆုံး or လုပ်ငန်းစဉ်.poll() is not None:raise AssertionError('Missing '+repr(တန်ဖိုးပြသ)+'\n'+မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:].decode('utf-8','replace'))
                    for သော့တန်ဖိုး,_ in ရွေးအချက်အလက်တစ်ခု.select(.1):
                        ဒေတာ=သော့တန်ဖိုး.fileobj.read(65536)
                        if ဒေတာ:မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒေတာ)
                return မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:].decode('utf-8','replace').replace('\r\n','\n')
            def ပို့(ဒေတာ):လုပ်ငန်းစဉ်.stdin.write(ဒေတာ);လုပ်ငန်းစဉ်.stdin.flush()
            def အမိန့်ဝင်း(စာသား):
                စာသား=ipTestText(စာသား)
                print(အစီရင်ခံစာတန်ဖိုး['country'],စာသား,flush=True);အစဉ်လိုက်တန်ဖိုး[0]+=1;တန်ဖိုးပြသ='__SYSTEM_DONE_'+str(အစဉ်လိုက်တန်ဖိုး[0])+'__';လုပ်ဆောင်=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့((စာသား+'; echo; echo '+တန်ဖိုးပြသ+'\n').encode())
                끝표시=('\r\n'+တန်ဖိုးပြသ+'\r\n').encode();လက်ခံ(끝표시,လုပ်ဆောင်)
                အဆုံးနေရာ=မှတ်တမ်းမှတ်တမ်းတစ်ခု.index(끝표시,လုပ်ဆောင်)+len(끝표시)
                လက်ခံ(b'jkoros-native> ',အဆုံးနေရာ)
                return မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:].decode('utf-8','replace').replace('\r\n','\n')
            def အတည်ပြု(စာသား,*တန်ဖိုးများ):
                အကြောင်းပြန်ချက်=အမိန့်ဝင်း(စာသား)
                for တန်ဖိုး in တန်ဖိုးများ:assert ipTestText(တန်ဖိုး) in အကြောင်းပြန်ချက်,(စာသား,တန်ဖိုး,အကြောင်းပြန်ချက်)
                return အကြောင်းပြန်ချက်
            try:
                လက်ခံ(b'jkoros-native> ')
                if not အချက်များ.poweroff_only:
                    အကူအညီတန်ဖိုး=အတည်ပြု('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in 별명.values():assert 별칭 in အကူအညီတန်ဖိုး,(별칭,အကူအညီတန်ဖိုး)
                    အတည်ပြု(별명['help']+' system','Network / system')
                    အတည်ပြု('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    အတည်ပြု(별명['ipconfig'],'inet 10.0.2.15');အတည်ပြု('ip addr show','sl0: UP');အတည်ပြု('ifconfig','sl0: UP')
                    for မမှန်ကန်သတ်မှတ်ချက် in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        အမှား=အတည်ပြု('ipconfig set '+မမှန်ကန်သတ်မှတ်ချက်+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in အမှား,အမှား
                        အတည်ပြု('ipconfig','inet 10.0.2.15')
                    အတည်ပြု('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    အတည်ပြု(별명['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    အတည်ပြု('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    အတည်ပြု('ip link set dev sl0 down','sl0: DOWN');အတည်ပြု('ping -c 1 10.0.2.2; echo STATUS=$?','အမှား -100','STATUS=1')
                    အတည်ပြု('ipconfig up','sl0: UP')
                    အတည်ပြု(별명['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    အတည်ပြု('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    အတည်ပြု('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');အတည်ပြု(별명['route'],'10.0.2.2 sl0')
                    အတည်ပြု('ftpd start','FTP listening')
                    အတည်ပြု(별명['netstat'],'10.0.2.20:21','LISTEN');အတည်ပြု('ss','LISTEN')
                    အတည်ပြု('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','အမှား -16')
                    with ftplib.FTP() as လက်ခံစက်တန်ဖိုး:
                        လက်ခံစက်တန်ဖိုး.connect('127.0.0.2',ဆက်သွယ်ပေါက်ကိန်း,timeout=20);လက်ခံစက်တန်ဖိုး.login();ဒေတာ=b'Network address was changed in the guest.\n'
                        လက်ခံစက်တန်ဖိုး.storbinary('STOR net-state.txt',io.BytesIO(ဒေတာ));ရရှိဒေတာ=bytearray();လက်ခံစက်တန်ဖိုး.retrbinary('RETR net-state.txt',ရရှိဒေတာ.extend);assert ရရှိဒေတာ==ဒေတာ;လက်ခံစက်တန်ဖိုး.delete('net-state.txt')
                    အတည်ပြု('ftpd stop','FTP stopped');အတည်ပြု('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    အစီရင်ခံစာတန်ဖိုး['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def သိမ်းပြီး(စာသား):
                        တွေ့တန်ဖိုး=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',စာသား);assert တွေ့တန်ဖိုး,စာသား;return tuple(map(int,တွေ့တန်ဖိုး.groups()))
                    전=သိမ်းပြီး(အတည်ပြု('df','RAM only'));အတည်ပြု('echo disk-proof > sys-state.txt');후=သိမ်းပြီး(အတည်ပြု(별명['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    အတည်ပြု('rm sys-state.txt');assert သိမ်းပြီး(အမိန့်ဝင်း('df'))==전
                    မှတ်ဉာဏ်=အတည်ပြု(별명['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',မှတ်ဉာဏ်).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    အတည်ပြု(별명['ps'],'kernel/shell');အတည်ပြု(별명['uptime'],'seconds')
                    လက်ရှိအခြေအနေ=အတည်ပြု(별명['top']+' -n 2','kernel/shell');assert လက်ရှိအခြေအနေ.count('PID SLOT STATE')==2,လက်ရှိအခြေအနေ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    အတည်ပြု('terminal','TERMINAL READY');လုပ်ဆောင်=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ပို့(b'vi process.txt\n');လက်ခံ(b'NORMAL',လုပ်ဆောင်)
                    လုပ်ဆောင်=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ပို့(bytes([30,2,1,0,0,0,0]));လက်ခံ(b'jkoros-native> ',လုပ်ဆောင်)
                    အချက်စာရင်း=အတည်ပြု('ps','SUSPENDED','vi process.txt');တွေ့တန်ဖိုး=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',အချက်စာရင်း);assert တွေ့တန်ဖိုး and int(တွေ့တန်ဖိုး.group(2))>0,အချက်စာရင်း
                    အတည်ပြု('free','EL0 mapped KiB: '+တွေ့တန်ဖိုး.group(2))
                    လုပ်ဆောင်=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ပို့(b'top\n');လက်ခံ(b'PID SLOT STATE',လုပ်ဆောင်);ပို့(b'q');လက်ခံ(b'jkoros-native> ',လုပ်ဆောင်)
                    # Test a multibyte prefix through the real shell completion path.
                    if 별명['df']!='df':
                        လုပ်ဆောင်=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ပို့((별명['df'][:-1]+'\t\n').encode());လက်ခံ(b'RAM only',လုပ်ဆောင်);လက်ခံ(b'jkoros-native> ',လုပ်ဆောင်)
                    အစီရင်ခံစာတန်ဖိုး['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ထိန်းချုပ်တန်ဖိုး:
                    ထိန်းချုပ်တန်ဖိုး.settimeout(15);ထိန်းချုပ်တန်ဖိုး.connect(str(ထိန်းချုပ်လမ်းကြောင်း));စီးကြောင်းတန်ဖိုး=ထိန်းချုပ်တန်ဖိုး.makefile('rwb');json.loads(စီးကြောင်းတန်ဖိုး.readline());စီးကြောင်းတန်ဖိုး.write(b'{"execute":"qmp_capabilities"}\n');စီးကြောင်းတန်ဖိုး.flush()
                    while 'return' not in json.loads(စီးကြောင်းတန်ဖိုး.readline()):pass
                    ပို့((('poweroff' if အချက်များ.poweroff_only else 별명['poweroff'])+'\n').encode())
                    while True:
                        ဖြစ်ရပ်=json.loads(စီးကြောင်းတန်ဖိုး.readline())
                        if ဖြစ်ရပ်.get('event')=='SHUTDOWN':break
                    assert ဖြစ်ရပ်['data']['guest'] and ဖြစ်ရပ်['data']['reason']=='guest-shutdown',ဖြစ်ရပ်
                    assert လုပ်ငန်းစဉ်.wait(timeout=15)==0
                    အစီရင်ခံစာတန်ဖိုး['shutdown']=ဖြစ်ရပ်;အစီရင်ခံစာတန်ဖိုး['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                အစီရင်ခံစာတန်ဖိုး['network_trace']=တံတားတန်ဖိုး.ခြေရာမှတ်တမ်း
                assert အချက်များ.poweroff_only or any(အချက်တန်ဖိုး['protocol']==1 and အချက်တန်ဖိုး['direction']=='from_guest' for အချက်တန်ဖိုး in တံတားတန်ဖိုး.ခြေရာမှတ်တမ်း)
                အစီရင်ခံစာတန်ဖိုး['passed']=True
            finally:
                if လုပ်ငန်းစဉ်.poll() is None:os.killpg(လုပ်ငန်းစဉ်.pid,signal.SIGTERM)
                try:လုပ်ငန်းစဉ်.wait(timeout=10)
                except subprocess.TimeoutExpired:လုပ်ငန်းစဉ်.kill();လုပ်ငန်းစဉ်.wait()
                ရွေးအချက်အလက်တစ်ခု.close();(အထွက်/'serial.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု);(အထွက်/'report.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({သော့တန်ဖိုး:တန်ဖိုး for သော့တန်ဖိုး,တန်ဖိုး in အစီရင်ခံစာတန်ဖိုး.items() if သော့တန်ဖိုး!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':လုပ်ဆောင်()
