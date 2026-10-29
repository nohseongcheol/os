#!/usr/bin/env python3
"""totoo_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Mag_execute_utos import Project_root, utos
from Network_bridge import Network_bridge


def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_root / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_root / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_root / 'build/verification/native-remote')
    인수 = parser_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Mga_Setting = json.loads(인수.access.read_text())
    ulat_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def walang_laman_port():
        with socket.socket() as CONNECT:
            CONNECT.bind(('127.0.0.5', 0))
            return CONNECT.getsockname()[1]
    shell_port, 화면포트, file_port = walang_laman_port(), walang_laman_port(), walang_laman_port()
    LOG_hanay = bytearray()
    Proseso_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Network_bridge(file_port,
                ['tcp:{}:22'.format(shell_port), 'tcp:{}:5900'.format(화면포트)], host_email='127.0.0.5') as bridge_VALUE:
            실행인수 = utos()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proseso_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bridge_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proseso_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_hanay.extend(data)
            thread_VALUE = threading.Thread(target=수집, daemon=True)
            thread_VALUE.start()
            def maghintay_katayuan(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_hanay[처음:]:
                    if time.monotonic()>끝 or Proseso_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_hanay[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            maghintay_katayuan(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def secure_shell(password_VALUE, instruksiyon_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=password_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksiyon_VALUE]
                sukat=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return sukat
            sukat=secure_shell('!' + Mga_Setting['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(sukat.stderr)
            assert sukat.returncode!=0 and b'Permission denied' in sukat.stderr and b'SHOULD_NOT_RUN' not in LOG_hanay, sukat.stderr
            ulat_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            sukat=secure_shell(Mga_Setting['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(sukat.stderr)
            (출력/'ssh-output.txt').write_bytes(sukat.stdout)
            assert sukat.returncode==0 and b'SSH_NATIVE_PASS' in sukat.stdout, (sukat.returncode,sukat.stdout,sukat.stderr)
            ulat_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in sukat.stderr, sukat.stderr
            ulat_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            sukat=secure_shell(Mga_Setting['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert sukat.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in sukat.stdout,sukat.stdout
            ulat_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            sukat=secure_shell(Mga_Setting['ssh_password'], 'missing_remote_command')
            assert sukat.returncode==127,sukat.returncode
            ulat_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            sukat=secure_shell(Mga_Setting['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(sukat.stderr)
            assert sukat.returncode==0 and 'class 창예제'.encode() in sukat.stdout, (sukat.returncode,sukat.stdout,sukat.stderr)
            assert sukat.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, sukat.stderr
            ulat_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            tumutugon_interactive_sesyon=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();seleksyon_VALUE=selectors.DefaultSelector();seleksyon_VALUE.register(tumutugon_interactive_sesyon.stdout,selectors.EVENT_READ)
            def 대화읽기(ipakita_VALUE):
                마감=time.monotonic()+30
                while ipakita_VALUE not in 대화기록:
                    if time.monotonic()>마감 or tumutugon_interactive_sesyon.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ipakita_VALUE)+' '+repr(bytes(대화기록)))
                    for pagpasok_VALUE,_ in seleksyon_VALUE.select(.1):
                        조각=pagpasok_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                tumutugon_interactive_sesyon.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');tumutugon_interactive_sesyon.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                tumutugon_interactive_sesyon.stdin.write(b'\x04');tumutugon_interactive_sesyon.stdin.flush();나머지,error=tumutugon_interactive_sesyon.communicate(timeout=15)
                assert tumutugon_interactive_sesyon.returncode==0 and b'PTY allocation request failed' not in error,(tumutugon_interactive_sesyon.returncode,error)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                seleksyon_VALUE.close()
                if tumutugon_interactive_sesyon.poll() is None:tumutugon_interactive_sesyon.kill();tumutugon_interactive_sesyon.wait()
            ulat_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(CONNECT, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=CONNECT.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(password_VALUE):
                CONNECT=socket.create_connection(('127.0.0.5',화면포트),10);CONNECT.settimeout(30)
                assert 정확히(CONNECT,12)==b'RFB 003.008\n'
                CONNECT.sendall(b'RFB 003.008\n');assert 정확히(CONNECT,2)==b'\x01\x02'
                CONNECT.sendall(b'\x02');hamon_VALUE=정확히(CONNECT,16)
                입력암호=password_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                CONNECT.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(hamon_VALUE))
                katayuan_VALUE=struct.unpack('!I',정확히(CONNECT,4))[0]
                return CONNECT,katayuan_VALUE
            hindi_tama_password='!' if not Mga_Setting['vnc_password'].startswith('!') else '?'
            CONNECT,katayuan_VALUE=화면인증(hindi_tama_password);assert katayuan_VALUE==1;CONNECT.close();time.sleep(.6)
            ulat_VALUE['checks'].append('VNC incorrect password rejected')
            CONNECT,katayuan_VALUE=화면인증(Mga_Setting['vnc_password']);assert katayuan_VALUE==0
            with CONNECT:
                CONNECT.sendall(b'\x01');초기=정확히(CONNECT,24);너비,높이=struct.unpack('!HH',초기[:4]);pangalan=정확히(CONNECT,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==pangalan
                def 화면(증분=0):
                    CONNECT.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(CONNECT,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    iginuhit_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_coordinate,Y_button_coordinate,영역너비,영역높이,pamamaraan_MODE=struct.unpack('!HHHHi',정확히(CONNECT,12));assert pamamaraan_MODE==0 and x_coordinate+영역너비<=너비 and Y_button_coordinate+영역높이<=높이
                        pel=정확히(CONNECT,영역너비*영역높이*4);합계+=len(pel)
                        for linya in range(영역높이):iginuhit_VALUE[((Y_button_coordinate+linya)*너비+x_coordinate)*4:((Y_button_coordinate+linya)*너비+x_coordinate+영역너비)*4]=pel[linya*영역너비*4:(linya+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(iginuhit_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ulat_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ulat_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_hanay)
                for karakter_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbolo=0xff0d if karakter_VALUE=='\r' else ord(karakter_VALUE)
                    CONNECT.sendall(struct.pack('!BBHI',4,1,0,simbolo));CONNECT.sendall(struct.pack('!BBHI',4,0,0,simbolo))
                maghintay_katayuan(b'VNC_NATIVE_PASS',처음)
                ulat_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbolo,누름=1):CONNECT.sendall(struct.pack('!BBHI',4,누름,0,simbolo))
                처음=len(LOG_hanay)
                for karakter_VALUE in 'echo ':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6)
                for karakter_VALUE in 'gksrmf':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                maghintay_katayuan('\r\n한글\r\n'.encode(),처음)
                ulat_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                CONNECT.sendall(struct.pack('!BBHH',5,0,120,100))
                ulat_VALUE['checks'].append('VNC pointer input accepted')
            Proseso_VALUE.stdin.write(b'poweroff\n');Proseso_VALUE.stdin.flush();Proseso_VALUE.wait(timeout=15);assert Proseso_VALUE.returncode==0
            ulat_VALUE['passed']=True
    finally:
        if Proseso_VALUE and Proseso_VALUE.poll() is None:
            Proseso_VALUE.terminate()
            try: Proseso_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proseso_VALUE.kill();Proseso_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_hanay)
        (출력/'report.json').write_text(json.dumps(ulat_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ulat_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': run()
