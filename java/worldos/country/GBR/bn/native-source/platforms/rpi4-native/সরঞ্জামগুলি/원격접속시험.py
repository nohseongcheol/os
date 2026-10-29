#!/usr/bin/env python3
"""প্রকৃত_ডাটা OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ
from নেটওয়ার্ক_ব্রিজ import নেটওয়ার্ক_ব্রিজ


def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--kernel', type=Path, default=প্রকল্প_মূল / 'build/kernel8.img')
    পার্সার_48ee4b1b.add_argument('--access', type=Path, default=প্রকল্প_মূল / 'build/remote/access.json')
    পার্সার_48ee4b1b.add_argument('--output', type=Path, default=প্রকল্প_মূল / 'build/verification/native-remote')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    নির্গম = আর্গুমেন্ট_তালিকা.output
    নির্গম.mkdir(parents=True, exist_ok=True)
    সেটিংস = json.loads(আর্গুমেন্ট_তালিকা.access.read_text())
    রিপোর্ট_মান = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(আর্গুমেন্ট_তালিকা.kernel.read_bytes()).hexdigest(), 'checks': []}
    def খালি_পোর্ট():
        with socket.socket() as সংযোগ_স্থাপনা:
            সংযোগ_স্থাপনা.bind(('127.0.0.5', 0))
            return সংযোগ_স্থাপনা.getsockname()[1]
    শেল_পোর্ট, 화면포트, ফাইল_পোর্ট = খালি_পোর্ট(), খালি_পোর্ট(), খালি_পোর্ট()
    লগ_সারি = bytearray()
    প্রসেসর_মান = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, নেটওয়ার্ক_ব্রিজ(ফাইল_পোর্ট,
                ['tcp:{}:22'.format(শেল_পোর্ট), 'tcp:{}:5900'.format(화면포트)], হোস্ট_ইমেইল='127.0.0.5') as ব্রিজ_মান:
            실행인수 = আদেশ()
            실행인수[실행인수.index('-kernel') + 1] = str(আর্গুমেন্ট_তালিকা.kernel.resolve())
            প্রসেসর_মান = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ব্রিজ_মান.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ডাটা = প্রসেসর_মান.stdout.read(4096)
                    if not ডাটা: break
                    লগ_সারি.extend(ডাটা)
            থ্রেড_মান = threading.Thread(target=수집, daemon=True)
            থ্রেড_মান.start()
            def অপেক্ষা_অবস্হা(শব্দ_পাঠ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while শব্দ_পাঠ not in লগ_সারি[처음:]:
                    if time.monotonic()>끝 or প্রসেসর_মান.poll() is not None:
                        raise AssertionError('Missing '+repr(শব্দ_পাঠ)+'\n'+লগ_সারি[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            অপেক্ষা_অবস্হা(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def নিরাপদ_শেল(পাসওয়ার্ড_মান, নির্দেশ_মান, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=পাসওয়ার্ড_মান
                আর্গুমেন্ট_তালিকা=['ssh','-v']+list(추가)+['-p',str(শেল_পোর্ট),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',নির্দেশ_মান]
                পরিমাপ=subprocess.run(আর্গুমেন্ট_তালিকা,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return পরিমাপ
            পরিমাপ=নিরাপদ_শেল('!' + সেটিংস['ssh_password'], 'echo SHOULD_NOT_RUN')
            (নির্গম/'ssh-rejected.log').write_bytes(পরিমাপ.stderr)
            assert পরিমাপ.returncode!=0 and b'Permission denied' in পরিমাপ.stderr and b'SHOULD_NOT_RUN' not in লগ_সারি, পরিমাপ.stderr
            রিপোর্ট_মান['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            পরিমাপ=নিরাপদ_শেল(সেটিংস['ssh_password'], 'echo SSH_NATIVE_PASS')
            (নির্গম/'ssh.log').write_bytes(পরিমাপ.stderr)
            (নির্গম/'ssh-output.txt').write_bytes(পরিমাপ.stdout)
            assert পরিমাপ.returncode==0 and b'SSH_NATIVE_PASS' in পরিমাপ.stdout, (পরিমাপ.returncode,পরিমাপ.stdout,পরিমাপ.stderr)
            রিপোর্ট_মান['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in পরিমাপ.stderr, পরিমাপ.stderr
            রিপোর্ট_মান['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            পরিমাপ=নিরাপদ_শেল(সেটিংস['ssh_password'], 'cd /example/java; java মুদ্রণনমুনা; cd /')
            assert পরিমাপ.returncode==0 and 'JAVA নির্গম: 안녕하세요 😀'.encode() in পরিমাপ.stdout,পরিমাপ.stdout
            রিপোর্ট_মান['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            পরিমাপ=নিরাপদ_শেল(সেটিংস['ssh_password'], 'missing_remote_command')
            assert পরিমাপ.returncode==127,পরিমাপ.returncode
            রিপোর্ট_মান['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            পরিমাপ=নিরাপদ_শেল(সেটিংস['ssh_password'], 'cat /example/java/জানালানমুনা.java', ('-o', 'RekeyLimit=1K'))
            (নির্গম/'ssh-rekey.log').write_bytes(পরিমাপ.stderr)
            assert পরিমাপ.returncode==0 and 'class জানালানমুনা'.encode() in পরিমাপ.stdout, (পরিমাপ.returncode,পরিমাপ.stdout,পরিমাপ.stderr)
            assert পরিমাপ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, পরিমাপ.stderr
            রিপোর্ট_মান['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(শেল_পোর্ট),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            মিথস্ক্রিয়_সত্র=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();বাছাই_মান=selectors.DefaultSelector();বাছাই_মান.register(মিথস্ক্রিয়_সত্র.stdout,selectors.EVENT_READ)
            def 대화읽기(শো_মান):
                마감=time.monotonic()+30
                while শো_মান not in 대화기록:
                    if time.monotonic()>마감 or মিথস্ক্রিয়_সত্র.poll() is not None:raise AssertionError('SSH interactive missing '+repr(শো_মান)+' '+repr(bytes(대화기록)))
                    for ভুক্তি_মান,_ in বাছাই_মান.select(.1):
                        조각=ভুক্তি_মান.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                মিথস্ক্রিয়_সত্র.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');মিথস্ক্রিয়_সত্র.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                মিথস্ক্রিয়_সত্র.stdin.write(b'\x04');মিথস্ক্রিয়_সত্র.stdin.flush();나머지,ত্রুটি=মিথস্ক্রিয়_সত্র.communicate(timeout=15)
                assert মিথস্ক্রিয়_সত্র.returncode==0 and b'PTY allocation request failed' not in ত্রুটি,(মিথস্ক্রিয়_সত্র.returncode,ত্রুটি)
                (নির্গম/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                বাছাই_মান.close()
                if মিথস্ক্রিয়_সত্র.poll() is None:মিথস্ক্রিয়_সত্র.kill();মিথস্ক্রিয়_সত্র.wait()
            রিপোর্ট_মান['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(সংযোগ_স্থাপনা, 수):
                ডাটা=bytearray()
                while len(ডাটা)<수:
                    덩이=সংযোগ_স্থাপনা.recv(수-len(ডাটা))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ডাটা.extend(덩이)
                return bytes(ডাটা)
            def 화면인증(পাসওয়ার্ড_মান):
                সংযোগ_স্থাপনা=socket.create_connection(('127.0.0.5',화면포트),10);সংযোগ_স্থাপনা.settimeout(30)
                assert 정확히(সংযোগ_স্থাপনা,12)==b'RFB 003.008\n'
                সংযোগ_স্থাপনা.sendall(b'RFB 003.008\n');assert 정확히(সংযোগ_স্থাপনা,2)==b'\x01\x02'
                সংযোগ_স্থাপনা.sendall(b'\x02');চ্যালেঞ্জ_মান=정확히(সংযোগ_স্থাপনা,16)
                입력암호=পাসওয়ার্ড_মান.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                সংযোগ_স্থাপনা.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(চ্যালেঞ্জ_মান))
                অবস্হা_মান=struct.unpack('!I',정확히(সংযোগ_স্থাপনা,4))[0]
                return সংযোগ_স্থাপনা,অবস্হা_মান
            অবৈধ_পাসওয়ার্ড='!' if not সেটিংস['vnc_password'].startswith('!') else '?'
            সংযোগ_স্থাপনা,অবস্হা_মান=화면인증(অবৈধ_পাসওয়ার্ড);assert অবস্হা_মান==1;সংযোগ_স্থাপনা.close();time.sleep(.6)
            রিপোর্ট_মান['checks'].append('VNC incorrect password rejected')
            সংযোগ_স্থাপনা,অবস্হা_মান=화면인증(সেটিংস['vnc_password']);assert অবস্হা_মান==0
            with সংযোগ_স্থাপনা:
                সংযোগ_স্থাপনা.sendall(b'\x01');초기=정확히(সংযোগ_স্থাপনা,24);너비,높이=struct.unpack('!HH',초기[:4]);নাম=정확히(সংযোগ_স্থাপনা,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==নাম
                def 화면(증분=0):
                    সংযোগ_স্থাপনা.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(সংযোগ_স্থাপনা,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    অঙ্কন_মান=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু,영역너비,영역높이,পদ্ধতি_মোড=struct.unpack('!HHHHi',정확히(সংযোগ_স্থাপনা,12));assert পদ্ধতি_মোড==0 and X_বোতাম_অক্ষবিন্দু+영역너비<=너비 and Y_বোতাম_অক্ষবিন্দু+영역높이<=높이
                        পেল্=정확히(সংযোগ_স্থাপনা,영역너비*영역높이*4);합계+=len(পেল্)
                        for নিবেশের_পঙ্_ক্তি in range(영역높이):অঙ্কন_মান[((Y_বোতাম_অক্ষবিন্দু+নিবেশের_পঙ্_ক্তি)*너비+X_বোতাম_অক্ষবিন্দু)*4:((Y_বোতাম_অক্ষবিন্দু+নিবেশের_পঙ্_ক্তি)*너비+X_বোতাম_অক্ষবিন্দু+영역너비)*4]=পেল্[নিবেশের_পঙ্_ক্তি*영역너비*4:(নিবেশের_পঙ্_ক্তি+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(অঙ্কন_মান),'raw','BGRX').save(str(নির্গম/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                রিপোর্ট_মান['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                রিপোর্ট_মান['checks'].append('RFB incremental update')
                처음=len(লগ_সারি)
                for অক্ষর_মান in 'echo VNC_NATIVE_PASS\r':
                    প্রতীক=0xff0d if অক্ষর_মান=='\r' else ord(অক্ষর_মান)
                    সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,1,0,প্রতীক));সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,0,0,প্রতীক))
                অপেক্ষা_অবস্হা(b'VNC_NATIVE_PASS',처음)
                রিপোর্ট_মান['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(প্রতীক,누름=1):সংযোগ_স্থাপনা.sendall(struct.pack('!BBHI',4,누름,0,প্রতীক))
                처음=len(লগ_সারি)
                for অক্ষর_মান in 'echo ':글쇠(ord(অক্ষর_মান))
                글쇠(0xffc6)
                for অক্ষর_মান in 'gksrmf':글쇠(ord(অক্ষর_মান))
                글쇠(0xffc6);글쇠(0xff0d)
                অপেক্ষা_অবস্হা('\r\n한글\r\n'.encode(),처음)
                রিপোর্ট_মান['checks'].append('Native VNC F9 two-set Hangul composition')
                সংযোগ_স্থাপনা.sendall(struct.pack('!BBHH',5,0,120,100))
                রিপোর্ট_মান['checks'].append('VNC pointer input accepted')
            প্রসেসর_মান.stdin.write(b'poweroff\n');প্রসেসর_মান.stdin.flush();প্রসেসর_মান.wait(timeout=15);assert প্রসেসর_মান.returncode==0
            রিপোর্ট_মান['passed']=True
    finally:
        if প্রসেসর_মান and প্রসেসর_মান.poll() is None:
            প্রসেসর_মান.terminate()
            try: প্রসেসর_মান.wait(timeout=5)
            except subprocess.TimeoutExpired: প্রসেসর_মান.kill();প্রসেসর_মান.wait()
        (নির্গম/'serial.log').write_bytes(লগ_সারি)
        (নির্গম/'report.json').write_text(json.dumps(রিপোর্ট_মান,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(রিপোর্ট_মান,ensure_ascii=False,indent=2))


if __name__=='__main__': চালনা()
