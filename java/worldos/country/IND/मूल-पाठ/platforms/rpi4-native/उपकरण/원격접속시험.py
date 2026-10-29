#!/usr/bin/env python3
"""वास्तविक_डेटा OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश
from ब्रिज_3de4fe3a import ब्रिज_3de4fe3a


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--kernel', type=Path, default=प्रोजेक्ट_करें_मूल / 'build/kernel8.img')
    पार्सर_48ee4b1b.add_argument('--access', type=Path, default=प्रोजेक्ट_करें_मूल / 'build/remote/access.json')
    पार्सर_48ee4b1b.add_argument('--output', type=Path, default=प्रोजेक्ट_करें_मूल / 'build/verification/native-remote')
    तर्क = पार्सर_48ee4b1b.parse_args()
    निर्गम = तर्क.output
    निर्गम.mkdir(parents=True, exist_ok=True)
    विन्यास = json.loads(तर्क.access.read_text())
    रिपोर्ट_मान = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(तर्क.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as जोड़ना:
            जोड़ना.bind(('127.0.0.5', 0))
            return जोड़ना.getsockname()[1]
    शेल_पोर्ट, 화면포트, फ़ाइल_पोर्ट = 빈포트(), 빈포트(), 빈포트()
    लॉग_रिकॉर्ड = bytearray()
    प्रक्रिया_मान = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ब्रिज_3de4fe3a(फ़ाइल_पोर्ट,
                ['tcp:{}:22'.format(शेल_पोर्ट), 'tcp:{}:5900'.format(화면포트)], आयोजक_पता='127.0.0.5') as ब्रिज_मान:
            실행인수 = आदेश()
            실행인수[실행인수.index('-kernel') + 1] = str(तर्क.kernel.resolve())
            प्रक्रिया_मान = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ब्रिज_मान.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    आँकड़े = प्रक्रिया_मान.stdout.read(4096)
                    if not आँकड़े: break
                    लॉग_रिकॉर्ड.extend(आँकड़े)
            थ्रेड_मान = threading.Thread(target=수집, daemon=True)
            थ्रेड_मान.start()
            def प्रतीक्षा_स्थिति(शब्द_पाठ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while शब्द_पाठ not in लॉग_रिकॉर्ड[처음:]:
                    if time.monotonic()>끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing '+repr(शब्द_पाठ)+'\n'+लॉग_रिकॉर्ड[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            प्रतीक्षा_स्थिति(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def सुरक्षित_शेल(पासवर्ड_मान, 명령어, जोड़ें_एन्ट्री=()):
                환경['JKOROS_TEST_PASSWORD']=पासवर्ड_मान
                तर्क=['ssh','-v']+list(जोड़ें_एन्ट्री)+['-p',str(शेल_पोर्ट),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                परिणाम=subprocess.run(तर्क,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return परिणाम
            परिणाम=सुरक्षित_शेल('!' + विन्यास['ssh_password'], 'echo SHOULD_NOT_RUN')
            (निर्गम/'ssh-rejected.log').write_bytes(परिणाम.stderr)
            assert परिणाम.returncode!=0 and b'Permission denied' in परिणाम.stderr and b'SHOULD_NOT_RUN' not in लॉग_रिकॉर्ड, परिणाम.stderr
            रिपोर्ट_मान['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            परिणाम=सुरक्षित_शेल(विन्यास['ssh_password'], 'echo SSH_NATIVE_PASS')
            (निर्गम/'ssh.log').write_bytes(परिणाम.stderr)
            (निर्गम/'ssh-output.txt').write_bytes(परिणाम.stdout)
            assert परिणाम.returncode==0 and b'SSH_NATIVE_PASS' in परिणाम.stdout, (परिणाम.returncode,परिणाम.stdout,परिणाम.stderr)
            रिपोर्ट_मान['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in परिणाम.stderr, परिणाम.stderr
            रिपोर्ट_मान['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            परिणाम=सुरक्षित_शेल(विन्यास['ssh_password'], 'cd /example/java; java लेखनउदाहरण; cd /')
            assert परिणाम.returncode==0 and 'JAVA निर्गम: 안녕하세요 😀'.encode() in परिणाम.stdout,परिणाम.stdout
            रिपोर्ट_मान['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            परिणाम=सुरक्षित_शेल(विन्यास['ssh_password'], 'missing_remote_command')
            assert परिणाम.returncode==127,परिणाम.returncode
            रिपोर्ट_मान['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            परिणाम=सुरक्षित_शेल(विन्यास['ssh_password'], 'cat /example/java/खिड़कीउदाहरण.java', ('-o', 'RekeyLimit=1K'))
            (निर्गम/'ssh-rekey.log').write_bytes(परिणाम.stderr)
            assert परिणाम.returncode==0 and 'class खिड़कीउदाहरण'.encode() in परिणाम.stdout, (परिणाम.returncode,परिणाम.stdout,परिणाम.stderr)
            assert परिणाम.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, परिणाम.stderr
            रिपोर्ट_मान['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(शेल_पोर्ट),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            बोला_गया_पाठ=bytearray();चयन_मान=selectors.DefaultSelector();चयन_मान.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(शो_मान):
                अंति_म_समय_सीमा_मान=time.monotonic()+30
                while शो_मान not in बोला_गया_पाठ:
                    if time.monotonic()>अंति_म_समय_सीमा_मान or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(शो_मान)+' '+repr(bytes(बोला_गया_पाठ)))
                    for एन्ट्री_मान,_ in चयन_मान.select(.1):
                        조각=एन्ट्री_मान.fileobj.read(4096)
                        if 조각:बोला_गया_पाठ.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,त्रुटि=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in त्रुटि,(대화.returncode,त्रुटि)
                (निर्गम/'ssh-interactive.txt').write_bytes(बोला_गया_पाठ+나머지)
            finally:
                चयन_मान.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            रिपोर्ट_मान['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(जोड़ना, 수):
                आँकड़े=bytearray()
                while len(आँकड़े)<수:
                    चंक_मान=जोड़ना.recv(수-len(आँकड़े))
                    if not चंक_मान: raise AssertionError('RFB EOF')
                    आँकड़े.extend(चंक_मान)
                return bytes(आँकड़े)
            def 화면인증(पासवर्ड_मान):
                जोड़ना=socket.create_connection(('127.0.0.5',화면포트),10);जोड़ना.settimeout(30)
                assert 정확히(जोड़ना,12)==b'RFB 003.008\n'
                जोड़ना.sendall(b'RFB 003.008\n');assert 정확히(जोड़ना,2)==b'\x01\x02'
                जोड़ना.sendall(b'\x02');चुनौती_मान=정확히(जोड़ना,16)
                입력암호=पासवर्ड_मान.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                जोड़ना.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(चुनौती_मान))
                अवस्था_मान=struct.unpack('!I',정확히(जोड़ना,4))[0]
                return जोड़ना,अवस्था_मान
            अमान्य_पासवर्ड='!' if not विन्यास['vnc_password'].startswith('!') else '?'
            जोड़ना,अवस्था_मान=화면인증(अमान्य_पासवर्ड);assert अवस्था_मान==1;जोड़ना.close();time.sleep(.6)
            रिपोर्ट_मान['checks'].append('VNC incorrect password rejected')
            जोड़ना,अवस्था_मान=화면인증(विन्यास['vnc_password']);assert अवस्था_मान==0
            with जोड़ना:
                जोड़ना.sendall(b'\x01');प्रारंभिक_स्थिति=정확히(जोड़ना,24);너비,높이=struct.unpack('!HH',प्रारंभिक_स्थिति[:4]);नाम=정확히(जोड़ना,struct.unpack('!I',प्रारंभिक_स्थिति[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==नाम
                def 화면(वृद्धि_चरण=0):
                    जोड़ना.sendall(struct.pack('!BBHHHH',3,वृद्धि_चरण,0,0,너비,높이));머리=정확히(जोड़ना,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ड्रॉइंग_मान=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_निर्देशांक,세로좌표,영역너비,영역높이,विधि_मोड=struct.unpack('!HHHHi',정확히(जोड़ना,12));assert विधि_मोड==0 and x_निर्देशांक+영역너비<=너비 and 세로좌표+영역높이<=높이
                        पिक्सेल=정확히(जोड़ना,영역너비*영역높이*4);합계+=len(पिक्सेल)
                        for पंक्ति in range(영역높이):ड्रॉइंग_मान[((세로좌표+पंक्ति)*너비+x_निर्देशांक)*4:((세로좌표+पंक्ति)*너비+x_निर्देशांक+영역너비)*4]=पिक्सेल[पंक्ति*영역너비*4:(पंक्ति+1)*영역너비*4]
                    if not वृद्धि_चरण:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ड्रॉइंग_मान),'raw','BGRX').save(str(निर्गम/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                रिपोर्ट_मान['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                रिपोर्ट_मान['checks'].append('RFB incremental update')
                처음=len(लॉग_रिकॉर्ड)
                for कैरेक्टर_मान in 'echo VNC_NATIVE_PASS\r':
                    प्रतीक=0xff0d if कैरेक्टर_मान=='\r' else ord(कैरेक्टर_मान)
                    जोड़ना.sendall(struct.pack('!BBHI',4,1,0,प्रतीक));जोड़ना.sendall(struct.pack('!BBHI',4,0,0,प्रतीक))
                प्रतीक्षा_स्थिति(b'VNC_NATIVE_PASS',처음)
                रिपोर्ट_मान['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def कुंजी_इंक_स्ट्रोक(प्रतीक,दबाएँ_मान=1):जोड़ना.sendall(struct.pack('!BBHI',4,दबाएँ_मान,0,प्रतीक))
                처음=len(लॉग_रिकॉर्ड)
                for कैरेक्टर_मान in 'echo ':कुंजी_इंक_स्ट्रोक(ord(कैरेक्टर_मान))
                कुंजी_इंक_स्ट्रोक(0xffc6)
                for कैरेक्टर_मान in 'gksrmf':कुंजी_इंक_स्ट्रोक(ord(कैरेक्टर_मान))
                कुंजी_इंक_स्ट्रोक(0xffc6);कुंजी_इंक_स्ट्रोक(0xff0d)
                प्रतीक्षा_स्थिति('\r\n한글\r\n'.encode(),처음)
                रिपोर्ट_मान['checks'].append('Native VNC F9 two-set Hangul composition')
                जोड़ना.sendall(struct.pack('!BBHH',5,0,120,100))
                रिपोर्ट_मान['checks'].append('VNC pointer input accepted')
            प्रक्रिया_मान.stdin.write(b'poweroff\n');प्रक्रिया_मान.stdin.flush();प्रक्रिया_मान.wait(timeout=15);assert प्रक्रिया_मान.returncode==0
            रिपोर्ट_मान['passed']=True
    finally:
        if प्रक्रिया_मान and प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try: प्रक्रिया_मान.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
        (निर्गम/'serial.log').write_bytes(लॉग_रिकॉर्ड)
        (निर्गम/'report.json').write_text(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2))


if __name__=='__main__': चलाएँ()
