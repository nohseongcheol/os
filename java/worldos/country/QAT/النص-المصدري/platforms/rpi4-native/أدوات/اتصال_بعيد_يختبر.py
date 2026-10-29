#!/usr/bin/env python3
"""الفعلي_بيانات OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from ينفذ_أمر import يعرض_جذر, أمر
from جسر_3de4fe3a import جسر_3de4fe3a


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--kernel', type=Path, default=يعرض_جذر / 'build/kernel8.img')
    المحلل_48ee4b1b.add_argument('--access', type=Path, default=يعرض_جذر / 'build/remote/access.json')
    المحلل_48ee4b1b.add_argument('--output', type=Path, default=يعرض_جذر / 'build/verification/native-remote')
    وسائط = المحلل_48ee4b1b.parse_args()
    مخرجات = وسائط.output
    مخرجات.mkdir(parents=True, exist_ok=True)
    إعدادات = json.loads(وسائط.access.read_text())
    إبلاغ_قيمة = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(وسائط.kernel.read_bytes()).hexdigest(), 'checks': []}
    def فارغ_منفذ():
        with socket.socket() as اتصال:
            اتصال.bind(('127.0.0.5', 0))
            return اتصال.getsockname()[1]
    셸포트, 화면포트, منفذ_الملف = فارغ_منفذ(), فارغ_منفذ(), فارغ_منفذ()
    سجل_سجل = bytearray()
    عملية_قيمة = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, جسر_3de4fe3a(منفذ_الملف,
                ['tcp:{}:22'.format(셸포트), 'tcp:{}:5900'.format(화면포트)], مضيف_عنوان='127.0.0.5') as جسر_قيمة:
            실행인수 = أمر()
            실행인수[실행인수.index('-kernel') + 1] = str(وسائط.kernel.resolve())
            عملية_قيمة = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + جسر_قيمة.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    بيانات = عملية_قيمة.stdout.read(4096)
                    if not بيانات: break
                    سجل_سجل.extend(بيانات)
            محادثة_قيمة = threading.Thread(target=수집, daemon=True)
            محادثة_قيمة.start()
            def حالة_انتظار(الكلمات_نص, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while الكلمات_نص not in سجل_سجل[처음:]:
                    if time.monotonic()>끝 or عملية_قيمة.poll() is not None:
                        raise AssertionError('Missing '+repr(الكلمات_نص)+'\n'+سجل_سجل[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            حالة_انتظار(b'jkoros-native> ')
            مساعد_قيمة = Path(임시)/'askpass'
            مساعد_قيمة.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            مساعد_قيمة.chmod(0o700)
            بيئة_التشغيل = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(مساعد_قيمة), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(رمز_الوصول_قيمة, تعليمة_قيمة, إلحاق_إدخال=()):
                بيئة_التشغيل['JKOROS_TEST_PASSWORD']=رمز_الوصول_قيمة
                وسائط=['ssh','-v']+list(إلحاق_إدخال)+['-p',str(셸포트),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',تعليمة_قيمة]
                نتيجة=subprocess.run(وسائط,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=بيئة_التشغيل,start_new_session=True,timeout=50)
                return نتيجة
            نتيجة=보안셸('!' + إعدادات['ssh_password'], 'echo SHOULD_NOT_RUN')
            (مخرجات/'ssh-rejected.log').write_bytes(نتيجة.stderr)
            assert نتيجة.returncode!=0 and b'Permission denied' in نتيجة.stderr and b'SHOULD_NOT_RUN' not in سجل_سجل, نتيجة.stderr
            إبلاغ_قيمة['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            نتيجة=보안셸(إعدادات['ssh_password'], 'echo SSH_NATIVE_PASS')
            (مخرجات/'ssh.log').write_bytes(نتيجة.stderr)
            (مخرجات/'ssh-output.txt').write_bytes(نتيجة.stdout)
            assert نتيجة.returncode==0 and b'SSH_NATIVE_PASS' in نتيجة.stdout, (نتيجة.returncode,نتيجة.stdout,نتيجة.stderr)
            إبلاغ_قيمة['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in نتيجة.stderr, نتيجة.stderr
            إبلاغ_قيمة['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            نتيجة=보안셸(إعدادات['ssh_password'], 'cd /example/java; java مثالطباعة; cd /')
            assert نتيجة.returncode==0 and 'JAVA مخرجات: 안녕하세요 😀'.encode() in نتيجة.stdout,نتيجة.stdout
            إبلاغ_قيمة['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            نتيجة=보안셸(إعدادات['ssh_password'], 'missing_remote_command')
            assert نتيجة.returncode==127,نتيجة.returncode
            إبلاغ_قيمة['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            نتيجة=보안셸(إعدادات['ssh_password'], 'cat /example/java/مثالنافذة.java', ('-o', 'RekeyLimit=1K'))
            (مخرجات/'ssh-rekey.log').write_bytes(نتيجة.stderr)
            assert نتيجة.returncode==0 and 'class مثالنافذة'.encode() in نتيجة.stdout, (نتيجة.returncode,نتيجة.stdout,نتيجة.stderr)
            assert نتيجة.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, نتيجة.stderr
            إبلاغ_قيمة['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(셸포트),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            تفاعلي_جلسة=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=بيئة_التشغيل,start_new_session=True,bufsize=0)
            نسخة_مكتوبة=bytearray();تحديد_قيمة=selectors.DefaultSelector();تحديد_قيمة.register(تفاعلي_جلسة.stdout,selectors.EVENT_READ)
            def يقرأ_تفاعلي(عرض_قيمة_487749b8):
                موعد_نهائي_قيمة=time.monotonic()+30
                while عرض_قيمة_487749b8 not in نسخة_مكتوبة:
                    if time.monotonic()>موعد_نهائي_قيمة or تفاعلي_جلسة.poll() is not None:raise AssertionError('SSH interactive missing '+repr(عرض_قيمة_487749b8)+' '+repr(bytes(نسخة_مكتوبة)))
                    for إدخال_قيمة_962f286b,_ in تحديد_قيمة.select(.1):
                        조각=إدخال_قيمة_962f286b.fileobj.read(4096)
                        if 조각:نسخة_مكتوبة.extend(조각)
            try:
                يقرأ_تفاعلي(b'shared native console')
                تفاعلي_جلسة.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');تفاعلي_جلسة.stdin.flush();يقرأ_تفاعلي(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                تفاعلي_جلسة.stdin.write(b'\x04');تفاعلي_جلسة.stdin.flush();나머지,خطأ=تفاعلي_جلسة.communicate(timeout=15)
                assert تفاعلي_جلسة.returncode==0 and b'PTY allocation request failed' not in خطأ,(تفاعلي_جلسة.returncode,خطأ)
                (مخرجات/'ssh-interactive.txt').write_bytes(نسخة_مكتوبة+나머지)
            finally:
                تحديد_قيمة.close()
                if تفاعلي_جلسة.poll() is None:تفاعلي_جلسة.kill();تفاعلي_جلسة.wait()
            إبلاغ_قيمة['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(اتصال, رقم):
                بيانات=bytearray()
                while len(بيانات)<رقم:
                    مجموعة_قيمة=اتصال.recv(رقم-len(بيانات))
                    if not مجموعة_قيمة: raise AssertionError('RFB EOF')
                    بيانات.extend(مجموعة_قيمة)
                return bytes(بيانات)
            def 화면인증(رمز_الوصول_قيمة):
                اتصال=socket.create_connection(('127.0.0.5',화면포트),10);اتصال.settimeout(30)
                assert 정확히(اتصال,12)==b'RFB 003.008\n'
                اتصال.sendall(b'RFB 003.008\n');assert 정확히(اتصال,2)==b'\x01\x02'
                اتصال.sendall(b'\x02');تحدي_قيمة=정확히(اتصال,16)
                إدخال_رمز_الوصول=رمز_الوصول_قيمة.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(رقم)[::-1],2) for رقم in إدخال_رمز_الوصول)
                اتصال.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(تحدي_قيمة))
                حالة_قيمة=struct.unpack('!I',정확히(اتصال,4))[0]
                return اتصال,حالة_قيمة
            غير_صالح_رمز_الوصول='!' if not إعدادات['vnc_password'].startswith('!') else '?'
            اتصال,حالة_قيمة=화면인증(غير_صالح_رمز_الوصول);assert حالة_قيمة==1;اتصال.close();time.sleep(.6)
            إبلاغ_قيمة['checks'].append('VNC incorrect password rejected')
            اتصال,حالة_قيمة=화면인증(إعدادات['vnc_password']);assert حالة_قيمة==0
            with اتصال:
                اتصال.sendall(b'\x01');حالة_أولية=정확히(اتصال,24);너비,ارتفاع_قيمة=struct.unpack('!HH',حالة_أولية[:4]);اسم=정확히(اتصال,struct.unpack('!I',حالة_أولية[20:24])[0])
                assert (너비,ارتفاع_قيمة)==(640,480) and b'jkoros native'==اسم
                def 화면(زيادة_خطوة=0):
                    اتصال.sendall(struct.pack('!BBHHHH',3,زيادة_خطوة,0,0,너비,ارتفاع_قيمة));رأس_قيمة=정확히(اتصال,4);رقم=struct.unpack('!H',رأس_قيمة[2:])[0];إجمالي_قيمة=0
                    رسم_قيمة=bytearray(너비*ارتفاع_قيمة*4)
                    for _ in range(رقم):
                        الإحداثي_س,الزر_Y_إحداثيات,영역너비,منطقة_ارتفاع,أسلوب_الوضع=struct.unpack('!HHHHi',정확히(اتصال,12));assert أسلوب_الوضع==0 and الإحداثي_س+영역너비<=너비 and الزر_Y_إحداثيات+منطقة_ارتفاع<=ارتفاع_قيمة
                        عنصر_صورة=정확히(اتصال,영역너비*منطقة_ارتفاع*4);إجمالي_قيمة+=len(عنصر_صورة)
                        for سطر in range(منطقة_ارتفاع):رسم_قيمة[((الزر_Y_إحداثيات+سطر)*너비+الإحداثي_س)*4:((الزر_Y_إحداثيات+سطر)*너비+الإحداثي_س+영역너비)*4]=عنصر_صورة[سطر*영역너비*4:(سطر+1)*영역너비*4]
                    if not زيادة_خطوة:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,ارتفاع_قيمة),bytes(رسم_قيمة),'raw','BGRX').save(str(مخرجات/'native-vnc.png'))
                    return رقم,إجمالي_قيمة
                رقم,إجمالي_قيمة=화면();assert رقم>0 and إجمالي_قيمة==너비*ارتفاع_قيمة*4
                إبلاغ_قيمة['checks'].append('Native framebuffer RFB full update {} bytes'.format(إجمالي_قيمة))
                رقم,إجمالي_قيمة=화면(1);assert إجمالي_قيمة<너비*ارتفاع_قيمة*4
                إبلاغ_قيمة['checks'].append('RFB incremental update')
                처음=len(سجل_سجل)
                for حرف_قيمة in 'echo VNC_NATIVE_PASS\r':
                    رمز=0xff0d if حرف_قيمة=='\r' else ord(حرف_قيمة)
                    اتصال.sendall(struct.pack('!BBHI',4,1,0,رمز));اتصال.sendall(struct.pack('!BBHI',4,0,0,رمز))
                حالة_انتظار(b'VNC_NATIVE_PASS',처음)
                إبلاغ_قيمة['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def مفتاح_كتابة(رمز,누름=1):اتصال.sendall(struct.pack('!BBHI',4,누름,0,رمز))
                처음=len(سجل_سجل)
                for حرف_قيمة in 'echo ':مفتاح_كتابة(ord(حرف_قيمة))
                مفتاح_كتابة(0xffc6)
                for حرف_قيمة in 'gksrmf':مفتاح_كتابة(ord(حرف_قيمة))
                مفتاح_كتابة(0xffc6);مفتاح_كتابة(0xff0d)
                حالة_انتظار('\r\n한글\r\n'.encode(),처음)
                إبلاغ_قيمة['checks'].append('Native VNC F9 two-set Hangul composition')
                اتصال.sendall(struct.pack('!BBHH',5,0,120,100))
                إبلاغ_قيمة['checks'].append('VNC pointer input accepted')
            عملية_قيمة.stdin.write(b'poweroff\n');عملية_قيمة.stdin.flush();عملية_قيمة.wait(timeout=15);assert عملية_قيمة.returncode==0
            إبلاغ_قيمة['passed']=True
    finally:
        if عملية_قيمة and عملية_قيمة.poll() is None:
            عملية_قيمة.terminate()
            try: عملية_قيمة.wait(timeout=5)
            except subprocess.TimeoutExpired: عملية_قيمة.kill();عملية_قيمة.wait()
        (مخرجات/'serial.log').write_bytes(سجل_سجل)
        (مخرجات/'report.json').write_text(json.dumps(إبلاغ_قيمة,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(إبلاغ_قيمة,ensure_ascii=False,indent=2))


if __name__=='__main__': تشغيل()
