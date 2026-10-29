#!/usr/bin/env python3
"""фактично_дані OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Виконати_команда import Дії_корінь, команда
from міст_3de4fe3a import міст_3de4fe3a


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--kernel', type=Path, default=Дії_корінь / 'build/kernel8.img')
    аналізатор_48ee4b1b.add_argument('--access', type=Path, default=Дії_корінь / 'build/remote/access.json')
    аналізатор_48ee4b1b.add_argument('--output', type=Path, default=Дії_корінь / 'build/verification/native-remote')
    аргументи = аналізатор_48ee4b1b.parse_args()
    Вивід = аргументи.output
    Вивід.mkdir(parents=True, exist_ok=True)
    Налаштування = json.loads(аргументи.access.read_text())
    звіт_значення = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(аргументи.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as З_єднання:
            З_єднання.bind(('127.0.0.5', 0))
            return З_єднання.getsockname()[1]
    оболонка_порт, 화면포트, Файл_порт = 빈포트(), 빈포트(), 빈포트()
    журнал_запис = bytearray()
    процес_значення = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, міст_3de4fe3a(Файл_порт,
                ['tcp:{}:22'.format(оболонка_порт), 'tcp:{}:5900'.format(화면포트)], хост_адреса='127.0.0.5') as міст_значення:
            실행인수 = команда()
            실행인수[실행인수.index('-kernel') + 1] = str(аргументи.kernel.resolve())
            процес_значення = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + міст_значення.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    дані = процес_значення.stdout.read(4096)
                    if not дані: break
                    журнал_запис.extend(дані)
            потік_значення_5b72a632 = threading.Thread(target=수집, daemon=True)
            потік_значення_5b72a632.start()
            def стан_очікування(Ігри_в_слова_Текст, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Ігри_в_слова_Текст not in журнал_запис[처음:]:
                    if time.monotonic()>끝 or процес_значення.poll() is not None:
                        raise AssertionError('Missing '+repr(Ігри_в_слова_Текст)+'\n'+журнал_запис[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            стан_очікування(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            середовище = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def захищений_оболонка(пароль_значення, 명령어, додавати_запис=()):
                середовище['JKOROS_TEST_PASSWORD']=пароль_значення
                аргументи=['ssh','-v']+list(додавати_запис)+['-p',str(оболонка_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                результат=subprocess.run(аргументи,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=середовище,start_new_session=True,timeout=50)
                return результат
            результат=захищений_оболонка('!' + Налаштування['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Вивід/'ssh-rejected.log').write_bytes(результат.stderr)
            assert результат.returncode!=0 and b'Permission denied' in результат.stderr and b'SHOULD_NOT_RUN' not in журнал_запис, результат.stderr
            звіт_значення['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            результат=захищений_оболонка(Налаштування['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Вивід/'ssh.log').write_bytes(результат.stderr)
            (Вивід/'ssh-output.txt').write_bytes(результат.stdout)
            assert результат.returncode==0 and b'SSH_NATIVE_PASS' in результат.stdout, (результат.returncode,результат.stdout,результат.stderr)
            звіт_значення['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in результат.stderr, результат.stderr
            звіт_значення['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            результат=захищений_оболонка(Налаштування['ssh_password'], 'cd /example/java; java ПрикладВиводу; cd /')
            assert результат.returncode==0 and 'JAVA Вивід: 안녕하세요 😀'.encode() in результат.stdout,результат.stdout
            звіт_значення['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            результат=захищений_оболонка(Налаштування['ssh_password'], 'missing_remote_command')
            assert результат.returncode==127,результат.returncode
            звіт_значення['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            результат=захищений_оболонка(Налаштування['ssh_password'], 'cat /example/java/ПрикладВікна.java', ('-o', 'RekeyLimit=1K'))
            (Вивід/'ssh-rekey.log').write_bytes(результат.stderr)
            assert результат.returncode==0 and 'class ПрикладВікна'.encode() in результат.stdout, (результат.returncode,результат.stdout,результат.stderr)
            assert результат.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, результат.stderr
            звіт_значення['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(оболонка_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=середовище,start_new_session=True,bufsize=0)
            транскрипт=bytearray();вибране_значення=selectors.DefaultSelector();вибране_значення.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(показувати_значення):
                крайнiй_термін_значення=time.monotonic()+30
                while показувати_значення not in транскрипт:
                    if time.monotonic()>крайнiй_термін_значення or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(показувати_значення)+' '+repr(bytes(транскрипт)))
                    for запис_значення_962f286b,_ in вибране_значення.select(.1):
                        조각=запис_значення_962f286b.fileobj.read(4096)
                        if 조각:транскрипт.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,ПОМИЛКА=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in ПОМИЛКА,(대화.returncode,ПОМИЛКА)
                (Вивід/'ssh-interactive.txt').write_bytes(транскрипт+나머지)
            finally:
                вибране_значення.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            звіт_значення['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(З_єднання, 수):
                дані=bytearray()
                while len(дані)<수:
                    блок_значення=З_єднання.recv(수-len(дані))
                    if not блок_значення: raise AssertionError('RFB EOF')
                    дані.extend(блок_значення)
                return bytes(дані)
            def 화면인증(пароль_значення):
                З_єднання=socket.create_connection(('127.0.0.5',화면포트),10);З_єднання.settimeout(30)
                assert 정확히(З_єднання,12)==b'RFB 003.008\n'
                З_єднання.sendall(b'RFB 003.008\n');assert 정확히(З_єднання,2)==b'\x01\x02'
                З_єднання.sendall(b'\x02');виклик_значення=정확히(З_єднання,16)
                입력암호=пароль_значення.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                З_єднання.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(виклик_значення))
                Стан_значення=struct.unpack('!I',정확히(З_єднання,4))[0]
                return З_єднання,Стан_значення
            недійсний_пароль='!' if not Налаштування['vnc_password'].startswith('!') else '?'
            З_єднання,Стан_значення=화면인증(недійсний_пароль);assert Стан_значення==1;З_єднання.close();time.sleep(.6)
            звіт_значення['checks'].append('VNC incorrect password rejected')
            З_єднання,Стан_значення=화면인증(Налаштування['vnc_password']);assert Стан_значення==0
            with З_єднання:
                З_єднання.sendall(b'\x01');початковий_стан=정확히(З_єднання,24);너비,높이=struct.unpack('!HH',початковий_стан[:4]);Назва=정확히(З_єднання,struct.unpack('!I',початковий_стан[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Назва
                def 화면(крок_приросту_крок=0):
                    З_єднання.sendall(struct.pack('!BBHHHH',3,крок_приросту_крок,0,0,너비,높이));머리=정확히(З_єднання,4);수=struct.unpack('!H',머리[2:])[0];усього_значення=0
                    малювання_значення=bytearray(너비*높이*4)
                    for _ in range(수):
                        координата_X,세로좌표,영역너비,영역높이,метод_режим=struct.unpack('!HHHHi',정확히(З_єднання,12));assert метод_режим==0 and координата_X+영역너비<=너비 and 세로좌표+영역높이<=높이
                        елемент_зображення=정확히(З_єднання,영역너비*영역높이*4);усього_значення+=len(елемент_зображення)
                        for рядок_введення in range(영역높이):малювання_значення[((세로좌표+рядок_введення)*너비+координата_X)*4:((세로좌표+рядок_введення)*너비+координата_X+영역너비)*4]=елемент_зображення[рядок_введення*영역너비*4:(рядок_введення+1)*영역너비*4]
                    if not крок_приросту_крок:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(малювання_значення),'raw','BGRX').save(str(Вивід/'native-vnc.png'))
                    return 수,усього_значення
                수,усього_значення=화면();assert 수>0 and усього_значення==너비*높이*4
                звіт_значення['checks'].append('Native framebuffer RFB full update {} bytes'.format(усього_значення))
                수,усього_значення=화면(1);assert усього_значення<너비*높이*4
                звіт_значення['checks'].append('RFB incremental update')
                처음=len(журнал_запис)
                for символ_значення_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if символ_значення_068c2631=='\r' else ord(символ_значення_068c2631)
                    З_єднання.sendall(struct.pack('!BBHI',4,1,0,символ));З_єднання.sendall(struct.pack('!BBHI',4,0,0,символ))
                стан_очікування(b'VNC_NATIVE_PASS',처음)
                звіт_значення['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ключ_розчерк(символ,натиснути_значення=1):З_єднання.sendall(struct.pack('!BBHI',4,натиснути_значення,0,символ))
                처음=len(журнал_запис)
                for символ_значення_068c2631 in 'echo ':Ключ_розчерк(ord(символ_значення_068c2631))
                Ключ_розчерк(0xffc6)
                for символ_значення_068c2631 in 'gksrmf':Ключ_розчерк(ord(символ_значення_068c2631))
                Ключ_розчерк(0xffc6);Ключ_розчерк(0xff0d)
                стан_очікування('\r\n한글\r\n'.encode(),처음)
                звіт_значення['checks'].append('Native VNC F9 two-set Hangul composition')
                З_єднання.sendall(struct.pack('!BBHH',5,0,120,100))
                звіт_значення['checks'].append('VNC pointer input accepted')
            процес_значення.stdin.write(b'poweroff\n');процес_значення.stdin.flush();процес_значення.wait(timeout=15);assert процес_значення.returncode==0
            звіт_значення['passed']=True
    finally:
        if процес_значення and процес_значення.poll() is None:
            процес_значення.terminate()
            try: процес_значення.wait(timeout=5)
            except subprocess.TimeoutExpired: процес_значення.kill();процес_значення.wait()
        (Вивід/'serial.log').write_bytes(журнал_запис)
        (Вивід/'report.json').write_text(json.dumps(звіт_значення,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(звіт_значення,ensure_ascii=False,indent=2))


if __name__=='__main__': запустити()
