#!/usr/bin/env python3
"""бодит_өгөгдөл OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Гүйцэтгэх_команд import 기준, Тушаал
from 통신다리 import 통신다리


def Ажиллуулах():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Тохиргоо = json.loads(인수.access.read_text())
    тайлан_утга_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def хоосон_порт():
        with socket.socket() as Холбох:
            Холбох.bind(('127.0.0.5', 0))
            return Холбох.getsockname()[1]
    бүрхүүл_порт, 화면포트, файл_порт = хоосон_порт(), хоосон_порт(), хоосон_порт()
    бичих_мөр_6e8b375a = bytearray()
    үйл_явц_утга = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(файл_порт,
                ['tcp:{}:22'.format(бүрхүүл_порт), 'tcp:{}:5900'.format(화면포트)], хост_хаяг='127.0.0.5') as 다리:
            실행인수 = Тушаал()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            үйл_явц_утга = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    өгөгдөл = үйл_явц_утга.stdout.read(4096)
                    if not өгөгдөл: break
                    бичих_мөр_6e8b375a.extend(өгөгдөл)
            яриа_утга = threading.Thread(target=수집, daemon=True)
            яриа_утга.start()
            def 기다림(Үгэн_Бичвэр, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Үгэн_Бичвэр not in бичих_мөр_6e8b375a[처음:]:
                    if time.monotonic()>끝 or үйл_явц_утга.poll() is not None:
                        raise AssertionError('Missing '+repr(Үгэн_Бичвэр)+'\n'+бичих_мөр_6e8b375a[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def аюулгүй_бүрхүүл(нууц_үг_утга, заавар_утга, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=нууц_үг_утга
                인수=['ssh','-v']+list(추가)+['-p',str(бүрхүүл_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',заавар_утга]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=аюулгүй_бүрхүүл('!' + Тохиргоо['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in бичих_мөр_6e8b375a, 결과.stderr
            тайлан_утга_ddf2aaf3['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=аюулгүй_бүрхүүл(Тохиргоо['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            тайлан_утга_ddf2aaf3['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            тайлан_утга_ddf2aaf3['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=аюулгүй_бүрхүүл(Тохиргоо['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            тайлан_утга_ddf2aaf3['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=аюулгүй_бүрхүүл(Тохиргоо['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            тайлан_утга_ddf2aaf3['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=аюулгүй_бүрхүүл(Тохиргоо['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            тайлан_утга_ddf2aaf3['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(бүрхүүл_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            харилцан_хандах_логик_холболт=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();сонгосон_хэсэг_утга=selectors.DefaultSelector();сонгосон_хэсэг_утга.register(харилцан_хандах_логик_холболт.stdout,selectors.EVENT_READ)
            def 대화읽기(үзүүлэх_утга):
                마감=time.monotonic()+30
                while үзүүлэх_утга not in 대화기록:
                    if time.monotonic()>마감 or харилцан_хандах_логик_холболт.poll() is not None:raise AssertionError('SSH interactive missing '+repr(үзүүлэх_утга)+' '+repr(bytes(대화기록)))
                    for оролт_утга,_ in сонгосон_хэсэг_утга.select(.1):
                        조각=оролт_утга.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                харилцан_хандах_логик_холболт.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');харилцан_хандах_логик_холболт.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                харилцан_хандах_логик_холболт.stdin.write(b'\x04');харилцан_хандах_логик_холболт.stdin.flush();나머지,Алдаа=харилцан_хандах_логик_холболт.communicate(timeout=15)
                assert харилцан_хандах_логик_холболт.returncode==0 and b'PTY allocation request failed' not in Алдаа,(харилцан_хандах_логик_холболт.returncode,Алдаа)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                сонгосон_хэсэг_утга.close()
                if харилцан_хандах_логик_холболт.poll() is None:харилцан_хандах_логик_холболт.kill();харилцан_хандах_логик_холболт.wait()
            тайлан_утга_ddf2aaf3['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Холбох, 수):
                өгөгдөл=bytearray()
                while len(өгөгдөл)<수:
                    덩이=Холбох.recv(수-len(өгөгдөл))
                    if not 덩이: raise AssertionError('RFB EOF')
                    өгөгдөл.extend(덩이)
                return bytes(өгөгдөл)
            def 화면인증(нууц_үг_утга):
                Холбох=socket.create_connection(('127.0.0.5',화면포트),10);Холбох.settimeout(30)
                assert 정확히(Холбох,12)==b'RFB 003.008\n'
                Холбох.sendall(b'RFB 003.008\n');assert 정확히(Холбох,2)==b'\x01\x02'
                Холбох.sendall(b'\x02');нотлох_код_утга=정확히(Холбох,16)
                입력암호=нууц_үг_утга.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Холбох.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(нотлох_код_утга))
                төлөв_утга=struct.unpack('!I',정확히(Холбох,4))[0]
                return Холбох,төлөв_утга
            буруу_нууц_үг='!' if not Тохиргоо['vnc_password'].startswith('!') else '?'
            Холбох,төлөв_утга=화면인증(буруу_нууц_үг);assert төлөв_утга==1;Холбох.close();time.sleep(.6)
            тайлан_утга_ddf2aaf3['checks'].append('VNC incorrect password rejected')
            Холбох,төлөв_утга=화면인증(Тохиргоо['vnc_password']);assert төлөв_утга==0
            with Холбох:
                Холбох.sendall(b'\x01');초기=정확히(Холбох,24);너비,높이=struct.unpack('!HH',초기[:4]);Нэр=정확히(Холбох,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Нэр
                def 화면(증분=0):
                    Холбох.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Холбох,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    зураг_утга_c143fe9e=bytearray(너비*높이*4)
                    for _ in range(수):
                        х_координат,세로좌표,영역너비,영역높이,арга_горим=struct.unpack('!HHHHi',정확히(Холбох,12));assert арга_горим==0 and х_координат+영역너비<=너비 and 세로좌표+영역높이<=높이
                        нягтрал=정확히(Холбох,영역너비*영역높이*4);합계+=len(нягтрал)
                        for Шугам in range(영역높이):зураг_утга_c143fe9e[((세로좌표+Шугам)*너비+х_координат)*4:((세로좌표+Шугам)*너비+х_координат+영역너비)*4]=нягтрал[Шугам*영역너비*4:(Шугам+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(зураг_утга_c143fe9e),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                тайлан_утга_ddf2aaf3['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                тайлан_утга_ddf2aaf3['checks'].append('RFB incremental update')
                처음=len(бичих_мөр_6e8b375a)
                for тэмдэгт_утга in 'echo VNC_NATIVE_PASS\r':
                    тэмдэг=0xff0d if тэмдэгт_утга=='\r' else ord(тэмдэгт_утга)
                    Холбох.sendall(struct.pack('!BBHI',4,1,0,тэмдэг));Холбох.sendall(struct.pack('!BBHI',4,0,0,тэмдэг))
                기다림(b'VNC_NATIVE_PASS',처음)
                тайлан_утга_ddf2aaf3['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(тэмдэг,누름=1):Холбох.sendall(struct.pack('!BBHI',4,누름,0,тэмдэг))
                처음=len(бичих_мөр_6e8b375a)
                for тэмдэгт_утга in 'echo ':글쇠(ord(тэмдэгт_утга))
                글쇠(0xffc6)
                for тэмдэгт_утга in 'gksrmf':글쇠(ord(тэмдэгт_утга))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                тайлан_утга_ddf2aaf3['checks'].append('Native VNC F9 two-set Hangul composition')
                Холбох.sendall(struct.pack('!BBHH',5,0,120,100))
                тайлан_утга_ddf2aaf3['checks'].append('VNC pointer input accepted')
            үйл_явц_утга.stdin.write(b'poweroff\n');үйл_явц_утга.stdin.flush();үйл_явц_утга.wait(timeout=15);assert үйл_явц_утга.returncode==0
            тайлан_утга_ddf2aaf3['passed']=True
    finally:
        if үйл_явц_утга and үйл_явц_утга.poll() is None:
            үйл_явц_утга.terminate()
            try: үйл_явц_утга.wait(timeout=5)
            except subprocess.TimeoutExpired: үйл_явц_утга.kill();үйл_явц_утга.wait()
        (출력/'serial.log').write_bytes(бичих_мөр_6e8b375a)
        (출력/'report.json').write_text(json.dumps(тайлан_утга_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(тайлан_утга_ddf2aaf3,ensure_ascii=False,indent=2))


if __name__=='__main__': Ажиллуулах()
