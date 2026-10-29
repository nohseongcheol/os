#!/usr/bin/env python3
"""aktual_të_dhëna OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from zbatoj_komandë import Project_rrënjë, Komanda
from rrjet_urë import rrjet_urë


def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--kernel', type=Path, default=Project_rrënjë / 'build/kernel8.img')
    analizues_48ee4b1b.add_argument('--access', type=Path, default=Project_rrënjë / 'build/remote/access.json')
    analizues_48ee4b1b.add_argument('--output', type=Path, default=Project_rrënjë / 'build/verification/native-remote')
    Argumente = analizues_48ee4b1b.parse_args()
    출력 = Argumente.output
    출력.mkdir(parents=True, exist_ok=True)
    Rregullime = json.loads(Argumente.access.read_text())
    raport_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argumente.kernel.read_bytes()).hexdigest(), 'checks': []}
    def bosh_portë():
        with socket.socket() as Lidhu:
            Lidhu.bind(('127.0.0.5', 0))
            return Lidhu.getsockname()[1]
    pasues_portë, 화면포트, skedar_portë = bosh_portë(), bosh_portë(), bosh_portë()
    LOG_RECORD = bytearray()
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, rrjet_urë(skedar_portë,
                ['tcp:{}:22'.format(pasues_portë), 'tcp:{}:5900'.format(화면포트)], pritës_email='127.0.0.5') as urë_VALUE:
            실행인수 = Komanda()
            실행인수[실행인수.index('-kernel') + 1] = str(Argumente.kernel.resolve())
            Proces_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + urë_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    të_dhëna = Proces_VALUE.stdout.read(4096)
                    if not të_dhëna: break
                    LOG_RECORD.extend(të_dhëna)
            thread_VALUE = threading.Thread(target=수집, daemon=True)
            thread_VALUE.start()
            def Prit_status(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            Prit_status(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def i_sigurt_pasues(fjalëkalim_VALUE, instruksion_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=fjalëkalim_VALUE
                Argumente=['ssh','-v']+list(추가)+['-p',str(pasues_portë),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksion_VALUE]
                llogaritje=subprocess.run(Argumente,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return llogaritje
            llogaritje=i_sigurt_pasues('!' + Rregullime['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(llogaritje.stderr)
            assert llogaritje.returncode!=0 and b'Permission denied' in llogaritje.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, llogaritje.stderr
            raport_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            llogaritje=i_sigurt_pasues(Rregullime['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(llogaritje.stderr)
            (출력/'ssh-output.txt').write_bytes(llogaritje.stdout)
            assert llogaritje.returncode==0 and b'SSH_NATIVE_PASS' in llogaritje.stdout, (llogaritje.returncode,llogaritje.stdout,llogaritje.stderr)
            raport_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in llogaritje.stderr, llogaritje.stderr
            raport_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            llogaritje=i_sigurt_pasues(Rregullime['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert llogaritje.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in llogaritje.stdout,llogaritje.stdout
            raport_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            llogaritje=i_sigurt_pasues(Rregullime['ssh_password'], 'missing_remote_command')
            assert llogaritje.returncode==127,llogaritje.returncode
            raport_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            llogaritje=i_sigurt_pasues(Rregullime['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(llogaritje.stderr)
            assert llogaritje.returncode==0 and 'class 창예제'.encode() in llogaritje.stdout, (llogaritje.returncode,llogaritje.stdout,llogaritje.stderr)
            assert llogaritje.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, llogaritje.stderr
            raport_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(pasues_portë),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ndërvepruese_sesion=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();përzgjedhje_VALUE=selectors.DefaultSelector();përzgjedhje_VALUE.register(ndërvepruese_sesion.stdout,selectors.EVENT_READ)
            def 대화읽기(shfaq_VALUE):
                마감=time.monotonic()+30
                while shfaq_VALUE not in 대화기록:
                    if time.monotonic()>마감 or ndërvepruese_sesion.poll() is not None:raise AssertionError('SSH interactive missing '+repr(shfaq_VALUE)+' '+repr(bytes(대화기록)))
                    for futje_VALUE,_ in përzgjedhje_VALUE.select(.1):
                        조각=futje_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ndërvepruese_sesion.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ndërvepruese_sesion.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ndërvepruese_sesion.stdin.write(b'\x04');ndërvepruese_sesion.stdin.flush();나머지,GABIM=ndërvepruese_sesion.communicate(timeout=15)
                assert ndërvepruese_sesion.returncode==0 and b'PTY allocation request failed' not in GABIM,(ndërvepruese_sesion.returncode,GABIM)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                përzgjedhje_VALUE.close()
                if ndërvepruese_sesion.poll() is None:ndërvepruese_sesion.kill();ndërvepruese_sesion.wait()
            raport_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Lidhu, 수):
                të_dhëna=bytearray()
                while len(të_dhëna)<수:
                    덩이=Lidhu.recv(수-len(të_dhëna))
                    if not 덩이: raise AssertionError('RFB EOF')
                    të_dhëna.extend(덩이)
                return bytes(të_dhëna)
            def 화면인증(fjalëkalim_VALUE):
                Lidhu=socket.create_connection(('127.0.0.5',화면포트),10);Lidhu.settimeout(30)
                assert 정확히(Lidhu,12)==b'RFB 003.008\n'
                Lidhu.sendall(b'RFB 003.008\n');assert 정확히(Lidhu,2)==b'\x01\x02'
                Lidhu.sendall(b'\x02');sfidë_VALUE=정확히(Lidhu,16)
                입력암호=fjalëkalim_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Lidhu.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(sfidë_VALUE))
                status_VALUE=struct.unpack('!I',정확히(Lidhu,4))[0]
                return Lidhu,status_VALUE
            i_pavlefshëm_fjalëkalim='!' if not Rregullime['vnc_password'].startswith('!') else '?'
            Lidhu,status_VALUE=화면인증(i_pavlefshëm_fjalëkalim);assert status_VALUE==1;Lidhu.close();time.sleep(.6)
            raport_VALUE['checks'].append('VNC incorrect password rejected')
            Lidhu,status_VALUE=화면인증(Rregullime['vnc_password']);assert status_VALUE==0
            with Lidhu:
                Lidhu.sendall(b'\x01');초기=정확히(Lidhu,24);너비,높이=struct.unpack('!HH',초기[:4]);Emër=정확히(Lidhu,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Emër
                def 화면(증분=0):
                    Lidhu.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Lidhu,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    vizatim_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        koordinata_x,Y_koordinatë,영역너비,영역높이,metoda_MODE=struct.unpack('!HHHHi',정확히(Lidhu,12));assert metoda_MODE==0 and koordinata_x+영역너비<=너비 and Y_koordinatë+영역높이<=높이
                        pikëz=정확히(Lidhu,영역너비*영역높이*4);합계+=len(pikëz)
                        for linjë in range(영역높이):vizatim_VALUE[((Y_koordinatë+linjë)*너비+koordinata_x)*4:((Y_koordinatë+linjë)*너비+koordinata_x+영역너비)*4]=pikëz[linjë*영역너비*4:(linjë+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(vizatim_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                raport_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                raport_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for karakter_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if karakter_VALUE=='\r' else ord(karakter_VALUE)
                    Lidhu.sendall(struct.pack('!BBHI',4,1,0,simbol));Lidhu.sendall(struct.pack('!BBHI',4,0,0,simbol))
                Prit_status(b'VNC_NATIVE_PASS',처음)
                raport_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbol,shtyp_VALUE=1):Lidhu.sendall(struct.pack('!BBHI',4,shtyp_VALUE,0,simbol))
                처음=len(LOG_RECORD)
                for karakter_VALUE in 'echo ':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6)
                for karakter_VALUE in 'gksrmf':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                Prit_status('\r\n한글\r\n'.encode(),처음)
                raport_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Lidhu.sendall(struct.pack('!BBHH',5,0,120,100))
                raport_VALUE['checks'].append('VNC pointer input accepted')
            Proces_VALUE.stdin.write(b'poweroff\n');Proces_VALUE.stdin.flush();Proces_VALUE.wait(timeout=15);assert Proces_VALUE.returncode==0
            raport_VALUE['passed']=True
    finally:
        if Proces_VALUE and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces_VALUE.kill();Proces_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_RECORD)
        (출력/'report.json').write_text(json.dumps(raport_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(raport_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Ekzekuto()
