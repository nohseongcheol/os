#!/usr/bin/env python3
"""стваран_подаци OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Изврши_команда import пројектовати_корен, Наредба
from Мрежа_мост import Мрежа_мост


def Покрени():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--kernel', type=Path, default=пројектовати_корен / 'build/kernel8.img')
    анализатор_48ee4b1b.add_argument('--access', type=Path, default=пројектовати_корен / 'build/remote/access.json')
    анализатор_48ee4b1b.add_argument('--output', type=Path, default=пројектовати_корен / 'build/verification/native-remote')
    Аргументи = анализатор_48ee4b1b.parse_args()
    Излаз = Аргументи.output
    Излаз.mkdir(parents=True, exist_ok=True)
    Поставке = json.loads(Аргументи.access.read_text())
    извештај_вриједност = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Аргументи.kernel.read_bytes()).hexdigest(), 'checks': []}
    def празно_порт():
        with socket.socket() as Повежи_се:
            Повежи_се.bind(('127.0.0.5', 0))
            return Повежи_се.getsockname()[1]
    љуска_порт, 화면포트, фајл_порт = празно_порт(), празно_порт(), празно_порт()
    евиденција_ред = bytearray()
    Процес_вриједност = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Мрежа_мост(фајл_порт,
                ['tcp:{}:22'.format(љуска_порт), 'tcp:{}:5900'.format(화면포트)], хост_адреса='127.0.0.5') as мост_вриједност:
            실행인수 = Наредба()
            실행인수[실행인수.index('-kernel') + 1] = str(Аргументи.kernel.resolve())
            Процес_вриједност = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + мост_вриједност.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    подаци = Процес_вриједност.stdout.read(4096)
                    if not подаци: break
                    евиденција_ред.extend(подаци)
            нит_вриједност = threading.Thread(target=수집, daemon=True)
            нит_вриједност.start()
            def чекај_стање(Укрштенице_Текст, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Укрштенице_Текст not in евиденција_ред[처음:]:
                    if time.monotonic()>끝 or Процес_вриједност.poll() is not None:
                        raise AssertionError('Missing '+repr(Укрштенице_Текст)+'\n'+евиденција_ред[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            чекај_стање(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            радно_окружење = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def безбедан_љуска(лозинка_вриједност, програмска_наредба_вриједност, додати_унос=()):
                радно_окружење['JKOROS_TEST_PASSWORD']=лозинка_вриједност
                Аргументи=['ssh','-v']+list(додати_унос)+['-p',str(љуска_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',програмска_наредба_вриједност]
                ИСХОД=subprocess.run(Аргументи,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=радно_окружење,start_new_session=True,timeout=50)
                return ИСХОД
            ИСХОД=безбедан_љуска('!' + Поставке['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Излаз/'ssh-rejected.log').write_bytes(ИСХОД.stderr)
            assert ИСХОД.returncode!=0 and b'Permission denied' in ИСХОД.stderr and b'SHOULD_NOT_RUN' not in евиденција_ред, ИСХОД.stderr
            извештај_вриједност['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ИСХОД=безбедан_љуска(Поставке['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Излаз/'ssh.log').write_bytes(ИСХОД.stderr)
            (Излаз/'ssh-output.txt').write_bytes(ИСХОД.stdout)
            assert ИСХОД.returncode==0 and b'SSH_NATIVE_PASS' in ИСХОД.stdout, (ИСХОД.returncode,ИСХОД.stdout,ИСХОД.stderr)
            извештај_вриједност['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ИСХОД.stderr, ИСХОД.stderr
            извештај_вриједност['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ИСХОД=безбедан_љуска(Поставке['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ИСХОД.returncode==0 and 'JAVA Излаз: 안녕하세요 😀'.encode() in ИСХОД.stdout,ИСХОД.stdout
            извештај_вриједност['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ИСХОД=безбедан_љуска(Поставке['ssh_password'], 'missing_remote_command')
            assert ИСХОД.returncode==127,ИСХОД.returncode
            извештај_вриједност['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ИСХОД=безбедан_љуска(Поставке['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Излаз/'ssh-rekey.log').write_bytes(ИСХОД.stderr)
            assert ИСХОД.returncode==0 and 'class 창예제'.encode() in ИСХОД.stdout, (ИСХОД.returncode,ИСХОД.stdout,ИСХОД.stderr)
            assert ИСХОД.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ИСХОД.stderr
            извештај_вриједност['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(љуска_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивно_сесија=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=радно_окружење,start_new_session=True,bufsize=0)
            транскрипт=bytearray();избор_вриједност=selectors.DefaultSelector();избор_вриједност.register(интерактивно_сесија.stdout,selectors.EVENT_READ)
            def 대화읽기(емисија_вриједност):
                마감=time.monotonic()+30
                while емисија_вриједност not in транскрипт:
                    if time.monotonic()>마감 or интерактивно_сесија.poll() is not None:raise AssertionError('SSH interactive missing '+repr(емисија_вриједност)+' '+repr(bytes(транскрипт)))
                    for унос_вриједност,_ in избор_вриједност.select(.1):
                        조각=унос_вриједност.fileobj.read(4096)
                        if 조각:транскрипт.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактивно_сесија.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивно_сесија.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивно_сесија.stdin.write(b'\x04');интерактивно_сесија.stdin.flush();나머지,ГРЕШКА=интерактивно_сесија.communicate(timeout=15)
                assert интерактивно_сесија.returncode==0 and b'PTY allocation request failed' not in ГРЕШКА,(интерактивно_сесија.returncode,ГРЕШКА)
                (Излаз/'ssh-interactive.txt').write_bytes(транскрипт+나머지)
            finally:
                избор_вриједност.close()
                if интерактивно_сесија.poll() is None:интерактивно_сесија.kill();интерактивно_сесија.wait()
            извештај_вриједност['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Повежи_се, 수):
                подаци=bytearray()
                while len(подаци)<수:
                    덩이=Повежи_се.recv(수-len(подаци))
                    if not 덩이: raise AssertionError('RFB EOF')
                    подаци.extend(덩이)
                return bytes(подаци)
            def 화면인증(лозинка_вриједност):
                Повежи_се=socket.create_connection(('127.0.0.5',화면포트),10);Повежи_се.settimeout(30)
                assert 정확히(Повежи_се,12)==b'RFB 003.008\n'
                Повежи_се.sendall(b'RFB 003.008\n');assert 정확히(Повежи_се,2)==b'\x01\x02'
                Повежи_се.sendall(b'\x02');тест_вриједност=정확히(Повежи_се,16)
                입력암호=лозинка_вриједност.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Повежи_се.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(тест_вриједност))
                стање_вриједност=struct.unpack('!I',정확히(Повежи_се,4))[0]
                return Повежи_се,стање_вриједност
            неважеће_лозинка='!' if not Поставке['vnc_password'].startswith('!') else '?'
            Повежи_се,стање_вриједност=화면인증(неважеће_лозинка);assert стање_вриједност==1;Повежи_се.close();time.sleep(.6)
            извештај_вриједност['checks'].append('VNC incorrect password rejected')
            Повежи_се,стање_вриједност=화면인증(Поставке['vnc_password']);assert стање_вриједност==0
            with Повежи_се:
                Повежи_се.sendall(b'\x01');초기=정확히(Повежи_се,24);너비,높이=struct.unpack('!HH',초기[:4]);Назив=정확히(Повежи_се,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Назив
                def 화면(증분=0):
                    Повежи_се.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Повежи_се,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    цртеж_вриједност=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_координата,дугме_Y_координата,영역너비,영역높이,метода_мод=struct.unpack('!HHHHi',정확히(Повежи_се,12));assert метода_мод==0 and x_координата+영역너비<=너비 and дугме_Y_координата+영역높이<=높이
                        пиксел=정확히(Повежи_се,영역너비*영역높이*4);합계+=len(пиксел)
                        for Ред in range(영역높이):цртеж_вриједност[((дугме_Y_координата+Ред)*너비+x_координата)*4:((дугме_Y_координата+Ред)*너비+x_координата+영역너비)*4]=пиксел[Ред*영역너비*4:(Ред+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(цртеж_вриједност),'raw','BGRX').save(str(Излаз/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                извештај_вриједност['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                извештај_вриједност['checks'].append('RFB incremental update')
                처음=len(евиденција_ред)
                for знак_вриједност in 'echo VNC_NATIVE_PASS\r':
                    симбол=0xff0d if знак_вриједност=='\r' else ord(знак_вриједност)
                    Повежи_се.sendall(struct.pack('!BBHI',4,1,0,симбол));Повежи_се.sendall(struct.pack('!BBHI',4,0,0,симбол))
                чекај_стање(b'VNC_NATIVE_PASS',처음)
                извештај_вриједност['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(симбол,отиснути_вриједност=1):Повежи_се.sendall(struct.pack('!BBHI',4,отиснути_вриједност,0,симбол))
                처음=len(евиденција_ред)
                for знак_вриједност in 'echo ':글쇠(ord(знак_вриједност))
                글쇠(0xffc6)
                for знак_вриједност in 'gksrmf':글쇠(ord(знак_вриједност))
                글쇠(0xffc6);글쇠(0xff0d)
                чекај_стање('\r\n한글\r\n'.encode(),처음)
                извештај_вриједност['checks'].append('Native VNC F9 two-set Hangul composition')
                Повежи_се.sendall(struct.pack('!BBHH',5,0,120,100))
                извештај_вриједност['checks'].append('VNC pointer input accepted')
            Процес_вриједност.stdin.write(b'poweroff\n');Процес_вриједност.stdin.flush();Процес_вриједност.wait(timeout=15);assert Процес_вриједност.returncode==0
            извештај_вриједност['passed']=True
    finally:
        if Процес_вриједност and Процес_вриједност.poll() is None:
            Процес_вриједност.terminate()
            try: Процес_вриједност.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес_вриједност.kill();Процес_вриједност.wait()
        (Излаз/'serial.log').write_bytes(евиденција_ред)
        (Излаз/'report.json').write_text(json.dumps(извештај_вриједност,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(извештај_вриједност,ensure_ascii=False,indent=2))


if __name__=='__main__': Покрени()
