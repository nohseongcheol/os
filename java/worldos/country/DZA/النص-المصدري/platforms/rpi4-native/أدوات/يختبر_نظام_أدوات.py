#!/usr/bin/env python3
"""الفعلي_بيانات ذاتي 커널의 IP/ICMP, حالة_قيمة يستعلم_قيمة, 현지어 أمر, 게스트 خروج_تطبيق التحقق_من_صحة."""
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


def تشغيل():
    المحلل_48ee4b1b=argparse.ArgumentParser();المحلل_48ee4b1b.add_argument('--edition',type=Path);المحلل_48ee4b1b.add_argument('--output',type=Path);المحلل_48ee4b1b.add_argument('--poweroff-only',action='store_true');وسائط=المحلل_48ee4b1b.parse_args()
    يعرض_جذر=Path(__file__).resolve().parents[1];إعدادات={};اسم_جدول={}
    if وسائط.edition:
        나라=وسائط.edition.resolve();إعدادات=json.loads((나라/'native.json').read_text());اسم_جدول=إعدادات['identifiers'];يعرض_جذر=나라/إعدادات['source']/إعدادات['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        مضيف=나라/'host/qemu'
        if مضيف.is_file():os.environ['QEMU_AARCH64']=str(مضيف)
    أدوات=يعرض_جذر/Path(إعدادات.get('runner','أدوات/ينفذ_أمر.py')).parent
    sys.path.insert(0,str(أدوات))
    def قراءة(اسم):
        مسار=أدوات/(اسم_جدول.get(اسم,اسم)+'.py');قيمة_العقد=importlib.util.spec_from_file_location('test_'+اسم,str(مسار));وحدة_نمطية_قيمة=importlib.util.module_from_spec(قيمة_العقد);قيمة_العقد.loader.exec_module(وحدة_نمطية_قيمة);return وحدة_نمطية_قيمة
    실행모듈=قراءة('ينفذ_أمر');شبكة_وحدة_نمطية=قراءة('جسر_3de4fe3a');أمر=getattr(실행모듈,اسم_جدول.get('أمر','أمر'));جسر_نوع=getattr(شبكة_وحدة_نمطية,اسم_جدول.get('جسر_3de4fe3a','جسر_3de4fe3a'))
    اختصار_قيمة_0a38607b=إعدادات.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'عنوان_IP','ping':'يختبر_رد','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'عرض_المساعدة'})
    sys.path.insert(0,str(يعرض_جذر/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(يعرض_جذر);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    مخرجات=وسائط.output or يعرض_جذر/'build/verification/system-tools';مخرجات.mkdir(parents=True,exist_ok=True)
    إبلاغ_قيمة={'passed':False,'country':إعدادات.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    سجل_سجل=bytearray();تسلسل_قيمة=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        تحكم_مسار=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as بحث_قيمة:بحث_قيمة.bind(('127.0.0.1',0));رقم_المنفذ=بحث_قيمة.getsockname()[1]
            if not 50000<=رقم_المنفذ<=50007:break
        with جسر_نوع(رقم_المنفذ,يسجل=True,ضيف_عنوان=ipTestText('10.0.2.20'),مضيف_عنوان='127.0.0.2') as جسر_قيمة:
            عملية_قيمة=subprocess.Popen(أمر()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(تحكم_مسار)]+جسر_قيمة.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            يختار_عنصر=selectors.DefaultSelector();يختار_عنصر.register(عملية_قيمة.stdout,selectors.EVENT_READ)
            def يستلم(عرض_قيمة_487749b8,تشغيل=0,제한=45):
                끝=time.monotonic()+제한
                while عرض_قيمة_487749b8 not in سجل_سجل[تشغيل:]:
                    if time.monotonic()>끝 or عملية_قيمة.poll() is not None:raise AssertionError('Missing '+repr(عرض_قيمة_487749b8)+'\n'+سجل_سجل[تشغيل:].decode('utf-8','replace'))
                    for مفتاح_قيمة,_ in يختار_عنصر.select(.1):
                        بيانات=مفتاح_قيمة.fileobj.read(65536)
                        if بيانات:سجل_سجل.extend(بيانات)
                return سجل_سجل[تشغيل:].decode('utf-8','replace').replace('\r\n','\n')
            def يرسل(بيانات):عملية_قيمة.stdin.write(بيانات);عملية_قيمة.stdin.flush()
            def 셸(نص):
                نص=ipTestText(نص)
                print(إبلاغ_قيمة['country'],نص,flush=True);تسلسل_قيمة[0]+=1;عرض_قيمة_487749b8='__SYSTEM_DONE_'+str(تسلسل_قيمة[0])+'__';تشغيل=len(سجل_سجل)
                يرسل((نص+'; echo; echo '+عرض_قيمة_487749b8+'\n').encode())
                إنهاء_مكالمة_علامة=('\r\n'+عرض_قيمة_487749b8+'\r\n').encode();يستلم(إنهاء_مكالمة_علامة,تشغيل)
                إنهاء_مكالمة_منصب=سجل_سجل.index(إنهاء_مكالمة_علامة,تشغيل)+len(إنهاء_مكالمة_علامة)
                يستلم(b'jkoros-native> ',إنهاء_مكالمة_منصب)
                return سجل_سجل[تشغيل:].decode('utf-8','replace').replace('\r\n','\n')
            def يتحقق(نص,*값들):
                رد=셸(نص)
                for قيمة in 값들:assert ipTestText(قيمة) in رد,(نص,قيمة,رد)
                return رد
            try:
                يستلم(b'jkoros-native> ')
                if not وسائط.poweroff_only:
                    التعليمات_قيمة=يتحقق('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in اختصار_قيمة_0a38607b.values():assert 별칭 in التعليمات_قيمة,(별칭,التعليمات_قيمة)
                    يتحقق(اختصار_قيمة_0a38607b['help']+' system','Network / system')
                    يتحقق('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    يتحقق(اختصار_قيمة_0a38607b['ipconfig'],'inet 10.0.2.15');يتحقق('ip addr show','sl0: UP');يتحقق('ifconfig','sl0: UP')
                    for غير_صالح_إعدادات in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        خطأ=يتحقق('ipconfig set '+غير_صالح_إعدادات+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in خطأ,خطأ
                        يتحقق('ipconfig','inet 10.0.2.15')
                    يتحقق('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    يتحقق(اختصار_قيمة_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    يتحقق('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    يتحقق('ip link set dev sl0 down','sl0: DOWN');يتحقق('ping -c 1 10.0.2.2; echo STATUS=$?','خطأ -100','STATUS=1')
                    يتحقق('ipconfig up','sl0: UP')
                    يتحقق(اختصار_قيمة_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    يتحقق('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    يتحقق('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');يتحقق(اختصار_قيمة_0a38607b['route'],'10.0.2.2 sl0')
                    يتحقق('ftpd start','FTP listening')
                    يتحقق(اختصار_قيمة_0a38607b['netstat'],'10.0.2.20:21','LISTEN');يتحقق('ss','LISTEN')
                    يتحقق('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','خطأ -16')
                    with ftplib.FTP() as عميل_قيمة:
                        عميل_قيمة.connect('127.0.0.2',رقم_المنفذ,timeout=20);عميل_قيمة.login();بيانات=b'Network address was changed in the guest.\n'
                        عميل_قيمة.storbinary('STOR net-state.txt',io.BytesIO(بيانات));받은자료=bytearray();عميل_قيمة.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==بيانات;عميل_قيمة.delete('net-state.txt')
                    يتحقق('ftpd stop','FTP stopped');يتحقق('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    إبلاغ_قيمة['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(نص):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',نص);assert 찾음,نص;return tuple(map(int,찾음.groups()))
                    전=저장값(يتحقق('df','RAM only'));يتحقق('echo disk-proof > sys-state.txt');후=저장값(يتحقق(اختصار_قيمة_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    يتحقق('rm sys-state.txt');assert 저장값(셸('df'))==전
                    ذاكرة_قيمة=يتحقق(اختصار_قيمة_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');كمية_قيمة=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ذاكرة_قيمة).groups()));assert 0<كمية_قيمة[1]<=كمية_قيمة[0] and كمية_قيمة[1]+كمية_قيمة[2]==كمية_قيمة[0]
                    يتحقق(اختصار_قيمة_0a38607b['ps'],'kernel/shell');يتحقق(اختصار_قيمة_0a38607b['uptime'],'seconds')
                    توفر_معلومات=يتحقق(اختصار_قيمة_0a38607b['top']+' -n 2','kernel/shell');assert توفر_معلومات.count('PID SLOT STATE')==2,توفر_معلومات
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    يتحقق('terminal','TERMINAL READY');تشغيل=len(سجل_سجل);يرسل(b'vi process.txt\n');يستلم(b'NORMAL',تشغيل)
                    تشغيل=len(سجل_سجل);يرسل(bytes([30,2,1,0,0,0,0]));يستلم(b'jkoros-native> ',تشغيل)
                    إدخال_قائمة_f07b3200=يتحقق('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',إدخال_قائمة_f07b3200);assert 찾음 and int(찾음.group(2))>0,إدخال_قائمة_f07b3200
                    يتحقق('free','EL0 mapped KiB: '+찾음.group(2))
                    تشغيل=len(سجل_سجل);يرسل(b'top\n');يستلم(b'PID SLOT STATE',تشغيل);يرسل(b'q');يستلم(b'jkoros-native> ',تشغيل)
                    # Test a multibyte prefix through the real shell completion path.
                    if اختصار_قيمة_0a38607b['df']!='df':
                        تشغيل=len(سجل_سجل);يرسل((اختصار_قيمة_0a38607b['df'][:-1]+'\t\n').encode());يستلم(b'RAM only',تشغيل);يستلم(b'jkoros-native> ',تشغيل)
                    إبلاغ_قيمة['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as تحكم_قيمة:
                    تحكم_قيمة.settimeout(15);تحكم_قيمة.connect(str(تحكم_مسار));بث_قيمة=تحكم_قيمة.makefile('rwb');json.loads(بث_قيمة.readline());بث_قيمة.write(b'{"execute":"qmp_capabilities"}\n');بث_قيمة.flush()
                    while 'return' not in json.loads(بث_قيمة.readline()):pass
                    يرسل((('poweroff' if وسائط.poweroff_only else اختصار_قيمة_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        حدث=json.loads(بث_قيمة.readline())
                        if حدث.get('event')=='SHUTDOWN':break
                    assert حدث['data']['guest'] and حدث['data']['reason']=='guest-shutdown',حدث
                    assert عملية_قيمة.wait(timeout=15)==0
                    إبلاغ_قيمة['shutdown']=حدث;إبلاغ_قيمة['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                إبلاغ_قيمة['network_trace']=جسر_قيمة.سجل_التتبّع
                assert وسائط.poweroff_only or any(إدخال_قيمة_962f286b['protocol']==1 and إدخال_قيمة_962f286b['direction']=='from_guest' for إدخال_قيمة_962f286b in جسر_قيمة.سجل_التتبّع)
                إبلاغ_قيمة['passed']=True
            finally:
                if عملية_قيمة.poll() is None:os.killpg(عملية_قيمة.pid,signal.SIGTERM)
                try:عملية_قيمة.wait(timeout=10)
                except subprocess.TimeoutExpired:عملية_قيمة.kill();عملية_قيمة.wait()
                يختار_عنصر.close();(مخرجات/'serial.log').write_bytes(سجل_سجل);(مخرجات/'report.json').write_text(json.dumps(إبلاغ_قيمة,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({مفتاح_قيمة:قيمة for مفتاح_قيمة,قيمة in إبلاغ_قيمة.items() if مفتاح_قيمة!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':تشغيل()
