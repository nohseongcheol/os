#!/usr/bin/env python3
"""фактический_данные OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from 실행 import задача_корень, команда
from мост_3de4fe3a import мост_3de4fe3a


def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--kernel', type=Path, default=задача_корень / 'build/kernel8.img')
    анализатор_48ee4b1b.add_argument('--access', type=Path, default=задача_корень / 'build/remote/access.json')
    анализатор_48ee4b1b.add_argument('--output', type=Path, default=задача_корень / 'build/verification/native-remote')
    аргументы = анализатор_48ee4b1b.parse_args()
    текстовыйВывод = аргументы.output
    текстовыйВывод.mkdir(parents=True, exist_ok=True)
    Настройки = json.loads(аргументы.access.read_text())
    Отчет_ЗНАЧЕН = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(аргументы.kernel.read_bytes()).hexdigest(), 'checks': []}
    def пустой_порт():
        with socket.socket() as Подключить:
            Подключить.bind(('127.0.0.5', 0))
            return Подключить.getsockname()[1]
    оболочка_порт, экран_порт, файловый_порт = пустой_порт(), пустой_порт(), пустой_порт()
    LOG_ЗАПИСЬ = bytearray()
    Процесс_ЗНАЧЕН = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, мост_3de4fe3a(файловый_порт,
                ['tcp:{}:22'.format(оболочка_порт), 'tcp:{}:5900'.format(экран_порт)], адрес_узла='127.0.0.5') as мост_ЗНАЧЕН:
            실행인수 = команда()
            실행인수[실행인수.index('-kernel') + 1] = str(аргументы.kernel.resolve())
            Процесс_ЗНАЧЕН = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + мост_ЗНАЧЕН.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    данные = Процесс_ЗНАЧЕН.stdout.read(4096)
                    if not данные: break
                    LOG_ЗАПИСЬ.extend(данные)
            поток_ЗНАЧЕН_5b72a632 = threading.Thread(target=수집, daemon=True)
            поток_ЗНАЧЕН_5b72a632.start()
            def состояние_ожидания(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_ЗАПИСЬ[처음:]:
                    if time.monotonic()>끝 or Процесс_ЗНАЧЕН.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_ЗАПИСЬ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            состояние_ожидания(b'jkoros-native> ')
            вспомогательное_приложение_ЗНАЧЕН = Path(임시)/'askpass'
            вспомогательное_приложение_ЗНАЧЕН.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            вспомогательное_приложение_ЗНАЧЕН.chmod(0o700)
            среда = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(вспомогательное_приложение_ЗНАЧЕН), SSH_ASKPASS_REQUIRE='force')
            def SSH(пароль_ЗНАЧЕН, 명령어, добавить_ввод=()):
                среда['JKOROS_TEST_PASSWORD']=пароль_ЗНАЧЕН
                аргументы=['ssh','-v']+list(добавить_ввод)+['-p',str(оболочка_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                результат=subprocess.run(аргументы,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=среда,start_new_session=True,timeout=50)
                return результат
            результат=SSH('!' + Настройки['ssh_password'], 'echo SHOULD_NOT_RUN')
            (текстовыйВывод/'ssh-rejected.log').write_bytes(результат.stderr)
            assert результат.returncode!=0 and b'Permission denied' in результат.stderr and b'SHOULD_NOT_RUN' not in LOG_ЗАПИСЬ, результат.stderr
            Отчет_ЗНАЧЕН['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            результат=SSH(Настройки['ssh_password'], 'echo SSH_NATIVE_PASS')
            (текстовыйВывод/'ssh.log').write_bytes(результат.stderr)
            (текстовыйВывод/'ssh-output.txt').write_bytes(результат.stdout)
            assert результат.returncode==0 and b'SSH_NATIVE_PASS' in результат.stdout, (результат.returncode,результат.stdout,результат.stderr)
            Отчет_ЗНАЧЕН['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in результат.stderr, результат.stderr
            Отчет_ЗНАЧЕН['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            результат=SSH(Настройки['ssh_password'], 'cd /example/java; java ПримерВывода; cd /')
            assert результат.returncode==0 and 'JAVA текстовыйВывод: 안녕하세요 😀'.encode() in результат.stdout,результат.stdout
            Отчет_ЗНАЧЕН['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            результат=SSH(Настройки['ssh_password'], 'missing_remote_command')
            assert результат.returncode==127,результат.returncode
            Отчет_ЗНАЧЕН['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            результат=SSH(Настройки['ssh_password'], 'cat /example/java/ПримерОкна.java', ('-o', 'RekeyLimit=1K'))
            (текстовыйВывод/'ssh-rekey.log').write_bytes(результат.stderr)
            assert результат.returncode==0 and 'class ПримерОкна'.encode() in результат.stdout, (результат.returncode,результат.stdout,результат.stderr)
            assert результат.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, результат.stderr
            Отчет_ЗНАЧЕН['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(оболочка_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивный_сеанс=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=среда,start_new_session=True,bufsize=0)
            расшифровка=bytearray();выделение_ЗНАЧЕН=selectors.DefaultSelector();выделение_ЗНАЧЕН.register(интерактивный_сеанс.stdout,selectors.EVENT_READ)
            def чтение_интерактивный(выпуск_ЗНАЧЕН):
                крайний_срок_ЗНАЧЕН=time.monotonic()+30
                while выпуск_ЗНАЧЕН not in расшифровка:
                    if time.monotonic()>крайний_срок_ЗНАЧЕН or интерактивный_сеанс.poll() is not None:raise AssertionError('SSH interactive missing '+repr(выпуск_ЗНАЧЕН)+' '+repr(bytes(расшифровка)))
                    for ввод_ЗНАЧЕН,_ in выделение_ЗНАЧЕН.select(.1):
                        блок_ЗНАЧЕН_652d4b53=ввод_ЗНАЧЕН.fileobj.read(4096)
                        if блок_ЗНАЧЕН_652d4b53:расшифровка.extend(блок_ЗНАЧЕН_652d4b53)
            try:
                чтение_интерактивный(b'shared native console')
                интерактивный_сеанс.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивный_сеанс.stdin.flush();чтение_интерактивный(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивный_сеанс.stdin.write(b'\x04');интерактивный_сеанс.stdin.flush();나머지,ошибка=интерактивный_сеанс.communicate(timeout=15)
                assert интерактивный_сеанс.returncode==0 and b'PTY allocation request failed' not in ошибка,(интерактивный_сеанс.returncode,ошибка)
                (текстовыйВывод/'ssh-interactive.txt').write_bytes(расшифровка+나머지)
            finally:
                выделение_ЗНАЧЕН.close()
                if интерактивный_сеанс.poll() is None:интерактивный_сеанс.kill();интерактивный_сеанс.wait()
            Отчет_ЗНАЧЕН['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Подключить, 수):
                данные=bytearray()
                while len(данные)<수:
                    блок_ЗНАЧЕН=Подключить.recv(수-len(данные))
                    if not блок_ЗНАЧЕН: raise AssertionError('RFB EOF')
                    данные.extend(блок_ЗНАЧЕН)
                return bytes(данные)
            def экран_аутентификация(пароль_ЗНАЧЕН):
                Подключить=socket.create_connection(('127.0.0.5',экран_порт),10);Подключить.settimeout(30)
                assert 정확히(Подключить,12)==b'RFB 003.008\n'
                Подключить.sendall(b'RFB 003.008\n');assert 정확히(Подключить,2)==b'\x01\x02'
                Подключить.sendall(b'\x02');испытание_ЗНАЧЕН=정확히(Подключить,16)
                входные_данные_пароль=пароль_ЗНАЧЕН.encode('ascii')[:8].ljust(8, b'\0')
                Ключ_материал=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in входные_данные_пароль)
                Подключить.sendall(DES.new(Ключ_материал,DES.MODE_ECB).encrypt(испытание_ЗНАЧЕН))
                Состояние_ЗНАЧЕН=struct.unpack('!I',정확히(Подключить,4))[0]
                return Подключить,Состояние_ЗНАЧЕН
            неверный_пароль='!' if not Настройки['vnc_password'].startswith('!') else '?'
            Подключить,Состояние_ЗНАЧЕН=экран_аутентификация(неверный_пароль);assert Состояние_ЗНАЧЕН==1;Подключить.close();time.sleep(.6)
            Отчет_ЗНАЧЕН['checks'].append('VNC incorrect password rejected')
            Подключить,Состояние_ЗНАЧЕН=экран_аутентификация(Настройки['vnc_password']);assert Состояние_ЗНАЧЕН==0
            with Подключить:
                Подключить.sendall(b'\x01');начальное_состояние=정확히(Подключить,24);너비,높이=struct.unpack('!HH',начальное_состояние[:4]);Название=정확히(Подключить,struct.unpack('!I',начальное_состояние[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Название
                def экран(увеличить_шаг=0):
                    Подключить.sendall(struct.pack('!BBHHHH',3,увеличить_шаг,0,0,너비,높이));HEAD_ЗНАЧЕН=정확히(Подключить,4);수=struct.unpack('!H',HEAD_ЗНАЧЕН[2:])[0];итог_ЗНАЧЕН=0
                    рисунок_ЗНАЧЕН=bytearray(너비*높이*4)
                    for _ in range(수):
                        координата_X,Y_координата,영역너비,영역높이,метод_МОДА=struct.unpack('!HHHHi',정확히(Подключить,12));assert метод_МОДА==0 and координата_X+영역너비<=너비 and Y_координата+영역높이<=높이
                        пиксель=정확히(Подключить,영역너비*영역높이*4);итог_ЗНАЧЕН+=len(пиксель)
                        for строка_ввода in range(영역높이):рисунок_ЗНАЧЕН[((Y_координата+строка_ввода)*너비+координата_X)*4:((Y_координата+строка_ввода)*너비+координата_X+영역너비)*4]=пиксель[строка_ввода*영역너비*4:(строка_ввода+1)*영역너비*4]
                    if not увеличить_шаг:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(рисунок_ЗНАЧЕН),'raw','BGRX').save(str(текстовыйВывод/'native-vnc.png'))
                    return 수,итог_ЗНАЧЕН
                수,итог_ЗНАЧЕН=экран();assert 수>0 and итог_ЗНАЧЕН==너비*높이*4
                Отчет_ЗНАЧЕН['checks'].append('Native framebuffer RFB full update {} bytes'.format(итог_ЗНАЧЕН))
                수,итог_ЗНАЧЕН=экран(1);assert итог_ЗНАЧЕН<너비*높이*4
                Отчет_ЗНАЧЕН['checks'].append('RFB incremental update')
                처음=len(LOG_ЗАПИСЬ)
                for знак_ЗНАЧЕН in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if знак_ЗНАЧЕН=='\r' else ord(знак_ЗНАЧЕН)
                    Подключить.sendall(struct.pack('!BBHI',4,1,0,символ));Подключить.sendall(struct.pack('!BBHI',4,0,0,символ))
                состояние_ожидания(b'VNC_NATIVE_PASS',처음)
                Отчет_ЗНАЧЕН['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Ключ_штрих(символ,누름=1):Подключить.sendall(struct.pack('!BBHI',4,누름,0,символ))
                처음=len(LOG_ЗАПИСЬ)
                for знак_ЗНАЧЕН in 'echo ':Ключ_штрих(ord(знак_ЗНАЧЕН))
                Ключ_штрих(0xffc6)
                for знак_ЗНАЧЕН in 'gksrmf':Ключ_штрих(ord(знак_ЗНАЧЕН))
                Ключ_штрих(0xffc6);Ключ_штрих(0xff0d)
                состояние_ожидания('\r\n한글\r\n'.encode(),처음)
                Отчет_ЗНАЧЕН['checks'].append('Native VNC F9 two-set Hangul composition')
                Подключить.sendall(struct.pack('!BBHH',5,0,120,100))
                Отчет_ЗНАЧЕН['checks'].append('VNC pointer input accepted')
            Процесс_ЗНАЧЕН.stdin.write(b'poweroff\n');Процесс_ЗНАЧЕН.stdin.flush();Процесс_ЗНАЧЕН.wait(timeout=15);assert Процесс_ЗНАЧЕН.returncode==0
            Отчет_ЗНАЧЕН['passed']=True
    finally:
        if Процесс_ЗНАЧЕН and Процесс_ЗНАЧЕН.poll() is None:
            Процесс_ЗНАЧЕН.terminate()
            try: Процесс_ЗНАЧЕН.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс_ЗНАЧЕН.kill();Процесс_ЗНАЧЕН.wait()
        (текстовыйВывод/'serial.log').write_bytes(LOG_ЗАПИСЬ)
        (текстовыйВывод/'report.json').write_text(json.dumps(Отчет_ЗНАЧЕН,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Отчет_ЗНАЧЕН,ensure_ascii=False,indent=2))


if __name__=='__main__': запустить()
