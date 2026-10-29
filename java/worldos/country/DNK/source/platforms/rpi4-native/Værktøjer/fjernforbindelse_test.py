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
from Udfør_kommando import To_do_rod, Kommando
from bro_3de4fe3a import bro_3de4fe3a


def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=To_do_rod / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=To_do_rod / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=To_do_rod / 'build/verification/native-remote')
    Argumenter = parser_48ee4b1b.parse_args()
    Udgang = Argumenter.output
    Udgang.mkdir(parents=True, exist_ok=True)
    Indstillinger = json.loads(Argumenter.access.read_text())
    rapport_VÆRDI = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumenter.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Tilslut:
            Tilslut.bind(('127.0.0.5', 0))
            return Tilslut.getsockname()[1]
    Shell_port, skærmbillede_port, filport = 빈포트(), 빈포트(), 빈포트()
    LOG_post = bytearray()
    Proces_VÆRDI = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, bro_3de4fe3a(filport,
                ['tcp:{}:22'.format(Shell_port), 'tcp:{}:5900'.format(skærmbillede_port)], vært_mail='127.0.0.5') as bro_VÆRDI:
            실행인수 = Kommando()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumenter.kernel.resolve())
            Proces_VÆRDI = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bro_VÆRDI.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proces_VÆRDI.stdout.read(4096)
                    if not data: break
                    LOG_post.extend(data)
            tråd_VÆRDI = threading.Thread(target=수집, daemon=True)
            tråd_VÆRDI.start()
            def ventetilstand(Ord_sms, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Ord_sms not in LOG_post[처음:]:
                    if time.monotonic()>끝 or Proces_VÆRDI.poll() is not None:
                        raise AssertionError('Missing '+repr(Ord_sms)+'\n'+LOG_post[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ventetilstand(b'jkoros-native> ')
            hjælper_VÆRDI = Path(임시)/'askpass'
            hjælper_VÆRDI.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            hjælper_VÆRDI.chmod(0o700)
            miljø = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(hjælper_VÆRDI), SSH_ASKPASS_REQUIRE='force')
            def sikker_Shell(adgangskode_VÆRDI, 명령어, tilføj_post=()):
                miljø['JKOROS_TEST_PASSWORD']=adgangskode_VÆRDI
                Argumenter=['ssh','-v']+list(tilføj_post)+['-p',str(Shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                KR=subprocess.run(Argumenter,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=miljø,start_new_session=True,timeout=50)
                return KR
            KR=sikker_Shell('!' + Indstillinger['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Udgang/'ssh-rejected.log').write_bytes(KR.stderr)
            assert KR.returncode!=0 and b'Permission denied' in KR.stderr and b'SHOULD_NOT_RUN' not in LOG_post, KR.stderr
            rapport_VÆRDI['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            KR=sikker_Shell(Indstillinger['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Udgang/'ssh.log').write_bytes(KR.stderr)
            (Udgang/'ssh-output.txt').write_bytes(KR.stdout)
            assert KR.returncode==0 and b'SSH_NATIVE_PASS' in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            rapport_VÆRDI['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in KR.stderr, KR.stderr
            rapport_VÆRDI['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            KR=sikker_Shell(Indstillinger['ssh_password'], 'cd /example/java; java Uddataeksempel; cd /')
            assert KR.returncode==0 and 'JAVA Udgang: 안녕하세요 😀'.encode() in KR.stdout,KR.stdout
            rapport_VÆRDI['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            KR=sikker_Shell(Indstillinger['ssh_password'], 'missing_remote_command')
            assert KR.returncode==127,KR.returncode
            rapport_VÆRDI['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            KR=sikker_Shell(Indstillinger['ssh_password'], 'cat /example/java/Vindueseksempel.java', ('-o', 'RekeyLimit=1K'))
            (Udgang/'ssh-rekey.log').write_bytes(KR.stderr)
            assert KR.returncode==0 and 'class Vindueseksempel'.encode() in KR.stdout, (KR.returncode,KR.stdout,KR.stderr)
            assert KR.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, KR.stderr
            rapport_VÆRDI['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_session=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=miljø,start_new_session=True,bufsize=0)
            afskrift=bytearray();markering_VÆRDI=selectors.DefaultSelector();markering_VÆRDI.register(interaktiv_session.stdout,selectors.EVENT_READ)
            def 대화읽기(vise_VÆRDI):
                deadline_VÆRDI=time.monotonic()+30
                while vise_VÆRDI not in afskrift:
                    if time.monotonic()>deadline_VÆRDI or interaktiv_session.poll() is not None:raise AssertionError('SSH interactive missing '+repr(vise_VÆRDI)+' '+repr(bytes(afskrift)))
                    for post_VÆRDI_962f286b,_ in markering_VÆRDI.select(.1):
                        조각=post_VÆRDI_962f286b.fileobj.read(4096)
                        if 조각:afskrift.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiv_session.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_session.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_session.stdin.write(b'\x04');interaktiv_session.stdin.flush();나머지,fejl=interaktiv_session.communicate(timeout=15)
                assert interaktiv_session.returncode==0 and b'PTY allocation request failed' not in fejl,(interaktiv_session.returncode,fejl)
                (Udgang/'ssh-interactive.txt').write_bytes(afskrift+나머지)
            finally:
                markering_VÆRDI.close()
                if interaktiv_session.poll() is None:interaktiv_session.kill();interaktiv_session.wait()
            rapport_VÆRDI['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Tilslut, tal):
                data=bytearray()
                while len(data)<tal:
                    del_VÆRDI=Tilslut.recv(tal-len(data))
                    if not del_VÆRDI: raise AssertionError('RFB EOF')
                    data.extend(del_VÆRDI)
                return bytes(data)
            def skærmbillede_godkendelse(adgangskode_VÆRDI):
                Tilslut=socket.create_connection(('127.0.0.5',skærmbillede_port),10);Tilslut.settimeout(30)
                assert 정확히(Tilslut,12)==b'RFB 003.008\n'
                Tilslut.sendall(b'RFB 003.008\n');assert 정확히(Tilslut,2)==b'\x01\x02'
                Tilslut.sendall(b'\x02');udfordring_VÆRDI=정확히(Tilslut,16)
                input_adgangskode=adgangskode_VÆRDI.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(tal)[::-1],2) for tal in input_adgangskode)
                Tilslut.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(udfordring_VÆRDI))
                status_VÆRDI=struct.unpack('!I',정확히(Tilslut,4))[0]
                return Tilslut,status_VÆRDI
            ugyldig_adgangskode='!' if not Indstillinger['vnc_password'].startswith('!') else '?'
            Tilslut,status_VÆRDI=skærmbillede_godkendelse(ugyldig_adgangskode);assert status_VÆRDI==1;Tilslut.close();time.sleep(.6)
            rapport_VÆRDI['checks'].append('VNC incorrect password rejected')
            Tilslut,status_VÆRDI=skærmbillede_godkendelse(Indstillinger['vnc_password']);assert status_VÆRDI==0
            with Tilslut:
                Tilslut.sendall(b'\x01');starttilstand=정확히(Tilslut,24);너비,높이=struct.unpack('!HH',starttilstand[:4]);Navn=정확히(Tilslut,struct.unpack('!I',starttilstand[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Navn
                def skærmbillede(gradvis_forøgelse_trin=0):
                    Tilslut.sendall(struct.pack('!BBHHHH',3,gradvis_forøgelse_trin,0,0,너비,높이));머리=정확히(Tilslut,4);tal=struct.unpack('!H',머리[2:])[0];i_alt_VÆRDI=0
                    tegning_VÆRDI=bytearray(너비*높이*4)
                    for _ in range(tal):
                        X_koordinat,Y_koordinat,영역너비,영역높이,metode_HYPPIGST=struct.unpack('!HHHHi',정확히(Tilslut,12));assert metode_HYPPIGST==0 and X_koordinat+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        pixel=정확히(Tilslut,영역너비*영역높이*4);i_alt_VÆRDI+=len(pixel)
                        for Linje in range(영역높이):tegning_VÆRDI[((Y_koordinat+Linje)*너비+X_koordinat)*4:((Y_koordinat+Linje)*너비+X_koordinat+영역너비)*4]=pixel[Linje*영역너비*4:(Linje+1)*영역너비*4]
                    if not gradvis_forøgelse_trin:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(tegning_VÆRDI),'raw','BGRX').save(str(Udgang/'native-vnc.png'))
                    return tal,i_alt_VÆRDI
                tal,i_alt_VÆRDI=skærmbillede();assert tal>0 and i_alt_VÆRDI==너비*높이*4
                rapport_VÆRDI['checks'].append('Native framebuffer RFB full update {} bytes'.format(i_alt_VÆRDI))
                tal,i_alt_VÆRDI=skærmbillede(1);assert i_alt_VÆRDI<너비*높이*4
                rapport_VÆRDI['checks'].append('RFB incremental update')
                처음=len(LOG_post)
                for tegn_VÆRDI in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if tegn_VÆRDI=='\r' else ord(tegn_VÆRDI)
                    Tilslut.sendall(struct.pack('!BBHI',4,1,0,symbol));Tilslut.sendall(struct.pack('!BBHI',4,0,0,symbol))
                ventetilstand(b'VNC_NATIVE_PASS',처음)
                rapport_VÆRDI['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def tast_pennestrøg(symbol,누름=1):Tilslut.sendall(struct.pack('!BBHI',4,누름,0,symbol))
                처음=len(LOG_post)
                for tegn_VÆRDI in 'echo ':tast_pennestrøg(ord(tegn_VÆRDI))
                tast_pennestrøg(0xffc6)
                for tegn_VÆRDI in 'gksrmf':tast_pennestrøg(ord(tegn_VÆRDI))
                tast_pennestrøg(0xffc6);tast_pennestrøg(0xff0d)
                ventetilstand('\r\n한글\r\n'.encode(),처음)
                rapport_VÆRDI['checks'].append('Native VNC F9 two-set Hangul composition')
                Tilslut.sendall(struct.pack('!BBHH',5,0,120,100))
                rapport_VÆRDI['checks'].append('VNC pointer input accepted')
            Proces_VÆRDI.stdin.write(b'poweroff\n');Proces_VÆRDI.stdin.flush();Proces_VÆRDI.wait(timeout=15);assert Proces_VÆRDI.returncode==0
            rapport_VÆRDI['passed']=True
    finally:
        if Proces_VÆRDI and Proces_VÆRDI.poll() is None:
            Proces_VÆRDI.terminate()
            try: Proces_VÆRDI.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VÆRDI.kill();Proces_VÆRDI.wait()
        (Udgang/'serial.log').write_bytes(LOG_post)
        (Udgang/'report.json').write_text(json.dumps(rapport_VÆRDI,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(rapport_VÆRDI,ensure_ascii=False,indent=2))


if __name__=='__main__': Kør_2()
