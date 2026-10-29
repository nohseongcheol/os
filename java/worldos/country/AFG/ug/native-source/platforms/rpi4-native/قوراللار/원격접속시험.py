#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق
from تور_كۆۋرۈك import تور_كۆۋرۈك


def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=كۆرسىتىش_يىلتىز / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=كۆرسىتىش_يىلتىز / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=كۆرسىتىش_يىلتىز / 'build/verification/native-remote')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    چىقار = ئۆزگەرگۈچىلەر.output
    چىقار.mkdir(parents=True, exist_ok=True)
    تەڭشەكلەر = json.loads(ئۆزگەرگۈچىلەر.access.read_text())
    خەۋەر_قىممىتى = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(ئۆزگەرگۈچىلەر.kernel.read_bytes()).hexdigest(), 'checks': []}
    def بوش_ئېغىز():
        with socket.socket() as ئۇلا:
            ئۇلا.bind(('127.0.0.5', 0))
            return ئۇلا.getsockname()[1]
    قاپ_ئېغىز, 화면포트, ھۆججەت_ئېغىز = بوش_ئېغىز(), بوش_ئېغىز(), بوش_ئېغىز()
    خاتىرە_قۇر = bytearray()
    جەريان_قىممىتى = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, تور_كۆۋرۈك(ھۆججەت_ئېغىز,
                ['tcp:{}:22'.format(قاپ_ئېغىز), 'tcp:{}:5900'.format(화면포트)], باقار_ئادرېس='127.0.0.5') as كۆۋرۈك_قىممىتى:
            실행인수 = بۇيرۇق()
            실행인수[실행인수.index('-kernel') + 1] = str(ئۆزگەرگۈچىلەر.kernel.resolve())
            جەريان_قىممىتى = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + كۆۋرۈك_قىممىتى.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    مەلۇمات = جەريان_قىممىتى.stdout.read(4096)
                    if not مەلۇمات: break
                    خاتىرە_قۇر.extend(مەلۇمات)
            ئېقىم_قىممىتى_5b72a632 = threading.Thread(target=수집, daemon=True)
            ئېقىم_قىممىتى_5b72a632.start()
            def 기다림(سۆز_تېكست, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while سۆز_تېكست not in خاتىرە_قۇر[처음:]:
                    if time.monotonic()>끝 or جەريان_قىممىتى.poll() is not None:
                        raise AssertionError('Missing '+repr(سۆز_تېكست)+'\n'+خاتىرە_قۇر[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def بىخەتەر_قاپ(پارول_قىممىتى, بۇيرۇق_قىممىتى, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=پارول_قىممىتى
                ئۆزگەرگۈچىلەر=['ssh','-v']+list(추가)+['-p',str(قاپ_ئېغىز),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',بۇيرۇق_قىممىتى]
                ئۆلچەم=subprocess.run(ئۆزگەرگۈچىلەر,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ئۆلچەم
            ئۆلچەم=بىخەتەر_قاپ('!' + تەڭشەكلەر['ssh_password'], 'echo SHOULD_NOT_RUN')
            (چىقار/'ssh-rejected.log').write_bytes(ئۆلچەم.stderr)
            assert ئۆلچەم.returncode!=0 and b'Permission denied' in ئۆلچەم.stderr and b'SHOULD_NOT_RUN' not in خاتىرە_قۇر, ئۆلچەم.stderr
            خەۋەر_قىممىتى['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ئۆلچەم=بىخەتەر_قاپ(تەڭشەكلەر['ssh_password'], 'echo SSH_NATIVE_PASS')
            (چىقار/'ssh.log').write_bytes(ئۆلچەم.stderr)
            (چىقار/'ssh-output.txt').write_bytes(ئۆلچەم.stdout)
            assert ئۆلچەم.returncode==0 and b'SSH_NATIVE_PASS' in ئۆلچەم.stdout, (ئۆلچەم.returncode,ئۆلچەم.stdout,ئۆلچەم.stderr)
            خەۋەر_قىممىتى['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ئۆلچەم.stderr, ئۆلچەم.stderr
            خەۋەر_قىممىتى['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ئۆلچەم=بىخەتەر_قاپ(تەڭشەكلەر['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ئۆلچەم.returncode==0 and 'JAVA چىقار: 안녕하세요 😀'.encode() in ئۆلچەم.stdout,ئۆلچەم.stdout
            خەۋەر_قىممىتى['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ئۆلچەم=بىخەتەر_قاپ(تەڭشەكلەر['ssh_password'], 'missing_remote_command')
            assert ئۆلچەم.returncode==127,ئۆلچەم.returncode
            خەۋەر_قىممىتى['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ئۆلچەم=بىخەتەر_قاپ(تەڭشەكلەر['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (چىقار/'ssh-rekey.log').write_bytes(ئۆلچەم.stderr)
            assert ئۆلچەم.returncode==0 and 'class 창예제'.encode() in ئۆلچەم.stdout, (ئۆلچەم.returncode,ئۆلچەم.stdout,ئۆلچەم.stderr)
            assert ئۆلچەم.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ئۆلچەم.stderr
            خەۋەر_قىممىتى['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(قاپ_ئېغىز),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ئۆز_ئارا_پاراڭ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();تاللاش_قىممىتى=selectors.DefaultSelector();تاللاش_قىممىتى.register(ئۆز_ئارا_پاراڭ.stdout,selectors.EVENT_READ)
            def 대화읽기(كۆرسەتمەك_قىممىتى):
                마감=time.monotonic()+30
                while كۆرسەتمەك_قىممىتى not in 대화기록:
                    if time.monotonic()>마감 or ئۆز_ئارا_پاراڭ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(كۆرسەتمەك_قىممىتى)+' '+repr(bytes(대화기록)))
                    for كىرگۈزۈش_قىممىتى,_ in تاللاش_قىممىتى.select(.1):
                        조각=كىرگۈزۈش_قىممىتى.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ئۆز_ئارا_پاراڭ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ئۆز_ئارا_پاراڭ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ئۆز_ئارا_پاراڭ.stdin.write(b'\x04');ئۆز_ئارا_پاراڭ.stdin.flush();나머지,خاتالىق=ئۆز_ئارا_پاراڭ.communicate(timeout=15)
                assert ئۆز_ئارا_پاراڭ.returncode==0 and b'PTY allocation request failed' not in خاتالىق,(ئۆز_ئارا_پاراڭ.returncode,خاتالىق)
                (چىقار/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                تاللاش_قىممىتى.close()
                if ئۆز_ئارا_پاراڭ.poll() is None:ئۆز_ئارا_پاراڭ.kill();ئۆز_ئارا_پاراڭ.wait()
            خەۋەر_قىممىتى['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ئۇلا, 수):
                مەلۇمات=bytearray()
                while len(مەلۇمات)<수:
                    덩이=ئۇلا.recv(수-len(مەلۇمات))
                    if not 덩이: raise AssertionError('RFB EOF')
                    مەلۇمات.extend(덩이)
                return bytes(مەلۇمات)
            def 화면인증(پارول_قىممىتى):
                ئۇلا=socket.create_connection(('127.0.0.5',화면포트),10);ئۇلا.settimeout(30)
                assert 정확히(ئۇلا,12)==b'RFB 003.008\n'
                ئۇلا.sendall(b'RFB 003.008\n');assert 정확히(ئۇلا,2)==b'\x01\x02'
                ئۇلا.sendall(b'\x02');سۈرۈشتۈرۈش_قىممىتى=정확히(ئۇلا,16)
                입력암호=پارول_قىممىتى.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ئۇلا.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(سۈرۈشتۈرۈش_قىممىتى))
                ھالەت_قىممىتى=struct.unpack('!I',정확히(ئۇلا,4))[0]
                return ئۇلا,ھالەت_قىممىتى
            ئۈنۈمسىز_پارول='!' if not تەڭشەكلەر['vnc_password'].startswith('!') else '?'
            ئۇلا,ھالەت_قىممىتى=화면인증(ئۈنۈمسىز_پارول);assert ھالەت_قىممىتى==1;ئۇلا.close();time.sleep(.6)
            خەۋەر_قىممىتى['checks'].append('VNC incorrect password rejected')
            ئۇلا,ھالەت_قىممىتى=화면인증(تەڭشەكلەر['vnc_password']);assert ھالەت_قىممىتى==0
            with ئۇلا:
                ئۇلا.sendall(b'\x01');초기=정확히(ئۇلا,24);너비,높이=struct.unpack('!HH',초기[:4]);ئاتى=정확히(ئۇلا,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ئاتى
                def 화면(증분=0):
                    ئۇلا.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ئۇلا,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    سىزىش_قىممىتى=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_كوردىنات,세로좌표,영역너비,영역높이,ئۇسۇل_ھالەت=struct.unpack('!HHHHi',정확히(ئۇلا,12));assert ئۇسۇل_ھالەت==0 and x_كوردىنات+영역너비<=너비 and 세로좌표+영역높이<=높이
                        پىكسېل=정확히(ئۇلا,영역너비*영역높이*4);합계+=len(پىكسېل)
                        for قۇر in range(영역높이):سىزىش_قىممىتى[((세로좌표+قۇر)*너비+x_كوردىنات)*4:((세로좌표+قۇر)*너비+x_كوردىنات+영역너비)*4]=پىكسېل[قۇر*영역너비*4:(قۇر+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(سىزىش_قىممىتى),'raw','BGRX').save(str(چىقار/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                خەۋەر_قىممىتى['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                خەۋەر_قىممىتى['checks'].append('RFB incremental update')
                처음=len(خاتىرە_قۇر)
                for ھەرپ_بەلگە_قىممىتى in 'echo VNC_NATIVE_PASS\r':
                    بەلگە=0xff0d if ھەرپ_بەلگە_قىممىتى=='\r' else ord(ھەرپ_بەلگە_قىممىتى)
                    ئۇلا.sendall(struct.pack('!BBHI',4,1,0,بەلگە));ئۇلا.sendall(struct.pack('!BBHI',4,0,0,بەلگە))
                기다림(b'VNC_NATIVE_PASS',처음)
                خەۋەر_قىممىتى['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(بەلگە,누름=1):ئۇلا.sendall(struct.pack('!BBHI',4,누름,0,بەلگە))
                처음=len(خاتىرە_قۇر)
                for ھەرپ_بەلگە_قىممىتى in 'echo ':글쇠(ord(ھەرپ_بەلگە_قىممىتى))
                글쇠(0xffc6)
                for ھەرپ_بەلگە_قىممىتى in 'gksrmf':글쇠(ord(ھەرپ_بەلگە_قىممىتى))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                خەۋەر_قىممىتى['checks'].append('Native VNC F9 two-set Hangul composition')
                ئۇلا.sendall(struct.pack('!BBHH',5,0,120,100))
                خەۋەر_قىممىتى['checks'].append('VNC pointer input accepted')
            جەريان_قىممىتى.stdin.write(b'poweroff\n');جەريان_قىممىتى.stdin.flush();جەريان_قىممىتى.wait(timeout=15);assert جەريان_قىممىتى.returncode==0
            خەۋەر_قىممىتى['passed']=True
    finally:
        if جەريان_قىممىتى and جەريان_قىممىتى.poll() is None:
            جەريان_قىممىتى.terminate()
            try: جەريان_قىممىتى.wait(timeout=5)
            except subprocess.TimeoutExpired: جەريان_قىممىتى.kill();جەريان_قىممىتى.wait()
        (چىقار/'serial.log').write_bytes(خاتىرە_قۇر)
        (چىقار/'report.json').write_text(json.dumps(خەۋەر_قىممىتى,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(خەۋەر_قىممىتى,ensure_ascii=False,indent=2))


if __name__=='__main__': ئىجرا_قىل_2()
