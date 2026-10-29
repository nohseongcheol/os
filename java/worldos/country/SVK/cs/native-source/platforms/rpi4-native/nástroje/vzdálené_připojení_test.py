#!/usr/bin/env python3
"""skutečný_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Provést_příkaz import akce_kořen, příkaz
from most_3de4fe3a import most_3de4fe3a


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--kernel', type=Path, default=akce_kořen / 'build/kernel8.img')
    analyzátor_48ee4b1b.add_argument('--access', type=Path, default=akce_kořen / 'build/remote/access.json')
    analyzátor_48ee4b1b.add_argument('--output', type=Path, default=akce_kořen / 'build/verification/native-remote')
    argumenty = analyzátor_48ee4b1b.parse_args()
    výstupní_pozice = argumenty.output
    výstupní_pozice.mkdir(parents=True, exist_ok=True)
    Nastavení = json.loads(argumenty.access.read_text())
    Zpráva_HODNOTA = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumenty.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Připojit:
            Připojit.bind(('127.0.0.5', 0))
            return Připojit.getsockname()[1]
    prostředí_port, 화면포트, souborový_port = 빈포트(), 빈포트(), 빈포트()
    LOGZ_ZÁZNAM = bytearray()
    Proces_HODNOTA = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, most_3de4fe3a(souborový_port,
                ['tcp:{}:22'.format(prostředí_port), 'tcp:{}:5900'.format(화면포트)], hostit_ODKAZ='127.0.0.5') as most_HODNOTA:
            실행인수 = příkaz()
            실행인수[실행인수.index('-kernel') + 1] = str(argumenty.kernel.resolve())
            Proces_HODNOTA = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_HODNOTA.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proces_HODNOTA.stdout.read(4096)
                    if not data: break
                    LOGZ_ZÁZNAM.extend(data)
            vlákno_HODNOTA = threading.Thread(target=수집, daemon=True)
            vlákno_HODNOTA.start()
            def čekací_stav(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOGZ_ZÁZNAM[처음:]:
                    if time.monotonic()>끝 or Proces_HODNOTA.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOGZ_ZÁZNAM[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            čekací_stav(b'jkoros-native> ')
            pomocná_rutina_HODNOTA = Path(임시)/'askpass'
            pomocná_rutina_HODNOTA.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            pomocná_rutina_HODNOTA.chmod(0o700)
            prostředí_5d36e09c = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(pomocná_rutina_HODNOTA), SSH_ASKPASS_REQUIRE='force')
            def SSH(heslo_HODNOTA, 명령어, Připojit_položka=()):
                prostředí_5d36e09c['JKOROS_TEST_PASSWORD']=heslo_HODNOTA
                argumenty=['ssh','-v']+list(Připojit_položka)+['-p',str(prostředí_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                VÝSLEDEK=subprocess.run(argumenty,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=prostředí_5d36e09c,start_new_session=True,timeout=50)
                return VÝSLEDEK
            VÝSLEDEK=SSH('!' + Nastavení['ssh_password'], 'echo SHOULD_NOT_RUN')
            (výstupní_pozice/'ssh-rejected.log').write_bytes(VÝSLEDEK.stderr)
            assert VÝSLEDEK.returncode!=0 and b'Permission denied' in VÝSLEDEK.stderr and b'SHOULD_NOT_RUN' not in LOGZ_ZÁZNAM, VÝSLEDEK.stderr
            Zpráva_HODNOTA['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            VÝSLEDEK=SSH(Nastavení['ssh_password'], 'echo SSH_NATIVE_PASS')
            (výstupní_pozice/'ssh.log').write_bytes(VÝSLEDEK.stderr)
            (výstupní_pozice/'ssh-output.txt').write_bytes(VÝSLEDEK.stdout)
            assert VÝSLEDEK.returncode==0 and b'SSH_NATIVE_PASS' in VÝSLEDEK.stdout, (VÝSLEDEK.returncode,VÝSLEDEK.stdout,VÝSLEDEK.stderr)
            Zpráva_HODNOTA['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in VÝSLEDEK.stderr, VÝSLEDEK.stderr
            Zpráva_HODNOTA['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            VÝSLEDEK=SSH(Nastavení['ssh_password'], 'cd /example/java; java UkázkaVýstupu; cd /')
            assert VÝSLEDEK.returncode==0 and 'JAVA výstupní_pozice: 안녕하세요 😀'.encode() in VÝSLEDEK.stdout,VÝSLEDEK.stdout
            Zpráva_HODNOTA['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            VÝSLEDEK=SSH(Nastavení['ssh_password'], 'missing_remote_command')
            assert VÝSLEDEK.returncode==127,VÝSLEDEK.returncode
            Zpráva_HODNOTA['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            VÝSLEDEK=SSH(Nastavení['ssh_password'], 'cat /example/java/UkázkaOkna.java', ('-o', 'RekeyLimit=1K'))
            (výstupní_pozice/'ssh-rekey.log').write_bytes(VÝSLEDEK.stderr)
            assert VÝSLEDEK.returncode==0 and 'class UkázkaOkna'.encode() in VÝSLEDEK.stdout, (VÝSLEDEK.returncode,VÝSLEDEK.stdout,VÝSLEDEK.stderr)
            assert VÝSLEDEK.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, VÝSLEDEK.stderr
            Zpráva_HODNOTA['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(prostředí_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktivní_relace=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=prostředí_5d36e09c,start_new_session=True,bufsize=0)
            přepis=bytearray();výběr_HODNOTA=selectors.DefaultSelector();výběr_HODNOTA.register(interaktivní_relace.stdout,selectors.EVENT_READ)
            def 대화읽기(zobrazit_HODNOTA):
                konečný_termín_HODNOTA=time.monotonic()+30
                while zobrazit_HODNOTA not in přepis:
                    if time.monotonic()>konečný_termín_HODNOTA or interaktivní_relace.poll() is not None:raise AssertionError('SSH interactive missing '+repr(zobrazit_HODNOTA)+' '+repr(bytes(přepis)))
                    for položka_HODNOTA,_ in výběr_HODNOTA.select(.1):
                        조각=položka_HODNOTA.fileobj.read(4096)
                        if 조각:přepis.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktivní_relace.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktivní_relace.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktivní_relace.stdin.write(b'\x04');interaktivní_relace.stdin.flush();나머지,chyba=interaktivní_relace.communicate(timeout=15)
                assert interaktivní_relace.returncode==0 and b'PTY allocation request failed' not in chyba,(interaktivní_relace.returncode,chyba)
                (výstupní_pozice/'ssh-interactive.txt').write_bytes(přepis+나머지)
            finally:
                výběr_HODNOTA.close()
                if interaktivní_relace.poll() is None:interaktivní_relace.kill();interaktivní_relace.wait()
            Zpráva_HODNOTA['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Připojit, číslo):
                data=bytearray()
                while len(data)<číslo:
                    blok_dat_HODNOTA=Připojit.recv(číslo-len(data))
                    if not blok_dat_HODNOTA: raise AssertionError('RFB EOF')
                    data.extend(blok_dat_HODNOTA)
                return bytes(data)
            def 화면인증(heslo_HODNOTA):
                Připojit=socket.create_connection(('127.0.0.5',화면포트),10);Připojit.settimeout(30)
                assert 정확히(Připojit,12)==b'RFB 003.008\n'
                Připojit.sendall(b'RFB 003.008\n');assert 정확히(Připojit,2)==b'\x01\x02'
                Připojit.sendall(b'\x02');výzva_HODNOTA=정확히(Připojit,16)
                vstup_heslo=heslo_HODNOTA.encode('ascii')[:8].ljust(8, b'\0')
                Klíč_materiál=bytes(int('{:08b}'.format(číslo)[::-1],2) for číslo in vstup_heslo)
                Připojit.sendall(DES.new(Klíč_materiál,DES.MODE_ECB).encrypt(výzva_HODNOTA))
                Stav_HODNOTA=struct.unpack('!I',정확히(Připojit,4))[0]
                return Připojit,Stav_HODNOTA
            neplatný_heslo='!' if not Nastavení['vnc_password'].startswith('!') else '?'
            Připojit,Stav_HODNOTA=화면인증(neplatný_heslo);assert Stav_HODNOTA==1;Připojit.close();time.sleep(.6)
            Zpráva_HODNOTA['checks'].append('VNC incorrect password rejected')
            Připojit,Stav_HODNOTA=화면인증(Nastavení['vnc_password']);assert Stav_HODNOTA==0
            with Připojit:
                Připojit.sendall(b'\x01');počáteční_stav=정확히(Připojit,24);너비,výška_HODNOTA=struct.unpack('!HH',počáteční_stav[:4]);Název=정확히(Připojit,struct.unpack('!I',počáteční_stav[20:24])[0])
                assert (너비,výška_HODNOTA)==(640,480) and b'jkoros native'==Název
                def 화면(증분=0):
                    Připojit.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,výška_HODNOTA));머리=정확히(Připojit,4);číslo=struct.unpack('!H',머리[2:])[0];celkem_HODNOTA=0
                    kreslení_HODNOTA=bytearray(너비*výška_HODNOTA*4)
                    for _ in range(číslo):
                        souřadnice_x,Y_souřadnice,영역너비,oblast_výška,metoda_MODE=struct.unpack('!HHHHi',정확히(Připojit,12));assert metoda_MODE==0 and souřadnice_x+영역너비<=너비 and Y_souřadnice+oblast_výška<=výška_HODNOTA
                        pixel=정확히(Připojit,영역너비*oblast_výška*4);celkem_HODNOTA+=len(pixel)
                        for vstupní_řádek in range(oblast_výška):kreslení_HODNOTA[((Y_souřadnice+vstupní_řádek)*너비+souřadnice_x)*4:((Y_souřadnice+vstupní_řádek)*너비+souřadnice_x+영역너비)*4]=pixel[vstupní_řádek*영역너비*4:(vstupní_řádek+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,výška_HODNOTA),bytes(kreslení_HODNOTA),'raw','BGRX').save(str(výstupní_pozice/'native-vnc.png'))
                    return číslo,celkem_HODNOTA
                číslo,celkem_HODNOTA=화면();assert číslo>0 and celkem_HODNOTA==너비*výška_HODNOTA*4
                Zpráva_HODNOTA['checks'].append('Native framebuffer RFB full update {} bytes'.format(celkem_HODNOTA))
                číslo,celkem_HODNOTA=화면(1);assert celkem_HODNOTA<너비*výška_HODNOTA*4
                Zpráva_HODNOTA['checks'].append('RFB incremental update')
                처음=len(LOGZ_ZÁZNAM)
                for znak_HODNOTA in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if znak_HODNOTA=='\r' else ord(znak_HODNOTA)
                    Připojit.sendall(struct.pack('!BBHI',4,1,0,symbol));Připojit.sendall(struct.pack('!BBHI',4,0,0,symbol))
                čekací_stav(b'VNC_NATIVE_PASS',처음)
                Zpráva_HODNOTA['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Klíč_tah(symbol,누름=1):Připojit.sendall(struct.pack('!BBHI',4,누름,0,symbol))
                처음=len(LOGZ_ZÁZNAM)
                for znak_HODNOTA in 'echo ':Klíč_tah(ord(znak_HODNOTA))
                Klíč_tah(0xffc6)
                for znak_HODNOTA in 'gksrmf':Klíč_tah(ord(znak_HODNOTA))
                Klíč_tah(0xffc6);Klíč_tah(0xff0d)
                čekací_stav('\r\n한글\r\n'.encode(),처음)
                Zpráva_HODNOTA['checks'].append('Native VNC F9 two-set Hangul composition')
                Připojit.sendall(struct.pack('!BBHH',5,0,120,100))
                Zpráva_HODNOTA['checks'].append('VNC pointer input accepted')
            Proces_HODNOTA.stdin.write(b'poweroff\n');Proces_HODNOTA.stdin.flush();Proces_HODNOTA.wait(timeout=15);assert Proces_HODNOTA.returncode==0
            Zpráva_HODNOTA['passed']=True
    finally:
        if Proces_HODNOTA and Proces_HODNOTA.poll() is None:
            Proces_HODNOTA.terminate()
            try: Proces_HODNOTA.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_HODNOTA.kill();Proces_HODNOTA.wait()
        (výstupní_pozice/'serial.log').write_bytes(LOGZ_ZÁZNAM)
        (výstupní_pozice/'report.json').write_text(json.dumps(Zpráva_HODNOTA,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Zpráva_HODNOTA,ensure_ascii=False,indent=2))


if __name__=='__main__': Spustit_2()
