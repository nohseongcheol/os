#!/usr/bin/env python3
"""בפועל_נתונים עצמי 커널의 IP/ICMP, מצב_ערך שאילתה_ערך, 현지어 פקודה, 게스트 יציאה_תוכנית לאמת."""
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


def הפעלה():
    מנתח_48ee4b1b=argparse.ArgumentParser();מנתח_48ee4b1b.add_argument('--edition',type=Path);מנתח_48ee4b1b.add_argument('--output',type=Path);מנתח_48ee4b1b.add_argument('--poweroff-only',action='store_true');ארגומנטים=מנתח_48ee4b1b.parse_args()
    לשקף_בסיס=Path(__file__).resolve().parents[1];הגדרות={};שם_טבלה={}
    if ארגומנטים.edition:
        מוסיקת_קאנטרי_ערך=ארגומנטים.edition.resolve();הגדרות=json.loads((מוסיקת_קאנטרי_ערך/'native.json').read_text());שם_טבלה=הגדרות['identifiers'];לשקף_בסיס=מוסיקת_קאנטרי_ערך/הגדרות['source']/הגדרות['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(מוסיקת_קאנטרי_ערך/'native-edition.py'),'check'])
        ארח=מוסיקת_קאנטרי_ערך/'host/qemu'
        if ארח.is_file():os.environ['QEMU_AARCH64']=str(ארח)
    כלים=לשקף_בסיס/Path(הגדרות.get('runner','כלים/לבצע_פקודה.py')).parent
    sys.path.insert(0,str(כלים))
    def קרא(שם):
        נתיב=כלים/(שם_טבלה.get(שם,שם)+'.py');ערך_חוזה=importlib.util.spec_from_file_location('test_'+שם,str(נתיב));מודול_ערך=importlib.util.module_from_spec(ערך_חוזה);ערך_חוזה.loader.exec_module(מודול_ערך);return מודול_ערך
    실행모듈=קרא('לבצע_פקודה');רשת_מודול=קרא('גשר_3de4fe3a');פקודה=getattr(실행모듈,שם_טבלה.get('פקודה','פקודה'));גשר_כתב=getattr(רשת_מודול,שם_טבלה.get('גשר_3de4fe3a','גשר_3de4fe3a'))
    כינוי_ערך=הגדרות.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'כתובת_IP','ping':'נסה_תגובה','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'הופעה_עזרה'})
    sys.path.insert(0,str(לשקף_בסיס/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(לשקף_בסיס);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    פלטטקסט=ארגומנטים.output or לשקף_בסיס/'build/verification/system-tools';פלטטקסט.mkdir(parents=True,exist_ok=True)
    דוח_ערך_ddf2aaf3={'passed':False,'country':הגדרות.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    לרשום_שיא=bytearray();רצף_ערך=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        פקד_נתיב=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as חפש_ערך:חפש_ערך.bind(('127.0.0.1',0));מספר_יציאה=חפש_ערך.getsockname()[1]
            if not 50000<=מספר_יציאה<=50007:break
        with גשר_כתב(מספר_יציאה,לכוד=True,אורח_למען=ipTestText('10.0.2.20'),ארח_למען='127.0.0.2') as גשר_ערך:
            תהליך_ערך=subprocess.Popen(פקודה()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(פקד_נתיב)]+גשר_ערך.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            בחר_פריט=selectors.DefaultSelector();בחר_פריט.register(תהליך_ערך.stdout,selectors.EVENT_READ)
            def לקבל(הופעה_ערך,הפעלה=0,제한=45):
                끝=time.monotonic()+제한
                while הופעה_ערך not in לרשום_שיא[הפעלה:]:
                    if time.monotonic()>끝 or תהליך_ערך.poll() is not None:raise AssertionError('Missing '+repr(הופעה_ערך)+'\n'+לרשום_שיא[הפעלה:].decode('utf-8','replace'))
                    for מקש_ערך,_ in בחר_פריט.select(.1):
                        נתונים=מקש_ערך.fileobj.read(65536)
                        if נתונים:לרשום_שיא.extend(נתונים)
                return לרשום_שיא[הפעלה:].decode('utf-8','replace').replace('\r\n','\n')
            def שלח(נתונים):תהליך_ערך.stdin.write(נתונים);תהליך_ערך.stdin.flush()
            def מעטפת(טקסט):
                טקסט=ipTestText(טקסט)
                print(דוח_ערך_ddf2aaf3['country'],טקסט,flush=True);רצף_ערך[0]+=1;הופעה_ערך='__SYSTEM_DONE_'+str(רצף_ערך[0])+'__';הפעלה=len(לרשום_שיא)
                שלח((טקסט+'; echo; echo '+הופעה_ערך+'\n').encode())
                סיים_שיחה_סמן=('\r\n'+הופעה_ערך+'\r\n').encode();לקבל(סיים_שיחה_סמן,הפעלה)
                סיים_שיחה_עמדה=לרשום_שיא.index(סיים_שיחה_סמן,הפעלה)+len(סיים_שיחה_סמן)
                לקבל(b'jkoros-native> ',סיים_שיחה_עמדה)
                return לרשום_שיא[הפעלה:].decode('utf-8','replace').replace('\r\n','\n')
            def ודא_אמת(טקסט,*값들):
                מענה=מעטפת(טקסט)
                for ערך in 값들:assert ipTestText(ערך) in מענה,(טקסט,ערך,מענה)
                return מענה
            try:
                לקבל(b'jkoros-native> ')
                if not ארגומנטים.poweroff_only:
                    עזרה_ערך=ודא_אמת('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in כינוי_ערך.values():assert 별칭 in עזרה_ערך,(별칭,עזרה_ערך)
                    ודא_אמת(כינוי_ערך['help']+' system','Network / system')
                    ודא_אמת('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    ודא_אמת(כינוי_ערך['ipconfig'],'inet 10.0.2.15');ודא_אמת('ip addr show','sl0: UP');ודא_אמת('ifconfig','sl0: UP')
                    for לא_חוקי_הגדרות in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        שגיאה=ודא_אמת('ipconfig set '+לא_חוקי_הגדרות+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in שגיאה,שגיאה
                        ודא_אמת('ipconfig','inet 10.0.2.15')
                    ודא_אמת('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    ודא_אמת(כינוי_ערך['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ודא_אמת('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    ודא_אמת('ip link set dev sl0 down','sl0: DOWN');ודא_אמת('ping -c 1 10.0.2.2; echo STATUS=$?','שגיאה -100','STATUS=1')
                    ודא_אמת('ipconfig up','sl0: UP')
                    ודא_אמת(כינוי_ערך['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    ודא_אמת('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    ודא_אמת('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');ודא_אמת(כינוי_ערך['route'],'10.0.2.2 sl0')
                    ודא_אמת('ftpd start','FTP listening')
                    ודא_אמת(כינוי_ערך['netstat'],'10.0.2.20:21','LISTEN');ודא_אמת('ss','LISTEN')
                    ודא_אמת('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','שגיאה -16')
                    with ftplib.FTP() as לקוח_ערך:
                        לקוח_ערך.connect('127.0.0.2',מספר_יציאה,timeout=20);לקוח_ערך.login();נתונים=b'Network address was changed in the guest.\n'
                        לקוח_ערך.storbinary('STOR net-state.txt',io.BytesIO(נתונים));받은자료=bytearray();לקוח_ערך.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==נתונים;לקוח_ערך.delete('net-state.txt')
                    ודא_אמת('ftpd stop','FTP stopped');ודא_אמת('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    דוח_ערך_ddf2aaf3['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(טקסט):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',טקסט);assert 찾음,טקסט;return tuple(map(int,찾음.groups()))
                    전=저장값(ודא_אמת('df','RAM only'));ודא_אמת('echo disk-proof > sys-state.txt');후=저장값(ודא_אמת(כינוי_ערך['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    ודא_אמת('rm sys-state.txt');assert 저장값(מעטפת('df'))==전
                    זיכרון_ערך=ודא_אמת(כינוי_ערך['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',זיכרון_ערך).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    ודא_אמת(כינוי_ערך['ps'],'kernel/shell');ודא_אמת(כינוי_ערך['uptime'],'seconds')
                    מצב_מידע=ודא_אמת(כינוי_ערך['top']+' -n 2','kernel/shell');assert מצב_מידע.count('PID SLOT STATE')==2,מצב_מידע
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    ודא_אמת('terminal','TERMINAL READY');הפעלה=len(לרשום_שיא);שלח(b'vi process.txt\n');לקבל(b'NORMAL',הפעלה)
                    הפעלה=len(לרשום_שיא);שלח(bytes([30,2,1,0,0,0,0]));לקבל(b'jkoros-native> ',הפעלה)
                    ערך_רשימה=ודא_אמת('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ערך_רשימה);assert 찾음 and int(찾음.group(2))>0,ערך_רשימה
                    ודא_אמת('free','EL0 mapped KiB: '+찾음.group(2))
                    הפעלה=len(לרשום_שיא);שלח(b'top\n');לקבל(b'PID SLOT STATE',הפעלה);שלח(b'q');לקבל(b'jkoros-native> ',הפעלה)
                    # Test a multibyte prefix through the real shell completion path.
                    if כינוי_ערך['df']!='df':
                        הפעלה=len(לרשום_שיא);שלח((כינוי_ערך['df'][:-1]+'\t\n').encode());לקבל(b'RAM only',הפעלה);לקבל(b'jkoros-native> ',הפעלה)
                    דוח_ערך_ddf2aaf3['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as פקד_ערך:
                    פקד_ערך.settimeout(15);פקד_ערך.connect(str(פקד_נתיב));זרם_ערך=פקד_ערך.makefile('rwb');json.loads(זרם_ערך.readline());זרם_ערך.write(b'{"execute":"qmp_capabilities"}\n');זרם_ערך.flush()
                    while 'return' not in json.loads(זרם_ערך.readline()):pass
                    שלח((('poweroff' if ארגומנטים.poweroff_only else כינוי_ערך['poweroff'])+'\n').encode())
                    while True:
                        אירוע=json.loads(זרם_ערך.readline())
                        if אירוע.get('event')=='SHUTDOWN':break
                    assert אירוע['data']['guest'] and אירוע['data']['reason']=='guest-shutdown',אירוע
                    assert תהליך_ערך.wait(timeout=15)==0
                    דוח_ערך_ddf2aaf3['shutdown']=אירוע;דוח_ערך_ddf2aaf3['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                דוח_ערך_ddf2aaf3['network_trace']=גשר_ערך.יומן_מעקב
                assert ארגומנטים.poweroff_only or any(ערך_ערך['protocol']==1 and ערך_ערך['direction']=='from_guest' for ערך_ערך in גשר_ערך.יומן_מעקב)
                דוח_ערך_ddf2aaf3['passed']=True
            finally:
                if תהליך_ערך.poll() is None:os.killpg(תהליך_ערך.pid,signal.SIGTERM)
                try:תהליך_ערך.wait(timeout=10)
                except subprocess.TimeoutExpired:תהליך_ערך.kill();תהליך_ערך.wait()
                בחר_פריט.close();(פלטטקסט/'serial.log').write_bytes(לרשום_שיא);(פלטטקסט/'report.json').write_text(json.dumps(דוח_ערך_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({מקש_ערך:ערך for מקש_ערך,ערך in דוח_ערך_ddf2aaf3.items() if מקש_ערך!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':הפעלה()
