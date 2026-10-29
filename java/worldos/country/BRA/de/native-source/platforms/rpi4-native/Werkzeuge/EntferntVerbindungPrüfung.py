#!/usr/bin/env python3
"""tatsächlichDaten OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from befehlAusführen import projektWurzel, befehl
from netzwerkBrücke import netzwerkBrücke


def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--kernel', type=Path, default=projektWurzel / 'build/kernel8.img')
    Strukturanalysierer.add_argument('--access', type=Path, default=projektWurzel / 'build/remote/access.json')
    Strukturanalysierer.add_argument('--output', type=Path, default=projektWurzel / 'build/verification/native-remote')
    argumente = Strukturanalysierer.parse_args()
    Ausgabe = argumente.output
    Ausgabe.mkdir(parents=True, exist_ok=True)
    einstellungen = json.loads(argumente.access.read_text())
    berichtWert = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumente.kernel.read_bytes()).hexdigest(), 'checks': []}
    def leerwertPort():
        with socket.socket() as verbinden:
            verbinden.bind(('127.0.0.5', 0))
            return verbinden.getsockname()[1]
    befehlshüllePort, bildschirmPort, dateiPort = leerwertPort(), leerwertPort(), leerwertPort()
    protokolldateiAufzeichnung = bytearray()
    prozessWert = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as vorläufigWert, netzwerkBrücke(dateiPort,
                ['tcp:{}:22'.format(befehlshüllePort), 'tcp:{}:5900'.format(bildschirmPort)], wirtssystemAdresse='127.0.0.5') as brückeWert:
            Argumente = befehl()
            Argumente[Argumente.index('-kernel') + 1] = str(argumente.kernel.resolve())
            prozessWert = subprocess.Popen(Argumente + ['-display','none','-monitor','none','-serial','stdio'] + brückeWert.weitergeleitetArgument(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def werteSammeln():
                while True:
                    Daten = prozessWert.stdout.read(4096)
                    if not Daten: break
                    protokolldateiAufzeichnung.extend(Daten)
            ausführungsfadenWert = threading.Thread(target=werteSammeln, daemon=True)
            ausführungsfadenWert.start()
            def statuswertWarten(maschinenwortText, anfänglichElementeintrag=0, grenzwertWert=60):
                endung = time.monotonic() + grenzwertWert
                while maschinenwortText not in protokolldateiAufzeichnung[anfänglichElementeintrag:]:
                    if time.monotonic()>endung or prozessWert.poll() is not None:
                        raise AssertionError('Missing '+repr(maschinenwortText)+'\n'+protokolldateiAufzeichnung[anfänglichElementeintrag:].decode('utf-8','replace'))
                    time.sleep(.02)
            statuswertWarten(b'jkoros-native> ')
            helferWert = Path(vorläufigWert)/'askpass'
            helferWert.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            helferWert.chmod(0o700)
            umgebung = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(helferWert), SSH_ASKPASS_REQUIRE='force')
            def absichernBefehlshülle(passwortWert, befehlswortWert, eintragAnhängen=()):
                umgebung['JKOROS_TEST_PASSWORD']=passwortWert
                argumente=['ssh','-v']+list(eintragAnhängen)+['-p',str(befehlshüllePort),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(vorläufigWert)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',befehlswortWert]
                ergebnis=subprocess.run(argumente,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=umgebung,start_new_session=True,timeout=50)
                return ergebnis
            ergebnis=absichernBefehlshülle('!' + einstellungen['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Ausgabe/'ssh-rejected.log').write_bytes(ergebnis.stderr)
            assert ergebnis.returncode!=0 and b'Permission denied' in ergebnis.stderr and b'SHOULD_NOT_RUN' not in protokolldateiAufzeichnung, ergebnis.stderr
            berichtWert['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ergebnis=absichernBefehlshülle(einstellungen['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Ausgabe/'ssh.log').write_bytes(ergebnis.stderr)
            (Ausgabe/'ssh-output.txt').write_bytes(ergebnis.stdout)
            assert ergebnis.returncode==0 and b'SSH_NATIVE_PASS' in ergebnis.stdout, (ergebnis.returncode,ergebnis.stdout,ergebnis.stderr)
            berichtWert['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ergebnis.stderr, ergebnis.stderr
            berichtWert['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ergebnis=absichernBefehlshülle(einstellungen['ssh_password'], 'cd /example/java; java Ausgabebeispiel; cd /')
            assert ergebnis.returncode==0 and 'JAVA Ausgabe: 안녕하세요 😀'.encode() in ergebnis.stdout,ergebnis.stdout
            berichtWert['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ergebnis=absichernBefehlshülle(einstellungen['ssh_password'], 'missing_remote_command')
            assert ergebnis.returncode==127,ergebnis.returncode
            berichtWert['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ergebnis=absichernBefehlshülle(einstellungen['ssh_password'], 'cat /example/java/Fensterbeispiel.java', ('-o', 'RekeyLimit=1K'))
            (Ausgabe/'ssh-rekey.log').write_bytes(ergebnis.stderr)
            assert ergebnis.returncode==0 and 'class Fensterbeispiel'.encode() in ergebnis.stdout, (ergebnis.returncode,ergebnis.stdout,ergebnis.stderr)
            assert ergebnis.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ergebnis.stderr
            berichtWert['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            interaktivArgumente=['ssh','-tt','-p',str(befehlshüllePort),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(vorläufigWert)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktivSitzung=subprocess.Popen(interaktivArgumente,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=umgebung,start_new_session=True,bufsize=0)
            ablaufprotokoll=bytearray();auswahlWert=selectors.DefaultSelector();auswahlWert.register(interaktivSitzung.stdout,selectors.EVENT_READ)
            def interaktivLesen(wertAnzeigen):
                fristWert=time.monotonic()+30
                while wertAnzeigen not in ablaufprotokoll:
                    if time.monotonic()>fristWert or interaktivSitzung.poll() is not None:raise AssertionError('SSH interactive missing '+repr(wertAnzeigen)+' '+repr(bytes(ablaufprotokoll)))
                    for eintragWert,_ in auswahlWert.select(.1):
                        fragmentWert=eintragWert.fileobj.read(4096)
                        if fragmentWert:ablaufprotokoll.extend(fragmentWert)
            try:
                interaktivLesen(b'shared native console')
                interaktivSitzung.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktivSitzung.stdin.flush();interaktivLesen(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktivSitzung.stdin.write(b'\x04');interaktivSitzung.stdin.flush();restwertWert,fehler=interaktivSitzung.communicate(timeout=15)
                assert interaktivSitzung.returncode==0 and b'PTY allocation request failed' not in fehler,(interaktivSitzung.returncode,fehler)
                (Ausgabe/'ssh-interactive.txt').write_bytes(ablaufprotokoll+restwertWert)
            finally:
                auswahlWert.close()
                if interaktivSitzung.poll() is None:interaktivSitzung.kill();interaktivSitzung.wait()
            berichtWert['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def genauWert(verbinden, Zahl):
                Daten=bytearray()
                while len(Daten)<Zahl:
                    teilblockWert=verbinden.recv(Zahl-len(Daten))
                    if not teilblockWert: raise AssertionError('RFB EOF')
                    Daten.extend(teilblockWert)
                return bytes(Daten)
            def bildschirmAuthentifizierung(passwortWert):
                verbinden=socket.create_connection(('127.0.0.5',bildschirmPort),10);verbinden.settimeout(30)
                assert genauWert(verbinden,12)==b'RFB 003.008\n'
                verbinden.sendall(b'RFB 003.008\n');assert genauWert(verbinden,2)==b'\x01\x02'
                verbinden.sendall(b'\x02');herausforderungWert=genauWert(verbinden,16)
                eingabePasswort=passwortWert.encode('ascii')[:8].ljust(8, b'\0')
                tasteMaterial=bytes(int('{:08b}'.format(Zahl)[::-1],2) for Zahl in eingabePasswort)
                verbinden.sendall(DES.new(tasteMaterial,DES.MODE_ECB).encrypt(herausforderungWert))
                statuswertWert=struct.unpack('!I',genauWert(verbinden,4))[0]
                return verbinden,statuswertWert
            ungültigPasswort='!' if not einstellungen['vnc_password'].startswith('!') else '?'
            verbinden,statuswertWert=bildschirmAuthentifizierung(ungültigPasswort);assert statuswertWert==1;verbinden.close();time.sleep(.6)
            berichtWert['checks'].append('VNC incorrect password rejected')
            verbinden,statuswertWert=bildschirmAuthentifizierung(einstellungen['vnc_password']);assert statuswertWert==0
            with verbinden:
                verbinden.sendall(b'\x01');anfänglichStatuswert=genauWert(verbinden,24);breiteWert,höheWert=struct.unpack('!HH',anfänglichStatuswert[:4]);Name=genauWert(verbinden,struct.unpack('!I',anfänglichStatuswert[20:24])[0])
                assert (breiteWert,höheWert)==(640,480) and b'jkoros native'==Name
                def Bildschirm(erhöhenSchrittSchritt=0):
                    verbinden.sendall(struct.pack('!BBHHHH',3,erhöhenSchrittSchritt,0,0,breiteWert,höheWert));kopfWert=genauWert(verbinden,4);Zahl=struct.unpack('!H',kopfWert[2:])[0];gesamtwertWert=0
                    Zeichnung=bytearray(breiteWert*höheWert*4)
                    for _ in range(Zahl):
                        waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,gebietBreite,gebietHöhe,methodeBetriebsart=struct.unpack('!HHHHi',genauWert(verbinden,12));assert methodeBetriebsart==0 and waagerechteKoordinateKoordinate+gebietBreite<=breiteWert and senkrechteKoordinateKoordinate+gebietHöhe<=höheWert
                        bildpunkt=genauWert(verbinden,gebietBreite*gebietHöhe*4);gesamtwertWert+=len(bildpunkt)
                        for zeile in range(gebietHöhe):Zeichnung[((senkrechteKoordinateKoordinate+zeile)*breiteWert+waagerechteKoordinateKoordinate)*4:((senkrechteKoordinateKoordinate+zeile)*breiteWert+waagerechteKoordinateKoordinate+gebietBreite)*4]=bildpunkt[zeile*gebietBreite*4:(zeile+1)*gebietBreite*4]
                    if not erhöhenSchrittSchritt:
                        from PIL import Image
                        Image.frombytes('RGB',(breiteWert,höheWert),bytes(Zeichnung),'raw','BGRX').save(str(Ausgabe/'native-vnc.png'))
                    return Zahl,gesamtwertWert
                Zahl,gesamtwertWert=Bildschirm();assert Zahl>0 and gesamtwertWert==breiteWert*höheWert*4
                berichtWert['checks'].append('Native framebuffer RFB full update {} bytes'.format(gesamtwertWert))
                Zahl,gesamtwertWert=Bildschirm(1);assert gesamtwertWert<breiteWert*höheWert*4
                berichtWert['checks'].append('RFB incremental update')
                anfänglichElementeintrag=len(protokolldateiAufzeichnung)
                for zeichenWert in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if zeichenWert=='\r' else ord(zeichenWert)
                    verbinden.sendall(struct.pack('!BBHI',4,1,0,symbol));verbinden.sendall(struct.pack('!BBHI',4,0,0,symbol))
                statuswertWarten(b'VNC_NATIVE_PASS',anfänglichElementeintrag)
                berichtWert['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def tasteStrich(symbol,drückenWert=1):verbinden.sendall(struct.pack('!BBHI',4,drückenWert,0,symbol))
                anfänglichElementeintrag=len(protokolldateiAufzeichnung)
                for zeichenWert in 'echo ':tasteStrich(ord(zeichenWert))
                tasteStrich(0xffc6)
                for zeichenWert in 'gksrmf':tasteStrich(ord(zeichenWert))
                tasteStrich(0xffc6);tasteStrich(0xff0d)
                statuswertWarten('\r\n한글\r\n'.encode(),anfänglichElementeintrag)
                berichtWert['checks'].append('Native VNC F9 two-set Hangul composition')
                verbinden.sendall(struct.pack('!BBHH',5,0,120,100))
                berichtWert['checks'].append('VNC pointer input accepted')
            prozessWert.stdin.write(b'poweroff\n');prozessWert.stdin.flush();prozessWert.wait(timeout=15);assert prozessWert.returncode==0
            berichtWert['passed']=True
    finally:
        if prozessWert and prozessWert.poll() is None:
            prozessWert.terminate()
            try: prozessWert.wait(timeout=5)
            except subprocess.TimeoutExpired: prozessWert.kill();prozessWert.wait()
        (Ausgabe/'serial.log').write_bytes(protokolldateiAufzeichnung)
        (Ausgabe/'report.json').write_text(json.dumps(berichtWert,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(berichtWert,ensure_ascii=False,indent=2))


if __name__=='__main__': ausführenVorgang()
