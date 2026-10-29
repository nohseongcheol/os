#!/usr/bin/env python3
"""faktiki_verilənlər OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from icra_etmək_əmr import Project_kök, Əmr
from Şəbəkə_körpü import Şəbəkə_körpü


def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_kök / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_kök / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_kök / 'build/verification/native-remote')
    인수 = parser_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Sazlama = json.loads(인수.access.read_text())
    hesabat_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def boş_port():
        with socket.socket() as Bağlan:
            Bağlan.bind(('127.0.0.5', 0))
            return Bağlan.getsockname()[1]
    örtük_port, 화면포트, fayl_port = boş_port(), boş_port(), boş_port()
    LOG_yaz = bytearray()
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Şəbəkə_körpü(fayl_port,
                ['tcp:{}:22'.format(örtük_port), 'tcp:{}:5900'.format(화면포트)], host_ünvan='127.0.0.5') as körpü_VALUE:
            실행인수 = Əmr()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proses_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + körpü_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    verilənlər = Proses_VALUE.stdout.read(4096)
                    if not verilənlər: break
                    LOG_yaz.extend(verilənlər)
            axın_VALUE_5b72a632 = threading.Thread(target=수집, daemon=True)
            axın_VALUE_5b72a632.start()
            def gözlə_vəziyyət(Söz_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Söz_SMS not in LOG_yaz[처음:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Söz_SMS)+'\n'+LOG_yaz[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            gözlə_vəziyyət(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def təhlükəsiz_örtük(parol_VALUE, təlimat_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=parol_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(örtük_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',təlimat_VALUE]
                ölçü=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ölçü
            ölçü=təhlükəsiz_örtük('!' + Sazlama['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(ölçü.stderr)
            assert ölçü.returncode!=0 and b'Permission denied' in ölçü.stderr and b'SHOULD_NOT_RUN' not in LOG_yaz, ölçü.stderr
            hesabat_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ölçü=təhlükəsiz_örtük(Sazlama['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(ölçü.stderr)
            (출력/'ssh-output.txt').write_bytes(ölçü.stdout)
            assert ölçü.returncode==0 and b'SSH_NATIVE_PASS' in ölçü.stdout, (ölçü.returncode,ölçü.stdout,ölçü.stderr)
            hesabat_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ölçü.stderr, ölçü.stderr
            hesabat_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ölçü=təhlükəsiz_örtük(Sazlama['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ölçü.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in ölçü.stdout,ölçü.stdout
            hesabat_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ölçü=təhlükəsiz_örtük(Sazlama['ssh_password'], 'missing_remote_command')
            assert ölçü.returncode==127,ölçü.returncode
            hesabat_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ölçü=təhlükəsiz_örtük(Sazlama['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(ölçü.stderr)
            assert ölçü.returncode==0 and 'class 창예제'.encode() in ölçü.stdout, (ölçü.returncode,ölçü.stdout,ölçü.stderr)
            assert ölçü.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ölçü.stderr
            hesabat_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(örtük_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktiv_seans=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();seçilmiş_sahə_VALUE=selectors.DefaultSelector();seçilmiş_sahə_VALUE.register(interaktiv_seans.stdout,selectors.EVENT_READ)
            def 대화읽기(göstərmək_VALUE):
                마감=time.monotonic()+30
                while göstərmək_VALUE not in 대화기록:
                    if time.monotonic()>마감 or interaktiv_seans.poll() is not None:raise AssertionError('SSH interactive missing '+repr(göstərmək_VALUE)+' '+repr(bytes(대화기록)))
                    for daxiletmə_VALUE,_ in seçilmiş_sahə_VALUE.select(.1):
                        조각=daxiletmə_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktiv_seans.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktiv_seans.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktiv_seans.stdin.write(b'\x04');interaktiv_seans.stdin.flush();나머지,XƏTA=interaktiv_seans.communicate(timeout=15)
                assert interaktiv_seans.returncode==0 and b'PTY allocation request failed' not in XƏTA,(interaktiv_seans.returncode,XƏTA)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                seçilmiş_sahə_VALUE.close()
                if interaktiv_seans.poll() is None:interaktiv_seans.kill();interaktiv_seans.wait()
            hesabat_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Bağlan, 수):
                verilənlər=bytearray()
                while len(verilənlər)<수:
                    덩이=Bağlan.recv(수-len(verilənlər))
                    if not 덩이: raise AssertionError('RFB EOF')
                    verilənlər.extend(덩이)
                return bytes(verilənlər)
            def 화면인증(parol_VALUE):
                Bağlan=socket.create_connection(('127.0.0.5',화면포트),10);Bağlan.settimeout(30)
                assert 정확히(Bağlan,12)==b'RFB 003.008\n'
                Bağlan.sendall(b'RFB 003.008\n');assert 정확히(Bağlan,2)==b'\x01\x02'
                Bağlan.sendall(b'\x02');yarış_VALUE=정확히(Bağlan,16)
                입력암호=parol_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Bağlan.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(yarış_VALUE))
                vəziyyət_VALUE=struct.unpack('!I',정확히(Bağlan,4))[0]
                return Bağlan,vəziyyət_VALUE
            yanlış_parol='!' if not Sazlama['vnc_password'].startswith('!') else '?'
            Bağlan,vəziyyət_VALUE=화면인증(yanlış_parol);assert vəziyyət_VALUE==1;Bağlan.close();time.sleep(.6)
            hesabat_VALUE['checks'].append('VNC incorrect password rejected')
            Bağlan,vəziyyət_VALUE=화면인증(Sazlama['vnc_password']);assert vəziyyət_VALUE==0
            with Bağlan:
                Bağlan.sendall(b'\x01');초기=정확히(Bağlan,24);너비,높이=struct.unpack('!HH',초기[:4]);Ad=정확히(Bağlan,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ad
                def 화면(증분=0):
                    Bağlan.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Bağlan,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    rəsm_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinatı,Y_koordinat,영역너비,영역높이,metod_MODE=struct.unpack('!HHHHi',정확히(Bağlan,12));assert metod_MODE==0 and x_koordinatı+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        piksel=정확히(Bağlan,영역너비*영역높이*4);합계+=len(piksel)
                        for Giriş in range(영역높이):rəsm_VALUE[((Y_koordinat+Giriş)*너비+x_koordinatı)*4:((Y_koordinat+Giriş)*너비+x_koordinatı+영역너비)*4]=piksel[Giriş*영역너비*4:(Giriş+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(rəsm_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                hesabat_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                hesabat_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_yaz)
                for simvol_VALUE_068c2631 in 'echo VNC_NATIVE_PASS\r':
                    simvol=0xff0d if simvol_VALUE_068c2631=='\r' else ord(simvol_VALUE_068c2631)
                    Bağlan.sendall(struct.pack('!BBHI',4,1,0,simvol));Bağlan.sendall(struct.pack('!BBHI',4,0,0,simvol))
                gözlə_vəziyyət(b'VNC_NATIVE_PASS',처음)
                hesabat_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simvol,bas_VALUE=1):Bağlan.sendall(struct.pack('!BBHI',4,bas_VALUE,0,simvol))
                처음=len(LOG_yaz)
                for simvol_VALUE_068c2631 in 'echo ':글쇠(ord(simvol_VALUE_068c2631))
                글쇠(0xffc6)
                for simvol_VALUE_068c2631 in 'gksrmf':글쇠(ord(simvol_VALUE_068c2631))
                글쇠(0xffc6);글쇠(0xff0d)
                gözlə_vəziyyət('\r\n한글\r\n'.encode(),처음)
                hesabat_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Bağlan.sendall(struct.pack('!BBHH',5,0,120,100))
                hesabat_VALUE['checks'].append('VNC pointer input accepted')
            Proses_VALUE.stdin.write(b'poweroff\n');Proses_VALUE.stdin.flush();Proses_VALUE.wait(timeout=15);assert Proses_VALUE.returncode==0
            hesabat_VALUE['passed']=True
    finally:
        if Proses_VALUE and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses_VALUE.kill();Proses_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_yaz)
        (출력/'report.json').write_text(json.dumps(hesabat_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(hesabat_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': İcra_Et()
