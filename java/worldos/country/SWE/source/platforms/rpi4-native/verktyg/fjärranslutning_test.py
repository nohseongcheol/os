#!/usr/bin/env python3
"""verklig_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from köra_kommando import åtgärd_rot, kommando
from brygga_3de4fe3a import brygga_3de4fe3a


def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=åtgärd_rot / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=åtgärd_rot / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=åtgärd_rot / 'build/verification/native-remote')
    argument = parser_48ee4b1b.parse_args()
    utmatningsposition = argument.output
    utmatningsposition.mkdir(parents=True, exist_ok=True)
    Inställningar = json.loads(argument.access.read_text())
    Rapport_värde = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argument.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Anslut:
            Anslut.bind(('127.0.0.5', 0))
            return Anslut.getsockname()[1]
    Shell_port, skärmbild_port, filport = 빈포트(), 빈포트(), 빈포트()
    LOG_POST = bytearray()
    Process_värde = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, brygga_3de4fe3a(filport,
                ['tcp:{}:22'.format(Shell_port), 'tcp:{}:5900'.format(skärmbild_port)], värd_ADRESS='127.0.0.5') as brygga_värde:
            실행인수 = kommando()
            실행인수[실행인수.index('-kernel') + 1] = str(argument.kernel.resolve())
            Process_värde = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + brygga_värde.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Process_värde.stdout.read(4096)
                    if not data: break
                    LOG_POST.extend(data)
            tråd_värde = threading.Thread(target=수집, daemon=True)
            tråd_värde.start()
            def tillståndet_Vänta(Ord_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Ord_SMS not in LOG_POST[처음:]:
                    if time.monotonic()>끝 or Process_värde.poll() is not None:
                        raise AssertionError('Missing '+repr(Ord_SMS)+'\n'+LOG_POST[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            tillståndet_Vänta(b'jkoros-native> ')
            hjälpkomponent_värde = Path(임시)/'askpass'
            hjälpkomponent_värde.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            hjälpkomponent_värde.chmod(0o700)
            miljö = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(hjälpkomponent_värde), SSH_ASKPASS_REQUIRE='force')
            def säker_Shell(lösenord_värde, instruktion_värde, Lägga_till_post=()):
                miljö['JKOROS_TEST_PASSWORD']=lösenord_värde
                argument=['ssh','-v']+list(Lägga_till_post)+['-p',str(Shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruktion_värde]
                RESULTAT=subprocess.run(argument,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=miljö,start_new_session=True,timeout=50)
                return RESULTAT
            RESULTAT=säker_Shell('!' + Inställningar['ssh_password'], 'echo SHOULD_NOT_RUN')
            (utmatningsposition/'ssh-rejected.log').write_bytes(RESULTAT.stderr)
            assert RESULTAT.returncode!=0 and b'Permission denied' in RESULTAT.stderr and b'SHOULD_NOT_RUN' not in LOG_POST, RESULTAT.stderr
            Rapport_värde['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            RESULTAT=säker_Shell(Inställningar['ssh_password'], 'echo SSH_NATIVE_PASS')
            (utmatningsposition/'ssh.log').write_bytes(RESULTAT.stderr)
            (utmatningsposition/'ssh-output.txt').write_bytes(RESULTAT.stdout)
            assert RESULTAT.returncode==0 and b'SSH_NATIVE_PASS' in RESULTAT.stdout, (RESULTAT.returncode,RESULTAT.stdout,RESULTAT.stderr)
            Rapport_värde['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in RESULTAT.stderr, RESULTAT.stderr
            Rapport_värde['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            RESULTAT=säker_Shell(Inställningar['ssh_password'], 'cd /example/java; java Utdataexempel; cd /')
            assert RESULTAT.returncode==0 and 'JAVA utmatningsposition: 안녕하세요 😀'.encode() in RESULTAT.stdout,RESULTAT.stdout
            Rapport_värde['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            RESULTAT=säker_Shell(Inställningar['ssh_password'], 'missing_remote_command')
            assert RESULTAT.returncode==127,RESULTAT.returncode
            Rapport_värde['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            RESULTAT=säker_Shell(Inställningar['ssh_password'], 'cat /example/java/Fönsterexempel.java', ('-o', 'RekeyLimit=1K'))
            (utmatningsposition/'ssh-rekey.log').write_bytes(RESULTAT.stderr)
            assert RESULTAT.returncode==0 and 'class Fönsterexempel'.encode() in RESULTAT.stdout, (RESULTAT.returncode,RESULTAT.stdout,RESULTAT.stderr)
            assert RESULTAT.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, RESULTAT.stderr
            Rapport_värde['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_session=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=miljö,start_new_session=True,bufsize=0)
            avskrift=bytearray();markering_värde=selectors.DefaultSelector();markering_värde.register(interaktiv_session.stdout,selectors.EVENT_READ)
            def läsa_interaktiv(visa_värde):
                måldatum_värde=time.monotonic()+30
                while visa_värde not in avskrift:
                    if time.monotonic()>måldatum_värde or interaktiv_session.poll() is not None:raise AssertionError('SSH interactive missing '+repr(visa_värde)+' '+repr(bytes(avskrift)))
                    for post_värde,_ in markering_värde.select(.1):
                        조각=post_värde.fileobj.read(4096)
                        if 조각:avskrift.extend(조각)
            try:
                läsa_interaktiv(b'shared native console')
                interaktiv_session.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_session.stdin.flush();läsa_interaktiv(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_session.stdin.write(b'\x04');interaktiv_session.stdin.flush();나머지,fel=interaktiv_session.communicate(timeout=15)
                assert interaktiv_session.returncode==0 and b'PTY allocation request failed' not in fel,(interaktiv_session.returncode,fel)
                (utmatningsposition/'ssh-interactive.txt').write_bytes(avskrift+나머지)
            finally:
                markering_värde.close()
                if interaktiv_session.poll() is None:interaktiv_session.kill();interaktiv_session.wait()
            Rapport_värde['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Anslut, nummer):
                data=bytearray()
                while len(data)<nummer:
                    segment_värde=Anslut.recv(nummer-len(data))
                    if not segment_värde: raise AssertionError('RFB EOF')
                    data.extend(segment_värde)
                return bytes(data)
            def skärmbild_autentisering(lösenord_värde):
                Anslut=socket.create_connection(('127.0.0.5',skärmbild_port),10);Anslut.settimeout(30)
                assert 정확히(Anslut,12)==b'RFB 003.008\n'
                Anslut.sendall(b'RFB 003.008\n');assert 정확히(Anslut,2)==b'\x01\x02'
                Anslut.sendall(b'\x02');kontroll_värde_c2a235ad=정확히(Anslut,16)
                indata_lösenord=lösenord_värde.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(nummer)[::-1],2) for nummer in indata_lösenord)
                Anslut.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(kontroll_värde_c2a235ad))
                status_värde=struct.unpack('!I',정확히(Anslut,4))[0]
                return Anslut,status_värde
            ogiltig_lösenord='!' if not Inställningar['vnc_password'].startswith('!') else '?'
            Anslut,status_värde=skärmbild_autentisering(ogiltig_lösenord);assert status_värde==1;Anslut.close();time.sleep(.6)
            Rapport_värde['checks'].append('VNC incorrect password rejected')
            Anslut,status_värde=skärmbild_autentisering(Inställningar['vnc_password']);assert status_värde==0
            with Anslut:
                Anslut.sendall(b'\x01');starttillstånd=정확히(Anslut,24);너비,높이=struct.unpack('!HH',starttillstånd[:4]);Namn=정확히(Anslut,struct.unpack('!I',starttillstånd[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Namn
                def skärmbild(inkrement_steg=0):
                    Anslut.sendall(struct.pack('!BBHHHH',3,inkrement_steg,0,0,너비,높이));머리=정확히(Anslut,4);nummer=struct.unpack('!H',머리[2:])[0];summa_värde=0
                    ritning_värde=bytearray(너비*높이*4)
                    for _ in range(nummer):
                        x_koordinat,Y_koordinat,영역너비,영역높이,metod_läge=struct.unpack('!HHHHi',정확히(Anslut,12));assert metod_läge==0 and x_koordinat+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        bildpunkt=정확히(Anslut,영역너비*영역높이*4);summa_värde+=len(bildpunkt)
                        for inmatningsrad in range(영역높이):ritning_värde[((Y_koordinat+inmatningsrad)*너비+x_koordinat)*4:((Y_koordinat+inmatningsrad)*너비+x_koordinat+영역너비)*4]=bildpunkt[inmatningsrad*영역너비*4:(inmatningsrad+1)*영역너비*4]
                    if not inkrement_steg:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ritning_värde),'raw','BGRX').save(str(utmatningsposition/'native-vnc.png'))
                    return nummer,summa_värde
                nummer,summa_värde=skärmbild();assert nummer>0 and summa_värde==너비*높이*4
                Rapport_värde['checks'].append('Native framebuffer RFB full update {} bytes'.format(summa_värde))
                nummer,summa_värde=skärmbild(1);assert summa_värde<너비*높이*4
                Rapport_värde['checks'].append('RFB incremental update')
                처음=len(LOG_POST)
                for tecken_värde in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if tecken_värde=='\r' else ord(tecken_värde)
                    Anslut.sendall(struct.pack('!BBHI',4,1,0,symbol));Anslut.sendall(struct.pack('!BBHI',4,0,0,symbol))
                tillståndet_Vänta(b'VNC_NATIVE_PASS',처음)
                Rapport_värde['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Nyckel_pennstreck(symbol,tryck_värde=1):Anslut.sendall(struct.pack('!BBHI',4,tryck_värde,0,symbol))
                처음=len(LOG_POST)
                for tecken_värde in 'echo ':Nyckel_pennstreck(ord(tecken_värde))
                Nyckel_pennstreck(0xffc6)
                for tecken_värde in 'gksrmf':Nyckel_pennstreck(ord(tecken_värde))
                Nyckel_pennstreck(0xffc6);Nyckel_pennstreck(0xff0d)
                tillståndet_Vänta('\r\n한글\r\n'.encode(),처음)
                Rapport_värde['checks'].append('Native VNC F9 two-set Hangul composition')
                Anslut.sendall(struct.pack('!BBHH',5,0,120,100))
                Rapport_värde['checks'].append('VNC pointer input accepted')
            Process_värde.stdin.write(b'poweroff\n');Process_värde.stdin.flush();Process_värde.wait(timeout=15);assert Process_värde.returncode==0
            Rapport_värde['passed']=True
    finally:
        if Process_värde and Process_värde.poll() is None:
            Process_värde.terminate()
            try: Process_värde.wait(timeout=5)
            except subprocess.TimeoutExpired: Process_värde.kill();Process_värde.wait()
        (utmatningsposition/'serial.log').write_bytes(LOG_POST)
        (utmatningsposition/'report.json').write_text(json.dumps(Rapport_värde,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Rapport_värde,ensure_ascii=False,indent=2))


if __name__=='__main__': Kör()
