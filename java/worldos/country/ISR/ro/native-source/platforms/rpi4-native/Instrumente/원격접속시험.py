#!/usr/bin/env python3
"""real_date OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from executa_comandă import Project_rădăcină, Comandă
from punte_3de4fe3a import punte_3de4fe3a


def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_rădăcină / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_rădăcină / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_rădăcină / 'build/verification/native-remote')
    Argumente = parser_48ee4b1b.parse_args()
    Rezultat = Argumente.output
    Rezultat.mkdir(parents=True, exist_ok=True)
    Setări = json.loads(Argumente.access.read_text())
    raport_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumente.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Conectează:
            Conectează.bind(('127.0.0.5', 0))
            return Conectează.getsockname()[1]
    shell_muta, 화면포트, Fișier_muta = 빈포트(), 빈포트(), 빈포트()
    LOG_RECORD = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, punte_3de4fe3a(Fișier_muta,
                ['tcp:{}:22'.format(shell_muta), 'tcp:{}:5900'.format(화면포트)], gazdă_adresa='127.0.0.5') as punte_VALUE:
            실행인수 = Comandă()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumente.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + punte_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    date = Proces_VALUE.stdout.read(4096)
                    if not date: break
                    LOG_RECORD.extend(date)
            fir_VALUE = threading.Thread(target=수집, daemon=True)
            fir_VALUE.start()
            def stare_de_așteptare(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stare_de_așteptare(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def securizat_shell(parolă_VALUE, 명령어, adăuga_intrare=()):
                환경['JKOROS_TEST_PASSWORD']=parolă_VALUE
                Argumente=['ssh','-v']+list(adăuga_intrare)+['-p',str(shell_muta),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                KR=subprocess.run(Argumente,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return KR
            KR=securizat_shell('!' + Setări['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Rezultat/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, KR.stderr
            raport_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=securizat_shell(Setări['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Rezultat/'ssh.log').write_bytes(KR.stderr)
            (Rezultat/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            raport_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            raport_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=securizat_shell(Setări['ssh_password'], 'cd /example/java; java ExempluIeșire; cd /')
            assert KR.returncode==0 and 'JAVA Rezultat: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            raport_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=securizat_shell(Setări['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            raport_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=securizat_shell(Setări['ssh_password'], 'cat /example/java/ExempluFereastră.java', ('-o', 'RekeyLimit=1K'))
            (Rezultat/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class ExempluFereastră'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            raport_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_muta),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            transcriere=bytearray();selecție_VALUE=selectors.DefaultSelector();selecție_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(afișa_VALUE):
                dată_limită_VALUE=time.monotonic()+30
                while afișa_VALUE not in transcriere:
                    if time.monotonic()>dată_limită_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(afișa_VALUE)+' '+repr(bytes(transcriere)))
                    for intrare_VALUE,_ in selecție_VALUE.select(.1):
                        조각=intrare_VALUE.fileobj.read(4096)
                        if 조각:transcriere.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,eroare=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in eroare,(대화.returncode,eroare)
                (Rezultat/'ssh-interactive.txt').write_bytes(transcriere+나머지)
            finally:
                selecție_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            raport_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Conectează, 수):
                date=bytearray()
                while len(date)<수:
                    bloc_VALUE=Conectează.recv(수-len(date))
                    if not bloc_VALUE: raise AssertionError('RFB EOF')
                    date.extend(bloc_VALUE)
                return bytes(date)
            def 화면인증(parolă_VALUE):
                Conectează=socket.create_connection(('127.0.0.5',화면포트),10);Conectează.settimeout(30)
                assert 정확히(Conectează,12)==b'RFB 003.008\n'
                Conectează.sendall(b'RFB 003.008\n');assert 정확히(Conectează,2)==b'\x01\x02'
                Conectează.sendall(b'\x02');verificare_VALUE=정확히(Conectează,16)
                입력암호=parolă_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Conectează.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(verificare_VALUE))
                Stare_VALUE=struct.unpack('!I',정확히(Conectează,4))[0]
                return Conectează,Stare_VALUE
            nul_parolă='!' if not Setări['vnc_password'].startswith('!') else '?'
            Conectează,Stare_VALUE=화면인증(nul_parolă);assert Stare_VALUE==1;Conectează.close();time.sleep(.6)
            raport_VALUE['checks'].append('VNC incorrect password rejected')
            Conectează,Stare_VALUE=화면인증(Setări['vnc_password']);assert Stare_VALUE==0
            with Conectează:
                Conectează.sendall(b'\x01');stare_inițială=정확히(Conectează,24);너비,높이=struct.unpack('!HH',stare_inițială[:4]);Nume=정확히(Conectează,struct.unpack('!I',stare_inițială[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nume
                def 화면(increment_pas=0):
                    Conectează.sendall(struct.pack('!BBHHHH',3,increment_pas,0,0,너비,높이));머리=정확히(Conectează,4);수=struct.unpack('!H',머리[2:])[0];total_VALUE=0
                    desen_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        coordonata_X,세로좌표,영역너비,영역높이,metodă_mod=struct.unpack('!HHHHi',정확히(Conectează,12));assert metodă_mod==0 and coordonata_X+영역너비<=너비 and 세로좌표+영역높이<=높이
                        element_imagine=정확히(Conectează,영역너비*영역높이*4);total_VALUE+=len(element_imagine)
                        for Linie in range(영역높이):desen_VALUE[((세로좌표+Linie)*너비+coordonata_X)*4:((세로좌표+Linie)*너비+coordonata_X+영역너비)*4]=element_imagine[Linie*영역너비*4:(Linie+1)*영역너비*4]
                    if not increment_pas:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(desen_VALUE),'raw','BGRX').save(str(Rezultat/'native-vnc.png'))
                    return 수,total_VALUE
                수,total_VALUE=화면();assert 수>0 and total_VALUE==너비*높이*4
                raport_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(total_VALUE))
                수,total_VALUE=화면(1);assert total_VALUE<너비*높이*4
                raport_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for caracter_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if caracter_VALUE=='\r' else ord(caracter_VALUE)
                    Conectează.sendall(struct.pack('!BBHI',4,1,0,simbol));Conectează.sendall(struct.pack('!BBHI',4,0,0,simbol))
                stare_de_așteptare(b'VNC_NATIVE_PASS',처음)
                raport_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Cheie_Urmă_de_cerneală(simbol,apăsa_VALUE=1):Conectează.sendall(struct.pack('!BBHI',4,apăsa_VALUE,0,simbol))
                처음=len(LOG_RECORD)
                for caracter_VALUE in 'echo ':Cheie_Urmă_de_cerneală(ord(caracter_VALUE))
                Cheie_Urmă_de_cerneală(0xffc6)
                for caracter_VALUE in 'gksrmf':Cheie_Urmă_de_cerneală(ord(caracter_VALUE))
                Cheie_Urmă_de_cerneală(0xffc6);Cheie_Urmă_de_cerneală(0xff0d)
                stare_de_așteptare('\r\n한글\r\n'.encode(),처음)
                raport_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Conectează.sendall(struct.pack('!BBHH',5,0,120,100))
                raport_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            raport_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (Rezultat/'serial.log').write_bytes(LOG_RECORD)
        (Rezultat/'report.json').write_text(json.dumps(raport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(raport_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Pornește()
