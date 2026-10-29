#!/usr/bin/env python3
"""фактик_мәгълүмат OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from үтәргә_команда import экранга_җибәрү_тамыр, команда
from Челтәр_күпер import Челтәр_күпер


def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=экранга_җибәрү_тамыр / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=экранга_җибәрү_тамыр / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=экранга_җибәрү_тамыр / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Caylaw = json.loads(인수.access.read_text())
    отчет_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def Буш_порт():
        with socket.socket() as ялгау:
            ялгау.bind(('127.0.0.5', 0))
            return ялгау.getsockname()[1]
    тышча_порт, 화면포트, файл_порт = Буш_порт(), Буш_порт(), Буш_порт()
    LOG_юл = bytearray()
    Процесс_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Челтәр_күпер(файл_порт,
                ['tcp:{}:22'.format(тышча_порт), 'tcp:{}:5900'.format(화면포트)], хост_адрес='127.0.0.5') as күпер_VALUE:
            실행인수 = команда()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Процесс_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + күпер_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    мәгълүмат = Процесс_VALUE.stdout.read(4096)
                    if not мәгълүмат: break
                    LOG_юл.extend(мәгълүмат)
            агым_VALUE_5b72a632 = threading.Thread(target=수집, daemon=True)
            агым_VALUE_5b72a632.start()
            def 기다림(Word_СМС, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_СМС not in LOG_юл[처음:]:
                    if time.monotonic()>끝 or Процесс_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_СМС)+'\n'+LOG_юл[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def имин_тышча(серсүз_VALUE, инструкция_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=серсүз_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(тышча_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',инструкция_VALUE]
                үлчәм=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return үлчәм
            үлчәм=имин_тышча('!' + Caylaw['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(үлчәм.stderr)
            assert үлчәм.returncode!=0 and b'Permission denied' in үлчәм.stderr and b'SHOULD_NOT_RUN' not in LOG_юл, үлчәм.stderr
            отчет_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            үлчәм=имин_тышча(Caylaw['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(үлчәм.stderr)
            (출력/'ssh-output.txt').write_bytes(үлчәм.stdout)
            assert үлчәм.returncode==0 and b'SSH_NATIVE_PASS' in үлчәм.stdout, (үлчәм.returncode,үлчәм.stdout,үлчәм.stderr)
            отчет_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in үлчәм.stderr, үлчәм.stderr
            отчет_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            үлчәм=имин_тышча(Caylaw['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert үлчәм.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in үлчәм.stdout,үлчәм.stdout
            отчет_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            үлчәм=имин_тышча(Caylaw['ssh_password'], 'missing_remote_command')
            assert үлчәм.returncode==127,үлчәм.returncode
            отчет_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            үлчәм=имин_тышча(Caylaw['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(үлчәм.stderr)
            assert үлчәм.returncode==0 and 'class 창예제'.encode() in үлчәм.stdout, (үлчәм.returncode,үлчәм.stdout,үлчәм.stderr)
            assert үлчәм.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, үлчәм.stderr
            отчет_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(тышча_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактив_сеанс=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();тамгаланган_өлеш_VALUE=selectors.DefaultSelector();тамгаланган_өлеш_VALUE.register(интерактив_сеанс.stdout,selectors.EVENT_READ)
            def 대화읽기(күрсәтү_VALUE):
                마감=time.monotonic()+30
                while күрсәтү_VALUE not in 대화기록:
                    if time.monotonic()>마감 or интерактив_сеанс.poll() is not None:raise AssertionError('SSH interactive missing '+repr(күрсәтү_VALUE)+' '+repr(bytes(대화기록)))
                    for кертү_VALUE,_ in тамгаланган_өлеш_VALUE.select(.1):
                        조각=кертү_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактив_сеанс.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактив_сеанс.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактив_сеанс.stdin.write(b'\x04');интерактив_сеанс.stdin.flush();나머지,Хата=интерактив_сеанс.communicate(timeout=15)
                assert интерактив_сеанс.returncode==0 and b'PTY allocation request failed' not in Хата,(интерактив_сеанс.returncode,Хата)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                тамгаланган_өлеш_VALUE.close()
                if интерактив_сеанс.poll() is None:интерактив_сеанс.kill();интерактив_сеанс.wait()
            отчет_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ялгау, 수):
                мәгълүмат=bytearray()
                while len(мәгълүмат)<수:
                    덩이=ялгау.recv(수-len(мәгълүмат))
                    if not 덩이: raise AssertionError('RFB EOF')
                    мәгълүмат.extend(덩이)
                return bytes(мәгълүмат)
            def 화면인증(серсүз_VALUE):
                ялгау=socket.create_connection(('127.0.0.5',화면포트),10);ялгау.settimeout(30)
                assert 정확히(ялгау,12)==b'RFB 003.008\n'
                ялгау.sendall(b'RFB 003.008\n');assert 정확히(ялгау,2)==b'\x01\x02'
                ялгау.sendall(b'\x02');тикшерү_чарасы_VALUE=정확히(ялгау,16)
                입력암호=серсүз_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ялгау.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(тикшерү_чарасы_VALUE))
                халәт_VALUE=struct.unpack('!I',정확히(ялгау,4))[0]
                return ялгау,халәт_VALUE
            дөрес_булмаган_серсүз='!' if not Caylaw['vnc_password'].startswith('!') else '?'
            ялгау,халәт_VALUE=화면인증(дөрес_булмаган_серсүз);assert халәт_VALUE==1;ялгау.close();time.sleep(.6)
            отчет_VALUE['checks'].append('VNC incorrect password rejected')
            ялгау,халәт_VALUE=화면인증(Caylaw['vnc_password']);assert халәт_VALUE==0
            with ялгау:
                ялгау.sendall(b'\x01');초기=정확히(ялгау,24);너비,높이=struct.unpack('!HH',초기[:4]);исем=정확히(ялгау,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==исем
                def 화면(증분=0):
                    ялгау.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ялгау,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    сызым_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_координатасы,세로좌표,영역너비,영역높이,ысул_MODE=struct.unpack('!HHHHi',정확히(ялгау,12));assert ысул_MODE==0 and X_координатасы+영역너비<=너비 and 세로좌표+영역높이<=높이
                        нокта=정확히(ялгау,영역너비*영역높이*4);합계+=len(нокта)
                        for юл in range(영역높이):сызым_VALUE[((세로좌표+юл)*너비+X_координатасы)*4:((세로좌표+юл)*너비+X_координатасы+영역너비)*4]=нокта[юл*영역너비*4:(юл+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(сызым_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                отчет_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                отчет_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_юл)
                for символ_VALUE_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if символ_VALUE_068c2631=='\r' else ord(символ_VALUE_068c2631)
                    ялгау.sendall(struct.pack('!BBHI',4,1,0,символ));ялгау.sendall(struct.pack('!BBHI',4,0,0,символ))
                기다림(b'VNC_NATIVE_PASS',처음)
                отчет_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(символ,누름=1):ялгау.sendall(struct.pack('!BBHI',4,누름,0,символ))
                처음=len(LOG_юл)
                for символ_VALUE_068c2631 in 'echo ':글쇠(ord(символ_VALUE_068c2631))
                글쇠(0xffc6)
                for символ_VALUE_068c2631 in 'gksrmf':글쇠(ord(символ_VALUE_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                отчет_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                ялгау.sendall(struct.pack('!BBHH',5,0,120,100))
                отчет_VALUE['checks'].append('VNC pointer input accepted')
            Процесс_VALUE.stdin.write(b'poweroff\n');Процесс_VALUE.stdin.flush();Процесс_VALUE.wait(timeout=15);assert Процесс_VALUE.returncode==0
            отчет_VALUE['passed']=True
    finally:
        if Процесс_VALUE and Процесс_VALUE.poll() is None:
            Процесс_VALUE.terminate()
            try: Процесс_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс_VALUE.kill();Процесс_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_юл)
        (출력/'report.json').write_text(json.dumps(отчет_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(отчет_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': эшләтү()
