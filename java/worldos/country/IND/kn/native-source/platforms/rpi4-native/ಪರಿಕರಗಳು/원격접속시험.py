#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ
from ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ import ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--kernel', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--access', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ / 'build/remote/access.json')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--output', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/native-remote')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ಔಟ್_ಪುಟ್ = 인수.output
    ಔಟ್_ಪುಟ್.mkdir(parents=True, exist_ok=True)
    ಸಿದ್ಧತೆಗಳು = json.loads(인수.access.read_text())
    ವರದಿ_ಮೌಲ್ಯ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ಖಾಲಿ_ಪೋರ್ಟ್():
        with socket.socket() as ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು:
            ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.bind(('127.0.0.5', 0))
            return ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getsockname()[1]
    ಶೆಲ್_ಪೋರ್ಟ್, 화면포트, ಫೈಲ್_ಪೋರ್ಟ್ = ಖಾಲಿ_ಪೋರ್ಟ್(), ಖಾಲಿ_ಪೋರ್ಟ್(), ಖಾಲಿ_ಪೋರ್ಟ್()
    ಲಾಗ್_ದಾಖಲೆ = bytearray()
    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ(ಫೈಲ್_ಪೋರ್ಟ್,
                ['tcp:{}:22'.format(ಶೆಲ್_ಪೋರ್ಟ್), 'tcp:{}:5900'.format(화면포트)], ಹೋಸ್ಟ್_ಇಮೇಲ್='127.0.0.5') as ಸೇತುವೆ_ಮೌಲ್ಯ:
            실행인수 = ಆಜ್ಞೆ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ಸೇತುವೆ_ಮೌಲ್ಯ.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ಡೇಟಾ = ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout.read(4096)
                    if not ಡೇಟಾ: break
                    ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
            ಎಳೆ_ಮೌಲ್ಯ = threading.Thread(target=수집, daemon=True)
            ಎಳೆ_ಮೌಲ್ಯ.start()
            def ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(ಪದ_ಪಠ್ಯ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ಪದ_ಪಠ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[처음:]:
                    if time.monotonic()>끝 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                        raise AssertionError('Missing '+repr(ಪದ_ಪಠ್ಯ)+'\n'+ಲಾಗ್_ದಾಖಲೆ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ಸುರಕ್ಷಿತ_ಶೆಲ್(ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ, ಸೂಚನೆ_ಮೌಲ್ಯ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ
                인수=['ssh','-v']+list(추가)+['-p',str(ಶೆಲ್_ಪೋರ್ಟ್),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ಸೂಚನೆ_ಮೌಲ್ಯ]
                ಮಾಪನ=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ಮಾಪನ
            ಮಾಪನ=ಸುರಕ್ಷಿತ_ಶೆಲ್('!' + ಸಿದ್ಧತೆಗಳು['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ಔಟ್_ಪುಟ್/'ssh-rejected.log').write_bytes(ಮಾಪನ.stderr)
            assert ಮಾಪನ.returncode!=0 and b'Permission denied' in ಮಾಪನ.stderr and b'SHOULD_NOT_RUN' not in ಲಾಗ್_ದಾಖಲೆ, ಮಾಪನ.stderr
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ಮಾಪನ=ಸುರಕ್ಷಿತ_ಶೆಲ್(ಸಿದ್ಧತೆಗಳು['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ಔಟ್_ಪುಟ್/'ssh.log').write_bytes(ಮಾಪನ.stderr)
            (ಔಟ್_ಪುಟ್/'ssh-output.txt').write_bytes(ಮಾಪನ.stdout)
            assert ಮಾಪನ.returncode==0 and b'SSH_NATIVE_PASS' in ಮಾಪನ.stdout, (ಮಾಪನ.returncode,ಮಾಪನ.stdout,ಮಾಪನ.stderr)
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ಮಾಪನ.stderr, ಮಾಪನ.stderr
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ಮಾಪನ=ಸುರಕ್ಷಿತ_ಶೆಲ್(ಸಿದ್ಧತೆಗಳು['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ಮಾಪನ.returncode==0 and 'JAVA ಔಟ್_ಪುಟ್: 안녕하세요 😀'.encode() in ಮಾಪನ.stdout,ಮಾಪನ.stdout
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ಮಾಪನ=ಸುರಕ್ಷಿತ_ಶೆಲ್(ಸಿದ್ಧತೆಗಳು['ssh_password'], 'missing_remote_command')
            assert ಮಾಪನ.returncode==127,ಮಾಪನ.returncode
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ಮಾಪನ=ಸುರಕ್ಷಿತ_ಶೆಲ್(ಸಿದ್ಧತೆಗಳು['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ಔಟ್_ಪುಟ್/'ssh-rekey.log').write_bytes(ಮಾಪನ.stderr)
            assert ಮಾಪನ.returncode==0 and 'class 창예제'.encode() in ಮಾಪನ.stdout, (ಮಾಪನ.returncode,ಮಾಪನ.stdout,ಮಾಪನ.stderr)
            assert ಮಾಪನ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ಮಾಪನ.stderr
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ಶೆಲ್_ಪೋರ್ಟ್),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ಸಂವಾದಕ_ಸೆಷನ್=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ಆಯ್ಕೆ_ಮೌಲ್ಯ=selectors.DefaultSelector();ಆಯ್ಕೆ_ಮೌಲ್ಯ.register(ಸಂವಾದಕ_ಸೆಷನ್.stdout,selectors.EVENT_READ)
            def 대화읽기(ಶೋ_ಮೌಲ್ಯ):
                마감=time.monotonic()+30
                while ಶೋ_ಮೌಲ್ಯ not in 대화기록:
                    if time.monotonic()>마감 or ಸಂವಾದಕ_ಸೆಷನ್.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ಶೋ_ಮೌಲ್ಯ)+' '+repr(bytes(대화기록)))
                    for ನಮೂದು_ಮೌಲ್ಯ,_ in ಆಯ್ಕೆ_ಮೌಲ್ಯ.select(.1):
                        조각=ನಮೂದು_ಮೌಲ್ಯ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ಸಂವಾದಕ_ಸೆಷನ್.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ಸಂವಾದಕ_ಸೆಷನ್.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ಸಂವಾದಕ_ಸೆಷನ್.stdin.write(b'\x04');ಸಂವಾದಕ_ಸೆಷನ್.stdin.flush();나머지,ದೋಷ=ಸಂವಾದಕ_ಸೆಷನ್.communicate(timeout=15)
                assert ಸಂವಾದಕ_ಸೆಷನ್.returncode==0 and b'PTY allocation request failed' not in ದೋಷ,(ಸಂವಾದಕ_ಸೆಷನ್.returncode,ದೋಷ)
                (ಔಟ್_ಪುಟ್/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ಆಯ್ಕೆ_ಮೌಲ್ಯ.close()
                if ಸಂವಾದಕ_ಸೆಷನ್.poll() is None:ಸಂವಾದಕ_ಸೆಷನ್.kill();ಸಂವಾದಕ_ಸೆಷನ್.wait()
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು, 수):
                ಡೇಟಾ=bytearray()
                while len(ಡೇಟಾ)<수:
                    덩이=ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.recv(수-len(ಡೇಟಾ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ಡೇಟಾ.extend(덩이)
                return bytes(ಡೇಟಾ)
            def 화면인증(ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ):
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು=socket.create_connection(('127.0.0.5',화면포트),10);ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.settimeout(30)
                assert 정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,12)==b'RFB 003.008\n'
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(b'RFB 003.008\n');assert 정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,2)==b'\x01\x02'
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(b'\x02');ಸವಾಲು_ಮೌಲ್ಯ=정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,16)
                입력암호=ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ಸವಾಲು_ಮೌಲ್ಯ))
                ಸ್ಥಿತಿ_ಮೌಲ್ಯ=struct.unpack('!I',정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,4))[0]
                return ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,ಸ್ಥಿತಿ_ಮೌಲ್ಯ
            ಅಮಾನ್ಯ_ಪಾಸ್_ವರ್ಡ್='!' if not ಸಿದ್ಧತೆಗಳು['vnc_password'].startswith('!') else '?'
            ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,ಸ್ಥಿತಿ_ಮೌಲ್ಯ=화면인증(ಅಮಾನ್ಯ_ಪಾಸ್_ವರ್ಡ್);assert ಸ್ಥಿತಿ_ಮೌಲ್ಯ==1;ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close();time.sleep(.6)
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('VNC incorrect password rejected')
            ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,ಸ್ಥಿತಿ_ಮೌಲ್ಯ=화면인증(ಸಿದ್ಧತೆಗಳು['vnc_password']);assert ಸ್ಥಿತಿ_ಮೌಲ್ಯ==0
            with ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು:
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(b'\x01');초기=정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,24);너비,높이=struct.unpack('!HH',초기[:4]);ಹೆಸರು=정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ಹೆಸರು
                def 화면(증분=0):
                    ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ,영역너비,영역높이,ವಿಧಾನ_ಮೋಡ್=struct.unpack('!HHHHi',정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,12));assert ವಿಧಾನ_ಮೋಡ್==0 and x_ಸಮಭಾಜಕ+영역너비<=너비 and Y_ಬಟನ್_ಸಮನ್ವಯ+영역높이<=높이
                        ಪೆಲ್=정확히(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು,영역너비*영역높이*4);합계+=len(ಪೆಲ್)
                        for ಸಾಲು in range(영역높이):ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ[((Y_ಬಟನ್_ಸಮನ್ವಯ+ಸಾಲು)*너비+x_ಸಮಭಾಜಕ)*4:((Y_ಬಟನ್_ಸಮನ್ವಯ+ಸಾಲು)*너비+x_ಸಮಭಾಜಕ+영역너비)*4]=ಪೆಲ್[ಸಾಲು*영역너비*4:(ಸಾಲು+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ),'raw','BGRX').save(str(ಔಟ್_ಪುಟ್/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('RFB incremental update')
                처음=len(ಲಾಗ್_ದಾಖಲೆ)
                for ಅಕ್ಷರ_ಮೌಲ್ಯ in 'echo VNC_NATIVE_PASS\r':
                    ಚಿಹ್ನೆ=0xff0d if ಅಕ್ಷರ_ಮೌಲ್ಯ=='\r' else ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)
                    ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(struct.pack('!BBHI',4,1,0,ಚಿಹ್ನೆ));ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(struct.pack('!BBHI',4,0,0,ಚಿಹ್ನೆ))
                ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(b'VNC_NATIVE_PASS',처음)
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ಚಿಹ್ನೆ,누름=1):ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(struct.pack('!BBHI',4,누름,0,ಚಿಹ್ನೆ))
                처음=len(ಲಾಗ್_ದಾಖಲೆ)
                for ಅಕ್ಷರ_ಮೌಲ್ಯ in 'echo ':글쇠(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ))
                글쇠(0xffc6)
                for ಅಕ್ಷರ_ಮೌಲ್ಯ in 'gksrmf':글쇠(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ))
                글쇠(0xffc6);글쇠(0xff0d)
                ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('\r\n한글\r\n'.encode(),처음)
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Native VNC F9 two-set Hangul composition')
                ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.sendall(struct.pack('!BBHH',5,0,120,100))
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('VNC pointer input accepted')
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.write(b'poweroff\n');ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.flush();ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=15);assert ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.returncode==0
            ವರದಿ_ಮೌಲ್ಯ['passed']=True
    finally:
        if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ and ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try: ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=5)
            except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill();ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
        (ಔಟ್_ಪುಟ್/'serial.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ)
        (ಔಟ್_ಪುಟ್/'report.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ವರದಿ_ಮೌಲ್ಯ,ensure_ascii=False,indent=2))


if __name__=='__main__': ಚಲಾಯಿಸು_2()
