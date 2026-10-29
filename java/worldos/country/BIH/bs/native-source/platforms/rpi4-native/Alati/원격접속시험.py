#!/usr/bin/env python3
"""stvaran_podaci OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Izvrši_komanda import projicirati_koijen, Naredba
from Mreža_most import Mreža_most


def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=projicirati_koijen / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=projicirati_koijen / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=projicirati_koijen / 'build/verification/native-remote')
    Argumenti = 해석기.parse_args()
    Ispis = Argumenti.output
    Ispis.mkdir(parents=True, exist_ok=True)
    Postavke = json.loads(Argumenti.access.read_text())
    izvještaj_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenti.kernel.read_bytes()).hexdigest(), 'checks': []}
    def prazno_port():
        with socket.socket() as Spoji_se:
            Spoji_se.bind(('127.0.0.5', 0))
            return Spoji_se.getsockname()[1]
    ljuska_port, 화면포트, fajl_port = prazno_port(), prazno_port(), prazno_port()
    LOG_red = bytearray()
    proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Mreža_most(fajl_port,
                ['tcp:{}:22'.format(ljuska_port), 'tcp:{}:5900'.format(화면포트)], organizator_adresa='127.0.0.5') as most_VALUE:
            실행인수 = Naredba()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenti.kernel.resolve())
            proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    podaci = proces_VALUE.stdout.read(4096)
                    if not podaci: break
                    LOG_red.extend(podaci)
            nit_VALUE = threading.Thread(target=수집, daemon=True)
            nit_VALUE.start()
            def čekaj_stanje(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_red[처음:]:
                    if time.monotonic()>끝 or proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_red[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            čekaj_stanje(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            operativno_okruženje = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def sigurno_ljuska(lozinka_VALUE, programska_naredba_VALUE, 추가=()):
                operativno_okruženje['JKOROS_TEST_PASSWORD']=lozinka_VALUE
                Argumenti=['ssh','-v']+list(추가)+['-p',str(ljuska_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',programska_naredba_VALUE]
                mjera=subprocess.run(Argumenti,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=operativno_okruženje,start_new_session=True,timeout=50)
                return mjera
            mjera=sigurno_ljuska('!' + Postavke['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Ispis/'ssh-rejected.log').write_bytes(mjera.stderr)
            assert mjera.returncode!=0 and b'Permission denied' in mjera.stderr and b'SHOULD_NOT_RUN' not in LOG_red, mjera.stderr
            izvještaj_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            mjera=sigurno_ljuska(Postavke['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Ispis/'ssh.log').write_bytes(mjera.stderr)
            (Ispis/'ssh-output.txt').write_bytes(mjera.stdout)
            assert mjera.returncode==0 and b'SSH_NATIVE_PASS' in mjera.stdout, (mjera.returncode,mjera.stdout,mjera.stderr)
            izvještaj_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in mjera.stderr, mjera.stderr
            izvještaj_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            mjera=sigurno_ljuska(Postavke['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert mjera.returncode==0 and 'JAVA Ispis: 안녕하세요 😀'.encode() in mjera.stdout,mjera.stdout
            izvještaj_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            mjera=sigurno_ljuska(Postavke['ssh_password'], 'missing_remote_command')
            assert mjera.returncode==127,mjera.returncode
            izvještaj_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            mjera=sigurno_ljuska(Postavke['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Ispis/'ssh-rekey.log').write_bytes(mjera.stderr)
            assert mjera.returncode==0 and 'class 창예제'.encode() in mjera.stdout, (mjera.returncode,mjera.stdout,mjera.stderr)
            assert mjera.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, mjera.stderr
            izvještaj_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ljuska_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktivno_sesija=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=operativno_okruženje,start_new_session=True,bufsize=0)
            대화기록=bytearray();izbor_VALUE=selectors.DefaultSelector();izbor_VALUE.register(interaktivno_sesija.stdout,selectors.EVENT_READ)
            def 대화읽기(program_VALUE):
                마감=time.monotonic()+30
                while program_VALUE not in 대화기록:
                    if time.monotonic()>마감 or interaktivno_sesija.poll() is not None:raise AssertionError('SSH interactive missing '+repr(program_VALUE)+' '+repr(bytes(대화기록)))
                    for unos_VALUE,_ in izbor_VALUE.select(.1):
                        조각=unos_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktivno_sesija.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktivno_sesija.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktivno_sesija.stdin.write(b'\x04');interaktivno_sesija.stdin.flush();나머지,GRESKA=interaktivno_sesija.communicate(timeout=15)
                assert interaktivno_sesija.returncode==0 and b'PTY allocation request failed' not in GRESKA,(interaktivno_sesija.returncode,GRESKA)
                (Ispis/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                izbor_VALUE.close()
                if interaktivno_sesija.poll() is None:interaktivno_sesija.kill();interaktivno_sesija.wait()
            izvještaj_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Spoji_se, 수):
                podaci=bytearray()
                while len(podaci)<수:
                    덩이=Spoji_se.recv(수-len(podaci))
                    if not 덩이: raise AssertionError('RFB EOF')
                    podaci.extend(덩이)
                return bytes(podaci)
            def 화면인증(lozinka_VALUE):
                Spoji_se=socket.create_connection(('127.0.0.5',화면포트),10);Spoji_se.settimeout(30)
                assert 정확히(Spoji_se,12)==b'RFB 003.008\n'
                Spoji_se.sendall(b'RFB 003.008\n');assert 정확히(Spoji_se,2)==b'\x01\x02'
                Spoji_se.sendall(b'\x02');test_VALUE=정확히(Spoji_se,16)
                입력암호=lozinka_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Spoji_se.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(test_VALUE))
                stanje_VALUE=struct.unpack('!I',정확히(Spoji_se,4))[0]
                return Spoji_se,stanje_VALUE
            nevažeće_lozinka='!' if not Postavke['vnc_password'].startswith('!') else '?'
            Spoji_se,stanje_VALUE=화면인증(nevažeće_lozinka);assert stanje_VALUE==1;Spoji_se.close();time.sleep(.6)
            izvještaj_VALUE['checks'].append('VNC incorrect password rejected')
            Spoji_se,stanje_VALUE=화면인증(Postavke['vnc_password']);assert stanje_VALUE==0
            with Spoji_se:
                Spoji_se.sendall(b'\x01');초기=정확히(Spoji_se,24);너비,높이=struct.unpack('!HH',초기[:4]);Naziv=정확히(Spoji_se,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Naziv
                def 화면(증분=0):
                    Spoji_se.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Spoji_se,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ucrtavanje_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        koordinata_x,Y_koordinata,영역너비,영역높이,metoda_mod=struct.unpack('!HHHHi',정확히(Spoji_se,12));assert metoda_mod==0 and koordinata_x+영역너비<=너비 and Y_koordinata+영역높이<=높이
                        pel=정확히(Spoji_se,영역너비*영역높이*4);합계+=len(pel)
                        for Linija in range(영역높이):ucrtavanje_VALUE[((Y_koordinata+Linija)*너비+koordinata_x)*4:((Y_koordinata+Linija)*너비+koordinata_x+영역너비)*4]=pel[Linija*영역너비*4:(Linija+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ucrtavanje_VALUE),'raw','BGRX').save(str(Ispis/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                izvještaj_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                izvještaj_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_red)
                for znak_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if znak_VALUE=='\r' else ord(znak_VALUE)
                    Spoji_se.sendall(struct.pack('!BBHI',4,1,0,simbol));Spoji_se.sendall(struct.pack('!BBHI',4,0,0,simbol))
                čekaj_stanje(b'VNC_NATIVE_PASS',처음)
                izvještaj_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbol,pritisnuti_VALUE=1):Spoji_se.sendall(struct.pack('!BBHI',4,pritisnuti_VALUE,0,simbol))
                처음=len(LOG_red)
                for znak_VALUE in 'echo ':글쇠(ord(znak_VALUE))
                글쇠(0xffc6)
                for znak_VALUE in 'gksrmf':글쇠(ord(znak_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                čekaj_stanje('\r\n한글\r\n'.encode(),처음)
                izvještaj_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Spoji_se.sendall(struct.pack('!BBHH',5,0,120,100))
                izvještaj_VALUE['checks'].append('VNC pointer input accepted')
            proces_VALUE.stdin.write(b'poweroff\n');proces_VALUE.stdin.flush();proces_VALUE.wait(timeout=15);assert proces_VALUE.returncode==0
            izvještaj_VALUE['passed']=True
    finally:
        if proces_VALUE and proces_VALUE.poll() is None:
            proces_VALUE.terminate()
            try: proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: proces_VALUE.kill();proces_VALUE.wait()
        (Ispis/'serial.log').write_bytes(LOG_red)
        (Ispis/'report.json').write_text(json.dumps(izvještaj_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(izvještaj_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Pokreni()
