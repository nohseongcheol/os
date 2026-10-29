#!/usr/bin/env python3
"""стваран_подаци OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from 실행 import 기준, команда
from 통신다리 import 통신다리


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Подешавања = json.loads(인수.access.read_text())
    извјештај_вриједност = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as повезати:
            повезати.bind(('127.0.0.5', 0))
            return повезати.getsockname()[1]
    љуска_порт, 화면포트, фајл_порт = 빈포트(), 빈포트(), 빈포트()
    дневник_рада_ред = bytearray()
    процес_вриједност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(фајл_порт,
                ['tcp:{}:22'.format(љуска_порт), 'tcp:{}:5900'.format(화면포트)], хост_рачунар_адреса='127.0.0.5') as 다리:
            실행인수 = команда()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            процес_вриједност = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    подаци = процес_вриједност.stdout.read(4096)
                    if not подаци: break
                    дневник_рада_ред.extend(подаци)
            нит_вриједност = threading.Thread(target=수집, daemon=True)
            нит_вриједност.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in дневник_рада_ред[처음:]:
                    if time.monotonic()>끝 or процес_вриједност.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+дневник_рада_ред[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(лозинка_вриједност, програмска_наредба_вриједност, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=лозинка_вриједност
                인수=['ssh','-v']+list(추가)+['-p',str(љуска_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',програмска_наредба_вриједност]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + Подешавања['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in дневник_рада_ред, 결과.stderr
            извјештај_вриједност['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(Подешавања['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            извјештај_вриједност['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            извјештај_вриједност['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(Подешавања['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            извјештај_вриједност['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(Подешавања['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            извјештај_вриједност['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(Подешавања['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            извјештај_вриједност['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(љуска_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивно_сесија=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();избор_вриједност=selectors.DefaultSelector();избор_вриједност.register(интерактивно_сесија.stdout,selectors.EVENT_READ)
            def 대화읽기(приказати_вриједност):
                마감=time.monotonic()+30
                while приказати_вриједност not in 대화기록:
                    if time.monotonic()>마감 or интерактивно_сесија.poll() is not None:raise AssertionError('SSH interactive missing '+repr(приказати_вриједност)+' '+repr(bytes(대화기록)))
                    for унос_вриједност,_ in избор_вриједност.select(.1):
                        조각=унос_вриједност.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактивно_сесија.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивно_сесија.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивно_сесија.stdin.write(b'\x04');интерактивно_сесија.stdin.flush();나머지,грешка=интерактивно_сесија.communicate(timeout=15)
                assert интерактивно_сесија.returncode==0 and b'PTY allocation request failed' not in грешка,(интерактивно_сесија.returncode,грешка)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                избор_вриједност.close()
                if интерактивно_сесија.poll() is None:интерактивно_сесија.kill();интерактивно_сесија.wait()
            извјештај_вриједност['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(повезати, 수):
                подаци=bytearray()
                while len(подаци)<수:
                    덩이=повезати.recv(수-len(подаци))
                    if not 덩이: raise AssertionError('RFB EOF')
                    подаци.extend(덩이)
                return bytes(подаци)
            def 화면인증(лозинка_вриједност):
                повезати=socket.create_connection(('127.0.0.5',화면포트),10);повезати.settimeout(30)
                assert 정확히(повезати,12)==b'RFB 003.008\n'
                повезати.sendall(b'RFB 003.008\n');assert 정확히(повезати,2)==b'\x01\x02'
                повезати.sendall(b'\x02');도전=정확히(повезати,16)
                입력암호=лозинка_вриједност.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                повезати.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                стање_вриједност=struct.unpack('!I',정확히(повезати,4))[0]
                return повезати,стање_вриједност
            Неважећи_лозинка='!' if not Подешавања['vnc_password'].startswith('!') else '?'
            повезати,стање_вриједност=화면인증(Неважећи_лозинка);assert стање_вриједност==1;повезати.close();time.sleep(.6)
            извјештај_вриједност['checks'].append('VNC incorrect password rejected')
            повезати,стање_вриједност=화면인증(Подешавања['vnc_password']);assert стање_вриједност==0
            with повезати:
                повезати.sendall(b'\x01');초기=정확히(повезати,24);너비,높이=struct.unpack('!HH',초기[:4]);назив=정확히(повезати,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==назив
                def 화면(증분=0):
                    повезати.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(повезати,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    уцртавање_вриједност=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(повезати,12));assert 방식==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        Пел=정확히(повезати,영역너비*영역높이*4);합계+=len(Пел)
                        for редак in range(영역높이):уцртавање_вриједност[((세로좌표+редак)*너비+가로좌표)*4:((세로좌표+редак)*너비+가로좌표+영역너비)*4]=Пел[редак*영역너비*4:(редак+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(уцртавање_вриједност),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                извјештај_вриједност['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                извјештај_вриједност['checks'].append('RFB incremental update')
                처음=len(дневник_рада_ред)
                for знак_вриједност in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if знак_вриједност=='\r' else ord(знак_вриједност)
                    повезати.sendall(struct.pack('!BBHI',4,1,0,기호));повезати.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                извјештај_вриједност['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):повезати.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(дневник_рада_ред)
                for знак_вриједност in 'echo ':글쇠(ord(знак_вриједност))
                글쇠(0xffc6)
                for знак_вриједност in 'gksrmf':글쇠(ord(знак_вриједност))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                извјештај_вриједност['checks'].append('Native VNC F9 two-set Hangul composition')
                повезати.sendall(struct.pack('!BBHH',5,0,120,100))
                извјештај_вриједност['checks'].append('VNC pointer input accepted')
            процес_вриједност.stdin.write(b'poweroff\n');процес_вриједност.stdin.flush();процес_вриједност.wait(timeout=15);assert процес_вриједност.returncode==0
            извјештај_вриједност['passed']=True
    finally:
        if процес_вриједност and процес_вриједност.poll() is None:
            процес_вриједност.terminate()
            try: процес_вриједност.wait(timeout=5)
            except subprocess.TimeoutExpired: процес_вриједност.kill();процес_вриједност.wait()
        (출력/'serial.log').write_bytes(дневник_рада_ред)
        (출력/'report.json').write_text(json.dumps(извјештај_вриједност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(извјештај_вриједност,ensure_ascii=False,indent=2))


if __name__=='__main__': 시작()
