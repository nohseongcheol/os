#!/usr/bin/env python3
"""benetako_datuak OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from exekutatu_komando import Project_erro, Komandoa
from sare_zubi import sare_zubi


def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--kernel', type=Path, default=Project_erro / 'build/kernel8.img')
    analizatzaile_48ee4b1b.add_argument('--access', type=Path, default=Project_erro / 'build/remote/access.json')
    analizatzaile_48ee4b1b.add_argument('--output', type=Path, default=Project_erro / 'build/verification/native-remote')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    Irteera = Argumentuak.output
    Irteera.mkdir(parents=True, exist_ok=True)
    Ezarpenak = json.loads(Argumentuak.access.read_text())
    txosten_balio = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumentuak.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Konektatu:
            Konektatu.bind(('127.0.0.5', 0))
            return Konektatu.getsockname()[1]
    shell_ataka, 화면포트, fitxategi_ataka = 빈포트(), 빈포트(), 빈포트()
    LOG_marka = bytearray()
    prozesu_balio = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, sare_zubi(fitxategi_ataka,
                ['tcp:{}:22'.format(shell_ataka), 'tcp:{}:5900'.format(화면포트)], Ostalari_helbide='127.0.0.5') as zubi_balio:
            실행인수 = Komandoa()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumentuak.kernel.resolve())
            prozesu_balio = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + zubi_balio.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    datuak = prozesu_balio.stdout.read(4096)
                    if not datuak: break
                    LOG_marka.extend(datuak)
            hari_balio = threading.Thread(target=수집, daemon=True)
            hari_balio.start()
            def itxaron_Egoera(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_marka[처음:]:
                    if time.monotonic()>끝 or prozesu_balio.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_marka[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            itxaron_Egoera(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def seguru_shell(pasahitz_balio, instrukzio_balio_4c26ea1b, Erantsi_sarrera=()):
                환경['JKOROS_TEST_PASSWORD']=pasahitz_balio
                Argumentuak=['ssh','-v']+list(Erantsi_sarrera)+['-p',str(shell_ataka),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instrukzio_balio_4c26ea1b]
                EMAITZA=subprocess.run(Argumentuak,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return EMAITZA
            EMAITZA=seguru_shell('!' + Ezarpenak['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Irteera/'ssh-rejected.log').write_bytes(EMAITZA.stderr)
            assert EMAITZA.returncode!=0 and b'Permission denied' in EMAITZA.stderr and b'SHOULD_NOT_RUN' not in LOG_marka, EMAITZA.stderr
            txosten_balio['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            EMAITZA=seguru_shell(Ezarpenak['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Irteera/'ssh.log').write_bytes(EMAITZA.stderr)
            (Irteera/'ssh-output.txt').write_bytes(EMAITZA.stdout)
            assert EMAITZA.returncode==0 and b'SSH_NATIVE_PASS' in EMAITZA.stdout, (EMAITZA.returncode,EMAITZA.stdout,EMAITZA.stderr)
            txosten_balio['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in EMAITZA.stderr, EMAITZA.stderr
            txosten_balio['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            EMAITZA=seguru_shell(Ezarpenak['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert EMAITZA.returncode==0 and 'JAVA Irteera: 안녕하세요 😀'.encode() in EMAITZA.stdout,EMAITZA.stdout
            txosten_balio['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            EMAITZA=seguru_shell(Ezarpenak['ssh_password'], 'missing_remote_command')
            assert EMAITZA.returncode==127,EMAITZA.returncode
            txosten_balio['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            EMAITZA=seguru_shell(Ezarpenak['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Irteera/'ssh-rekey.log').write_bytes(EMAITZA.stderr)
            assert EMAITZA.returncode==0 and 'class 창예제'.encode() in EMAITZA.stdout, (EMAITZA.returncode,EMAITZA.stdout,EMAITZA.stderr)
            assert EMAITZA.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, EMAITZA.stderr
            txosten_balio['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_ataka),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktibo_saio=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();hautapen_balio=selectors.DefaultSelector();hautapen_balio.register(interaktibo_saio.stdout,selectors.EVENT_READ)
            def 대화읽기(erakutsi_balio):
                마감=time.monotonic()+30
                while erakutsi_balio not in 대화기록:
                    if time.monotonic()>마감 or interaktibo_saio.poll() is not None:raise AssertionError('SSH interactive missing '+repr(erakutsi_balio)+' '+repr(bytes(대화기록)))
                    for sarrera_balio,_ in hautapen_balio.select(.1):
                        조각=sarrera_balio.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktibo_saio.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktibo_saio.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktibo_saio.stdin.write(b'\x04');interaktibo_saio.stdin.flush();나머지,errorea=interaktibo_saio.communicate(timeout=15)
                assert interaktibo_saio.returncode==0 and b'PTY allocation request failed' not in errorea,(interaktibo_saio.returncode,errorea)
                (Irteera/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                hautapen_balio.close()
                if interaktibo_saio.poll() is None:interaktibo_saio.kill();interaktibo_saio.wait()
            txosten_balio['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Konektatu, 수):
                datuak=bytearray()
                while len(datuak)<수:
                    덩이=Konektatu.recv(수-len(datuak))
                    if not 덩이: raise AssertionError('RFB EOF')
                    datuak.extend(덩이)
                return bytes(datuak)
            def 화면인증(pasahitz_balio):
                Konektatu=socket.create_connection(('127.0.0.5',화면포트),10);Konektatu.settimeout(30)
                assert 정확히(Konektatu,12)==b'RFB 003.008\n'
                Konektatu.sendall(b'RFB 003.008\n');assert 정확히(Konektatu,2)==b'\x01\x02'
                Konektatu.sendall(b'\x02');erronka_balio=정확히(Konektatu,16)
                입력암호=pasahitz_balio.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Konektatu.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(erronka_balio))
                Egoera_balio=struct.unpack('!I',정확히(Konektatu,4))[0]
                return Konektatu,Egoera_balio
            baliogabe_pasahitz='!' if not Ezarpenak['vnc_password'].startswith('!') else '?'
            Konektatu,Egoera_balio=화면인증(baliogabe_pasahitz);assert Egoera_balio==1;Konektatu.close();time.sleep(.6)
            txosten_balio['checks'].append('VNC incorrect password rejected')
            Konektatu,Egoera_balio=화면인증(Ezarpenak['vnc_password']);assert Egoera_balio==0
            with Konektatu:
                Konektatu.sendall(b'\x01');초기=정확히(Konektatu,24);너비,높이=struct.unpack('!HH',초기[:4]);Izena=정확히(Konektatu,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Izena
                def 화면(증분=0):
                    Konektatu.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Konektatu,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    그림=bytearray(너비*높이*4)
                    for _ in range(수):
                        X_koordenatu,Y_koordenatu,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(Konektatu,12));assert 방식==0 and X_koordenatu+영역너비<=너비 and Y_koordenatu+영역높이<=높이
                        pixel=정확히(Konektatu,영역너비*영역높이*4);합계+=len(pixel)
                        for Marra in range(영역높이):그림[((Y_koordenatu+Marra)*너비+X_koordenatu)*4:((Y_koordenatu+Marra)*너비+X_koordenatu+영역너비)*4]=pixel[Marra*영역너비*4:(Marra+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(그림),'raw','BGRX').save(str(Irteera/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                txosten_balio['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                txosten_balio['checks'].append('RFB incremental update')
                처음=len(LOG_marka)
                for karaktere_balio in 'echo VNC_NATIVE_PASS\r':
                    ikur=0xff0d if karaktere_balio=='\r' else ord(karaktere_balio)
                    Konektatu.sendall(struct.pack('!BBHI',4,1,0,ikur));Konektatu.sendall(struct.pack('!BBHI',4,0,0,ikur))
                itxaron_Egoera(b'VNC_NATIVE_PASS',처음)
                txosten_balio['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ikur,sakatu_balio=1):Konektatu.sendall(struct.pack('!BBHI',4,sakatu_balio,0,ikur))
                처음=len(LOG_marka)
                for karaktere_balio in 'echo ':글쇠(ord(karaktere_balio))
                글쇠(0xffc6)
                for karaktere_balio in 'gksrmf':글쇠(ord(karaktere_balio))
                글쇠(0xffc6);글쇠(0xff0d)
                itxaron_Egoera('\r\n한글\r\n'.encode(),처음)
                txosten_balio['checks'].append('Native VNC F9 two-set Hangul composition')
                Konektatu.sendall(struct.pack('!BBHH',5,0,120,100))
                txosten_balio['checks'].append('VNC pointer input accepted')
            prozesu_balio.stdin.write(b'poweroff\n');prozesu_balio.stdin.flush();prozesu_balio.wait(timeout=15);assert prozesu_balio.returncode==0
            txosten_balio['passed']=True
    finally:
        if prozesu_balio and prozesu_balio.poll() is None:
            prozesu_balio.terminate()
            try: prozesu_balio.wait(timeout=5)
            except subprocess.TimeoutExpired: prozesu_balio.kill();prozesu_balio.wait()
        (Irteera/'serial.log').write_bytes(LOG_marka)
        (Irteera/'report.json').write_text(json.dumps(txosten_balio,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(txosten_balio,ensure_ascii=False,indent=2))


if __name__=='__main__': Exekutatu_2()
