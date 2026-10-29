#!/usr/bin/env python3
"""фактычны_дадзеныя OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from выканаць_каманда import 기준, Загад
from Сетка_мост import Сетка_мост


def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    аналізатар_48ee4b1b.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    аналізатар_48ee4b1b.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = аналізатар_48ee4b1b.parse_args()
    Выхад = 인수.output
    Выхад.mkdir(parents=True, exist_ok=True)
    Усталёўкі = json.loads(인수.access.read_text())
    справаздача_значэнне = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def нулявая_порт():
        with socket.socket() as Злучыцца:
            Злучыцца.bind(('127.0.0.5', 0))
            return Злучыцца.getsockname()[1]
    абалонка_порт, 화면포트, файл_порт = нулявая_порт(), нулявая_порт(), нулявая_порт()
    журнал_запіс = bytearray()
    Працэс_значэнне = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Сетка_мост(файл_порт,
                ['tcp:{}:22'.format(абалонка_порт), 'tcp:{}:5900'.format(화면포트)], вузел_адрас='127.0.0.5') as мост_значэнне:
            실행인수 = Загад()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Працэс_значэнне = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + мост_значэнне.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    дадзеныя = Працэс_значэнне.stdout.read(4096)
                    if not дадзеныя: break
                    журнал_запіс.extend(дадзеныя)
            паток_значэнне_5b72a632 = threading.Thread(target=수집, daemon=True)
            паток_значэнне_5b72a632.start()
            def чакае_стан(Гульні_са_словамі_Тэкст, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Гульні_са_словамі_Тэкст not in журнал_запіс[처음:]:
                    if time.monotonic()>끝 or Працэс_значэнне.poll() is not None:
                        raise AssertionError('Missing '+repr(Гульні_са_словамі_Тэкст)+'\n'+журнал_запіс[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            чакае_стан(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def бяспечны_абалонка(пароль_значэнне, інструкцыя_значэнне, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=пароль_значэнне
                인수=['ssh','-v']+list(추가)+['-p',str(абалонка_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',інструкцыя_значэнне]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=бяспечны_абалонка('!' + Усталёўкі['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Выхад/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in журнал_запіс, 결과.stderr
            справаздача_значэнне['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=бяспечны_абалонка(Усталёўкі['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Выхад/'ssh.log').write_bytes(결과.stderr)
            (Выхад/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            справаздача_значэнне['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            справаздача_значэнне['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=бяспечны_абалонка(Усталёўкі['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA Выхад: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            справаздача_значэнне['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=бяспечны_абалонка(Усталёўкі['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            справаздача_значэнне['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=бяспечны_абалонка(Усталёўкі['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Выхад/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            справаздача_значэнне['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(абалонка_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            інтэрактыўны_сеанс=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();вылучанае_значэнне=selectors.DefaultSelector();вылучанае_значэнне.register(інтэрактыўны_сеанс.stdout,selectors.EVENT_READ)
            def 대화읽기(паказаць_значэнне):
                마감=time.monotonic()+30
                while паказаць_значэнне not in 대화기록:
                    if time.monotonic()>마감 or інтэрактыўны_сеанс.poll() is not None:raise AssertionError('SSH interactive missing '+repr(паказаць_значэнне)+' '+repr(bytes(대화기록)))
                    for увядзенне_значэнне,_ in вылучанае_значэнне.select(.1):
                        조각=увядзенне_значэнне.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                інтэрактыўны_сеанс.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');інтэрактыўны_сеанс.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                інтэрактыўны_сеанс.stdin.write(b'\x04');інтэрактыўны_сеанс.stdin.flush();나머지,ПАМЫЛКА=інтэрактыўны_сеанс.communicate(timeout=15)
                assert інтэрактыўны_сеанс.returncode==0 and b'PTY allocation request failed' not in ПАМЫЛКА,(інтэрактыўны_сеанс.returncode,ПАМЫЛКА)
                (Выхад/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                вылучанае_значэнне.close()
                if інтэрактыўны_сеанс.poll() is None:інтэрактыўны_сеанс.kill();інтэрактыўны_сеанс.wait()
            справаздача_значэнне['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Злучыцца, 수):
                дадзеныя=bytearray()
                while len(дадзеныя)<수:
                    덩이=Злучыцца.recv(수-len(дадзеныя))
                    if not 덩이: raise AssertionError('RFB EOF')
                    дадзеныя.extend(덩이)
                return bytes(дадзеныя)
            def 화면인증(пароль_значэнне):
                Злучыцца=socket.create_connection(('127.0.0.5',화면포트),10);Злучыцца.settimeout(30)
                assert 정확히(Злучыцца,12)==b'RFB 003.008\n'
                Злучыцца.sendall(b'RFB 003.008\n');assert 정확히(Злучыцца,2)==b'\x01\x02'
                Злучыцца.sendall(b'\x02');задача_значэнне=정확히(Злучыцца,16)
                입력암호=пароль_значэнне.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Злучыцца.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(задача_значэнне))
                стан_значэнне=struct.unpack('!I',정확히(Злучыцца,4))[0]
                return Злучыцца,стан_значэнне
            памылковы_пароль='!' if not Усталёўкі['vnc_password'].startswith('!') else '?'
            Злучыцца,стан_значэнне=화면인증(памылковы_пароль);assert стан_значэнне==1;Злучыцца.close();time.sleep(.6)
            справаздача_значэнне['checks'].append('VNC incorrect password rejected')
            Злучыцца,стан_значэнне=화면인증(Усталёўкі['vnc_password']);assert стан_значэнне==0
            with Злучыцца:
                Злучыцца.sendall(b'\x01');초기=정확히(Злучыцца,24);너비,높이=struct.unpack('!HH',초기[:4]);Назва=정확히(Злучыцца,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Назва
                def 화면(증분=0):
                    Злучыцца.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Злучыцца,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    рукапісная_графіка_значэнне=bytearray(너비*높이*4)
                    for _ in range(수):
                        каардыната_x,세로좌표,영역너비,영역높이,спосаб_рэжым=struct.unpack('!HHHHi',정확히(Злучыцца,12));assert спосаб_рэжым==0 and каардыната_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        пэл=정확히(Злучыцца,영역너비*영역높이*4);합계+=len(пэл)
                        for лінія in range(영역높이):рукапісная_графіка_значэнне[((세로좌표+лінія)*너비+каардыната_x)*4:((세로좌표+лінія)*너비+каардыната_x+영역너비)*4]=пэл[лінія*영역너비*4:(лінія+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(рукапісная_графіка_значэнне),'raw','BGRX').save(str(Выхад/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                справаздача_значэнне['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                справаздача_значэнне['checks'].append('RFB incremental update')
                처음=len(журнал_запіс)
                for сімвал_значэнне_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    сімвал=0xff0d if сімвал_значэнне_068c2631=='\r' else ord(сімвал_значэнне_068c2631)
                    Злучыцца.sendall(struct.pack('!BBHI',4,1,0,сімвал));Злучыцца.sendall(struct.pack('!BBHI',4,0,0,сімвал))
                чакае_стан(b'VNC_NATIVE_PASS',처음)
                справаздача_значэнне['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(сімвал,누름=1):Злучыцца.sendall(struct.pack('!BBHI',4,누름,0,сімвал))
                처음=len(журнал_запіс)
                for сімвал_значэнне_068c2631 in 'echo ':글쇠(ord(сімвал_значэнне_068c2631))
                글쇠(0xffc6)
                for сімвал_значэнне_068c2631 in 'gksrmf':글쇠(ord(сімвал_значэнне_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                чакае_стан('\r\n한글\r\n'.encode(),처음)
                справаздача_значэнне['checks'].append('Native VNC F9 two-set Hangul composition')
                Злучыцца.sendall(struct.pack('!BBHH',5,0,120,100))
                справаздача_значэнне['checks'].append('VNC pointer input accepted')
            Працэс_значэнне.stdin.write(b'poweroff\n');Працэс_значэнне.stdin.flush();Працэс_значэнне.wait(timeout=15);assert Працэс_значэнне.returncode==0
            справаздача_значэнне['passed']=True
    finally:
        if Працэс_значэнне and Працэс_значэнне.poll() is None:
            Працэс_значэнне.terminate()
            try: Працэс_значэнне.wait(timeout=5)
            except subprocess.TimeoutExpired: Працэс_значэнне.kill();Працэс_значэнне.wait()
        (Выхад/'serial.log').write_bytes(журнал_запіс)
        (Выхад/'report.json').write_text(json.dumps(справаздача_значэнне,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(справаздача_значэнне,ensure_ascii=False,indent=2))


if __name__=='__main__': Выканаць()
