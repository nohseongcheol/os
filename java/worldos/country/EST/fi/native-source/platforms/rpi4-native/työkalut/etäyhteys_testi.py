#!/usr/bin/env python3
"""todellinen_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Suorita_komento import aloite_juuri, komento
from silta_3de4fe3a import silta_3de4fe3a


def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--kernel', type=Path, default=aloite_juuri / 'build/kernel8.img')
    jäsennin_48ee4b1b.add_argument('--access', type=Path, default=aloite_juuri / 'build/remote/access.json')
    jäsennin_48ee4b1b.add_argument('--output', type=Path, default=aloite_juuri / 'build/verification/native-remote')
    argumentit = jäsennin_48ee4b1b.parse_args()
    tulostuspaikka = argumentit.output
    tulostuspaikka.mkdir(parents=True, exist_ok=True)
    Asetukset = json.loads(argumentit.access.read_text())
    raportti_ARVO = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumentit.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Yhdistä:
            Yhdistä.bind(('127.0.0.5', 0))
            return Yhdistä.getsockname()[1]
    liittymä_portti, 화면포트, tiedostoportti = 빈포트(), 빈포트(), 빈포트()
    LOG_TIETUE = bytearray()
    prosessi_ARVO = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, silta_3de4fe3a(tiedostoportti,
                ['tcp:{}:22'.format(liittymä_portti), 'tcp:{}:5900'.format(화면포트)], isäntä_OSOITE='127.0.0.5') as silta_ARVO:
            실행인수 = komento()
            실행인수[실행인수.index('-kernel') + 1] = str(argumentit.kernel.resolve())
            prosessi_ARVO = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + silta_ARVO.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = prosessi_ARVO.stdout.read(4096)
                    if not data: break
                    LOG_TIETUE.extend(data)
            säie_ARVO = threading.Thread(target=수집, daemon=True)
            säie_ARVO.start()
            def odotustila(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_TIETUE[처음:]:
                    if time.monotonic()>끝 or prosessi_ARVO.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_TIETUE[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            odotustila(b'jkoros-native> ')
            apuosa_ARVO = Path(임시)/'askpass'
            apuosa_ARVO.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            apuosa_ARVO.chmod(0o700)
            ympäristö = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(apuosa_ARVO), SSH_ASKPASS_REQUIRE='force')
            def suojattu_liittymä(salasana_ARVO, käsky_ARVO, liitä_merkintä=()):
                ympäristö['JKOROS_TEST_PASSWORD']=salasana_ARVO
                argumentit=['ssh','-v']+list(liitä_merkintä)+['-p',str(liittymä_portti),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',käsky_ARVO]
                TULOS=subprocess.run(argumentit,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=ympäristö,start_new_session=True,timeout=50)
                return TULOS
            TULOS=suojattu_liittymä('!' + Asetukset['ssh_password'], 'echo SHOULD_NOT_RUN')
            (tulostuspaikka/'ssh-rejected.log').write_bytes(TULOS.stderr)
            assert TULOS.returncode!=0 and b'Permission denied' in TULOS.stderr and b'SHOULD_NOT_RUN' not in LOG_TIETUE, TULOS.stderr
            raportti_ARVO['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            TULOS=suojattu_liittymä(Asetukset['ssh_password'], 'echo SSH_NATIVE_PASS')
            (tulostuspaikka/'ssh.log').write_bytes(TULOS.stderr)
            (tulostuspaikka/'ssh-output.txt').write_bytes(TULOS.stdout)
            assert TULOS.returncode==0 and b'SSH_NATIVE_PASS' in TULOS.stdout, (TULOS.returncode,TULOS.stdout,TULOS.stderr)
            raportti_ARVO['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in TULOS.stderr, TULOS.stderr
            raportti_ARVO['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            TULOS=suojattu_liittymä(Asetukset['ssh_password'], 'cd /example/java; java Tulostusesimerkki; cd /')
            assert TULOS.returncode==0 and 'JAVA tulostuspaikka: 안녕하세요 😀'.encode() in TULOS.stdout,TULOS.stdout
            raportti_ARVO['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            TULOS=suojattu_liittymä(Asetukset['ssh_password'], 'missing_remote_command')
            assert TULOS.returncode==127,TULOS.returncode
            raportti_ARVO['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            TULOS=suojattu_liittymä(Asetukset['ssh_password'], 'cat /example/java/Ikkunaesimerkki.java', ('-o', 'RekeyLimit=1K'))
            (tulostuspaikka/'ssh-rekey.log').write_bytes(TULOS.stderr)
            assert TULOS.returncode==0 and 'class Ikkunaesimerkki'.encode() in TULOS.stdout, (TULOS.returncode,TULOS.stdout,TULOS.stderr)
            assert TULOS.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, TULOS.stderr
            raportti_ARVO['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(liittymä_portti),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            vuorovaikutteinen_istunto=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ympäristö,start_new_session=True,bufsize=0)
            transkriptio=bytearray();valinta_ARVO=selectors.DefaultSelector();valinta_ARVO.register(vuorovaikutteinen_istunto.stdout,selectors.EVENT_READ)
            def lukea_vuorovaikutteinen(näyttää_ARVO):
                määräaika_ARVO=time.monotonic()+30
                while näyttää_ARVO not in transkriptio:
                    if time.monotonic()>määräaika_ARVO or vuorovaikutteinen_istunto.poll() is not None:raise AssertionError('SSH interactive missing '+repr(näyttää_ARVO)+' '+repr(bytes(transkriptio)))
                    for merkintä_ARVO_962f286b,_ in valinta_ARVO.select(.1):
                        조각=merkintä_ARVO_962f286b.fileobj.read(4096)
                        if 조각:transkriptio.extend(조각)
            try:
                lukea_vuorovaikutteinen(b'shared native console')
                vuorovaikutteinen_istunto.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');vuorovaikutteinen_istunto.stdin.flush();lukea_vuorovaikutteinen(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                vuorovaikutteinen_istunto.stdin.write(b'\x04');vuorovaikutteinen_istunto.stdin.flush();나머지,VIRHE=vuorovaikutteinen_istunto.communicate(timeout=15)
                assert vuorovaikutteinen_istunto.returncode==0 and b'PTY allocation request failed' not in VIRHE,(vuorovaikutteinen_istunto.returncode,VIRHE)
                (tulostuspaikka/'ssh-interactive.txt').write_bytes(transkriptio+나머지)
            finally:
                valinta_ARVO.close()
                if vuorovaikutteinen_istunto.poll() is None:vuorovaikutteinen_istunto.kill();vuorovaikutteinen_istunto.wait()
            raportti_ARVO['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Yhdistä, numero):
                data=bytearray()
                while len(data)<numero:
                    lohko_ARVO=Yhdistä.recv(numero-len(data))
                    if not lohko_ARVO: raise AssertionError('RFB EOF')
                    data.extend(lohko_ARVO)
                return bytes(data)
            def 화면인증(salasana_ARVO):
                Yhdistä=socket.create_connection(('127.0.0.5',화면포트),10);Yhdistä.settimeout(30)
                assert 정확히(Yhdistä,12)==b'RFB 003.008\n'
                Yhdistä.sendall(b'RFB 003.008\n');assert 정확히(Yhdistä,2)==b'\x01\x02'
                Yhdistä.sendall(b'\x02');haaste_ARVO=정확히(Yhdistä,16)
                syöte_salasana=salasana_ARVO.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(numero)[::-1],2) for numero in syöte_salasana)
                Yhdistä.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(haaste_ARVO))
                Tila_ARVO=struct.unpack('!I',정확히(Yhdistä,4))[0]
                return Yhdistä,Tila_ARVO
            pätemätön_salasana='!' if not Asetukset['vnc_password'].startswith('!') else '?'
            Yhdistä,Tila_ARVO=화면인증(pätemätön_salasana);assert Tila_ARVO==1;Yhdistä.close();time.sleep(.6)
            raportti_ARVO['checks'].append('VNC incorrect password rejected')
            Yhdistä,Tila_ARVO=화면인증(Asetukset['vnc_password']);assert Tila_ARVO==0
            with Yhdistä:
                Yhdistä.sendall(b'\x01');alkutila=정확히(Yhdistä,24);너비,높이=struct.unpack('!HH',alkutila[:4]);Nimi=정확히(Yhdistä,struct.unpack('!I',alkutila[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nimi
                def 화면(증분=0):
                    Yhdistä.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Yhdistä,4);numero=struct.unpack('!H',머리[2:])[0];summa_ARVO=0
                    piirustus_ARVO=bytearray(너비*높이*4)
                    for _ in range(numero):
                        x_koordinaatti,Y_koordinaatti,영역너비,영역높이,menetelmä_tila=struct.unpack('!HHHHi',정확히(Yhdistä,12));assert menetelmä_tila==0 and x_koordinaatti+영역너비<=너비 and Y_koordinaatti+영역높이<=높이
                        kuvapiste=정확히(Yhdistä,영역너비*영역높이*4);summa_ARVO+=len(kuvapiste)
                        for syöterivi in range(영역높이):piirustus_ARVO[((Y_koordinaatti+syöterivi)*너비+x_koordinaatti)*4:((Y_koordinaatti+syöterivi)*너비+x_koordinaatti+영역너비)*4]=kuvapiste[syöterivi*영역너비*4:(syöterivi+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(piirustus_ARVO),'raw','BGRX').save(str(tulostuspaikka/'native-vnc.png'))
                    return numero,summa_ARVO
                numero,summa_ARVO=화면();assert numero>0 and summa_ARVO==너비*높이*4
                raportti_ARVO['checks'].append('Native framebuffer RFB full update {} bytes'.format(summa_ARVO))
                numero,summa_ARVO=화면(1);assert summa_ARVO<너비*높이*4
                raportti_ARVO['checks'].append('RFB incremental update')
                처음=len(LOG_TIETUE)
                for merkki_ARVO in 'echo VNC_NATIVE_PASS\r':
                    symboli=0xff0d if merkki_ARVO=='\r' else ord(merkki_ARVO)
                    Yhdistä.sendall(struct.pack('!BBHI',4,1,0,symboli));Yhdistä.sendall(struct.pack('!BBHI',4,0,0,symboli))
                odotustila(b'VNC_NATIVE_PASS',처음)
                raportti_ARVO['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Avain_kynänpiirto(symboli,paina_ARVO=1):Yhdistä.sendall(struct.pack('!BBHI',4,paina_ARVO,0,symboli))
                처음=len(LOG_TIETUE)
                for merkki_ARVO in 'echo ':Avain_kynänpiirto(ord(merkki_ARVO))
                Avain_kynänpiirto(0xffc6)
                for merkki_ARVO in 'gksrmf':Avain_kynänpiirto(ord(merkki_ARVO))
                Avain_kynänpiirto(0xffc6);Avain_kynänpiirto(0xff0d)
                odotustila('\r\n한글\r\n'.encode(),처음)
                raportti_ARVO['checks'].append('Native VNC F9 two-set Hangul composition')
                Yhdistä.sendall(struct.pack('!BBHH',5,0,120,100))
                raportti_ARVO['checks'].append('VNC pointer input accepted')
            prosessi_ARVO.stdin.write(b'poweroff\n');prosessi_ARVO.stdin.flush();prosessi_ARVO.wait(timeout=15);assert prosessi_ARVO.returncode==0
            raportti_ARVO['passed']=True
    finally:
        if prosessi_ARVO and prosessi_ARVO.poll() is None:
            prosessi_ARVO.terminate()
            try: prosessi_ARVO.wait(timeout=5)
            except subprocess.TimeoutExpired: prosessi_ARVO.kill();prosessi_ARVO.wait()
        (tulostuspaikka/'serial.log').write_bytes(LOG_TIETUE)
        (tulostuspaikka/'report.json').write_text(json.dumps(raportti_ARVO,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(raportti_ARVO,ensure_ascii=False,indent=2))


if __name__=='__main__': Suorita_2()
