#!/usr/bin/env python3
"""stvarni_podaci OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Izvrši_komanda import radnja_koren, komanda
from mrežni_most import mrežni_most


def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--kernel', type=Path, default=radnja_koren / 'build/kernel8.img')
    analizator_48ee4b1b.add_argument('--access', type=Path, default=radnja_koren / 'build/remote/access.json')
    analizator_48ee4b1b.add_argument('--output', type=Path, default=radnja_koren / 'build/verification/native-remote')
    인수 = analizator_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Postavke = json.loads(인수.access.read_text())
    izveštaj_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as veze:
            veze.bind(('127.0.0.5', 0))
            return veze.getsockname()[1]
    ljuska_port, 화면포트, Datoteka_port = 빈포트(), 빈포트(), 빈포트()
    LOG_snimi = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, mrežni_most(Datoteka_port,
                ['tcp:{}:22'.format(ljuska_port), 'tcp:{}:5900'.format(화면포트)], host_adresa='127.0.0.5') as most_VALUE:
            실행인수 = komanda()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    podaci = Proces_VALUE.stdout.read(4096)
                    if not podaci: break
                    LOG_snimi.extend(podaci)
            nit_VALUE = threading.Thread(target=수집, daemon=True)
            nit_VALUE.start()
            def stanje_čekanja(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_snimi[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_snimi[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stanje_čekanja(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def bezbedan_ljuska(lozinka_VALUE, 명령어, dodati_stavka=()):
                환경['JKOROS_TEST_PASSWORD']=lozinka_VALUE
                인수=['ssh','-v']+list(dodati_stavka)+['-p',str(ljuska_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                KR=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return KR
            KR=bezbedan_ljuska('!' + Postavke['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_snimi, KR.stderr
            izveštaj_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=bezbedan_ljuska(Postavke['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(KR.stderr)
            (출력/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            izveštaj_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            izveštaj_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=bezbedan_ljuska(Postavke['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert KR.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            izveštaj_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=bezbedan_ljuska(Postavke['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            izveštaj_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=bezbedan_ljuska(Postavke['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class 창예제'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            izveštaj_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ljuska_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            transkript=bytearray();izbor_VALUE=selectors.DefaultSelector();izbor_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(emisija_VALUE):
                krajnji_rok_VALUE=time.monotonic()+30
                while emisija_VALUE not in transkript:
                    if time.monotonic()>krajnji_rok_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(emisija_VALUE)+' '+repr(bytes(transkript)))
                    for stavka_VALUE,_ in izbor_VALUE.select(.1):
                        조각=stavka_VALUE.fileobj.read(4096)
                        if 조각:transkript.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,greška=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in greška,(대화.returncode,greška)
                (출력/'ssh-interactive.txt').write_bytes(transkript+나머지)
            finally:
                izbor_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            izveštaj_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(veze, 수):
                podaci=bytearray()
                while len(podaci)<수:
                    odlomak_VALUE=veze.recv(수-len(podaci))
                    if not odlomak_VALUE: raise AssertionError('RFB EOF')
                    podaci.extend(odlomak_VALUE)
                return bytes(podaci)
            def 화면인증(lozinka_VALUE):
                veze=socket.create_connection(('127.0.0.5',화면포트),10);veze.settimeout(30)
                assert 정확히(veze,12)==b'RFB 003.008\n'
                veze.sendall(b'RFB 003.008\n');assert 정확히(veze,2)==b'\x01\x02'
                veze.sendall(b'\x02');izazov_VALUE=정확히(veze,16)
                입력암호=lozinka_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                veze.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(izazov_VALUE))
                Status_VALUE=struct.unpack('!I',정확히(veze,4))[0]
                return veze,Status_VALUE
            nevažeći_lozinka='!' if not Postavke['vnc_password'].startswith('!') else '?'
            veze,Status_VALUE=화면인증(nevažeći_lozinka);assert Status_VALUE==1;veze.close();time.sleep(.6)
            izveštaj_VALUE['checks'].append('VNC incorrect password rejected')
            veze,Status_VALUE=화면인증(Postavke['vnc_password']);assert Status_VALUE==0
            with veze:
                veze.sendall(b'\x01');početno_stanje=정확히(veze,24);너비,높이=struct.unpack('!HH',početno_stanje[:4]);ime=정확히(veze,struct.unpack('!I',početno_stanje[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ime
                def 화면(증분=0):
                    veze.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(veze,4);수=struct.unpack('!H',머리[2:])[0];ukupan_VALUE=0
                    crtež_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinata,세로좌표,영역너비,영역높이,metod_MODE=struct.unpack('!HHHHi',정확히(veze,12));assert metod_MODE==0 and x_koordinata+영역너비<=너비 and 세로좌표+영역높이<=높이
                        piksel=정확히(veze,영역너비*영역높이*4);ukupan_VALUE+=len(piksel)
                        for red in range(영역높이):crtež_VALUE[((세로좌표+red)*너비+x_koordinata)*4:((세로좌표+red)*너비+x_koordinata+영역너비)*4]=piksel[red*영역너비*4:(red+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(crtež_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,ukupan_VALUE
                수,ukupan_VALUE=화면();assert 수>0 and ukupan_VALUE==너비*높이*4
                izveštaj_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(ukupan_VALUE))
                수,ukupan_VALUE=화면(1);assert ukupan_VALUE<너비*높이*4
                izveštaj_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_snimi)
                for znak_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if znak_VALUE=='\r' else ord(znak_VALUE)
                    veze.sendall(struct.pack('!BBHI',4,1,0,simbol));veze.sendall(struct.pack('!BBHI',4,0,0,simbol))
                stanje_čekanja(b'VNC_NATIVE_PASS',처음)
                izveštaj_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ključ_potez_mastilom(simbol,pritisnuti_VALUE=1):veze.sendall(struct.pack('!BBHI',4,pritisnuti_VALUE,0,simbol))
                처음=len(LOG_snimi)
                for znak_VALUE in 'echo ':Ključ_potez_mastilom(ord(znak_VALUE))
                Ključ_potez_mastilom(0xffc6)
                for znak_VALUE in 'gksrmf':Ključ_potez_mastilom(ord(znak_VALUE))
                Ključ_potez_mastilom(0xffc6);Ključ_potez_mastilom(0xff0d)
                stanje_čekanja('\r\n한글\r\n'.encode(),처음)
                izveštaj_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                veze.sendall(struct.pack('!BBHH',5,0,120,100))
                izveštaj_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            izveštaj_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_snimi)
        (출력/'report.json').write_text(json.dumps(izveštaj_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(izveštaj_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': koristiti()
