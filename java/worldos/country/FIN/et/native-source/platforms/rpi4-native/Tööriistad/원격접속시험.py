#!/usr/bin/env python3
"""tegelik_andmed OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Täida_käsk import Project_juur, Käsk
from sild_3de4fe3a import sild_3de4fe3a


def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_juur / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_juur / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_juur / 'build/verification/native-remote')
    Argumendid = parser_48ee4b1b.parse_args()
    Väljund = Argumendid.output
    Väljund.mkdir(parents=True, exist_ok=True)
    Seaded = json.loads(Argumendid.access.read_text())
    aruanne_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumendid.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Ühendu:
            Ühendu.bind(('127.0.0.5', 0))
            return Ühendu.getsockname()[1]
    kest_port, 화면포트, Fail_port = 빈포트(), 빈포트(), 빈포트()
    LOG_kirje = bytearray()
    Joonis_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, sild_3de4fe3a(Fail_port,
                ['tcp:{}:22'.format(kest_port), 'tcp:{}:5900'.format(화면포트)], host_ADDRESS='127.0.0.5') as sild_VALUE:
            실행인수 = Käsk()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumendid.kernel.resolve())
            Joonis_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + sild_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    andmed = Joonis_VALUE.stdout.read(4096)
                    if not andmed: break
                    LOG_kirje.extend(andmed)
            lõim_VALUE = threading.Thread(target=수집, daemon=True)
            lõim_VALUE.start()
            def ooteolek(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_kirje[처음:]:
                    if time.monotonic()>끝 or Joonis_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_kirje[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ooteolek(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def turvaline_kest(parool_VALUE, 명령어, Lisa_kirje=()):
                환경['JKOROS_TEST_PASSWORD']=parool_VALUE
                Argumendid=['ssh','-v']+list(Lisa_kirje)+['-p',str(kest_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                TULEMUS=subprocess.run(Argumendid,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return TULEMUS
            TULEMUS=turvaline_kest('!' + Seaded['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Väljund/'ssh-rejected.log').write_bytes(TULEMUS.stderr)
            assert TULEMUS.returncode!=0 and b'Permission denied' in TULEMUS.stderr and b'SHOULD_NOT_RUN' not in LOG_kirje, TULEMUS.stderr
            aruanne_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            TULEMUS=turvaline_kest(Seaded['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Väljund/'ssh.log').write_bytes(TULEMUS.stderr)
            (Väljund/'ssh-output.txt').write_bytes(TULEMUS.stdout)
            assert TULEMUS.returncode==0 and b'SSH_NATIVE_PASS' in TULEMUS.stdout, (TULEMUS.returncode,TULEMUS.stdout,TULEMUS.stderr)
            aruanne_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in TULEMUS.stderr, TULEMUS.stderr
            aruanne_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            TULEMUS=turvaline_kest(Seaded['ssh_password'], 'cd /example/java; java VäljundiNäide; cd /')
            assert TULEMUS.returncode==0 and 'JAVA Väljund: 안녕하세요 😀'.encode() in TULEMUS.stdout,TULEMUS.stdout
            aruanne_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            TULEMUS=turvaline_kest(Seaded['ssh_password'], 'missing_remote_command')
            assert TULEMUS.returncode==127,TULEMUS.returncode
            aruanne_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            TULEMUS=turvaline_kest(Seaded['ssh_password'], 'cat /example/java/AknaNäide.java', ('-o', 'RekeyLimit=1K'))
            (Väljund/'ssh-rekey.log').write_bytes(TULEMUS.stderr)
            assert TULEMUS.returncode==0 and 'class AknaNäide'.encode() in TULEMUS.stdout, (TULEMUS.returncode,TULEMUS.stdout,TULEMUS.stderr)
            assert TULEMUS.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, TULEMUS.stderr
            aruanne_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(kest_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            transkriptsioon=bytearray();valim_VALUE=selectors.DefaultSelector();valim_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(saade_VALUE):
                tähtaeg_VALUE=time.monotonic()+30
                while saade_VALUE not in transkriptsioon:
                    if time.monotonic()>tähtaeg_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(saade_VALUE)+' '+repr(bytes(transkriptsioon)))
                    for kirje_VALUE,_ in valim_VALUE.select(.1):
                        조각=kirje_VALUE.fileobj.read(4096)
                        if 조각:transkriptsioon.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,VIGA=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in VIGA,(대화.returncode,VIGA)
                (Väljund/'ssh-interactive.txt').write_bytes(transkriptsioon+나머지)
            finally:
                valim_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            aruanne_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Ühendu, number):
                andmed=bytearray()
                while len(andmed)<number:
                    kogum_VALUE=Ühendu.recv(number-len(andmed))
                    if not kogum_VALUE: raise AssertionError('RFB EOF')
                    andmed.extend(kogum_VALUE)
                return bytes(andmed)
            def 화면인증(parool_VALUE):
                Ühendu=socket.create_connection(('127.0.0.5',화면포트),10);Ühendu.settimeout(30)
                assert 정확히(Ühendu,12)==b'RFB 003.008\n'
                Ühendu.sendall(b'RFB 003.008\n');assert 정확히(Ühendu,2)==b'\x01\x02'
                Ühendu.sendall(b'\x02');küsimus_VALUE=정확히(Ühendu,16)
                입력암호=parool_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(number)[::-1],2) for number in 입력암호)
                Ühendu.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(küsimus_VALUE))
                Olek_VALUE=struct.unpack('!I',정확히(Ühendu,4))[0]
                return Ühendu,Olek_VALUE
            kehtetu_parool='!' if not Seaded['vnc_password'].startswith('!') else '?'
            Ühendu,Olek_VALUE=화면인증(kehtetu_parool);assert Olek_VALUE==1;Ühendu.close();time.sleep(.6)
            aruanne_VALUE['checks'].append('VNC incorrect password rejected')
            Ühendu,Olek_VALUE=화면인증(Seaded['vnc_password']);assert Olek_VALUE==0
            with Ühendu:
                Ühendu.sendall(b'\x01');lähteolek=정확히(Ühendu,24);너비,높이=struct.unpack('!HH',lähteolek[:4]);Nimi_2=정확히(Ühendu,struct.unpack('!I',lähteolek[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nimi_2
                def 화면(samm_samm=0):
                    Ühendu.sendall(struct.pack('!BBHHHH',3,samm_samm,0,0,너비,높이));머리=정확히(Ühendu,4);number=struct.unpack('!H',머리[2:])[0];kokku_VALUE=0
                    joonis_VALUE=bytearray(너비*높이*4)
                    for _ in range(number):
                        가로좌표,세로좌표,영역너비,영역높이,meetod_MODE=struct.unpack('!HHHHi',정확히(Ühendu,12));assert meetod_MODE==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        piksel=정확히(Ühendu,영역너비*영역높이*4);kokku_VALUE+=len(piksel)
                        for Joon in range(영역높이):joonis_VALUE[((세로좌표+Joon)*너비+가로좌표)*4:((세로좌표+Joon)*너비+가로좌표+영역너비)*4]=piksel[Joon*영역너비*4:(Joon+1)*영역너비*4]
                    if not samm_samm:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(joonis_VALUE),'raw','BGRX').save(str(Väljund/'native-vnc.png'))
                    return number,kokku_VALUE
                number,kokku_VALUE=화면();assert number>0 and kokku_VALUE==너비*높이*4
                aruanne_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(kokku_VALUE))
                number,kokku_VALUE=화면(1);assert kokku_VALUE<너비*높이*4
                aruanne_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_kirje)
                for märk_VALUE in 'echo VNC_NATIVE_PASS\r':
                    sümbol=0xff0d if märk_VALUE=='\r' else ord(märk_VALUE)
                    Ühendu.sendall(struct.pack('!BBHI',4,1,0,sümbol));Ühendu.sendall(struct.pack('!BBHI',4,0,0,sümbol))
                ooteolek(b'VNC_NATIVE_PASS',처음)
                aruanne_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Võti_tinditõmme(sümbol,vajutama_VALUE=1):Ühendu.sendall(struct.pack('!BBHI',4,vajutama_VALUE,0,sümbol))
                처음=len(LOG_kirje)
                for märk_VALUE in 'echo ':Võti_tinditõmme(ord(märk_VALUE))
                Võti_tinditõmme(0xffc6)
                for märk_VALUE in 'gksrmf':Võti_tinditõmme(ord(märk_VALUE))
                Võti_tinditõmme(0xffc6);Võti_tinditõmme(0xff0d)
                ooteolek('\r\n한글\r\n'.encode(),처음)
                aruanne_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Ühendu.sendall(struct.pack('!BBHH',5,0,120,100))
                aruanne_VALUE['checks'].append('VNC pointer input accepted')
            Joonis_VALUE.stdin.write(b'poweroff\n');Joonis_VALUE.stdin.flush();Joonis_VALUE.wait(timeout=15);assert Joonis_VALUE.returncode==0
            aruanne_VALUE['passed']=True
    finally:
        if Joonis_VALUE and Joonis_VALUE.poll() is None:
            Joonis_VALUE.terminate()
            try: Joonis_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Joonis_VALUE.kill();Joonis_VALUE.wait()
        (Väljund/'serial.log').write_bytes(LOG_kirje)
        (Väljund/'report.json').write_text(json.dumps(aruanne_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(aruanne_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Käivita_2()
