#!/usr/bin/env python3
"""faktinis_duomenys OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Vykdyti_komanda import Project_šaknis, Komanda
from tiltas_3de4fe3a import tiltas_3de4fe3a


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--kernel', type=Path, default=Project_šaknis / 'build/kernel8.img')
    analizatorius_48ee4b1b.add_argument('--access', type=Path, default=Project_šaknis / 'build/remote/access.json')
    analizatorius_48ee4b1b.add_argument('--output', type=Path, default=Project_šaknis / 'build/verification/native-remote')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    Išvestis = Argumentai.output
    Išvestis.mkdir(parents=True, exist_ok=True)
    Nustatymai = json.loads(Argumentai.access.read_text())
    pranešti_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumentai.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Prisijungti:
            Prisijungti.bind(('127.0.0.5', 0))
            return Prisijungti.getsockname()[1]
    apvalkalas_jungtis, 화면포트, Failas_jungtis = 빈포트(), 빈포트(), 빈포트()
    LOG_RECORD = bytearray()
    Procesas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, tiltas_3de4fe3a(Failas_jungtis,
                ['tcp:{}:22'.format(apvalkalas_jungtis), 'tcp:{}:5900'.format(화면포트)], organizuoti_ADDRESS='127.0.0.5') as tiltas_VALUE:
            실행인수 = Komanda()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumentai.kernel.resolve())
            Procesas_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + tiltas_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    duomenys = Procesas_VALUE.stdout.read(4096)
                    if not duomenys: break
                    LOG_RECORD.extend(duomenys)
            gija_VALUE = threading.Thread(target=수집, daemon=True)
            gija_VALUE.start()
            def laukimo_būsena(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Procesas_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            laukimo_būsena(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def saugus_apvalkalas(slaptažodis_VALUE, 명령어, sujungti_įrašas=()):
                환경['JKOROS_TEST_PASSWORD']=slaptažodis_VALUE
                Argumentai=['ssh','-v']+list(sujungti_įrašas)+['-p',str(apvalkalas_jungtis),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                REZULTATAS=subprocess.run(Argumentai,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return REZULTATAS
            REZULTATAS=saugus_apvalkalas('!' + Nustatymai['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Išvestis/'ssh-rejected.log').write_bytes(REZULTATAS.stderr)
            assert REZULTATAS.returncode!=0 and b'Permission denied' in REZULTATAS.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, REZULTATAS.stderr
            pranešti_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            REZULTATAS=saugus_apvalkalas(Nustatymai['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Išvestis/'ssh.log').write_bytes(REZULTATAS.stderr)
            (Išvestis/'ssh-output.txt').write_bytes(REZULTATAS.stdout)
            assert REZULTATAS.returncode==0 and b'SSH_NATIVE_PASS' in REZULTATAS.stdout, (REZULTATAS.returncode,REZULTATAS.stdout,REZULTATAS.stderr)
            pranešti_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in REZULTATAS.stderr, REZULTATAS.stderr
            pranešti_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            REZULTATAS=saugus_apvalkalas(Nustatymai['ssh_password'], 'cd /example/java; java IšvestiesPavyzdys; cd /')
            assert REZULTATAS.returncode==0 and 'JAVA Išvestis: 안녕하세요 😀'.encode() in REZULTATAS.stdout,REZULTATAS.stdout
            pranešti_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            REZULTATAS=saugus_apvalkalas(Nustatymai['ssh_password'], 'missing_remote_command')
            assert REZULTATAS.returncode==127,REZULTATAS.returncode
            pranešti_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            REZULTATAS=saugus_apvalkalas(Nustatymai['ssh_password'], 'cat /example/java/LangoPavyzdys.java', ('-o', 'RekeyLimit=1K'))
            (Išvestis/'ssh-rekey.log').write_bytes(REZULTATAS.stderr)
            assert REZULTATAS.returncode==0 and 'class LangoPavyzdys'.encode() in REZULTATAS.stdout, (REZULTATAS.returncode,REZULTATAS.stdout,REZULTATAS.stderr)
            assert REZULTATAS.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, REZULTATAS.stderr
            pranešti_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(apvalkalas_jungtis),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            transkribavimas=bytearray();žymėjimas_VALUE=selectors.DefaultSelector();žymėjimas_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(laida_VALUE):
                terminas_VALUE=time.monotonic()+30
                while laida_VALUE not in transkribavimas:
                    if time.monotonic()>terminas_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(laida_VALUE)+' '+repr(bytes(transkribavimas)))
                    for įrašas_VALUE,_ in žymėjimas_VALUE.select(.1):
                        조각=įrašas_VALUE.fileobj.read(4096)
                        if 조각:transkribavimas.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,KLAIDA=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in KLAIDA,(대화.returncode,KLAIDA)
                (Išvestis/'ssh-interactive.txt').write_bytes(transkribavimas+나머지)
            finally:
                žymėjimas_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            pranešti_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Prisijungti, numeris):
                duomenys=bytearray()
                while len(duomenys)<numeris:
                    segmentas_VALUE=Prisijungti.recv(numeris-len(duomenys))
                    if not segmentas_VALUE: raise AssertionError('RFB EOF')
                    duomenys.extend(segmentas_VALUE)
                return bytes(duomenys)
            def 화면인증(slaptažodis_VALUE):
                Prisijungti=socket.create_connection(('127.0.0.5',화면포트),10);Prisijungti.settimeout(30)
                assert 정확히(Prisijungti,12)==b'RFB 003.008\n'
                Prisijungti.sendall(b'RFB 003.008\n');assert 정확히(Prisijungti,2)==b'\x01\x02'
                Prisijungti.sendall(b'\x02');iššūkis_VALUE=정확히(Prisijungti,16)
                입력암호=slaptažodis_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(numeris)[::-1],2) for numeris in 입력암호)
                Prisijungti.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(iššūkis_VALUE))
                Būsena_VALUE=struct.unpack('!I',정확히(Prisijungti,4))[0]
                return Prisijungti,Būsena_VALUE
            neleistinas_slaptažodis='!' if not Nustatymai['vnc_password'].startswith('!') else '?'
            Prisijungti,Būsena_VALUE=화면인증(neleistinas_slaptažodis);assert Būsena_VALUE==1;Prisijungti.close();time.sleep(.6)
            pranešti_VALUE['checks'].append('VNC incorrect password rejected')
            Prisijungti,Būsena_VALUE=화면인증(Nustatymai['vnc_password']);assert Būsena_VALUE==0
            with Prisijungti:
                Prisijungti.sendall(b'\x01');pradinė_būsena=정확히(Prisijungti,24);너비,높이=struct.unpack('!HH',pradinė_būsena[:4]);Pavadinimas_2=정확히(Prisijungti,struct.unpack('!I',pradinė_būsena[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Pavadinimas_2
                def 화면(padidinimas_veiksmas=0):
                    Prisijungti.sendall(struct.pack('!BBHHHH',3,padidinimas_veiksmas,0,0,너비,높이));머리=정확히(Prisijungti,4);numeris=struct.unpack('!H',머리[2:])[0];bendras_VALUE=0
                    piešinys_VALUE=bytearray(너비*높이*4)
                    for _ in range(numeris):
                        x_koordinatė,세로좌표,영역너비,영역높이,metodas_MODE=struct.unpack('!HHHHi',정확히(Prisijungti,12));assert metodas_MODE==0 and x_koordinatė+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pikselis=정확히(Prisijungti,영역너비*영역높이*4);bendras_VALUE+=len(pikselis)
                        for Eilutė in range(영역높이):piešinys_VALUE[((세로좌표+Eilutė)*너비+x_koordinatė)*4:((세로좌표+Eilutė)*너비+x_koordinatė+영역너비)*4]=pikselis[Eilutė*영역너비*4:(Eilutė+1)*영역너비*4]
                    if not padidinimas_veiksmas:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(piešinys_VALUE),'raw','BGRX').save(str(Išvestis/'native-vnc.png'))
                    return numeris,bendras_VALUE
                numeris,bendras_VALUE=화면();assert numeris>0 and bendras_VALUE==너비*높이*4
                pranešti_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(bendras_VALUE))
                numeris,bendras_VALUE=화면(1);assert bendras_VALUE<너비*높이*4
                pranešti_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for simbolis_VALUE_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    simbolis=0xff0d if simbolis_VALUE_068c2631=='\r' else ord(simbolis_VALUE_068c2631)
                    Prisijungti.sendall(struct.pack('!BBHI',4,1,0,simbolis));Prisijungti.sendall(struct.pack('!BBHI',4,0,0,simbolis))
                laukimo_būsena(b'VNC_NATIVE_PASS',처음)
                pranešti_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Raktas_brūkštelėjimas_stiliumi(simbolis,paspausti_VALUE=1):Prisijungti.sendall(struct.pack('!BBHI',4,paspausti_VALUE,0,simbolis))
                처음=len(LOG_RECORD)
                for simbolis_VALUE_068c2631 in 'echo ':Raktas_brūkštelėjimas_stiliumi(ord(simbolis_VALUE_068c2631))
                Raktas_brūkštelėjimas_stiliumi(0xffc6)
                for simbolis_VALUE_068c2631 in 'gksrmf':Raktas_brūkštelėjimas_stiliumi(ord(simbolis_VALUE_068c2631))
                Raktas_brūkštelėjimas_stiliumi(0xffc6);Raktas_brūkštelėjimas_stiliumi(0xff0d)
                laukimo_būsena('\r\n한글\r\n'.encode(),처음)
                pranešti_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Prisijungti.sendall(struct.pack('!BBHH',5,0,120,100))
                pranešti_VALUE['checks'].append('VNC pointer input accepted')
            Procesas_VALUE.stdin.write(b'poweroff\n');Procesas_VALUE.stdin.flush();Procesas_VALUE.wait(timeout=15);assert Procesas_VALUE.returncode==0
            pranešti_VALUE['passed']=True
    finally:
        if Procesas_VALUE and Procesas_VALUE.poll() is None:
            Procesas_VALUE.terminate()
            try: Procesas_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Procesas_VALUE.kill();Procesas_VALUE.wait()
        (Išvestis/'serial.log').write_bytes(LOG_RECORD)
        (Išvestis/'report.json').write_text(json.dumps(pranešti_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pranešti_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Paleisti()
