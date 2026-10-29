#!/usr/bin/env python3
"""rzeczywisty_dane OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Wykonaj_polecenie import Project_korzeń, polecenie
from mostek_3de4fe3a import mostek_3de4fe3a


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_korzeń / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_korzeń / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_korzeń / 'build/verification/native-remote')
    argumenty = parser_48ee4b1b.parse_args()
    pozycja_wyjścia = argumenty.output
    pozycja_wyjścia.mkdir(parents=True, exist_ok=True)
    Ustawienia = json.loads(argumenty.access.read_text())
    Raport_WARTOŚĆ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumenty.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Połącz:
            Połącz.bind(('127.0.0.5', 0))
            return Połącz.getsockname()[1]
    powłoka_port, 화면포트, port_plików = 빈포트(), 빈포트(), 빈포트()
    LOG_zapis = bytearray()
    Proces_WARTOŚĆ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, mostek_3de4fe3a(port_plików,
                ['tcp:{}:22'.format(powłoka_port), 'tcp:{}:5900'.format(화면포트)], host_ADRES='127.0.0.5') as mostek_WARTOŚĆ:
            실행인수 = polecenie()
            실행인수[실행인수.index('-kernel') + 1] = str(argumenty.kernel.resolve())
            Proces_WARTOŚĆ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + mostek_WARTOŚĆ.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dane = Proces_WARTOŚĆ.stdout.read(4096)
                    if not dane: break
                    LOG_zapis.extend(dane)
            wątek_WARTOŚĆ = threading.Thread(target=수집, daemon=True)
            wątek_WARTOŚĆ.start()
            def stan_oczekiwania(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_zapis[처음:]:
                    if time.monotonic()>끝 or Proces_WARTOŚĆ.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_zapis[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stan_oczekiwania(b'jkoros-native> ')
            pomocnik_WARTOŚĆ = Path(임시)/'askpass'
            pomocnik_WARTOŚĆ.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            pomocnik_WARTOŚĆ.chmod(0o700)
            środowisko = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(pomocnik_WARTOŚĆ), SSH_ASKPASS_REQUIRE='force')
            def SSH(hasło_WARTOŚĆ, instrukcja_WARTOŚĆ, dołączać_wpis=()):
                środowisko['JKOROS_TEST_PASSWORD']=hasło_WARTOŚĆ
                argumenty=['ssh','-v']+list(dołączać_wpis)+['-p',str(powłoka_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instrukcja_WARTOŚĆ]
                WYNIK=subprocess.run(argumenty,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=środowisko,start_new_session=True,timeout=50)
                return WYNIK
            WYNIK=SSH('!' + Ustawienia['ssh_password'], 'echo SHOULD_NOT_RUN')
            (pozycja_wyjścia/'ssh-rejected.log').write_bytes(WYNIK.stderr)
            assert WYNIK.returncode!=0 and b'Permission denied' in WYNIK.stderr and b'SHOULD_NOT_RUN' not in LOG_zapis, WYNIK.stderr
            Raport_WARTOŚĆ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            WYNIK=SSH(Ustawienia['ssh_password'], 'echo SSH_NATIVE_PASS')
            (pozycja_wyjścia/'ssh.log').write_bytes(WYNIK.stderr)
            (pozycja_wyjścia/'ssh-output.txt').write_bytes(WYNIK.stdout)
            assert WYNIK.returncode==0 and b'SSH_NATIVE_PASS' in WYNIK.stdout, (WYNIK.returncode,WYNIK.stdout,WYNIK.stderr)
            Raport_WARTOŚĆ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in WYNIK.stderr, WYNIK.stderr
            Raport_WARTOŚĆ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            WYNIK=SSH(Ustawienia['ssh_password'], 'cd /example/java; java PrzykładWyjścia; cd /')
            assert WYNIK.returncode==0 and 'JAVA pozycja_wyjścia: 안녕하세요 😀'.encode() in WYNIK.stdout,WYNIK.stdout
            Raport_WARTOŚĆ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            WYNIK=SSH(Ustawienia['ssh_password'], 'missing_remote_command')
            assert WYNIK.returncode==127,WYNIK.returncode
            Raport_WARTOŚĆ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            WYNIK=SSH(Ustawienia['ssh_password'], 'cat /example/java/PrzykładOkna.java', ('-o', 'RekeyLimit=1K'))
            (pozycja_wyjścia/'ssh-rekey.log').write_bytes(WYNIK.stderr)
            assert WYNIK.returncode==0 and 'class PrzykładOkna'.encode() in WYNIK.stdout, (WYNIK.returncode,WYNIK.stdout,WYNIK.stderr)
            assert WYNIK.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, WYNIK.stderr
            Raport_WARTOŚĆ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(powłoka_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interakcyjny_sesja=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=środowisko,start_new_session=True,bufsize=0)
            transkrypcja=bytearray();zaznaczenie_WARTOŚĆ=selectors.DefaultSelector();zaznaczenie_WARTOŚĆ.register(interakcyjny_sesja.stdout,selectors.EVENT_READ)
            def 대화읽기(program_WARTOŚĆ):
                termin_ostateczny_WARTOŚĆ=time.monotonic()+30
                while program_WARTOŚĆ not in transkrypcja:
                    if time.monotonic()>termin_ostateczny_WARTOŚĆ or interakcyjny_sesja.poll() is not None:raise AssertionError('SSH interactive missing '+repr(program_WARTOŚĆ)+' '+repr(bytes(transkrypcja)))
                    for wpis_WARTOŚĆ,_ in zaznaczenie_WARTOŚĆ.select(.1):
                        fragment_WARTOŚĆ_652d4b53=wpis_WARTOŚĆ.fileobj.read(4096)
                        if fragment_WARTOŚĆ_652d4b53:transkrypcja.extend(fragment_WARTOŚĆ_652d4b53)
            try:
                대화읽기(b'shared native console')
                interakcyjny_sesja.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interakcyjny_sesja.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interakcyjny_sesja.stdin.write(b'\x04');interakcyjny_sesja.stdin.flush();나머지,błąd=interakcyjny_sesja.communicate(timeout=15)
                assert interakcyjny_sesja.returncode==0 and b'PTY allocation request failed' not in błąd,(interakcyjny_sesja.returncode,błąd)
                (pozycja_wyjścia/'ssh-interactive.txt').write_bytes(transkrypcja+나머지)
            finally:
                zaznaczenie_WARTOŚĆ.close()
                if interakcyjny_sesja.poll() is None:interakcyjny_sesja.kill();interakcyjny_sesja.wait()
            Raport_WARTOŚĆ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Połącz, identyfikator):
                dane=bytearray()
                while len(dane)<identyfikator:
                    fragment_WARTOŚĆ=Połącz.recv(identyfikator-len(dane))
                    if not fragment_WARTOŚĆ: raise AssertionError('RFB EOF')
                    dane.extend(fragment_WARTOŚĆ)
                return bytes(dane)
            def 화면인증(hasło_WARTOŚĆ):
                Połącz=socket.create_connection(('127.0.0.5',화면포트),10);Połącz.settimeout(30)
                assert 정확히(Połącz,12)==b'RFB 003.008\n'
                Połącz.sendall(b'RFB 003.008\n');assert 정확히(Połącz,2)==b'\x01\x02'
                Połącz.sendall(b'\x02');test_WARTOŚĆ=정확히(Połącz,16)
                wejście_hasło=hasło_WARTOŚĆ.encode('ascii')[:8].ljust(8, b'\0')
                Klucz_materiał=bytes(int('{:08b}'.format(identyfikator)[::-1],2) for identyfikator in wejście_hasło)
                Połącz.sendall(DES.new(Klucz_materiał,DES.MODE_ECB).encrypt(test_WARTOŚĆ))
                Stan_WARTOŚĆ=struct.unpack('!I',정확히(Połącz,4))[0]
                return Połącz,Stan_WARTOŚĆ
            nieważny_hasło='!' if not Ustawienia['vnc_password'].startswith('!') else '?'
            Połącz,Stan_WARTOŚĆ=화면인증(nieważny_hasło);assert Stan_WARTOŚĆ==1;Połącz.close();time.sleep(.6)
            Raport_WARTOŚĆ['checks'].append('VNC incorrect password rejected')
            Połącz,Stan_WARTOŚĆ=화면인증(Ustawienia['vnc_password']);assert Stan_WARTOŚĆ==0
            with Połącz:
                Połącz.sendall(b'\x01');stan_początkowy=정확히(Połącz,24);너비,wysokość_WARTOŚĆ=struct.unpack('!HH',stan_początkowy[:4]);Nazwa=정확히(Połącz,struct.unpack('!I',stan_początkowy[20:24])[0])
                assert (너비,wysokość_WARTOŚĆ)==(640,480) and b'jkoros native'==Nazwa
                def 화면(przyrost_krok=0):
                    Połącz.sendall(struct.pack('!BBHHHH',3,przyrost_krok,0,0,너비,wysokość_WARTOŚĆ));머리=정확히(Połącz,4);identyfikator=struct.unpack('!H',머리[2:])[0];suma_WARTOŚĆ=0
                    rysunek_WARTOŚĆ=bytearray(너비*wysokość_WARTOŚĆ*4)
                    for _ in range(identyfikator):
                        współrzędna_X,Y_współrzędna,영역너비,region_wysokość,metoda_tryb=struct.unpack('!HHHHi',정확히(Połącz,12));assert metoda_tryb==0 and współrzędna_X+영역너비<=너비 and Y_współrzędna+region_wysokość<=wysokość_WARTOŚĆ
                        piksel=정확히(Połącz,영역너비*region_wysokość*4);suma_WARTOŚĆ+=len(piksel)
                        for wiersz_wejścia in range(region_wysokość):rysunek_WARTOŚĆ[((Y_współrzędna+wiersz_wejścia)*너비+współrzędna_X)*4:((Y_współrzędna+wiersz_wejścia)*너비+współrzędna_X+영역너비)*4]=piksel[wiersz_wejścia*영역너비*4:(wiersz_wejścia+1)*영역너비*4]
                    if not przyrost_krok:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,wysokość_WARTOŚĆ),bytes(rysunek_WARTOŚĆ),'raw','BGRX').save(str(pozycja_wyjścia/'native-vnc.png'))
                    return identyfikator,suma_WARTOŚĆ
                identyfikator,suma_WARTOŚĆ=화면();assert identyfikator>0 and suma_WARTOŚĆ==너비*wysokość_WARTOŚĆ*4
                Raport_WARTOŚĆ['checks'].append('Native framebuffer RFB full update {} bytes'.format(suma_WARTOŚĆ))
                identyfikator,suma_WARTOŚĆ=화면(1);assert suma_WARTOŚĆ<너비*wysokość_WARTOŚĆ*4
                Raport_WARTOŚĆ['checks'].append('RFB incremental update')
                처음=len(LOG_zapis)
                for znak_WARTOŚĆ in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if znak_WARTOŚĆ=='\r' else ord(znak_WARTOŚĆ)
                    Połącz.sendall(struct.pack('!BBHI',4,1,0,symbol));Połącz.sendall(struct.pack('!BBHI',4,0,0,symbol))
                stan_oczekiwania(b'VNC_NATIVE_PASS',처음)
                Raport_WARTOŚĆ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Klucz_ślad_pędzla(symbol,누름=1):Połącz.sendall(struct.pack('!BBHI',4,누름,0,symbol))
                처음=len(LOG_zapis)
                for znak_WARTOŚĆ in 'echo ':Klucz_ślad_pędzla(ord(znak_WARTOŚĆ))
                Klucz_ślad_pędzla(0xffc6)
                for znak_WARTOŚĆ in 'gksrmf':Klucz_ślad_pędzla(ord(znak_WARTOŚĆ))
                Klucz_ślad_pędzla(0xffc6);Klucz_ślad_pędzla(0xff0d)
                stan_oczekiwania('\r\n한글\r\n'.encode(),처음)
                Raport_WARTOŚĆ['checks'].append('Native VNC F9 two-set Hangul composition')
                Połącz.sendall(struct.pack('!BBHH',5,0,120,100))
                Raport_WARTOŚĆ['checks'].append('VNC pointer input accepted')
            Proces_WARTOŚĆ.stdin.write(b'poweroff\n');Proces_WARTOŚĆ.stdin.flush();Proces_WARTOŚĆ.wait(timeout=15);assert Proces_WARTOŚĆ.returncode==0
            Raport_WARTOŚĆ['passed']=True
    finally:
        if Proces_WARTOŚĆ and Proces_WARTOŚĆ.poll() is None:
            Proces_WARTOŚĆ.terminate()
            try: Proces_WARTOŚĆ.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_WARTOŚĆ.kill();Proces_WARTOŚĆ.wait()
        (pozycja_wyjścia/'serial.log').write_bytes(LOG_zapis)
        (pozycja_wyjścia/'report.json').write_text(json.dumps(Raport_WARTOŚĆ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Raport_WARTOŚĆ,ensure_ascii=False,indent=2))


if __name__=='__main__': Uruchom_2()
