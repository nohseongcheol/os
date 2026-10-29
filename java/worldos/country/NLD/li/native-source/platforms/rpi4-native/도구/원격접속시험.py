#!/usr/bin/env python3
"""실제 OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from 실행 import 기준, 명령
from 통신다리 import 통신다리


def Oetveure():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Insjtèllinge = json.loads(인수.access.read_text())
    보고 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Verbènje:
            Verbènje.bind(('127.0.0.5', 0))
            return Verbènje.getsockname()[1]
    셸포트, 화면포트, 파일포트 = 빈포트(), 빈포트(), 빈포트()
    기록 = bytearray()
    과정 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(파일포트,
                ['tcp:{}:22'.format(셸포트), 'tcp:{}:5900'.format(화면포트)], 호스트주소='127.0.0.5') as 다리:
            실행인수 = 명령()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            과정 = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    자료 = 과정.stdout.read(4096)
                    if not 자료: break
                    기록.extend(자료)
            가닥 = threading.Thread(target=수집, daemon=True)
            가닥.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in 기록[처음:]:
                    if time.monotonic()>끝 or 과정.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+기록[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(암호, 명령어, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=암호
                인수=['ssh','-v']+list(추가)+['-p',str(셸포트),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + Insjtèllinge['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in 기록, 결과.stderr
            보고['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(Insjtèllinge['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            보고['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            보고['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(Insjtèllinge['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            보고['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(Insjtèllinge['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            보고['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(Insjtèllinge['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            보고['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(셸포트),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();선택=selectors.DefaultSelector();선택.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(표시):
                마감=time.monotonic()+30
                while 표시 not in 대화기록:
                    if time.monotonic()>마감 or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(표시)+' '+repr(bytes(대화기록)))
                    for 항목,_ in 선택.select(.1):
                        조각=항목.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,Faeler=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in Faeler,(대화.returncode,Faeler)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                선택.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            보고['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Verbènje, 수):
                자료=bytearray()
                while len(자료)<수:
                    덩이=Verbènje.recv(수-len(자료))
                    if not 덩이: raise AssertionError('RFB EOF')
                    자료.extend(덩이)
                return bytes(자료)
            def 화면인증(암호):
                Verbènje=socket.create_connection(('127.0.0.5',화면포트),10);Verbènje.settimeout(30)
                assert 정확히(Verbènje,12)==b'RFB 003.008\n'
                Verbènje.sendall(b'RFB 003.008\n');assert 정확히(Verbènje,2)==b'\x01\x02'
                Verbènje.sendall(b'\x02');도전=정확히(Verbènje,16)
                입력암호=암호.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Verbènje.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                상태=struct.unpack('!I',정확히(Verbènje,4))[0]
                return Verbènje,상태
            잘못된암호='!' if not Insjtèllinge['vnc_password'].startswith('!') else '?'
            Verbènje,상태=화면인증(잘못된암호);assert 상태==1;Verbènje.close();time.sleep(.6)
            보고['checks'].append('VNC incorrect password rejected')
            Verbènje,상태=화면인증(Insjtèllinge['vnc_password']);assert 상태==0
            with Verbènje:
                Verbènje.sendall(b'\x01');초기=정확히(Verbènje,24);너비,높이=struct.unpack('!HH',초기[:4]);Naam=정확히(Verbènje,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Naam
                def 화면(증분=0):
                    Verbènje.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Verbènje,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    그림=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(Verbènje,12));assert 방식==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        화소=정확히(Verbènje,영역너비*영역높이*4);합계+=len(화소)
                        for 줄 in range(영역높이):그림[((세로좌표+줄)*너비+가로좌표)*4:((세로좌표+줄)*너비+가로좌표+영역너비)*4]=화소[줄*영역너비*4:(줄+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(그림),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                보고['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                보고['checks'].append('RFB incremental update')
                처음=len(기록)
                for 글자 in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if 글자=='\r' else ord(글자)
                    Verbènje.sendall(struct.pack('!BBHI',4,1,0,기호));Verbènje.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                보고['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):Verbènje.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(기록)
                for 글자 in 'echo ':글쇠(ord(글자))
                글쇠(0xffc6)
                for 글자 in 'gksrmf':글쇠(ord(글자))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                보고['checks'].append('Native VNC F9 two-set Hangul composition')
                Verbènje.sendall(struct.pack('!BBHH',5,0,120,100))
                보고['checks'].append('VNC pointer input accepted')
            과정.stdin.write(b'poweroff\n');과정.stdin.flush();과정.wait(timeout=15);assert 과정.returncode==0
            보고['passed']=True
    finally:
        if 과정 and 과정.poll() is None:
            과정.terminate()
            try: 과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 과정.kill();과정.wait()
        (출력/'serial.log').write_bytes(기록)
        (출력/'report.json').write_text(json.dumps(보고,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(보고,ensure_ascii=False,indent=2))


if __name__=='__main__': Oetveure()
