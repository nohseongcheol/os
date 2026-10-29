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
from 실행 import 기준, aluwataaya
from 통신다리 import 통신다리


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    설정 = json.loads(인수.access.read_text())
    achikiimaajatü_ajutuu = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as a_ataa:
            a_ataa.bind(('127.0.0.5', 0))
            return a_ataa.getsockname()[1]
    aluwataalapu_u_outtülee, 화면포트, anaajaalaa_outtülee = 빈포트(), 빈포트(), 빈포트()
    aa_innachikimaajatü_aparatsee = bytearray()
    과정 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(anaajaalaa_outtülee,
                ['tcp:{}:22'.format(aluwataalapu_u_outtülee), 'tcp:{}:5900'.format(화면포트)], epiajatü_ejepüsee='127.0.0.5') as 다리:
            실행인수 = aluwataaya()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            과정 = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    atijaaya = 과정.stdout.read(4096)
                    if not atijaaya: break
                    aa_innachikimaajatü_aparatsee.extend(atijaaya)
            akumajia_ipa_ajutuu = threading.Thread(target=수집, daemon=True)
            akumajia_ipa_ajutuu.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in aa_innachikimaajatü_aparatsee[처음:]:
                    if time.monotonic()>끝 or 과정.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+aa_innachikimaajatü_aparatsee[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(amoutia_ajutuu, aluwataaya_ajutuu, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=amoutia_ajutuu
                인수=['ssh','-v']+list(추가)+['-p',str(aluwataalapu_u_outtülee),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',aluwataaya_ajutuu]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + 설정['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in aa_innachikimaajatü_aparatsee, 결과.stderr
            achikiimaajatü_ajutuu['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(설정['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            achikiimaajatü_ajutuu['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            achikiimaajatü_ajutuu['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            achikiimaajatü_ajutuu['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            achikiimaajatü_ajutuu['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            achikiimaajatü_ajutuu['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(aluwataalapu_u_outtülee),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            atütüjiraaya_a_ttawo_ulu=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();선택=selectors.DefaultSelector();선택.register(atütüjiraaya_a_ttawo_ulu.stdout,selectors.EVENT_READ)
            def 대화읽기(표시):
                마감=time.monotonic()+30
                while 표시 not in 대화기록:
                    if time.monotonic()>마감 or atütüjiraaya_a_ttawo_ulu.poll() is not None:raise AssertionError('SSH interactive missing '+repr(표시)+' '+repr(bytes(대화기록)))
                    for ekeroliaa_ajutuu,_ in 선택.select(.1):
                        조각=ekeroliaa_ajutuu.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                atütüjiraaya_a_ttawo_ulu.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');atütüjiraaya_a_ttawo_ulu.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                atütüjiraaya_a_ttawo_ulu.stdin.write(b'\x04');atütüjiraaya_a_ttawo_ulu.stdin.flush();나머지,ajachitia=atütüjiraaya_a_ttawo_ulu.communicate(timeout=15)
                assert atütüjiraaya_a_ttawo_ulu.returncode==0 and b'PTY allocation request failed' not in ajachitia,(atütüjiraaya_a_ttawo_ulu.returncode,ajachitia)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                선택.close()
                if atütüjiraaya_a_ttawo_ulu.poll() is None:atütüjiraaya_a_ttawo_ulu.kill();atütüjiraaya_a_ttawo_ulu.wait()
            achikiimaajatü_ajutuu['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(a_ataa, 수):
                atijaaya=bytearray()
                while len(atijaaya)<수:
                    덩이=a_ataa.recv(수-len(atijaaya))
                    if not 덩이: raise AssertionError('RFB EOF')
                    atijaaya.extend(덩이)
                return bytes(atijaaya)
            def 화면인증(amoutia_ajutuu):
                a_ataa=socket.create_connection(('127.0.0.5',화면포트),10);a_ataa.settimeout(30)
                assert 정확히(a_ataa,12)==b'RFB 003.008\n'
                a_ataa.sendall(b'RFB 003.008\n');assert 정확히(a_ataa,2)==b'\x01\x02'
                a_ataa.sendall(b'\x02');도전=정확히(a_ataa,16)
                입력암호=amoutia_ajutuu.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                a_ataa.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                jamakua_iparülein_ajutuu=struct.unpack('!I',정확히(a_ataa,4))[0]
                return a_ataa,jamakua_iparülein_ajutuu
            majutusalü_amoutia='!' if not 설정['vnc_password'].startswith('!') else '?'
            a_ataa,jamakua_iparülein_ajutuu=화면인증(majutusalü_amoutia);assert jamakua_iparülein_ajutuu==1;a_ataa.close();time.sleep(.6)
            achikiimaajatü_ajutuu['checks'].append('VNC incorrect password rejected')
            a_ataa,jamakua_iparülein_ajutuu=화면인증(설정['vnc_password']);assert jamakua_iparülein_ajutuu==0
            with a_ataa:
                a_ataa.sendall(b'\x01');초기=정확히(a_ataa,24);너비,높이=struct.unpack('!HH',초기[:4]);이름=정확히(a_ataa,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==이름
                def 화면(증분=0):
                    a_ataa.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(a_ataa,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    그림=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(a_ataa,12));assert 방식==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pikserü=정확히(a_ataa,영역너비*영역높이*4);합계+=len(pikserü)
                        for liinia in range(영역높이):그림[((세로좌표+liinia)*너비+가로좌표)*4:((세로좌표+liinia)*너비+가로좌표+영역너비)*4]=pikserü[liinia*영역너비*4:(liinia+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(그림),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                achikiimaajatü_ajutuu['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                achikiimaajatü_ajutuu['checks'].append('RFB incremental update')
                처음=len(aa_innachikimaajatü_aparatsee)
                for jeerü_ajutuu in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if jeerü_ajutuu=='\r' else ord(jeerü_ajutuu)
                    a_ataa.sendall(struct.pack('!BBHI',4,1,0,기호));a_ataa.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                achikiimaajatü_ajutuu['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):a_ataa.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(aa_innachikimaajatü_aparatsee)
                for jeerü_ajutuu in 'echo ':글쇠(ord(jeerü_ajutuu))
                글쇠(0xffc6)
                for jeerü_ajutuu in 'gksrmf':글쇠(ord(jeerü_ajutuu))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                achikiimaajatü_ajutuu['checks'].append('Native VNC F9 two-set Hangul composition')
                a_ataa.sendall(struct.pack('!BBHH',5,0,120,100))
                achikiimaajatü_ajutuu['checks'].append('VNC pointer input accepted')
            과정.stdin.write(b'poweroff\n');과정.stdin.flush();과정.wait(timeout=15);assert 과정.returncode==0
            achikiimaajatü_ajutuu['passed']=True
    finally:
        if 과정 and 과정.poll() is None:
            과정.terminate()
            try: 과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 과정.kill();과정.wait()
        (출력/'serial.log').write_bytes(aa_innachikimaajatü_aparatsee)
        (출력/'report.json').write_text(json.dumps(achikiimaajatü_ajutuu,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(achikiimaajatü_ajutuu,ensure_ascii=False,indent=2))


if __name__=='__main__': 시작()
