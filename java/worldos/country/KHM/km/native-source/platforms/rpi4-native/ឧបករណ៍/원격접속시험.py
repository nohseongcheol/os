#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា
from 통신다리 import 통신다리


def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--kernel', type=Path, default=បញ្ចាំង_ឬស / 'build/kernel8.img')
    មុខងារ_ញែក_48ee4b1b.add_argument('--access', type=Path, default=បញ្ចាំង_ឬស / 'build/remote/access.json')
    មុខងារ_ញែក_48ee4b1b.add_argument('--output', type=Path, default=បញ្ចាំង_ឬស / 'build/verification/native-remote')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    លទ្ធផល = អាគុយម៉ង់.output
    លទ្ធផល.mkdir(parents=True, exist_ok=True)
    ការកំណត់ = json.loads(អាគុយម៉ង់.access.read_text())
    រាយការណ៍_តំលៃ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(អាគុយម៉ង់.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ទទេរ_ច្រក():
        with socket.socket() as ភ្ជាប់:
            ភ្ជាប់.bind(('127.0.0.5', 0))
            return ភ្ជាប់.getsockname()[1]
    셸포트, 화면포트, ឯកសារ_ច្រក = ទទេរ_ច្រក(), ទទេរ_ច្រក(), ទទេរ_ច្រក()
    កំណត់_ហេតុ_ថត = bytearray()
    ដំណើរការ_តំលៃ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(ឯកសារ_ច្រក,
                ['tcp:{}:22'.format(셸포트), 'tcp:{}:5900'.format(화면포트)], ហូស_អ៊ីម៉ែល='127.0.0.5') as 다리:
            실행인수 = ពាក្យ_បញ្ជា()
            실행인수[실행인수.index('-kernel') + 1] = str(អាគុយម៉ង់.kernel.resolve())
            ដំណើរការ_តំលៃ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ទិន្នន័យ = ដំណើរការ_តំលៃ.stdout.read(4096)
                    if not ទិន្នន័យ: break
                    កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
            ស្រេត_តំលៃ = threading.Thread(target=수집, daemon=True)
            ស្រេត_តំលៃ.start()
            def រង់ចាំ_ភាព(ពាក្យ_អត្ថបទ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ពាក្យ_អត្ថបទ not in កំណត់_ហេតុ_ថត[처음:]:
                    if time.monotonic()>끝 or ដំណើរការ_តំលៃ.poll() is not None:
                        raise AssertionError('Missing '+repr(ពាក្យ_អត្ថបទ)+'\n'+កំណត់_ហេតុ_ថត[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            រង់ចាំ_ភាព(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(លេខសម្ងាត់_តំលៃ, ការណែនាំ_តំលៃ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=លេខសម្ងាត់_តំលៃ
                អាគុយម៉ង់=['ssh','-v']+list(추가)+['-p',str(셸포트),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ការណែនាំ_តំលៃ]
                ការវាស់វែង=subprocess.run(អាគុយម៉ង់,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ការវាស់វែង
            ការវាស់វែង=보안셸('!' + ការកំណត់['ssh_password'], 'echo SHOULD_NOT_RUN')
            (លទ្ធផល/'ssh-rejected.log').write_bytes(ការវាស់វែង.stderr)
            assert ការវាស់វែង.returncode!=0 and b'Permission denied' in ការវាស់វែង.stderr and b'SHOULD_NOT_RUN' not in កំណត់_ហេតុ_ថត, ការវាស់វែង.stderr
            រាយការណ៍_តំលៃ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ការវាស់វែង=보안셸(ការកំណត់['ssh_password'], 'echo SSH_NATIVE_PASS')
            (លទ្ធផល/'ssh.log').write_bytes(ការវាស់វែង.stderr)
            (លទ្ធផល/'ssh-output.txt').write_bytes(ការវាស់វែង.stdout)
            assert ការវាស់វែង.returncode==0 and b'SSH_NATIVE_PASS' in ការវាស់វែង.stdout, (ការវាស់វែង.returncode,ការវាស់វែង.stdout,ការវាស់វែង.stderr)
            រាយការណ៍_តំលៃ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ការវាស់វែង.stderr, ការវាស់វែង.stderr
            រាយការណ៍_តំលៃ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ការវាស់វែង=보안셸(ការកំណត់['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ការវាស់វែង.returncode==0 and 'JAVA លទ្ធផល: 안녕하세요 😀'.encode() in ការវាស់វែង.stdout,ការវាស់វែង.stdout
            រាយការណ៍_តំលៃ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ការវាស់វែង=보안셸(ការកំណត់['ssh_password'], 'missing_remote_command')
            assert ការវាស់វែង.returncode==127,ការវាស់វែង.returncode
            រាយការណ៍_តំលៃ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ការវាស់វែង=보안셸(ការកំណត់['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (លទ្ធផល/'ssh-rekey.log').write_bytes(ការវាស់វែង.stderr)
            assert ការវាស់វែង.returncode==0 and 'class 창예제'.encode() in ការវាស់វែង.stdout, (ការវាស់វែង.returncode,ការវាស់វែង.stdout,ការវាស់វែង.stderr)
            assert ការវាស់វែង.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ការវាស់វែង.stderr
            រាយការណ៍_តំលៃ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(셸포트),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            អន្តរកម្ម_ពេល=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ការជ្រើស_តំលៃ=selectors.DefaultSelector();ការជ្រើស_តំលៃ.register(អន្តរកម្ម_ពេល.stdout,selectors.EVENT_READ)
            def 대화읽기(បង្ហាញ_តំលៃ):
                마감=time.monotonic()+30
                while បង្ហាញ_តំលៃ not in 대화기록:
                    if time.monotonic()>마감 or អន្តរកម្ម_ពេល.poll() is not None:raise AssertionError('SSH interactive missing '+repr(បង្ហាញ_តំលៃ)+' '+repr(bytes(대화기록)))
                    for ការបញ្ចូល_តំលៃ,_ in ការជ្រើស_តំលៃ.select(.1):
                        조각=ការបញ្ចូល_តំលៃ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                អន្តរកម្ម_ពេល.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');អន្តរកម្ម_ពេល.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                អន្តរកម្ម_ពេល.stdin.write(b'\x04');អន្តរកម្ម_ពេល.stdin.flush();나머지,កំហុស=អន្តរកម្ម_ពេល.communicate(timeout=15)
                assert អន្តរកម្ម_ពេល.returncode==0 and b'PTY allocation request failed' not in កំហុស,(អន្តរកម្ម_ពេល.returncode,កំហុស)
                (លទ្ធផល/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ការជ្រើស_តំលៃ.close()
                if អន្តរកម្ម_ពេល.poll() is None:អន្តរកម្ម_ពេល.kill();អន្តរកម្ម_ពេល.wait()
            រាយការណ៍_តំលៃ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ភ្ជាប់, 수):
                ទិន្នន័យ=bytearray()
                while len(ទិន្នន័យ)<수:
                    덩이=ភ្ជាប់.recv(수-len(ទិន្នន័យ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ទិន្នន័យ.extend(덩이)
                return bytes(ទិន្នន័យ)
            def 화면인증(លេខសម្ងាត់_តំលៃ):
                ភ្ជាប់=socket.create_connection(('127.0.0.5',화면포트),10);ភ្ជាប់.settimeout(30)
                assert 정확히(ភ្ជាប់,12)==b'RFB 003.008\n'
                ភ្ជាប់.sendall(b'RFB 003.008\n');assert 정확히(ភ្ជាប់,2)==b'\x01\x02'
                ភ្ជាប់.sendall(b'\x02');បញ្ហា_តំលៃ=정확히(ភ្ជាប់,16)
                입력암호=លេខសម្ងាត់_តំលៃ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ភ្ជាប់.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(បញ្ហា_តំលៃ))
                ភាព_តំលៃ=struct.unpack('!I',정확히(ភ្ជាប់,4))[0]
                return ភ្ជាប់,ភាព_តំលៃ
            មិនត្រឹមត្រូវ_លេខសម្ងាត់='!' if not ការកំណត់['vnc_password'].startswith('!') else '?'
            ភ្ជាប់,ភាព_តំលៃ=화면인증(មិនត្រឹមត្រូវ_លេខសម្ងាត់);assert ភាព_តំលៃ==1;ភ្ជាប់.close();time.sleep(.6)
            រាយការណ៍_តំលៃ['checks'].append('VNC incorrect password rejected')
            ភ្ជាប់,ភាព_តំលៃ=화면인증(ការកំណត់['vnc_password']);assert ភាព_តំលៃ==0
            with ភ្ជាប់:
                ភ្ជាប់.sendall(b'\x01');초기=정확히(ភ្ជាប់,24);너비,높이=struct.unpack('!HH',초기[:4]);ឈ្មោះ=정확히(ភ្ជាប់,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ឈ្មោះ
                def 화면(증분=0):
                    ភ្ជាប់.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ភ្ជាប់,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ការគូរ_តំលៃ=bytearray(너비*높이*4)
                    for _ in range(수):
                        កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ,영역너비,영역높이,វិធីសាស្រ្ត_ម៉ូដ=struct.unpack('!HHHHi',정확히(ភ្ជាប់,12));assert វិធីសាស្រ្ត_ម៉ូដ==0 and កូអរដោណេ_x+영역너비<=너비 and ប៊ូតុង_Y_កូអរដោនេ+영역높이<=높이
                        ចំនុចតូចៗ=정확히(ភ្ជាប់,영역너비*영역높이*4);합계+=len(ចំនុចតូចៗ)
                        for បន្ទាត់ in range(영역높이):ការគូរ_តំលៃ[((ប៊ូតុង_Y_កូអរដោនេ+បន្ទាត់)*너비+កូអរដោណេ_x)*4:((ប៊ូតុង_Y_កូអរដោនេ+បន្ទាត់)*너비+កូអរដោណេ_x+영역너비)*4]=ចំនុចតូចៗ[បន្ទាត់*영역너비*4:(បន្ទាត់+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ការគូរ_តំលៃ),'raw','BGRX').save(str(លទ្ធផល/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                រាយការណ៍_តំលៃ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                រាយការណ៍_តំលៃ['checks'].append('RFB incremental update')
                처음=len(កំណត់_ហេតុ_ថត)
                for តួអក្សរ_តំលៃ in 'echo VNC_NATIVE_PASS\r':
                    និមិត្ត_សញ្ញា=0xff0d if តួអក្សរ_តំលៃ=='\r' else ord(តួអក្សរ_តំលៃ)
                    ភ្ជាប់.sendall(struct.pack('!BBHI',4,1,0,និមិត្ត_សញ្ញា));ភ្ជាប់.sendall(struct.pack('!BBHI',4,0,0,និមិត្ត_សញ្ញា))
                រង់ចាំ_ភាព(b'VNC_NATIVE_PASS',처음)
                រាយការណ៍_តំលៃ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(និមិត្ត_សញ្ញា,누름=1):ភ្ជាប់.sendall(struct.pack('!BBHI',4,누름,0,និមិត្ត_សញ្ញា))
                처음=len(កំណត់_ហេតុ_ថត)
                for តួអក្សរ_តំលៃ in 'echo ':글쇠(ord(តួអក្សរ_តំលៃ))
                글쇠(0xffc6)
                for តួអក្សរ_តំលៃ in 'gksrmf':글쇠(ord(តួអក្សរ_តំលៃ))
                글쇠(0xffc6);글쇠(0xff0d)
                រង់ចាំ_ភាព('\r\n한글\r\n'.encode(),처음)
                រាយការណ៍_តំលៃ['checks'].append('Native VNC F9 two-set Hangul composition')
                ភ្ជាប់.sendall(struct.pack('!BBHH',5,0,120,100))
                រាយការណ៍_តំលៃ['checks'].append('VNC pointer input accepted')
            ដំណើរការ_តំលៃ.stdin.write(b'poweroff\n');ដំណើរការ_តំលៃ.stdin.flush();ដំណើរការ_តំលៃ.wait(timeout=15);assert ដំណើរការ_តំលៃ.returncode==0
            រាយការណ៍_តំលៃ['passed']=True
    finally:
        if ដំណើរការ_តំលៃ and ដំណើរការ_តំលៃ.poll() is None:
            ដំណើរការ_តំលៃ.terminate()
            try: ដំណើរការ_តំលៃ.wait(timeout=5)
            except subprocess.TimeoutExpired: ដំណើរការ_តំលៃ.kill();ដំណើរការ_តំលៃ.wait()
        (លទ្ធផល/'serial.log').write_bytes(កំណត់_ហេតុ_ថត)
        (លទ្ធផល/'report.json').write_text(json.dumps(រាយការណ៍_តំលៃ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(រាយការណ៍_តំលៃ,ensure_ascii=False,indent=2))


if __name__=='__main__': រត់()
