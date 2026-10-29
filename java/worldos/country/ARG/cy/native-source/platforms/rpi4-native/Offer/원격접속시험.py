#!/usr/bin/env python3
"""go_iawn_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Gweithredu_gorchymyn import prosiect_gwraidd, Gorchymyn
from Rhwydwaith_pont import Rhwydwaith_pont


def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=prosiect_gwraidd / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=prosiect_gwraidd / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=prosiect_gwraidd / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    Allbwn = 인수.output
    Allbwn.mkdir(parents=True, exist_ok=True)
    Gosodiadau = json.loads(인수.access.read_text())
    adrodd_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def gwag_porth():
        with socket.socket() as Cysylltu:
            Cysylltu.bind(('127.0.0.5', 0))
            return Cysylltu.getsockname()[1]
    cragen_porth, 화면포트, ffeil_porth = gwag_porth(), gwag_porth(), gwag_porth()
    LOG_rhes = bytearray()
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Rhwydwaith_pont(ffeil_porth,
                ['tcp:{}:22'.format(cragen_porth), 'tcp:{}:5900'.format(화면포트)], lletya_ADDRESS='127.0.0.5') as pont_VALUE:
            실행인수 = Gorchymyn()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proses_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + pont_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proses_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_rhes.extend(data)
            edefyn_VALUE = threading.Thread(target=수집, daemon=True)
            edefyn_VALUE.start()
            def aros_cyflwr(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_rhes[처음:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_rhes[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            aros_cyflwr(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def diogel_cragen(cyfrinair_VALUE, cyfarwyddyd_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=cyfrinair_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(cragen_porth),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',cyfarwyddyd_VALUE]
                mesur=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return mesur
            mesur=diogel_cragen('!' + Gosodiadau['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Allbwn/'ssh-rejected.log').write_bytes(mesur.stderr)
            assert mesur.returncode!=0 and b'Permission denied' in mesur.stderr and b'SHOULD_NOT_RUN' not in LOG_rhes, mesur.stderr
            adrodd_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            mesur=diogel_cragen(Gosodiadau['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Allbwn/'ssh.log').write_bytes(mesur.stderr)
            (Allbwn/'ssh-output.txt').write_bytes(mesur.stdout)
            assert mesur.returncode==0 and b'SSH_NATIVE_PASS' in mesur.stdout, (mesur.returncode,mesur.stdout,mesur.stderr)
            adrodd_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in mesur.stderr, mesur.stderr
            adrodd_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            mesur=diogel_cragen(Gosodiadau['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert mesur.returncode==0 and 'JAVA Allbwn: 안녕하세요 😀'.encode() in mesur.stdout,mesur.stdout
            adrodd_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            mesur=diogel_cragen(Gosodiadau['ssh_password'], 'missing_remote_command')
            assert mesur.returncode==127,mesur.returncode
            adrodd_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            mesur=diogel_cragen(Gosodiadau['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (Allbwn/'ssh-rekey.log').write_bytes(mesur.stderr)
            assert mesur.returncode==0 and 'class 창예제'.encode() in mesur.stdout, (mesur.returncode,mesur.stdout,mesur.stderr)
            assert mesur.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, mesur.stderr
            adrodd_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(cragen_porth),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            rhyngweithiol_sesiwn=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();dewisiad_VALUE=selectors.DefaultSelector();dewisiad_VALUE.register(rhyngweithiol_sesiwn.stdout,selectors.EVENT_READ)
            def 대화읽기(sioe_VALUE):
                마감=time.monotonic()+30
                while sioe_VALUE not in 대화기록:
                    if time.monotonic()>마감 or rhyngweithiol_sesiwn.poll() is not None:raise AssertionError('SSH interactive missing '+repr(sioe_VALUE)+' '+repr(bytes(대화기록)))
                    for cofnod_VALUE,_ in dewisiad_VALUE.select(.1):
                        조각=cofnod_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                rhyngweithiol_sesiwn.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');rhyngweithiol_sesiwn.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                rhyngweithiol_sesiwn.stdin.write(b'\x04');rhyngweithiol_sesiwn.stdin.flush();나머지,Gwall=rhyngweithiol_sesiwn.communicate(timeout=15)
                assert rhyngweithiol_sesiwn.returncode==0 and b'PTY allocation request failed' not in Gwall,(rhyngweithiol_sesiwn.returncode,Gwall)
                (Allbwn/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                dewisiad_VALUE.close()
                if rhyngweithiol_sesiwn.poll() is None:rhyngweithiol_sesiwn.kill();rhyngweithiol_sesiwn.wait()
            adrodd_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Cysylltu, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=Cysylltu.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(cyfrinair_VALUE):
                Cysylltu=socket.create_connection(('127.0.0.5',화면포트),10);Cysylltu.settimeout(30)
                assert 정확히(Cysylltu,12)==b'RFB 003.008\n'
                Cysylltu.sendall(b'RFB 003.008\n');assert 정확히(Cysylltu,2)==b'\x01\x02'
                Cysylltu.sendall(b'\x02');her_VALUE=정확히(Cysylltu,16)
                입력암호=cyfrinair_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Cysylltu.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(her_VALUE))
                cyflwr_VALUE=struct.unpack('!I',정확히(Cysylltu,4))[0]
                return Cysylltu,cyflwr_VALUE
            annilys_cyfrinair='!' if not Gosodiadau['vnc_password'].startswith('!') else '?'
            Cysylltu,cyflwr_VALUE=화면인증(annilys_cyfrinair);assert cyflwr_VALUE==1;Cysylltu.close();time.sleep(.6)
            adrodd_VALUE['checks'].append('VNC incorrect password rejected')
            Cysylltu,cyflwr_VALUE=화면인증(Gosodiadau['vnc_password']);assert cyflwr_VALUE==0
            with Cysylltu:
                Cysylltu.sendall(b'\x01');초기=정확히(Cysylltu,24);너비,높이=struct.unpack('!HH',초기[:4]);Enw=정확히(Cysylltu,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Enw
                def 화면(증분=0):
                    Cysylltu.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Cysylltu,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    lluniad_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        cyfesuryn_x,Y_cyfesuryn,영역너비,영역높이,dull_MODE=struct.unpack('!HHHHi',정확히(Cysylltu,12));assert dull_MODE==0 and cyfesuryn_x+영역너비<=너비 and Y_cyfesuryn+영역높이<=높이
                        pel=정확히(Cysylltu,영역너비*영역높이*4);합계+=len(pel)
                        for llinell in range(영역높이):lluniad_VALUE[((Y_cyfesuryn+llinell)*너비+cyfesuryn_x)*4:((Y_cyfesuryn+llinell)*너비+cyfesuryn_x+영역너비)*4]=pel[llinell*영역너비*4:(llinell+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(lluniad_VALUE),'raw','BGRX').save(str(Allbwn/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                adrodd_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                adrodd_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_rhes)
                for nod_VALUE in 'echo VNC_NATIVE_PASS\r':
                    symbol=0xff0d if nod_VALUE=='\r' else ord(nod_VALUE)
                    Cysylltu.sendall(struct.pack('!BBHI',4,1,0,symbol));Cysylltu.sendall(struct.pack('!BBHI',4,0,0,symbol))
                aros_cyflwr(b'VNC_NATIVE_PASS',처음)
                adrodd_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(symbol,pwyso_VALUE=1):Cysylltu.sendall(struct.pack('!BBHI',4,pwyso_VALUE,0,symbol))
                처음=len(LOG_rhes)
                for nod_VALUE in 'echo ':글쇠(ord(nod_VALUE))
                글쇠(0xffc6)
                for nod_VALUE in 'gksrmf':글쇠(ord(nod_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                aros_cyflwr('\r\n한글\r\n'.encode(),처음)
                adrodd_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Cysylltu.sendall(struct.pack('!BBHH',5,0,120,100))
                adrodd_VALUE['checks'].append('VNC pointer input accepted')
            Proses_VALUE.stdin.write(b'poweroff\n');Proses_VALUE.stdin.flush();Proses_VALUE.wait(timeout=15);assert Proses_VALUE.returncode==0
            adrodd_VALUE['passed']=True
    finally:
        if Proses_VALUE and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses_VALUE.kill();Proses_VALUE.wait()
        (Allbwn/'serial.log').write_bytes(LOG_rhes)
        (Allbwn/'report.json').write_text(json.dumps(adrodd_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(adrodd_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Gweithredu_2()
