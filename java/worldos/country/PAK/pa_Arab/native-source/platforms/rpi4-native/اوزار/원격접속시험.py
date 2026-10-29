#!/usr/bin/env python3
"""اصلی_کوائف OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from نفاذ_کرو_حکم import 기준, حکم
from نیٹ_ورک_برج import نیٹ_ورک_برج


def چلاؤ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    سیٹنگاں = json.loads(인수.access.read_text())
    رپورٹ_قدر = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def خالی_دہانہ():
        with socket.socket() as جڑو:
            جڑو.bind(('127.0.0.5', 0))
            return جڑو.getsockname()[1]
    شیل_دہانہ, 화면포트, فائل_دہانہ = خالی_دہانہ(), خالی_دہانہ(), خالی_دہانہ()
    لاگ_صف = bytearray()
    عمل_قدر = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, نیٹ_ورک_برج(فائل_دہانہ,
                ['tcp:{}:22'.format(شیل_دہانہ), 'tcp:{}:5900'.format(화면포트)], مہمان_پتا='127.0.0.5') as برج_قدر:
            실행인수 = حکم()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            عمل_قدر = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + برج_قدر.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    کوائف = عمل_قدر.stdout.read(4096)
                    if not کوائف: break
                    لاگ_صف.extend(کوائف)
            لڑی_قدر = threading.Thread(target=수집, daemon=True)
            لڑی_قدر.start()
            def 기다림(لفظ_متن, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while لفظ_متن not in لاگ_صف[처음:]:
                    if time.monotonic()>끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing '+repr(لفظ_متن)+'\n'+لاگ_صف[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def محفوظ_شیل(لفظی_کنجی_قدر, ہدایت_قدر, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=لفظی_کنجی_قدر
                인수=['ssh','-v']+list(추가)+['-p',str(شیل_دہانہ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ہدایت_قدر]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=محفوظ_شیل('!' + سیٹنگاں['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in لاگ_صف, 결과.stderr
            رپورٹ_قدر['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=محفوظ_شیل(سیٹنگاں['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            رپورٹ_قدر['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            رپورٹ_قدر['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=محفوظ_شیل(سیٹنگاں['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            رپورٹ_قدر['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=محفوظ_شیل(سیٹنگاں['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            رپورٹ_قدر['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=محفوظ_شیل(سیٹنگاں['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            رپورٹ_قدر['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(شیل_دہانہ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            متعامل_سیشن=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();انتخاب_قدر=selectors.DefaultSelector();انتخاب_قدر.register(متعامل_سیشن.stdout,selectors.EVENT_READ)
            def 대화읽기(نمایش_کرو_قدر):
                마감=time.monotonic()+30
                while نمایش_کرو_قدر not in 대화기록:
                    if time.monotonic()>마감 or متعامل_سیشن.poll() is not None:raise AssertionError('SSH interactive missing '+repr(نمایش_کرو_قدر)+' '+repr(bytes(대화기록)))
                    for داخلہ_قدر,_ in انتخاب_قدر.select(.1):
                        조각=داخلہ_قدر.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                متعامل_سیشن.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');متعامل_سیشن.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                متعامل_سیشن.stdin.write(b'\x04');متعامل_سیشن.stdin.flush();나머지,نقص=متعامل_سیشن.communicate(timeout=15)
                assert متعامل_سیشن.returncode==0 and b'PTY allocation request failed' not in نقص,(متعامل_سیشن.returncode,نقص)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                انتخاب_قدر.close()
                if متعامل_سیشن.poll() is None:متعامل_سیشن.kill();متعامل_سیشن.wait()
            رپورٹ_قدر['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(جڑو, 수):
                کوائف=bytearray()
                while len(کوائف)<수:
                    덩이=جڑو.recv(수-len(کوائف))
                    if not 덩이: raise AssertionError('RFB EOF')
                    کوائف.extend(덩이)
                return bytes(کوائف)
            def 화면인증(لفظی_کنجی_قدر):
                جڑو=socket.create_connection(('127.0.0.5',화면포트),10);جڑو.settimeout(30)
                assert 정확히(جڑو,12)==b'RFB 003.008\n'
                جڑو.sendall(b'RFB 003.008\n');assert 정확히(جڑو,2)==b'\x01\x02'
                جڑو.sendall(b'\x02');چیلنج_قدر=정확히(جڑو,16)
                입력암호=لفظی_کنجی_قدر.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                جڑو.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(چیلنج_قدر))
                حالت_قدر=struct.unpack('!I',정확히(جڑو,4))[0]
                return جڑو,حالت_قدر
            ناجائز_لفظی_کنجی='!' if not سیٹنگاں['vnc_password'].startswith('!') else '?'
            جڑو,حالت_قدر=화면인증(ناجائز_لفظی_کنجی);assert حالت_قدر==1;جڑو.close();time.sleep(.6)
            رپورٹ_قدر['checks'].append('VNC incorrect password rejected')
            جڑو,حالت_قدر=화면인증(سیٹنگاں['vnc_password']);assert حالت_قدر==0
            with جڑو:
                جڑو.sendall(b'\x01');초기=정확히(جڑو,24);너비,높이=struct.unpack('!HH',초기[:4]);ناں=정확히(جڑو,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ناں
                def 화면(증분=0):
                    جڑو.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(جڑو,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ڈرائنگ_قدر=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_محدد,세로좌표,영역너비,영역높이,طریقہ_موڈ=struct.unpack('!HHHHi',정확히(جڑو,12));assert طریقہ_موڈ==0 and x_محدد+영역너비<=너비 and 세로좌표+영역높이<=높이
                        دانہ=정확히(جڑو,영역너비*영역높이*4);합계+=len(دانہ)
                        for لائن in range(영역높이):ڈرائنگ_قدر[((세로좌표+لائن)*너비+x_محدد)*4:((세로좌표+لائن)*너비+x_محدد+영역너비)*4]=دانہ[لائن*영역너비*4:(لائن+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ڈرائنگ_قدر),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                رپورٹ_قدر['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                رپورٹ_قدر['checks'].append('RFB incremental update')
                처음=len(لاگ_صف)
                for کریکٹر_قدر in 'echo VNC_NATIVE_PASS\r':
                    علامت=0xff0d if کریکٹر_قدر=='\r' else ord(کریکٹر_قدر)
                    جڑو.sendall(struct.pack('!BBHI',4,1,0,علامت));جڑو.sendall(struct.pack('!BBHI',4,0,0,علامت))
                기다림(b'VNC_NATIVE_PASS',처음)
                رپورٹ_قدر['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(علامت,누름=1):جڑو.sendall(struct.pack('!BBHI',4,누름,0,علامت))
                처음=len(لاگ_صف)
                for کریکٹر_قدر in 'echo ':글쇠(ord(کریکٹر_قدر))
                글쇠(0xffc6)
                for کریکٹر_قدر in 'gksrmf':글쇠(ord(کریکٹر_قدر))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                رپورٹ_قدر['checks'].append('Native VNC F9 two-set Hangul composition')
                جڑو.sendall(struct.pack('!BBHH',5,0,120,100))
                رپورٹ_قدر['checks'].append('VNC pointer input accepted')
            عمل_قدر.stdin.write(b'poweroff\n');عمل_قدر.stdin.flush();عمل_قدر.wait(timeout=15);assert عمل_قدر.returncode==0
            رپورٹ_قدر['passed']=True
    finally:
        if عمل_قدر and عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try: عمل_قدر.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل_قدر.kill();عمل_قدر.wait()
        (출력/'serial.log').write_bytes(لاگ_صف)
        (출력/'report.json').write_text(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(رپورٹ_قدر,ensure_ascii=False,indent=2))


if __name__=='__main__': چلاؤ()
