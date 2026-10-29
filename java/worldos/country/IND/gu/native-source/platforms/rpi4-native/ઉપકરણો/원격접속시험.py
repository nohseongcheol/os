#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ, આદેશ
from નેટવર્ક_બ્રિજ import નેટવર્ક_બ્રિજ


def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=પ્રોજેક્ટ_રૂટ / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=પ્રોજેક્ટ_રૂટ / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=પ્રોજેક્ટ_રૂટ / 'build/verification/native-remote')
    દલીલો = 해석기.parse_args()
    આઉટપુટ = દલીલો.output
    આઉટપુટ.mkdir(parents=True, exist_ok=True)
    સુયોજના = json.loads(દલીલો.access.read_text())
    અહેવાલ_મૂલ્ય = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(દલીલો.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ખાલી_પૉર્ટ():
        with socket.socket() as સંપર્ક_કરો:
            સંપર્ક_કરો.bind(('127.0.0.5', 0))
            return સંપર્ક_કરો.getsockname()[1]
    શેલ_પૉર્ટ, 화면포트, ફાઇલ_પૉર્ટ = ખાલી_પૉર્ટ(), ખાલી_પૉર્ટ(), ખાલી_પૉર્ટ()
    લૉગ_પંક્તિ = bytearray()
    પ્રક્રિયા_મૂલ્ય = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, નેટવર્ક_બ્રિજ(ફાઇલ_પૉર્ટ,
                ['tcp:{}:22'.format(શેલ_પૉર્ટ), 'tcp:{}:5900'.format(화면포트)], હોસ્ટ_સરનામું='127.0.0.5') as બ્રિજ_મૂલ્ય:
            실행인수 = આદેશ()
            실행인수[실행인수.index('-kernel') + 1] = str(દલીલો.kernel.resolve())
            પ્રક્રિયા_મૂલ્ય = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + બ્રિજ_મૂલ્ય.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ડેટા = પ્રક્રિયા_મૂલ્ય.stdout.read(4096)
                    if not ડેટા: break
                    લૉગ_પંક્તિ.extend(ડેટા)
            થ્રેડ_મૂલ્ય = threading.Thread(target=수집, daemon=True)
            થ્રેડ_મૂલ્ય.start()
            def પ્રતીક્ષા_સ્થિતિ(શબ્દ_પાઠ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while શબ્દ_પાઠ not in લૉગ_પંક્તિ[처음:]:
                    if time.monotonic()>끝 or પ્રક્રિયા_મૂલ્ય.poll() is not None:
                        raise AssertionError('Missing '+repr(શબ્દ_પાઠ)+'\n'+લૉગ_પંક્તિ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            પ્રતીક્ષા_સ્થિતિ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def સુરક્ષિત_શેલ(પાસવર્ડ_મૂલ્ય, સૂચના_મૂલ્ય, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=પાસવર્ડ_મૂલ્ય
                દલીલો=['ssh','-v']+list(추가)+['-p',str(શેલ_પૉર્ટ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',સૂચના_મૂલ્ય]
                પરિમાણ=subprocess.run(દલીલો,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return પરિમાણ
            પરિમાણ=સુરક્ષિત_શેલ('!' + સુયોજના['ssh_password'], 'echo SHOULD_NOT_RUN')
            (આઉટપુટ/'ssh-rejected.log').write_bytes(પરિમાણ.stderr)
            assert પરિમાણ.returncode!=0 and b'Permission denied' in પરિમાણ.stderr and b'SHOULD_NOT_RUN' not in લૉગ_પંક્તિ, પરિમાણ.stderr
            અહેવાલ_મૂલ્ય['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            પરિમાણ=સુરક્ષિત_શેલ(સુયોજના['ssh_password'], 'echo SSH_NATIVE_PASS')
            (આઉટપુટ/'ssh.log').write_bytes(પરિમાણ.stderr)
            (આઉટપુટ/'ssh-output.txt').write_bytes(પરિમાણ.stdout)
            assert પરિમાણ.returncode==0 and b'SSH_NATIVE_PASS' in પરિમાણ.stdout, (પરિમાણ.returncode,પરિમાણ.stdout,પરિમાણ.stderr)
            અહેવાલ_મૂલ્ય['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in પરિમાણ.stderr, પરિમાણ.stderr
            અહેવાલ_મૂલ્ય['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            પરિમાણ=સુરક્ષિત_શેલ(સુયોજના['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert પરિમાણ.returncode==0 and 'JAVA આઉટપુટ: 안녕하세요 😀'.encode() in પરિમાણ.stdout,પરિમાણ.stdout
            અહેવાલ_મૂલ્ય['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            પરિમાણ=સુરક્ષિત_શેલ(સુયોજના['ssh_password'], 'missing_remote_command')
            assert પરિમાણ.returncode==127,પરિમાણ.returncode
            અહેવાલ_મૂલ્ય['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            પરિમાણ=સુરક્ષિત_શેલ(સુયોજના['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (આઉટપુટ/'ssh-rekey.log').write_bytes(પરિમાણ.stderr)
            assert પરિમાણ.returncode==0 and 'class 창예제'.encode() in પરિમાણ.stdout, (પરિમાણ.returncode,પરિમાણ.stdout,પરિમાણ.stderr)
            assert પરિમાણ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, પરિમાણ.stderr
            અહેવાલ_મૂલ્ય['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(શેલ_પૉર્ટ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            સહભાગી_સત્ર=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ચયન_મૂલ્ય=selectors.DefaultSelector();ચયન_મૂલ્ય.register(સહભાગી_સત્ર.stdout,selectors.EVENT_READ)
            def 대화읽기(શૉ_મૂલ્ય):
                마감=time.monotonic()+30
                while શૉ_મૂલ્ય not in 대화기록:
                    if time.monotonic()>마감 or સહભાગી_સત્ર.poll() is not None:raise AssertionError('SSH interactive missing '+repr(શૉ_મૂલ્ય)+' '+repr(bytes(대화기록)))
                    for પ્રવેશ_મૂલ્ય,_ in ચયન_મૂલ્ય.select(.1):
                        조각=પ્રવેશ_મૂલ્ય.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                સહભાગી_સત્ર.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');સહભાગી_સત્ર.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                સહભાગી_સત્ર.stdin.write(b'\x04');સહભાગી_સત્ર.stdin.flush();나머지,ભૂલ=સહભાગી_સત્ર.communicate(timeout=15)
                assert સહભાગી_સત્ર.returncode==0 and b'PTY allocation request failed' not in ભૂલ,(સહભાગી_સત્ર.returncode,ભૂલ)
                (આઉટપુટ/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ચયન_મૂલ્ય.close()
                if સહભાગી_સત્ર.poll() is None:સહભાગી_સત્ર.kill();સહભાગી_સત્ર.wait()
            અહેવાલ_મૂલ્ય['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(સંપર્ક_કરો, 수):
                ડેટા=bytearray()
                while len(ડેટા)<수:
                    덩이=સંપર્ક_કરો.recv(수-len(ડેટા))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ડેટા.extend(덩이)
                return bytes(ડેટા)
            def 화면인증(પાસવર્ડ_મૂલ્ય):
                સંપર્ક_કરો=socket.create_connection(('127.0.0.5',화면포트),10);સંપર્ક_કરો.settimeout(30)
                assert 정확히(સંપર્ક_કરો,12)==b'RFB 003.008\n'
                સંપર્ક_કરો.sendall(b'RFB 003.008\n');assert 정확히(સંપર્ક_કરો,2)==b'\x01\x02'
                સંપર્ક_કરો.sendall(b'\x02');ચેલેન્જ_મૂલ્ય=정확히(સંપર્ક_કરો,16)
                입력암호=પાસવર્ડ_મૂલ્ય.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                સંપર્ક_કરો.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ચેલેન્જ_મૂલ્ય))
                સ્થિતિ_મૂલ્ય_e10195a1=struct.unpack('!I',정확히(સંપર્ક_કરો,4))[0]
                return સંપર્ક_કરો,સ્થિતિ_મૂલ્ય_e10195a1
            અમાન્ય_પાસવર્ડ='!' if not સુયોજના['vnc_password'].startswith('!') else '?'
            સંપર્ક_કરો,સ્થિતિ_મૂલ્ય_e10195a1=화면인증(અમાન્ય_પાસવર્ડ);assert સ્થિતિ_મૂલ્ય_e10195a1==1;સંપર્ક_કરો.close();time.sleep(.6)
            અહેવાલ_મૂલ્ય['checks'].append('VNC incorrect password rejected')
            સંપર્ક_કરો,સ્થિતિ_મૂલ્ય_e10195a1=화면인증(સુયોજના['vnc_password']);assert સ્થિતિ_મૂલ્ય_e10195a1==0
            with સંપર્ક_કરો:
                સંપર્ક_કરો.sendall(b'\x01');초기=정확히(સંપર્ક_કરો,24);너비,높이=struct.unpack('!HH',초기[:4]);નામ=정확히(સંપર્ક_કરો,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==નામ
                def 화면(증분=0):
                    સંપર્ક_કરો.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(સંપર્ક_કરો,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    રેખાંકન_મૂલ્ય=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_યામ,세로좌표,영역너비,영역높이,પદ્ધતિ_મોડ=struct.unpack('!HHHHi',정확히(સંપર્ક_કરો,12));assert પદ્ધતિ_મોડ==0 and x_યામ+영역너비<=너비 and 세로좌표+영역높이<=높이
                        પેલ=정확히(સંપર્ક_કરો,영역너비*영역높이*4);합계+=len(પેલ)
                        for લાઇન in range(영역높이):રેખાંકન_મૂલ્ય[((세로좌표+લાઇન)*너비+x_યામ)*4:((세로좌표+લાઇન)*너비+x_યામ+영역너비)*4]=પેલ[લાઇન*영역너비*4:(લાઇન+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(રેખાંકન_મૂલ્ય),'raw','BGRX').save(str(આઉટપુટ/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                અહેવાલ_મૂલ્ય['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                અહેવાલ_મૂલ્ય['checks'].append('RFB incremental update')
                처음=len(લૉગ_પંક્તિ)
                for વર્ણ_મૂલ્ય in 'echo VNC_NATIVE_PASS\r':
                    પ્રતીક=0xff0d if વર્ણ_મૂલ્ય=='\r' else ord(વર્ણ_મૂલ્ય)
                    સંપર્ક_કરો.sendall(struct.pack('!BBHI',4,1,0,પ્રતીક));સંપર્ક_કરો.sendall(struct.pack('!BBHI',4,0,0,પ્રતીક))
                પ્રતીક્ષા_સ્થિતિ(b'VNC_NATIVE_PASS',처음)
                અહેવાલ_મૂલ્ય['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(પ્રતીક,누름=1):સંપર્ક_કરો.sendall(struct.pack('!BBHI',4,누름,0,પ્રતીક))
                처음=len(લૉગ_પંક્તિ)
                for વર્ણ_મૂલ્ય in 'echo ':글쇠(ord(વર્ણ_મૂલ્ય))
                글쇠(0xffc6)
                for વર્ણ_મૂલ્ય in 'gksrmf':글쇠(ord(વર્ણ_મૂલ્ય))
                글쇠(0xffc6);글쇠(0xff0d)
                પ્રતીક્ષા_સ્થિતિ('\r\n한글\r\n'.encode(),처음)
                અહેવાલ_મૂલ્ય['checks'].append('Native VNC F9 two-set Hangul composition')
                સંપર્ક_કરો.sendall(struct.pack('!BBHH',5,0,120,100))
                અહેવાલ_મૂલ્ય['checks'].append('VNC pointer input accepted')
            પ્રક્રિયા_મૂલ્ય.stdin.write(b'poweroff\n');પ્રક્રિયા_મૂલ્ય.stdin.flush();પ્રક્રિયા_મૂલ્ય.wait(timeout=15);assert પ્રક્રિયા_મૂલ્ય.returncode==0
            અહેવાલ_મૂલ્ય['passed']=True
    finally:
        if પ્રક્રિયા_મૂલ્ય and પ્રક્રિયા_મૂલ્ય.poll() is None:
            પ્રક્રિયા_મૂલ્ય.terminate()
            try: પ્રક્રિયા_મૂલ્ય.wait(timeout=5)
            except subprocess.TimeoutExpired: પ્રક્રિયા_મૂલ્ય.kill();પ્રક્રિયા_મૂલ્ય.wait()
        (આઉટપુટ/'serial.log').write_bytes(લૉગ_પંક્તિ)
        (આઉટપુટ/'report.json').write_text(json.dumps(અહેવાલ_મૂલ્ય,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(અહેવાલ_મૂલ્ય,ensure_ascii=False,indent=2))


if __name__=='__main__': ચલાવો_2()
