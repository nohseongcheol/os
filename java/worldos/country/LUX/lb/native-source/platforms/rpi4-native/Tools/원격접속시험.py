#!/usr/bin/env python3
"""aktuell_Daten OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ausféieren_Befeel import projezéieren_Racinn, Befeel
from Reseau_Bréck import Reseau_Bréck


def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=projezéieren_Racinn / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=projezéieren_Racinn / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=projezéieren_Racinn / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Astellungen = json.loads(인수.access.read_text())
    mellen_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def eidel_Port():
        with socket.socket() as Verbannen:
            Verbannen.bind(('127.0.0.5', 0))
            return Verbannen.getsockname()[1]
    Shell_Port, 화면포트, Fichier_Port = eidel_Port(), eidel_Port(), eidel_Port()
    LOG_Rei = bytearray()
    Prozess_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Reseau_Bréck(Fichier_Port,
                ['tcp:{}:22'.format(Shell_Port), 'tcp:{}:5900'.format(화면포트)], Host_Adress='127.0.0.5') as Bréck_VALUE:
            실행인수 = Befeel()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Prozess_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + Bréck_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    Daten = Prozess_VALUE.stdout.read(4096)
                    if not Daten: break
                    LOG_Rei.extend(Daten)
            Thread_VALUE = threading.Thread(target=수집, daemon=True)
            Thread_VALUE.start()
            def Waart_Status(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_Rei[처음:]:
                    if time.monotonic()>끝 or Prozess_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_Rei[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            Waart_Status(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def sécher_Shell(Passwuert_VALUE, Instruktioun_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=Passwuert_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(Shell_Port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',Instruktioun_VALUE]
                Mooss=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return Mooss
            Mooss=sécher_Shell('!' + Astellungen['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(Mooss.stderr)
            assert Mooss.returncode!=0 and b'Permission denied' in Mooss.stderr and b'SHOULD_NOT_RUN' not in LOG_Rei, Mooss.stderr
            mellen_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            Mooss=sécher_Shell(Astellungen['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(Mooss.stderr)
            (출력/'ssh-output.txt').write_bytes(Mooss.stdout)
            assert Mooss.returncode==0 and b'SSH_NATIVE_PASS' in Mooss.stdout, (Mooss.returncode,Mooss.stdout,Mooss.stderr)
            mellen_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in Mooss.stderr, Mooss.stderr
            mellen_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            Mooss=sécher_Shell(Astellungen['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert Mooss.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in Mooss.stdout,Mooss.stdout
            mellen_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            Mooss=sécher_Shell(Astellungen['ssh_password'], 'missing_remote_command')
            assert Mooss.returncode==127,Mooss.returncode
            mellen_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            Mooss=sécher_Shell(Astellungen['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(Mooss.stderr)
            assert Mooss.returncode==0 and 'class 창예제'.encode() in Mooss.stdout, (Mooss.returncode,Mooss.stdout,Mooss.stderr)
            assert Mooss.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, Mooss.stderr
            mellen_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_Port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_Sessioun=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();Auswiel_VALUE=selectors.DefaultSelector();Auswiel_VALUE.register(interaktiv_Sessioun.stdout,selectors.EVENT_READ)
            def 대화읽기(Show_VALUE):
                마감=time.monotonic()+30
                while Show_VALUE not in 대화기록:
                    if time.monotonic()>마감 or interaktiv_Sessioun.poll() is not None:raise AssertionError('SSH interactive missing '+repr(Show_VALUE)+' '+repr(bytes(대화기록)))
                    for Agab_VALUE,_ in Auswiel_VALUE.select(.1):
                        조각=Agab_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiv_Sessioun.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_Sessioun.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_Sessioun.stdin.write(b'\x04');interaktiv_Sessioun.stdin.flush();나머지,Feeler=interaktiv_Sessioun.communicate(timeout=15)
                assert interaktiv_Sessioun.returncode==0 and b'PTY allocation request failed' not in Feeler,(interaktiv_Sessioun.returncode,Feeler)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                Auswiel_VALUE.close()
                if interaktiv_Sessioun.poll() is None:interaktiv_Sessioun.kill();interaktiv_Sessioun.wait()
            mellen_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Verbannen, 수):
                Daten=bytearray()
                while len(Daten)<수:
                    덩이=Verbannen.recv(수-len(Daten))
                    if not 덩이: raise AssertionError('RFB EOF')
                    Daten.extend(덩이)
                return bytes(Daten)
            def 화면인증(Passwuert_VALUE):
                Verbannen=socket.create_connection(('127.0.0.5',화면포트),10);Verbannen.settimeout(30)
                assert 정확히(Verbannen,12)==b'RFB 003.008\n'
                Verbannen.sendall(b'RFB 003.008\n');assert 정확히(Verbannen,2)==b'\x01\x02'
                Verbannen.sendall(b'\x02');Opfuerderung_VALUE=정확히(Verbannen,16)
                입력암호=Passwuert_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Verbannen.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(Opfuerderung_VALUE))
                Status_VALUE=struct.unpack('!I',정확히(Verbannen,4))[0]
                return Verbannen,Status_VALUE
            ongëlteg_Passwuert='!' if not Astellungen['vnc_password'].startswith('!') else '?'
            Verbannen,Status_VALUE=화면인증(ongëlteg_Passwuert);assert Status_VALUE==1;Verbannen.close();time.sleep(.6)
            mellen_VALUE['checks'].append('VNC incorrect password rejected')
            Verbannen,Status_VALUE=화면인증(Astellungen['vnc_password']);assert Status_VALUE==0
            with Verbannen:
                Verbannen.sendall(b'\x01');초기=정확히(Verbannen,24);너비,높이=struct.unpack('!HH',초기[:4]);Numm=정확히(Verbannen,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Numm
                def 화면(증분=0):
                    Verbannen.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Verbannen,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    Zeechnung_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_Koordinat,세로좌표,영역너비,영역높이,Method_MODE=struct.unpack('!HHHHi',정확히(Verbannen,12));assert Method_MODE==0 and X_Koordinat+영역너비<=너비 and 세로좌표+영역높이<=높이
                        Pel=정확히(Verbannen,영역너비*영역높이*4);합계+=len(Pel)
                        for Zeil in range(영역높이):Zeechnung_VALUE[((세로좌표+Zeil)*너비+X_Koordinat)*4:((세로좌표+Zeil)*너비+X_Koordinat+영역너비)*4]=Pel[Zeil*영역너비*4:(Zeil+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(Zeechnung_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                mellen_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                mellen_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_Rei)
                for Zeechen_VALUE in 'echo VNC_NATIVE_PASS\r':
                    Symbol=0xff0d if Zeechen_VALUE=='\r' else ord(Zeechen_VALUE)
                    Verbannen.sendall(struct.pack('!BBHI',4,1,0,Symbol));Verbannen.sendall(struct.pack('!BBHI',4,0,0,Symbol))
                Waart_Status(b'VNC_NATIVE_PASS',처음)
                mellen_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(Symbol,누름=1):Verbannen.sendall(struct.pack('!BBHI',4,누름,0,Symbol))
                처음=len(LOG_Rei)
                for Zeechen_VALUE in 'echo ':글쇠(ord(Zeechen_VALUE))
                글쇠(0xffc6)
                for Zeechen_VALUE in 'gksrmf':글쇠(ord(Zeechen_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                Waart_Status('\r\n한글\r\n'.encode(),처음)
                mellen_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Verbannen.sendall(struct.pack('!BBHH',5,0,120,100))
                mellen_VALUE['checks'].append('VNC pointer input accepted')
            Prozess_VALUE.stdin.write(b'poweroff\n');Prozess_VALUE.stdin.flush();Prozess_VALUE.wait(timeout=15);assert Prozess_VALUE.returncode==0
            mellen_VALUE['passed']=True
    finally:
        if Prozess_VALUE and Prozess_VALUE.poll() is None:
            Prozess_VALUE.terminate()
            try: Prozess_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Prozess_VALUE.kill();Prozess_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_Rei)
        (출력/'report.json').write_text(json.dumps(mellen_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(mellen_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Laf()
