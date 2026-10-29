#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश
from नॅटवर्क_ब्रिज import नॅटवर्क_ब्रिज


def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=प्रॉजॅक्ट_रूट / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=प्रॉजॅक्ट_रूट / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=प्रॉजॅक्ट_रूट / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    मांडावळी = json.loads(인수.access.read_text())
    अहवाल_मोल = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def रिकामें_पोर्ट():
        with socket.socket() as कनॅक्ट:
            कनॅक्ट.bind(('127.0.0.5', 0))
            return कनॅक्ट.getsockname()[1]
    शॅल_पोर्ट, 화면포트, फायल_पोर्ट = रिकामें_पोर्ट(), रिकामें_पोर्ट(), रिकामें_पोर्ट()
    LOG_नोंद = bytearray()
    प्रक्रिया_मोल = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, नॅटवर्क_ब्रिज(फायल_पोर्ट,
                ['tcp:{}:22'.format(शॅल_पोर्ट), 'tcp:{}:5900'.format(화면포트)], येजमान_नामो='127.0.0.5') as ब्रिज_मोल:
            실행인수 = आदेश()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            प्रक्रिया_मोल = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ब्रिज_मोल.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    डेटा = प्रक्रिया_मोल.stdout.read(4096)
                    if not डेटा: break
                    LOG_नोंद.extend(डेटा)
            थ्रॅड_मोल = threading.Thread(target=수집, daemon=True)
            थ्रॅड_मोल.start()
            def 기다림(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_नोंद[처음:]:
                    if time.monotonic()>끝 or प्रक्रिया_मोल.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_नोंद[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def सुरक्षीत_शॅल(पासवर्ड_मोल, समजावणी_मोल, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=पासवर्ड_मोल
                인수=['ssh','-v']+list(추가)+['-p',str(शॅल_पोर्ट),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',समजावणी_मोल]
                मेजप=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return मेजप
            मेजप=सुरक्षीत_शॅल('!' + मांडावळी['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(मेजप.stderr)
            assert मेजप.returncode!=0 and b'Permission denied' in मेजप.stderr and b'SHOULD_NOT_RUN' not in LOG_नोंद, मेजप.stderr
            अहवाल_मोल['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            मेजप=सुरक्षीत_शॅल(मांडावळी['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(मेजप.stderr)
            (출력/'ssh-output.txt').write_bytes(मेजप.stdout)
            assert मेजप.returncode==0 and b'SSH_NATIVE_PASS' in मेजप.stdout, (मेजप.returncode,मेजप.stdout,मेजप.stderr)
            अहवाल_मोल['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in मेजप.stderr, मेजप.stderr
            अहवाल_मोल['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            मेजप=सुरक्षीत_शॅल(मांडावळी['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert मेजप.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in मेजप.stdout,मेजप.stdout
            अहवाल_मोल['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            मेजप=सुरक्षीत_शॅल(मांडावळी['ssh_password'], 'missing_remote_command')
            assert मेजप.returncode==127,मेजप.returncode
            अहवाल_मोल['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            मेजप=सुरक्षीत_शॅल(मांडावळी['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(मेजप.stderr)
            assert मेजप.returncode==0 and 'class 창예제'.encode() in मेजप.stdout, (मेजप.returncode,मेजप.stdout,मेजप.stderr)
            assert मेजप.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, मेजप.stderr
            अहवाल_मोल['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(शॅल_पोर्ट),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            परस्पर_संवादी_सत्र=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();निवड_मोल=selectors.DefaultSelector();निवड_मोल.register(परस्पर_संवादी_सत्र.stdout,selectors.EVENT_READ)
            def 대화읽기(शो_मोल):
                마감=time.monotonic()+30
                while शो_मोल not in 대화기록:
                    if time.monotonic()>마감 or परस्पर_संवादी_सत्र.poll() is not None:raise AssertionError('SSH interactive missing '+repr(शो_मोल)+' '+repr(bytes(대화기록)))
                    for प्रवेश_मोल,_ in निवड_मोल.select(.1):
                        조각=प्रवेश_मोल.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                परस्पर_संवादी_सत्र.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');परस्पर_संवादी_सत्र.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                परस्पर_संवादी_सत्र.stdin.write(b'\x04');परस्पर_संवादी_सत्र.stdin.flush();나머지,चूक=परस्पर_संवादी_सत्र.communicate(timeout=15)
                assert परस्पर_संवादी_सत्र.returncode==0 and b'PTY allocation request failed' not in चूक,(परस्पर_संवादी_सत्र.returncode,चूक)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                निवड_मोल.close()
                if परस्पर_संवादी_सत्र.poll() is None:परस्पर_संवादी_सत्र.kill();परस्पर_संवादी_सत्र.wait()
            अहवाल_मोल['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(कनॅक्ट, 수):
                डेटा=bytearray()
                while len(डेटा)<수:
                    덩이=कनॅक्ट.recv(수-len(डेटा))
                    if not 덩이: raise AssertionError('RFB EOF')
                    डेटा.extend(덩이)
                return bytes(डेटा)
            def 화면인증(पासवर्ड_मोल):
                कनॅक्ट=socket.create_connection(('127.0.0.5',화면포트),10);कनॅक्ट.settimeout(30)
                assert 정확히(कनॅक्ट,12)==b'RFB 003.008\n'
                कनॅक्ट.sendall(b'RFB 003.008\n');assert 정확히(कनॅक्ट,2)==b'\x01\x02'
                कनॅक्ट.sendall(b'\x02');आव्हान_मोल=정확히(कनॅक्ट,16)
                입력암호=पासवर्ड_मोल.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                कनॅक्ट.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(आव्हान_मोल))
                स्थिती_मोल_e10195a1=struct.unpack('!I',정확히(कनॅक्ट,4))[0]
                return कनॅक्ट,स्थिती_मोल_e10195a1
            अवैध_पासवर्ड='!' if not मांडावळी['vnc_password'].startswith('!') else '?'
            कनॅक्ट,स्थिती_मोल_e10195a1=화면인증(अवैध_पासवर्ड);assert स्थिती_मोल_e10195a1==1;कनॅक्ट.close();time.sleep(.6)
            अहवाल_मोल['checks'].append('VNC incorrect password rejected')
            कनॅक्ट,स्थिती_मोल_e10195a1=화면인증(मांडावळी['vnc_password']);assert स्थिती_मोल_e10195a1==0
            with कनॅक्ट:
                कनॅक्ट.sendall(b'\x01');초기=정확히(कनॅक्ट,24);너비,높이=struct.unpack('!HH',초기[:4]);नांव=정확히(कनॅक्ट,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==नांव
                def 화면(증분=0):
                    कनॅक्ट.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(कनॅक्ट,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    रेखाटन_मोल=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_coordinate,세로좌표,영역너비,영역높이,पद्दत_मोड=struct.unpack('!HHHHi',정확히(कनॅक्ट,12));assert पद्दत_मोड==0 and x_coordinate+영역너비<=너비 and 세로좌표+영역높이<=높이
                        पिक्सॅल=정확히(कनॅक्ट,영역너비*영역높이*4);합계+=len(पिक्सॅल)
                        for रेग in range(영역높이):रेखाटन_मोल[((세로좌표+रेग)*너비+x_coordinate)*4:((세로좌표+रेग)*너비+x_coordinate+영역너비)*4]=पिक्सॅल[रेग*영역너비*4:(रेग+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(रेखाटन_मोल),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                अहवाल_मोल['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                अहवाल_मोल['checks'].append('RFB incremental update')
                처음=len(LOG_नोंद)
                for वर्ण_मोल in 'echo VNC_NATIVE_PASS\r':
                    चिन्न=0xff0d if वर्ण_मोल=='\r' else ord(वर्ण_मोल)
                    कनॅक्ट.sendall(struct.pack('!BBHI',4,1,0,चिन्न));कनॅक्ट.sendall(struct.pack('!BBHI',4,0,0,चिन्न))
                기다림(b'VNC_NATIVE_PASS',처음)
                अहवाल_मोल['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(चिन्न,누름=1):कनॅक्ट.sendall(struct.pack('!BBHI',4,누름,0,चिन्न))
                처음=len(LOG_नोंद)
                for वर्ण_मोल in 'echo ':글쇠(ord(वर्ण_मोल))
                글쇠(0xffc6)
                for वर्ण_मोल in 'gksrmf':글쇠(ord(वर्ण_मोल))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                अहवाल_मोल['checks'].append('Native VNC F9 two-set Hangul composition')
                कनॅक्ट.sendall(struct.pack('!BBHH',5,0,120,100))
                अहवाल_मोल['checks'].append('VNC pointer input accepted')
            प्रक्रिया_मोल.stdin.write(b'poweroff\n');प्रक्रिया_मोल.stdin.flush();प्रक्रिया_मोल.wait(timeout=15);assert प्रक्रिया_मोल.returncode==0
            अहवाल_मोल['passed']=True
    finally:
        if प्रक्रिया_मोल and प्रक्रिया_मोल.poll() is None:
            प्रक्रिया_मोल.terminate()
            try: प्रक्रिया_मोल.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया_मोल.kill();प्रक्रिया_मोल.wait()
        (출력/'serial.log').write_bytes(LOG_नोंद)
        (출력/'report.json').write_text(json.dumps(अहवाल_मोल,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(अहवाल_मोल,ensure_ascii=False,indent=2))


if __name__=='__main__': चलोवप()
