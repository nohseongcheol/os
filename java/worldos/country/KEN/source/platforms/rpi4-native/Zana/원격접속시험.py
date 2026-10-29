#!/usr/bin/env python3
"""halisi_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from tekeleza_amri import 기준, amri
from Mtandao_daraja import Mtandao_daraja


def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    kichanganuzi_48ee4b1b.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    kichanganuzi_48ee4b1b.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Mipangilio = json.loads(인수.access.read_text())
    ripoti_thamani = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def tupu_kituo():
        with socket.socket() as UNGANISHA:
            UNGANISHA.bind(('127.0.0.5', 0))
            return UNGANISHA.getsockname()[1]
    sheli_kituo, 화면포트, faili_kituo = tupu_kituo(), tupu_kituo(), tupu_kituo()
    batli_REKODI = bytearray()
    Mchakato_thamani = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Mtandao_daraja(faili_kituo,
                ['tcp:{}:22'.format(sheli_kituo), 'tcp:{}:5900'.format(화면포트)], mwenyeji_anwani='127.0.0.5') as daraja_thamani:
            실행인수 = amri()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Mchakato_thamani = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + daraja_thamani.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Mchakato_thamani.stdout.read(4096)
                    if not data: break
                    batli_REKODI.extend(data)
            mtungo_thamani = threading.Thread(target=수집, daemon=True)
            mtungo_thamani.start()
            def subiri_hali(Neno_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Neno_SMS not in batli_REKODI[처음:]:
                    if time.monotonic()>끝 or Mchakato_thamani.poll() is not None:
                        raise AssertionError('Missing '+repr(Neno_SMS)+'\n'+batli_REKODI[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            subiri_hali(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def salama_sheli(nywila_thamani, agizo_thamani, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=nywila_thamani
                인수=['ssh','-v']+list(추가)+['-p',str(sheli_kituo),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',agizo_thamani]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=salama_sheli('!' + Mipangilio['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in batli_REKODI, 결과.stderr
            ripoti_thamani['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=salama_sheli(Mipangilio['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ripoti_thamani['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ripoti_thamani['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=salama_sheli(Mipangilio['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ripoti_thamani['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=salama_sheli(Mipangilio['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ripoti_thamani['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=salama_sheli(Mipangilio['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ripoti_thamani['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(sheli_kituo),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ingiliani_kipindi=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();uteuzi_thamani=selectors.DefaultSelector();uteuzi_thamani.register(ingiliani_kipindi.stdout,selectors.EVENT_READ)
            def 대화읽기(onyesha_thamani):
                마감=time.monotonic()+30
                while onyesha_thamani not in 대화기록:
                    if time.monotonic()>마감 or ingiliani_kipindi.poll() is not None:raise AssertionError('SSH interactive missing '+repr(onyesha_thamani)+' '+repr(bytes(대화기록)))
                    for ingizo_thamani,_ in uteuzi_thamani.select(.1):
                        조각=ingizo_thamani.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ingiliani_kipindi.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ingiliani_kipindi.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ingiliani_kipindi.stdin.write(b'\x04');ingiliani_kipindi.stdin.flush();나머지,kosa=ingiliani_kipindi.communicate(timeout=15)
                assert ingiliani_kipindi.returncode==0 and b'PTY allocation request failed' not in kosa,(ingiliani_kipindi.returncode,kosa)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                uteuzi_thamani.close()
                if ingiliani_kipindi.poll() is None:ingiliani_kipindi.kill();ingiliani_kipindi.wait()
            ripoti_thamani['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(UNGANISHA, 수):
                data=bytearray()
                while len(data)<수:
                    덩이=UNGANISHA.recv(수-len(data))
                    if not 덩이: raise AssertionError('RFB EOF')
                    data.extend(덩이)
                return bytes(data)
            def 화면인증(nywila_thamani):
                UNGANISHA=socket.create_connection(('127.0.0.5',화면포트),10);UNGANISHA.settimeout(30)
                assert 정확히(UNGANISHA,12)==b'RFB 003.008\n'
                UNGANISHA.sendall(b'RFB 003.008\n');assert 정확히(UNGANISHA,2)==b'\x01\x02'
                UNGANISHA.sendall(b'\x02');changamoto_thamani=정확히(UNGANISHA,16)
                입력암호=nywila_thamani.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                UNGANISHA.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(changamoto_thamani))
                hali_thamani=struct.unpack('!I',정확히(UNGANISHA,4))[0]
                return UNGANISHA,hali_thamani
            batili_nywila='!' if not Mipangilio['vnc_password'].startswith('!') else '?'
            UNGANISHA,hali_thamani=화면인증(batili_nywila);assert hali_thamani==1;UNGANISHA.close();time.sleep(.6)
            ripoti_thamani['checks'].append('VNC incorrect password rejected')
            UNGANISHA,hali_thamani=화면인증(Mipangilio['vnc_password']);assert hali_thamani==0
            with UNGANISHA:
                UNGANISHA.sendall(b'\x01');초기=정확히(UNGANISHA,24);너비,높이=struct.unpack('!HH',초기[:4]);Jina=정확히(UNGANISHA,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Jina
                def 화면(증분=0):
                    UNGANISHA.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(UNGANISHA,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    mchoro_thamani=bytearray(너비*높이*4)
                    for _ in range(수):
                        jira_x,Kitufe_cha_Y_kiratibu,영역너비,영역높이,mbinu_hali_tumizi=struct.unpack('!HHHHi',정확히(UNGANISHA,12));assert mbinu_hali_tumizi==0 and jira_x+영역너비<=너비 and Kitufe_cha_Y_kiratibu+영역높이<=높이
                        elepi=정확히(UNGANISHA,영역너비*영역높이*4);합계+=len(elepi)
                        for laini in range(영역높이):mchoro_thamani[((Kitufe_cha_Y_kiratibu+laini)*너비+jira_x)*4:((Kitufe_cha_Y_kiratibu+laini)*너비+jira_x+영역너비)*4]=elepi[laini*영역너비*4:(laini+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(mchoro_thamani),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ripoti_thamani['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ripoti_thamani['checks'].append('RFB incremental update')
                처음=len(batli_REKODI)
                for kibambo_thamani in 'echo VNC_NATIVE_PASS\r':
                    ishara=0xff0d if kibambo_thamani=='\r' else ord(kibambo_thamani)
                    UNGANISHA.sendall(struct.pack('!BBHI',4,1,0,ishara));UNGANISHA.sendall(struct.pack('!BBHI',4,0,0,ishara))
                subiri_hali(b'VNC_NATIVE_PASS',처음)
                ripoti_thamani['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ishara,누름=1):UNGANISHA.sendall(struct.pack('!BBHI',4,누름,0,ishara))
                처음=len(batli_REKODI)
                for kibambo_thamani in 'echo ':글쇠(ord(kibambo_thamani))
                글쇠(0xffc6)
                for kibambo_thamani in 'gksrmf':글쇠(ord(kibambo_thamani))
                글쇠(0xffc6);글쇠(0xff0d)
                subiri_hali('\r\n한글\r\n'.encode(),처음)
                ripoti_thamani['checks'].append('Native VNC F9 two-set Hangul composition')
                UNGANISHA.sendall(struct.pack('!BBHH',5,0,120,100))
                ripoti_thamani['checks'].append('VNC pointer input accepted')
            Mchakato_thamani.stdin.write(b'poweroff\n');Mchakato_thamani.stdin.flush();Mchakato_thamani.wait(timeout=15);assert Mchakato_thamani.returncode==0
            ripoti_thamani['passed']=True
    finally:
        if Mchakato_thamani and Mchakato_thamani.poll() is None:
            Mchakato_thamani.terminate()
            try: Mchakato_thamani.wait(timeout=5)
            except subprocess.TimeoutExpired: Mchakato_thamani.kill();Mchakato_thamani.wait()
        (출력/'serial.log').write_bytes(batli_REKODI)
        (출력/'report.json').write_text(json.dumps(ripoti_thamani,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ripoti_thamani,ensure_ascii=False,indent=2))


if __name__=='__main__': endesha()
