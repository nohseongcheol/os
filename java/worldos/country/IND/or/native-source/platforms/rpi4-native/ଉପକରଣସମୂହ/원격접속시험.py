#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ
from ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍ import ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍


def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    ନିର୍ଗମ = 인수.output
    ନିର୍ଗମ.mkdir(parents=True, exist_ok=True)
    ବିନ୍ଯାସ = json.loads(인수.access.read_text())
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ଖାଲି_ପୋର୍ଟ():
        with socket.socket() as ସଂଯୋଗ_କରନ୍ତୁ:
            ସଂଯୋଗ_କରନ୍ତୁ.bind(('127.0.0.5', 0))
            return ସଂଯୋଗ_କରନ୍ତୁ.getsockname()[1]
    ଖୋଳ_ପୋର୍ଟ, 화면포트, ଫାଇଲ୍_ପୋର୍ଟ = ଖାଲି_ପୋର୍ଟ(), ଖାଲି_ପୋର୍ଟ(), ଖାଲି_ପୋର୍ଟ()
    ଲଗ୍_ଧାଡ଼ି = bytearray()
    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍(ଫାଇଲ୍_ପୋର୍ଟ,
                ['tcp:{}:22'.format(ଖୋଳ_ପୋର୍ଟ), 'tcp:{}:5900'.format(화면포트)], ଆୟୋଜକ_ଠିକଣା='127.0.0.5') as ବ୍ରିଜ୍_ମୂଲ୍ୟ:
            실행인수 = ନିର୍ଦ୍ଦେଶ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ବ୍ରିଜ୍_ମୂଲ୍ୟ.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ଡାଟା = ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout.read(4096)
                    if not ଡାଟା: break
                    ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
            ଧାରା_ମୂଲ୍ୟ = threading.Thread(target=수집, daemon=True)
            ଧାରା_ମୂଲ୍ୟ.start()
            def ଅପେକ୍ଷା_ସ୍ଥିତି(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in ଲଗ୍_ଧାଡ଼ି[처음:]:
                    if time.monotonic()>끝 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+ଲଗ୍_ଧାଡ଼ି[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ଅପେକ୍ଷା_ସ୍ଥିତି(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ସୁରକ୍ଷିତ_ଖୋଳ(ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ, ପରାମର୍ଶ_ମୂଲ୍ୟ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ
                인수=['ssh','-v']+list(추가)+['-p',str(ଖୋଳ_ପୋର୍ଟ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ପରାମର୍ଶ_ମୂଲ୍ୟ]
                ମାପ=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ମାପ
            ମାପ=ସୁରକ୍ଷିତ_ଖୋଳ('!' + ବିନ୍ଯାସ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ନିର୍ଗମ/'ssh-rejected.log').write_bytes(ମାପ.stderr)
            assert ମାପ.returncode!=0 and b'Permission denied' in ମାପ.stderr and b'SHOULD_NOT_RUN' not in ଲଗ୍_ଧାଡ଼ି, ମାପ.stderr
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ମାପ=ସୁରକ୍ଷିତ_ଖୋଳ(ବିନ୍ଯାସ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ନିର୍ଗମ/'ssh.log').write_bytes(ମାପ.stderr)
            (ନିର୍ଗମ/'ssh-output.txt').write_bytes(ମାପ.stdout)
            assert ମାପ.returncode==0 and b'SSH_NATIVE_PASS' in ମାପ.stdout, (ମାପ.returncode,ମାପ.stdout,ମାପ.stderr)
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ମାପ.stderr, ମାପ.stderr
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ମାପ=ସୁରକ୍ଷିତ_ଖୋଳ(ବିନ୍ଯାସ['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ମାପ.returncode==0 and 'JAVA ନିର୍ଗମ: 안녕하세요 😀'.encode() in ମାପ.stdout,ମାପ.stdout
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ମାପ=ସୁରକ୍ଷିତ_ଖୋଳ(ବିନ୍ଯାସ['ssh_password'], 'missing_remote_command')
            assert ମାପ.returncode==127,ମାପ.returncode
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ମାପ=ସୁରକ୍ଷିତ_ଖୋଳ(ବିନ୍ଯାସ['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ନିର୍ଗମ/'ssh-rekey.log').write_bytes(ମାପ.stderr)
            assert ମାପ.returncode==0 and 'class 창예제'.encode() in ମାପ.stdout, (ମାପ.returncode,ମାପ.stdout,ମାପ.stderr)
            assert ମାପ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ମାପ.stderr
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ଖୋଳ_ପୋର୍ଟ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ଚୟନ_ମୂଲ୍ୟ=selectors.DefaultSelector();ଚୟନ_ମୂଲ୍ୟ.register(ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.stdout,selectors.EVENT_READ)
            def 대화읽기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ):
                마감=time.monotonic()+30
                while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in 대화기록:
                    if time.monotonic()>마감 or ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ)+' '+repr(bytes(대화기록)))
                    for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ,_ in ଚୟନ_ମୂଲ୍ୟ.select(.1):
                        조각=ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.stdin.write(b'\x04');ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.stdin.flush();나머지,ତ୍ରୁଟି=ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.communicate(timeout=15)
                assert ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.returncode==0 and b'PTY allocation request failed' not in ତ୍ରୁଟି,(ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.returncode,ତ୍ରୁଟି)
                (ନିର୍ଗମ/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ଚୟନ_ମୂଲ୍ୟ.close()
                if ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.poll() is None:ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.kill();ଆଦାନ_ପ୍ରଦାନ_ଯୋଗ୍ୟ_ଅଧିବେଶନ.wait()
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ସଂଯୋଗ_କରନ୍ତୁ, 수):
                ଡାଟା=bytearray()
                while len(ଡାଟା)<수:
                    덩이=ସଂଯୋଗ_କରନ୍ତୁ.recv(수-len(ଡାଟା))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ଡାଟା.extend(덩이)
                return bytes(ଡାଟା)
            def 화면인증(ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ):
                ସଂଯୋଗ_କରନ୍ତୁ=socket.create_connection(('127.0.0.5',화면포트),10);ସଂଯୋଗ_କରନ୍ତୁ.settimeout(30)
                assert 정확히(ସଂଯୋଗ_କରନ୍ତୁ,12)==b'RFB 003.008\n'
                ସଂଯୋଗ_କରନ୍ତୁ.sendall(b'RFB 003.008\n');assert 정확히(ସଂଯୋଗ_କରନ୍ତୁ,2)==b'\x01\x02'
                ସଂଯୋଗ_କରନ୍ତୁ.sendall(b'\x02');ଚ୍ୟାଲେଞ୍ଜ୍_ମୂଲ୍ୟ=정확히(ସଂଯୋଗ_କରନ୍ତୁ,16)
                입력암호=ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ସଂଯୋଗ_କରନ୍ତୁ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ଚ୍ୟାଲେଞ୍ଜ୍_ମୂଲ୍ୟ))
                ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1=struct.unpack('!I',정확히(ସଂଯୋଗ_କରନ୍ତୁ,4))[0]
                return ସଂଯୋଗ_କରନ୍ତୁ,ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1
            ଅବୈଧ_ପାସ୍_ୱାର୍ଡ୍='!' if not ବିନ୍ଯାସ['vnc_password'].startswith('!') else '?'
            ସଂଯୋଗ_କରନ୍ତୁ,ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1=화면인증(ଅବୈଧ_ପାସ୍_ୱାର୍ଡ୍);assert ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1==1;ସଂଯୋଗ_କରନ୍ତୁ.close();time.sleep(.6)
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('VNC incorrect password rejected')
            ସଂଯୋଗ_କରନ୍ତୁ,ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1=화면인증(ବିନ୍ଯାସ['vnc_password']);assert ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1==0
            with ସଂଯୋଗ_କରନ୍ତୁ:
                ସଂଯୋଗ_କରନ୍ତୁ.sendall(b'\x01');초기=정확히(ସଂଯୋଗ_କରନ୍ତୁ,24);너비,높이=struct.unpack('!HH',초기[:4]);ନାମ=정확히(ସଂଯୋଗ_କରନ୍ତୁ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ନାମ
                def 화면(증분=0):
                    ସଂଯୋଗ_କରନ୍ତୁ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ସଂଯୋଗ_କରନ୍ତୁ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ଅଙ୍କନ_ମୂଲ୍ୟ=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ସଂଯୋଜନ,세로좌표,영역너비,영역높이,ପଦ୍ଧତି_ମୋଡ୍=struct.unpack('!HHHHi',정확히(ସଂଯୋଗ_କରନ୍ତୁ,12));assert ପଦ୍ଧତି_ମୋଡ୍==0 and x_ସଂଯୋଜନ+영역너비<=너비 and 세로좌표+영역높이<=높이
                        ପିକ୍ସେଲ୍=정확히(ସଂଯୋଗ_କରନ୍ତୁ,영역너비*영역높이*4);합계+=len(ପିକ୍ସେଲ୍)
                        for ରେଖା in range(영역높이):ଅଙ୍କନ_ମୂଲ୍ୟ[((세로좌표+ରେଖା)*너비+x_ସଂଯୋଜନ)*4:((세로좌표+ରେଖା)*너비+x_ସଂଯୋଜନ+영역너비)*4]=ପିକ୍ସେଲ୍[ରେଖା*영역너비*4:(ରେଖା+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ଅଙ୍କନ_ମୂଲ୍ୟ),'raw','BGRX').save(str(ନିର୍ଗମ/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('RFB incremental update')
                처음=len(ଲଗ୍_ଧାଡ଼ି)
                for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 'echo VNC_NATIVE_PASS\r':
                    ସଙ୍କେତ=0xff0d if ବର୍ଣ୍ଣ_ମୂଲ୍ୟ=='\r' else ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)
                    ସଂଯୋଗ_କରନ୍ତୁ.sendall(struct.pack('!BBHI',4,1,0,ସଙ୍କେତ));ସଂଯୋଗ_କରନ୍ତୁ.sendall(struct.pack('!BBHI',4,0,0,ସଙ୍କେତ))
                ଅପେକ୍ଷା_ସ୍ଥିତି(b'VNC_NATIVE_PASS',처음)
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ସଙ୍କେତ,누름=1):ସଂଯୋଗ_କରନ୍ତୁ.sendall(struct.pack('!BBHI',4,누름,0,ସଙ୍କେତ))
                처음=len(ଲଗ୍_ଧାଡ଼ି)
                for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 'echo ':글쇠(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ))
                글쇠(0xffc6)
                for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 'gksrmf':글쇠(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ))
                글쇠(0xffc6);글쇠(0xff0d)
                ଅପେକ୍ଷା_ସ୍ଥିତି('\r\n한글\r\n'.encode(),처음)
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Native VNC F9 two-set Hangul composition')
                ସଂଯୋଗ_କରନ୍ତୁ.sendall(struct.pack('!BBHH',5,0,120,100))
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('VNC pointer input accepted')
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.write(b'poweroff\n');ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.flush();ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=15);assert ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.returncode==0
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed']=True
    finally:
        if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ and ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try: ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=5)
            except subprocess.TimeoutExpired: ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill();ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
        (ନିର୍ଗମ/'serial.log').write_bytes(ଲଗ୍_ଧାଡ଼ି)
        (ନିର୍ଗମ/'report.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ,ensure_ascii=False,indent=2))


if __name__=='__main__': ଚଳାନ୍ତୁ()
