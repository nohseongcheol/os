#!/usr/bin/env python3
"""skutočný_údaje OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Vykonať_príkaz import akcia_koreň, Príkaz
from sieťový_most import sieťový_most


def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--kernel', type=Path, default=akcia_koreň / 'build/kernel8.img')
    analyzátor_48ee4b1b.add_argument('--access', type=Path, default=akcia_koreň / 'build/remote/access.json')
    analyzátor_48ee4b1b.add_argument('--output', type=Path, default=akcia_koreň / 'build/verification/native-remote')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    Výstup = Argumenty.output
    Výstup.mkdir(parents=True, exist_ok=True)
    Nastavenia = json.loads(Argumenty.access.read_text())
    správa_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenty.kernel.read_bytes()).hexdigest(), 'checks': []}
    def prázdny_port():
        with socket.socket() as Pripojiť:
            Pripojiť.bind(('127.0.0.5', 0))
            return Pripojiť.getsockname()[1]
    셸포트, 화면포트, Súbor_port = prázdny_port(), prázdny_port(), prázdny_port()
    LOG_RECORD = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, sieťový_most(Súbor_port,
                ['tcp:{}:22'.format(셸포트), 'tcp:{}:5900'.format(화면포트)], hostiteľ_adresa='127.0.0.5') as most_VALUE:
            실행인수 = Príkaz()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenty.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + most_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    údaje = Proces_VALUE.stdout.read(4096)
                    if not údaje: break
                    LOG_RECORD.extend(údaje)
            vlákno_VALUE = threading.Thread(target=수집, daemon=True)
            vlákno_VALUE.start()
            def stav_čakania(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stav_čakania(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(heslo_VALUE, inštrukcia_VALUE, Pripojiť_položka=()):
                환경['JKOROS_TEST_PASSWORD']=heslo_VALUE
                Argumenty=['ssh','-v']+list(Pripojiť_položka)+['-p',str(셸포트),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',inštrukcia_VALUE]
                KR=subprocess.run(Argumenty,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return KR
            KR=보안셸('!' + Nastavenia['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Výstup/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, KR.stderr
            správa_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=보안셸(Nastavenia['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Výstup/'ssh.log').write_bytes(KR.stderr)
            (Výstup/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            správa_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            správa_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=보안셸(Nastavenia['ssh_password'], 'cd /example/java; java UkážkaVýstupu; cd /')
            assert KR.returncode==0 and 'JAVA Výstup: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            správa_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=보안셸(Nastavenia['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            správa_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=보안셸(Nastavenia['ssh_password'], 'cat /example/java/UkážkaOkna.java', ('-o', 'RekeyLimit=1K'))
            (Výstup/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class UkážkaOkna'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            správa_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(셸포트),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktívny_relácia=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            prepis=bytearray();výber_VALUE=selectors.DefaultSelector();výber_VALUE.register(interaktívny_relácia.stdout,selectors.EVENT_READ)
            def 대화읽기(zobraziť_VALUE_487749b8):
                termín_VALUE=time.monotonic()+30
                while zobraziť_VALUE_487749b8 not in prepis:
                    if time.monotonic()>termín_VALUE or interaktívny_relácia.poll() is not None:raise AssertionError('SSH interactive missing '+repr(zobraziť_VALUE_487749b8)+' '+repr(bytes(prepis)))
                    for položka_VALUE,_ in výber_VALUE.select(.1):
                        조각=položka_VALUE.fileobj.read(4096)
                        if 조각:prepis.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktívny_relácia.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktívny_relácia.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktívny_relácia.stdin.write(b'\x04');interaktívny_relácia.stdin.flush();나머지,chyba=interaktívny_relácia.communicate(timeout=15)
                assert interaktívny_relácia.returncode==0 and b'PTY allocation request failed' not in chyba,(interaktívny_relácia.returncode,chyba)
                (Výstup/'ssh-interactive.txt').write_bytes(prepis+나머지)
            finally:
                výber_VALUE.close()
                if interaktívny_relácia.poll() is None:interaktívny_relácia.kill();interaktívny_relácia.wait()
            správa_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Pripojiť, 수):
                údaje=bytearray()
                while len(údaje)<수:
                    blok_údajov_VALUE=Pripojiť.recv(수-len(údaje))
                    if not blok_údajov_VALUE: raise AssertionError('RFB EOF')
                    údaje.extend(blok_údajov_VALUE)
                return bytes(údaje)
            def 화면인증(heslo_VALUE):
                Pripojiť=socket.create_connection(('127.0.0.5',화면포트),10);Pripojiť.settimeout(30)
                assert 정확히(Pripojiť,12)==b'RFB 003.008\n'
                Pripojiť.sendall(b'RFB 003.008\n');assert 정확히(Pripojiť,2)==b'\x01\x02'
                Pripojiť.sendall(b'\x02');výzva_VALUE=정확히(Pripojiť,16)
                vstup_heslo=heslo_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in vstup_heslo)
                Pripojiť.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(výzva_VALUE))
                Stav_VALUE=struct.unpack('!I',정확히(Pripojiť,4))[0]
                return Pripojiť,Stav_VALUE
            neplatné_heslo='!' if not Nastavenia['vnc_password'].startswith('!') else '?'
            Pripojiť,Stav_VALUE=화면인증(neplatné_heslo);assert Stav_VALUE==1;Pripojiť.close();time.sleep(.6)
            správa_VALUE['checks'].append('VNC incorrect password rejected')
            Pripojiť,Stav_VALUE=화면인증(Nastavenia['vnc_password']);assert Stav_VALUE==0
            with Pripojiť:
                Pripojiť.sendall(b'\x01');počiatočný_stav=정확히(Pripojiť,24);너비,výška_VALUE=struct.unpack('!HH',počiatočný_stav[:4]);Názov=정확히(Pripojiť,struct.unpack('!I',počiatočný_stav[20:24])[0])
                assert (너비,výška_VALUE)==(640,480) and b'jkoros native'==Názov
                def 화면(prírastok_krok=0):
                    Pripojiť.sendall(struct.pack('!BBHHHH',3,prírastok_krok,0,0,너비,výška_VALUE));머리=정확히(Pripojiť,4);수=struct.unpack('!H',머리[2:])[0];celkovo_VALUE=0
                    kresba_VALUE=bytearray(너비*výška_VALUE*4)
                    for _ in range(수):
                        X_súradnica,Y_súradnica,영역너비,oblasť_výška,metóda_MODE=struct.unpack('!HHHHi',정확히(Pripojiť,12));assert metóda_MODE==0 and X_súradnica+영역너비<=너비 and Y_súradnica+oblasť_výška<=výška_VALUE
                        pixel=정확히(Pripojiť,영역너비*oblasť_výška*4);celkovo_VALUE+=len(pixel)
                        for riadok in range(oblasť_výška):kresba_VALUE[((Y_súradnica+riadok)*너비+X_súradnica)*4:((Y_súradnica+riadok)*너비+X_súradnica+영역너비)*4]=pixel[riadok*영역너비*4:(riadok+1)*영역너비*4]
                    if not prírastok_krok:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,výška_VALUE),bytes(kresba_VALUE),'raw','BGRX').save(str(Výstup/'native-vnc.png'))
                    return 수,celkovo_VALUE
                수,celkovo_VALUE=화면();assert 수>0 and celkovo_VALUE==너비*výška_VALUE*4
                správa_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(celkovo_VALUE))
                수,celkovo_VALUE=화면(1);assert celkovo_VALUE<너비*výška_VALUE*4
                správa_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for znak_VALUE in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if znak_VALUE=='\r' else ord(znak_VALUE)
                    Pripojiť.sendall(struct.pack('!BBHI',4,1,0,symbol));Pripojiť.sendall(struct.pack('!BBHI',4,0,0,symbol))
                stav_čakania(b'VNC_NATIVE_PASS',처음)
                správa_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Kľúč_ťah_perom(symbol,누름=1):Pripojiť.sendall(struct.pack('!BBHI',4,누름,0,symbol))
                처음=len(LOG_RECORD)
                for znak_VALUE in 'echo ':Kľúč_ťah_perom(ord(znak_VALUE))
                Kľúč_ťah_perom(0xffc6)
                for znak_VALUE in 'gksrmf':Kľúč_ťah_perom(ord(znak_VALUE))
                Kľúč_ťah_perom(0xffc6);Kľúč_ťah_perom(0xff0d)
                stav_čakania('\r\n한글\r\n'.encode(),처음)
                správa_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Pripojiť.sendall(struct.pack('!BBHH',5,0,120,100))
                správa_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            správa_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (Výstup/'serial.log').write_bytes(LOG_RECORD)
        (Výstup/'report.json').write_text(json.dumps(správa_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(správa_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Spustiť_2()
