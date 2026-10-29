#!/usr/bin/env python3
"""faktisks_dati OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Izpildīt_komanda import Project_sakne, Komanda
from tilts_3de4fe3a import tilts_3de4fe3a


def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--kernel', type=Path, default=Project_sakne / 'build/kernel8.img')
    parsētājs_48ee4b1b.add_argument('--access', type=Path, default=Project_sakne / 'build/remote/access.json')
    parsētājs_48ee4b1b.add_argument('--output', type=Path, default=Project_sakne / 'build/verification/native-remote')
    Parametri = parsētājs_48ee4b1b.parse_args()
    Izvade = Parametri.output
    Izvade.mkdir(parents=True, exist_ok=True)
    Uzstādījumi = json.loads(Parametri.access.read_text())
    ziņot_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Parametri.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Savienoties:
            Savienoties.bind(('127.0.0.5', 0))
            return Savienoties.getsockname()[1]
    čaula_ports, 화면포트, Fails_ports = 빈포트(), 빈포트(), 빈포트()
    LOG_RECORD = bytearray()
    Process_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, tilts_3de4fe3a(Fails_ports,
                ['tcp:{}:22'.format(čaula_ports), 'tcp:{}:5900'.format(화면포트)], viesot_adrese='127.0.0.5') as tilts_VALUE:
            실행인수 = Komanda()
            실행인수[실행인수.index('-kernel') + 1] = str(Parametri.kernel.resolve())
            Process_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + tilts_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dati = Process_VALUE.stdout.read(4096)
                    if not dati: break
                    LOG_RECORD.extend(dati)
            saruna_VALUE = threading.Thread(target=수집, daemon=True)
            saruna_VALUE.start()
            def nogaides_stāvoklis(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Process_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            nogaides_stāvoklis(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def drošs_čaula(parole_VALUE, 명령어, Pievienot_ievade=()):
                환경['JKOROS_TEST_PASSWORD']=parole_VALUE
                Parametri=['ssh','-v']+list(Pievienot_ievade)+['-p',str(čaula_ports),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                mērs=subprocess.run(Parametri,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return mērs
            mērs=drošs_čaula('!' + Uzstādījumi['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Izvade/'ssh-rejected.log').write_bytes(mērs.stderr)
            assert mērs.returncode!=0 and b'Permission denied' in mērs.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, mērs.stderr
            ziņot_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            mērs=drošs_čaula(Uzstādījumi['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Izvade/'ssh.log').write_bytes(mērs.stderr)
            (Izvade/'ssh-output.txt').write_bytes(mērs.stdout)
            assert mērs.returncode==0 and b'SSH_NATIVE_PASS' in mērs.stdout, (mērs.returncode,mērs.stdout,mērs.stderr)
            ziņot_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in mērs.stderr, mērs.stderr
            ziņot_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            mērs=drošs_čaula(Uzstādījumi['ssh_password'], 'cd /example/java; java IzvadesPiemērs; cd /')
            assert mērs.returncode==0 and 'JAVA Izvade: 안녕하세요 😀'.encode() in mērs.stdout,mērs.stdout
            ziņot_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            mērs=drošs_čaula(Uzstādījumi['ssh_password'], 'missing_remote_command')
            assert mērs.returncode==127,mērs.returncode
            ziņot_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            mērs=drošs_čaula(Uzstādījumi['ssh_password'], 'cat /example/java/LogaPiemērs.java', ('-o', 'RekeyLimit=1K'))
            (Izvade/'ssh-rekey.log').write_bytes(mērs.stderr)
            assert mērs.returncode==0 and 'class LogaPiemērs'.encode() in mērs.stdout, (mērs.returncode,mērs.stdout,mērs.stderr)
            assert mērs.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, mērs.stderr
            ziņot_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(čaula_ports),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            transkripcija=bytearray();atlase_VALUE=selectors.DefaultSelector();atlase_VALUE.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(rādīt_VALUE):
                izpildes_termiņš_VALUE=time.monotonic()+30
                while rādīt_VALUE not in transkripcija:
                    if time.monotonic()>izpildes_termiņš_VALUE or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(rādīt_VALUE)+' '+repr(bytes(transkripcija)))
                    for ievade_VALUE,_ in atlase_VALUE.select(.1):
                        조각=ievade_VALUE.fileobj.read(4096)
                        if 조각:transkripcija.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,Kļūda=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in Kļūda,(대화.returncode,Kļūda)
                (Izvade/'ssh-interactive.txt').write_bytes(transkripcija+나머지)
            finally:
                atlase_VALUE.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            ziņot_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Savienoties, numurs):
                dati=bytearray()
                while len(dati)<numurs:
                    porcija_VALUE=Savienoties.recv(numurs-len(dati))
                    if not porcija_VALUE: raise AssertionError('RFB EOF')
                    dati.extend(porcija_VALUE)
                return bytes(dati)
            def 화면인증(parole_VALUE):
                Savienoties=socket.create_connection(('127.0.0.5',화면포트),10);Savienoties.settimeout(30)
                assert 정확히(Savienoties,12)==b'RFB 003.008\n'
                Savienoties.sendall(b'RFB 003.008\n');assert 정확히(Savienoties,2)==b'\x01\x02'
                Savienoties.sendall(b'\x02');izaicinājums_VALUE=정확히(Savienoties,16)
                입력암호=parole_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(numurs)[::-1],2) for numurs in 입력암호)
                Savienoties.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(izaicinājums_VALUE))
                Statuss_VALUE=struct.unpack('!I',정확히(Savienoties,4))[0]
                return Savienoties,Statuss_VALUE
            nederīgs_parole='!' if not Uzstādījumi['vnc_password'].startswith('!') else '?'
            Savienoties,Statuss_VALUE=화면인증(nederīgs_parole);assert Statuss_VALUE==1;Savienoties.close();time.sleep(.6)
            ziņot_VALUE['checks'].append('VNC incorrect password rejected')
            Savienoties,Statuss_VALUE=화면인증(Uzstādījumi['vnc_password']);assert Statuss_VALUE==0
            with Savienoties:
                Savienoties.sendall(b'\x01');sākumstāvoklis=정확히(Savienoties,24);너비,높이=struct.unpack('!HH',sākumstāvoklis[:4]);Nosaukums=정확히(Savienoties,struct.unpack('!I',sākumstāvoklis[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nosaukums
                def 화면(palielinājums_solis=0):
                    Savienoties.sendall(struct.pack('!BBHHHH',3,palielinājums_solis,0,0,너비,높이));머리=정확히(Savienoties,4);numurs=struct.unpack('!H',머리[2:])[0];kopsumma_VALUE=0
                    zīmējums_VALUE=bytearray(너비*높이*4)
                    for _ in range(numurs):
                        x_koordināta,세로좌표,영역너비,영역높이,metode_MODE=struct.unpack('!HHHHi',정확히(Savienoties,12));assert metode_MODE==0 and x_koordināta+영역너비<=너비 and 세로좌표+영역높이<=높이
                        attēla_elements=정확히(Savienoties,영역너비*영역높이*4);kopsumma_VALUE+=len(attēla_elements)
                        for Līniju in range(영역높이):zīmējums_VALUE[((세로좌표+Līniju)*너비+x_koordināta)*4:((세로좌표+Līniju)*너비+x_koordināta+영역너비)*4]=attēla_elements[Līniju*영역너비*4:(Līniju+1)*영역너비*4]
                    if not palielinājums_solis:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(zīmējums_VALUE),'raw','BGRX').save(str(Izvade/'native-vnc.png'))
                    return numurs,kopsumma_VALUE
                numurs,kopsumma_VALUE=화면();assert numurs>0 and kopsumma_VALUE==너비*높이*4
                ziņot_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(kopsumma_VALUE))
                numurs,kopsumma_VALUE=화면(1);assert kopsumma_VALUE<너비*높이*4
                ziņot_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for rakstzīme_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbols=0xff0d if rakstzīme_VALUE=='\r' else ord(rakstzīme_VALUE)
                    Savienoties.sendall(struct.pack('!BBHI',4,1,0,simbols));Savienoties.sendall(struct.pack('!BBHI',4,0,0,simbols))
                nogaides_stāvoklis(b'VNC_NATIVE_PASS',처음)
                ziņot_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Atslēga_ciparrokraksta_vilkums(simbols,nospiest_VALUE=1):Savienoties.sendall(struct.pack('!BBHI',4,nospiest_VALUE,0,simbols))
                처음=len(LOG_RECORD)
                for rakstzīme_VALUE in 'echo ':Atslēga_ciparrokraksta_vilkums(ord(rakstzīme_VALUE))
                Atslēga_ciparrokraksta_vilkums(0xffc6)
                for rakstzīme_VALUE in 'gksrmf':Atslēga_ciparrokraksta_vilkums(ord(rakstzīme_VALUE))
                Atslēga_ciparrokraksta_vilkums(0xffc6);Atslēga_ciparrokraksta_vilkums(0xff0d)
                nogaides_stāvoklis('\r\n한글\r\n'.encode(),처음)
                ziņot_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Savienoties.sendall(struct.pack('!BBHH',5,0,120,100))
                ziņot_VALUE['checks'].append('VNC pointer input accepted')
            Process_VALUE.stdin.write(b'poweroff\n');Process_VALUE.stdin.flush();Process_VALUE.wait(timeout=15);assert Process_VALUE.returncode==0
            ziņot_VALUE['passed']=True
    finally:
        if Process_VALUE and Process_VALUE.poll() is None:
            Process_VALUE.terminate()
            try: Process_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Process_VALUE.kill();Process_VALUE.wait()
        (Izvade/'serial.log').write_bytes(LOG_RECORD)
        (Izvade/'report.json').write_text(json.dumps(ziņot_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ziņot_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Palaist()
