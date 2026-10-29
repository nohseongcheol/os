#!/usr/bin/env python3
"""effettivo_dati OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Esegui_comando import azione_radice, comando
from bridge_3de4fe3a import bridge_3de4fe3a


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=azione_radice / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=azione_radice / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=azione_radice / 'build/verification/native-remote')
    argomenti = parser_48ee4b1b.parse_args()
    uscitaTesto = argomenti.output
    uscitaTesto.mkdir(parents=True, exist_ok=True)
    Impostazioni = json.loads(argomenti.access.read_text())
    Report_VALORE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argomenti.kernel.read_bytes()).hexdigest(), 'checks': []}
    def vuota_porta():
        with socket.socket() as Connetti:
            Connetti.bind(('127.0.0.5', 0))
            return Connetti.getsockname()[1]
    Shell_porta, schermata_porta, porta_file = vuota_porta(), vuota_porta(), vuota_porta()
    LOG_riga = bytearray()
    Processi_VALORE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, bridge_3de4fe3a(porta_file,
                ['tcp:{}:22'.format(Shell_porta), 'tcp:{}:5900'.format(schermata_porta)], ID_host='127.0.0.5') as bridge_VALORE:
            실행인수 = comando()
            실행인수[실행인수.index('-kernel') + 1] = str(argomenti.kernel.resolve())
            Processi_VALORE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bridge_VALORE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dati = Processi_VALORE.stdout.read(4096)
                    if not dati: break
                    LOG_riga.extend(dati)
            thread_VALORE = threading.Thread(target=수집, daemon=True)
            thread_VALORE.start()
            def stato_di_attesa(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_riga[처음:]:
                    if time.monotonic()>끝 or Processi_VALORE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_riga[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            stato_di_attesa(b'jkoros-native> ')
            helper_VALORE = Path(임시)/'askpass'
            helper_VALORE.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            helper_VALORE.chmod(0o700)
            ambiente = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(helper_VALORE), SSH_ASKPASS_REQUIRE='force')
            def SSH(password_VALORE, istruzione_VALORE_4c26ea1b, Aggiunta_voce=()):
                ambiente['JKOROS_TEST_PASSWORD']=password_VALORE
                argomenti=['ssh','-v']+list(Aggiunta_voce)+['-p',str(Shell_porta),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',istruzione_VALORE_4c26ea1b]
                risultato=subprocess.run(argomenti,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=ambiente,start_new_session=True,timeout=50)
                return risultato
            risultato=SSH('!' + Impostazioni['ssh_password'], 'echo SHOULD_NOT_RUN')
            (uscitaTesto/'ssh-rejected.log').write_bytes(risultato.stderr)
            assert risultato.returncode!=0 and b'Permission denied' in risultato.stderr and b'SHOULD_NOT_RUN' not in LOG_riga, risultato.stderr
            Report_VALORE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            risultato=SSH(Impostazioni['ssh_password'], 'echo SSH_NATIVE_PASS')
            (uscitaTesto/'ssh.log').write_bytes(risultato.stderr)
            (uscitaTesto/'ssh-output.txt').write_bytes(risultato.stdout)
            assert risultato.returncode==0 and b'SSH_NATIVE_PASS' in risultato.stdout, (risultato.returncode,risultato.stdout,risultato.stderr)
            Report_VALORE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in risultato.stderr, risultato.stderr
            Report_VALORE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            risultato=SSH(Impostazioni['ssh_password'], 'cd /example/java; java EsempioUscita; cd /')
            assert risultato.returncode==0 and 'JAVA uscitaTesto: 안녕하세요 😀'.encode() in risultato.stdout,risultato.stdout
            Report_VALORE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            risultato=SSH(Impostazioni['ssh_password'], 'missing_remote_command')
            assert risultato.returncode==127,risultato.returncode
            Report_VALORE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            risultato=SSH(Impostazioni['ssh_password'], 'cat /example/java/EsempioFinestra.java', ('-o', 'RekeyLimit=1K'))
            (uscitaTesto/'ssh-rekey.log').write_bytes(risultato.stderr)
            assert risultato.returncode==0 and 'class EsempioFinestra'.encode() in risultato.stdout, (risultato.returncode,risultato.stdout,risultato.stderr)
            assert risultato.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, risultato.stderr
            Report_VALORE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Shell_porta),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interattivo_sessione=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ambiente,start_new_session=True,bufsize=0)
            trascrizione=bytearray();selezione_VALORE=selectors.DefaultSelector();selezione_VALORE.register(interattivo_sessione.stdout,selectors.EVENT_READ)
            def 대화읽기(mostrare_VALORE):
                scadenza_VALORE=time.monotonic()+30
                while mostrare_VALORE not in trascrizione:
                    if time.monotonic()>scadenza_VALORE or interattivo_sessione.poll() is not None:raise AssertionError('SSH interactive missing '+repr(mostrare_VALORE)+' '+repr(bytes(trascrizione)))
                    for voce_VALORE,_ in selezione_VALORE.select(.1):
                        blocco_VALORE_652d4b53=voce_VALORE.fileobj.read(4096)
                        if blocco_VALORE_652d4b53:trascrizione.extend(blocco_VALORE_652d4b53)
            try:
                대화읽기(b'shared native console')
                interattivo_sessione.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interattivo_sessione.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interattivo_sessione.stdin.write(b'\x04');interattivo_sessione.stdin.flush();나머지,errore=interattivo_sessione.communicate(timeout=15)
                assert interattivo_sessione.returncode==0 and b'PTY allocation request failed' not in errore,(interattivo_sessione.returncode,errore)
                (uscitaTesto/'ssh-interactive.txt').write_bytes(trascrizione+나머지)
            finally:
                selezione_VALORE.close()
                if interattivo_sessione.poll() is None:interattivo_sessione.kill();interattivo_sessione.wait()
            Report_VALORE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Connetti, numero):
                dati=bytearray()
                while len(dati)<numero:
                    blocco_VALORE=Connetti.recv(numero-len(dati))
                    if not blocco_VALORE: raise AssertionError('RFB EOF')
                    dati.extend(blocco_VALORE)
                return bytes(dati)
            def schermata_autenticazione(password_VALORE):
                Connetti=socket.create_connection(('127.0.0.5',schermata_porta),10);Connetti.settimeout(30)
                assert 정확히(Connetti,12)==b'RFB 003.008\n'
                Connetti.sendall(b'RFB 003.008\n');assert 정확히(Connetti,2)==b'\x01\x02'
                Connetti.sendall(b'\x02');test_VALORE=정확히(Connetti,16)
                input_password=password_VALORE.encode('ascii')[:8].ljust(8, b'\0')
                tasto_materiale=bytes(int('{:08b}'.format(numero)[::-1],2) for numero in input_password)
                Connetti.sendall(DES.new(tasto_materiale,DES.MODE_ECB).encrypt(test_VALORE))
                Stato_VALORE=struct.unpack('!I',정확히(Connetti,4))[0]
                return Connetti,Stato_VALORE
            non_valida_password='!' if not Impostazioni['vnc_password'].startswith('!') else '?'
            Connetti,Stato_VALORE=schermata_autenticazione(non_valida_password);assert Stato_VALORE==1;Connetti.close();time.sleep(.6)
            Report_VALORE['checks'].append('VNC incorrect password rejected')
            Connetti,Stato_VALORE=schermata_autenticazione(Impostazioni['vnc_password']);assert Stato_VALORE==0
            with Connetti:
                Connetti.sendall(b'\x01');stato_iniziale=정확히(Connetti,24);너비,altezza_VALORE=struct.unpack('!HH',stato_iniziale[:4]);Nome=정확히(Connetti,struct.unpack('!I',stato_iniziale[20:24])[0])
                assert (너비,altezza_VALORE)==(640,480) and b'jkoros native'==Nome
                def schermata(incremento_passaggio=0):
                    Connetti.sendall(struct.pack('!BBHHHH',3,incremento_passaggio,0,0,너비,altezza_VALORE));intestazione_VALORE=정확히(Connetti,4);numero=struct.unpack('!H',intestazione_VALORE[2:])[0];totale_VALORE=0
                    disegno_VALORE=bytearray(너비*altezza_VALORE*4)
                    for _ in range(numero):
                        coordinata_x,Y_coordinata,영역너비,area_altezza,metodo_MODA=struct.unpack('!HHHHi',정확히(Connetti,12));assert metodo_MODA==0 and coordinata_x+영역너비<=너비 and Y_coordinata+area_altezza<=altezza_VALORE
                        pixel=정확히(Connetti,영역너비*area_altezza*4);totale_VALORE+=len(pixel)
                        for riga_di_ingresso in range(area_altezza):disegno_VALORE[((Y_coordinata+riga_di_ingresso)*너비+coordinata_x)*4:((Y_coordinata+riga_di_ingresso)*너비+coordinata_x+영역너비)*4]=pixel[riga_di_ingresso*영역너비*4:(riga_di_ingresso+1)*영역너비*4]
                    if not incremento_passaggio:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,altezza_VALORE),bytes(disegno_VALORE),'raw','BGRX').save(str(uscitaTesto/'native-vnc.png'))
                    return numero,totale_VALORE
                numero,totale_VALORE=schermata();assert numero>0 and totale_VALORE==너비*altezza_VALORE*4
                Report_VALORE['checks'].append('Native framebuffer RFB full update {} bytes'.format(totale_VALORE))
                numero,totale_VALORE=schermata(1);assert totale_VALORE<너비*altezza_VALORE*4
                Report_VALORE['checks'].append('RFB incremental update')
                처음=len(LOG_riga)
                for carattere_VALORE in 'echo VNC_NATIVE_PASS\r':
                    simbolo=0xff0d if carattere_VALORE=='\r' else ord(carattere_VALORE)
                    Connetti.sendall(struct.pack('!BBHI',4,1,0,simbolo));Connetti.sendall(struct.pack('!BBHI',4,0,0,simbolo))
                stato_di_attesa(b'VNC_NATIVE_PASS',처음)
                Report_VALORE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def tasto_Tratto(simbolo,누름=1):Connetti.sendall(struct.pack('!BBHI',4,누름,0,simbolo))
                처음=len(LOG_riga)
                for carattere_VALORE in 'echo ':tasto_Tratto(ord(carattere_VALORE))
                tasto_Tratto(0xffc6)
                for carattere_VALORE in 'gksrmf':tasto_Tratto(ord(carattere_VALORE))
                tasto_Tratto(0xffc6);tasto_Tratto(0xff0d)
                stato_di_attesa('\r\n한글\r\n'.encode(),처음)
                Report_VALORE['checks'].append('Native VNC F9 two-set Hangul composition')
                Connetti.sendall(struct.pack('!BBHH',5,0,120,100))
                Report_VALORE['checks'].append('VNC pointer input accepted')
            Processi_VALORE.stdin.write(b'poweroff\n');Processi_VALORE.stdin.flush();Processi_VALORE.wait(timeout=15);assert Processi_VALORE.returncode==0
            Report_VALORE['passed']=True
    finally:
        if Processi_VALORE and Processi_VALORE.poll() is None:
            Processi_VALORE.terminate()
            try: Processi_VALORE.wait(timeout=5)
            except subprocess.TimeoutExpired: Processi_VALORE.kill();Processi_VALORE.wait()
        (uscitaTesto/'serial.log').write_bytes(LOG_riga)
        (uscitaTesto/'report.json').write_text(json.dumps(Report_VALORE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Report_VALORE,ensure_ascii=False,indent=2))


if __name__=='__main__': avvia()
