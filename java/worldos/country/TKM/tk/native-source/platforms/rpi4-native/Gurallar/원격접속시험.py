#!/usr/bin/env python3
"""hakyky_maglumat OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ýerine_ýetir_buýruk import 기준, buýruk
from 통신다리 import 통신다리


def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Düzümler = json.loads(인수.access.read_text())
    hasabat_baha = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def boş_port():
        with socket.socket() as Birikme:
            Birikme.bind(('127.0.0.5', 0))
            return Birikme.getsockname()[1]
    gabyjak_port, 화면포트, faýl_port = boş_port(), boş_port(), boş_port()
    hasaba_alyş_setir = bytearray()
    Proses_baha = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(faýl_port,
                ['tcp:{}:22'.format(gabyjak_port), 'tcp:{}:5900'.format(화면포트)], esasy_salgy='127.0.0.5') as 다리:
            실행인수 = buýruk()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proses_baha = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    maglumat = Proses_baha.stdout.read(4096)
                    if not maglumat: break
                    hasaba_alyş_setir.extend(maglumat)
            akym_baha = threading.Thread(target=수집, daemon=True)
            akym_baha.start()
            def 기다림(Söz_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Söz_SMS not in hasaba_alyş_setir[처음:]:
                    if time.monotonic()>끝 or Proses_baha.poll() is not None:
                        raise AssertionError('Missing '+repr(Söz_SMS)+'\n'+hasaba_alyş_setir[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def goragly_gabyjak(parol_baha, instruksiýa_baha, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=parol_baha
                인수=['ssh','-v']+list(추가)+['-p',str(gabyjak_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksiýa_baha]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=goragly_gabyjak('!' + Düzümler['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in hasaba_alyş_setir, 결과.stderr
            hasabat_baha['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=goragly_gabyjak(Düzümler['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            hasabat_baha['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            hasabat_baha['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=goragly_gabyjak(Düzümler['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            hasabat_baha['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=goragly_gabyjak(Düzümler['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            hasabat_baha['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=goragly_gabyjak(Düzümler['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            hasabat_baha['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(gabyjak_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiw_seans=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();saýlama_baha=selectors.DefaultSelector();saýlama_baha.register(interaktiw_seans.stdout,selectors.EVENT_READ)
            def 대화읽기(görkez_baha_487749b8):
                마감=time.monotonic()+30
                while görkez_baha_487749b8 not in 대화기록:
                    if time.monotonic()>마감 or interaktiw_seans.poll() is not None:raise AssertionError('SSH interactive missing '+repr(görkez_baha_487749b8)+' '+repr(bytes(대화기록)))
                    for girizmeklik_baha,_ in saýlama_baha.select(.1):
                        조각=girizmeklik_baha.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiw_seans.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiw_seans.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiw_seans.stdin.write(b'\x04');interaktiw_seans.stdin.flush();나머지,Hata=interaktiw_seans.communicate(timeout=15)
                assert interaktiw_seans.returncode==0 and b'PTY allocation request failed' not in Hata,(interaktiw_seans.returncode,Hata)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                saýlama_baha.close()
                if interaktiw_seans.poll() is None:interaktiw_seans.kill();interaktiw_seans.wait()
            hasabat_baha['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Birikme, 수):
                maglumat=bytearray()
                while len(maglumat)<수:
                    덩이=Birikme.recv(수-len(maglumat))
                    if not 덩이: raise AssertionError('RFB EOF')
                    maglumat.extend(덩이)
                return bytes(maglumat)
            def 화면인증(parol_baha):
                Birikme=socket.create_connection(('127.0.0.5',화면포트),10);Birikme.settimeout(30)
                assert 정확히(Birikme,12)==b'RFB 003.008\n'
                Birikme.sendall(b'RFB 003.008\n');assert 정확히(Birikme,2)==b'\x01\x02'
                Birikme.sendall(b'\x02');barlag_baha=정확히(Birikme,16)
                입력암호=parol_baha.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Birikme.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(barlag_baha))
                ýagdaý_baha=struct.unpack('!I',정확히(Birikme,4))[0]
                return Birikme,ýagdaý_baha
            nädogry_parol='!' if not Düzümler['vnc_password'].startswith('!') else '?'
            Birikme,ýagdaý_baha=화면인증(nädogry_parol);assert ýagdaý_baha==1;Birikme.close();time.sleep(.6)
            hasabat_baha['checks'].append('VNC incorrect password rejected')
            Birikme,ýagdaý_baha=화면인증(Düzümler['vnc_password']);assert ýagdaý_baha==0
            with Birikme:
                Birikme.sendall(b'\x01');초기=정확히(Birikme,24);너비,높이=struct.unpack('!HH',초기[:4]);Ad=정확히(Birikme,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ad
                def 화면(증분=0):
                    Birikme.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Birikme,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    çyzgy_baha=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinatasy,세로좌표,영역너비,영역높이,usul_reje=struct.unpack('!HHHHi',정확히(Birikme,12));assert usul_reje==0 and x_koordinatasy+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pel=정확히(Birikme,영역너비*영역높이*4);합계+=len(pel)
                        for setir in range(영역높이):çyzgy_baha[((세로좌표+setir)*너비+x_koordinatasy)*4:((세로좌표+setir)*너비+x_koordinatasy+영역너비)*4]=pel[setir*영역너비*4:(setir+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(çyzgy_baha),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                hasabat_baha['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                hasabat_baha['checks'].append('RFB incremental update')
                처음=len(hasaba_alyş_setir)
                for nyşan_baha_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    nyşan=0xff0d if nyşan_baha_068c2631=='\r' else ord(nyşan_baha_068c2631)
                    Birikme.sendall(struct.pack('!BBHI',4,1,0,nyşan));Birikme.sendall(struct.pack('!BBHI',4,0,0,nyşan))
                기다림(b'VNC_NATIVE_PASS',처음)
                hasabat_baha['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(nyşan,누름=1):Birikme.sendall(struct.pack('!BBHI',4,누름,0,nyşan))
                처음=len(hasaba_alyş_setir)
                for nyşan_baha_068c2631 in 'echo ':글쇠(ord(nyşan_baha_068c2631))
                글쇠(0xffc6)
                for nyşan_baha_068c2631 in 'gksrmf':글쇠(ord(nyşan_baha_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                hasabat_baha['checks'].append('Native VNC F9 two-set Hangul composition')
                Birikme.sendall(struct.pack('!BBHH',5,0,120,100))
                hasabat_baha['checks'].append('VNC pointer input accepted')
            Proses_baha.stdin.write(b'poweroff\n');Proses_baha.stdin.flush();Proses_baha.wait(timeout=15);assert Proses_baha.returncode==0
            hasabat_baha['passed']=True
    finally:
        if Proses_baha and Proses_baha.poll() is None:
            Proses_baha.terminate()
            try: Proses_baha.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses_baha.kill();Proses_baha.wait()
        (출력/'serial.log').write_bytes(hasaba_alyş_setir)
        (출력/'report.json').write_text(json.dumps(hasabat_baha,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(hasabat_baha,ensure_ascii=False,indent=2))


if __name__=='__main__': Bitir()
