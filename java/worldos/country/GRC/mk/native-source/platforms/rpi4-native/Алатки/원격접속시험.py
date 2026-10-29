#!/usr/bin/env python3
"""реален_податоци OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Изврши_наредба import Project_корен, Команда
from Мрежа_мост import Мрежа_мост


def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--kernel', type=Path, default=Project_корен / 'build/kernel8.img')
    анализатор_48ee4b1b.add_argument('--access', type=Path, default=Project_корен / 'build/remote/access.json')
    анализатор_48ee4b1b.add_argument('--output', type=Path, default=Project_корен / 'build/verification/native-remote')
    Аргументи = анализатор_48ee4b1b.parse_args()
    출력 = Аргументи.output
    출력.mkdir(parents=True, exist_ok=True)
    Подесувања = json.loads(Аргументи.access.read_text())
    извештај_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Аргументи.kernel.read_bytes()).hexdigest(), 'checks': []}
    def празно_порта():
        with socket.socket() as Врзи_се:
            Врзи_се.bind(('127.0.0.5', 0))
            return Врзи_се.getsockname()[1]
    обвивка_порта, 화면포트, датотека_порта = празно_порта(), празно_порта(), празно_порта()
    LOG_ред = bytearray()
    Процес_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Мрежа_мост(датотека_порта,
                ['tcp:{}:22'.format(обвивка_порта), 'tcp:{}:5900'.format(화면포트)], вдоми_адреса='127.0.0.5') as мост_VALUE:
            실행인수 = Команда()
            실행인수[실행인수.index('-kernel') + 1] = str(Аргументи.kernel.resolve())
            Процес_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + мост_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    податоци = Процес_VALUE.stdout.read(4096)
                    if not податоци: break
                    LOG_ред.extend(податоци)
            нишка_VALUE = threading.Thread(target=수집, daemon=True)
            нишка_VALUE.start()
            def почекај_статус(Word_СМС, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_СМС not in LOG_ред[처음:]:
                    if time.monotonic()>끝 or Процес_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_СМС)+'\n'+LOG_ред[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            почекај_статус(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def безбедно_обвивка(лозинка_VALUE, инструкција_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=лозинка_VALUE
                Аргументи=['ssh','-v']+list(추가)+['-p',str(обвивка_порта),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',инструкција_VALUE]
                мерка=subprocess.run(Аргументи,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return мерка
            мерка=безбедно_обвивка('!' + Подесувања['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(мерка.stderr)
            assert мерка.returncode!=0 and b'Permission denied' in мерка.stderr and b'SHOULD_NOT_RUN' not in LOG_ред, мерка.stderr
            извештај_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            мерка=безбедно_обвивка(Подесувања['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(мерка.stderr)
            (출력/'ssh-output.txt').write_bytes(мерка.stdout)
            assert мерка.returncode==0 and b'SSH_NATIVE_PASS' in мерка.stdout, (мерка.returncode,мерка.stdout,мерка.stderr)
            извештај_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in мерка.stderr, мерка.stderr
            извештај_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            мерка=безбедно_обвивка(Подесувања['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert мерка.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in мерка.stdout,мерка.stdout
            извештај_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            мерка=безбедно_обвивка(Подесувања['ssh_password'], 'missing_remote_command')
            assert мерка.returncode==127,мерка.returncode
            извештај_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            мерка=безбедно_обвивка(Подесувања['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(мерка.stderr)
            assert мерка.returncode==0 and 'class 창예제'.encode() in мерка.stdout, (мерка.returncode,мерка.stdout,мерка.stderr)
            assert мерка.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, мерка.stderr
            извештај_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(обвивка_порта),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивен_сесија=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();селекција_VALUE=selectors.DefaultSelector();селекција_VALUE.register(интерактивен_сесија.stdout,selectors.EVENT_READ)
            def 대화읽기(прикажи_VALUE):
                마감=time.monotonic()+30
                while прикажи_VALUE not in 대화기록:
                    if time.monotonic()>마감 or интерактивен_сесија.poll() is not None:raise AssertionError('SSH interactive missing '+repr(прикажи_VALUE)+' '+repr(bytes(대화기록)))
                    for внес_VALUE,_ in селекција_VALUE.select(.1):
                        조각=внес_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактивен_сесија.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивен_сесија.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивен_сесија.stdin.write(b'\x04');интерактивен_сесија.stdin.flush();나머지,ГРЕШКА=интерактивен_сесија.communicate(timeout=15)
                assert интерактивен_сесија.returncode==0 and b'PTY allocation request failed' not in ГРЕШКА,(интерактивен_сесија.returncode,ГРЕШКА)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                селекција_VALUE.close()
                if интерактивен_сесија.poll() is None:интерактивен_сесија.kill();интерактивен_сесија.wait()
            извештај_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Врзи_се, 수):
                податоци=bytearray()
                while len(податоци)<수:
                    덩이=Врзи_се.recv(수-len(податоци))
                    if not 덩이: raise AssertionError('RFB EOF')
                    податоци.extend(덩이)
                return bytes(податоци)
            def 화면인증(лозинка_VALUE):
                Врзи_се=socket.create_connection(('127.0.0.5',화면포트),10);Врзи_се.settimeout(30)
                assert 정확히(Врзи_се,12)==b'RFB 003.008\n'
                Врзи_се.sendall(b'RFB 003.008\n');assert 정확히(Врзи_се,2)==b'\x01\x02'
                Врзи_се.sendall(b'\x02');предизвик_VALUE=정확히(Врзи_се,16)
                입력암호=лозинка_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Врзи_се.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(предизвик_VALUE))
                статус_VALUE=struct.unpack('!I',정확히(Врзи_се,4))[0]
                return Врзи_се,статус_VALUE
            неважечки_лозинка='!' if not Подесувања['vnc_password'].startswith('!') else '?'
            Врзи_се,статус_VALUE=화면인증(неважечки_лозинка);assert статус_VALUE==1;Врзи_се.close();time.sleep(.6)
            извештај_VALUE['checks'].append('VNC incorrect password rejected')
            Врзи_се,статус_VALUE=화면인증(Подесувања['vnc_password']);assert статус_VALUE==0
            with Врзи_се:
                Врзи_се.sendall(b'\x01');초기=정확히(Врзи_се,24);너비,높이=struct.unpack('!HH',초기[:4]);Име=정확히(Врзи_се,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Име
                def 화면(증분=0):
                    Врзи_се.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Врзи_се,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    цртеж_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        координата_х,세로좌표,영역너비,영역높이,метод_MODE=struct.unpack('!HHHHi',정확히(Врзи_се,12));assert метод_MODE==0 and координата_х+영역너비<=너비 and 세로좌표+영역높이<=높이
                        пиксел=정확히(Врзи_се,영역너비*영역높이*4);합계+=len(пиксел)
                        for ред in range(영역높이):цртеж_VALUE[((세로좌표+ред)*너비+координата_х)*4:((세로좌표+ред)*너비+координата_х+영역너비)*4]=пиксел[ред*영역너비*4:(ред+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(цртеж_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                извештај_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                извештај_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_ред)
                for знак_VALUE in 'echo VNC_NATIVE_PASS\r':
                    симбол=0xff0d if знак_VALUE=='\r' else ord(знак_VALUE)
                    Врзи_се.sendall(struct.pack('!BBHI',4,1,0,симбол));Врзи_се.sendall(struct.pack('!BBHI',4,0,0,симбол))
                почекај_статус(b'VNC_NATIVE_PASS',처음)
                извештај_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(симбол,누름=1):Врзи_се.sendall(struct.pack('!BBHI',4,누름,0,симбол))
                처음=len(LOG_ред)
                for знак_VALUE in 'echo ':글쇠(ord(знак_VALUE))
                글쇠(0xffc6)
                for знак_VALUE in 'gksrmf':글쇠(ord(знак_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                почекај_статус('\r\n한글\r\n'.encode(),처음)
                извештај_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Врзи_се.sendall(struct.pack('!BBHH',5,0,120,100))
                извештај_VALUE['checks'].append('VNC pointer input accepted')
            Процес_VALUE.stdin.write(b'poweroff\n');Процес_VALUE.stdin.flush();Процес_VALUE.wait(timeout=15);assert Процес_VALUE.returncode==0
            извештај_VALUE['passed']=True
    finally:
        if Процес_VALUE and Процес_VALUE.poll() is None:
            Процес_VALUE.terminate()
            try: Процес_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес_VALUE.kill();Процес_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_ред)
        (출력/'report.json').write_text(json.dumps(извештај_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(извештај_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Изврши_2()
