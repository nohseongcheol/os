#!/usr/bin/env python3
"""իրական_տվյալ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from կատարել_հրաման import արձակել_արմատ, Հրահանգ
from Ցանց_կամուրջ import Ցանց_կամուրջ


def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=արձակել_արմատ / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=արձակել_արմատ / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=արձակել_արմատ / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    Ելք = 인수.output
    Ելք.mkdir(parents=True, exist_ok=True)
    Նախընտրանքներ = json.loads(인수.access.read_text())
    զեկույց_արժեք = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def դատարկ_միացք():
        with socket.socket() as Միացնել:
            Միացնել.bind(('127.0.0.5', 0))
            return Միացնել.getsockname()[1]
    խեցի_միացք, 화면포트, նիշք_միացք = դատարկ_միացք(), դատարկ_միացք(), դատարկ_միացք()
    մատյան_տող = bytearray()
    Ընթացք_արժեք = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Ցանց_կամուրջ(նիշք_միացք,
                ['tcp:{}:22'.format(խեցի_միացք), 'tcp:{}:5900'.format(화면포트)], հոստ_հասցե='127.0.0.5') as կամուրջ_արժեք:
            실행인수 = Հրահանգ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Ընթացք_արժեք = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + կամուրջ_արժեք.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    տվյալ = Ընթացք_արժեք.stdout.read(4096)
                    if not տվյալ: break
                    մատյան_տող.extend(տվյալ)
            շղթա_արժեք = threading.Thread(target=수집, daemon=True)
            շղթա_արժեք.start()
            def 기다림(Բառ_Գրվածք, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Բառ_Գրվածք not in մատյան_տող[처음:]:
                    if time.monotonic()>끝 or Ընթացք_արժեք.poll() is not None:
                        raise AssertionError('Missing '+repr(Բառ_Գրվածք)+'\n'+մատյան_տող[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def անվտանգ_խեցի(գաղտնաբառ_արժեք, հրահանգ_արժեք, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=գաղտնաբառ_արժեք
                인수=['ssh','-v']+list(추가)+['-p',str(խեցի_միացք),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',հրահանգ_արժեք]
                չափ=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return չափ
            չափ=անվտանգ_խեցի('!' + Նախընտրանքներ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Ելք/'ssh-rejected.log').write_bytes(չափ.stderr)
            assert չափ.returncode!=0 and b'Permission denied' in չափ.stderr and b'SHOULD_NOT_RUN' not in մատյան_տող, չափ.stderr
            զեկույց_արժեք['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            չափ=անվտանգ_խեցի(Նախընտրանքներ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Ելք/'ssh.log').write_bytes(չափ.stderr)
            (Ելք/'ssh-output.txt').write_bytes(չափ.stdout)
            assert չափ.returncode==0 and b'SSH_NATIVE_PASS' in չափ.stdout, (չափ.returncode,չափ.stdout,չափ.stderr)
            զեկույց_արժեք['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in չափ.stderr, չափ.stderr
            զեկույց_արժեք['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            չափ=անվտանգ_խեցի(Նախընտրանքներ['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert չափ.returncode==0 and 'JAVA Ելք: 안녕하세요 😀'.encode() in չափ.stdout,չափ.stdout
            զեկույց_արժեք['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            չափ=անվտանգ_խեցի(Նախընտրանքներ['ssh_password'], 'missing_remote_command')
            assert չափ.returncode==127,չափ.returncode
            զեկույց_արժեք['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            չափ=անվտանգ_խեցի(Նախընտրանքներ['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Ելք/'ssh-rekey.log').write_bytes(չափ.stderr)
            assert չափ.returncode==0 and 'class 창예제'.encode() in չափ.stdout, (չափ.returncode,չափ.stdout,չափ.stderr)
            assert չափ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, չափ.stderr
            զեկույց_արժեք['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(խեցի_միացք),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            փոխազդու_աշխատաշրջան=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ընտրվածք_արժեք=selectors.DefaultSelector();ընտրվածք_արժեք.register(փոխազդու_աշխատաշրջան.stdout,selectors.EVENT_READ)
            def 대화읽기(ցուցադրել_արժեք):
                마감=time.monotonic()+30
                while ցուցադրել_արժեք not in 대화기록:
                    if time.monotonic()>마감 or փոխազդու_աշխատաշրջան.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ցուցադրել_արժեք)+' '+repr(bytes(대화기록)))
                    for մուտքագրում_արժեք,_ in ընտրվածք_արժեք.select(.1):
                        조각=մուտքագրում_արժեք.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                փոխազդու_աշխատաշրջան.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');փոխազդու_աշխատաշրջան.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                փոխազդու_աշխատաշրջան.stdin.write(b'\x04');փոխազդու_աշխատաշրջան.stdin.flush();나머지,Սխալ=փոխազդու_աշխատաշրջան.communicate(timeout=15)
                assert փոխազդու_աշխատաշրջան.returncode==0 and b'PTY allocation request failed' not in Սխալ,(փոխազդու_աշխատաշրջան.returncode,Սխալ)
                (Ելք/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ընտրվածք_արժեք.close()
                if փոխազդու_աշխատաշրջան.poll() is None:փոխազդու_աշխատաշրջան.kill();փոխազդու_աշխատաշրջան.wait()
            զեկույց_արժեք['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Միացնել, 수):
                տվյալ=bytearray()
                while len(տվյալ)<수:
                    덩이=Միացնել.recv(수-len(տվյալ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    տվյալ.extend(덩이)
                return bytes(տվյալ)
            def 화면인증(գաղտնաբառ_արժեք):
                Միացնել=socket.create_connection(('127.0.0.5',화면포트),10);Միացնել.settimeout(30)
                assert 정확히(Միացնել,12)==b'RFB 003.008\n'
                Միացնել.sendall(b'RFB 003.008\n');assert 정확히(Միացնել,2)==b'\x01\x02'
                Միացնել.sendall(b'\x02');իսկորոշում_արժեք=정확히(Միացնել,16)
                입력암호=գաղտնաբառ_արժեք.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Միացնել.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(իսկորոշում_արժեք))
                վիճակ_արժեք=struct.unpack('!I',정확히(Միացնել,4))[0]
                return Միացնել,վիճակ_արժեք
            անվավեր_գաղտնաբառ='!' if not Նախընտրանքներ['vnc_password'].startswith('!') else '?'
            Միացնել,վիճակ_արժեք=화면인증(անվավեր_գաղտնաբառ);assert վիճակ_արժեք==1;Միացնել.close();time.sleep(.6)
            զեկույց_արժեք['checks'].append('VNC incorrect password rejected')
            Միացնել,վիճակ_արժեք=화면인증(Նախընտրանքներ['vnc_password']);assert վիճակ_արժեք==0
            with Միացնել:
                Միացնել.sendall(b'\x01');초기=정확히(Միացնել,24);너비,높이=struct.unpack('!HH',초기[:4]);Անուն=정확히(Միացնել,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Անուն
                def 화면(증분=0):
                    Միացնել.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Միացնել,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    նկար_արժեք_c143fe9e=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_կոորդինատ,세로좌표,영역너비,영역높이,եղանակ_կերպ=struct.unpack('!HHHHi',정확히(Միացնել,12));assert եղանակ_կերպ==0 and x_կոորդինատ+영역너비<=너비 and 세로좌표+영역높이<=높이
                        փիքսել=정확히(Միացնել,영역너비*영역높이*4);합계+=len(փիքսել)
                        for կապ in range(영역높이):նկար_արժեք_c143fe9e[((세로좌표+կապ)*너비+x_կոորդինատ)*4:((세로좌표+կապ)*너비+x_կոորդինատ+영역너비)*4]=փիքսել[կապ*영역너비*4:(կապ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(նկար_արժեք_c143fe9e),'raw','BGRX').save(str(Ելք/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                զեկույց_արժեք['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                զեկույց_արժեք['checks'].append('RFB incremental update')
                처음=len(մատյան_տող)
                for գրանշան_արժեք in 'echo VNC_NATIVE_PASS\r':
                    նշան=0xff0d if գրանշան_արժեք=='\r' else ord(գրանշան_արժեք)
                    Միացնել.sendall(struct.pack('!BBHI',4,1,0,նշան));Միացնել.sendall(struct.pack('!BBHI',4,0,0,նշան))
                기다림(b'VNC_NATIVE_PASS',처음)
                զեկույց_արժեք['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(նշան,누름=1):Միացնել.sendall(struct.pack('!BBHI',4,누름,0,նշան))
                처음=len(մատյան_տող)
                for գրանշան_արժեք in 'echo ':글쇠(ord(գրանշան_արժեք))
                글쇠(0xffc6)
                for գրանշան_արժեք in 'gksrmf':글쇠(ord(գրանշան_արժեք))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                զեկույց_արժեք['checks'].append('Native VNC F9 two-set Hangul composition')
                Միացնել.sendall(struct.pack('!BBHH',5,0,120,100))
                զեկույց_արժեք['checks'].append('VNC pointer input accepted')
            Ընթացք_արժեք.stdin.write(b'poweroff\n');Ընթացք_արժեք.stdin.flush();Ընթացք_արժեք.wait(timeout=15);assert Ընթացք_արժեք.returncode==0
            զեկույց_արժեք['passed']=True
    finally:
        if Ընթացք_արժեք and Ընթացք_արժեք.poll() is None:
            Ընթացք_արժեք.terminate()
            try: Ընթացք_արժեք.wait(timeout=5)
            except subprocess.TimeoutExpired: Ընթացք_արժեք.kill();Ընթացք_արժեք.wait()
        (Ելք/'serial.log').write_bytes(մատյան_տող)
        (Ելք/'report.json').write_text(json.dumps(զեկույց_արժեք,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(զեկույց_արժեք,ensure_ascii=False,indent=2))


if __name__=='__main__': Գործարկել()
