#!/usr/bin/env python3
"""რეალური_მონაცემები OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება
from ქსელი_ხიდი import ქსელი_ხიდი


def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=პროეცირება_ფესვი / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=პროეცირება_ფესვი / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=პროეცირება_ფესვი / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    პარამეტრები = json.loads(인수.access.read_text())
    ანგარიში_მნიშვნელობა = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ცარიელი_პორტი():
        with socket.socket() as დაკავშირება:
            დაკავშირება.bind(('127.0.0.5', 0))
            return დაკავშირება.getsockname()[1]
    გარემო_პორტი, 화면포트, ფაილი_პორტი = ცარიელი_პორტი(), ცარიელი_პორტი(), ცარიელი_პორტი()
    ჟურნალი_ჩაწერა = bytearray()
    პროცესი_მნიშვნელობა = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ქსელი_ხიდი(ფაილი_პორტი,
                ['tcp:{}:22'.format(გარემო_პორტი), 'tcp:{}:5900'.format(화면포트)], მასპინძელი_მისამართი='127.0.0.5') as ხიდი_მნიშვნელობა:
            실행인수 = ბრძანება()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            პროცესი_მნიშვნელობა = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ხიდი_მნიშვნელობა.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    მონაცემები = პროცესი_მნიშვნელობა.stdout.read(4096)
                    if not მონაცემები: break
                    ჟურნალი_ჩაწერა.extend(მონაცემები)
            თემა_მნიშვნელობა = threading.Thread(target=수집, daemon=True)
            თემა_მნიშვნელობა.start()
            def მოლოდინი_სტატუსი(სიტყვები_ტექსტი, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while სიტყვები_ტექსტი not in ჟურნალი_ჩაწერა[처음:]:
                    if time.monotonic()>끝 or პროცესი_მნიშვნელობა.poll() is not None:
                        raise AssertionError('Missing '+repr(სიტყვები_ტექსტი)+'\n'+ჟურნალი_ჩაწერა[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            მოლოდინი_სტატუსი(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def უსაფრთხო_გარემო(პაროლი_მნიშვნელობა, ინსტრუქცია_მნიშვნელობა, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=პაროლი_მნიშვნელობა
                인수=['ssh','-v']+list(추가)+['-p',str(გარემო_პორტი),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ინსტრუქცია_მნიშვნელობა]
                გაზომვა=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return გაზომვა
            გაზომვა=უსაფრთხო_გარემო('!' + პარამეტრები['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(გაზომვა.stderr)
            assert გაზომვა.returncode!=0 and b'Permission denied' in გაზომვა.stderr and b'SHOULD_NOT_RUN' not in ჟურნალი_ჩაწერა, გაზომვა.stderr
            ანგარიში_მნიშვნელობა['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            გაზომვა=უსაფრთხო_გარემო(პარამეტრები['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(გაზომვა.stderr)
            (출력/'ssh-output.txt').write_bytes(გაზომვა.stdout)
            assert გაზომვა.returncode==0 and b'SSH_NATIVE_PASS' in გაზომვა.stdout, (გაზომვა.returncode,გაზომვა.stdout,გაზომვა.stderr)
            ანგარიში_მნიშვნელობა['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in გაზომვა.stderr, გაზომვა.stderr
            ანგარიში_მნიშვნელობა['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            გაზომვა=უსაფრთხო_გარემო(პარამეტრები['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert გაზომვა.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in გაზომვა.stdout,გაზომვა.stdout
            ანგარიში_მნიშვნელობა['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            გაზომვა=უსაფრთხო_გარემო(პარამეტრები['ssh_password'], 'missing_remote_command')
            assert გაზომვა.returncode==127,გაზომვა.returncode
            ანგარიში_მნიშვნელობა['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            გაზომვა=უსაფრთხო_გარემო(პარამეტრები['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(გაზომვა.stderr)
            assert გაზომვა.returncode==0 and 'class 창예제'.encode() in გაზომვა.stdout, (გაზომვა.returncode,გაზომვა.stdout,გაზომვა.stderr)
            assert გაზომვა.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, გაზომვა.stderr
            ანგარიში_მნიშვნელობა['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(გარემო_პორტი),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ინტერაქტიული_სესია=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();მონიშნული_ობიექტი_მნიშვნელობა=selectors.DefaultSelector();მონიშნული_ობიექტი_მნიშვნელობა.register(ინტერაქტიული_სესია.stdout,selectors.EVENT_READ)
            def 대화읽기(ჩვენება_მნიშვნელობა):
                마감=time.monotonic()+30
                while ჩვენება_მნიშვნელობა not in 대화기록:
                    if time.monotonic()>마감 or ინტერაქტიული_სესია.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ჩვენება_მნიშვნელობა)+' '+repr(bytes(대화기록)))
                    for შენატანი_მნიშვნელობა,_ in მონიშნული_ობიექტი_მნიშვნელობა.select(.1):
                        조각=შენატანი_მნიშვნელობა.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ინტერაქტიული_სესია.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ინტერაქტიული_სესია.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ინტერაქტიული_სესია.stdin.write(b'\x04');ინტერაქტიული_სესია.stdin.flush();나머지,შეცდომა=ინტერაქტიული_სესია.communicate(timeout=15)
                assert ინტერაქტიული_სესია.returncode==0 and b'PTY allocation request failed' not in შეცდომა,(ინტერაქტიული_სესია.returncode,შეცდომა)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                მონიშნული_ობიექტი_მნიშვნელობა.close()
                if ინტერაქტიული_სესია.poll() is None:ინტერაქტიული_სესია.kill();ინტერაქტიული_სესია.wait()
            ანგარიში_მნიშვნელობა['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(დაკავშირება, 수):
                მონაცემები=bytearray()
                while len(მონაცემები)<수:
                    덩이=დაკავშირება.recv(수-len(მონაცემები))
                    if not 덩이: raise AssertionError('RFB EOF')
                    მონაცემები.extend(덩이)
                return bytes(მონაცემები)
            def 화면인증(პაროლი_მნიშვნელობა):
                დაკავშირება=socket.create_connection(('127.0.0.5',화면포트),10);დაკავშირება.settimeout(30)
                assert 정확히(დაკავშირება,12)==b'RFB 003.008\n'
                დაკავშირება.sendall(b'RFB 003.008\n');assert 정확히(დაკავშირება,2)==b'\x01\x02'
                დაკავშირება.sendall(b'\x02');გამოცდა_მნიშვნელობა=정확히(დაკავშირება,16)
                입력암호=პაროლი_მნიშვნელობა.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                დაკავშირება.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(გამოცდა_მნიშვნელობა))
                სტატუსი_მნიშვნელობა=struct.unpack('!I',정확히(დაკავშირება,4))[0]
                return დაკავშირება,სტატუსი_მნიშვნელობა
            არასწორი_პაროლი='!' if not პარამეტრები['vnc_password'].startswith('!') else '?'
            დაკავშირება,სტატუსი_მნიშვნელობა=화면인증(არასწორი_პაროლი);assert სტატუსი_მნიშვნელობა==1;დაკავშირება.close();time.sleep(.6)
            ანგარიში_მნიშვნელობა['checks'].append('VNC incorrect password rejected')
            დაკავშირება,სტატუსი_მნიშვნელობა=화면인증(პარამეტრები['vnc_password']);assert სტატუსი_მნიშვნელობა==0
            with დაკავშირება:
                დაკავშირება.sendall(b'\x01');초기=정확히(დაკავშირება,24);너비,높이=struct.unpack('!HH',초기[:4]);სახელი=정확히(დაკავშირება,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==სახელი
                def 화면(증분=0):
                    დაკავშირება.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(დაკავშირება,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ნახატი_მნიშვნელობა_c143fe9e=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_კოორდინატა,Y_ღილაკი_კოორდინატი,영역너비,영역높이,მეთოდი_რეჟიმი=struct.unpack('!HHHHi',정확히(დაკავშირება,12));assert მეთოდი_რეჟიმი==0 and x_კოორდინატა+영역너비<=너비 and Y_ღილაკი_კოორდინატი+영역높이<=높이
                        პიქსელი=정확히(დაკავშირება,영역너비*영역높이*4);합계+=len(პიქსელი)
                        for ხაზი in range(영역높이):ნახატი_მნიშვნელობა_c143fe9e[((Y_ღილაკი_კოორდინატი+ხაზი)*너비+x_კოორდინატა)*4:((Y_ღილაკი_კოორდინატი+ხაზი)*너비+x_კოორდინატა+영역너비)*4]=პიქსელი[ხაზი*영역너비*4:(ხაზი+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ნახატი_მნიშვნელობა_c143fe9e),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ანგარიში_მნიშვნელობა['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ანგარიში_მნიშვნელობა['checks'].append('RFB incremental update')
                처음=len(ჟურნალი_ჩაწერა)
                for სიმბოლო_მნიშვნელობა_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    სიმბოლო=0xff0d if სიმბოლო_მნიშვნელობა_068c2631=='\r' else ord(სიმბოლო_მნიშვნელობა_068c2631)
                    დაკავშირება.sendall(struct.pack('!BBHI',4,1,0,სიმბოლო));დაკავშირება.sendall(struct.pack('!BBHI',4,0,0,სიმბოლო))
                მოლოდინი_სტატუსი(b'VNC_NATIVE_PASS',처음)
                ანგარიში_მნიშვნელობა['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(სიმბოლო,დაჭერა_მნიშვნელობა=1):დაკავშირება.sendall(struct.pack('!BBHI',4,დაჭერა_მნიშვნელობა,0,სიმბოლო))
                처음=len(ჟურნალი_ჩაწერა)
                for სიმბოლო_მნიშვნელობა_068c2631 in 'echo ':글쇠(ord(სიმბოლო_მნიშვნელობა_068c2631))
                글쇠(0xffc6)
                for სიმბოლო_მნიშვნელობა_068c2631 in 'gksrmf':글쇠(ord(სიმბოლო_მნიშვნელობა_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                მოლოდინი_სტატუსი('\r\n한글\r\n'.encode(),처음)
                ანგარიში_მნიშვნელობა['checks'].append('Native VNC F9 two-set Hangul composition')
                დაკავშირება.sendall(struct.pack('!BBHH',5,0,120,100))
                ანგარიში_მნიშვნელობა['checks'].append('VNC pointer input accepted')
            პროცესი_მნიშვნელობა.stdin.write(b'poweroff\n');პროცესი_მნიშვნელობა.stdin.flush();პროცესი_მნიშვნელობა.wait(timeout=15);assert პროცესი_მნიშვნელობა.returncode==0
            ანგარიში_მნიშვნელობა['passed']=True
    finally:
        if პროცესი_მნიშვნელობა and პროცესი_მნიშვნელობა.poll() is None:
            პროცესი_მნიშვნელობა.terminate()
            try: პროცესი_მნიშვნელობა.wait(timeout=5)
            except subprocess.TimeoutExpired: პროცესი_მნიშვნელობა.kill();პროცესი_მნიშვნელობა.wait()
        (출력/'serial.log').write_bytes(ჟურნალი_ჩაწერა)
        (출력/'report.json').write_text(json.dumps(ანგარიში_მნიშვნელობა,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ანგარიში_მნიშვნელობა,ensure_ascii=False,indent=2))


if __name__=='__main__': გაშვება()
