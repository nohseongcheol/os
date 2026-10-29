#!/usr/bin/env python3
"""актуалдуу_берилмелер OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from аткаруу_буйрук import 기준, Команда
from 통신다리 import 통신다리


def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    Чыгыш = 인수.output
    Чыгыш.mkdir(parents=True, exist_ok=True)
    Орнотуулар = json.loads(인수.access.read_text())
    отчет_маани_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def бош_порт():
        with socket.socket() as Туташуу:
            Туташуу.bind(('127.0.0.5', 0))
            return Туташуу.getsockname()[1]
    сырты_порт, 화면포트, файл_порт = бош_порт(), бош_порт(), бош_порт()
    жазуу_катар = bytearray()
    Процесс_маани = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(файл_порт,
                ['tcp:{}:22'.format(сырты_порт), 'tcp:{}:5900'.format(화면포트)], кабылдоо_дарек='127.0.0.5') as 다리:
            실행인수 = Команда()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Процесс_маани = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    берилмелер = Процесс_маани.stdout.read(4096)
                    if not берилмелер: break
                    жазуу_катар.extend(берилмелер)
            трэд_маани = threading.Thread(target=수집, daemon=True)
            трэд_маани.start()
            def 기다림(Сөз_СМС, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Сөз_СМС not in жазуу_катар[처음:]:
                    if time.monotonic()>끝 or Процесс_маани.poll() is not None:
                        raise AssertionError('Missing '+repr(Сөз_СМС)+'\n'+жазуу_катар[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def коопсуз_сырты(жашыруун_сөз_маани, аткаруу_буйругу_маани, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=жашыруун_сөз_маани
                인수=['ssh','-v']+list(추가)+['-p',str(сырты_порт),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',аткаруу_буйругу_маани]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=коопсуз_сырты('!' + Орнотуулар['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Чыгыш/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in жазуу_катар, 결과.stderr
            отчет_маани_ddf2aaf3['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=коопсуз_сырты(Орнотуулар['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Чыгыш/'ssh.log').write_bytes(결과.stderr)
            (Чыгыш/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            отчет_маани_ddf2aaf3['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            отчет_маани_ddf2aaf3['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=коопсуз_сырты(Орнотуулар['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA Чыгыш: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            отчет_маани_ddf2aaf3['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=коопсуз_сырты(Орнотуулар['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            отчет_маани_ddf2aaf3['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=коопсуз_сырты(Орнотуулар['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Чыгыш/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            отчет_маани_ddf2aaf3['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(сырты_порт),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            интерактивдүү_сеанс=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();белгилөө_маани=selectors.DefaultSelector();белгилөө_маани.register(интерактивдүү_сеанс.stdout,selectors.EVENT_READ)
            def 대화읽기(көрсөтүү_маани):
                마감=time.monotonic()+30
                while көрсөтүү_маани not in 대화기록:
                    if time.monotonic()>마감 or интерактивдүү_сеанс.poll() is not None:raise AssertionError('SSH interactive missing '+repr(көрсөтүү_маани)+' '+repr(bytes(대화기록)))
                    for киргизме_жазуу_маани,_ in белгилөө_маани.select(.1):
                        조각=киргизме_жазуу_маани.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                интерактивдүү_сеанс.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');интерактивдүү_сеанс.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                интерактивдүү_сеанс.stdin.write(b'\x04');интерактивдүү_сеанс.stdin.flush();나머지,Ката=интерактивдүү_сеанс.communicate(timeout=15)
                assert интерактивдүү_сеанс.returncode==0 and b'PTY allocation request failed' not in Ката,(интерактивдүү_сеанс.returncode,Ката)
                (Чыгыш/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                белгилөө_маани.close()
                if интерактивдүү_сеанс.poll() is None:интерактивдүү_сеанс.kill();интерактивдүү_сеанс.wait()
            отчет_маани_ddf2aaf3['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Туташуу, 수):
                берилмелер=bytearray()
                while len(берилмелер)<수:
                    덩이=Туташуу.recv(수-len(берилмелер))
                    if not 덩이: raise AssertionError('RFB EOF')
                    берилмелер.extend(덩이)
                return bytes(берилмелер)
            def 화면인증(жашыруун_сөз_маани):
                Туташуу=socket.create_connection(('127.0.0.5',화면포트),10);Туташуу.settimeout(30)
                assert 정확히(Туташуу,12)==b'RFB 003.008\n'
                Туташуу.sendall(b'RFB 003.008\n');assert 정확히(Туташуу,2)==b'\x01\x02'
                Туташуу.sendall(b'\x02');текшерүү_маани=정확히(Туташуу,16)
                입력암호=жашыруун_сөз_маани.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Туташуу.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(текшерүү_маани))
                абал_маани=struct.unpack('!I',정확히(Туташуу,4))[0]
                return Туташуу,абал_маани
            бузук_жашыруун_сөз='!' if not Орнотуулар['vnc_password'].startswith('!') else '?'
            Туташуу,абал_маани=화면인증(бузук_жашыруун_сөз);assert абал_маани==1;Туташуу.close();time.sleep(.6)
            отчет_маани_ddf2aaf3['checks'].append('VNC incorrect password rejected')
            Туташуу,абал_маани=화면인증(Орнотуулар['vnc_password']);assert абал_маани==0
            with Туташуу:
                Туташуу.sendall(b'\x01');초기=정확히(Туташуу,24);너비,높이=struct.unpack('!HH',초기[:4]);Аты=정확히(Туташуу,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Аты
                def 화면(증분=0):
                    Туташуу.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Туташуу,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    чийүү_маани=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_координата,세로좌표,영역너비,영역높이,ыкма_режим=struct.unpack('!HHHHi',정확히(Туташуу,12));assert ыкма_режим==0 and x_координата+영역너비<=너비 and 세로좌표+영역높이<=높이
                        пиксел=정확히(Туташуу,영역너비*영역높이*4);합계+=len(пиксел)
                        for сап in range(영역높이):чийүү_маани[((세로좌표+сап)*너비+x_координата)*4:((세로좌표+сап)*너비+x_координата+영역너비)*4]=пиксел[сап*영역너비*4:(сап+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(чийүү_маани),'raw','BGRX').save(str(Чыгыш/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                отчет_маани_ddf2aaf3['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                отчет_маани_ddf2aaf3['checks'].append('RFB incremental update')
                처음=len(жазуу_катар)
                for символ_маани_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    символ=0xff0d if символ_маани_068c2631=='\r' else ord(символ_маани_068c2631)
                    Туташуу.sendall(struct.pack('!BBHI',4,1,0,символ));Туташуу.sendall(struct.pack('!BBHI',4,0,0,символ))
                기다림(b'VNC_NATIVE_PASS',처음)
                отчет_маани_ddf2aaf3['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(символ,누름=1):Туташуу.sendall(struct.pack('!BBHI',4,누름,0,символ))
                처음=len(жазуу_катар)
                for символ_маани_068c2631 in 'echo ':글쇠(ord(символ_маани_068c2631))
                글쇠(0xffc6)
                for символ_маани_068c2631 in 'gksrmf':글쇠(ord(символ_маани_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                отчет_маани_ddf2aaf3['checks'].append('Native VNC F9 two-set Hangul composition')
                Туташуу.sendall(struct.pack('!BBHH',5,0,120,100))
                отчет_маани_ddf2aaf3['checks'].append('VNC pointer input accepted')
            Процесс_маани.stdin.write(b'poweroff\n');Процесс_маани.stdin.flush();Процесс_маани.wait(timeout=15);assert Процесс_маани.returncode==0
            отчет_маани_ddf2aaf3['passed']=True
    finally:
        if Процесс_маани and Процесс_маани.poll() is None:
            Процесс_маани.terminate()
            try: Процесс_маани.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс_маани.kill();Процесс_маани.wait()
        (Чыгыш/'serial.log').write_bytes(жазуу_катар)
        (Чыгыш/'report.json').write_text(json.dumps(отчет_маани_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(отчет_маани_ddf2aaf3,ensure_ascii=False,indent=2))


if __name__=='__main__': Жүргүзүү()
