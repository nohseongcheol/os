#!/usr/bin/env python3
"""kgonthe_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from phethagatša_taelo import 기준, Taelo
from Netweke_kgokaganyo import Netweke_kgokaganyo


def Diriša():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Dipeakanyo = json.loads(인수.access.read_text())
    pego_boleng = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def hloka_selo_phote():
        with socket.socket() as Ikgokaganye:
            Ikgokaganye.bind(('127.0.0.5', 0))
            return Ikgokaganye.getsockname()[1]
    šele_phote, 화면포트, faele_phote = hloka_selo_phote(), hloka_selo_phote(), hloka_selo_phote()
    pego_rei = bytearray()
    tiragalo_boleng = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Netweke_kgokaganyo(faele_phote,
                ['tcp:{}:22'.format(šele_phote), 'tcp:{}:5900'.format(화면포트)], go_nea_ditirelo_atrese='127.0.0.5') as kgokaganyo_boleng_982037b1:
            실행인수 = Taelo()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            tiragalo_boleng = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + kgokaganyo_boleng_982037b1.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = tiragalo_boleng.stdout.read(4096)
                    if not data: break
                    pego_rei.extend(data)
            threte_boleng = threading.Thread(target=수집, daemon=True)
            threte_boleng.start()
            def 기다림(Thalokontšu_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Thalokontšu_SMS not in pego_rei[처음:]:
                    if time.monotonic()>끝 or tiragalo_boleng.poll() is not None:
                        raise AssertionError('Missing '+repr(Thalokontšu_SMS)+'\n'+pego_rei[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def šireletšegile_šele(phasewete_boleng, taelo_boleng, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=phasewete_boleng
                인수=['ssh','-v']+list(추가)+['-p',str(šele_phote),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',taelo_boleng]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=šireletšegile_šele('!' + Dipeakanyo['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in pego_rei, 결과.stderr
            pego_boleng['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=šireletšegile_šele(Dipeakanyo['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            pego_boleng['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            pego_boleng['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=šireletšegile_šele(Dipeakanyo['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            pego_boleng['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=šireletšegile_šele(Dipeakanyo['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            pego_boleng['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=šireletšegile_šele(Dipeakanyo['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            pego_boleng['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(šele_phote),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ya_kgokagano_nakotiragalo=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();kgetho_boleng=selectors.DefaultSelector();kgetho_boleng.register(ya_kgokagano_nakotiragalo.stdout,selectors.EVENT_READ)
            def 대화읽기(bontšha_boleng):
                마감=time.monotonic()+30
                while bontšha_boleng not in 대화기록:
                    if time.monotonic()>마감 or ya_kgokagano_nakotiragalo.poll() is not None:raise AssertionError('SSH interactive missing '+repr(bontšha_boleng)+' '+repr(bytes(대화기록)))
                    for go_tsenya_tshedimošo_boleng,_ in kgetho_boleng.select(.1):
                        조각=go_tsenya_tshedimošo_boleng.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ya_kgokagano_nakotiragalo.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ya_kgokagano_nakotiragalo.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ya_kgokagano_nakotiragalo.stdin.write(b'\x04');ya_kgokagano_nakotiragalo.stdin.flush();나머지,Phošo=ya_kgokagano_nakotiragalo.communicate(timeout=15)
                assert ya_kgokagano_nakotiragalo.returncode==0 and b'PTY allocation request failed' not in Phošo,(ya_kgokagano_nakotiragalo.returncode,Phošo)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                kgetho_boleng.close()
                if ya_kgokagano_nakotiragalo.poll() is None:ya_kgokagano_nakotiragalo.kill();ya_kgokagano_nakotiragalo.wait()
            pego_boleng['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Ikgokaganye, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=Ikgokaganye.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(phasewete_boleng):
                Ikgokaganye=socket.create_connection(('127.0.0.5',화면포트),10);Ikgokaganye.settimeout(30)
                assert 정확히(Ikgokaganye,12)==b'RFB 003.008\n'
                Ikgokaganye.sendall(b'RFB 003.008\n');assert 정확히(Ikgokaganye,2)==b'\x01\x02'
                Ikgokaganye.sendall(b'\x02');tlhohlo_boleng=정확히(Ikgokaganye,16)
                입력암호=phasewete_boleng.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Ikgokaganye.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(tlhohlo_boleng))
                boemo_boleng=struct.unpack('!I',정확히(Ikgokaganye,4))[0]
                return Ikgokaganye,boemo_boleng
            ye_e_phošagetšego_phasewete='!' if not Dipeakanyo['vnc_password'].startswith('!') else '?'
            Ikgokaganye,boemo_boleng=화면인증(ye_e_phošagetšego_phasewete);assert boemo_boleng==1;Ikgokaganye.close();time.sleep(.6)
            pego_boleng['checks'].append('VNC incorrect password rejected')
            Ikgokaganye,boemo_boleng=화면인증(Dipeakanyo['vnc_password']);assert boemo_boleng==0
            with Ikgokaganye:
                Ikgokaganye.sendall(b'\x01');초기=정확히(Ikgokaganye,24);너비,높이=struct.unpack('!HH',초기[:4]);Leina=정확히(Ikgokaganye,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Leina
                def 화면(증분=0):
                    Ikgokaganye.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Ikgokaganye,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    sethalwa_boleng=bytearray(너비*높이*4)
                    for _ in range(수):
                        kamano_ya_x,세로좌표,영역너비,영역높이,mokgwa_mokgwa=struct.unpack('!HHHHi',정확히(Ikgokaganye,12));assert mokgwa_mokgwa==0 and kamano_ya_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        phele=정확히(Ikgokaganye,영역너비*영역높이*4);합계+=len(phele)
                        for mothaladi in range(영역높이):sethalwa_boleng[((세로좌표+mothaladi)*너비+kamano_ya_x)*4:((세로좌표+mothaladi)*너비+kamano_ya_x+영역너비)*4]=phele[mothaladi*영역너비*4:(mothaladi+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(sethalwa_boleng),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                pego_boleng['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                pego_boleng['checks'].append('RFB incremental update')
                처음=len(pego_rei)
                for tlhaka_boleng in 'echo VNC_NATIVE_PASS\r':
                    leswao=0xff0d if tlhaka_boleng=='\r' else ord(tlhaka_boleng)
                    Ikgokaganye.sendall(struct.pack('!BBHI',4,1,0,leswao));Ikgokaganye.sendall(struct.pack('!BBHI',4,0,0,leswao))
                기다림(b'VNC_NATIVE_PASS',처음)
                pego_boleng['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(leswao,누름=1):Ikgokaganye.sendall(struct.pack('!BBHI',4,누름,0,leswao))
                처음=len(pego_rei)
                for tlhaka_boleng in 'echo ':글쇠(ord(tlhaka_boleng))
                글쇠(0xffc6)
                for tlhaka_boleng in 'gksrmf':글쇠(ord(tlhaka_boleng))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                pego_boleng['checks'].append('Native VNC F9 two-set Hangul composition')
                Ikgokaganye.sendall(struct.pack('!BBHH',5,0,120,100))
                pego_boleng['checks'].append('VNC pointer input accepted')
            tiragalo_boleng.stdin.write(b'poweroff\n');tiragalo_boleng.stdin.flush();tiragalo_boleng.wait(timeout=15);assert tiragalo_boleng.returncode==0
            pego_boleng['passed']=True
    finally:
        if tiragalo_boleng and tiragalo_boleng.poll() is None:
            tiragalo_boleng.terminate()
            try: tiragalo_boleng.wait(timeout=5)
            except subprocess.TimeoutExpired: tiragalo_boleng.kill();tiragalo_boleng.wait()
        (출력/'serial.log').write_bytes(pego_rei)
        (출력/'report.json').write_text(json.dumps(pego_boleng,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pego_boleng,ensure_ascii=False,indent=2))


if __name__=='__main__': Diriša()
