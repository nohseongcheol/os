#!/usr/bin/env python3
"""нақты_деректер OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from орындау_пәрмен import жоба_түбір, Команда
from желі_көпір import желі_көпір


def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--kernel', type=Path, default=жоба_түбір / 'build/kernel8.img')
    талдау_құралы_48ee4b1b.add_argument('--access', type=Path, default=жоба_түбір / 'build/remote/access.json')
    талдау_құралы_48ee4b1b.add_argument('--output', type=Path, default=жоба_түбір / 'build/verification/native-remote')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    Шығысы = Аргументтер.output
    Шығысы.mkdir(parents=True, exist_ok=True)
    Баптаулар = json.loads(Аргументтер.access.read_text())
    есеп_мән = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Аргументтер.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Байланысу:
            Байланысу.bind(('127.0.0.5', 0))
            return Байланысу.getsockname()[1]
    қоршам_порт, 화면포트, файл_порт = 빈포트(), 빈포트(), 빈포트()
    журнал_жол = bytearray()
    Процесс_мән = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, желі_көпір(файл_порт,
                ['tcp:{}:22'.format(қоршам_порт), 'tcp:{}:5900'.format(화면포트)], орналастыру_мекенжай='127.0.0.5') as көпір_мән:
            실행인수 = Команда()
            실행인수[실행인수.index('-kernel') + 1] = str(Аргументтер.kernel.resolve())
            Процесс_мән = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + көпір_мән.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    деректер = Процесс_мән.stdout.read(4096)
                    if not деректер: break
                    журнал_жол.extend(деректер)
            ағын_мән = threading.Thread(target=수집, daemon=True)
            ағын_мән.start()
            def күту_күйі(Сөз_Мәтін, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Сөз_Мәтін not in журнал_жол[처음:]:
                    if time.monotonic()>끝 or Процесс_мән.poll() is not None:
                        raise AssertionError('Missing '+repr(Сөз_Мәтін)+'\n'+журнал_жол[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            күту_күйі(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def қауіпсіз_қоршам(құпиясөз_мән, нұсқау_мән_4c26ea1b, қосу_енгізу=()):
                환경['JKOROS_TEST_PASSWORD']=құпиясөз_мән
                Аргументтер=['ssh','-v']+list(қосу_енгізу)+['-p',str(қоршам_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',нұсқау_мән_4c26ea1b]
                НӘТИЖЕ=subprocess.run(Аргументтер,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return НӘТИЖЕ
            НӘТИЖЕ=қауіпсіз_қоршам('!' + Баптаулар['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Шығысы/'ssh-rejected.log').write_bytes(НӘТИЖЕ.stderr)
            assert НӘТИЖЕ.returncode!=0 and b'Permission denied' in НӘТИЖЕ.stderr and b'SHOULD_NOT_RUN' not in журнал_жол, НӘТИЖЕ.stderr
            есеп_мән['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            НӘТИЖЕ=қауіпсіз_қоршам(Баптаулар['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Шығысы/'ssh.log').write_bytes(НӘТИЖЕ.stderr)
            (Шығысы/'ssh-output.txt').write_bytes(НӘТИЖЕ.stdout)
            assert НӘТИЖЕ.returncode==0 and b'SSH_NATIVE_PASS' in НӘТИЖЕ.stdout, (НӘТИЖЕ.returncode,НӘТИЖЕ.stdout,НӘТИЖЕ.stderr)
            есеп_мән['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in НӘТИЖЕ.stderr, НӘТИЖЕ.stderr
            есеп_мән['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            НӘТИЖЕ=қауіпсіз_қоршам(Баптаулар['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert НӘТИЖЕ.returncode==0 and 'JAVA Шығысы: 안녕하세요 😀'.encode() in НӘТИЖЕ.stdout,НӘТИЖЕ.stdout
            есеп_мән['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            НӘТИЖЕ=қауіпсіз_қоршам(Баптаулар['ssh_password'], 'missing_remote_command')
            assert НӘТИЖЕ.returncode==127,НӘТИЖЕ.returncode
            есеп_мән['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            НӘТИЖЕ=қауіпсіз_қоршам(Баптаулар['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Шығысы/'ssh-rekey.log').write_bytes(НӘТИЖЕ.stderr)
            assert НӘТИЖЕ.returncode==0 and 'class 창예제'.encode() in НӘТИЖЕ.stdout, (НӘТИЖЕ.returncode,НӘТИЖЕ.stdout,НӘТИЖЕ.stderr)
            assert НӘТИЖЕ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, НӘТИЖЕ.stderr
            есеп_мән['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(қоршам_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            көзбе_көз_белсенді_сеанс=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();таңдау_мән=selectors.DefaultSelector();таңдау_мән.register(көзбе_көз_белсенді_сеанс.stdout,selectors.EVENT_READ)
            def 대화읽기(көрсету_мән):
                ең_соңғы_мерзім_мән=time.monotonic()+30
                while көрсету_мән not in 대화기록:
                    if time.monotonic()>ең_соңғы_мерзім_мән or көзбе_көз_белсенді_сеанс.poll() is not None:raise AssertionError('SSH interactive missing '+repr(көрсету_мән)+' '+repr(bytes(대화기록)))
                    for енгізу_мән,_ in таңдау_мән.select(.1):
                        조각=енгізу_мән.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                көзбе_көз_белсенді_сеанс.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');көзбе_көз_белсенді_сеанс.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                көзбе_көз_белсенді_сеанс.stdin.write(b'\x04');көзбе_көз_белсенді_сеанс.stdin.flush();나머지,Қате=көзбе_көз_белсенді_сеанс.communicate(timeout=15)
                assert көзбе_көз_белсенді_сеанс.returncode==0 and b'PTY allocation request failed' not in Қате,(көзбе_көз_белсенді_сеанс.returncode,Қате)
                (Шығысы/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                таңдау_мән.close()
                if көзбе_көз_белсенді_сеанс.poll() is None:көзбе_көз_белсенді_сеанс.kill();көзбе_көз_белсенді_сеанс.wait()
            есеп_мән['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Байланысу, 수):
                деректер=bytearray()
                while len(деректер)<수:
                    блок_мән=Байланысу.recv(수-len(деректер))
                    if not блок_мән: raise AssertionError('RFB EOF')
                    деректер.extend(блок_мән)
                return bytes(деректер)
            def 화면인증(құпиясөз_мән):
                Байланысу=socket.create_connection(('127.0.0.5',화면포트),10);Байланысу.settimeout(30)
                assert 정확히(Байланысу,12)==b'RFB 003.008\n'
                Байланысу.sendall(b'RFB 003.008\n');assert 정확히(Байланысу,2)==b'\x01\x02'
                Байланысу.sendall(b'\x02');тексеріс_мән=정확히(Байланысу,16)
                입력암호=құпиясөз_мән.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Байланысу.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(тексеріс_мән))
                күй_мән=struct.unpack('!I',정확히(Байланысу,4))[0]
                return Байланысу,күй_мән
            дұрыс_емес_құпиясөз='!' if not Баптаулар['vnc_password'].startswith('!') else '?'
            Байланысу,күй_мән=화면인증(дұрыс_емес_құпиясөз);assert күй_мән==1;Байланысу.close();time.sleep(.6)
            есеп_мән['checks'].append('VNC incorrect password rejected')
            Байланысу,күй_мән=화면인증(Баптаулар['vnc_password']);assert күй_мән==0
            with Байланысу:
                Байланысу.sendall(b'\x01');бастапқы_күй=정확히(Байланысу,24);너비,높이=struct.unpack('!HH',бастапқы_күй[:4]);Аты=정확히(Байланысу,struct.unpack('!I',бастапқы_күй[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Аты
                def 화면(өсім_қадамы_қадам=0):
                    Байланысу.sendall(struct.pack('!BBHHHH',3,өсім_қадамы_қадам,0,0,너비,높이));머리=정확히(Байланысу,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    сызба_мән=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_координатасы,Y_түймешігі_координата,영역너비,영역높이,әдіс_режим=struct.unpack('!HHHHi',정확히(Байланысу,12));assert әдіс_режим==0 and x_координатасы+영역너비<=너비 and Y_түймешігі_координата+영역높이<=높이
                        нүкте=정확히(Байланысу,영역너비*영역높이*4);합계+=len(нүкте)
                        for Жол in range(영역높이):сызба_мән[((Y_түймешігі_координата+Жол)*너비+x_координатасы)*4:((Y_түймешігі_координата+Жол)*너비+x_координатасы+영역너비)*4]=нүкте[Жол*영역너비*4:(Жол+1)*영역너비*4]
                    if not өсім_қадамы_қадам:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(сызба_мән),'raw','BGRX').save(str(Шығысы/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                есеп_мән['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                есеп_мән['checks'].append('RFB incremental update')
                처음=len(журнал_жол)
                for таңба_мән in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if таңба_мән=='\r' else ord(таңба_мән)
                    Байланысу.sendall(struct.pack('!BBHI',4,1,0,символ));Байланысу.sendall(struct.pack('!BBHI',4,0,0,символ))
                күту_күйі(b'VNC_NATIVE_PASS',처음)
                есеп_мән['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(символ,басу_мән_3efd25d6=1):Байланысу.sendall(struct.pack('!BBHI',4,басу_мән_3efd25d6,0,символ))
                처음=len(журнал_жол)
                for таңба_мән in 'echo ':글쇠(ord(таңба_мән))
                글쇠(0xffc6)
                for таңба_мән in 'gksrmf':글쇠(ord(таңба_мән))
                글쇠(0xffc6);글쇠(0xff0d)
                күту_күйі('\r\n한글\r\n'.encode(),처음)
                есеп_мән['checks'].append('Native VNC F9 two-set Hangul composition')
                Байланысу.sendall(struct.pack('!BBHH',5,0,120,100))
                есеп_мән['checks'].append('VNC pointer input accepted')
            Процесс_мән.stdin.write(b'poweroff\n');Процесс_мән.stdin.flush();Процесс_мән.wait(timeout=15);assert Процесс_мән.returncode==0
            есеп_мән['passed']=True
    finally:
        if Процесс_мән and Процесс_мән.poll() is None:
            Процесс_мән.terminate()
            try: Процесс_мән.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс_мән.kill();Процесс_мән.wait()
        (Шығысы/'serial.log').write_bytes(журнал_жол)
        (Шығысы/'report.json').write_text(json.dumps(есеп_мән,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(есеп_мән,ensure_ascii=False,indent=2))


if __name__=='__main__': Орындау_2()
