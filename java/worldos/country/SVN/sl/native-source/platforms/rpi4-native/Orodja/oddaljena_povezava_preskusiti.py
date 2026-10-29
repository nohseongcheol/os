#!/usr/bin/env python3
"""dejanski_podatki OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Izvedi_ukaz import pobuda_koren, Ukaz
from most_3de4fe3a import most_3de4fe3a


def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--kernel', type=Path, default=pobuda_koren / 'build/kernel8.img')
    razčlenjevalnik_48ee4b1b.add_argument('--access', type=Path, default=pobuda_koren / 'build/remote/access.json')
    razčlenjevalnik_48ee4b1b.add_argument('--output', type=Path, default=pobuda_koren / 'build/verification/native-remote')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    Izpis = Argumenti.output
    Izpis.mkdir(parents=True, exist_ok=True)
    Nastavitve = json.loads(Argumenti.access.read_text())
    prijavi_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenti.kernel.read_bytes()).hexdigest(), 'checks': []}
    def prazen_vrata():
        with socket.socket() as Poveži:
            Poveži.bind(('127.0.0.5', 0))
            return Poveži.getsockname()[1]
    lupina_vrata, 화면포트, Datoteka_vrata = prazen_vrata(), prazen_vrata(), prazen_vrata()
    LOG_zapis = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, most_3de4fe3a(Datoteka_vrata,
                ['tcp:{}:22'.format(lupina_vrata), 'tcp:{}:5900'.format(화면포트)], gostiti_naslov='127.0.0.5') as most_VALUE:
            실행인수 = Ukaz()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenti.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    podatki = Proces_VALUE.stdout.read(4096)
                    if not podatki: break
                    LOG_zapis.extend(podatki)
            nit_VALUE = threading.Thread(target=수집, daemon=True)
            nit_VALUE.start()
            def čakalno_stanje(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_zapis[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_zapis[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            čakalno_stanje(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def varen_lupina(geslo_VALUE, navodilo_VALUE, dodati_vnos=()):
                환경['JKOROS_TEST_PASSWORD']=geslo_VALUE
                Argumenti=['ssh','-v']+list(dodati_vnos)+['-p',str(lupina_vrata),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',navodilo_VALUE]
                REZULTAT=subprocess.run(Argumenti,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return REZULTAT
            REZULTAT=varen_lupina('!' + Nastavitve['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Izpis/'ssh-rejected.log').write_bytes(REZULTAT.stderr)
            assert REZULTAT.returncode!=0 and b'Permission denied' in REZULTAT.stderr and b'SHOULD_NOT_RUN' not in LOG_zapis, REZULTAT.stderr
            prijavi_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            REZULTAT=varen_lupina(Nastavitve['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Izpis/'ssh.log').write_bytes(REZULTAT.stderr)
            (Izpis/'ssh-output.txt').write_bytes(REZULTAT.stdout)
            assert REZULTAT.returncode==0 and b'SSH_NATIVE_PASS' in REZULTAT.stdout, (REZULTAT.returncode,REZULTAT.stdout,REZULTAT.stderr)
            prijavi_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in REZULTAT.stderr, REZULTAT.stderr
            prijavi_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            REZULTAT=varen_lupina(Nastavitve['ssh_password'], 'cd /example/java; java PrimerIzpisa; cd /')
            assert REZULTAT.returncode==0 and 'JAVA Izpis: 안녕하세요 😀'.encode() in REZULTAT.stdout,REZULTAT.stdout
            prijavi_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            REZULTAT=varen_lupina(Nastavitve['ssh_password'], 'missing_remote_command')
            assert REZULTAT.returncode==127,REZULTAT.returncode
            prijavi_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            REZULTAT=varen_lupina(Nastavitve['ssh_password'], 'cat /example/java/PrimerOkna.java', ('-o', 'RekeyLimit=1K'))
            (Izpis/'ssh-rekey.log').write_bytes(REZULTAT.stderr)
            assert REZULTAT.returncode==0 and 'class PrimerOkna'.encode() in REZULTAT.stdout, (REZULTAT.returncode,REZULTAT.stdout,REZULTAT.stderr)
            assert REZULTAT.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, REZULTAT.stderr
            prijavi_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(lupina_vrata),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiven_seja=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            prepis=bytearray();izbor_VALUE=selectors.DefaultSelector();izbor_VALUE.register(interaktiven_seja.stdout,selectors.EVENT_READ)
            def 대화읽기(oddaja_VALUE_487749b8):
                rok_VALUE=time.monotonic()+30
                while oddaja_VALUE_487749b8 not in prepis:
                    if time.monotonic()>rok_VALUE or interaktiven_seja.poll() is not None:raise AssertionError('SSH interactive missing '+repr(oddaja_VALUE_487749b8)+' '+repr(bytes(prepis)))
                    for vnos_VALUE,_ in izbor_VALUE.select(.1):
                        조각=vnos_VALUE.fileobj.read(4096)
                        if 조각:prepis.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiven_seja.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiven_seja.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiven_seja.stdin.write(b'\x04');interaktiven_seja.stdin.flush();나머지,NAPAKA=interaktiven_seja.communicate(timeout=15)
                assert interaktiven_seja.returncode==0 and b'PTY allocation request failed' not in NAPAKA,(interaktiven_seja.returncode,NAPAKA)
                (Izpis/'ssh-interactive.txt').write_bytes(prepis+나머지)
            finally:
                izbor_VALUE.close()
                if interaktiven_seja.poll() is None:interaktiven_seja.kill();interaktiven_seja.wait()
            prijavi_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Poveži, 수):
                podatki=bytearray()
                while len(podatki)<수:
                    košček_VALUE=Poveži.recv(수-len(podatki))
                    if not košček_VALUE: raise AssertionError('RFB EOF')
                    podatki.extend(košček_VALUE)
                return bytes(podatki)
            def 화면인증(geslo_VALUE):
                Poveži=socket.create_connection(('127.0.0.5',화면포트),10);Poveži.settimeout(30)
                assert 정확히(Poveži,12)==b'RFB 003.008\n'
                Poveži.sendall(b'RFB 003.008\n');assert 정확히(Poveži,2)==b'\x01\x02'
                Poveži.sendall(b'\x02');izziv_VALUE=정확히(Poveži,16)
                입력암호=geslo_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Poveži.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(izziv_VALUE))
                stanje_VALUE=struct.unpack('!I',정확히(Poveži,4))[0]
                return Poveži,stanje_VALUE
            neveljaven_geslo='!' if not Nastavitve['vnc_password'].startswith('!') else '?'
            Poveži,stanje_VALUE=화면인증(neveljaven_geslo);assert stanje_VALUE==1;Poveži.close();time.sleep(.6)
            prijavi_VALUE['checks'].append('VNC incorrect password rejected')
            Poveži,stanje_VALUE=화면인증(Nastavitve['vnc_password']);assert stanje_VALUE==0
            with Poveži:
                Poveži.sendall(b'\x01');začetno_stanje=정확히(Poveži,24);너비,višina_VALUE=struct.unpack('!HH',začetno_stanje[:4]);Ime=정확히(Poveži,struct.unpack('!I',začetno_stanje[20:24])[0])
                assert (너비,višina_VALUE)==(640,480) and b'jkoros native'==Ime
                def 화면(증분=0):
                    Poveži.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,višina_VALUE));머리=정확히(Poveži,4);수=struct.unpack('!H',머리[2:])[0];skupaj_VALUE=0
                    risba_VALUE=bytearray(너비*višina_VALUE*4)
                    for _ in range(수):
                        koordinata_x,세로좌표,영역너비,območje_višina,metoda_MODE=struct.unpack('!HHHHi',정확히(Poveži,12));assert metoda_MODE==0 and koordinata_x+영역너비<=너비 and 세로좌표+območje_višina<=višina_VALUE
                        slikovna_pika=정확히(Poveži,영역너비*območje_višina*4);skupaj_VALUE+=len(slikovna_pika)
                        for Črtni in range(območje_višina):risba_VALUE[((세로좌표+Črtni)*너비+koordinata_x)*4:((세로좌표+Črtni)*너비+koordinata_x+영역너비)*4]=slikovna_pika[Črtni*영역너비*4:(Črtni+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,višina_VALUE),bytes(risba_VALUE),'raw','BGRX').save(str(Izpis/'native-vnc.png'))
                    return 수,skupaj_VALUE
                수,skupaj_VALUE=화면();assert 수>0 and skupaj_VALUE==너비*višina_VALUE*4
                prijavi_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(skupaj_VALUE))
                수,skupaj_VALUE=화면(1);assert skupaj_VALUE<너비*višina_VALUE*4
                prijavi_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_zapis)
                for znak_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if znak_VALUE=='\r' else ord(znak_VALUE)
                    Poveži.sendall(struct.pack('!BBHI',4,1,0,simbol));Poveži.sendall(struct.pack('!BBHI',4,0,0,simbol))
                čakalno_stanje(b'VNC_NATIVE_PASS',처음)
                prijavi_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ključ_poteza_rokopisa(simbol,pritisniti_VALUE=1):Poveži.sendall(struct.pack('!BBHI',4,pritisniti_VALUE,0,simbol))
                처음=len(LOG_zapis)
                for znak_VALUE in 'echo ':Ključ_poteza_rokopisa(ord(znak_VALUE))
                Ključ_poteza_rokopisa(0xffc6)
                for znak_VALUE in 'gksrmf':Ključ_poteza_rokopisa(ord(znak_VALUE))
                Ključ_poteza_rokopisa(0xffc6);Ključ_poteza_rokopisa(0xff0d)
                čakalno_stanje('\r\n한글\r\n'.encode(),처음)
                prijavi_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Poveži.sendall(struct.pack('!BBHH',5,0,120,100))
                prijavi_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            prijavi_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (Izpis/'serial.log').write_bytes(LOG_zapis)
        (Izpis/'report.json').write_text(json.dumps(prijavi_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(prijavi_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Zaženi()
