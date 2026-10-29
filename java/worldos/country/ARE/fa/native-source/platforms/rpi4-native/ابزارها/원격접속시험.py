#!/usr/bin/env python3
"""واقعی_داده_ها OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from اجرا_فرمان import نمایش_دادن_جذر, فرمان
from شبکه_پل import شبکه_پل


def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--kernel', type=Path, default=نمایش_دادن_جذر / 'build/kernel8.img')
    مفسر_48ee4b1b.add_argument('--access', type=Path, default=نمایش_دادن_جذر / 'build/remote/access.json')
    مفسر_48ee4b1b.add_argument('--output', type=Path, default=نمایش_دادن_جذر / 'build/verification/native-remote')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    خروجی = نشانوندها.output
    خروجی.mkdir(parents=True, exist_ok=True)
    تنظیمات = json.loads(نشانوندها.access.read_text())
    گزارش_مقدار = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(نشانوندها.kernel.read_bytes()).hexdigest(), 'checks': []}
    def خالی_تبدیل():
        with socket.socket() as اتصال:
            اتصال.bind(('127.0.0.5', 0))
            return اتصال.getsockname()[1]
    واسط_تبدیل, 화면포트, فایل_تبدیل = خالی_تبدیل(), خالی_تبدیل(), خالی_تبدیل()
    واقعه_نگار_ردیف = bytearray()
    فرآیند_مقدار = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, شبکه_پل(فایل_تبدیل,
                ['tcp:{}:22'.format(واسط_تبدیل), 'tcp:{}:5900'.format(화면포트)], میزبان_آدرس='127.0.0.5') as پل_مقدار:
            실행인수 = فرمان()
            실행인수[실행인수.index('-kernel') + 1] = str(نشانوندها.kernel.resolve())
            فرآیند_مقدار = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + پل_مقدار.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    داده_ها = فرآیند_مقدار.stdout.read(4096)
                    if not داده_ها: break
                    واقعه_نگار_ردیف.extend(داده_ها)
            رشته_مقدار = threading.Thread(target=수집, daemon=True)
            رشته_مقدار.start()
            def منتظر_ماندن_وضعیت(کلمات_متن, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while کلمات_متن not in واقعه_نگار_ردیف[처음:]:
                    if time.monotonic()>끝 or فرآیند_مقدار.poll() is not None:
                        raise AssertionError('Missing '+repr(کلمات_متن)+'\n'+واقعه_نگار_ردیف[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            منتظر_ماندن_وضعیت(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ایمن_واسط(رمز_عبور_مقدار, دستورالعمل_مقدار, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=رمز_عبور_مقدار
                نشانوندها=['ssh','-v']+list(추가)+['-p',str(واسط_تبدیل),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',دستورالعمل_مقدار]
                سنجش=subprocess.run(نشانوندها,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return سنجش
            سنجش=ایمن_واسط('!' + تنظیمات['ssh_password'], 'echo SHOULD_NOT_RUN')
            (خروجی/'ssh-rejected.log').write_bytes(سنجش.stderr)
            assert سنجش.returncode!=0 and b'Permission denied' in سنجش.stderr and b'SHOULD_NOT_RUN' not in واقعه_نگار_ردیف, سنجش.stderr
            گزارش_مقدار['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            سنجش=ایمن_واسط(تنظیمات['ssh_password'], 'echo SSH_NATIVE_PASS')
            (خروجی/'ssh.log').write_bytes(سنجش.stderr)
            (خروجی/'ssh-output.txt').write_bytes(سنجش.stdout)
            assert سنجش.returncode==0 and b'SSH_NATIVE_PASS' in سنجش.stdout, (سنجش.returncode,سنجش.stdout,سنجش.stderr)
            گزارش_مقدار['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in سنجش.stderr, سنجش.stderr
            گزارش_مقدار['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            سنجش=ایمن_واسط(تنظیمات['ssh_password'], 'cd /example/java; java نمونهچاپ; cd /')
            assert سنجش.returncode==0 and 'JAVA خروجی: 안녕하세요 😀'.encode() in سنجش.stdout,سنجش.stdout
            گزارش_مقدار['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            سنجش=ایمن_واسط(تنظیمات['ssh_password'], 'missing_remote_command')
            assert سنجش.returncode==127,سنجش.returncode
            گزارش_مقدار['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            سنجش=ایمن_واسط(تنظیمات['ssh_password'], 'cat /example/java/نمونهپنجره.java', ('-o', 'RekeyLimit=1K'))
            (خروجی/'ssh-rekey.log').write_bytes(سنجش.stderr)
            assert سنجش.returncode==0 and 'class نمونهپنجره'.encode() in سنجش.stdout, (سنجش.returncode,سنجش.stdout,سنجش.stderr)
            assert سنجش.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, سنجش.stderr
            گزارش_مقدار['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(واسط_تبدیل),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            محاوره_ای_جلسه=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();مورد_انتخابی_مقدار=selectors.DefaultSelector();مورد_انتخابی_مقدار.register(محاوره_ای_جلسه.stdout,selectors.EVENT_READ)
            def 대화읽기(نمایش_مقدار):
                마감=time.monotonic()+30
                while نمایش_مقدار not in 대화기록:
                    if time.monotonic()>마감 or محاوره_ای_جلسه.poll() is not None:raise AssertionError('SSH interactive missing '+repr(نمایش_مقدار)+' '+repr(bytes(대화기록)))
                    for ورودی_مقدار,_ in مورد_انتخابی_مقدار.select(.1):
                        조각=ورودی_مقدار.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                محاوره_ای_جلسه.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');محاوره_ای_جلسه.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                محاوره_ای_جلسه.stdin.write(b'\x04');محاوره_ای_جلسه.stdin.flush();나머지,خطا=محاوره_ای_جلسه.communicate(timeout=15)
                assert محاوره_ای_جلسه.returncode==0 and b'PTY allocation request failed' not in خطا,(محاوره_ای_جلسه.returncode,خطا)
                (خروجی/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                مورد_انتخابی_مقدار.close()
                if محاوره_ای_جلسه.poll() is None:محاوره_ای_جلسه.kill();محاوره_ای_جلسه.wait()
            گزارش_مقدار['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(اتصال, 수):
                داده_ها=bytearray()
                while len(داده_ها)<수:
                    덩이=اتصال.recv(수-len(داده_ها))
                    if not 덩이: raise AssertionError('RFB EOF')
                    داده_ها.extend(덩이)
                return bytes(داده_ها)
            def 화면인증(رمز_عبور_مقدار):
                اتصال=socket.create_connection(('127.0.0.5',화면포트),10);اتصال.settimeout(30)
                assert 정확히(اتصال,12)==b'RFB 003.008\n'
                اتصال.sendall(b'RFB 003.008\n');assert 정확히(اتصال,2)==b'\x01\x02'
                اتصال.sendall(b'\x02');رقابت_مقدار=정확히(اتصال,16)
                입력암호=رمز_عبور_مقدار.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                اتصال.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(رقابت_مقدار))
                وضعیت_مقدار=struct.unpack('!I',정확히(اتصال,4))[0]
                return اتصال,وضعیت_مقدار
            بی_اعتبار_رمز_عبور='!' if not تنظیمات['vnc_password'].startswith('!') else '?'
            اتصال,وضعیت_مقدار=화면인증(بی_اعتبار_رمز_عبور);assert وضعیت_مقدار==1;اتصال.close();time.sleep(.6)
            گزارش_مقدار['checks'].append('VNC incorrect password rejected')
            اتصال,وضعیت_مقدار=화면인증(تنظیمات['vnc_password']);assert وضعیت_مقدار==0
            with اتصال:
                اتصال.sendall(b'\x01');초기=정확히(اتصال,24);너비,높이=struct.unpack('!HH',초기[:4]);نام=정확히(اتصال,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==نام
                def 화면(증분=0):
                    اتصال.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(اتصال,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    نقاشی_مقدار=bytearray(너비*높이*4)
                    for _ in range(수):
                        مختصات_x,دکمه_Y_مختصات,영역너비,영역높이,روش_حالت=struct.unpack('!HHHHi',정확히(اتصال,12));assert روش_حالت==0 and مختصات_x+영역너비<=너비 and دکمه_Y_مختصات+영역높이<=높이
                        پیکسل=정확히(اتصال,영역너비*영역높이*4);합계+=len(پیکسل)
                        for خط in range(영역높이):نقاشی_مقدار[((دکمه_Y_مختصات+خط)*너비+مختصات_x)*4:((دکمه_Y_مختصات+خط)*너비+مختصات_x+영역너비)*4]=پیکسل[خط*영역너비*4:(خط+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(نقاشی_مقدار),'raw','BGRX').save(str(خروجی/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                گزارش_مقدار['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                گزارش_مقدار['checks'].append('RFB incremental update')
                처음=len(واقعه_نگار_ردیف)
                for نویسه_مقدار in 'echo VNC_NATIVE_PASS\r':
                    نماد=0xff0d if نویسه_مقدار=='\r' else ord(نویسه_مقدار)
                    اتصال.sendall(struct.pack('!BBHI',4,1,0,نماد));اتصال.sendall(struct.pack('!BBHI',4,0,0,نماد))
                منتظر_ماندن_وضعیت(b'VNC_NATIVE_PASS',처음)
                گزارش_مقدار['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(نماد,فشار_دادن_مقدار=1):اتصال.sendall(struct.pack('!BBHI',4,فشار_دادن_مقدار,0,نماد))
                처음=len(واقعه_نگار_ردیف)
                for نویسه_مقدار in 'echo ':글쇠(ord(نویسه_مقدار))
                글쇠(0xffc6)
                for نویسه_مقدار in 'gksrmf':글쇠(ord(نویسه_مقدار))
                글쇠(0xffc6);글쇠(0xff0d)
                منتظر_ماندن_وضعیت('\r\n한글\r\n'.encode(),처음)
                گزارش_مقدار['checks'].append('Native VNC F9 two-set Hangul composition')
                اتصال.sendall(struct.pack('!BBHH',5,0,120,100))
                گزارش_مقدار['checks'].append('VNC pointer input accepted')
            فرآیند_مقدار.stdin.write(b'poweroff\n');فرآیند_مقدار.stdin.flush();فرآیند_مقدار.wait(timeout=15);assert فرآیند_مقدار.returncode==0
            گزارش_مقدار['passed']=True
    finally:
        if فرآیند_مقدار and فرآیند_مقدار.poll() is None:
            فرآیند_مقدار.terminate()
            try: فرآیند_مقدار.wait(timeout=5)
            except subprocess.TimeoutExpired: فرآیند_مقدار.kill();فرآیند_مقدار.wait()
        (خروجی/'serial.log').write_bytes(واقعه_نگار_ردیف)
        (خروجی/'report.json').write_text(json.dumps(گزارش_مقدار,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(گزارش_مقدار,ensure_ascii=False,indent=2))


if __name__=='__main__': اجرا_2()
