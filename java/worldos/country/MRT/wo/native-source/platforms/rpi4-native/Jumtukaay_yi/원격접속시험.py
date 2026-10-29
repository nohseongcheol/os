#!/usr/bin/env python3
"""liteew_mbir OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from def_ndigel import 기준, ndigel
from mbaal_poŋ import mbaal_poŋ


def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Jekkal_yi = json.loads(인수.access.read_text())
    tënk_xëyma = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def neen_jël():
        with socket.socket() as JOKKOO:
            JOKKOO.bind(('127.0.0.5', 0))
            return JOKKOO.getsockname()[1]
    Wëreef_jël, 화면포트, bara_denc_jël = neen_jël(), neen_jël(), neen_jël()
    làq_Dënk = bytearray()
    yokkute_xëyma = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, mbaal_poŋ(bara_denc_jël,
                ['tcp:{}:22'.format(Wëreef_jël), 'tcp:{}:5900'.format(화면포트)], dalal_dëkkuwaay='127.0.0.5') as poŋ_xëyma:
            실행인수 = ndigel()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            yokkute_xëyma = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + poŋ_xëyma.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    mbir = yokkute_xëyma.stdout.read(4096)
                    if not mbir: break
                    làq_Dënk.extend(mbir)
            buumug_jokkale_xëyma = threading.Thread(target=수집, daemon=True)
            buumug_jokkale_xëyma.start()
            def 기다림(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in làq_Dënk[처음:]:
                    if time.monotonic()>끝 or yokkute_xëyma.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+làq_Dënk[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def wóor_Wëreef(pasu_dugg_xëyma, ndigal_xëyma, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=pasu_dugg_xëyma
                인수=['ssh','-v']+list(추가)+['-p',str(Wëreef_jël),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ndigal_xëyma]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=wóor_Wëreef('!' + Jekkal_yi['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in làq_Dënk, 결과.stderr
            tënk_xëyma['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=wóor_Wëreef(Jekkal_yi['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            tënk_xëyma['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            tënk_xëyma['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=wóor_Wëreef(Jekkal_yi['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            tënk_xëyma['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=wóor_Wëreef(Jekkal_yi['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            tënk_xëyma['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=wóor_Wëreef(Jekkal_yi['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            tënk_xëyma['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Wëreef_jël),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            duglante_lël=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();tanneef_xëyma=selectors.DefaultSelector();tanneef_xëyma.register(duglante_lël.stdout,selectors.EVENT_READ)
            def 대화읽기(féeñal_xëyma):
                마감=time.monotonic()+30
                while féeñal_xëyma not in 대화기록:
                    if time.monotonic()>마감 or duglante_lël.poll() is not None:raise AssertionError('SSH interactive missing '+repr(féeñal_xëyma)+' '+repr(bytes(대화기록)))
                    for dugal_xabaar_xëyma,_ in tanneef_xëyma.select(.1):
                        조각=dugal_xabaar_xëyma.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                duglante_lël.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');duglante_lël.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                duglante_lël.stdin.write(b'\x04');duglante_lël.stdin.flush();나머지,njumte=duglante_lël.communicate(timeout=15)
                assert duglante_lël.returncode==0 and b'PTY allocation request failed' not in njumte,(duglante_lël.returncode,njumte)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                tanneef_xëyma.close()
                if duglante_lël.poll() is None:duglante_lël.kill();duglante_lël.wait()
            tënk_xëyma['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(JOKKOO, 수):
                mbir=bytearray()
                while len(mbir)<수:
                    덩이=JOKKOO.recv(수-len(mbir))
                    if not 덩이: raise AssertionError('RFB EOF')
                    mbir.extend(덩이)
                return bytes(mbir)
            def 화면인증(pasu_dugg_xëyma):
                JOKKOO=socket.create_connection(('127.0.0.5',화면포트),10);JOKKOO.settimeout(30)
                assert 정확히(JOKKOO,12)==b'RFB 003.008\n'
                JOKKOO.sendall(b'RFB 003.008\n');assert 정확히(JOKKOO,2)==b'\x01\x02'
                JOKKOO.sendall(b'\x02');natt_xëyma=정확히(JOKKOO,16)
                입력암호=pasu_dugg_xëyma.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                JOKKOO.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(natt_xëyma))
                nekkin_xëyma=struct.unpack('!I',정확히(JOKKOO,4))[0]
                return JOKKOO,nekkin_xëyma
            baaxul_pasu_dugg='!' if not Jekkal_yi['vnc_password'].startswith('!') else '?'
            JOKKOO,nekkin_xëyma=화면인증(baaxul_pasu_dugg);assert nekkin_xëyma==1;JOKKOO.close();time.sleep(.6)
            tënk_xëyma['checks'].append('VNC incorrect password rejected')
            JOKKOO,nekkin_xëyma=화면인증(Jekkal_yi['vnc_password']);assert nekkin_xëyma==0
            with JOKKOO:
                JOKKOO.sendall(b'\x01');초기=정확히(JOKKOO,24);너비,높이=struct.unpack('!HH',초기[:4]);tur_253d1510=정확히(JOKKOO,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==tur_253d1510
                def 화면(증분=0):
                    JOKKOO.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(JOKKOO,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    deseñ_xëyma=bytearray(너비*높이*4)
                    for _ in range(수):
                        rëddu_iks_yi,세로좌표,영역너비,영역높이,doxalin_anam=struct.unpack('!HHHHi',정확히(JOKKOO,12));assert doxalin_anam==0 and rëddu_iks_yi+영역너비<=너비 and 세로좌표+영역높이<=높이
                        piksel=정확히(JOKKOO,영역너비*영역높이*4);합계+=len(piksel)
                        for buum in range(영역높이):deseñ_xëyma[((세로좌표+buum)*너비+rëddu_iks_yi)*4:((세로좌표+buum)*너비+rëddu_iks_yi+영역너비)*4]=piksel[buum*영역너비*4:(buum+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(deseñ_xëyma),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                tënk_xëyma['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                tënk_xëyma['checks'].append('RFB incremental update')
                처음=len(làq_Dënk)
                for Araf_xëyma in 'echo VNC_NATIVE_PASS\r':
                    sembóol=0xff0d if Araf_xëyma=='\r' else ord(Araf_xëyma)
                    JOKKOO.sendall(struct.pack('!BBHI',4,1,0,sembóol));JOKKOO.sendall(struct.pack('!BBHI',4,0,0,sembóol))
                기다림(b'VNC_NATIVE_PASS',처음)
                tënk_xëyma['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(sembóol,누름=1):JOKKOO.sendall(struct.pack('!BBHI',4,누름,0,sembóol))
                처음=len(làq_Dënk)
                for Araf_xëyma in 'echo ':글쇠(ord(Araf_xëyma))
                글쇠(0xffc6)
                for Araf_xëyma in 'gksrmf':글쇠(ord(Araf_xëyma))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                tënk_xëyma['checks'].append('Native VNC F9 two-set Hangul composition')
                JOKKOO.sendall(struct.pack('!BBHH',5,0,120,100))
                tënk_xëyma['checks'].append('VNC pointer input accepted')
            yokkute_xëyma.stdin.write(b'poweroff\n');yokkute_xëyma.stdin.flush();yokkute_xëyma.wait(timeout=15);assert yokkute_xëyma.returncode==0
            tënk_xëyma['passed']=True
    finally:
        if yokkute_xëyma and yokkute_xëyma.poll() is None:
            yokkute_xëyma.terminate()
            try: yokkute_xëyma.wait(timeout=5)
            except subprocess.TimeoutExpired: yokkute_xëyma.kill();yokkute_xëyma.wait()
        (출력/'serial.log').write_bytes(làq_Dënk)
        (출력/'report.json').write_text(json.dumps(tënk_xëyma,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(tënk_xëyma,ensure_ascii=False,indent=2))


if __name__=='__main__': daw()
