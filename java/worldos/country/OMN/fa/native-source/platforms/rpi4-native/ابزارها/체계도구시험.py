#!/usr/bin/env python3
"""واقعی_داده_ها بومی 커널의 IP/ICMP, وضعیت_مقدار جستار_مقدار, 현지어 فرمان, 게스트 خروج_برنامه ارزیابی_کردن."""
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


def اجرا_2():
    مفسر_48ee4b1b=argparse.ArgumentParser();مفسر_48ee4b1b.add_argument('--edition',type=Path);مفسر_48ee4b1b.add_argument('--output',type=Path);مفسر_48ee4b1b.add_argument('--poweroff-only',action='store_true');نشانوندها=مفسر_48ee4b1b.parse_args()
    نمایش_دادن_جذر=Path(__file__).resolve().parents[1];تنظیمات={};نام_جدول={}
    if نشانوندها.edition:
        나라=نشانوندها.edition.resolve();تنظیمات=json.loads((나라/'native.json').read_text());نام_جدول=تنظیمات['identifiers'];نمایش_دادن_جذر=나라/تنظیمات['source']/تنظیمات['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        میزبان=나라/'host/qemu'
        if میزبان.is_file():os.environ['QEMU_AARCH64']=str(میزبان)
    ابزارها=نمایش_دادن_جذر/Path(تنظیمات.get('runner','ابزارها/اجرا_فرمان.py')).parent
    sys.path.insert(0,str(ابزارها))
    def خواندن(نام):
        مسیر=ابزارها/(نام_جدول.get(نام,نام)+'.py');شغل_مقدار=importlib.util.spec_from_file_location('test_'+نام,str(مسیر));مدول_مقدار=importlib.util.module_from_spec(شغل_مقدار);شغل_مقدار.loader.exec_module(مدول_مقدار);return مدول_مقدار
    실행모듈=خواندن('اجرا_فرمان');شبکه_مدول=خواندن('شبکه_پل');فرمان=getattr(실행모듈,نام_جدول.get('فرمان','فرمان'));پل_تایپ_کردن=getattr(شبکه_مدول,نام_جدول.get('شبکه_پل','شبکه_پل'))
    میانبر_مقدار_0a38607b=تنظیمات.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'آدرس_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'نمایش_راهنما'})
    sys.path.insert(0,str(نمایش_دادن_جذر/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(نمایش_دادن_جذر);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    خروجی=نشانوندها.output or نمایش_دادن_جذر/'build/verification/system-tools';خروجی.mkdir(parents=True,exist_ok=True)
    گزارش_مقدار={'passed':False,'country':تنظیمات.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    واقعه_نگار_ردیف=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        کنترل_مسیر=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as جستجو_مقدار:جستجو_مقدار.bind(('127.0.0.1',0));شماره_درگاه=جستجو_مقدار.getsockname()[1]
            if not 50000<=شماره_درگاه<=50007:break
        with پل_تایپ_کردن(شماره_درگاه,ضبط_کردن=True,مهمان_آدرس=ipTestText('10.0.2.20'),میزبان_آدرس='127.0.0.2') as پل_مقدار:
            فرآیند_مقدار=subprocess.Popen(فرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(کنترل_مسیر)]+پل_مقدار.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            انتخاب_کردن_مورد=selectors.DefaultSelector();انتخاب_کردن_مورد.register(فرآیند_مقدار.stdout,selectors.EVENT_READ)
            def 받기(نمایش_مقدار,اجرا_2=0,제한=45):
                끝=time.monotonic()+제한
                while نمایش_مقدار not in واقعه_نگار_ردیف[اجرا_2:]:
                    if time.monotonic()>끝 or فرآیند_مقدار.poll() is not None:raise AssertionError('Missing '+repr(نمایش_مقدار)+'\n'+واقعه_نگار_ردیف[اجرا_2:].decode('utf-8','replace'))
                    for کلید_مقدار,_ in انتخاب_کردن_مورد.select(.1):
                        داده_ها=کلید_مقدار.fileobj.read(65536)
                        if داده_ها:واقعه_نگار_ردیف.extend(داده_ها)
                return واقعه_نگار_ردیف[اجرا_2:].decode('utf-8','replace').replace('\r\n','\n')
            def ارسال(داده_ها):فرآیند_مقدار.stdin.write(داده_ها);فرآیند_مقدار.stdin.flush()
            def واسط(متن):
                متن=ipTestText(متن)
                print(گزارش_مقدار['country'],متن,flush=True);차례[0]+=1;نمایش_مقدار='__SYSTEM_DONE_'+str(차례[0])+'__';اجرا_2=len(واقعه_نگار_ردیف)
                ارسال((متن+'; echo; echo '+نمایش_مقدار+'\n').encode())
                끝표시=('\r\n'+نمایش_مقدار+'\r\n').encode();받기(끝표시,اجرا_2)
                پایان_دادن_مرتب_کردن=واقعه_نگار_ردیف.index(끝표시,اجرا_2)+len(끝표시)
                받기(b'jkoros-native> ',پایان_دادن_مرتب_کردن)
                return واقعه_نگار_ردیف[اجرا_2:].decode('utf-8','replace').replace('\r\n','\n')
            def تأیید_صحت(متن,*값들):
                پاسخ_دادن=واسط(متن)
                for مقدار in 값들:assert ipTestText(مقدار) in پاسخ_دادن,(متن,مقدار,پاسخ_دادن)
                return پاسخ_دادن
            try:
                받기(b'jkoros-native> ')
                if not نشانوندها.poweroff_only:
                    راهنما_مقدار=تأیید_صحت('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in میانبر_مقدار_0a38607b.values():assert 별칭 in راهنما_مقدار,(별칭,راهنما_مقدار)
                    تأیید_صحت(میانبر_مقدار_0a38607b['help']+' system','Network / system')
                    تأیید_صحت('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    تأیید_صحت(میانبر_مقدار_0a38607b['ipconfig'],'inet 10.0.2.15');تأیید_صحت('ip addr show','sl0: UP');تأیید_صحت('ifconfig','sl0: UP')
                    for بی_اعتبار_تنظیمات in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        خطا=تأیید_صحت('ipconfig set '+بی_اعتبار_تنظیمات+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in خطا,خطا
                        تأیید_صحت('ipconfig','inet 10.0.2.15')
                    تأیید_صحت('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    تأیید_صحت(میانبر_مقدار_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تأیید_صحت('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    تأیید_صحت('ip link set dev sl0 down','sl0: DOWN');تأیید_صحت('ping -c 1 10.0.2.2; echo STATUS=$?','خطا -100','STATUS=1')
                    تأیید_صحت('ipconfig up','sl0: UP')
                    تأیید_صحت(میانبر_مقدار_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    تأیید_صحت('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    تأیید_صحت('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');تأیید_صحت(میانبر_مقدار_0a38607b['route'],'10.0.2.2 sl0')
                    تأیید_صحت('ftpd start','FTP listening')
                    تأیید_صحت(میانبر_مقدار_0a38607b['netstat'],'10.0.2.20:21','LISTEN');تأیید_صحت('ss','LISTEN')
                    تأیید_صحت('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','خطا -16')
                    with ftplib.FTP() as سرویس_گیرنده_مقدار:
                        سرویس_گیرنده_مقدار.connect('127.0.0.2',شماره_درگاه,timeout=20);سرویس_گیرنده_مقدار.login();داده_ها=b'Network address was changed in the guest.\n'
                        سرویس_گیرنده_مقدار.storbinary('STOR net-state.txt',io.BytesIO(داده_ها));받은자료=bytearray();سرویس_گیرنده_مقدار.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==داده_ها;سرویس_گیرنده_مقدار.delete('net-state.txt')
                    تأیید_صحت('ftpd stop','FTP stopped');تأیید_صحت('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    گزارش_مقدار['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(متن):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',متن);assert 찾음,متن;return tuple(map(int,찾음.groups()))
                    전=저장값(تأیید_صحت('df','RAM only'));تأیید_صحت('echo disk-proof > sys-state.txt');후=저장값(تأیید_صحت(میانبر_مقدار_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    تأیید_صحت('rm sys-state.txt');assert 저장값(واسط('df'))==전
                    حافظه_مقدار=تأیید_صحت(میانبر_مقدار_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',حافظه_مقدار).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    تأیید_صحت(میانبر_مقدار_0a38607b['ps'],'kernel/shell');تأیید_صحت(میانبر_مقدار_0a38607b['uptime'],'seconds')
                    وضعیت_اطلاعات=تأیید_صحت(میانبر_مقدار_0a38607b['top']+' -n 2','kernel/shell');assert وضعیت_اطلاعات.count('PID SLOT STATE')==2,وضعیت_اطلاعات
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    تأیید_صحت('terminal','TERMINAL READY');اجرا_2=len(واقعه_نگار_ردیف);ارسال(b'vi process.txt\n');받기(b'NORMAL',اجرا_2)
                    اجرا_2=len(واقعه_نگار_ردیف);ارسال(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',اجرا_2)
                    ورودی_لیست=تأیید_صحت('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ورودی_لیست);assert 찾음 and int(찾음.group(2))>0,ورودی_لیست
                    تأیید_صحت('free','EL0 mapped KiB: '+찾음.group(2))
                    اجرا_2=len(واقعه_نگار_ردیف);ارسال(b'top\n');받기(b'PID SLOT STATE',اجرا_2);ارسال(b'q');받기(b'jkoros-native> ',اجرا_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if میانبر_مقدار_0a38607b['df']!='df':
                        اجرا_2=len(واقعه_نگار_ردیف);ارسال((میانبر_مقدار_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',اجرا_2);받기(b'jkoros-native> ',اجرا_2)
                    گزارش_مقدار['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as کنترل_مقدار:
                    کنترل_مقدار.settimeout(15);کنترل_مقدار.connect(str(کنترل_مسیر));جریان_مقدار=کنترل_مقدار.makefile('rwb');json.loads(جریان_مقدار.readline());جریان_مقدار.write(b'{"execute":"qmp_capabilities"}\n');جریان_مقدار.flush()
                    while 'return' not in json.loads(جریان_مقدار.readline()):pass
                    ارسال((('poweroff' if نشانوندها.poweroff_only else میانبر_مقدار_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        رویداد=json.loads(جریان_مقدار.readline())
                        if رویداد.get('event')=='SHUTDOWN':break
                    assert رویداد['data']['guest'] and رویداد['data']['reason']=='guest-shutdown',رویداد
                    assert فرآیند_مقدار.wait(timeout=15)==0
                    گزارش_مقدار['shutdown']=رویداد;گزارش_مقدار['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                گزارش_مقدار['network_trace']=پل_مقدار.اثر_ماتریس_واقعه_نگار
                assert نشانوندها.poweroff_only or any(ورودی_مقدار['protocol']==1 and ورودی_مقدار['direction']=='from_guest' for ورودی_مقدار in پل_مقدار.اثر_ماتریس_واقعه_نگار)
                گزارش_مقدار['passed']=True
            finally:
                if فرآیند_مقدار.poll() is None:os.killpg(فرآیند_مقدار.pid,signal.SIGTERM)
                try:فرآیند_مقدار.wait(timeout=10)
                except subprocess.TimeoutExpired:فرآیند_مقدار.kill();فرآیند_مقدار.wait()
                انتخاب_کردن_مورد.close();(خروجی/'serial.log').write_bytes(واقعه_نگار_ردیف);(خروجی/'report.json').write_text(json.dumps(گزارش_مقدار,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({کلید_مقدار:مقدار for کلید_مقدار,مقدار in گزارش_مقدار.items() if کلید_مقدار!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':اجرا_2()
