#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ
from ਨੈਟਵਰਕ_ਬਰਿਜ import ਨੈਟਵਰਕ_ਬਰਿਜ


def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/native-remote')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    ਆਉਟਪੁੱਟ = ਆਰਗੂਮੈਂਟ.output
    ਆਉਟਪੁੱਟ.mkdir(parents=True, exist_ok=True)
    ਸੈਟਿੰਗ = json.loads(ਆਰਗੂਮੈਂਟ.access.read_text())
    ਵਿਵਰਨ_ਕੀਮਤ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(ਆਰਗੂਮੈਂਟ.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ਖਾਲੀ_ਪੋਰਟ():
        with socket.socket() as ਕੁਨੈਕਸ਼ਨ_ਕਰੋ:
            ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.bind(('127.0.0.5', 0))
            return ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getsockname()[1]
    ਸ਼ੈਲ_ਪੋਰਟ, 화면포트, ਲਿਖਤ_ਪੱਤਰ_ਪੋਰਟ = ਖਾਲੀ_ਪੋਰਟ(), ਖਾਲੀ_ਪੋਰਟ(), ਖਾਲੀ_ਪੋਰਟ()
    ਲੌਗ_ਕਤਾਰ = bytearray()
    ਕਾਰਵਾਈ_ਕੀਮਤ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ਨੈਟਵਰਕ_ਬਰਿਜ(ਲਿਖਤ_ਪੱਤਰ_ਪੋਰਟ,
                ['tcp:{}:22'.format(ਸ਼ੈਲ_ਪੋਰਟ), 'tcp:{}:5900'.format(화면포트)], ਹੋਸਟ_ਪਤਾ='127.0.0.5') as ਬਰਿਜ_ਕੀਮਤ:
            실행인수 = ਕਮਾਂਡ()
            실행인수[실행인수.index('-kernel') + 1] = str(ਆਰਗੂਮੈਂਟ.kernel.resolve())
            ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ਬਰਿਜ_ਕੀਮਤ.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ਸਮੱਗਰੀ = ਕਾਰਵਾਈ_ਕੀਮਤ.stdout.read(4096)
                    if not ਸਮੱਗਰੀ: break
                    ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
            ਥ੍ਰੈਡ_ਕੀਮਤ = threading.Thread(target=수집, daemon=True)
            ਥ੍ਰੈਡ_ਕੀਮਤ.start()
            def 기다림(ਸ਼ਬਦ_ਪਾਠ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ਸ਼ਬਦ_ਪਾਠ not in ਲੌਗ_ਕਤਾਰ[처음:]:
                    if time.monotonic()>끝 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                        raise AssertionError('Missing '+repr(ਸ਼ਬਦ_ਪਾਠ)+'\n'+ਲੌਗ_ਕਤਾਰ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ(ਪਾਸਵਰਡ_ਕੀਮਤ, ਨਿਰਦੇਸ਼_ਕੀਮਤ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ਪਾਸਵਰਡ_ਕੀਮਤ
                ਆਰਗੂਮੈਂਟ=['ssh','-v']+list(추가)+['-p',str(ਸ਼ੈਲ_ਪੋਰਟ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ਨਿਰਦੇਸ਼_ਕੀਮਤ]
                ਮਾਪ=subprocess.run(ਆਰਗੂਮੈਂਟ,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ਮਾਪ
            ਮਾਪ=ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ('!' + ਸੈਟਿੰਗ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ਆਉਟਪੁੱਟ/'ssh-rejected.log').write_bytes(ਮਾਪ.stderr)
            assert ਮਾਪ.returncode!=0 and b'Permission denied' in ਮਾਪ.stderr and b'SHOULD_NOT_RUN' not in ਲੌਗ_ਕਤਾਰ, ਮਾਪ.stderr
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ਮਾਪ=ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ(ਸੈਟਿੰਗ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ਆਉਟਪੁੱਟ/'ssh.log').write_bytes(ਮਾਪ.stderr)
            (ਆਉਟਪੁੱਟ/'ssh-output.txt').write_bytes(ਮਾਪ.stdout)
            assert ਮਾਪ.returncode==0 and b'SSH_NATIVE_PASS' in ਮਾਪ.stdout, (ਮਾਪ.returncode,ਮਾਪ.stdout,ਮਾਪ.stderr)
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ਮਾਪ.stderr, ਮਾਪ.stderr
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ਮਾਪ=ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ(ਸੈਟਿੰਗ['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ਮਾਪ.returncode==0 and 'JAVA ਆਉਟਪੁੱਟ: 안녕하세요 😀'.encode() in ਮਾਪ.stdout,ਮਾਪ.stdout
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ਮਾਪ=ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ(ਸੈਟਿੰਗ['ssh_password'], 'missing_remote_command')
            assert ਮਾਪ.returncode==127,ਮਾਪ.returncode
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ਮਾਪ=ਸੁਰੱਖਿਅਤ_ਸ਼ੈਲ(ਸੈਟਿੰਗ['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ਆਉਟਪੁੱਟ/'ssh-rekey.log').write_bytes(ਮਾਪ.stderr)
            assert ਮਾਪ.returncode==0 and 'class 창예제'.encode() in ਮਾਪ.stdout, (ਮਾਪ.returncode,ਮਾਪ.stdout,ਮਾਪ.stderr)
            assert ਮਾਪ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ਮਾਪ.stderr
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ਸ਼ੈਲ_ਪੋਰਟ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ਚੋਣ_ਕੀਮਤ=selectors.DefaultSelector();ਚੋਣ_ਕੀਮਤ.register(ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.stdout,selectors.EVENT_READ)
            def 대화읽기(ਸ਼ੋਅ_ਕੀਮਤ):
                마감=time.monotonic()+30
                while ਸ਼ੋਅ_ਕੀਮਤ not in 대화기록:
                    if time.monotonic()>마감 or ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ਸ਼ੋਅ_ਕੀਮਤ)+' '+repr(bytes(대화기록)))
                    for ਦਾਖਲਾ_ਕੀਮਤ,_ in ਚੋਣ_ਕੀਮਤ.select(.1):
                        조각=ਦਾਖਲਾ_ਕੀਮਤ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.stdin.write(b'\x04');ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.stdin.flush();나머지,ਗਲਤੀ=ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.communicate(timeout=15)
                assert ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.returncode==0 and b'PTY allocation request failed' not in ਗਲਤੀ,(ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.returncode,ਗਲਤੀ)
                (ਆਉਟਪੁੱਟ/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ਚੋਣ_ਕੀਮਤ.close()
                if ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.poll() is None:ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.kill();ਪਰਸਪਰਸਕ੍ਰਿਆਸ਼ੀਲ_ਸੈਸ਼ਨ.wait()
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ, 수):
                ਸਮੱਗਰੀ=bytearray()
                while len(ਸਮੱਗਰੀ)<수:
                    덩이=ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.recv(수-len(ਸਮੱਗਰੀ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ਸਮੱਗਰੀ.extend(덩이)
                return bytes(ਸਮੱਗਰੀ)
            def 화면인증(ਪਾਸਵਰਡ_ਕੀਮਤ):
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ=socket.create_connection(('127.0.0.5',화면포트),10);ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.settimeout(30)
                assert 정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,12)==b'RFB 003.008\n'
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(b'RFB 003.008\n');assert 정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,2)==b'\x01\x02'
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(b'\x02');ਚੈਲੇਂਜ_ਕੀਮਤ=정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,16)
                입력암호=ਪਾਸਵਰਡ_ਕੀਮਤ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ਚੈਲੇਂਜ_ਕੀਮਤ))
                ਸਥਿਤੀ_ਕੀਮਤ=struct.unpack('!I',정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,4))[0]
                return ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,ਸਥਿਤੀ_ਕੀਮਤ
            ਅਯੋਗ_ਪਾਸਵਰਡ='!' if not ਸੈਟਿੰਗ['vnc_password'].startswith('!') else '?'
            ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,ਸਥਿਤੀ_ਕੀਮਤ=화면인증(ਅਯੋਗ_ਪਾਸਵਰਡ);assert ਸਥਿਤੀ_ਕੀਮਤ==1;ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close();time.sleep(.6)
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('VNC incorrect password rejected')
            ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,ਸਥਿਤੀ_ਕੀਮਤ=화면인증(ਸੈਟਿੰਗ['vnc_password']);assert ਸਥਿਤੀ_ਕੀਮਤ==0
            with ਕੁਨੈਕਸ਼ਨ_ਕਰੋ:
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(b'\x01');초기=정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,24);너비,높이=struct.unpack('!HH',초기[:4]);ਨਾਂ=정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ਨਾਂ
                def 화면(증분=0):
                    ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ਕੌਔਰਡੀਨੇਟ,세로좌표,영역너비,영역높이,ਮੈਥਡ_ਮੋਡ=struct.unpack('!HHHHi',정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,12));assert ਮੈਥਡ_ਮੋਡ==0 and x_ਕੌਔਰਡੀਨੇਟ+영역너비<=너비 and 세로좌표+영역높이<=높이
                        ਬਿੰਦੂ=정확히(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ,영역너비*영역높이*4);합계+=len(ਬਿੰਦੂ)
                        for ਲਾਈਨ in range(영역높이):ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ[((세로좌표+ਲਾਈਨ)*너비+x_ਕੌਔਰਡੀਨੇਟ)*4:((세로좌표+ਲਾਈਨ)*너비+x_ਕੌਔਰਡੀਨੇਟ+영역너비)*4]=ਬਿੰਦੂ[ਲਾਈਨ*영역너비*4:(ਲਾਈਨ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ),'raw','BGRX').save(str(ਆਉਟਪੁੱਟ/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('RFB incremental update')
                처음=len(ਲੌਗ_ਕਤਾਰ)
                for ਵਰਣ_ਕੀਮਤ in 'echo VNC_NATIVE_PASS\r':
                    ਪ੍ਰਤੀਕ=0xff0d if ਵਰਣ_ਕੀਮਤ=='\r' else ord(ਵਰਣ_ਕੀਮਤ)
                    ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(struct.pack('!BBHI',4,1,0,ਪ੍ਰਤੀਕ));ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(struct.pack('!BBHI',4,0,0,ਪ੍ਰਤੀਕ))
                기다림(b'VNC_NATIVE_PASS',처음)
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ਪ੍ਰਤੀਕ,누름=1):ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(struct.pack('!BBHI',4,누름,0,ਪ੍ਰਤੀਕ))
                처음=len(ਲੌਗ_ਕਤਾਰ)
                for ਵਰਣ_ਕੀਮਤ in 'echo ':글쇠(ord(ਵਰਣ_ਕੀਮਤ))
                글쇠(0xffc6)
                for ਵਰਣ_ਕੀਮਤ in 'gksrmf':글쇠(ord(ਵਰਣ_ਕੀਮਤ))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Native VNC F9 two-set Hangul composition')
                ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.sendall(struct.pack('!BBHH',5,0,120,100))
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('VNC pointer input accepted')
            ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.write(b'poweroff\n');ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.flush();ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=15);assert ਕਾਰਵਾਈ_ਕੀਮਤ.returncode==0
            ਵਿਵਰਨ_ਕੀਮਤ['passed']=True
    finally:
        if ਕਾਰਵਾਈ_ਕੀਮਤ and ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
            ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try: ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=5)
            except subprocess.TimeoutExpired: ਕਾਰਵਾਈ_ਕੀਮਤ.kill();ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
        (ਆਉਟਪੁੱਟ/'serial.log').write_bytes(ਲੌਗ_ਕਤਾਰ)
        (ਆਉਟਪੁੱਟ/'report.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ,ensure_ascii=False,indent=2))


if __name__=='__main__': ਚਲਾਓ_2()
