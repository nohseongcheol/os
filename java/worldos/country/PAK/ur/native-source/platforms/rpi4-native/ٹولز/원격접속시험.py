#!/usr/bin/env python3
"""اصل_کوائف OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ, حکم
from نیٹ_ورک_برج import نیٹ_ورک_برج


def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=عکس_ڈالنا_روٹ / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=عکس_ڈالنا_روٹ / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=عکس_ڈالنا_روٹ / 'build/verification/native-remote')
    دلائل = 해석기.parse_args()
    اخراج_کا_مقام = دلائل.output
    اخراج_کا_مقام.mkdir(parents=True, exist_ok=True)
    ترتیبات = json.loads(دلائل.access.read_text())
    رپورٹ_قدر = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(دلائل.kernel.read_bytes()).hexdigest(), 'checks': []}
    def خالی_پورٹ():
        with socket.socket() as متصل_ہوں:
            متصل_ہوں.bind(('127.0.0.5', 0))
            return متصل_ہوں.getsockname()[1]
    شیل_پورٹ, 화면포트, فائل_پورٹ = خالی_پورٹ(), خالی_پورٹ(), خالی_پورٹ()
    لاگ_صف = bytearray()
    عمل_قدر = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, نیٹ_ورک_برج(فائل_پورٹ,
                ['tcp:{}:22'.format(شیل_پورٹ), 'tcp:{}:5900'.format(화면포트)], میزبان_پتہ='127.0.0.5') as برج_قدر:
            실행인수 = حکم()
            실행인수[실행인수.index('-kernel') + 1] = str(دلائل.kernel.resolve())
            عمل_قدر = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + برج_قدر.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    کوائف = عمل_قدر.stdout.read(4096)
                    if not کوائف: break
                    لاگ_صف.extend(کوائف)
            تھریڈ_قدر = threading.Thread(target=수집, daemon=True)
            تھریڈ_قدر.start()
            def انتظار_حالت(الفاظ_متن, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while الفاظ_متن not in لاگ_صف[처음:]:
                    if time.monotonic()>끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing '+repr(الفاظ_متن)+'\n'+لاگ_صف[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            انتظار_حالت(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def محفوظ_شیل(پاس_ورڈ_قدر, ہدایت_قدر, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=پاس_ورڈ_قدر
                دلائل=['ssh','-v']+list(추가)+['-p',str(شیل_پورٹ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ہدایت_قدر]
                پیمائش=subprocess.run(دلائل,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return پیمائش
            پیمائش=محفوظ_شیل('!' + ترتیبات['ssh_password'], 'echo SHOULD_NOT_RUN')
            (اخراج_کا_مقام/'ssh-rejected.log').write_bytes(پیمائش.stderr)
            assert پیمائش.returncode!=0 and b'Permission denied' in پیمائش.stderr and b'SHOULD_NOT_RUN' not in لاگ_صف, پیمائش.stderr
            رپورٹ_قدر['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            پیمائش=محفوظ_شیل(ترتیبات['ssh_password'], 'echo SSH_NATIVE_PASS')
            (اخراج_کا_مقام/'ssh.log').write_bytes(پیمائش.stderr)
            (اخراج_کا_مقام/'ssh-output.txt').write_bytes(پیمائش.stdout)
            assert پیمائش.returncode==0 and b'SSH_NATIVE_PASS' in پیمائش.stdout, (پیمائش.returncode,پیمائش.stdout,پیمائش.stderr)
            رپورٹ_قدر['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in پیمائش.stderr, پیمائش.stderr
            رپورٹ_قدر['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            پیمائش=محفوظ_شیل(ترتیبات['ssh_password'], 'cd /example/java; java چھپائیمثال; cd /')
            assert پیمائش.returncode==0 and 'JAVA اخراج_کا_مقام: 안녕하세요 😀'.encode() in پیمائش.stdout,پیمائش.stdout
            رپورٹ_قدر['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            پیمائش=محفوظ_شیل(ترتیبات['ssh_password'], 'missing_remote_command')
            assert پیمائش.returncode==127,پیمائش.returncode
            رپورٹ_قدر['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            پیمائش=محفوظ_شیل(ترتیبات['ssh_password'], 'cat /example/java/کھڑکیمثال.java', ('-o', 'RekeyLimit=1K'))
            (اخراج_کا_مقام/'ssh-rekey.log').write_bytes(پیمائش.stderr)
            assert پیمائش.returncode==0 and 'class کھڑکیمثال'.encode() in پیمائش.stdout, (پیمائش.returncode,پیمائش.stdout,پیمائش.stderr)
            assert پیمائش.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, پیمائش.stderr
            رپورٹ_قدر['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(شیل_پورٹ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            متعامل_سیشن=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();انتخاب_قدر=selectors.DefaultSelector();انتخاب_قدر.register(متعامل_سیشن.stdout,selectors.EVENT_READ)
            def 대화읽기(دکھانا_قدر):
                마감=time.monotonic()+30
                while دکھانا_قدر not in 대화기록:
                    if time.monotonic()>마감 or متعامل_سیشن.poll() is not None:raise AssertionError('SSH interactive missing '+repr(دکھانا_قدر)+' '+repr(bytes(대화기록)))
                    for اندراج_قدر,_ in انتخاب_قدر.select(.1):
                        조각=اندراج_قدر.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                متعامل_سیشن.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');متعامل_سیشن.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                متعامل_سیشن.stdin.write(b'\x04');متعامل_سیشن.stdin.flush();나머지,غلطی=متعامل_سیشن.communicate(timeout=15)
                assert متعامل_سیشن.returncode==0 and b'PTY allocation request failed' not in غلطی,(متعامل_سیشن.returncode,غلطی)
                (اخراج_کا_مقام/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                انتخاب_قدر.close()
                if متعامل_سیشن.poll() is None:متعامل_سیشن.kill();متعامل_سیشن.wait()
            رپورٹ_قدر['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(متصل_ہوں, 수):
                کوائف=bytearray()
                while len(کوائف)<수:
                    덩이=متصل_ہوں.recv(수-len(کوائف))
                    if not 덩이: raise AssertionError('RFB EOF')
                    کوائف.extend(덩이)
                return bytes(کوائف)
            def 화면인증(پاس_ورڈ_قدر):
                متصل_ہوں=socket.create_connection(('127.0.0.5',화면포트),10);متصل_ہوں.settimeout(30)
                assert 정확히(متصل_ہوں,12)==b'RFB 003.008\n'
                متصل_ہوں.sendall(b'RFB 003.008\n');assert 정확히(متصل_ہوں,2)==b'\x01\x02'
                متصل_ہوں.sendall(b'\x02');چیلنج_قدر=정확히(متصل_ہوں,16)
                입력암호=پاس_ورڈ_قدر.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                متصل_ہوں.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(چیلنج_قدر))
                حالت_قدر=struct.unpack('!I',정확히(متصل_ہوں,4))[0]
                return متصل_ہوں,حالت_قدر
            بے_جواز_پاس_ورڈ='!' if not ترتیبات['vnc_password'].startswith('!') else '?'
            متصل_ہوں,حالت_قدر=화면인증(بے_جواز_پاس_ورڈ);assert حالت_قدر==1;متصل_ہوں.close();time.sleep(.6)
            رپورٹ_قدر['checks'].append('VNC incorrect password rejected')
            متصل_ہوں,حالت_قدر=화면인증(ترتیبات['vnc_password']);assert حالت_قدر==0
            with متصل_ہوں:
                متصل_ہوں.sendall(b'\x01');초기=정확히(متصل_ہوں,24);너비,높이=struct.unpack('!HH',초기[:4]);نام=정확히(متصل_ہوں,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==نام
                def 화면(증분=0):
                    متصل_ہوں.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(متصل_ہوں,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ڈرائنگ_قدر=bytearray(너비*높이*4)
                    for _ in range(수):
                        ایکس_مربوط,세로좌표,영역너비,영역높이,طریقہ_موڈ=struct.unpack('!HHHHi',정확히(متصل_ہوں,12));assert طریقہ_موڈ==0 and ایکس_مربوط+영역너비<=너비 and 세로좌표+영역높이<=높이
                        پکسل=정확히(متصل_ہوں,영역너비*영역높이*4);합계+=len(پکسل)
                        for اندراج_کی_سطر in range(영역높이):ڈرائنگ_قدر[((세로좌표+اندراج_کی_سطر)*너비+ایکس_مربوط)*4:((세로좌표+اندراج_کی_سطر)*너비+ایکس_مربوط+영역너비)*4]=پکسل[اندراج_کی_سطر*영역너비*4:(اندراج_کی_سطر+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ڈرائنگ_قدر),'raw','BGRX').save(str(اخراج_کا_مقام/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                رپورٹ_قدر['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                رپورٹ_قدر['checks'].append('RFB incremental update')
                처음=len(لاگ_صف)
                for کریکٹر_قدر in 'echo VNC_NATIVE_PASS\r':
                    علامت=0xff0d if کریکٹر_قدر=='\r' else ord(کریکٹر_قدر)
                    متصل_ہوں.sendall(struct.pack('!BBHI',4,1,0,علامت));متصل_ہوں.sendall(struct.pack('!BBHI',4,0,0,علامت))
                انتظار_حالت(b'VNC_NATIVE_PASS',처음)
                رپورٹ_قدر['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(علامت,누름=1):متصل_ہوں.sendall(struct.pack('!BBHI',4,누름,0,علامت))
                처음=len(لاگ_صف)
                for کریکٹر_قدر in 'echo ':글쇠(ord(کریکٹر_قدر))
                글쇠(0xffc6)
                for کریکٹر_قدر in 'gksrmf':글쇠(ord(کریکٹر_قدر))
                글쇠(0xffc6);글쇠(0xff0d)
                انتظار_حالت('\r\n한글\r\n'.encode(),처음)
                رپورٹ_قدر['checks'].append('Native VNC F9 two-set Hangul composition')
                متصل_ہوں.sendall(struct.pack('!BBHH',5,0,120,100))
                رپورٹ_قدر['checks'].append('VNC pointer input accepted')
            عمل_قدر.stdin.write(b'poweroff\n');عمل_قدر.stdin.flush();عمل_قدر.wait(timeout=15);assert عمل_قدر.returncode==0
            رپورٹ_قدر['passed']=True
    finally:
        if عمل_قدر and عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try: عمل_قدر.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل_قدر.kill();عمل_قدر.wait()
        (اخراج_کا_مقام/'serial.log').write_bytes(لاگ_صف)
        (اخراج_کا_مقام/'report.json').write_text(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2))


if __name__=='__main__': چلائیں()
