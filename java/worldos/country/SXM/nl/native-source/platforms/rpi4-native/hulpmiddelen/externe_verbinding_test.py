#!/usr/bin/env python3
"""werkelijk_gegevens OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Uitvoeren_opdracht import Taken_wortel, opdracht
from brug_3de4fe3a import brug_3de4fe3a


def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Taken_wortel / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Taken_wortel / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Taken_wortel / 'build/verification/native-remote')
    argumenten = parser_48ee4b1b.parse_args()
    tekstuitvoer = argumenten.output
    tekstuitvoer.mkdir(parents=True, exist_ok=True)
    Instellingen = json.loads(argumenten.access.read_text())
    Rapport_WAARDE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumenten.kernel.read_bytes()).hexdigest(), 'checks': []}
    def leeg_poort():
        with socket.socket() as Verbinden:
            Verbinden.bind(('127.0.0.5', 0))
            return Verbinden.getsockname()[1]
    Shell_poort, scherm_poort, bestandspoort = leeg_poort(), leeg_poort(), leeg_poort()
    LOG_RECORD = bytearray()
    Proces_WAARDE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, brug_3de4fe3a(bestandspoort,
                ['tcp:{}:22'.format(Shell_poort), 'tcp:{}:5900'.format(scherm_poort)], host_ADRES='127.0.0.5') as brug_WAARDE:
            실행인수 = opdracht()
            실행인수[실행인수.index('-kernel') + 1] = str(argumenten.kernel.resolve())
            Proces_WAARDE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + brug_WAARDE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    gegevens = Proces_WAARDE.stdout.read(4096)
                    if not gegevens: break
                    LOG_RECORD.extend(gegevens)
            thread_WAARDE = threading.Thread(target=수집, daemon=True)
            thread_WAARDE.start()
            def wachtstatus(Word_sms, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_sms not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Proces_WAARDE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_sms)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            wachtstatus(b'jkoros-native> ')
            helper_WAARDE = Path(임시)/'askpass'
            helper_WAARDE.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            helper_WAARDE.chmod(0o700)
            omgeving = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(helper_WAARDE), SSH_ASKPASS_REQUIRE='force')
            def veilig_Shell(wachtwoord_WAARDE, instructie_WAARDE, toevoegen_invoer=()):
                omgeving['JKOROS_TEST_PASSWORD']=wachtwoord_WAARDE
                argumenten=['ssh','-v']+list(toevoegen_invoer)+['-p',str(Shell_poort),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instructie_WAARDE]
                resultaat=subprocess.run(argumenten,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=omgeving,start_new_session=True,timeout=50)
                return resultaat
            resultaat=veilig_Shell('!' + Instellingen['ssh_password'], 'echo SHOULD_NOT_RUN')
            (tekstuitvoer/'ssh-rejected.log').write_bytes(resultaat.stderr)
            assert resultaat.returncode!=0 and b'Permission denied' in resultaat.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, resultaat.stderr
            Rapport_WAARDE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            resultaat=veilig_Shell(Instellingen['ssh_password'], 'echo SSH_NATIVE_PASS')
            (tekstuitvoer/'ssh.log').write_bytes(resultaat.stderr)
            (tekstuitvoer/'ssh-output.txt').write_bytes(resultaat.stdout)
            assert resultaat.returncode==0 and b'SSH_NATIVE_PASS' in resultaat.stdout, (resultaat.returncode,resultaat.stdout,resultaat.stderr)
            Rapport_WAARDE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in resultaat.stderr, resultaat.stderr
            Rapport_WAARDE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            resultaat=veilig_Shell(Instellingen['ssh_password'], 'cd /example/java; java Uitvoervoorbeeld; cd /')
            assert resultaat.returncode==0 and 'JAVA tekstuitvoer: 안녕하세요 😀'.encode() in resultaat.stdout,resultaat.stdout
            Rapport_WAARDE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            resultaat=veilig_Shell(Instellingen['ssh_password'], 'missing_remote_command')
            assert resultaat.returncode==127,resultaat.returncode
            Rapport_WAARDE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            resultaat=veilig_Shell(Instellingen['ssh_password'], 'cat /example/java/Venstervoorbeeld.java', ('-o', 'RekeyLimit=1K'))
            (tekstuitvoer/'ssh-rekey.log').write_bytes(resultaat.stderr)
            assert resultaat.returncode==0 and 'class Venstervoorbeeld'.encode() in resultaat.stdout, (resultaat.returncode,resultaat.stdout,resultaat.stderr)
            assert resultaat.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, resultaat.stderr
            Rapport_WAARDE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_poort),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interactief_sessie=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=omgeving,start_new_session=True,bufsize=0)
            transcriptie=bytearray();selectie_WAARDE=selectors.DefaultSelector();selectie_WAARDE.register(interactief_sessie.stdout,selectors.EVENT_READ)
            def 대화읽기(weergeven_WAARDE):
                deadline_WAARDE=time.monotonic()+30
                while weergeven_WAARDE not in transcriptie:
                    if time.monotonic()>deadline_WAARDE or interactief_sessie.poll() is not None:raise AssertionError('SSH interactive missing '+repr(weergeven_WAARDE)+' '+repr(bytes(transcriptie)))
                    for invoer_WAARDE_962f286b,_ in selectie_WAARDE.select(.1):
                        조각=invoer_WAARDE_962f286b.fileobj.read(4096)
                        if 조각:transcriptie.extend(조각)
            try:
                대화읽기(b'shared native console')
                interactief_sessie.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interactief_sessie.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interactief_sessie.stdin.write(b'\x04');interactief_sessie.stdin.flush();나머지,fout=interactief_sessie.communicate(timeout=15)
                assert interactief_sessie.returncode==0 and b'PTY allocation request failed' not in fout,(interactief_sessie.returncode,fout)
                (tekstuitvoer/'ssh-interactive.txt').write_bytes(transcriptie+나머지)
            finally:
                selectie_WAARDE.close()
                if interactief_sessie.poll() is None:interactief_sessie.kill();interactief_sessie.wait()
            Rapport_WAARDE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Verbinden, nummer):
                gegevens=bytearray()
                while len(gegevens)<nummer:
                    chunk_WAARDE=Verbinden.recv(nummer-len(gegevens))
                    if not chunk_WAARDE: raise AssertionError('RFB EOF')
                    gegevens.extend(chunk_WAARDE)
                return bytes(gegevens)
            def scherm_verificatie(wachtwoord_WAARDE):
                Verbinden=socket.create_connection(('127.0.0.5',scherm_poort),10);Verbinden.settimeout(30)
                assert 정확히(Verbinden,12)==b'RFB 003.008\n'
                Verbinden.sendall(b'RFB 003.008\n');assert 정확히(Verbinden,2)==b'\x01\x02'
                Verbinden.sendall(b'\x02');vraag_WAARDE=정확히(Verbinden,16)
                invoer_wachtwoord=wachtwoord_WAARDE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(nummer)[::-1],2) for nummer in invoer_wachtwoord)
                Verbinden.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(vraag_WAARDE))
                Status_WAARDE=struct.unpack('!I',정확히(Verbinden,4))[0]
                return Verbinden,Status_WAARDE
            nietig_wachtwoord='!' if not Instellingen['vnc_password'].startswith('!') else '?'
            Verbinden,Status_WAARDE=scherm_verificatie(nietig_wachtwoord);assert Status_WAARDE==1;Verbinden.close();time.sleep(.6)
            Rapport_WAARDE['checks'].append('VNC incorrect password rejected')
            Verbinden,Status_WAARDE=scherm_verificatie(Instellingen['vnc_password']);assert Status_WAARDE==0
            with Verbinden:
                Verbinden.sendall(b'\x01');begintoestand=정확히(Verbinden,24);너비,hoogte_WAARDE=struct.unpack('!HH',begintoestand[:4]);Naam=정확히(Verbinden,struct.unpack('!I',begintoestand[20:24])[0])
                assert (너비,hoogte_WAARDE)==(640,480) and b'jkoros native'==Naam
                def scherm(toename_stap=0):
                    Verbinden.sendall(struct.pack('!BBHHHH',3,toename_stap,0,0,너비,hoogte_WAARDE));kop_WAARDE=정확히(Verbinden,4);nummer=struct.unpack('!H',kop_WAARDE[2:])[0];totaal_WAARDE=0
                    tekening_WAARDE=bytearray(너비*hoogte_WAARDE*4)
                    for _ in range(nummer):
                        x_coördinaat,Y_coördinaat,영역너비,regio_hoogte,methode_MODUS=struct.unpack('!HHHHi',정확히(Verbinden,12));assert methode_MODUS==0 and x_coördinaat+영역너비<=너비 and Y_coördinaat+regio_hoogte<=hoogte_WAARDE
                        pixel=정확히(Verbinden,영역너비*regio_hoogte*4);totaal_WAARDE+=len(pixel)
                        for invoerregel in range(regio_hoogte):tekening_WAARDE[((Y_coördinaat+invoerregel)*너비+x_coördinaat)*4:((Y_coördinaat+invoerregel)*너비+x_coördinaat+영역너비)*4]=pixel[invoerregel*영역너비*4:(invoerregel+1)*영역너비*4]
                    if not toename_stap:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,hoogte_WAARDE),bytes(tekening_WAARDE),'raw','BGRX').save(str(tekstuitvoer/'native-vnc.png'))
                    return nummer,totaal_WAARDE
                nummer,totaal_WAARDE=scherm();assert nummer>0 and totaal_WAARDE==너비*hoogte_WAARDE*4
                Rapport_WAARDE['checks'].append('Native framebuffer RFB full update {} bytes'.format(totaal_WAARDE))
                nummer,totaal_WAARDE=scherm(1);assert totaal_WAARDE<너비*hoogte_WAARDE*4
                Rapport_WAARDE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for teken_WAARDE in 'echo VNC_NATIVE_PASS\r':
                    symbool=0xff0d if teken_WAARDE=='\r' else ord(teken_WAARDE)
                    Verbinden.sendall(struct.pack('!BBHI',4,1,0,symbool));Verbinden.sendall(struct.pack('!BBHI',4,0,0,symbool))
                wachtstatus(b'VNC_NATIVE_PASS',처음)
                Rapport_WAARDE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def toets_kwaststreek(symbool,누름=1):Verbinden.sendall(struct.pack('!BBHI',4,누름,0,symbool))
                처음=len(LOG_RECORD)
                for teken_WAARDE in 'echo ':toets_kwaststreek(ord(teken_WAARDE))
                toets_kwaststreek(0xffc6)
                for teken_WAARDE in 'gksrmf':toets_kwaststreek(ord(teken_WAARDE))
                toets_kwaststreek(0xffc6);toets_kwaststreek(0xff0d)
                wachtstatus('\r\n한글\r\n'.encode(),처음)
                Rapport_WAARDE['checks'].append('Native VNC F9 two-set Hangul composition')
                Verbinden.sendall(struct.pack('!BBHH',5,0,120,100))
                Rapport_WAARDE['checks'].append('VNC pointer input accepted')
            Proces_WAARDE.stdin.write(b'poweroff\n');Proces_WAARDE.stdin.flush();Proces_WAARDE.wait(timeout=15);assert Proces_WAARDE.returncode==0
            Rapport_WAARDE['passed']=True
    finally:
        if Proces_WAARDE and Proces_WAARDE.poll() is None:
            Proces_WAARDE.terminate()
            try: Proces_WAARDE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_WAARDE.kill();Proces_WAARDE.wait()
        (tekstuitvoer/'serial.log').write_bytes(LOG_RECORD)
        (tekstuitvoer/'report.json').write_text(json.dumps(Rapport_WAARDE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Rapport_WAARDE,ensure_ascii=False,indent=2))


if __name__=='__main__': starten()
