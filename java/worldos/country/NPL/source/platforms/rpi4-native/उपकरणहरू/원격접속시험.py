#!/usr/bin/env python3
"""वास्तविक_लगत OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट, आदेश
from सञ्जाल_ब्रिज import सञ्जाल_ब्रिज


def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=परियोजना_रूट / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=परियोजना_रूट / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=परियोजना_रूट / 'build/verification/native-remote')
    तर्क = 해석기.parse_args()
    출력 = तर्क.output
    출력.mkdir(parents=True, exist_ok=True)
    सेटिङ = json.loads(तर्क.access.read_text())
    रिपोर्ट_मान = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(तर्क.kernel.read_bytes()).hexdigest(), 'checks': []}
    def रिक्त_पोर्ट():
        with socket.socket() as जडान:
            जडान.bind(('127.0.0.5', 0))
            return जडान.getsockname()[1]
    शेल_पोर्ट, 화면포트, फाइल_पोर्ट = रिक्त_पोर्ट(), रिक्त_पोर्ट(), रिक्त_पोर्ट()
    लग_रेकर्ड = bytearray()
    प्रक्रिया_मान = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, सञ्जाल_ब्रिज(फाइल_पोर्ट,
                ['tcp:{}:22'.format(शेल_पोर्ट), 'tcp:{}:5900'.format(화면포트)], होस्ट_ठेगाना='127.0.0.5') as ब्रिज_मान:
            실행인수 = आदेश()
            실행인수[실행인수.index('-kernel') + 1] = str(तर्क.kernel.resolve())
            प्रक्रिया_मान = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ब्रिज_मान.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    लगत = प्रक्रिया_मान.stdout.read(4096)
                    if not लगत: break
                    लग_रेकर्ड.extend(लगत)
            धागो_मान = threading.Thread(target=수집, daemon=True)
            धागो_मान.start()
            def 기다림(शब्द_पाठ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while शब्द_पाठ not in लग_रेकर्ड[처음:]:
                    if time.monotonic()>끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing '+repr(शब्द_पाठ)+'\n'+लग_रेकर्ड[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def सुरक्षित_गर्नुहोस्_शेल(पासवर्ड_मान, निर्देशन_मान, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=पासवर्ड_मान
                तर्क=['ssh','-v']+list(추가)+['-p',str(शेल_पोर्ट),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',निर्देशन_मान]
                मापन=subprocess.run(तर्क,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return मापन
            मापन=सुरक्षित_गर्नुहोस्_शेल('!' + सेटिङ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(मापन.stderr)
            assert मापन.returncode!=0 and b'Permission denied' in मापन.stderr and b'SHOULD_NOT_RUN' not in लग_रेकर्ड, मापन.stderr
            रिपोर्ट_मान['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            मापन=सुरक्षित_गर्नुहोस्_शेल(सेटिङ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(मापन.stderr)
            (출력/'ssh-output.txt').write_bytes(मापन.stdout)
            assert मापन.returncode==0 and b'SSH_NATIVE_PASS' in मापन.stdout, (मापन.returncode,मापन.stdout,मापन.stderr)
            रिपोर्ट_मान['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in मापन.stderr, मापन.stderr
            रिपोर्ट_मान['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            मापन=सुरक्षित_गर्नुहोस्_शेल(सेटिङ['ssh_password'], 'cd /example/java; java लेखनउदाहरण; cd /')
            assert मापन.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in मापन.stdout,मापन.stdout
            रिपोर्ट_मान['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            मापन=सुरक्षित_गर्नुहोस्_शेल(सेटिङ['ssh_password'], 'missing_remote_command')
            assert मापन.returncode==127,मापन.returncode
            रिपोर्ट_मान['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            मापन=सुरक्षित_गर्नुहोस्_शेल(सेटिङ['ssh_password'], 'cat /example/java/झ्यालउदाहरण.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(मापन.stderr)
            assert मापन.returncode==0 and 'class झ्यालउदाहरण'.encode() in मापन.stdout, (मापन.returncode,मापन.stdout,मापन.stderr)
            assert मापन.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, मापन.stderr
            रिपोर्ट_मान['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(शेल_पोर्ट),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            अन्तरक्रियाशील_सत्र=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();चयन_मान=selectors.DefaultSelector();चयन_मान.register(अन्तरक्रियाशील_सत्र.stdout,selectors.EVENT_READ)
            def 대화읽기(शो_मान):
                마감=time.monotonic()+30
                while शो_मान not in 대화기록:
                    if time.monotonic()>마감 or अन्तरक्रियाशील_सत्र.poll() is not None:raise AssertionError('SSH interactive missing '+repr(शो_मान)+' '+repr(bytes(대화기록)))
                    for प्रविष्टि_मान,_ in चयन_मान.select(.1):
                        조각=प्रविष्टि_मान.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                अन्तरक्रियाशील_सत्र.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');अन्तरक्रियाशील_सत्र.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                अन्तरक्रियाशील_सत्र.stdin.write(b'\x04');अन्तरक्रियाशील_सत्र.stdin.flush();나머지,त्रुटि=अन्तरक्रियाशील_सत्र.communicate(timeout=15)
                assert अन्तरक्रियाशील_सत्र.returncode==0 and b'PTY allocation request failed' not in त्रुटि,(अन्तरक्रियाशील_सत्र.returncode,त्रुटि)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                चयन_मान.close()
                if अन्तरक्रियाशील_सत्र.poll() is None:अन्तरक्रियाशील_सत्र.kill();अन्तरक्रियाशील_सत्र.wait()
            रिपोर्ट_मान['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(जडान, 수):
                लगत=bytearray()
                while len(लगत)<수:
                    덩이=जडान.recv(수-len(लगत))
                    if not 덩이: raise AssertionError('RFB EOF')
                    लगत.extend(덩이)
                return bytes(लगत)
            def 화면인증(पासवर्ड_मान):
                जडान=socket.create_connection(('127.0.0.5',화면포트),10);जडान.settimeout(30)
                assert 정확히(जडान,12)==b'RFB 003.008\n'
                जडान.sendall(b'RFB 003.008\n');assert 정확히(जडान,2)==b'\x01\x02'
                जडान.sendall(b'\x02');चुनौती_मान=정확히(जडान,16)
                입력암호=पासवर्ड_मान.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                जडान.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(चुनौती_मान))
                स्थिति_मान=struct.unpack('!I',정확히(जडान,4))[0]
                return जडान,स्थिति_मान
            अवैधानिक_पासवर्ड='!' if not सेटिङ['vnc_password'].startswith('!') else '?'
            जडान,स्थिति_मान=화면인증(अवैधानिक_पासवर्ड);assert स्थिति_मान==1;जडान.close();time.sleep(.6)
            रिपोर्ट_मान['checks'].append('VNC incorrect password rejected')
            जडान,स्थिति_मान=화면인증(सेटिङ['vnc_password']);assert स्थिति_मान==0
            with जडान:
                जडान.sendall(b'\x01');초기=정확히(जडान,24);너비,높이=struct.unpack('!HH',초기[:4]);नाम=정확히(जडान,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==नाम
                def 화면(증분=0):
                    जडान.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(जडान,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    चित्रकारी_मान=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_समन्वय,세로좌표,영역너비,영역높이,तरिका_मोड=struct.unpack('!HHHHi',정확히(जडान,12));assert तरिका_मोड==0 and x_समन्वय+영역너비<=너비 and 세로좌표+영역높이<=높이
                        पेल=정확히(जडान,영역너비*영역높이*4);합계+=len(पेल)
                        for रेखा in range(영역높이):चित्रकारी_मान[((세로좌표+रेखा)*너비+x_समन्वय)*4:((세로좌표+रेखा)*너비+x_समन्वय+영역너비)*4]=पेल[रेखा*영역너비*4:(रेखा+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(चित्रकारी_मान),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                रिपोर्ट_मान['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                रिपोर्ट_मान['checks'].append('RFB incremental update')
                처음=len(लग_रेकर्ड)
                for वर्ण_मान in 'echo VNC_NATIVE_PASS\r':
                    चिन्ह=0xff0d if वर्ण_मान=='\r' else ord(वर्ण_मान)
                    जडान.sendall(struct.pack('!BBHI',4,1,0,चिन्ह));जडान.sendall(struct.pack('!BBHI',4,0,0,चिन्ह))
                기다림(b'VNC_NATIVE_PASS',처음)
                रिपोर्ट_मान['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(चिन्ह,누름=1):जडान.sendall(struct.pack('!BBHI',4,누름,0,चिन्ह))
                처음=len(लग_रेकर्ड)
                for वर्ण_मान in 'echo ':글쇠(ord(वर्ण_मान))
                글쇠(0xffc6)
                for वर्ण_मान in 'gksrmf':글쇠(ord(वर्ण_मान))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                रिपोर्ट_मान['checks'].append('Native VNC F9 two-set Hangul composition')
                जडान.sendall(struct.pack('!BBHH',5,0,120,100))
                रिपोर्ट_मान['checks'].append('VNC pointer input accepted')
            प्रक्रिया_मान.stdin.write(b'poweroff\n');प्रक्रिया_मान.stdin.flush();प्रक्रिया_मान.wait(timeout=15);assert प्रक्रिया_मान.returncode==0
            रिपोर्ट_मान['passed']=True
    finally:
        if प्रक्रिया_मान and प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try: प्रक्रिया_मान.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
        (출력/'serial.log').write_bytes(लग_रेकर्ड)
        (출력/'report.json').write_text(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(रिपोर्ट_मान,ensure_ascii=False,indent=2))


if __name__=='__main__': चलाउनुहोस्()
