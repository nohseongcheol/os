#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ተግብር_ትእዛዝ import 기준, ትእዛዝ
from 통신다리 import 통신다리


def ኣኺድ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    ኣቀማምጣታት = json.loads(인수.access.read_text())
    ጸብጻብ_ዋጋ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ባዶ_ወደብ():
        with socket.socket() as ኣላግብ:
            ኣላግብ.bind(('127.0.0.5', 0))
            return ኣላግብ.getsockname()[1]
    ሽፋን_ወደብ, 화면포트, ፋይል_ወደብ = ባዶ_ወደብ(), ባዶ_ወደብ(), ባዶ_ወደብ()
    ምዝጉብ_ሪጋ = bytearray()
    መስርሕ_ዋጋ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(ፋይል_ወደብ,
                ['tcp:{}:22'.format(ሽፋን_ወደብ), 'tcp:{}:5900'.format(화면포트)], አዐንግድ_ኣድራሻ='127.0.0.5') as 다리:
            실행인수 = ትእዛዝ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            መስርሕ_ዋጋ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ሓበሬታ = መስርሕ_ዋጋ.stdout.read(4096)
                    if not ሓበሬታ: break
                    ምዝጉብ_ሪጋ.extend(ሓበሬታ)
            ፈትሊ_ዋጋ = threading.Thread(target=수집, daemon=True)
            ፈትሊ_ዋጋ.start()
            def 기다림(ናይ_ቃል_ጸወታ_ጽሑፍ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ናይ_ቃል_ጸወታ_ጽሑፍ not in ምዝጉብ_ሪጋ[처음:]:
                    if time.monotonic()>끝 or መስርሕ_ዋጋ.poll() is not None:
                        raise AssertionError('Missing '+repr(ናይ_ቃል_ጸወታ_ጽሑፍ)+'\n'+ምዝጉብ_ሪጋ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ውሑስ_ሽፋን(መሕለፊ_ቃል_ዋጋ, መምርሒ_ዋጋ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=መሕለፊ_ቃል_ዋጋ
                인수=['ssh','-v']+list(추가)+['-p',str(ሽፋን_ወደብ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',መምርሒ_ዋጋ]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=ውሑስ_ሽፋን('!' + ኣቀማምጣታት['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in ምዝጉብ_ሪጋ, 결과.stderr
            ጸብጻብ_ዋጋ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=ውሑስ_ሽፋን(ኣቀማምጣታት['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ጸብጻብ_ዋጋ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ጸብጻብ_ዋጋ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=ውሑስ_ሽፋን(ኣቀማምጣታት['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ጸብጻብ_ዋጋ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=ውሑስ_ሽፋን(ኣቀማምጣታት['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ጸብጻብ_ዋጋ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=ውሑስ_ሽፋን(ኣቀማምጣታት['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ጸብጻብ_ዋጋ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ሽፋን_ወደብ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ምሩጽ_ዋጋ=selectors.DefaultSelector();ምሩጽ_ዋጋ.register(ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.stdout,selectors.EVENT_READ)
            def 대화읽기(ኣርእይ_ዋጋ):
                마감=time.monotonic()+30
                while ኣርእይ_ዋጋ not in 대화기록:
                    if time.monotonic()>마감 or ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ኣርእይ_ዋጋ)+' '+repr(bytes(대화기록)))
                    for ምእታው_ዋጋ,_ in ምሩጽ_ዋጋ.select(.1):
                        조각=ምእታው_ዋጋ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.stdin.write(b'\x04');ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.stdin.flush();나머지,ጌጋ=ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.communicate(timeout=15)
                assert ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.returncode==0 and b'PTY allocation request failed' not in ጌጋ,(ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.returncode,ጌጋ)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ምሩጽ_ዋጋ.close()
                if ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.poll() is None:ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.kill();ንተጠቃሚ_ቀሊል_ክፍለ_ግዘ.wait()
            ጸብጻብ_ዋጋ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ኣላግብ, 수):
                ሓበሬታ=bytearray()
                while len(ሓበሬታ)<수:
                    덩이=ኣላግብ.recv(수-len(ሓበሬታ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ሓበሬታ.extend(덩이)
                return bytes(ሓበሬታ)
            def 화면인증(መሕለፊ_ቃል_ዋጋ):
                ኣላግብ=socket.create_connection(('127.0.0.5',화면포트),10);ኣላግብ.settimeout(30)
                assert 정확히(ኣላግብ,12)==b'RFB 003.008\n'
                ኣላግብ.sendall(b'RFB 003.008\n');assert 정확히(ኣላግብ,2)==b'\x01\x02'
                ኣላግብ.sendall(b'\x02');ፈተና_ዋጋ=정확히(ኣላግብ,16)
                입력암호=መሕለፊ_ቃል_ዋጋ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ኣላግብ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ፈተና_ዋጋ))
                ደረጃ_ዋጋ=struct.unpack('!I',정확히(ኣላግብ,4))[0]
                return ኣላግብ,ደረጃ_ዋጋ
            ዘይቅቡል_መሕለፊ_ቃል='!' if not ኣቀማምጣታት['vnc_password'].startswith('!') else '?'
            ኣላግብ,ደረጃ_ዋጋ=화면인증(ዘይቅቡል_መሕለፊ_ቃል);assert ደረጃ_ዋጋ==1;ኣላግብ.close();time.sleep(.6)
            ጸብጻብ_ዋጋ['checks'].append('VNC incorrect password rejected')
            ኣላግብ,ደረጃ_ዋጋ=화면인증(ኣቀማምጣታት['vnc_password']);assert ደረጃ_ዋጋ==0
            with ኣላግብ:
                ኣላግብ.sendall(b'\x01');초기=정확히(ኣላግብ,24);너비,높이=struct.unpack('!HH',초기[:4]);ሽም=정확히(ኣላግብ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ሽም
                def 화면(증분=0):
                    ኣላግብ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ኣላግብ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ስእሊ_ዋጋ=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,ሜላ_ኹነት=struct.unpack('!HHHHi',정확히(ኣላግብ,12));assert ሜላ_ኹነት==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        ንጣብ=정확히(ኣላግብ,영역너비*영역높이*4);합계+=len(ንጣብ)
                        for መስመር in range(영역높이):ስእሊ_ዋጋ[((세로좌표+መስመር)*너비+가로좌표)*4:((세로좌표+መስመር)*너비+가로좌표+영역너비)*4]=ንጣብ[መስመር*영역너비*4:(መስመር+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ስእሊ_ዋጋ),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ጸብጻብ_ዋጋ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ጸብጻብ_ዋጋ['checks'].append('RFB incremental update')
                처음=len(ምዝጉብ_ሪጋ)
                for ፊደል_ዋጋ in 'echo VNC_NATIVE_PASS\r':
                    ምልክት=0xff0d if ፊደል_ዋጋ=='\r' else ord(ፊደል_ዋጋ)
                    ኣላግብ.sendall(struct.pack('!BBHI',4,1,0,ምልክት));ኣላግብ.sendall(struct.pack('!BBHI',4,0,0,ምልክት))
                기다림(b'VNC_NATIVE_PASS',처음)
                ጸብጻብ_ዋጋ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ምልክት,누름=1):ኣላግብ.sendall(struct.pack('!BBHI',4,누름,0,ምልክት))
                처음=len(ምዝጉብ_ሪጋ)
                for ፊደል_ዋጋ in 'echo ':글쇠(ord(ፊደል_ዋጋ))
                글쇠(0xffc6)
                for ፊደል_ዋጋ in 'gksrmf':글쇠(ord(ፊደል_ዋጋ))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ጸብጻብ_ዋጋ['checks'].append('Native VNC F9 two-set Hangul composition')
                ኣላግብ.sendall(struct.pack('!BBHH',5,0,120,100))
                ጸብጻብ_ዋጋ['checks'].append('VNC pointer input accepted')
            መስርሕ_ዋጋ.stdin.write(b'poweroff\n');መስርሕ_ዋጋ.stdin.flush();መስርሕ_ዋጋ.wait(timeout=15);assert መስርሕ_ዋጋ.returncode==0
            ጸብጻብ_ዋጋ['passed']=True
    finally:
        if መስርሕ_ዋጋ and መስርሕ_ዋጋ.poll() is None:
            መስርሕ_ዋጋ.terminate()
            try: መስርሕ_ዋጋ.wait(timeout=5)
            except subprocess.TimeoutExpired: መስርሕ_ዋጋ.kill();መስርሕ_ዋጋ.wait()
        (출력/'serial.log').write_bytes(ምዝጉብ_ሪጋ)
        (출력/'report.json').write_text(json.dumps(ጸብጻብ_ዋጋ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ጸብጻብ_ዋጋ,ensure_ascii=False,indent=2))


if __name__=='__main__': ኣኺድ()
