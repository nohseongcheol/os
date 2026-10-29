#!/usr/bin/env python3
"""real_ma_lumotlar OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from bajarmoq_buyruq import Project_ildiz, Buyruq
from 통신다리 import 통신다리


def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Project_ildiz / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Project_ildiz / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Project_ildiz / 'build/verification/native-remote')
    인수 = parser_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Moslamalar = json.loads(인수.access.read_text())
    hisobot_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def bo_sh_port():
        with socket.socket() as Ulanish:
            Ulanish.bind(('127.0.0.5', 0))
            return Ulanish.getsockname()[1]
    qobiq_port, 화면포트, fayl_port = bo_sh_port(), bo_sh_port(), bo_sh_port()
    LOG_satr = bytearray()
    Jarayon_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(fayl_port,
                ['tcp:{}:22'.format(qobiq_port), 'tcp:{}:5900'.format(화면포트)], tashkilotchi_manzil='127.0.0.5') as 다리:
            실행인수 = Buyruq()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Jarayon_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ma_lumotlar = Jarayon_VALUE.stdout.read(4096)
                    if not ma_lumotlar: break
                    LOG_satr.extend(ma_lumotlar)
            oqim_VALUE_5b72a632 = threading.Thread(target=수집, daemon=True)
            oqim_VALUE_5b72a632.start()
            def bir_daqiqa_holat(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_satr[처음:]:
                    if time.monotonic()>끝 or Jarayon_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_satr[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            bir_daqiqa_holat(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def xavfsiz_qobiq(parol_VALUE, qo_llanma_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=parol_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(qobiq_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',qo_llanma_VALUE]
                o_lchov=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return o_lchov
            o_lchov=xavfsiz_qobiq('!' + Moslamalar['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(o_lchov.stderr)
            assert o_lchov.returncode!=0 and b'Permission denied' in o_lchov.stderr and b'SHOULD_NOT_RUN' not in LOG_satr, o_lchov.stderr
            hisobot_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            o_lchov=xavfsiz_qobiq(Moslamalar['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(o_lchov.stderr)
            (출력/'ssh-output.txt').write_bytes(o_lchov.stdout)
            assert o_lchov.returncode==0 and b'SSH_NATIVE_PASS' in o_lchov.stdout, (o_lchov.returncode,o_lchov.stdout,o_lchov.stderr)
            hisobot_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in o_lchov.stderr, o_lchov.stderr
            hisobot_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            o_lchov=xavfsiz_qobiq(Moslamalar['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert o_lchov.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in o_lchov.stdout,o_lchov.stdout
            hisobot_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            o_lchov=xavfsiz_qobiq(Moslamalar['ssh_password'], 'missing_remote_command')
            assert o_lchov.returncode==127,o_lchov.returncode
            hisobot_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            o_lchov=xavfsiz_qobiq(Moslamalar['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(o_lchov.stderr)
            assert o_lchov.returncode==0 and 'class 창예제'.encode() in o_lchov.stdout, (o_lchov.returncode,o_lchov.stdout,o_lchov.stderr)
            assert o_lchov.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, o_lchov.stderr
            hisobot_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(qobiq_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            o_zaro_faol_seans=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();tanlanma_VALUE=selectors.DefaultSelector();tanlanma_VALUE.register(o_zaro_faol_seans.stdout,selectors.EVENT_READ)
            def 대화읽기(ko_rsatmoq_VALUE):
                마감=time.monotonic()+30
                while ko_rsatmoq_VALUE not in 대화기록:
                    if time.monotonic()>마감 or o_zaro_faol_seans.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ko_rsatmoq_VALUE)+' '+repr(bytes(대화기록)))
                    for kiritish_VALUE,_ in tanlanma_VALUE.select(.1):
                        조각=kiritish_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                o_zaro_faol_seans.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');o_zaro_faol_seans.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                o_zaro_faol_seans.stdin.write(b'\x04');o_zaro_faol_seans.stdin.flush();나머지,Xato=o_zaro_faol_seans.communicate(timeout=15)
                assert o_zaro_faol_seans.returncode==0 and b'PTY allocation request failed' not in Xato,(o_zaro_faol_seans.returncode,Xato)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                tanlanma_VALUE.close()
                if o_zaro_faol_seans.poll() is None:o_zaro_faol_seans.kill();o_zaro_faol_seans.wait()
            hisobot_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Ulanish, 수):
                ma_lumotlar=bytearray()
                while len(ma_lumotlar)<수:
                    덩이=Ulanish.recv(수-len(ma_lumotlar))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ma_lumotlar.extend(덩이)
                return bytes(ma_lumotlar)
            def 화면인증(parol_VALUE):
                Ulanish=socket.create_connection(('127.0.0.5',화면포트),10);Ulanish.settimeout(30)
                assert 정확히(Ulanish,12)==b'RFB 003.008\n'
                Ulanish.sendall(b'RFB 003.008\n');assert 정확히(Ulanish,2)==b'\x01\x02'
                Ulanish.sendall(b'\x02');chaqiruv_VALUE=정확히(Ulanish,16)
                입력암호=parol_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Ulanish.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(chaqiruv_VALUE))
                holat_VALUE_e10195a1=struct.unpack('!I',정확히(Ulanish,4))[0]
                return Ulanish,holat_VALUE_e10195a1
            xato_parol='!' if not Moslamalar['vnc_password'].startswith('!') else '?'
            Ulanish,holat_VALUE_e10195a1=화면인증(xato_parol);assert holat_VALUE_e10195a1==1;Ulanish.close();time.sleep(.6)
            hisobot_VALUE['checks'].append('VNC incorrect password rejected')
            Ulanish,holat_VALUE_e10195a1=화면인증(Moslamalar['vnc_password']);assert holat_VALUE_e10195a1==0
            with Ulanish:
                Ulanish.sendall(b'\x01');초기=정확히(Ulanish,24);너비,높이=struct.unpack('!HH',초기[:4]);Nomi=정확히(Ulanish,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nomi
                def 화면(증분=0):
                    Ulanish.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Ulanish,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    chizish_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinata,Y_tugmasi_koordinat,영역너비,영역높이,uslub_MODE=struct.unpack('!HHHHi',정확히(Ulanish,12));assert uslub_MODE==0 and x_koordinata+영역너비<=너비 and Y_tugmasi_koordinat+영역높이<=높이
                        piksel=정확히(Ulanish,영역너비*영역높이*4);합계+=len(piksel)
                        for satr in range(영역높이):chizish_VALUE[((Y_tugmasi_koordinat+satr)*너비+x_koordinata)*4:((Y_tugmasi_koordinat+satr)*너비+x_koordinata+영역너비)*4]=piksel[satr*영역너비*4:(satr+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(chizish_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                hisobot_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                hisobot_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_satr)
                for belgi_VALUE in 'echo VNC_NATIVE_PASS\r':
                    ramz=0xff0d if belgi_VALUE=='\r' else ord(belgi_VALUE)
                    Ulanish.sendall(struct.pack('!BBHI',4,1,0,ramz));Ulanish.sendall(struct.pack('!BBHI',4,0,0,ramz))
                bir_daqiqa_holat(b'VNC_NATIVE_PASS',처음)
                hisobot_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ramz,누름=1):Ulanish.sendall(struct.pack('!BBHI',4,누름,0,ramz))
                처음=len(LOG_satr)
                for belgi_VALUE in 'echo ':글쇠(ord(belgi_VALUE))
                글쇠(0xffc6)
                for belgi_VALUE in 'gksrmf':글쇠(ord(belgi_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                bir_daqiqa_holat('\r\n한글\r\n'.encode(),처음)
                hisobot_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Ulanish.sendall(struct.pack('!BBHH',5,0,120,100))
                hisobot_VALUE['checks'].append('VNC pointer input accepted')
            Jarayon_VALUE.stdin.write(b'poweroff\n');Jarayon_VALUE.stdin.flush();Jarayon_VALUE.wait(timeout=15);assert Jarayon_VALUE.returncode==0
            hisobot_VALUE['passed']=True
    finally:
        if Jarayon_VALUE and Jarayon_VALUE.poll() is None:
            Jarayon_VALUE.terminate()
            try: Jarayon_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Jarayon_VALUE.kill();Jarayon_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_satr)
        (출력/'report.json').write_text(json.dumps(hisobot_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(hisobot_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Bajarish()
