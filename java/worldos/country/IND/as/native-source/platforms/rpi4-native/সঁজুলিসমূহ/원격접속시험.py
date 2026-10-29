#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from নিষ্পাদন_আদেশ import 기준, কমান্ড
from নেটৱৰ্ক_ব্ৰীজ import নেটৱৰ্ক_ব্ৰীজ


def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    নিৰ্গম = 인수.output
    নিৰ্গম.mkdir(parents=True, exist_ok=True)
    বৈশিষ্ট্য = json.loads(인수.access.read_text())
    ৰিপ_ৰ্ট_মান = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def খালী_পৰ্ট():
        with socket.socket() as সংযোগ_স্থাপনা:
            সংযোগ_স্থাপনা.bind(('127.0.0.5', 0))
            return সংযোগ_স্থাপনা.getsockname()[1]
    শ্বেল_পৰ্ট, 화면포트, ফাইল_পৰ্ট = খালী_পৰ্ট(), খালী_পৰ্ট(), খালী_পৰ্ট()
    লগ_শাৰী = bytearray()
    প্ৰক্ৰিয়া_মান = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, নেটৱৰ্ক_ব্ৰীজ(ফাইল_পৰ্ট,
                ['tcp:{}:22'.format(শ্বেল_পৰ্ট), 'tcp:{}:5900'.format(화면포트)], হ_ষ্ট_ঠিকনা='127.0.0.5') as ব্ৰীজ_মান:
            실행인수 = কমান্ড()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            প্ৰক্ৰিয়া_মান = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ব্ৰীজ_মান.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ডাটা = প্ৰক্ৰিয়া_মান.stdout.read(4096)
                    if not ডাটা: break
                    লগ_শাৰী.extend(ডাটা)
            আঁহ_মান = threading.Thread(target=수집, daemon=True)
            আঁহ_মান.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in লগ_শাৰী[처음:]:
                    if time.monotonic()>끝 or প্ৰক্ৰিয়া_মান.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+লগ_শাৰী[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def নিৰাপদ_শ্বেল(পাছৱৰ্ড_মান, নিৰ্দেশনা_মান, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=পাছৱৰ্ড_মান
                인수=['ssh','-v']+list(추가)+['-p',str(শ্বেল_পৰ্ট),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',নিৰ্দেশনা_মান]
                পৰিমাপ=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return পৰিমাপ
            পৰিমাপ=নিৰাপদ_শ্বেল('!' + বৈশিষ্ট্য['ssh_password'], 'echo SHOULD_NOT_RUN')
            (নিৰ্গম/'ssh-rejected.log').write_bytes(পৰিমাপ.stderr)
            assert পৰিমাপ.returncode!=0 and b'Permission denied' in পৰিমাপ.stderr and b'SHOULD_NOT_RUN' not in লগ_শাৰী, পৰিমাপ.stderr
            ৰিপ_ৰ্ট_মান['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            পৰিমাপ=নিৰাপদ_শ্বেল(বৈশিষ্ট্য['ssh_password'], 'echo SSH_NATIVE_PASS')
            (নিৰ্গম/'ssh.log').write_bytes(পৰিমাপ.stderr)
            (নিৰ্গম/'ssh-output.txt').write_bytes(পৰিমাপ.stdout)
            assert পৰিমাপ.returncode==0 and b'SSH_NATIVE_PASS' in পৰিমাপ.stdout, (পৰিমাপ.returncode,পৰিমাপ.stdout,পৰিমাপ.stderr)
            ৰিপ_ৰ্ট_মান['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in পৰিমাপ.stderr, পৰিমাপ.stderr
            ৰিপ_ৰ্ট_মান['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            পৰিমাপ=নিৰাপদ_শ্বেল(বৈশিষ্ট্য['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert পৰিমাপ.returncode==0 and 'JAVA নিৰ্গম: 안녕하세요 😀'.encode() in পৰিমাপ.stdout,পৰিমাপ.stdout
            ৰিপ_ৰ্ট_মান['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            পৰিমাপ=নিৰাপদ_শ্বেল(বৈশিষ্ট্য['ssh_password'], 'missing_remote_command')
            assert পৰিমাপ.returncode==127,পৰিমাপ.returncode
            ৰিপ_ৰ্ট_মান['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            পৰিমাপ=নিৰাপদ_শ্বেল(বৈশিষ্ট্য['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (নিৰ্গম/'ssh-rekey.log').write_bytes(পৰিমাপ.stderr)
            assert পৰিমাপ.returncode==0 and 'class 창예제'.encode() in পৰিমাপ.stdout, (পৰিমাপ.returncode,পৰিমাপ.stdout,পৰিমাপ.stderr)
            assert পৰিমাপ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, পৰিমাপ.stderr
            ৰিপ_ৰ্ট_মান['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(শ্বেল_পৰ্ট),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            আন্তঃসক্রিয়_চেচন=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();চয়ন_মান=selectors.DefaultSelector();চয়ন_মান.register(আন্তঃসক্রিয়_চেচন.stdout,selectors.EVENT_READ)
            def 대화읽기(শ্ব_মান):
                마감=time.monotonic()+30
                while শ্ব_মান not in 대화기록:
                    if time.monotonic()>마감 or আন্তঃসক্রিয়_চেচন.poll() is not None:raise AssertionError('SSH interactive missing '+repr(শ্ব_মান)+' '+repr(bytes(대화기록)))
                    for প্রবিষ্ট_মান,_ in চয়ন_মান.select(.1):
                        조각=প্রবিষ্ট_মান.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                আন্তঃসক্রিয়_চেচন.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');আন্তঃসক্রিয়_চেচন.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                আন্তঃসক্রিয়_চেচন.stdin.write(b'\x04');আন্তঃসক্রিয়_চেচন.stdin.flush();나머지,ত্ৰুটি=আন্তঃসক্রিয়_চেচন.communicate(timeout=15)
                assert আন্তঃসক্রিয়_চেচন.returncode==0 and b'PTY allocation request failed' not in ত্ৰুটি,(আন্তঃসক্রিয়_চেচন.returncode,ত্ৰুটি)
                (নিৰ্গম/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                চয়ন_মান.close()
                if আন্তঃসক্রিয়_চেচন.poll() is None:আন্তঃসক্রিয়_চেচন.kill();আন্তঃসক্রিয়_চেচন.wait()
            ৰিপ_ৰ্ট_মান['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(সংযোগ_স্থাপনা, 수):
                ডাটা=bytearray()
                while len(ডাটা)<수:
                    덩이=সংযোগ_স্থাপনা.recv(수-len(ডাটা))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ডাটা.extend(덩이)
                return bytes(ডাটা)
            def 화면인증(পাছৱৰ্ড_মান):
                সংযোগ_স্থাপনা=socket.create_connection(('127.0.0.5',화면포트),10);সংযোগ_স্থাপনা.settimeout(30)
                assert 정확히(সংযোগ_স্থাপনা,12)==b'RFB 003.008\n'
                সংযোগ_স্থাপনা.sendall(b'RFB 003.008\n');assert 정확히(সংযোগ_স্থাপনা,2)==b'\x01\x02'
                সংযোগ_স্থাপনা.sendall(b'\x02');চেলেঞ্জ_মান=정확히(সংযোগ_স্থাপনা,16)
                입력암호=পাছৱৰ্ড_মান.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                সংযোগ_স্থাপনা.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(চেলেঞ্জ_মান))
                অৱস্থা_মান=struct.unpack('!I',정확히(সংযোগ_স্থাপনা,4))[0]
                return সংযোগ_স্থাপনা,অৱস্থা_মান
            অবৈধ_পাছৱৰ্ড='!' if not বৈশিষ্ট্য['vnc_password'].startswith('!') else '?'
            সংযোগ_স্থাপনা,অৱস্থা_মান=화면인증(অবৈধ_পাছৱৰ্ড);assert অৱস্থা_মান==1;সংযোগ_স্থাপনা.close();time.sleep(.6)
            ৰিপ_ৰ্ট_মান['checks'].append('VNC incorrect password rejected')
            সংযোগ_স্থাপনা,অৱস্থা_মান=화면인증(বৈশিষ্ট্য['vnc_password']);assert অৱস্থা_মান==0
            with সংযোগ_স্থাপনা:
                সংযোগ_স্থাপনা.sendall(b'\x01');초기=정확히(সংযোগ_স্থাপনা,24);너비,높이=struct.unpack('!HH',초기[:4]);নাম=정확히(সংযোগ_স্থাপনা,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==নাম
                def 화면(증분=0):
                    সংযোগ_স্থাপনা.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(সংযোগ_স্থাপনা,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    অংকন_মান=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ক_ৰ্ডিনেট,세로좌표,영역너비,영역높이,পদ্ধতি_মোড=struct.unpack('!HHHHi',정확히(সংযোগ_স্থাপনা,12));assert পদ্ধতি_মোড==0 and x_ক_ৰ্ডিনেট+영역너비<=너비 and 세로좌표+영역높이<=높이
                        পিক্সেল=정확히(সংযোগ_স্থাপনা,영역너비*영역높이*4);합계+=len(পিক্সেল)
                        for লাইন in range(영역높이):অংকন_মান[((세로좌표+লাইন)*너비+x_ক_ৰ্ডিনেট)*4:((세로좌표+লাইন)*너비+x_ক_ৰ্ডিনেট+영역너비)*4]=পিক্সেল[লাইন*영역너비*4:(লাইন+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(অংকন_মান),'raw','BGRX').save(str(নিৰ্গম/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ৰিপ_ৰ্ট_মান['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ৰিপ_ৰ্ট_মান['checks'].append('RFB incremental update')
                처음=len(লগ_শাৰী)
                for বৰ্ণ_মান in 'echo VNC_NATIVE_PASS\r':
                    প্ৰতীক=0xff0d if বৰ্ণ_মান=='\r' else ord(বৰ্ণ_মান)
                    সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,1,0,প্ৰতীক));সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,0,0,প্ৰতীক))
                기다림(b'VNC_NATIVE_PASS',처음)
                ৰিপ_ৰ্ট_মান['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(প্ৰতীক,누름=1):সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,누름,0,প্ৰতীক))
                처음=len(লগ_শাৰী)
                for বৰ্ণ_মান in 'echo ':글쇠(ord(বৰ্ণ_মান))
                글쇠(0xffc6)
                for বৰ্ণ_মান in 'gksrmf':글쇠(ord(বৰ্ণ_মান))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ৰিপ_ৰ্ট_মান['checks'].append('Native VNC F9 two-set Hangul composition')
                সংযোগ_স্থাপনা.sendall(struct.pack('!BBHH',5,0,120,100))
                ৰিপ_ৰ্ট_মান['checks'].append('VNC pointer input accepted')
            প্ৰক্ৰিয়া_মান.stdin.write(b'poweroff\n');প্ৰক্ৰিয়া_মান.stdin.flush();প্ৰক্ৰিয়া_মান.wait(timeout=15);assert প্ৰক্ৰিয়া_মান.returncode==0
            ৰিপ_ৰ্ট_মান['passed']=True
    finally:
        if প্ৰক্ৰিয়া_মান and প্ৰক্ৰিয়া_মান.poll() is None:
            প্ৰক্ৰিয়া_মান.terminate()
            try: প্ৰক্ৰিয়া_মান.wait(timeout=5)
            except subprocess.TimeoutExpired: প্ৰক্ৰিয়া_মান.kill();প্ৰক্ৰিয়া_মান.wait()
        (নিৰ্গম/'serial.log').write_bytes(লগ_শাৰী)
        (নিৰ্গম/'report.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ৰিপ_ৰ্ট_মান,ensure_ascii=False,indent=2))


if __name__=='__main__': সঞ্চালন()
