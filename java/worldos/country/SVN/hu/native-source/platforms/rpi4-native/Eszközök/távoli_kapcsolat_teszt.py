#!/usr/bin/env python3
"""tényleges_adat OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from végrehajt_parancs import teendő_gyök, Parancs
from híd_3de4fe3a import híd_3de4fe3a


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--kernel', type=Path, default=teendő_gyök / 'build/kernel8.img')
    elemző_48ee4b1b.add_argument('--access', type=Path, default=teendő_gyök / 'build/remote/access.json')
    elemző_48ee4b1b.add_argument('--output', type=Path, default=teendő_gyök / 'build/verification/native-remote')
    Argumentumok = elemző_48ee4b1b.parse_args()
    Kimenet = Argumentumok.output
    Kimenet.mkdir(parents=True, exist_ok=True)
    Beállítások = json.loads(Argumentumok.access.read_text())
    jelent_ÉRTÉK = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumentumok.kernel.read_bytes()).hexdigest(), 'checks': []}
    def üres_port():
        with socket.socket() as Kapcsolódás:
            Kapcsolódás.bind(('127.0.0.5', 0))
            return Kapcsolódás.getsockname()[1]
    felület_port, 화면포트, fájlport = üres_port(), üres_port(), üres_port()
    LOG_REKORD = bytearray()
    folyamat_ÉRTÉK = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, híd_3de4fe3a(fájlport,
                ['tcp:{}:22'.format(felület_port), 'tcp:{}:5900'.format(화면포트)], gazda_CÍM='127.0.0.5') as híd_ÉRTÉK:
            실행인수 = Parancs()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumentumok.kernel.resolve())
            folyamat_ÉRTÉK = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + híd_ÉRTÉK.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    adat = folyamat_ÉRTÉK.stdout.read(4096)
                    if not adat: break
                    LOG_REKORD.extend(adat)
            szál_ÉRTÉK = threading.Thread(target=수집, daemon=True)
            szál_ÉRTÉK.start()
            def várakozóállapot(szó_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while szó_SMS not in LOG_REKORD[처음:]:
                    if time.monotonic()>끝 or folyamat_ÉRTÉK.poll() is not None:
                        raise AssertionError('Missing '+repr(szó_SMS)+'\n'+LOG_REKORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            várakozóállapot(b'jkoros-native> ')
            segéd_ÉRTÉK = Path(임시)/'askpass'
            segéd_ÉRTÉK.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            segéd_ÉRTÉK.chmod(0o700)
            környezet_5d36e09c = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(segéd_ÉRTÉK), SSH_ASKPASS_REQUIRE='force')
            def biztonságos_felület(jelszó_ÉRTÉK, 명령어, hozzáfűz_bejegyzés=()):
                környezet_5d36e09c['JKOROS_TEST_PASSWORD']=jelszó_ÉRTÉK
                Argumentumok=['ssh','-v']+list(hozzáfűz_bejegyzés)+['-p',str(felület_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                KR=subprocess.run(Argumentumok,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=környezet_5d36e09c,start_new_session=True,timeout=50)
                return KR
            KR=biztonságos_felület('!' + Beállítások['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Kimenet/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_REKORD, KR.stderr
            jelent_ÉRTÉK['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=biztonságos_felület(Beállítások['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Kimenet/'ssh.log').write_bytes(KR.stderr)
            (Kimenet/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            jelent_ÉRTÉK['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            jelent_ÉRTÉK['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=biztonságos_felület(Beállítások['ssh_password'], 'cd /example/java; java KimenetiPélda; cd /')
            assert KR.returncode==0 and 'JAVA Kimenet: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            jelent_ÉRTÉK['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=biztonságos_felület(Beállítások['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            jelent_ÉRTÉK['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=biztonságos_felület(Beállítások['ssh_password'], 'cat /example/java/AblakPélda.java', ('-o', 'RekeyLimit=1K'))
            (Kimenet/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class AblakPélda'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            jelent_ÉRTÉK['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(felület_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktív_munkamenet=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=környezet_5d36e09c,start_new_session=True,bufsize=0)
            átirat=bytearray();kijelölés_ÉRTÉK=selectors.DefaultSelector();kijelölés_ÉRTÉK.register(interaktív_munkamenet.stdout,selectors.EVENT_READ)
            def 대화읽기(bemutató_ÉRTÉK):
                határidő_ÉRTÉK=time.monotonic()+30
                while bemutató_ÉRTÉK not in átirat:
                    if time.monotonic()>határidő_ÉRTÉK or interaktív_munkamenet.poll() is not None:raise AssertionError('SSH interactive missing '+repr(bemutató_ÉRTÉK)+' '+repr(bytes(átirat)))
                    for bejegyzés_ÉRTÉK,_ in kijelölés_ÉRTÉK.select(.1):
                        조각=bejegyzés_ÉRTÉK.fileobj.read(4096)
                        if 조각:átirat.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktív_munkamenet.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktív_munkamenet.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktív_munkamenet.stdin.write(b'\x04');interaktív_munkamenet.stdin.flush();나머지,HIBA=interaktív_munkamenet.communicate(timeout=15)
                assert interaktív_munkamenet.returncode==0 and b'PTY allocation request failed' not in HIBA,(interaktív_munkamenet.returncode,HIBA)
                (Kimenet/'ssh-interactive.txt').write_bytes(átirat+나머지)
            finally:
                kijelölés_ÉRTÉK.close()
                if interaktív_munkamenet.poll() is None:interaktív_munkamenet.kill();interaktív_munkamenet.wait()
            jelent_ÉRTÉK['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Kapcsolódás, szám):
                adat=bytearray()
                while len(adat)<szám:
                    adatrészlet_ÉRTÉK=Kapcsolódás.recv(szám-len(adat))
                    if not adatrészlet_ÉRTÉK: raise AssertionError('RFB EOF')
                    adat.extend(adatrészlet_ÉRTÉK)
                return bytes(adat)
            def 화면인증(jelszó_ÉRTÉK):
                Kapcsolódás=socket.create_connection(('127.0.0.5',화면포트),10);Kapcsolódás.settimeout(30)
                assert 정확히(Kapcsolódás,12)==b'RFB 003.008\n'
                Kapcsolódás.sendall(b'RFB 003.008\n');assert 정확히(Kapcsolódás,2)==b'\x01\x02'
                Kapcsolódás.sendall(b'\x02');kihívás_ÉRTÉK=정확히(Kapcsolódás,16)
                bevitel_jelszó=jelszó_ÉRTÉK.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(szám)[::-1],2) for szám in bevitel_jelszó)
                Kapcsolódás.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(kihívás_ÉRTÉK))
                Állapot_ÉRTÉK=struct.unpack('!I',정확히(Kapcsolódás,4))[0]
                return Kapcsolódás,Állapot_ÉRTÉK
            alaptalan_jelszó='!' if not Beállítások['vnc_password'].startswith('!') else '?'
            Kapcsolódás,Állapot_ÉRTÉK=화면인증(alaptalan_jelszó);assert Állapot_ÉRTÉK==1;Kapcsolódás.close();time.sleep(.6)
            jelent_ÉRTÉK['checks'].append('VNC incorrect password rejected')
            Kapcsolódás,Állapot_ÉRTÉK=화면인증(Beállítások['vnc_password']);assert Állapot_ÉRTÉK==0
            with Kapcsolódás:
                Kapcsolódás.sendall(b'\x01');kiinduló_állapot=정확히(Kapcsolódás,24);너비,높이=struct.unpack('!HH',kiinduló_állapot[:4]);Név=정확히(Kapcsolódás,struct.unpack('!I',kiinduló_állapot[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Név
                def 화면(növekmény_lépés=0):
                    Kapcsolódás.sendall(struct.pack('!BBHHHH',3,növekmény_lépés,0,0,너비,높이));머리=정확히(Kapcsolódás,4);szám=struct.unpack('!H',머리[2:])[0];összesen_ÉRTÉK=0
                    rajz_ÉRTÉK=bytearray(너비*높이*4)
                    for _ in range(szám):
                        x_koordináta,Y_koordináta,영역너비,영역높이,metódus_mód=struct.unpack('!HHHHi',정확히(Kapcsolódás,12));assert metódus_mód==0 and x_koordináta+영역너비<=너비 and Y_koordináta+영역높이<=높이
                        képpont=정확히(Kapcsolódás,영역너비*영역높이*4);összesen_ÉRTÉK+=len(képpont)
                        for Vonal in range(영역높이):rajz_ÉRTÉK[((Y_koordináta+Vonal)*너비+x_koordináta)*4:((Y_koordináta+Vonal)*너비+x_koordináta+영역너비)*4]=képpont[Vonal*영역너비*4:(Vonal+1)*영역너비*4]
                    if not növekmény_lépés:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(rajz_ÉRTÉK),'raw','BGRX').save(str(Kimenet/'native-vnc.png'))
                    return szám,összesen_ÉRTÉK
                szám,összesen_ÉRTÉK=화면();assert szám>0 and összesen_ÉRTÉK==너비*높이*4
                jelent_ÉRTÉK['checks'].append('Native framebuffer RFB full update {} bytes'.format(összesen_ÉRTÉK))
                szám,összesen_ÉRTÉK=화면(1);assert összesen_ÉRTÉK<너비*높이*4
                jelent_ÉRTÉK['checks'].append('RFB incremental update')
                처음=len(LOG_REKORD)
                for karakter_ÉRTÉK in 'echo VNC_NATIVE_PASS\r':
                    szimbólum=0xff0d if karakter_ÉRTÉK=='\r' else ord(karakter_ÉRTÉK)
                    Kapcsolódás.sendall(struct.pack('!BBHI',4,1,0,szimbólum));Kapcsolódás.sendall(struct.pack('!BBHI',4,0,0,szimbólum))
                várakozóállapot(b'VNC_NATIVE_PASS',처음)
                jelent_ÉRTÉK['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Kulcs_tollvonás(szimbólum,누름=1):Kapcsolódás.sendall(struct.pack('!BBHI',4,누름,0,szimbólum))
                처음=len(LOG_REKORD)
                for karakter_ÉRTÉK in 'echo ':Kulcs_tollvonás(ord(karakter_ÉRTÉK))
                Kulcs_tollvonás(0xffc6)
                for karakter_ÉRTÉK in 'gksrmf':Kulcs_tollvonás(ord(karakter_ÉRTÉK))
                Kulcs_tollvonás(0xffc6);Kulcs_tollvonás(0xff0d)
                várakozóállapot('\r\n한글\r\n'.encode(),처음)
                jelent_ÉRTÉK['checks'].append('Native VNC F9 two-set Hangul composition')
                Kapcsolódás.sendall(struct.pack('!BBHH',5,0,120,100))
                jelent_ÉRTÉK['checks'].append('VNC pointer input accepted')
            folyamat_ÉRTÉK.stdin.write(b'poweroff\n');folyamat_ÉRTÉK.stdin.flush();folyamat_ÉRTÉK.wait(timeout=15);assert folyamat_ÉRTÉK.returncode==0
            jelent_ÉRTÉK['passed']=True
    finally:
        if folyamat_ÉRTÉK and folyamat_ÉRTÉK.poll() is None:
            folyamat_ÉRTÉK.terminate()
            try: folyamat_ÉRTÉK.wait(timeout=5)
            except subprocess.TimeoutExpired: folyamat_ÉRTÉK.kill();folyamat_ÉRTÉK.wait()
        (Kimenet/'serial.log').write_bytes(LOG_REKORD)
        (Kimenet/'report.json').write_text(json.dumps(jelent_ÉRTÉK,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(jelent_ÉRTÉK,ensure_ascii=False,indent=2))


if __name__=='__main__': Futtatás()
