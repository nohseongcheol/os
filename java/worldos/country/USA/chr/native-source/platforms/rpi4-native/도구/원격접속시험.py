#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ
from 통신다리 import 통신다리


def ᎠᎢᏎᏍᏗ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    ᏕᎦᎧᎲᎢ = json.loads(인수.access.read_text())
    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as ᎫᏓᎳ:
            ᎫᏓᎳ.bind(('127.0.0.5', 0))
            return ᎫᏓᎳ.getsockname()[1]
    ᎤᏯᏍᎦ_ᎫᏓᎸᏗ, 화면포트, ᎠᏍᏆᏂᎪᏙᏗ_ᎫᏓᎸᏗ = 빈포트(), 빈포트(), 빈포트()
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray()
    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᏓᎸᏗ,
                ['tcp:{}:22'.format(ᎤᏯᏍᎦ_ᎫᏓᎸᏗ), 'tcp:{}:5900'.format(화면포트)], ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ='127.0.0.5') as 다리:
            실행인수 = ᎤᏁᏤᎸᎩ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ᎦᏟᏌᏅᎯ = ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout.read(4096)
                    if not ᎦᏟᏌᏅᎯ: break
                    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
            ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ = threading.Thread(target=수집, daemon=True)
            ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:]:
                    if time.monotonic()>끝 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ, ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ
                인수=['ssh','-v']+list(추가)+['-p',str(ᎤᏯᏍᎦ_ᎫᏓᎸᏗ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + ᏕᎦᎧᎲᎢ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, 결과.stderr
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(ᏕᎦᎧᎲᎢ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(ᏕᎦᎧᎲᎢ['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(ᏕᎦᎧᎲᎢ['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(ᏕᎦᎧᎲᎢ['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ᎤᏯᏍᎦ_ᎫᏓᎸᏗ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ=selectors.DefaultSelector();ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.register(ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.stdout,selectors.EVENT_READ)
            def 대화읽기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ):
                마감=time.monotonic()+30
                while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in 대화기록:
                    if time.monotonic()>마감 or ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ)+' '+repr(bytes(대화기록)))
                    for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ,_ in ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.select(.1):
                        조각=Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.stdin.write(b'\x04');ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.stdin.flush();나머지,ᎦᎵᏓᏍᏔᏅ=ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.communicate(timeout=15)
                assert ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.returncode==0 and b'PTY allocation request failed' not in ᎦᎵᏓᏍᏔᏅ,(ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.returncode,ᎦᎵᏓᏍᏔᏅ)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.close()
                if ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.poll() is None:ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.kill();ᏗᎵᎪᎲᏍᎩ_ᎤᎾᏓᏡᎩ.wait()
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ᎫᏓᎳ, 수):
                ᎦᏟᏌᏅᎯ=bytearray()
                while len(ᎦᏟᏌᏅᎯ)<수:
                    덩이=ᎫᏓᎳ.recv(수-len(ᎦᏟᏌᏅᎯ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ᎦᏟᏌᏅᎯ.extend(덩이)
                return bytes(ᎦᏟᏌᏅᎯ)
            def 화면인증(ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ):
                ᎫᏓᎳ=socket.create_connection(('127.0.0.5',화면포트),10);ᎫᏓᎳ.settimeout(30)
                assert 정확히(ᎫᏓᎳ,12)==b'RFB 003.008\n'
                ᎫᏓᎳ.sendall(b'RFB 003.008\n');assert 정확히(ᎫᏓᎳ,2)==b'\x01\x02'
                ᎫᏓᎳ.sendall(b'\x02');도전=정확히(ᎫᏓᎳ,16)
                입력암호=ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ᎫᏓᎳ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ=struct.unpack('!I',정확히(ᎫᏓᎳ,4))[0]
                return ᎫᏓᎳ,ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ
            ᏂᏓᏓᏂᎸᎬᎾ_ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ='!' if not ᏕᎦᎧᎲᎢ['vnc_password'].startswith('!') else '?'
            ᎫᏓᎳ,ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ=화면인증(ᏂᏓᏓᏂᎸᎬᎾ_ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ);assert ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ==1;ᎫᏓᎳ.close();time.sleep(.6)
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('VNC incorrect password rejected')
            ᎫᏓᎳ,ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ=화면인증(ᏕᎦᎧᎲᎢ['vnc_password']);assert ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ==0
            with ᎫᏓᎳ:
                ᎫᏓᎳ.sendall(b'\x01');초기=정확히(ᎫᏓᎳ,24);너비,높이=struct.unpack('!HH',초기[:4]);ᏚᏙᎥᎢ=정확히(ᎫᏓᎳ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ᏚᏙᎥᎢ
                def 화면(증분=0):
                    ᎫᏓᎳ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ᎫᏓᎳ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,method_ᎬᏙᏗ=struct.unpack('!HHHHi',정확히(ᎫᏓᎳ,12));assert method_ᎬᏙᏗ==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pel=정확히(ᎫᏓᎳ,영역너비*영역높이*4);합계+=len(pel)
                        for ᏚᏓᏅᏅᎢ in range(영역높이):ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ[((세로좌표+ᏚᏓᏅᏅᎢ)*너비+가로좌표)*4:((세로좌표+ᏚᏓᏅᏅᎢ)*너비+가로좌표+영역너비)*4]=pel[ᏚᏓᏅᏅᎢ*영역너비*4:(ᏚᏓᏅᏅᎢ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('RFB incremental update')
                처음=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ=='\r' else ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)
                    ᎫᏓᎳ.sendall(struct.pack('!BBHI',4,1,0,기호));ᎫᏓᎳ.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):ᎫᏓᎳ.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 'echo ':글쇠(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ))
                글쇠(0xffc6)
                for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 'gksrmf':글쇠(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Native VNC F9 two-set Hangul composition')
                ᎫᏓᎳ.sendall(struct.pack('!BBHH',5,0,120,100))
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('VNC pointer input accepted')
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.write(b'poweroff\n');ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.flush();ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=15);assert ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.returncode==0
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed']=True
    finally:
        if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ and ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
            try: ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=5)
            except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill();ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
        (출력/'serial.log').write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        (출력/'report.json').write_text(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ,ensure_ascii=False,indent=2))


if __name__=='__main__': ᎠᎢᏎᏍᏗ()
