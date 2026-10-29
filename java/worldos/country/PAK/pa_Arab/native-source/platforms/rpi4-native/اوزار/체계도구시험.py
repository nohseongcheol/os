#!/usr/bin/env python3
"""اصلی_کوائف 자체 커널의 IP/ICMP, حالت_قدر طلب_قدر, 현지어 حکم, 게스트 خارج_کرو_ایپ تریخ_دے_مطابق_کرو."""
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


def چلاؤ():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];سیٹنگاں={};ناں_جدول={}
    if 인수.edition:
        나라=인수.edition.resolve();سیٹنگاں=json.loads((나라/'native.json').read_text());ناں_جدول=سیٹنگاں['identifiers'];기준=나라/سیٹنگاں['source']/سیٹنگاں['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        مہمان_b78e430d=나라/'host/qemu'
        if مہمان_b78e430d.is_file():os.environ['QEMU_AARCH64']=str(مہمان_b78e430d)
    اوزار=기준/Path(سیٹنگاں.get('runner','اوزار/نفاذ_کرو_حکم.py')).parent
    sys.path.insert(0,str(اوزار))
    def 읽기(ناں):
        راہ=اوزار/(ناں_جدول.get(ناں,ناں)+'.py');حالت_قدر_102996da=importlib.util.spec_from_file_location('test_'+ناں,str(راہ));모듈=importlib.util.module_from_spec(حالت_قدر_102996da);حالت_قدر_102996da.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('نفاذ_کرو_حکم');망모듈=읽기('نیٹ_ورک_برج');حکم=getattr(실행모듈,ناں_جدول.get('حکم','حکم'));برج_ٹائپ_کرو=getattr(망모듈,ناں_جدول.get('نیٹ_ورک_برج','نیٹ_ورک_برج'))
    عرف_قدر=سیٹنگاں.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_پتا','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'نمایش_کرو_مدد'})
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
    رپورٹ_قدر={'passed':False,'country':سیٹنگاں.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    لاگ_صف=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        کنٹرول_راہ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as تلاش_قدر:تلاش_قدر.bind(('127.0.0.1',0));접속번호=تلاش_قدر.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with برج_ٹائپ_کرو(접속번호,کھیچو=True,مہمان_پتا_4bde7f91=ipTestText('10.0.2.20'),مہمان_پتا='127.0.0.2') as برج_قدر:
            عمل_قدر=subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(کنٹرول_راہ)]+برج_قدر.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            انتخاب_کرو_شے=selectors.DefaultSelector();انتخاب_کرو_شے.register(عمل_قدر.stdout,selectors.EVENT_READ)
            def 받기(نمایش_کرو_قدر,چلاؤ=0,제한=45):
                끝=time.monotonic()+제한
                while نمایش_کرو_قدر not in لاگ_صف[چلاؤ:]:
                    if time.monotonic()>끝 or عمل_قدر.poll() is not None:raise AssertionError('Missing '+repr(نمایش_کرو_قدر)+'\n'+لاگ_صف[چلاؤ:].decode('utf-8','replace'))
                    for کلید_قدر,_ in انتخاب_کرو_شے.select(.1):
                        کوائف=کلید_قدر.fileobj.read(65536)
                        if کوائف:لاگ_صف.extend(کوائف)
                return لاگ_صف[چلاؤ:].decode('utf-8','replace').replace('\r\n','\n')
            def بھیجو(کوائف):عمل_قدر.stdin.write(کوائف);عمل_قدر.stdin.flush()
            def شیل(متن):
                متن=ipTestText(متن)
                print(رپورٹ_قدر['country'],متن,flush=True);차례[0]+=1;نمایش_کرو_قدر='__SYSTEM_DONE_'+str(차례[0])+'__';چلاؤ=len(لاگ_صف)
                بھیجو((متن+'; echo; echo '+نمایش_کرو_قدر+'\n').encode())
                끝표시=('\r\n'+نمایش_کرو_قدر+'\r\n').encode();받기(끝표시,چلاؤ)
                끝자리=لاگ_صف.index(끝표시,چلاؤ)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return لاگ_صف[چلاؤ:].decode('utf-8','replace').replace('\r\n','\n')
            def تصدیق_کرو(متن,*값들):
                جواب_دیوؤ=شیل(متن)
                for قدر in 값들:assert ipTestText(قدر) in جواب_دیوؤ,(متن,قدر,جواب_دیوؤ)
                return جواب_دیوؤ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    مدد_قدر_8d901cc2=تصدیق_کرو('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in عرف_قدر.values():assert 별칭 in مدد_قدر_8d901cc2,(별칭,مدد_قدر_8d901cc2)
                    تصدیق_کرو(عرف_قدر['help']+' system','Network / system')
                    تصدیق_کرو('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    تصدیق_کرو(عرف_قدر['ipconfig'],'inet 10.0.2.15');تصدیق_کرو('ip addr show','sl0: UP');تصدیق_کرو('ifconfig','sl0: UP')
                    for ناجائز_سیٹنگاں in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        نقص=تصدیق_کرو('ipconfig set '+ناجائز_سیٹنگاں+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in نقص,نقص
                        تصدیق_کرو('ipconfig','inet 10.0.2.15')
                    تصدیق_کرو('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    تصدیق_کرو(عرف_قدر['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصدیق_کرو('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    تصدیق_کرو('ip link set dev sl0 down','sl0: DOWN');تصدیق_کرو('ping -c 1 10.0.2.2; echo STATUS=$?','نقص -100','STATUS=1')
                    تصدیق_کرو('ipconfig up','sl0: UP')
                    تصدیق_کرو(عرف_قدر['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    تصدیق_کرو('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصدیق_کرو('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');تصدیق_کرو(عرف_قدر['route'],'10.0.2.2 sl0')
                    تصدیق_کرو('ftpd start','FTP listening')
                    تصدیق_کرو(عرف_قدر['netstat'],'10.0.2.20:21','LISTEN');تصدیق_کرو('ss','LISTEN')
                    تصدیق_کرو('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','نقص -16')
                    with ftplib.FTP() as گاہک_قدر:
                        گاہک_قدر.connect('127.0.0.2',접속번호,timeout=20);گاہک_قدر.login();کوائف=b'Network address was changed in the guest.\n'
                        گاہک_قدر.storbinary('STOR net-state.txt',io.BytesIO(کوائف));받은자료=bytearray();گاہک_قدر.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==کوائف;گاہک_قدر.delete('net-state.txt')
                    تصدیق_کرو('ftpd stop','FTP stopped');تصدیق_کرو('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    رپورٹ_قدر['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(متن):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',متن);assert 찾음,متن;return tuple(map(int,찾음.groups()))
                    전=저장값(تصدیق_کرو('df','RAM only'));تصدیق_کرو('echo disk-proof > sys-state.txt');후=저장값(تصدیق_کرو(عرف_قدر['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    تصدیق_کرو('rm sys-state.txt');assert 저장값(شیل('df'))==전
                    میموری_قدر=تصدیق_کرو(عرف_قدر['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',میموری_قدر).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    تصدیق_کرو(عرف_قدر['ps'],'kernel/shell');تصدیق_کرو(عرف_قدر['uptime'],'seconds')
                    حالت_معلومات=تصدیق_کرو(عرف_قدر['top']+' -n 2','kernel/shell');assert حالت_معلومات.count('PID SLOT STATE')==2,حالت_معلومات
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    تصدیق_کرو('terminal','TERMINAL READY');چلاؤ=len(لاگ_صف);بھیجو(b'vi process.txt\n');받기(b'NORMAL',چلاؤ)
                    چلاؤ=len(لاگ_صف);بھیجو(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',چلاؤ)
                    داخلہ_فرست=تصدیق_کرو('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',داخلہ_فرست);assert 찾음 and int(찾음.group(2))>0,داخلہ_فرست
                    تصدیق_کرو('free','EL0 mapped KiB: '+찾음.group(2))
                    چلاؤ=len(لاگ_صف);بھیجو(b'top\n');받기(b'PID SLOT STATE',چلاؤ);بھیجو(b'q');받기(b'jkoros-native> ',چلاؤ)
                    # Test a multibyte prefix through the real shell completion path.
                    if عرف_قدر['df']!='df':
                        چلاؤ=len(لاگ_صف);بھیجو((عرف_قدر['df'][:-1]+'\t\n').encode());받기(b'RAM only',چلاؤ);받기(b'jkoros-native> ',چلاؤ)
                    رپورٹ_قدر['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as کنٹرول_قدر:
                    کنٹرول_قدر.settimeout(15);کنٹرول_قدر.connect(str(کنٹرول_راہ));سٹریم_قدر=کنٹرول_قدر.makefile('rwb');json.loads(سٹریم_قدر.readline());سٹریم_قدر.write(b'{"execute":"qmp_capabilities"}\n');سٹریم_قدر.flush()
                    while 'return' not in json.loads(سٹریم_قدر.readline()):pass
                    بھیجو((('poweroff' if 인수.poweroff_only else عرف_قدر['poweroff'])+'\n').encode())
                    while True:
                        واقعہ=json.loads(سٹریم_قدر.readline())
                        if واقعہ.get('event')=='SHUTDOWN':break
                    assert واقعہ['data']['guest'] and واقعہ['data']['reason']=='guest-shutdown',واقعہ
                    assert عمل_قدر.wait(timeout=15)==0
                    رپورٹ_قدر['shutdown']=واقعہ;رپورٹ_قدر['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                رپورٹ_قدر['network_trace']=برج_قدر.추적기록
                assert 인수.poweroff_only or any(داخلہ_قدر['protocol']==1 and داخلہ_قدر['direction']=='from_guest' for داخلہ_قدر in برج_قدر.추적기록)
                رپورٹ_قدر['passed']=True
            finally:
                if عمل_قدر.poll() is None:os.killpg(عمل_قدر.pid,signal.SIGTERM)
                try:عمل_قدر.wait(timeout=10)
                except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
                انتخاب_کرو_شے.close();(출력/'serial.log').write_bytes(لاگ_صف);(출력/'report.json').write_text(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({کلید_قدر:قدر for کلید_قدر,قدر in رپورٹ_قدر.items() if کلید_قدر!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':چلاؤ()
