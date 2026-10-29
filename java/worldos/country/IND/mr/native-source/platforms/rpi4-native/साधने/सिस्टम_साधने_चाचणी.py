#!/usr/bin/env python3
"""वास्तविक_डेटा स्वकीय 커널의 IP/ICMP, राज्य_मूल्य क्वेरी_मूल्य, 현지어 आदेश, 게스트 निर्गमन_करा_अनुप्रयोग प्रमाणित."""
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


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b=argparse.ArgumentParser();व्याकरणविश्लेषक_48ee4b1b.add_argument('--edition',type=Path);व्याकरणविश्लेषक_48ee4b1b.add_argument('--output',type=Path);व्याकरणविश्लेषक_48ee4b1b.add_argument('--poweroff-only',action='store_true');बाबी=व्याकरणविश्लेषक_48ee4b1b.parse_args()
    प्रोजेक्ट_मूळ=Path(__file__).resolve().parents[1];संयोजना={};नाव_सारणी={}
    if बाबी.edition:
        देश_मूल्य=बाबी.edition.resolve();संयोजना=json.loads((देश_मूल्य/'native.json').read_text());नाव_सारणी=संयोजना['identifiers'];प्रोजेक्ट_मूळ=देश_मूल्य/संयोजना['source']/संयोजना['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(देश_मूल्य/'native-edition.py'),'check'])
        होस्ट=देश_मूल्य/'host/qemu'
        if होस्ट.is_file():os.environ['QEMU_AARCH64']=str(होस्ट)
    साधने=प्रोजेक्ट_मूळ/Path(संयोजना.get('runner','साधने/आज्ञा_कार्यवाही_करा.py')).parent
    sys.path.insert(0,str(साधने))
    def वाचन(नाव):
        मार्ग=साधने/(नाव_सारणी.get(नाव,नाव)+'.py');काम_मूल्य=importlib.util.spec_from_file_location('test_'+नाव,str(मार्ग));मॉड्यूल_मूल्य=importlib.util.module_from_spec(काम_मूल्य);काम_मूल्य.loader.exec_module(मॉड्यूल_मूल्य);return मॉड्यूल_मूल्य
    निष्पादन_मॉड्यूल=वाचन('आज्ञा_कार्यवाही_करा');संचारजाळे_मॉड्यूल=वाचन('संचारजाळे_ब्रिज');आदेश=getattr(निष्पादन_मॉड्यूल,नाव_सारणी.get('आदेश','आदेश'));ब्रिज_टाइप_करा=getattr(संचारजाळे_मॉड्यूल,नाव_सारणी.get('संचारजाळे_ब्रिज','संचारजाळे_ब्रिज'))
    उपनाम_मूल्य=संयोजना.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_पत्ता','ping':'प्रतिसाद_चाचणी','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'पॉवर_बंद','help':'मदत_शो'})
    sys.path.insert(0,str(प्रोजेक्ट_मूळ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(प्रोजेक्ट_मूळ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    आउटपुट=बाबी.output or प्रोजेक्ट_मूळ/'build/verification/system-tools';आउटपुट.mkdir(parents=True,exist_ok=True)
    अहवाल_मूल्य={'passed':False,'country':संयोजना.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    लॉग_नोंद=bytearray();क्रम_मूल्य_e9fa7815=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as तात्पुरते_मूल्य:
        नियंत्रण_पथ=Path(तात्पुरते_मूल्य)/'qmp.sock'
        while True:
            with socket.socket() as शोध_मूल्य:शोध_मूल्य.bind(('127.0.0.1',0));पोर्ट_नंबर=शोध_मूल्य.getsockname()[1]
            if not 50000<=पोर्ट_नंबर<=50007:break
        with ब्रिज_टाइप_करा(पोर्ट_नंबर,कॅप्चर_करा=True,अतिथी_पत्ता=ipTestText('10.0.2.20'),होस्ट_पत्ता='127.0.0.2') as ब्रिज_मूल्य:
            प्रक्रिया_मूल्य=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(नियंत्रण_पथ)]+ब्रिज_मूल्य.अग्रेषित_वितर्क(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            निवडून_घ्या_आयटम=selectors.DefaultSelector();निवडून_घ्या_आयटम.register(प्रक्रिया_मूल्य.stdout,selectors.EVENT_READ)
            def स्वीकारा(मूल्य_शो,सुरू_करा=0,मर्यादा_मूल्य=45):
                शेवट=time.monotonic()+मर्यादा_मूल्य
                while मूल्य_शो not in लॉग_नोंद[सुरू_करा:]:
                    if time.monotonic()>शेवट or प्रक्रिया_मूल्य.poll() is not None:raise AssertionError('Missing '+repr(मूल्य_शो)+'\n'+लॉग_नोंद[सुरू_करा:].decode('utf-8','replace'))
                    for कळ_मूल्य,_ in निवडून_घ्या_आयटम.select(.1):
                        डेटा=कळ_मूल्य.fileobj.read(65536)
                        if डेटा:लॉग_नोंद.extend(डेटा)
                return लॉग_नोंद[सुरू_करा:].decode('utf-8','replace').replace('\r\n','\n')
            def पाठवा(डेटा):प्रक्रिया_मूल्य.stdin.write(डेटा);प्रक्रिया_मूल्य.stdin.flush()
            def शेल(पाठ्य):
                पाठ्य=ipTestText(पाठ्य)
                print(अहवाल_मूल्य['country'],पाठ्य,flush=True);क्रम_मूल्य_e9fa7815[0]+=1;मूल्य_शो='__SYSTEM_DONE_'+str(क्रम_मूल्य_e9fa7815[0])+'__';सुरू_करा=len(लॉग_नोंद)
                पाठवा((पाठ्य+'; echo; echo '+मूल्य_शो+'\n').encode())
                शेवट_करा_खूण=('\r\n'+मूल्य_शो+'\r\n').encode();स्वीकारा(शेवट_करा_खूण,सुरू_करा)
                शेवट_करा_स्थान=लॉग_नोंद.index(शेवट_करा_खूण,सुरू_करा)+len(शेवट_करा_खूण)
                स्वीकारा(b'jkoros-native> ',शेवट_करा_स्थान)
                return लॉग_नोंद[सुरू_करा:].decode('utf-8','replace').replace('\r\n','\n')
            def पडताळा(पाठ्य,*मूल्ये):
                प्रत्युत्तर_द्या=शेल(पाठ्य)
                for मूल्य in मूल्ये:assert ipTestText(मूल्य) in प्रत्युत्तर_द्या,(पाठ्य,मूल्य,प्रत्युत्तर_द्या)
                return प्रत्युत्तर_द्या
            try:
                स्वीकारा(b'jkoros-native> ')
                if not बाबी.poweroff_only:
                    मदत_मूल्य=पडताळा('help system','ipconfig','ping','ps','top','df','poweroff')
                    for पर्यायी_नाव in उपनाम_मूल्य.values():assert पर्यायी_नाव in मदत_मूल्य,(पर्यायी_नाव,मदत_मूल्य)
                    पडताळा(उपनाम_मूल्य['help']+' system','Network / system')
                    पडताळा('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    पडताळा(उपनाम_मूल्य['ipconfig'],'inet 10.0.2.15');पडताळा('ip addr show','sl0: UP');पडताळा('ifconfig','sl0: UP')
                    for अवैध_सेटिंग्ज in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        त्रुटी=पडताळा('ipconfig set '+अवैध_सेटिंग्ज+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in त्रुटी,त्रुटी
                        पडताळा('ipconfig','inet 10.0.2.15')
                    पडताळा('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    पडताळा(उपनाम_मूल्य['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    पडताळा('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    पडताळा('ip link set dev sl0 down','sl0: DOWN');पडताळा('ping -c 1 10.0.2.2; echo STATUS=$?','त्रुटी -100','STATUS=1')
                    पडताळा('ipconfig up','sl0: UP')
                    पडताळा(उपनाम_मूल्य['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    पडताळा('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    पडताळा('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');पडताळा(उपनाम_मूल्य['route'],'10.0.2.2 sl0')
                    पडताळा('ftpd start','FTP listening')
                    पडताळा(उपनाम_मूल्य['netstat'],'10.0.2.20:21','LISTEN');पडताळा('ss','LISTEN')
                    पडताळा('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','त्रुटी -16')
                    with ftplib.FTP() as क्लायंट_मूल्य:
                        क्लायंट_मूल्य.connect('127.0.0.2',पोर्ट_नंबर,timeout=20);क्लायंट_मूल्य.login();डेटा=b'Network address was changed in the guest.\n'
                        क्लायंट_मूल्य.storbinary('STOR net-state.txt',io.BytesIO(डेटा));स्वीकारलेले_डेटा=bytearray();क्लायंट_मूल्य.retrbinary('RETR net-state.txt',स्वीकारलेले_डेटा.extend);assert स्वीकारलेले_डेटा==डेटा;क्लायंट_मूल्य.delete('net-state.txt')
                    पडताळा('ftpd stop','FTP stopped');पडताळा('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    अहवाल_मूल्य['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def साठवलेले(पाठ्य):
                        सापडलेले_मूल्य=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',पाठ्य);assert सापडलेले_मूल्य,पाठ्य;return tuple(map(int,सापडलेले_मूल्य.groups()))
                    आधी_मूल्य=साठवलेले(पडताळा('df','RAM only'));पडताळा('echo disk-proof > sys-state.txt');नंतर_राज्य=साठवलेले(पडताळा(उपनाम_मूल्य['df'],'RAM only'))
                    assert नंतर_राज्य[1]-आधी_मूल्य[1]==16384 and नंतर_राज्य[4]-आधी_मूल्य[4]==1 and नंतर_राज्य[3]-आधी_मूल्य[3]==11,(आधी_मूल्य,नंतर_राज्य)
                    पडताळा('rm sys-state.txt');assert साठवलेले(शेल('df'))==आधी_मूल्य
                    स्मृती_मूल्य=पडताळा(उपनाम_मूल्य['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');परिमाण_मूल्य=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',स्मृती_मूल्य).groups()));assert 0<परिमाण_मूल्य[1]<=परिमाण_मूल्य[0] and परिमाण_मूल्य[1]+परिमाण_मूल्य[2]==परिमाण_मूल्य[0]
                    पडताळा(उपनाम_मूल्य['ps'],'kernel/shell');पडताळा(उपनाम_मूल्य['uptime'],'seconds')
                    राज्य_माहिती=पडताळा(उपनाम_मूल्य['top']+' -n 2','kernel/shell');assert राज्य_माहिती.count('PID SLOT STATE')==2,राज्य_माहिती
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    पडताळा('terminal','TERMINAL READY');सुरू_करा=len(लॉग_नोंद);पाठवा(b'vi process.txt\n');स्वीकारा(b'NORMAL',सुरू_करा)
                    सुरू_करा=len(लॉग_नोंद);पाठवा(bytes([30,2,1,0,0,0,0]));स्वीकारा(b'jkoros-native> ',सुरू_करा)
                    प्रविष्टी_यादी=पडताळा('ps','SUSPENDED','vi process.txt');सापडलेले_मूल्य=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',प्रविष्टी_यादी);assert सापडलेले_मूल्य and int(सापडलेले_मूल्य.group(2))>0,प्रविष्टी_यादी
                    पडताळा('free','EL0 mapped KiB: '+सापडलेले_मूल्य.group(2))
                    सुरू_करा=len(लॉग_नोंद);पाठवा(b'top\n');स्वीकारा(b'PID SLOT STATE',सुरू_करा);पाठवा(b'q');स्वीकारा(b'jkoros-native> ',सुरू_करा)
                    # Test a multibyte prefix through the real shell completion path.
                    if उपनाम_मूल्य['df']!='df':
                        सुरू_करा=len(लॉग_नोंद);पाठवा((उपनाम_मूल्य['df'][:-1]+'\t\n').encode());स्वीकारा(b'RAM only',सुरू_करा);स्वीकारा(b'jkoros-native> ',सुरू_करा)
                    अहवाल_मूल्य['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as नियंत्रण_मूल्य:
                    नियंत्रण_मूल्य.settimeout(15);नियंत्रण_मूल्य.connect(str(नियंत्रण_पथ));प्रवाह_मूल्य=नियंत्रण_मूल्य.makefile('rwb');json.loads(प्रवाह_मूल्य.readline());प्रवाह_मूल्य.write(b'{"execute":"qmp_capabilities"}\n');प्रवाह_मूल्य.flush()
                    while 'return' not in json.loads(प्रवाह_मूल्य.readline()):pass
                    पाठवा((('poweroff' if बाबी.poweroff_only else उपनाम_मूल्य['poweroff'])+'\n').encode())
                    while True:
                        इव्हेंट=json.loads(प्रवाह_मूल्य.readline())
                        if इव्हेंट.get('event')=='SHUTDOWN':break
                    assert इव्हेंट['data']['guest'] and इव्हेंट['data']['reason']=='guest-shutdown',इव्हेंट
                    assert प्रक्रिया_मूल्य.wait(timeout=15)==0
                    अहवाल_मूल्य['shutdown']=इव्हेंट;अहवाल_मूल्य['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                अहवाल_मूल्य['network_trace']=ब्रिज_मूल्य.मागोवा_लॉग
                assert बाबी.poweroff_only or any(प्रविष्टी_मूल्य['protocol']==1 and प्रविष्टी_मूल्य['direction']=='from_guest' for प्रविष्टी_मूल्य in ब्रिज_मूल्य.मागोवा_लॉग)
                अहवाल_मूल्य['passed']=True
            finally:
                if प्रक्रिया_मूल्य.poll() is None:os.killpg(प्रक्रिया_मूल्य.pid,signal.SIGTERM)
                try:प्रक्रिया_मूल्य.wait(timeout=10)
                except subprocess.TimeoutExpired:प्रक्रिया_मूल्य.kill();प्रक्रिया_मूल्य.wait()
                निवडून_घ्या_आयटम.close();(आउटपुट/'serial.log').write_bytes(लॉग_नोंद);(आउटपुट/'report.json').write_text(json.dumps(अहवाल_मूल्य,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({कळ_मूल्य:मूल्य for कळ_मूल्य,मूल्य in अहवाल_मूल्य.items() if कळ_मूल्य!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':सुरू_करा()
