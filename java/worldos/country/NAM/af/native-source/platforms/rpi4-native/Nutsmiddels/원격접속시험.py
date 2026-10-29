#!/usr/bin/env python3
"""werklik_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from uitvoer_bevel import Project_wortel, Opdrag
from Netwerk_brug import Netwerk_brug


def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--kernel', type=Path, default=Project_wortel / 'build/kernel8.img')
    ontleder_48ee4b1b.add_argument('--access', type=Path, default=Project_wortel / 'build/remote/access.json')
    ontleder_48ee4b1b.add_argument('--output', type=Path, default=Project_wortel / 'build/verification/native-remote')
    인수 = ontleder_48ee4b1b.parse_args()
    Afvoer = 인수.output
    Afvoer.mkdir(parents=True, exist_ok=True)
    Instellings = json.loads(인수.access.read_text())
    verslag_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def leeg_ombou():
        with socket.socket() as Koppel:
            Koppel.bind(('127.0.0.5', 0))
            return Koppel.getsockname()[1]
    dop_ombou, 화면포트, lêer_ombou = leeg_ombou(), leeg_ombou(), leeg_ombou()
    LOG_ry = bytearray()
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Netwerk_brug(lêer_ombou,
                ['tcp:{}:22'.format(dop_ombou), 'tcp:{}:5900'.format(화면포트)], hou_adres='127.0.0.5') as brug_VALUE:
            실행인수 = Opdrag()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proses_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + brug_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proses_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_ry.extend(data)
            draad_VALUE = threading.Thread(target=수집, daemon=True)
            draad_VALUE.start()
            def wag_stand(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_ry[처음:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_ry[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            wag_stand(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def beveiligde_dop(wagwoord_VALUE, instruksie_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=wagwoord_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(dop_ombou),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksie_VALUE]
                maatreël=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return maatreël
            maatreël=beveiligde_dop('!' + Instellings['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Afvoer/'ssh-rejected.log').write_bytes(maatreël.stderr)
            assert maatreël.returncode!=0 and b'Permission denied' in maatreël.stderr and b'SHOULD_NOT_RUN' not in LOG_ry, maatreël.stderr
            verslag_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            maatreël=beveiligde_dop(Instellings['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Afvoer/'ssh.log').write_bytes(maatreël.stderr)
            (Afvoer/'ssh-output.txt').write_bytes(maatreël.stdout)
            assert maatreël.returncode==0 and b'SSH_NATIVE_PASS' in maatreël.stdout, (maatreël.returncode,maatreël.stdout,maatreël.stderr)
            verslag_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in maatreël.stderr, maatreël.stderr
            verslag_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            maatreël=beveiligde_dop(Instellings['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert maatreël.returncode==0 and 'JAVA Afvoer: 안녕하세요 😀'.encode() in maatreël.stdout,maatreël.stdout
            verslag_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            maatreël=beveiligde_dop(Instellings['ssh_password'], 'missing_remote_command')
            assert maatreël.returncode==127,maatreël.returncode
            verslag_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            maatreël=beveiligde_dop(Instellings['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Afvoer/'ssh-rekey.log').write_bytes(maatreël.stderr)
            assert maatreël.returncode==0 and 'class 창예제'.encode() in maatreël.stdout, (maatreël.returncode,maatreël.stdout,maatreël.stderr)
            assert maatreël.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, maatreël.stderr
            verslag_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(dop_ombou),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktief_sessie=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();seleksie_VALUE=selectors.DefaultSelector();seleksie_VALUE.register(interaktief_sessie.stdout,selectors.EVENT_READ)
            def 대화읽기(wys_VALUE):
                마감=time.monotonic()+30
                while wys_VALUE not in 대화기록:
                    if time.monotonic()>마감 or interaktief_sessie.poll() is not None:raise AssertionError('SSH interactive missing '+repr(wys_VALUE)+' '+repr(bytes(대화기록)))
                    for inskrywing_VALUE,_ in seleksie_VALUE.select(.1):
                        조각=inskrywing_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktief_sessie.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktief_sessie.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktief_sessie.stdin.write(b'\x04');interaktief_sessie.stdin.flush();나머지,Fout=interaktief_sessie.communicate(timeout=15)
                assert interaktief_sessie.returncode==0 and b'PTY allocation request failed' not in Fout,(interaktief_sessie.returncode,Fout)
                (Afvoer/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                seleksie_VALUE.close()
                if interaktief_sessie.poll() is None:interaktief_sessie.kill();interaktief_sessie.wait()
            verslag_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Koppel, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=Koppel.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(wagwoord_VALUE):
                Koppel=socket.create_connection(('127.0.0.5',화면포트),10);Koppel.settimeout(30)
                assert 정확히(Koppel,12)==b'RFB 003.008\n'
                Koppel.sendall(b'RFB 003.008\n');assert 정확히(Koppel,2)==b'\x01\x02'
                Koppel.sendall(b'\x02');uitdaging_VALUE=정확히(Koppel,16)
                입력암호=wagwoord_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Koppel.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(uitdaging_VALUE))
                stand_VALUE=struct.unpack('!I',정확히(Koppel,4))[0]
                return Koppel,stand_VALUE
            ongeldig_wagwoord='!' if not Instellings['vnc_password'].startswith('!') else '?'
            Koppel,stand_VALUE=화면인증(ongeldig_wagwoord);assert stand_VALUE==1;Koppel.close();time.sleep(.6)
            verslag_VALUE['checks'].append('VNC incorrect password rejected')
            Koppel,stand_VALUE=화면인증(Instellings['vnc_password']);assert stand_VALUE==0
            with Koppel:
                Koppel.sendall(b'\x01');초기=정확히(Koppel,24);너비,높이=struct.unpack('!HH',초기[:4]);Naam=정확히(Koppel,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Naam
                def 화면(증분=0):
                    Koppel.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Koppel,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    tekening_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koördinaat,Y_koördinaat,영역너비,영역높이,metode_MODE=struct.unpack('!HHHHi',정확히(Koppel,12));assert metode_MODE==0 and x_koördinaat+영역너비<=너비 and Y_koördinaat+영역높이<=높이
                        pieksel=정확히(Koppel,영역너비*영역높이*4);합계+=len(pieksel)
                        for lyn in range(영역높이):tekening_VALUE[((Y_koördinaat+lyn)*너비+x_koördinaat)*4:((Y_koördinaat+lyn)*너비+x_koördinaat+영역너비)*4]=pieksel[lyn*영역너비*4:(lyn+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(tekening_VALUE),'raw','BGRX').save(str(Afvoer/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                verslag_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                verslag_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_ry)
                for karakter_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbool=0xff0d if karakter_VALUE=='\r' else ord(karakter_VALUE)
                    Koppel.sendall(struct.pack('!BBHI',4,1,0,simbool));Koppel.sendall(struct.pack('!BBHI',4,0,0,simbool))
                wag_stand(b'VNC_NATIVE_PASS',처음)
                verslag_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbool,druk_VALUE=1):Koppel.sendall(struct.pack('!BBHI',4,druk_VALUE,0,simbool))
                처음=len(LOG_ry)
                for karakter_VALUE in 'echo ':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6)
                for karakter_VALUE in 'gksrmf':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                wag_stand('\r\n한글\r\n'.encode(),처음)
                verslag_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Koppel.sendall(struct.pack('!BBHH',5,0,120,100))
                verslag_VALUE['checks'].append('VNC pointer input accepted')
            Proses_VALUE.stdin.write(b'poweroff\n');Proses_VALUE.stdin.flush();Proses_VALUE.wait(timeout=15);assert Proses_VALUE.returncode==0
            verslag_VALUE['passed']=True
    finally:
        if Proses_VALUE and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses_VALUE.kill();Proses_VALUE.wait()
        (Afvoer/'serial.log').write_bytes(LOG_ry)
        (Afvoer/'report.json').write_text(json.dumps(verslag_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(verslag_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Loop()
