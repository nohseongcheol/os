#!/usr/bin/env python3
"""තථ්_ය_දත්ත OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය
from ජාලය_පාලම import ජාලය_පාලම


def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    විස්තාරක = 해석기.parse_args()
    출력 = විස්තාරක.output
    출력.mkdir(parents=True, exist_ok=True)
    සැකසුම් = json.loads(විස්තාරක.access.read_text())
    වාර්තාව_අගය = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(විස්තාරක.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ශූන්_ය_තොට():
        with socket.socket() as සම්බන්ද_වන්න:
            සම්බන්ද_වන්න.bind(('127.0.0.5', 0))
            return සම්බන්ද_වන්න.getsockname()[1]
    කවචය_තොට, 화면포트, ගොනුව_තොට = ශූන්_ය_තොට(), ශූන්_ය_තොට(), ශූන්_ය_තොට()
    ලොගය_පේළිය = bytearray()
    ක්_රියාවලිය_අගය = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ජාලය_පාලම(ගොනුව_තොට,
                ['tcp:{}:22'.format(කවචය_තොට), 'tcp:{}:5900'.format(화면포트)], ධාරකය_යොමුව='127.0.0.5') as පාලම_අගය:
            실행인수 = විධානය()
            실행인수[실행인수.index('-kernel') + 1] = str(විස්තාරක.kernel.resolve())
            ක්_රියාවලිය_අගය = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + පාලම_අගය.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    දත්ත = ක්_රියාවලිය_අගය.stdout.read(4096)
                    if not දත්ත: break
                    ලොගය_පේළිය.extend(දත්ත)
            පොට_අගය = threading.Thread(target=수집, daemon=True)
            පොට_අගය.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in ලොගය_පේළිය[처음:]:
                    if time.monotonic()>끝 or ක්_රියාවලිය_අගය.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+ලොගය_පේළිය[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def සුරක්ෂිත_කවචය(මුර_පදය_අගය, උපදෙස_අගය, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=මුර_පදය_අගය
                විස්තාරක=['ssh','-v']+list(추가)+['-p',str(කවචය_තොට),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',උපදෙස_අගය]
                결과=subprocess.run(විස්තාරක,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=සුරක්ෂිත_කවචය('!' + සැකසුම්['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in ලොගය_පේළිය, 결과.stderr
            වාර්තාව_අගය['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=සුරක්ෂිත_කවචය(සැකසුම්['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            වාර්තාව_අගය['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            වාර්තාව_අගය['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=සුරක්ෂිත_කවචය(සැකසුම්['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            වාර්තාව_අගය['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=සුරක්ෂිත_කවචය(සැකසුම්['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            වාර්තාව_අගය['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=සුරක්ෂිත_කවචය(සැකසුම්['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            වාර්තාව_අගය['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(කවචය_තොට),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            අන්තර්ක්_රියාකාරී_සැසිය=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();තේරීම_අගය=selectors.DefaultSelector();තේරීම_අගය.register(අන්තර්ක්_රියාකාරී_සැසිය.stdout,selectors.EVENT_READ)
            def 대화읽기(දර්ශනය_අගය):
                마감=time.monotonic()+30
                while දර්ශනය_අගය not in 대화기록:
                    if time.monotonic()>마감 or අන්තර්ක්_රියාකාරී_සැසිය.poll() is not None:raise AssertionError('SSH interactive missing '+repr(දර්ශනය_අගය)+' '+repr(bytes(대화기록)))
                    for පිවිසුම_අගය,_ in තේරීම_අගය.select(.1):
                        조각=පිවිසුම_අගය.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                අන්තර්ක්_රියාකාරී_සැසිය.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');අන්තර්ක්_රියාකාරී_සැසිය.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                අන්තර්ක්_රියාකාරී_සැසිය.stdin.write(b'\x04');අන්තර්ක්_රියාකාරී_සැසිය.stdin.flush();나머지,දෝෂය=අන්තර්ක්_රියාකාරී_සැසිය.communicate(timeout=15)
                assert අන්තර්ක්_රියාකාරී_සැසිය.returncode==0 and b'PTY allocation request failed' not in දෝෂය,(අන්තර්ක්_රියාකාරී_සැසිය.returncode,දෝෂය)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                තේරීම_අගය.close()
                if අන්තර්ක්_රියාකාරී_සැසිය.poll() is None:අන්තර්ක්_රියාකාරී_සැසිය.kill();අන්තර්ක්_රියාකාරී_සැසිය.wait()
            වාර්තාව_අගය['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(සම්බන්ද_වන්න, 수):
                දත්ත=bytearray()
                while len(දත්ත)<수:
                    덩이=සම්බන්ද_වන්න.recv(수-len(දත්ත))
                    if not 덩이: raise AssertionError('RFB EOF')
                    දත්ත.extend(덩이)
                return bytes(දත්ත)
            def 화면인증(මුර_පදය_අගය):
                සම්බන්ද_වන්න=socket.create_connection(('127.0.0.5',화면포트),10);සම්බන්ද_වන්න.settimeout(30)
                assert 정확히(සම්බන්ද_වන්න,12)==b'RFB 003.008\n'
                සම්බන්ද_වන්න.sendall(b'RFB 003.008\n');assert 정확히(සම්බන්ද_වන්න,2)==b'\x01\x02'
                සම්බන්ද_වන්න.sendall(b'\x02');අභියෝගය_අගය=정확히(සම්බන්ද_වන්න,16)
                입력암호=මුර_පදය_අගය.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                සම්බන්ද_වන්න.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(අභියෝගය_අගය))
                තත්වය_අගය=struct.unpack('!I',정확히(සම්බන්ද_වන්න,4))[0]
                return සම්බන්ද_වන්න,තත්වය_අගය
            අවලංගු_මුර_පදය='!' if not සැකසුම්['vnc_password'].startswith('!') else '?'
            සම්බන්ද_වන්න,තත්වය_අගය=화면인증(අවලංගු_මුර_පදය);assert තත්වය_අගය==1;සම්බන්ද_වන්න.close();time.sleep(.6)
            වාර්තාව_අගය['checks'].append('VNC incorrect password rejected')
            සම්බන්ද_වන්න,තත්වය_අගය=화면인증(සැකසුම්['vnc_password']);assert තත්වය_අගය==0
            with සම්බන්ද_වන්න:
                සම්බන්ද_වන්න.sendall(b'\x01');초기=정확히(සම්බන්ද_වන්න,24);너비,높이=struct.unpack('!HH',초기[:4]);නම=정확히(සම්බන්ද_වන්න,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==නම
                def 화면(증분=0):
                    සම්බන්ද_වන්න.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(සම්බන්ද_වන්න,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    චිත්_රය_අගය=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ඛණ්ඩාංකය,세로좌표,영역너비,영역높이,ක්_රමය_ප්_රකාරය=struct.unpack('!HHHHi',정확히(සම්බන්ද_වන්න,12));assert ක්_රමය_ප්_රකාරය==0 and x_ඛණ්ඩාංකය+영역너비<=너비 and 세로좌표+영역높이<=높이
                        පික්සලය=정확히(සම්බන්ද_වන්න,영역너비*영역높이*4);합계+=len(පික්සලය)
                        for පේළිය in range(영역높이):චිත්_රය_අගය[((세로좌표+පේළිය)*너비+x_ඛණ්ඩාංකය)*4:((세로좌표+පේළිය)*너비+x_ඛණ්ඩාංකය+영역너비)*4]=පික්සලය[පේළිය*영역너비*4:(පේළිය+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(චිත්_රය_අගය),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                වාර්තාව_අගය['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                වාර්තාව_අගය['checks'].append('RFB incremental update')
                처음=len(ලොගය_පේළිය)
                for අනුලකුණ_අගය in 'echo VNC_NATIVE_PASS\r':
                    සංකේතය=0xff0d if අනුලකුණ_අගය=='\r' else ord(අනුලකුණ_අගය)
                    සම්බන්ද_වන්න.sendall(struct.pack('!BBHI',4,1,0,සංකේතය));සම්බන්ද_වන්න.sendall(struct.pack('!BBHI',4,0,0,සංකේතය))
                기다림(b'VNC_NATIVE_PASS',처음)
                වාර්තාව_අගය['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(සංකේතය,누름=1):සම්බන්ද_වන්න.sendall(struct.pack('!BBHI',4,누름,0,සංකේතය))
                처음=len(ලොගය_පේළිය)
                for අනුලකුණ_අගය in 'echo ':글쇠(ord(අනුලකුණ_අගය))
                글쇠(0xffc6)
                for අනුලකුණ_අගය in 'gksrmf':글쇠(ord(අනුලකුණ_අගය))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                වාර්තාව_අගය['checks'].append('Native VNC F9 two-set Hangul composition')
                සම්බන්ද_වන්න.sendall(struct.pack('!BBHH',5,0,120,100))
                වාර්තාව_අගය['checks'].append('VNC pointer input accepted')
            ක්_රියාවලිය_අගය.stdin.write(b'poweroff\n');ක්_රියාවලිය_අගය.stdin.flush();ක්_රියාවලිය_අගය.wait(timeout=15);assert ක්_රියාවලිය_අගය.returncode==0
            වාර්තාව_අගය['passed']=True
    finally:
        if ක්_රියාවලිය_අගය and ක්_රියාවලිය_අගය.poll() is None:
            ක්_රියාවලිය_අගය.terminate()
            try: ක්_රියාවලිය_අගය.wait(timeout=5)
            except subprocess.TimeoutExpired: ක්_රියාවලිය_අගය.kill();ක්_රියාවලිය_අගය.wait()
        (출력/'serial.log').write_bytes(ලොගය_පේළිය)
        (출력/'report.json').write_text(json.dumps(වාර්තාව_අගය,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(වාර්තාව_අගය,ensure_ascii=False,indent=2))


if __name__=='__main__': ක්_රියාත්මක_කරන්න_2()
