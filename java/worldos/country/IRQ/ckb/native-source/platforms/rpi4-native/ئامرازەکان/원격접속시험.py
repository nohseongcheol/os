#!/usr/bin/env python3
"""ڕاستەکی_دەیتا OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from جێبەجێکردن_فەرمان import 기준, فەرمان
from 통신다리 import 통신다리


def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    ڕێكبەندەكان = json.loads(인수.access.read_text())
    ڕاپۆرت_نرخ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def بەتاڵ_دەرگا():
        with socket.socket() as لكاندن:
            لكاندن.bind(('127.0.0.5', 0))
            return لكاندن.getsockname()[1]
    توێکڵ_دەرگا, 화면포트, فایل_دەرگا = بەتاڵ_دەرگا(), بەتاڵ_دەرگا(), بەتاڵ_دەرگا()
    تۆمار_ڕزن = bytearray()
    پرۆسە_نرخ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(فایل_دەرگا,
                ['tcp:{}:22'.format(توێکڵ_دەرگا), 'tcp:{}:5900'.format(화면포트)], جێدەر_ناونیشان='127.0.0.5') as 다리:
            실행인수 = فەرمان()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            پرۆسە_نرخ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    دەیتا = پرۆسە_نرخ.stdout.read(4096)
                    if not دەیتا: break
                    تۆمار_ڕزن.extend(دەیتا)
            ڕستە_نرخ = threading.Thread(target=수집, daemon=True)
            ڕستە_نرخ.start()
            def چاوەڕوان_کردن_دۆخ(وشە_دەق, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while وشە_دەق not in تۆمار_ڕزن[처음:]:
                    if time.monotonic()>끝 or پرۆسە_نرخ.poll() is not None:
                        raise AssertionError('Missing '+repr(وشە_دەق)+'\n'+تۆمار_ڕزن[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            چاوەڕوان_کردن_دۆخ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def پارێزراو_توێکڵ(نهێنوشە_نرخ, ڕێنمایی_نرخ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=نهێنوشە_نرخ
                인수=['ssh','-v']+list(추가)+['-p',str(توێکڵ_دەرگا),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ڕێنمایی_نرخ]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=پارێزراو_توێکڵ('!' + ڕێكبەندەكان['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in تۆمار_ڕزن, 결과.stderr
            ڕاپۆرت_نرخ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=پارێزراو_توێکڵ(ڕێكبەندەكان['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ڕاپۆرت_نرخ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ڕاپۆرت_نرخ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=پارێزراو_توێکڵ(ڕێكبەندەكان['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ڕاپۆرت_نرخ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=پارێزراو_توێکڵ(ڕێكبەندەكان['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ڕاپۆرت_نرخ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=پارێزراو_توێکڵ(ڕێكبەندەكان['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ڕاپۆرت_نرخ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(توێکڵ_دەرگا),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            دانوستانی_سێشن=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();بژاردە_نرخ=selectors.DefaultSelector();بژاردە_نرخ.register(دانوستانی_سێشن.stdout,selectors.EVENT_READ)
            def 대화읽기(نیشاندان_نرخ):
                마감=time.monotonic()+30
                while نیشاندان_نرخ not in 대화기록:
                    if time.monotonic()>마감 or دانوستانی_سێشن.poll() is not None:raise AssertionError('SSH interactive missing '+repr(نیشاندان_نرخ)+' '+repr(bytes(대화기록)))
                    for تێنووسین_نرخ,_ in بژاردە_نرخ.select(.1):
                        조각=تێنووسین_نرخ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                دانوستانی_سێشن.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');دانوستانی_سێشن.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                دانوستانی_سێشن.stdin.write(b'\x04');دانوستانی_سێشن.stdin.flush();나머지,هەڵە=دانوستانی_سێشن.communicate(timeout=15)
                assert دانوستانی_سێشن.returncode==0 and b'PTY allocation request failed' not in هەڵە,(دانوستانی_سێشن.returncode,هەڵە)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                بژاردە_نرخ.close()
                if دانوستانی_سێشن.poll() is None:دانوستانی_سێشن.kill();دانوستانی_سێشن.wait()
            ڕاپۆرت_نرخ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(لكاندن, 수):
                دەیتا=bytearray()
                while len(دەیتا)<수:
                    덩이=لكاندن.recv(수-len(دەیتا))
                    if not 덩이: raise AssertionError('RFB EOF')
                    دەیتا.extend(덩이)
                return bytes(دەیتا)
            def 화면인증(نهێنوشە_نرخ):
                لكاندن=socket.create_connection(('127.0.0.5',화면포트),10);لكاندن.settimeout(30)
                assert 정확히(لكاندن,12)==b'RFB 003.008\n'
                لكاندن.sendall(b'RFB 003.008\n');assert 정확히(لكاندن,2)==b'\x01\x02'
                لكاندن.sendall(b'\x02');ئاستەنگ_نرخ=정확히(لكاندن,16)
                입력암호=نهێنوشە_نرخ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                لكاندن.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ئاستەنگ_نرخ))
                دۆخ_نرخ=struct.unpack('!I',정확히(لكاندن,4))[0]
                return لكاندن,دۆخ_نرخ
            بێبایەخ_نهێنوشە='!' if not ڕێكبەندەكان['vnc_password'].startswith('!') else '?'
            لكاندن,دۆخ_نرخ=화면인증(بێبایەخ_نهێنوشە);assert دۆخ_نرخ==1;لكاندن.close();time.sleep(.6)
            ڕاپۆرت_نرخ['checks'].append('VNC incorrect password rejected')
            لكاندن,دۆخ_نرخ=화면인증(ڕێكبەندەكان['vnc_password']);assert دۆخ_نرخ==0
            with لكاندن:
                لكاندن.sendall(b'\x01');초기=정확히(لكاندن,24);너비,높이=struct.unpack('!HH',초기[:4]);ناو=정확히(لكاندن,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ناو
                def 화면(증분=0):
                    لكاندن.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(لكاندن,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    نگار_نرخ=bytearray(너비*높이*4)
                    for _ in range(수):
                        پۆوتانی_x,세로좌표,영역너비,영역높이,ڕێگا_دۆخ=struct.unpack('!HHHHi',정확히(لكاندن,12));assert ڕێگا_دۆخ==0 and پۆوتانی_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        پێڵ=정확히(لكاندن,영역너비*영역높이*4);합계+=len(پێڵ)
                        for دێڕ in range(영역높이):نگار_نرخ[((세로좌표+دێڕ)*너비+پۆوتانی_x)*4:((세로좌표+دێڕ)*너비+پۆوتانی_x+영역너비)*4]=پێڵ[دێڕ*영역너비*4:(دێڕ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(نگار_نرخ),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ڕاپۆرت_نرخ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ڕاپۆرت_نرخ['checks'].append('RFB incremental update')
                처음=len(تۆمار_ڕزن)
                for نووسە_نرخ in 'echo VNC_NATIVE_PASS\r':
                    سیمبۆل=0xff0d if نووسە_نرخ=='\r' else ord(نووسە_نرخ)
                    لكاندن.sendall(struct.pack('!BBHI',4,1,0,سیمبۆل));لكاندن.sendall(struct.pack('!BBHI',4,0,0,سیمبۆل))
                چاوەڕوان_کردن_دۆخ(b'VNC_NATIVE_PASS',처음)
                ڕاپۆرت_نرخ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(سیمبۆل,누름=1):لكاندن.sendall(struct.pack('!BBHI',4,누름,0,سیمبۆل))
                처음=len(تۆمار_ڕزن)
                for نووسە_نرخ in 'echo ':글쇠(ord(نووسە_نرخ))
                글쇠(0xffc6)
                for نووسە_نرخ in 'gksrmf':글쇠(ord(نووسە_نرخ))
                글쇠(0xffc6);글쇠(0xff0d)
                چاوەڕوان_کردن_دۆخ('\r\n한글\r\n'.encode(),처음)
                ڕاپۆرت_نرخ['checks'].append('Native VNC F9 two-set Hangul composition')
                لكاندن.sendall(struct.pack('!BBHH',5,0,120,100))
                ڕاپۆرت_نرخ['checks'].append('VNC pointer input accepted')
            پرۆسە_نرخ.stdin.write(b'poweroff\n');پرۆسە_نرخ.stdin.flush();پرۆسە_نرخ.wait(timeout=15);assert پرۆسە_نرخ.returncode==0
            ڕاپۆرت_نرخ['passed']=True
    finally:
        if پرۆسە_نرخ and پرۆسە_نرخ.poll() is None:
            پرۆسە_نرخ.terminate()
            try: پرۆسە_نرخ.wait(timeout=5)
            except subprocess.TimeoutExpired: پرۆسە_نرخ.kill();پرۆسە_نرخ.wait()
        (출력/'serial.log').write_bytes(تۆمار_ڕزن)
        (출력/'report.json').write_text(json.dumps(ڕاپۆرت_نرخ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ڕاپۆرت_نرخ,ensure_ascii=False,indent=2))


if __name__=='__main__': ڕادان()
