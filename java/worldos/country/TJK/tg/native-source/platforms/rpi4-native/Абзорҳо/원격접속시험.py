#!/usr/bin/env python3
"""воқеӣ_иттилоот OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from иҷро_кардан_фармон import 기준, фармон
from Шабака_кӯпрук import Шабака_кӯпрук


def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Танзимот = json.loads(인수.access.read_text())
    гузориш_қимат = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def холӣ_порт():
        with socket.socket() as ПАЙВАСТ:
            ПАЙВАСТ.bind(('127.0.0.5', 0))
            return ПАЙВАСТ.getsockname()[1]
    восит_порт, 화면포트, файл_порт = холӣ_порт(), холӣ_порт(), холӣ_порт()
    сабт_кардан_сабт = bytearray()
    Раванд_қимат = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Шабака_кӯпрук(файл_порт,
                ['tcp:{}:22'.format(восит_порт), 'tcp:{}:5900'.format(화면포트)], мизбон_суроға='127.0.0.5') as кӯпрук_қимат:
            실행인수 = фармон()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Раванд_қимат = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + кӯпрук_қимат.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    иттилоот = Раванд_қимат.stdout.read(4096)
                    if not иттилоот: break
                    сабт_кардан_сабт.extend(иттилоот)
            ришта_қимат = threading.Thread(target=수집, daemon=True)
            ришта_қимат.start()
            def 기다림(Калимабозӣ_Матн, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Калимабозӣ_Матн not in сабт_кардан_сабт[처음:]:
                    if time.monotonic()>끝 or Раванд_қимат.poll() is not None:
                        raise AssertionError('Missing '+repr(Калимабозӣ_Матн)+'\n'+сабт_кардан_сабт[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def эмин_восит(парол_қимат, дастур_қимат, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=парол_қимат
                인수=['ssh','-v']+list(추가)+['-p',str(восит_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',дастур_қимат]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=эмин_восит('!' + Танзимот['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in сабт_кардан_сабт, 결과.stderr
            гузориш_қимат['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=эмин_восит(Танзимот['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            гузориш_қимат['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            гузориш_қимат['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=эмин_восит(Танзимот['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            гузориш_қимат['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=эмин_восит(Танзимот['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            гузориш_қимат['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=эмин_восит(Танзимот['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            гузориш_қимат['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(восит_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивӣ_сессия=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();интихоб_қимат=selectors.DefaultSelector();интихоб_қимат.register(интерактивӣ_сессия.stdout,selectors.EVENT_READ)
            def 대화읽기(намоиш_додан_қимат):
                마감=time.monotonic()+30
                while намоиш_додан_қимат not in 대화기록:
                    if time.monotonic()>마감 or интерактивӣ_сессия.poll() is not None:raise AssertionError('SSH interactive missing '+repr(намоиш_додан_қимат)+' '+repr(bytes(대화기록)))
                    for ворида_қимат,_ in интихоб_қимат.select(.1):
                        조각=ворида_қимат.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактивӣ_сессия.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивӣ_сессия.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивӣ_сессия.stdin.write(b'\x04');интерактивӣ_сессия.stdin.flush();나머지,Хато=интерактивӣ_сессия.communicate(timeout=15)
                assert интерактивӣ_сессия.returncode==0 and b'PTY allocation request failed' not in Хато,(интерактивӣ_сессия.returncode,Хато)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                интихоб_қимат.close()
                if интерактивӣ_сессия.poll() is None:интерактивӣ_сессия.kill();интерактивӣ_сессия.wait()
            гузориш_қимат['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ПАЙВАСТ, 수):
                иттилоот=bytearray()
                while len(иттилоот)<수:
                    덩이=ПАЙВАСТ.recv(수-len(иттилоот))
                    if not 덩이: raise AssertionError('RFB EOF')
                    иттилоот.extend(덩이)
                return bytes(иттилоот)
            def 화면인증(парол_қимат):
                ПАЙВАСТ=socket.create_connection(('127.0.0.5',화면포트),10);ПАЙВАСТ.settimeout(30)
                assert 정확히(ПАЙВАСТ,12)==b'RFB 003.008\n'
                ПАЙВАСТ.sendall(b'RFB 003.008\n');assert 정확히(ПАЙВАСТ,2)==b'\x01\x02'
                ПАЙВАСТ.sendall(b'\x02');санҷиши_амният_қимат=정확히(ПАЙВАСТ,16)
                입력암호=парол_қимат.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ПАЙВАСТ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(санҷиши_амният_қимат))
                вазъият_қимат=struct.unpack('!I',정확히(ПАЙВАСТ,4))[0]
                return ПАЙВАСТ,вазъият_қимат
            беэътибор_парол='!' if not Танзимот['vnc_password'].startswith('!') else '?'
            ПАЙВАСТ,вазъият_қимат=화면인증(беэътибор_парол);assert вазъият_қимат==1;ПАЙВАСТ.close();time.sleep(.6)
            гузориш_қимат['checks'].append('VNC incorrect password rejected')
            ПАЙВАСТ,вазъият_қимат=화면인증(Танзимот['vnc_password']);assert вазъият_қимат==0
            with ПАЙВАСТ:
                ПАЙВАСТ.sendall(b'\x01');초기=정확히(ПАЙВАСТ,24);너비,높이=struct.unpack('!HH',초기[:4]);Ном=정확히(ПАЙВАСТ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ном
                def 화면(증분=0):
                    ПАЙВАСТ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ПАЙВАСТ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    нақша_қимат=bytearray(너비*높이*4)
                    for _ in range(수):
                        координатаи_х,세로좌표,영역너비,영역높이,сабк_ҳолат=struct.unpack('!HHHHi',정확히(ПАЙВАСТ,12));assert сабк_ҳолат==0 and координатаи_х+영역너비<=너비 and 세로좌표+영역높이<=높이
                        пиксел=정확히(ПАЙВАСТ,영역너비*영역높이*4);합계+=len(пиксел)
                        for хат in range(영역높이):нақша_қимат[((세로좌표+хат)*너비+координатаи_х)*4:((세로좌표+хат)*너비+координатаи_х+영역너비)*4]=пиксел[хат*영역너비*4:(хат+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(нақша_қимат),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                гузориш_қимат['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                гузориш_қимат['checks'].append('RFB incremental update')
                처음=len(сабт_кардан_сабт)
                for аломат_қимат_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    аломат=0xff0d if аломат_қимат_068c2631=='\r' else ord(аломат_қимат_068c2631)
                    ПАЙВАСТ.sendall(struct.pack('!BBHI',4,1,0,аломат));ПАЙВАСТ.sendall(struct.pack('!BBHI',4,0,0,аломат))
                기다림(b'VNC_NATIVE_PASS',처음)
                гузориш_қимат['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(аломат,누름=1):ПАЙВАСТ.sendall(struct.pack('!BBHI',4,누름,0,аломат))
                처음=len(сабт_кардан_сабт)
                for аломат_қимат_068c2631 in 'echo ':글쇠(ord(аломат_қимат_068c2631))
                글쇠(0xffc6)
                for аломат_қимат_068c2631 in 'gksrmf':글쇠(ord(аломат_қимат_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                гузориш_қимат['checks'].append('Native VNC F9 two-set Hangul composition')
                ПАЙВАСТ.sendall(struct.pack('!BBHH',5,0,120,100))
                гузориш_қимат['checks'].append('VNC pointer input accepted')
            Раванд_қимат.stdin.write(b'poweroff\n');Раванд_қимат.stdin.flush();Раванд_қимат.wait(timeout=15);assert Раванд_қимат.returncode==0
            гузориш_қимат['passed']=True
    finally:
        if Раванд_қимат and Раванд_қимат.poll() is None:
            Раванд_қимат.terminate()
            try: Раванд_қимат.wait(timeout=5)
            except subprocess.TimeoutExpired: Раванд_қимат.kill();Раванд_қимат.wait()
        (출력/'serial.log').write_bytes(сабт_кардан_сабт)
        (출력/'report.json').write_text(json.dumps(гузориш_қимат,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(гузориш_қимат,ensure_ascii=False,indent=2))


if __name__=='__main__': порча()
