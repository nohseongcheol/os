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
from Izvrši_naredba import akcija_korijen, Naredba
from most_3de4fe3a import most_3de4fe3a


def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--kernel', type=Path, default=akcija_korijen / 'build/kernel8.img')
    analizator_48ee4b1b.add_argument('--access', type=Path, default=akcija_korijen / 'build/remote/access.json')
    analizator_48ee4b1b.add_argument('--output', type=Path, default=akcija_korijen / 'build/verification/native-remote')
    Argumenti = analizator_48ee4b1b.parse_args()
    Izlaz = Argumenti.output
    Izlaz.mkdir(parents=True, exist_ok=True)
    Postavke = json.loads(Argumenti.access.read_text())
    izvješće_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenti.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Spoji_se:
            Spoji_se.bind(('127.0.0.5', 0))
            return Spoji_se.getsockname()[1]
    ljuska_prebaciti, 화면포트, Datoteka_prebaciti = 빈포트(), 빈포트(), 빈포트()
    LOG_zapis = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, most_3de4fe3a(Datoteka_prebaciti,
                ['tcp:{}:22'.format(ljuska_prebaciti), 'tcp:{}:5900'.format(화면포트)], domaćin_adresa='127.0.0.5') as most_VALUE:
            실행인수 = Naredba()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenti.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    podaci = Proces_VALUE.stdout.read(4096)
                    if not podaci: break
                    LOG_zapis.extend(podaci)
            nit_VALUE = threading.Thread(target=수집, daemon=True)
            nit_VALUE.start()
            def stanje_čekanja(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_zapis[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_zapis[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stanje_čekanja(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            okruženje = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def sigurno_ljuska(lozinka_VALUE, 명령어, dodati_unos=()):
                okruženje['JKOROS_TEST_PASSWORD']=lozinka_VALUE
                Argumenti=['ssh','-v']+list(dodati_unos)+['-p',str(ljuska_prebaciti),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                REZULTAT=subprocess.run(Argumenti,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=okruženje,start_new_session=True,timeout=50)
                return REZULTAT
            REZULTAT=sigurno_ljuska('!' + Postavke['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Izlaz/'ssh-rejected.log').write_bytes(REZULTAT.stderr)
            assert REZULTAT.returncode!=0 and b'Permission denied' in REZULTAT.stderr and b'SHOULD_NOT_RUN' not in LOG_zapis, REZULTAT.stderr
            izvješće_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            REZULTAT=sigurno_ljuska(Postavke['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Izlaz/'ssh.log').write_bytes(REZULTAT.stderr)
            (Izlaz/'ssh-output.txt').write_bytes(REZULTAT.stdout)
            assert REZULTAT.returncode==0 and b'SSH_NATIVE_PASS' in REZULTAT.stdout, (REZULTAT.returncode,REZULTAT.stdout,REZULTAT.stderr)
            izvješće_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in REZULTAT.stderr, REZULTAT.stderr
            izvješće_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            REZULTAT=sigurno_ljuska(Postavke['ssh_password'], 'cd /example/java; java PrimjerIspisa; cd /')
            assert REZULTAT.returncode==0 and 'JAVA Izlaz: 안녕하세요 😀'.encode() in REZULTAT.stdout,REZULTAT.stdout
            izvješće_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            REZULTAT=sigurno_ljuska(Postavke['ssh_password'], 'missing_remote_command')
            assert REZULTAT.returncode==127,REZULTAT.returncode
            izvješće_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            REZULTAT=sigurno_ljuska(Postavke['ssh_password'], 'cat /example/java/PrimjerProzora.java', ('-o', 'RekeyLimit=1K'))
            (Izlaz/'ssh-rekey.log').write_bytes(REZULTAT.stderr)
            assert REZULTAT.returncode==0 and 'class PrimjerProzora'.encode() in REZULTAT.stdout, (REZULTAT.returncode,REZULTAT.stdout,REZULTAT.stderr)
            assert REZULTAT.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, REZULTAT.stderr
            izvješće_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ljuska_prebaciti),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=okruženje,start_new_session=True,bufsize=0)
            transkript=bytearray();odabir_VALUE=selectors.DefaultSelector();odabir_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(emisija_VALUE):
                rok_za_dovršetak_VALUE=time.monotonic()+30
                while emisija_VALUE not in transkript:
                    if time.monotonic()>rok_za_dovršetak_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(emisija_VALUE)+' '+repr(bytes(transkript)))
                    for unos_VALUE,_ in odabir_VALUE.select(.1):
                        fragment_VALUE=unos_VALUE.fileobj.read(4096)
                        if fragment_VALUE:transkript.extend(fragment_VALUE)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,GREŠKA=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in GREŠKA,(대화.returncode,GREŠKA)
                (Izlaz/'ssh-interactive.txt').write_bytes(transkript+나머지)
            finally:
                odabir_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            izvješće_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Spoji_se, 수):
                podaci=bytearray()
                while len(podaci)<수:
                    blok_VALUE=Spoji_se.recv(수-len(podaci))
                    if not blok_VALUE: raise AssertionError('RFB EOF')
                    podaci.extend(blok_VALUE)
                return bytes(podaci)
            def 화면인증(lozinka_VALUE):
                Spoji_se=socket.create_connection(('127.0.0.5',화면포트),10);Spoji_se.settimeout(30)
                assert 정확히(Spoji_se,12)==b'RFB 003.008\n'
                Spoji_se.sendall(b'RFB 003.008\n');assert 정확히(Spoji_se,2)==b'\x01\x02'
                Spoji_se.sendall(b'\x02');test_VALUE=정확히(Spoji_se,16)
                입력암호=lozinka_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Spoji_se.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(test_VALUE))
                Stanje_VALUE=struct.unpack('!I',정확히(Spoji_se,4))[0]
                return Spoji_se,Stanje_VALUE
            nevaljan_lozinka='!' if not Postavke['vnc_password'].startswith('!') else '?'
            Spoji_se,Stanje_VALUE=화면인증(nevaljan_lozinka);assert Stanje_VALUE==1;Spoji_se.close();time.sleep(.6)
            izvješće_VALUE['checks'].append('VNC incorrect password rejected')
            Spoji_se,Stanje_VALUE=화면인증(Postavke['vnc_password']);assert Stanje_VALUE==0
            with Spoji_se:
                Spoji_se.sendall(b'\x01');početno_stanje=정확히(Spoji_se,24);너비,높이=struct.unpack('!HH',početno_stanje[:4]);Ime=정확히(Spoji_se,struct.unpack('!I',početno_stanje[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ime
                def 화면(inkrement_korak=0):
                    Spoji_se.sendall(struct.pack('!BBHHHH',3,inkrement_korak,0,0,너비,높이));머리=정확히(Spoji_se,4);수=struct.unpack('!H',머리[2:])[0];ukupni_zbroj_VALUE=0
                    crtež_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        koordinata_x,세로좌표,영역너비,영역높이,postupak_MODE=struct.unpack('!HHHHi',정확히(Spoji_se,12));assert postupak_MODE==0 and koordinata_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        slikovni_element=정확히(Spoji_se,영역너비*영역높이*4);ukupni_zbroj_VALUE+=len(slikovni_element)
                        for red in range(영역높이):crtež_VALUE[((세로좌표+red)*너비+koordinata_x)*4:((세로좌표+red)*너비+koordinata_x+영역너비)*4]=slikovni_element[red*영역너비*4:(red+1)*영역너비*4]
                    if not inkrement_korak:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(crtež_VALUE),'raw','BGRX').save(str(Izlaz/'native-vnc.png'))
                    return 수,ukupni_zbroj_VALUE
                수,ukupni_zbroj_VALUE=화면();assert 수>0 and ukupni_zbroj_VALUE==너비*높이*4
                izvješće_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(ukupni_zbroj_VALUE))
                수,ukupni_zbroj_VALUE=화면(1);assert ukupni_zbroj_VALUE<너비*높이*4
                izvješće_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_zapis)
                for znak_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if znak_VALUE=='\r' else ord(znak_VALUE)
                    Spoji_se.sendall(struct.pack('!BBHI',4,1,0,simbol));Spoji_se.sendall(struct.pack('!BBHI',4,0,0,simbol))
                stanje_čekanja(b'VNC_NATIVE_PASS',처음)
                izvješće_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ključ_rukopisni_potez(simbol,pritisnuti_VALUE=1):Spoji_se.sendall(struct.pack('!BBHI',4,pritisnuti_VALUE,0,simbol))
                처음=len(LOG_zapis)
                for znak_VALUE in 'echo ':Ključ_rukopisni_potez(ord(znak_VALUE))
                Ključ_rukopisni_potez(0xffc6)
                for znak_VALUE in 'gksrmf':Ključ_rukopisni_potez(ord(znak_VALUE))
                Ključ_rukopisni_potez(0xffc6);Ključ_rukopisni_potez(0xff0d)
                stanje_čekanja('\r\n한글\r\n'.encode(),처음)
                izvješće_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Spoji_se.sendall(struct.pack('!BBHH',5,0,120,100))
                izvješće_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            izvješće_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (Izlaz/'serial.log').write_bytes(LOG_zapis)
        (Izlaz/'report.json').write_text(json.dumps(izvješće_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(izvješće_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Pokreni()
