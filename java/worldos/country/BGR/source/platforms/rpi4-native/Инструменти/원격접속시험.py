#!/usr/bin/env python3
"""действителен_данни OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from изпълнявам_команда import проект_корен, Команда
from мост_3de4fe3a import мост_3de4fe3a


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--kernel', type=Path, default=проект_корен / 'build/kernel8.img')
    анализатор_48ee4b1b.add_argument('--access', type=Path, default=проект_корен / 'build/remote/access.json')
    анализатор_48ee4b1b.add_argument('--output', type=Path, default=проект_корен / 'build/verification/native-remote')
    Параметри = анализатор_48ee4b1b.parse_args()
    Изход = Параметри.output
    Изход.mkdir(parents=True, exist_ok=True)
    Настройки = json.loads(Параметри.access.read_text())
    отчет_стойност = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Параметри.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Свързване:
            Свързване.bind(('127.0.0.5', 0))
            return Свързване.getsockname()[1]
    обвивка_порт, 화면포트, Файл_порт = 빈포트(), 빈포트(), 빈포트()
    регистрирам_запис = bytearray()
    Процес_стойност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, мост_3de4fe3a(Файл_порт,
                ['tcp:{}:22'.format(обвивка_порт), 'tcp:{}:5900'.format(화면포트)], хост_адрес='127.0.0.5') as мост_стойност:
            실행인수 = Команда()
            실행인수[실행인수.index('-kernel') + 1] = str(Параметри.kernel.resolve())
            Процес_стойност = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + мост_стойност.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    данни = Процес_стойност.stdout.read(4096)
                    if not данни: break
                    регистрирам_запис.extend(данни)
            нишка_стойност = threading.Thread(target=수집, daemon=True)
            нишка_стойност.start()
            def състояние_на_изчакване(Игри_с_думи_Текст, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Игри_с_думи_Текст not in регистрирам_запис[처음:]:
                    if time.monotonic()>끝 or Процес_стойност.poll() is not None:
                        raise AssertionError('Missing '+repr(Игри_с_думи_Текст)+'\n'+регистрирам_запис[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            състояние_на_изчакване(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def защитен_обвивка(парола_стойност, 명령어, добавям_запис=()):
                환경['JKOROS_TEST_PASSWORD']=парола_стойност
                Параметри=['ssh','-v']+list(добавям_запис)+['-p',str(обвивка_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                РЕЗУЛТАТ=subprocess.run(Параметри,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return РЕЗУЛТАТ
            РЕЗУЛТАТ=защитен_обвивка('!' + Настройки['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Изход/'ssh-rejected.log').write_bytes(РЕЗУЛТАТ.stderr)
            assert РЕЗУЛТАТ.returncode!=0 and b'Permission denied' in РЕЗУЛТАТ.stderr and b'SHOULD_NOT_RUN' not in регистрирам_запис, РЕЗУЛТАТ.stderr
            отчет_стойност['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            РЕЗУЛТАТ=защитен_обвивка(Настройки['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Изход/'ssh.log').write_bytes(РЕЗУЛТАТ.stderr)
            (Изход/'ssh-output.txt').write_bytes(РЕЗУЛТАТ.stdout)
            assert РЕЗУЛТАТ.returncode==0 and b'SSH_NATIVE_PASS' in РЕЗУЛТАТ.stdout, (РЕЗУЛТАТ.returncode,РЕЗУЛТАТ.stdout,РЕЗУЛТАТ.stderr)
            отчет_стойност['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in РЕЗУЛТАТ.stderr, РЕЗУЛТАТ.stderr
            отчет_стойност['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            РЕЗУЛТАТ=защитен_обвивка(Настройки['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert РЕЗУЛТАТ.returncode==0 and 'JAVA Изход: 안녕하세요 😀'.encode() in РЕЗУЛТАТ.stdout,РЕЗУЛТАТ.stdout
            отчет_стойност['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            РЕЗУЛТАТ=защитен_обвивка(Настройки['ssh_password'], 'missing_remote_command')
            assert РЕЗУЛТАТ.returncode==127,РЕЗУЛТАТ.returncode
            отчет_стойност['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            РЕЗУЛТАТ=защитен_обвивка(Настройки['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Изход/'ssh-rekey.log').write_bytes(РЕЗУЛТАТ.stderr)
            assert РЕЗУЛТАТ.returncode==0 and 'class 창예제'.encode() in РЕЗУЛТАТ.stdout, (РЕЗУЛТАТ.returncode,РЕЗУЛТАТ.stdout,РЕЗУЛТАТ.stderr)
            assert РЕЗУЛТАТ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, РЕЗУЛТАТ.stderr
            отчет_стойност['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(обвивка_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            препис=bytearray();избор_стойност=selectors.DefaultSelector();избор_стойност.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(показвам_стойност):
                краен_срок_стойност=time.monotonic()+30
                while показвам_стойност not in препис:
                    if time.monotonic()>краен_срок_стойност or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(показвам_стойност)+' '+repr(bytes(препис)))
                    for запис_стойност,_ in избор_стойност.select(.1):
                        조각=запис_стойност.fileobj.read(4096)
                        if 조각:препис.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,ГРЕШКА=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in ГРЕШКА,(대화.returncode,ГРЕШКА)
                (Изход/'ssh-interactive.txt').write_bytes(препис+나머지)
            finally:
                избор_стойност.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            отчет_стойност['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Свързване, 수):
                данни=bytearray()
                while len(данни)<수:
                    блок_стойност=Свързване.recv(수-len(данни))
                    if not блок_стойност: raise AssertionError('RFB EOF')
                    данни.extend(блок_стойност)
                return bytes(данни)
            def 화면인증(парола_стойност):
                Свързване=socket.create_connection(('127.0.0.5',화면포트),10);Свързване.settimeout(30)
                assert 정확히(Свързване,12)==b'RFB 003.008\n'
                Свързване.sendall(b'RFB 003.008\n');assert 정확히(Свързване,2)==b'\x01\x02'
                Свързване.sendall(b'\x02');проверка_стойност=정확히(Свързване,16)
                입력암호=парола_стойност.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Свързване.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(проверка_стойност))
                Състояние_стойност=struct.unpack('!I',정확히(Свързване,4))[0]
                return Свързване,Състояние_стойност
            невалиден_парола='!' if not Настройки['vnc_password'].startswith('!') else '?'
            Свързване,Състояние_стойност=화면인증(невалиден_парола);assert Състояние_стойност==1;Свързване.close();time.sleep(.6)
            отчет_стойност['checks'].append('VNC incorrect password rejected')
            Свързване,Състояние_стойност=화면인증(Настройки['vnc_password']);assert Състояние_стойност==0
            with Свързване:
                Свързване.sendall(b'\x01');първоначално_състояние=정확히(Свързване,24);너비,높이=struct.unpack('!HH',първоначално_състояние[:4]);Име=정확히(Свързване,struct.unpack('!I',първоначално_състояние[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Име
                def 화면(нарастване_стъпка=0):
                    Свързване.sendall(struct.pack('!BBHHHH',3,нарастване_стъпка,0,0,너비,높이));머리=정확히(Свързване,4);수=struct.unpack('!H',머리[2:])[0];общо_стойност=0
                    чертеж_стойност=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_координата,세로좌표,영역너비,영역높이,метод_режим=struct.unpack('!HHHHi',정확히(Свързване,12));assert метод_режим==0 and x_координата+영역너비<=너비 and 세로좌표+영역높이<=높이
                        пиксел=정확히(Свързване,영역너비*영역높이*4);общо_стойност+=len(пиксел)
                        for ред in range(영역높이):чертеж_стойност[((세로좌표+ред)*너비+x_координата)*4:((세로좌표+ред)*너비+x_координата+영역너비)*4]=пиксел[ред*영역너비*4:(ред+1)*영역너비*4]
                    if not нарастване_стъпка:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(чертеж_стойност),'raw','BGRX').save(str(Изход/'native-vnc.png'))
                    return 수,общо_стойност
                수,общо_стойност=화면();assert 수>0 and общо_стойност==너비*높이*4
                отчет_стойност['checks'].append('Native framebuffer RFB full update {} bytes'.format(общо_стойност))
                수,общо_стойност=화면(1);assert общо_стойност<너비*높이*4
                отчет_стойност['checks'].append('RFB incremental update')
                처음=len(регистрирам_запис)
                for знак_стойност in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if знак_стойност=='\r' else ord(знак_стойност)
                    Свързване.sendall(struct.pack('!BBHI',4,1,0,символ));Свързване.sendall(struct.pack('!BBHI',4,0,0,символ))
                състояние_на_изчакване(b'VNC_NATIVE_PASS',처음)
                отчет_стойност['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ключ_ръкописна_линия(символ,натискам_стойност=1):Свързване.sendall(struct.pack('!BBHI',4,натискам_стойност,0,символ))
                처음=len(регистрирам_запис)
                for знак_стойност in 'echo ':Ключ_ръкописна_линия(ord(знак_стойност))
                Ключ_ръкописна_линия(0xffc6)
                for знак_стойност in 'gksrmf':Ключ_ръкописна_линия(ord(знак_стойност))
                Ключ_ръкописна_линия(0xffc6);Ключ_ръкописна_линия(0xff0d)
                състояние_на_изчакване('\r\n한글\r\n'.encode(),처음)
                отчет_стойност['checks'].append('Native VNC F9 two-set Hangul composition')
                Свързване.sendall(struct.pack('!BBHH',5,0,120,100))
                отчет_стойност['checks'].append('VNC pointer input accepted')
            Процес_стойност.stdin.write(b'poweroff\n');Процес_стойност.stdin.flush();Процес_стойност.wait(timeout=15);assert Процес_стойност.returncode==0
            отчет_стойност['passed']=True
    finally:
        if Процес_стойност and Процес_стойност.poll() is None:
            Процес_стойност.terminate()
            try: Процес_стойност.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес_стойност.kill();Процес_стойност.wait()
        (Изход/'serial.log').write_bytes(регистрирам_запис)
        (Изход/'report.json').write_text(json.dumps(отчет_стойност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(отчет_стойност,ensure_ascii=False,indent=2))


if __name__=='__main__': Стартиране()
