#!/usr/bin/env python3
"""اصل_کوائف اپنا 커널의 IP/ICMP, حالت_قدر طلب_قدر, 현지어 حکم, 게스트 خروج_ایپ جواز_دہی_کریں."""
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


def چلائیں():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');دلائل=해석기.parse_args()
    عکس_ڈالنا_روٹ=Path(__file__).resolve().parents[1];ترتیبات={};نام_جدول={}
    if دلائل.edition:
        나라=دلائل.edition.resolve();ترتیبات=json.loads((나라/'native.json').read_text());نام_جدول=ترتیبات['identifiers'];عکس_ڈالنا_روٹ=나라/ترتیبات['source']/ترتیبات['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        میزبان=나라/'host/qemu'
        if میزبان.is_file():os.environ['QEMU_AARCH64']=str(میزبان)
    ٹولز=عکس_ڈالنا_روٹ/Path(ترتیبات.get('runner','ٹولز/نفاذ_کریں_حکم.py')).parent
    sys.path.insert(0,str(ٹولز))
    def پڑھیں(نام):
        راستہ_2=ٹولز/(نام_جدول.get(نام,نام)+'.py');جاب_قدر=importlib.util.spec_from_file_location('test_'+نام,str(راستہ_2));ماڈیول_قدر=importlib.util.module_from_spec(جاب_قدر);جاب_قدر.loader.exec_module(ماڈیول_قدر);return ماڈیول_قدر
    실행모듈=پڑھیں('نفاذ_کریں_حکم');نیٹ_ورک_ماڈیول=پڑھیں('نیٹ_ورک_برج');حکم=getattr(실행모듈,نام_جدول.get('حکم','حکم'));برج_ٹائپ_کریں=getattr(نیٹ_ورک_ماڈیول,نام_جدول.get('نیٹ_ورک_برج','نیٹ_ورک_برج'))
    عرف_قدر=ترتیبات.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_پتا','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'مدد_دکھانا'})
    sys.path.insert(0,str(عکس_ڈالنا_روٹ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(عکس_ڈالنا_روٹ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    اخراج_کا_مقام=دلائل.output or عکس_ڈالنا_روٹ/'build/verification/system-tools';اخراج_کا_مقام.mkdir(parents=True,exist_ok=True)
    رپورٹ_قدر={'passed':False,'country':ترتیبات.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    لاگ_صف=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        کنٹرول_راہ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as تلاش_قدر:تلاش_قدر.bind(('127.0.0.1',0));دہانہ_نمبر=تلاش_قدر.getsockname()[1]
            if not 50000<=دہانہ_نمبر<=50007:break
        with برج_ٹائپ_کریں(دہانہ_نمبر,کیپچر_کریں=True,مہمان_پتہ=ipTestText('10.0.2.20'),میزبان_پتہ='127.0.0.2') as برج_قدر:
            عمل_قدر=subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(کنٹرول_راہ)]+برج_قدر.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            انتخاب_کریں_شے=selectors.DefaultSelector();انتخاب_کریں_شے.register(عمل_قدر.stdout,selectors.EVENT_READ)
            def 받기(دکھانا_قدر,چلائیں=0,제한=45):
                끝=time.monotonic()+제한
                while دکھانا_قدر not in لاگ_صف[چلائیں:]:
                    if time.monotonic()>끝 or عمل_قدر.poll() is not None:raise AssertionError('Missing '+repr(دکھانا_قدر)+'\n'+لاگ_صف[چلائیں:].decode('utf-8','replace'))
                    for کلید_قدر,_ in انتخاب_کریں_شے.select(.1):
                        کوائف=کلید_قدر.fileobj.read(65536)
                        if کوائف:لاگ_صف.extend(کوائف)
                return لاگ_صف[چلائیں:].decode('utf-8','replace').replace('\r\n','\n')
            def بھیجیں(کوائف):عمل_قدر.stdin.write(کوائف);عمل_قدر.stdin.flush()
            def شیل(متن):
                متن=ipTestText(متن)
                print(رپورٹ_قدر['country'],متن,flush=True);차례[0]+=1;دکھانا_قدر='__SYSTEM_DONE_'+str(차례[0])+'__';چلائیں=len(لاگ_صف)
                بھیجیں((متن+'; echo; echo '+دکھانا_قدر+'\n').encode())
                끝표시=('\r\n'+دکھانا_قدر+'\r\n').encode();받기(끝표시,چلائیں)
                اختتام_پوزیشن_ٹھیک_کریں=لاگ_صف.index(끝표시,چلائیں)+len(끝표시)
                받기(b'jkoros-native> ',اختتام_پوزیشن_ٹھیک_کریں)
                return لاگ_صف[چلائیں:].decode('utf-8','replace').replace('\r\n','\n')
            def تصدیق_کریں(متن,*값들):
                جواب_دیں=شیل(متن)
                for قدر in 값들:assert ipTestText(قدر) in جواب_دیں,(متن,قدر,جواب_دیں)
                return جواب_دیں
            try:
                받기(b'jkoros-native> ')
                if not دلائل.poweroff_only:
                    مدد_قدر=تصدیق_کریں('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in عرف_قدر.values():assert 별칭 in مدد_قدر,(별칭,مدد_قدر)
                    تصدیق_کریں(عرف_قدر['help']+' system','Network / system')
                    تصدیق_کریں('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    تصدیق_کریں(عرف_قدر['ipconfig'],'inet 10.0.2.15');تصدیق_کریں('ip addr show','sl0: UP');تصدیق_کریں('ifconfig','sl0: UP')
                    for بے_جواز_سیٹنگز in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        غلطی=تصدیق_کریں('ipconfig set '+بے_جواز_سیٹنگز+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in غلطی,غلطی
                        تصدیق_کریں('ipconfig','inet 10.0.2.15')
                    تصدیق_کریں('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    تصدیق_کریں(عرف_قدر['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصدیق_کریں('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    تصدیق_کریں('ip link set dev sl0 down','sl0: DOWN');تصدیق_کریں('ping -c 1 10.0.2.2; echo STATUS=$?','غلطی -100','STATUS=1')
                    تصدیق_کریں('ipconfig up','sl0: UP')
                    تصدیق_کریں(عرف_قدر['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    تصدیق_کریں('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تصدیق_کریں('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');تصدیق_کریں(عرف_قدر['route'],'10.0.2.2 sl0')
                    تصدیق_کریں('ftpd start','FTP listening')
                    تصدیق_کریں(عرف_قدر['netstat'],'10.0.2.20:21','LISTEN');تصدیق_کریں('ss','LISTEN')
                    تصدیق_کریں('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','غلطی -16')
                    with ftplib.FTP() as کلائنٹ_قدر:
                        کلائنٹ_قدر.connect('127.0.0.2',دہانہ_نمبر,timeout=20);کلائنٹ_قدر.login();کوائف=b'Network address was changed in the guest.\n'
                        کلائنٹ_قدر.storbinary('STOR net-state.txt',io.BytesIO(کوائف));받은자료=bytearray();کلائنٹ_قدر.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==کوائف;کلائنٹ_قدر.delete('net-state.txt')
                    تصدیق_کریں('ftpd stop','FTP stopped');تصدیق_کریں('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    رپورٹ_قدر['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(متن):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',متن);assert 찾음,متن;return tuple(map(int,찾음.groups()))
                    전=저장값(تصدیق_کریں('df','RAM only'));تصدیق_کریں('echo disk-proof > sys-state.txt');후=저장값(تصدیق_کریں(عرف_قدر['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    تصدیق_کریں('rm sys-state.txt');assert 저장값(شیل('df'))==전
                    میموری_قدر=تصدیق_کریں(عرف_قدر['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',میموری_قدر).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    تصدیق_کریں(عرف_قدر['ps'],'kernel/shell');تصدیق_کریں(عرف_قدر['uptime'],'seconds')
                    حالت_معلومات=تصدیق_کریں(عرف_قدر['top']+' -n 2','kernel/shell');assert حالت_معلومات.count('PID SLOT STATE')==2,حالت_معلومات
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    تصدیق_کریں('terminal','TERMINAL READY');چلائیں=len(لاگ_صف);بھیجیں(b'vi process.txt\n');받기(b'NORMAL',چلائیں)
                    چلائیں=len(لاگ_صف);بھیجیں(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',چلائیں)
                    اندراج_فہرست=تصدیق_کریں('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',اندراج_فہرست);assert 찾음 and int(찾음.group(2))>0,اندراج_فہرست
                    تصدیق_کریں('free','EL0 mapped KiB: '+찾음.group(2))
                    چلائیں=len(لاگ_صف);بھیجیں(b'top\n');받기(b'PID SLOT STATE',چلائیں);بھیجیں(b'q');받기(b'jkoros-native> ',چلائیں)
                    # Test a multibyte prefix through the real shell completion path.
                    if عرف_قدر['df']!='df':
                        چلائیں=len(لاگ_صف);بھیجیں((عرف_قدر['df'][:-1]+'\t\n').encode());받기(b'RAM only',چلائیں);받기(b'jkoros-native> ',چلائیں)
                    رپورٹ_قدر['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as کنٹرول_قدر:
                    کنٹرول_قدر.settimeout(15);کنٹرول_قدر.connect(str(کنٹرول_راہ));بہاؤ_قدر=کنٹرول_قدر.makefile('rwb');json.loads(بہاؤ_قدر.readline());بہاؤ_قدر.write(b'{"execute":"qmp_capabilities"}\n');بہاؤ_قدر.flush()
                    while 'return' not in json.loads(بہاؤ_قدر.readline()):pass
                    بھیجیں((('poweroff' if دلائل.poweroff_only else عرف_قدر['poweroff'])+'\n').encode())
                    while True:
                        واقعہ=json.loads(بہاؤ_قدر.readline())
                        if واقعہ.get('event')=='SHUTDOWN':break
                    assert واقعہ['data']['guest'] and واقعہ['data']['reason']=='guest-shutdown',واقعہ
                    assert عمل_قدر.wait(timeout=15)==0
                    رپورٹ_قدر['shutdown']=واقعہ;رپورٹ_قدر['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                رپورٹ_قدر['network_trace']=برج_قدر.ٹریس_لاگ
                assert دلائل.poweroff_only or any(اندراج_قدر['protocol']==1 and اندراج_قدر['direction']=='from_guest' for اندراج_قدر in برج_قدر.ٹریس_لاگ)
                رپورٹ_قدر['passed']=True
            finally:
                if عمل_قدر.poll() is None:os.killpg(عمل_قدر.pid,signal.SIGTERM)
                try:عمل_قدر.wait(timeout=10)
                except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
                انتخاب_کریں_شے.close();(اخراج_کا_مقام/'serial.log').write_bytes(لاگ_صف);(اخراج_کا_مقام/'report.json').write_text(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({کلید_قدر:قدر for کلید_قدر,قدر in رپورٹ_قدر.items() if کلید_قدر!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':چلائیں()
