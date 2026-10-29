#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ
from መረብ_ድልድይ import መረብ_ድልድይ


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--kernel', type=Path, default=አሳይ_ስር / 'build/kernel8.img')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--access', type=Path, default=አሳይ_ስር / 'build/remote/access.json')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--output', type=Path, default=አሳይ_ስር / 'build/verification/native-remote')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    ውጤት = 인수.output
    ውጤት.mkdir(parents=True, exist_ok=True)
    ማሰናጃዎች = json.loads(인수.access.read_text())
    ዘገባ_እሴት = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ባዶ_ወደብ():
        with socket.socket() as መገናኛ:
            መገናኛ.bind(('127.0.0.5', 0))
            return መገናኛ.getsockname()[1]
    ሼል_ወደብ, 화면포트, ፋይል_ወደብ = ባዶ_ወደብ(), ባዶ_ወደብ(), ባዶ_ወደብ()
    መዝግብ_ረድፍ = bytearray()
    ሂደት_እሴት = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, መረብ_ድልድይ(ፋይል_ወደብ,
                ['tcp:{}:22'.format(ሼል_ወደብ), 'tcp:{}:5900'.format(화면포트)], አዘጋጅ_አድራሻ='127.0.0.5') as ድልድይ_እሴት:
            실행인수 = ትእዛዝ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            ሂደት_እሴት = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ድልድይ_እሴት.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ውሂብ = ሂደት_እሴት.stdout.read(4096)
                    if not ውሂብ: break
                    መዝግብ_ረድፍ.extend(ውሂብ)
            ክር_እሴት = threading.Thread(target=수집, daemon=True)
            ክር_እሴት.start()
            def መጠበቅ_ዞን(ቃል_ጽሁፍ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ቃል_ጽሁፍ not in መዝግብ_ረድፍ[처음:]:
                    if time.monotonic()>끝 or ሂደት_እሴት.poll() is not None:
                        raise AssertionError('Missing '+repr(ቃል_ጽሁፍ)+'\n'+መዝግብ_ረድፍ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            መጠበቅ_ዞን(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ደህንነቱ_የተጠበቀ_ሼል(የይለፍ_ቃል_እሴት, መምሪያ_እሴት, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=የይለፍ_ቃል_እሴት
                인수=['ssh','-v']+list(추가)+['-p',str(ሼል_ወደብ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',መምሪያ_እሴት]
                ልኬት=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ልኬት
            ልኬት=ደህንነቱ_የተጠበቀ_ሼል('!' + ማሰናጃዎች['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ውጤት/'ssh-rejected.log').write_bytes(ልኬት.stderr)
            assert ልኬት.returncode!=0 and b'Permission denied' in ልኬት.stderr and b'SHOULD_NOT_RUN' not in መዝግብ_ረድፍ, ልኬት.stderr
            ዘገባ_እሴት['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ልኬት=ደህንነቱ_የተጠበቀ_ሼል(ማሰናጃዎች['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ውጤት/'ssh.log').write_bytes(ልኬት.stderr)
            (ውጤት/'ssh-output.txt').write_bytes(ልኬት.stdout)
            assert ልኬት.returncode==0 and b'SSH_NATIVE_PASS' in ልኬት.stdout, (ልኬት.returncode,ልኬት.stdout,ልኬት.stderr)
            ዘገባ_እሴት['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ልኬት.stderr, ልኬት.stderr
            ዘገባ_እሴት['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ልኬት=ደህንነቱ_የተጠበቀ_ሼል(ማሰናጃዎች['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ልኬት.returncode==0 and 'JAVA ውጤት: 안녕하세요 😀'.encode() in ልኬት.stdout,ልኬት.stdout
            ዘገባ_እሴት['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ልኬት=ደህንነቱ_የተጠበቀ_ሼል(ማሰናጃዎች['ssh_password'], 'missing_remote_command')
            assert ልኬት.returncode==127,ልኬት.returncode
            ዘገባ_እሴት['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ልኬት=ደህንነቱ_የተጠበቀ_ሼል(ማሰናጃዎች['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ውጤት/'ssh-rekey.log').write_bytes(ልኬት.stderr)
            assert ልኬት.returncode==0 and 'class 창예제'.encode() in ልኬት.stdout, (ልኬት.returncode,ልኬት.stdout,ልኬት.stderr)
            assert ልኬት.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ልኬት.stderr
            ዘገባ_እሴት['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ሼል_ወደብ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            በይነተገናኝ_ክፍለ_ጊዜ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();የተመረጠ_እሴት=selectors.DefaultSelector();የተመረጠ_እሴት.register(በይነተገናኝ_ክፍለ_ጊዜ.stdout,selectors.EVENT_READ)
            def 대화읽기(አሳይ_እሴት):
                마감=time.monotonic()+30
                while አሳይ_እሴት not in 대화기록:
                    if time.monotonic()>마감 or በይነተገናኝ_ክፍለ_ጊዜ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(አሳይ_እሴት)+' '+repr(bytes(대화기록)))
                    for ምዝግብ_እሴት,_ in የተመረጠ_እሴት.select(.1):
                        조각=ምዝግብ_እሴት.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                በይነተገናኝ_ክፍለ_ጊዜ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');በይነተገናኝ_ክፍለ_ጊዜ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                በይነተገናኝ_ክፍለ_ጊዜ.stdin.write(b'\x04');በይነተገናኝ_ክፍለ_ጊዜ.stdin.flush();나머지,ስህተት=በይነተገናኝ_ክፍለ_ጊዜ.communicate(timeout=15)
                assert በይነተገናኝ_ክፍለ_ጊዜ.returncode==0 and b'PTY allocation request failed' not in ስህተት,(በይነተገናኝ_ክፍለ_ጊዜ.returncode,ስህተት)
                (ውጤት/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                የተመረጠ_እሴት.close()
                if በይነተገናኝ_ክፍለ_ጊዜ.poll() is None:በይነተገናኝ_ክፍለ_ጊዜ.kill();በይነተገናኝ_ክፍለ_ጊዜ.wait()
            ዘገባ_እሴት['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(መገናኛ, 수):
                ውሂብ=bytearray()
                while len(ውሂብ)<수:
                    덩이=መገናኛ.recv(수-len(ውሂብ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ውሂብ.extend(덩이)
                return bytes(ውሂብ)
            def 화면인증(የይለፍ_ቃል_እሴት):
                መገናኛ=socket.create_connection(('127.0.0.5',화면포트),10);መገናኛ.settimeout(30)
                assert 정확히(መገናኛ,12)==b'RFB 003.008\n'
                መገናኛ.sendall(b'RFB 003.008\n');assert 정확히(መገናኛ,2)==b'\x01\x02'
                መገናኛ.sendall(b'\x02');ተግዳሮት_እሴት=정확히(መገናኛ,16)
                입력암호=የይለፍ_ቃል_እሴት.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                መገናኛ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ተግዳሮት_እሴት))
                ዞን_እሴት=struct.unpack('!I',정확히(መገናኛ,4))[0]
                return መገናኛ,ዞን_እሴት
            ልክ_ያልኾነ_የይለፍ_ቃል='!' if not ማሰናጃዎች['vnc_password'].startswith('!') else '?'
            መገናኛ,ዞን_እሴት=화면인증(ልክ_ያልኾነ_የይለፍ_ቃል);assert ዞን_እሴት==1;መገናኛ.close();time.sleep(.6)
            ዘገባ_እሴት['checks'].append('VNC incorrect password rejected')
            መገናኛ,ዞን_እሴት=화면인증(ማሰናጃዎች['vnc_password']);assert ዞን_እሴት==0
            with መገናኛ:
                መገናኛ.sendall(b'\x01');초기=정확히(መገናኛ,24);너비,높이=struct.unpack('!HH',초기[:4]);ስም=정확히(መገናኛ,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ስም
                def 화면(증분=0):
                    መገናኛ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(መገናኛ,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ስዕል_እሴት=bytearray(너비*높이*4)
                    for _ in range(수):
                        ኤክስ_አስተባባሪ,세로좌표,영역너비,영역높이,ስልት_ሁነታ=struct.unpack('!HHHHi',정확히(መገናኛ,12));assert ስልት_ሁነታ==0 and ኤክስ_አስተባባሪ+영역너비<=너비 and 세로좌표+영역높이<=높이
                        ፒክስል=정확히(መገናኛ,영역너비*영역높이*4);합계+=len(ፒክስል)
                        for መስመር in range(영역높이):ስዕል_እሴት[((세로좌표+መስመር)*너비+ኤክስ_አስተባባሪ)*4:((세로좌표+መስመር)*너비+ኤክስ_አስተባባሪ+영역너비)*4]=ፒክስል[መስመር*영역너비*4:(መስመር+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ስዕል_እሴት),'raw','BGRX').save(str(ውጤት/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ዘገባ_እሴት['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ዘገባ_እሴት['checks'].append('RFB incremental update')
                처음=len(መዝግብ_ረድፍ)
                for ቁምፊ_እሴት in 'echo VNC_NATIVE_PASS\r':
                    ምልክት_ad6f1a96=0xff0d if ቁምፊ_እሴት=='\r' else ord(ቁምፊ_እሴት)
                    መገናኛ.sendall(struct.pack('!BBHI',4,1,0,ምልክት_ad6f1a96));መገናኛ.sendall(struct.pack('!BBHI',4,0,0,ምልክት_ad6f1a96))
                መጠበቅ_ዞን(b'VNC_NATIVE_PASS',처음)
                ዘገባ_እሴት['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ምልክት_ad6f1a96,누름=1):መገናኛ.sendall(struct.pack('!BBHI',4,누름,0,ምልክት_ad6f1a96))
                처음=len(መዝግብ_ረድፍ)
                for ቁምፊ_እሴት in 'echo ':글쇠(ord(ቁምፊ_እሴት))
                글쇠(0xffc6)
                for ቁምፊ_እሴት in 'gksrmf':글쇠(ord(ቁምፊ_እሴት))
                글쇠(0xffc6);글쇠(0xff0d)
                መጠበቅ_ዞን('\r\n한글\r\n'.encode(),처음)
                ዘገባ_እሴት['checks'].append('Native VNC F9 two-set Hangul composition')
                መገናኛ.sendall(struct.pack('!BBHH',5,0,120,100))
                ዘገባ_እሴት['checks'].append('VNC pointer input accepted')
            ሂደት_እሴት.stdin.write(b'poweroff\n');ሂደት_እሴት.stdin.flush();ሂደት_እሴት.wait(timeout=15);assert ሂደት_እሴት.returncode==0
            ዘገባ_እሴት['passed']=True
    finally:
        if ሂደት_እሴት and ሂደት_እሴት.poll() is None:
            ሂደት_እሴት.terminate()
            try: ሂደት_እሴት.wait(timeout=5)
            except subprocess.TimeoutExpired: ሂደት_እሴት.kill();ሂደት_እሴት.wait()
        (ውጤት/'serial.log').write_bytes(መዝግብ_ረድፍ)
        (ውጤት/'report.json').write_text(json.dumps(ዘገባ_እሴት,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ዘገባ_እሴት,ensure_ascii=False,indent=2))


if __name__=='__main__': ማስኬጃ()
