#!/usr/bin/env python3
"""iarbhír_sonraí OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Rith_ordú import teilgean_fréamh, Ordú
from Líonra_traschóiritheoir import Líonra_traschóiritheoir


def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=teilgean_fréamh / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=teilgean_fréamh / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=teilgean_fréamh / 'build/verification/native-remote')
    Argóintí = 해석기.parse_args()
    Aschur = Argóintí.output
    Aschur.mkdir(parents=True, exist_ok=True)
    Socruithe = json.loads(Argóintí.access.read_text())
    tuairisc_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Argóintí.kernel.read_bytes()).hexdigest(), 'checks': []}
    def folamh_port():
        with socket.socket() as Nasc:
            Nasc.bind(('127.0.0.5', 0))
            return Nasc.getsockname()[1]
    blaosc_port, 화면포트, comhad_port = folamh_port(), folamh_port(), folamh_port()
    LOG_ró = bytearray()
    Próiseas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Líonra_traschóiritheoir(comhad_port,
                ['tcp:{}:22'.format(blaosc_port), 'tcp:{}:5900'.format(화면포트)], óstach_ADDRESS='127.0.0.5') as traschóiritheoir_VALUE:
            실행인수 = Ordú()
            실행인수[실행인수.index('-kernel') + 1] = str(Argóintí.kernel.resolve())
            Próiseas_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + traschóiritheoir_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    sonraí = Próiseas_VALUE.stdout.read(4096)
                    if not sonraí: break
                    LOG_ró.extend(sonraí)
            snáithe_VALUE = threading.Thread(target=수집, daemon=True)
            snáithe_VALUE.start()
            def 기다림(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_ró[처음:]:
                    if time.monotonic()>끝 or Próiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_ró[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def slán_blaosc(pasfhocal_VALUE, treoir_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=pasfhocal_VALUE
                Argóintí=['ssh','-v']+list(추가)+['-p',str(blaosc_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',treoir_VALUE]
                tomhas=subprocess.run(Argóintí,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return tomhas
            tomhas=slán_blaosc('!' + Socruithe['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Aschur/'ssh-rejected.log').write_bytes(tomhas.stderr)
            assert tomhas.returncode!=0 and b'Permission denied' in tomhas.stderr and b'SHOULD_NOT_RUN' not in LOG_ró, tomhas.stderr
            tuairisc_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            tomhas=slán_blaosc(Socruithe['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Aschur/'ssh.log').write_bytes(tomhas.stderr)
            (Aschur/'ssh-output.txt').write_bytes(tomhas.stdout)
            assert tomhas.returncode==0 and b'SSH_NATIVE_PASS' in tomhas.stdout, (tomhas.returncode,tomhas.stdout,tomhas.stderr)
            tuairisc_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in tomhas.stderr, tomhas.stderr
            tuairisc_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            tomhas=slán_blaosc(Socruithe['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert tomhas.returncode==0 and 'JAVA Aschur: 안녕하세요 😀'.encode() in tomhas.stdout,tomhas.stdout
            tuairisc_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            tomhas=slán_blaosc(Socruithe['ssh_password'], 'missing_remote_command')
            assert tomhas.returncode==127,tomhas.returncode
            tuairisc_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            tomhas=slán_blaosc(Socruithe['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Aschur/'ssh-rekey.log').write_bytes(tomhas.stderr)
            assert tomhas.returncode==0 and 'class 창예제'.encode() in tomhas.stdout, (tomhas.returncode,tomhas.stdout,tomhas.stderr)
            assert tomhas.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, tomhas.stderr
            tuairisc_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(blaosc_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            idirghníomhach_seisiún=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();roghnú_VALUE=selectors.DefaultSelector();roghnú_VALUE.register(idirghníomhach_seisiún.stdout,selectors.EVENT_READ)
            def 대화읽기(seó_VALUE):
                마감=time.monotonic()+30
                while seó_VALUE not in 대화기록:
                    if time.monotonic()>마감 or idirghníomhach_seisiún.poll() is not None:raise AssertionError('SSH interactive missing '+repr(seó_VALUE)+' '+repr(bytes(대화기록)))
                    for iontráil_VALUE,_ in roghnú_VALUE.select(.1):
                        조각=iontráil_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                idirghníomhach_seisiún.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');idirghníomhach_seisiún.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                idirghníomhach_seisiún.stdin.write(b'\x04');idirghníomhach_seisiún.stdin.flush();나머지,ERREÁID=idirghníomhach_seisiún.communicate(timeout=15)
                assert idirghníomhach_seisiún.returncode==0 and b'PTY allocation request failed' not in ERREÁID,(idirghníomhach_seisiún.returncode,ERREÁID)
                (Aschur/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                roghnú_VALUE.close()
                if idirghníomhach_seisiún.poll() is None:idirghníomhach_seisiún.kill();idirghníomhach_seisiún.wait()
            tuairisc_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Nasc, 수):
                sonraí=bytearray()
                while len(sonraí)<수:
                    덩이=Nasc.recv(수-len(sonraí))
                    if not 덩이: raise AssertionError('RFB EOF')
                    sonraí.extend(덩이)
                return bytes(sonraí)
            def 화면인증(pasfhocal_VALUE):
                Nasc=socket.create_connection(('127.0.0.5',화면포트),10);Nasc.settimeout(30)
                assert 정확히(Nasc,12)==b'RFB 003.008\n'
                Nasc.sendall(b'RFB 003.008\n');assert 정확히(Nasc,2)==b'\x01\x02'
                Nasc.sendall(b'\x02');dúshlán_VALUE=정확히(Nasc,16)
                입력암호=pasfhocal_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Nasc.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(dúshlán_VALUE))
                staid_VALUE=struct.unpack('!I',정확히(Nasc,4))[0]
                return Nasc,staid_VALUE
            neamhbhailí_pasfhocal='!' if not Socruithe['vnc_password'].startswith('!') else '?'
            Nasc,staid_VALUE=화면인증(neamhbhailí_pasfhocal);assert staid_VALUE==1;Nasc.close();time.sleep(.6)
            tuairisc_VALUE['checks'].append('VNC incorrect password rejected')
            Nasc,staid_VALUE=화면인증(Socruithe['vnc_password']);assert staid_VALUE==0
            with Nasc:
                Nasc.sendall(b'\x01');초기=정확히(Nasc,24);너비,높이=struct.unpack('!HH',초기[:4]);Ainm=정확히(Nasc,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ainm
                def 화면(증분=0):
                    Nasc.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Nasc,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    líníocht_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_chomhordanáid,세로좌표,영역너비,영역높이,modh_mód=struct.unpack('!HHHHi',정확히(Nasc,12));assert modh_mód==0 and x_chomhordanáid+영역너비<=너비 and 세로좌표+영역높이<=높이
                        picteilín=정확히(Nasc,영역너비*영역높이*4);합계+=len(picteilín)
                        for Líne in range(영역높이):líníocht_VALUE[((세로좌표+Líne)*너비+x_chomhordanáid)*4:((세로좌표+Líne)*너비+x_chomhordanáid+영역너비)*4]=picteilín[Líne*영역너비*4:(Líne+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(líníocht_VALUE),'raw','BGRX').save(str(Aschur/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                tuairisc_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                tuairisc_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_ró)
                for carachtar_VALUE in 'echo VNC_NATIVE_PASS\r':
                    siombail=0xff0d if carachtar_VALUE=='\r' else ord(carachtar_VALUE)
                    Nasc.sendall(struct.pack('!BBHI',4,1,0,siombail));Nasc.sendall(struct.pack('!BBHI',4,0,0,siombail))
                기다림(b'VNC_NATIVE_PASS',처음)
                tuairisc_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(siombail,누름=1):Nasc.sendall(struct.pack('!BBHI',4,누름,0,siombail))
                처음=len(LOG_ró)
                for carachtar_VALUE in 'echo ':글쇠(ord(carachtar_VALUE))
                글쇠(0xffc6)
                for carachtar_VALUE in 'gksrmf':글쇠(ord(carachtar_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                tuairisc_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Nasc.sendall(struct.pack('!BBHH',5,0,120,100))
                tuairisc_VALUE['checks'].append('VNC pointer input accepted')
            Próiseas_VALUE.stdin.write(b'poweroff\n');Próiseas_VALUE.stdin.flush();Próiseas_VALUE.wait(timeout=15);assert Próiseas_VALUE.returncode==0
            tuairisc_VALUE['passed']=True
    finally:
        if Próiseas_VALUE and Próiseas_VALUE.poll() is None:
            Próiseas_VALUE.terminate()
            try: Próiseas_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Próiseas_VALUE.kill();Próiseas_VALUE.wait()
        (Aschur/'serial.log').write_bytes(LOG_ró)
        (Aschur/'report.json').write_text(json.dumps(tuairisc_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(tuairisc_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Rith_2()
