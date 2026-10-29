#!/usr/bin/env python3
"""laatii_keɓe OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from 실행 import 기준, ginol
from 통신다리 import 통신다리


def huutoraade():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    설정 = json.loads(인수.access.read_text())
    ciimtol_njaru = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as seŋaade:
            seŋaade.bind(('127.0.0.5', 0))
            return seŋaade.getsockname()[1]
    laalagal_poor, 화면포트, fiilde_poor = 빈포트(), 빈포트(), 빈포트()
    suurnal_winndande = bytearray()
    Yuɓɓo_golle_njaru = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(fiilde_poor,
                ['tcp:{}:22'.format(laalagal_poor), 'tcp:{}:5900'.format(화면포트)], njaatigi_ñiiɓirde='127.0.0.5') as 다리:
            실행인수 = ginol()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Yuɓɓo_golle_njaru = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    keɓe = Yuɓɓo_golle_njaru.stdout.read(4096)
                    if not keɓe: break
                    suurnal_winndande.extend(keɓe)
            piilol_njaru = threading.Thread(target=수집, daemon=True)
            piilol_njaru.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in suurnal_winndande[처음:]:
                    if time.monotonic()>끝 or Yuɓɓo_golle_njaru.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+suurnal_winndande[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(finnde_njaru, yamiroore_njaru, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=finnde_njaru
                인수=['ssh','-v']+list(추가)+['-p',str(laalagal_poor),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',yamiroore_njaru]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + 설정['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in suurnal_winndande, 결과.stderr
            ciimtol_njaru['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(설정['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ciimtol_njaru['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ciimtol_njaru['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ciimtol_njaru['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ciimtol_njaru['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ciimtol_njaru['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(laalagal_poor),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            jokkondirtoo_jokkondiral=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();cuɓal_njaru=selectors.DefaultSelector();cuɓal_njaru.register(jokkondirtoo_jokkondiral.stdout,selectors.EVENT_READ)
            def 대화읽기(hollirde_njaru):
                마감=time.monotonic()+30
                while hollirde_njaru not in 대화기록:
                    if time.monotonic()>마감 or jokkondirtoo_jokkondiral.poll() is not None:raise AssertionError('SSH interactive missing '+repr(hollirde_njaru)+' '+repr(bytes(대화기록)))
                    for naatnugol_njaru,_ in cuɓal_njaru.select(.1):
                        조각=naatnugol_njaru.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                jokkondirtoo_jokkondiral.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');jokkondirtoo_jokkondiral.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                jokkondirtoo_jokkondiral.stdin.write(b'\x04');jokkondirtoo_jokkondiral.stdin.flush();나머지,juumre=jokkondirtoo_jokkondiral.communicate(timeout=15)
                assert jokkondirtoo_jokkondiral.returncode==0 and b'PTY allocation request failed' not in juumre,(jokkondirtoo_jokkondiral.returncode,juumre)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                cuɓal_njaru.close()
                if jokkondirtoo_jokkondiral.poll() is None:jokkondirtoo_jokkondiral.kill();jokkondirtoo_jokkondiral.wait()
            ciimtol_njaru['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(seŋaade, 수):
                keɓe=bytearray()
                while len(keɓe)<수:
                    덩이=seŋaade.recv(수-len(keɓe))
                    if not 덩이: raise AssertionError('RFB EOF')
                    keɓe.extend(덩이)
                return bytes(keɓe)
            def 화면인증(finnde_njaru):
                seŋaade=socket.create_connection(('127.0.0.5',화면포트),10);seŋaade.settimeout(30)
                assert 정확히(seŋaade,12)==b'RFB 003.008\n'
                seŋaade.sendall(b'RFB 003.008\n');assert 정확히(seŋaade,2)==b'\x01\x02'
                seŋaade.sendall(b'\x02');도전=정확히(seŋaade,16)
                입력암호=finnde_njaru.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                seŋaade.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                ngonka_njaru=struct.unpack('!I',정확히(seŋaade,4))[0]
                return seŋaade,ngonka_njaru
            heɓtinaake_finnde='!' if not 설정['vnc_password'].startswith('!') else '?'
            seŋaade,ngonka_njaru=화면인증(heɓtinaake_finnde);assert ngonka_njaru==1;seŋaade.close();time.sleep(.6)
            ciimtol_njaru['checks'].append('VNC incorrect password rejected')
            seŋaade,ngonka_njaru=화면인증(설정['vnc_password']);assert ngonka_njaru==0
            with seŋaade:
                seŋaade.sendall(b'\x01');초기=정확히(seŋaade,24);너비,높이=struct.unpack('!HH',초기[:4]);innde=정확히(seŋaade,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==innde
                def 화면(증분=0):
                    seŋaade.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(seŋaade,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    natal_njaru_c143fe9e=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(seŋaade,12));assert 방식==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        piksel=정확히(seŋaade,영역너비*영역높이*4);합계+=len(piksel)
                        for diidol in range(영역높이):natal_njaru_c143fe9e[((세로좌표+diidol)*너비+가로좌표)*4:((세로좌표+diidol)*너비+가로좌표+영역너비)*4]=piksel[diidol*영역너비*4:(diidol+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(natal_njaru_c143fe9e),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ciimtol_njaru['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ciimtol_njaru['checks'].append('RFB incremental update')
                처음=len(suurnal_winndande)
                for alkulal_njaru in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if alkulal_njaru=='\r' else ord(alkulal_njaru)
                    seŋaade.sendall(struct.pack('!BBHI',4,1,0,기호));seŋaade.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                ciimtol_njaru['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):seŋaade.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(suurnal_winndande)
                for alkulal_njaru in 'echo ':글쇠(ord(alkulal_njaru))
                글쇠(0xffc6)
                for alkulal_njaru in 'gksrmf':글쇠(ord(alkulal_njaru))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ciimtol_njaru['checks'].append('Native VNC F9 two-set Hangul composition')
                seŋaade.sendall(struct.pack('!BBHH',5,0,120,100))
                ciimtol_njaru['checks'].append('VNC pointer input accepted')
            Yuɓɓo_golle_njaru.stdin.write(b'poweroff\n');Yuɓɓo_golle_njaru.stdin.flush();Yuɓɓo_golle_njaru.wait(timeout=15);assert Yuɓɓo_golle_njaru.returncode==0
            ciimtol_njaru['passed']=True
    finally:
        if Yuɓɓo_golle_njaru and Yuɓɓo_golle_njaru.poll() is None:
            Yuɓɓo_golle_njaru.terminate()
            try: Yuɓɓo_golle_njaru.wait(timeout=5)
            except subprocess.TimeoutExpired: Yuɓɓo_golle_njaru.kill();Yuɓɓo_golle_njaru.wait()
        (출력/'serial.log').write_bytes(suurnal_winndande)
        (출력/'report.json').write_text(json.dumps(ciimtol_njaru,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ciimtol_njaru,ensure_ascii=False,indent=2))


if __name__=='__main__': huutoraade()
