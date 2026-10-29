#!/usr/bin/env python3
"""tota_tshedimosetso OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from diragatsa_Taelo import 기준, Taelo
from Neteweke_leborogo import Neteweke_leborogo


def dirisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Diseting = json.loads(인수.access.read_text())
    pego_Boleng = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def lolea_gorogisetsa():
        with socket.socket() as Golaganya:
            Golaganya.bind(('127.0.0.5', 0))
            return Golaganya.getsockname()[1]
    setlhalosataelo_gorogisetsa, 화면포트, faele_gorogisetsa = lolea_gorogisetsa(), lolea_gorogisetsa(), lolea_gorogisetsa()
    rekota_mola = bytearray()
    Thulaganyo_Boleng = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Neteweke_leborogo(faele_gorogisetsa,
                ['tcp:{}:22'.format(setlhalosataelo_gorogisetsa), 'tcp:{}:5900'.format(화면포트)], pinagare_aterese='127.0.0.5') as leborogo_Boleng:
            실행인수 = Taelo()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Thulaganyo_Boleng = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + leborogo_Boleng.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    tshedimosetso = Thulaganyo_Boleng.stdout.read(4096)
                    if not tshedimosetso: break
                    rekota_mola.extend(tshedimosetso)
            tlhale_Boleng = threading.Thread(target=수집, daemon=True)
            tlhale_Boleng.start()
            def 기다림(Lefoko_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Lefoko_SMS not in rekota_mola[처음:]:
                    if time.monotonic()>끝 or Thulaganyo_Boleng.poll() is not None:
                        raise AssertionError('Missing '+repr(Lefoko_SMS)+'\n'+rekota_mola[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def sireletsegile_setlhalosataelo(khoututseno_Boleng, taelo_Boleng, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=khoututseno_Boleng
                인수=['ssh','-v']+list(추가)+['-p',str(setlhalosataelo_gorogisetsa),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',taelo_Boleng]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=sireletsegile_setlhalosataelo('!' + Diseting['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in rekota_mola, 결과.stderr
            pego_Boleng['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=sireletsegile_setlhalosataelo(Diseting['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            pego_Boleng['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            pego_Boleng['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=sireletsegile_setlhalosataelo(Diseting['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            pego_Boleng['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=sireletsegile_setlhalosataelo(Diseting['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            pego_Boleng['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=sireletsegile_setlhalosataelo(Diseting['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            pego_Boleng['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(setlhalosataelo_gorogisetsa),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            Tirisano_nakotiriso=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();tlhopho_Boleng=selectors.DefaultSelector();tlhopho_Boleng.register(Tirisano_nakotiriso.stdout,selectors.EVENT_READ)
            def 대화읽기(bontsha_Boleng):
                마감=time.monotonic()+30
                while bontsha_Boleng not in 대화기록:
                    if time.monotonic()>마감 or Tirisano_nakotiriso.poll() is not None:raise AssertionError('SSH interactive missing '+repr(bontsha_Boleng)+' '+repr(bytes(대화기록)))
                    for tsenyo_Boleng,_ in tlhopho_Boleng.select(.1):
                        조각=tsenyo_Boleng.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                Tirisano_nakotiriso.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');Tirisano_nakotiriso.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                Tirisano_nakotiriso.stdin.write(b'\x04');Tirisano_nakotiriso.stdin.flush();나머지,phoso=Tirisano_nakotiriso.communicate(timeout=15)
                assert Tirisano_nakotiriso.returncode==0 and b'PTY allocation request failed' not in phoso,(Tirisano_nakotiriso.returncode,phoso)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                tlhopho_Boleng.close()
                if Tirisano_nakotiriso.poll() is None:Tirisano_nakotiriso.kill();Tirisano_nakotiriso.wait()
            pego_Boleng['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Golaganya, 수):
                tshedimosetso=bytearray()
                while len(tshedimosetso)<수:
                    덩이=Golaganya.recv(수-len(tshedimosetso))
                    if not 덩이: raise AssertionError('RFB EOF')
                    tshedimosetso.extend(덩이)
                return bytes(tshedimosetso)
            def 화면인증(khoututseno_Boleng):
                Golaganya=socket.create_connection(('127.0.0.5',화면포트),10);Golaganya.settimeout(30)
                assert 정확히(Golaganya,12)==b'RFB 003.008\n'
                Golaganya.sendall(b'RFB 003.008\n');assert 정확히(Golaganya,2)==b'\x01\x02'
                Golaganya.sendall(b'\x02');kgwetlho_Boleng=정확히(Golaganya,16)
                입력암호=khoututseno_Boleng.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Golaganya.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(kgwetlho_Boleng))
                kemo_Boleng=struct.unpack('!I',정확히(Golaganya,4))[0]
                return Golaganya,kemo_Boleng
            Ga_e_a_siama_khoututseno='!' if not Diseting['vnc_password'].startswith('!') else '?'
            Golaganya,kemo_Boleng=화면인증(Ga_e_a_siama_khoututseno);assert kemo_Boleng==1;Golaganya.close();time.sleep(.6)
            pego_Boleng['checks'].append('VNC incorrect password rejected')
            Golaganya,kemo_Boleng=화면인증(Diseting['vnc_password']);assert kemo_Boleng==0
            with Golaganya:
                Golaganya.sendall(b'\x01');초기=정확히(Golaganya,24);너비,높이=struct.unpack('!HH',초기[:4]);leina=정확히(Golaganya,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==leina
                def 화면(증분=0):
                    Golaganya.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Golaganya,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    sethalo_Boleng=bytearray(너비*높이*4)
                    for _ in range(수):
                        kgokagano_ya_x,세로좌표,영역너비,영역높이,mokgwa_mokgwa=struct.unpack('!HHHHi',정확히(Golaganya,12));assert mokgwa_mokgwa==0 and kgokagano_ya_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        phele=정확히(Golaganya,영역너비*영역높이*4);합계+=len(phele)
                        for Mola in range(영역높이):sethalo_Boleng[((세로좌표+Mola)*너비+kgokagano_ya_x)*4:((세로좌표+Mola)*너비+kgokagano_ya_x+영역너비)*4]=phele[Mola*영역너비*4:(Mola+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(sethalo_Boleng),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                pego_Boleng['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                pego_Boleng['checks'].append('RFB incremental update')
                처음=len(rekota_mola)
                for Letshwao_Boleng in 'echo VNC_NATIVE_PASS\r':
                    letshwao=0xff0d if Letshwao_Boleng=='\r' else ord(Letshwao_Boleng)
                    Golaganya.sendall(struct.pack('!BBHI',4,1,0,letshwao));Golaganya.sendall(struct.pack('!BBHI',4,0,0,letshwao))
                기다림(b'VNC_NATIVE_PASS',처음)
                pego_Boleng['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(letshwao,누름=1):Golaganya.sendall(struct.pack('!BBHI',4,누름,0,letshwao))
                처음=len(rekota_mola)
                for Letshwao_Boleng in 'echo ':글쇠(ord(Letshwao_Boleng))
                글쇠(0xffc6)
                for Letshwao_Boleng in 'gksrmf':글쇠(ord(Letshwao_Boleng))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                pego_Boleng['checks'].append('Native VNC F9 two-set Hangul composition')
                Golaganya.sendall(struct.pack('!BBHH',5,0,120,100))
                pego_Boleng['checks'].append('VNC pointer input accepted')
            Thulaganyo_Boleng.stdin.write(b'poweroff\n');Thulaganyo_Boleng.stdin.flush();Thulaganyo_Boleng.wait(timeout=15);assert Thulaganyo_Boleng.returncode==0
            pego_Boleng['passed']=True
    finally:
        if Thulaganyo_Boleng and Thulaganyo_Boleng.poll() is None:
            Thulaganyo_Boleng.terminate()
            try: Thulaganyo_Boleng.wait(timeout=5)
            except subprocess.TimeoutExpired: Thulaganyo_Boleng.kill();Thulaganyo_Boleng.wait()
        (출력/'serial.log').write_bytes(rekota_mola)
        (출력/'report.json').write_text(json.dumps(pego_Boleng,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pego_Boleng,ensure_ascii=False,indent=2))


if __name__=='__main__': dirisa()
