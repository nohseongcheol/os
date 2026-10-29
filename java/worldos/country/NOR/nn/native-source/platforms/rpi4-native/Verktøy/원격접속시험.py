#!/usr/bin/env python3
"""faktisk_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Utfør_kommando import spegle_rot, Kommando
from Nettverk_bru import Nettverk_bru


def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=spegle_rot / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=spegle_rot / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=spegle_rot / 'build/verification/native-remote')
    Argument = 해석기.parse_args()
    Utdata = Argument.output
    Utdata.mkdir(parents=True, exist_ok=True)
    Innstillingar = json.loads(Argument.access.read_text())
    rapport_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argument.kernel.read_bytes()).hexdigest(), 'checks': []}
    def tom_port():
        with socket.socket() as Kopla_til:
            Kopla_til.bind(('127.0.0.5', 0))
            return Kopla_til.getsockname()[1]
    grensesnitt_port, 화면포트, fil_port = tom_port(), tom_port(), tom_port()
    LOG_rad = bytearray()
    Prosess_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Nettverk_bru(fil_port,
                ['tcp:{}:22'.format(grensesnitt_port), 'tcp:{}:5900'.format(화면포트)], vert_ADDRESS='127.0.0.5') as bru_VALUE:
            실행인수 = Kommando()
            실행인수[실행인수.index('-kernel') + 1] = str(Argument.kernel.resolve())
            Prosess_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bru_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Prosess_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_rad.extend(data)
            tråd_VALUE = threading.Thread(target=수집, daemon=True)
            tråd_VALUE.start()
            def vent_status(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_rad[처음:]:
                    if time.monotonic()>끝 or Prosess_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_rad[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            vent_status(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def sikker_grensesnitt(passord_VALUE, instruksjon_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=passord_VALUE
                Argument=['ssh','-v']+list(추가)+['-p',str(grensesnitt_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksjon_VALUE]
                forretningsmål=subprocess.run(Argument,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return forretningsmål
            forretningsmål=sikker_grensesnitt('!' + Innstillingar['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Utdata/'ssh-rejected.log').write_bytes(forretningsmål.stderr)
            assert forretningsmål.returncode!=0 and b'Permission denied' in forretningsmål.stderr and b'SHOULD_NOT_RUN' not in LOG_rad, forretningsmål.stderr
            rapport_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            forretningsmål=sikker_grensesnitt(Innstillingar['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Utdata/'ssh.log').write_bytes(forretningsmål.stderr)
            (Utdata/'ssh-output.txt').write_bytes(forretningsmål.stdout)
            assert forretningsmål.returncode==0 and b'SSH_NATIVE_PASS' in forretningsmål.stdout, (forretningsmål.returncode,forretningsmål.stdout,forretningsmål.stderr)
            rapport_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in forretningsmål.stderr, forretningsmål.stderr
            rapport_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            forretningsmål=sikker_grensesnitt(Innstillingar['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert forretningsmål.returncode==0 and 'JAVA Utdata: 안녕하세요 😀'.encode() in forretningsmål.stdout,forretningsmål.stdout
            rapport_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            forretningsmål=sikker_grensesnitt(Innstillingar['ssh_password'], 'missing_remote_command')
            assert forretningsmål.returncode==127,forretningsmål.returncode
            rapport_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            forretningsmål=sikker_grensesnitt(Innstillingar['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Utdata/'ssh-rekey.log').write_bytes(forretningsmål.stderr)
            assert forretningsmål.returncode==0 and 'class 창예제'.encode() in forretningsmål.stdout, (forretningsmål.returncode,forretningsmål.stdout,forretningsmål.stderr)
            assert forretningsmål.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, forretningsmål.stderr
            rapport_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(grensesnitt_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_økt=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();merkt_område_VALUE=selectors.DefaultSelector();merkt_område_VALUE.register(interaktiv_økt.stdout,selectors.EVENT_READ)
            def 대화읽기(vise_VALUE_487749b8):
                마감=time.monotonic()+30
                while vise_VALUE_487749b8 not in 대화기록:
                    if time.monotonic()>마감 or interaktiv_økt.poll() is not None:raise AssertionError('SSH interactive missing '+repr(vise_VALUE_487749b8)+' '+repr(bytes(대화기록)))
                    for oppføring_VALUE,_ in merkt_område_VALUE.select(.1):
                        조각=oppføring_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiv_økt.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_økt.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_økt.stdin.write(b'\x04');interaktiv_økt.stdin.flush();나머지,FEIL=interaktiv_økt.communicate(timeout=15)
                assert interaktiv_økt.returncode==0 and b'PTY allocation request failed' not in FEIL,(interaktiv_økt.returncode,FEIL)
                (Utdata/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                merkt_område_VALUE.close()
                if interaktiv_økt.poll() is None:interaktiv_økt.kill();interaktiv_økt.wait()
            rapport_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Kopla_til, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=Kopla_til.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(passord_VALUE):
                Kopla_til=socket.create_connection(('127.0.0.5',화면포트),10);Kopla_til.settimeout(30)
                assert 정확히(Kopla_til,12)==b'RFB 003.008\n'
                Kopla_til.sendall(b'RFB 003.008\n');assert 정확히(Kopla_til,2)==b'\x01\x02'
                Kopla_til.sendall(b'\x02');utfordring_VALUE=정확히(Kopla_til,16)
                입력암호=passord_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Kopla_til.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(utfordring_VALUE))
                status_VALUE=struct.unpack('!I',정확히(Kopla_til,4))[0]
                return Kopla_til,status_VALUE
            ugyldig_passord='!' if not Innstillingar['vnc_password'].startswith('!') else '?'
            Kopla_til,status_VALUE=화면인증(ugyldig_passord);assert status_VALUE==1;Kopla_til.close();time.sleep(.6)
            rapport_VALUE['checks'].append('VNC incorrect password rejected')
            Kopla_til,status_VALUE=화면인증(Innstillingar['vnc_password']);assert status_VALUE==0
            with Kopla_til:
                Kopla_til.sendall(b'\x01');초기=정확히(Kopla_til,24);너비,높이=struct.unpack('!HH',초기[:4]);Namn=정확히(Kopla_til,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Namn
                def 화면(증분=0):
                    Kopla_til.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Kopla_til,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    teikning_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinat,Y_koordinat,영역너비,영역높이,metode_MODE=struct.unpack('!HHHHi',정확히(Kopla_til,12));assert metode_MODE==0 and x_koordinat+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        piksel=정확히(Kopla_til,영역너비*영역높이*4);합계+=len(piksel)
                        for linje in range(영역높이):teikning_VALUE[((Y_koordinat+linje)*너비+x_koordinat)*4:((Y_koordinat+linje)*너비+x_koordinat+영역너비)*4]=piksel[linje*영역너비*4:(linje+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(teikning_VALUE),'raw','BGRX').save(str(Utdata/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                rapport_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                rapport_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_rad)
                for teikn_VALUE in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if teikn_VALUE=='\r' else ord(teikn_VALUE)
                    Kopla_til.sendall(struct.pack('!BBHI',4,1,0,symbol));Kopla_til.sendall(struct.pack('!BBHI',4,0,0,symbol))
                vent_status(b'VNC_NATIVE_PASS',처음)
                rapport_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(symbol,trykkje_VALUE=1):Kopla_til.sendall(struct.pack('!BBHI',4,trykkje_VALUE,0,symbol))
                처음=len(LOG_rad)
                for teikn_VALUE in 'echo ':글쇠(ord(teikn_VALUE))
                글쇠(0xffc6)
                for teikn_VALUE in 'gksrmf':글쇠(ord(teikn_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                vent_status('\r\n한글\r\n'.encode(),처음)
                rapport_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Kopla_til.sendall(struct.pack('!BBHH',5,0,120,100))
                rapport_VALUE['checks'].append('VNC pointer input accepted')
            Prosess_VALUE.stdin.write(b'poweroff\n');Prosess_VALUE.stdin.flush();Prosess_VALUE.wait(timeout=15);assert Prosess_VALUE.returncode==0
            rapport_VALUE['passed']=True
    finally:
        if Prosess_VALUE and Prosess_VALUE.poll() is None:
            Prosess_VALUE.terminate()
            try: Prosess_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess_VALUE.kill();Prosess_VALUE.wait()
        (Utdata/'serial.log').write_bytes(LOG_rad)
        (Utdata/'report.json').write_text(json.dumps(rapport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(rapport_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Køyr_2()
