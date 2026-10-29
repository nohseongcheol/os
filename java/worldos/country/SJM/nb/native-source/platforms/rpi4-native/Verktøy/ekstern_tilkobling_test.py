#!/usr/bin/env python3
"""faktisk_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Utfør_kommando import speile_rot, Kommando
from bro_3de4fe3a import bro_3de4fe3a


def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=speile_rot / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=speile_rot / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=speile_rot / 'build/verification/native-remote')
    Argumenter = parser_48ee4b1b.parse_args()
    Utgang = Argumenter.output
    Utgang.mkdir(parents=True, exist_ok=True)
    Innstillinger = json.loads(Argumenter.access.read_text())
    rapport_VERDI = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenter.kernel.read_bytes()).hexdigest(), 'checks': []}
    def tom_port():
        with socket.socket() as Koble_til:
            Koble_til.bind(('127.0.0.5', 0))
            return Koble_til.getsockname()[1]
    Shell_port, skjermbilde_port, filport = tom_port(), tom_port(), tom_port()
    LOG_POST = bytearray()
    Prosess_VERDI = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, bro_3de4fe3a(filport,
                ['tcp:{}:22'.format(Shell_port), 'tcp:{}:5900'.format(skjermbilde_port)], vert_e_post='127.0.0.5') as bro_VERDI:
            실행인수 = Kommando()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenter.kernel.resolve())
            Prosess_VERDI = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bro_VERDI.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Prosess_VERDI.stdout.read(4096)
                    if not data: break
                    LOG_POST.extend(data)
            tråd_VERDI = threading.Thread(target=수집, daemon=True)
            tråd_VERDI.start()
            def ventende_tilstand(ord_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ord_SMS not in LOG_POST[처음:]:
                    if time.monotonic()>끝 or Prosess_VERDI.poll() is not None:
                        raise AssertionError('Missing '+repr(ord_SMS)+'\n'+LOG_POST[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ventende_tilstand(b'jkoros-native> ')
            hjelper_VERDI = Path(임시)/'askpass'
            hjelper_VERDI.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            hjelper_VERDI.chmod(0o700)
            miljø = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(hjelper_VERDI), SSH_ASKPASS_REQUIRE='force')
            def sikker_Shell(passord_VERDI, 명령어, Tilføye_oppføring=()):
                miljø['JKOROS_TEST_PASSWORD']=passord_VERDI
                Argumenter=['ssh','-v']+list(Tilføye_oppføring)+['-p',str(Shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                KR=subprocess.run(Argumenter,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=miljø,start_new_session=True,timeout=50)
                return KR
            KR=sikker_Shell('!' + Innstillinger['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Utgang/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_POST, KR.stderr
            rapport_VERDI['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=sikker_Shell(Innstillinger['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Utgang/'ssh.log').write_bytes(KR.stderr)
            (Utgang/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            rapport_VERDI['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            rapport_VERDI['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=sikker_Shell(Innstillinger['ssh_password'], 'cd /example/java; java Utdataeksempel; cd /')
            assert KR.returncode==0 and 'JAVA Utgang: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            rapport_VERDI['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=sikker_Shell(Innstillinger['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            rapport_VERDI['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=sikker_Shell(Innstillinger['ssh_password'], 'cat /example/java/Vinduseksempel.java', ('-o', 'RekeyLimit=1K'))
            (Utgang/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class Vinduseksempel'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            rapport_VERDI['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_økt=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=miljø,start_new_session=True,bufsize=0)
            utskrift=bytearray();merket_område_VERDI=selectors.DefaultSelector();merket_område_VERDI.register(interaktiv_økt.stdout,selectors.EVENT_READ)
            def 대화읽기(vise_VERDI_487749b8):
                tidsfrist_VERDI=time.monotonic()+30
                while vise_VERDI_487749b8 not in utskrift:
                    if time.monotonic()>tidsfrist_VERDI or interaktiv_økt.poll() is not None:raise AssertionError('SSH interactive missing '+repr(vise_VERDI_487749b8)+' '+repr(bytes(utskrift)))
                    for oppføring_VERDI,_ in merket_område_VERDI.select(.1):
                        조각=oppføring_VERDI.fileobj.read(4096)
                        if 조각:utskrift.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiv_økt.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_økt.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_økt.stdin.write(b'\x04');interaktiv_økt.stdin.flush();나머지,feil=interaktiv_økt.communicate(timeout=15)
                assert interaktiv_økt.returncode==0 and b'PTY allocation request failed' not in feil,(interaktiv_økt.returncode,feil)
                (Utgang/'ssh-interactive.txt').write_bytes(utskrift+나머지)
            finally:
                merket_område_VERDI.close()
                if interaktiv_økt.poll() is None:interaktiv_økt.kill();interaktiv_økt.wait()
            rapport_VERDI['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Koble_til, nummer):
                data=bytearray()
                while len(data)<nummer:
                    덩이=Koble_til.recv(nummer-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def skjermbilde_godkjenning(passord_VERDI):
                Koble_til=socket.create_connection(('127.0.0.5',skjermbilde_port),10);Koble_til.settimeout(30)
                assert 정확히(Koble_til,12)==b'RFB 003.008\n'
                Koble_til.sendall(b'RFB 003.008\n');assert 정확히(Koble_til,2)==b'\x01\x02'
                Koble_til.sendall(b'\x02');utfordring_VERDI=정확히(Koble_til,16)
                inndata_passord=passord_VERDI.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(nummer)[::-1],2) for nummer in inndata_passord)
                Koble_til.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(utfordring_VERDI))
                status_VERDI=struct.unpack('!I',정확히(Koble_til,4))[0]
                return Koble_til,status_VERDI
            ugyldig_passord='!' if not Innstillinger['vnc_password'].startswith('!') else '?'
            Koble_til,status_VERDI=skjermbilde_godkjenning(ugyldig_passord);assert status_VERDI==1;Koble_til.close();time.sleep(.6)
            rapport_VERDI['checks'].append('VNC incorrect password rejected')
            Koble_til,status_VERDI=skjermbilde_godkjenning(Innstillinger['vnc_password']);assert status_VERDI==0
            with Koble_til:
                Koble_til.sendall(b'\x01');opprinnelig_tilstand=정확히(Koble_til,24);너비,높이=struct.unpack('!HH',opprinnelig_tilstand[:4]);Navn=정확히(Koble_til,struct.unpack('!I',opprinnelig_tilstand[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Navn
                def skjermbilde(øke_trinnvis_trinn=0):
                    Koble_til.sendall(struct.pack('!BBHHHH',3,øke_trinnvis_trinn,0,0,너비,높이));머리=정확히(Koble_til,4);nummer=struct.unpack('!H',머리[2:])[0];total_VERDI=0
                    tegning_VERDI=bytearray(너비*높이*4)
                    for _ in range(nummer):
                        x_koordinat,Y_koordinat,영역너비,영역높이,metode_MODUS=struct.unpack('!HHHHi',정확히(Koble_til,12));assert metode_MODUS==0 and x_koordinat+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        piksel=정확히(Koble_til,영역너비*영역높이*4);total_VERDI+=len(piksel)
                        for Linje in range(영역높이):tegning_VERDI[((Y_koordinat+Linje)*너비+x_koordinat)*4:((Y_koordinat+Linje)*너비+x_koordinat+영역너비)*4]=piksel[Linje*영역너비*4:(Linje+1)*영역너비*4]
                    if not øke_trinnvis_trinn:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(tegning_VERDI),'raw','BGRX').save(str(Utgang/'native-vnc.png'))
                    return nummer,total_VERDI
                nummer,total_VERDI=skjermbilde();assert nummer>0 and total_VERDI==너비*높이*4
                rapport_VERDI['checks'].append('Native framebuffer RFB full update {} bytes'.format(total_VERDI))
                nummer,total_VERDI=skjermbilde(1);assert total_VERDI<너비*높이*4
                rapport_VERDI['checks'].append('RFB incremental update')
                처음=len(LOG_POST)
                for tegn_VERDI in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if tegn_VERDI=='\r' else ord(tegn_VERDI)
                    Koble_til.sendall(struct.pack('!BBHI',4,1,0,symbol));Koble_til.sendall(struct.pack('!BBHI',4,0,0,symbol))
                ventende_tilstand(b'VNC_NATIVE_PASS',처음)
                rapport_VERDI['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def tast_pennestrøk(symbol,누름=1):Koble_til.sendall(struct.pack('!BBHI',4,누름,0,symbol))
                처음=len(LOG_POST)
                for tegn_VERDI in 'echo ':tast_pennestrøk(ord(tegn_VERDI))
                tast_pennestrøk(0xffc6)
                for tegn_VERDI in 'gksrmf':tast_pennestrøk(ord(tegn_VERDI))
                tast_pennestrøk(0xffc6);tast_pennestrøk(0xff0d)
                ventende_tilstand('\r\n한글\r\n'.encode(),처음)
                rapport_VERDI['checks'].append('Native VNC F9 two-set Hangul composition')
                Koble_til.sendall(struct.pack('!BBHH',5,0,120,100))
                rapport_VERDI['checks'].append('VNC pointer input accepted')
            Prosess_VERDI.stdin.write(b'poweroff\n');Prosess_VERDI.stdin.flush();Prosess_VERDI.wait(timeout=15);assert Prosess_VERDI.returncode==0
            rapport_VERDI['passed']=True
    finally:
        if Prosess_VERDI and Prosess_VERDI.poll() is None:
            Prosess_VERDI.terminate()
            try: Prosess_VERDI.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess_VERDI.kill();Prosess_VERDI.wait()
        (Utgang/'serial.log').write_bytes(LOG_POST)
        (Utgang/'report.json').write_text(json.dumps(rapport_VERDI,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(rapport_VERDI,ensure_ascii=False,indent=2))


if __name__=='__main__': Kjør_2()
