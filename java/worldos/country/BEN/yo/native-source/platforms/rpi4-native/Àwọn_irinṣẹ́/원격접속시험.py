#!/usr/bin/env python3
"""gangan_détà OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ
from Alásopọ̀_afará import Alásopọ̀_afará


def Rọ́ọ̀nù():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Àwọn_ààtò = json.loads(인수.access.read_text())
    ìjábọ̀_iye = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def òfìfo_ojú():
        with socket.socket() as Darapọ̀:
            Darapọ̀.bind(('127.0.0.5', 0))
            return Darapọ̀.getsockname()[1]
    ṣẹ́ẹ̀lì_ojú, 화면포트, fáìlì_ojú = òfìfo_ojú(), òfìfo_ojú(), òfìfo_ojú()
    àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray()
    Ìlànà_iye = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Alásopọ̀_afará(fáìlì_ojú,
                ['tcp:{}:22'.format(ṣẹ́ẹ̀lì_ojú), 'tcp:{}:5900'.format(화면포트)], olùpèsè_àdírẹ́ẹ̀sì='127.0.0.5') as afará_iye:
            실행인수 = Àṣẹ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Ìlànà_iye = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + afará_iye.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    détà = Ìlànà_iye.stdout.read(4096)
                    if not détà: break
                    àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
            èròjà_atẹ̀lélànà_iye = threading.Thread(target=수집, daemon=True)
            èròjà_atẹ̀lélànà_iye.start()
            def 기다림(Ọ̀rọ̀_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Ọ̀rọ̀_SMS not in àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:]:
                    if time.monotonic()>끝 or Ìlànà_iye.poll() is not None:
                        raise AssertionError('Missing '+repr(Ọ̀rọ̀_SMS)+'\n'+àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def Tóláàbò_ṣẹ́ẹ̀lì(ọ̀rọ̀_aṣínà_iye, ìtọ́sọ́nà_iye, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ọ̀rọ̀_aṣínà_iye
                인수=['ssh','-v']+list(추가)+['-p',str(ṣẹ́ẹ̀lì_ojú),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ìtọ́sọ́nà_iye]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=Tóláàbò_ṣẹ́ẹ̀lì('!' + Àwọn_ààtò['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in àkọsílẹ̀_ìṣe_ìlà_ìbú, 결과.stderr
            ìjábọ̀_iye['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=Tóláàbò_ṣẹ́ẹ̀lì(Àwọn_ààtò['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ìjábọ̀_iye['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ìjábọ̀_iye['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=Tóláàbò_ṣẹ́ẹ̀lì(Àwọn_ààtò['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ìjábọ̀_iye['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=Tóláàbò_ṣẹ́ẹ̀lì(Àwọn_ààtò['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ìjábọ̀_iye['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=Tóláàbò_ṣẹ́ẹ̀lì(Àwọn_ààtò['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ìjábọ̀_iye['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ṣẹ́ẹ̀lì_ojú),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ìjọṣepọ̀_sáà=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ẹ̀yàn_iye=selectors.DefaultSelector();ẹ̀yàn_iye.register(ìjọṣepọ̀_sáà.stdout,selectors.EVENT_READ)
            def 대화읽기(ṣàfihàn_iye):
                마감=time.monotonic()+30
                while ṣàfihàn_iye not in 대화기록:
                    if time.monotonic()>마감 or ìjọṣepọ̀_sáà.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ṣàfihàn_iye)+' '+repr(bytes(대화기록)))
                    for ìgbéwọlé_iye,_ in ẹ̀yàn_iye.select(.1):
                        조각=ìgbéwọlé_iye.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ìjọṣepọ̀_sáà.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ìjọṣepọ̀_sáà.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ìjọṣepọ̀_sáà.stdin.write(b'\x04');ìjọṣepọ̀_sáà.stdin.flush();나머지,àṣìṣe=ìjọṣepọ̀_sáà.communicate(timeout=15)
                assert ìjọṣepọ̀_sáà.returncode==0 and b'PTY allocation request failed' not in àṣìṣe,(ìjọṣepọ̀_sáà.returncode,àṣìṣe)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ẹ̀yàn_iye.close()
                if ìjọṣepọ̀_sáà.poll() is None:ìjọṣepọ̀_sáà.kill();ìjọṣepọ̀_sáà.wait()
            ìjábọ̀_iye['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Darapọ̀, 수):
                détà=bytearray()
                while len(détà)<수:
                    덩이=Darapọ̀.recv(수-len(détà))
                    if not 덩이: raise AssertionError('RFB EOF')
                    détà.extend(덩이)
                return bytes(détà)
            def 화면인증(ọ̀rọ̀_aṣínà_iye):
                Darapọ̀=socket.create_connection(('127.0.0.5',화면포트),10);Darapọ̀.settimeout(30)
                assert 정확히(Darapọ̀,12)==b'RFB 003.008\n'
                Darapọ̀.sendall(b'RFB 003.008\n');assert 정확히(Darapọ̀,2)==b'\x01\x02'
                Darapọ̀.sendall(b'\x02');ìpèníjà_iye=정확히(Darapọ̀,16)
                입력암호=ọ̀rọ̀_aṣínà_iye.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Darapọ̀.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ìpèníjà_iye))
                ipò_iye=struct.unpack('!I',정확히(Darapọ̀,4))[0]
                return Darapọ̀,ipò_iye
            aláìbẹgbẹmu_ọ̀rọ̀_aṣínà='!' if not Àwọn_ààtò['vnc_password'].startswith('!') else '?'
            Darapọ̀,ipò_iye=화면인증(aláìbẹgbẹmu_ọ̀rọ̀_aṣínà);assert ipò_iye==1;Darapọ̀.close();time.sleep(.6)
            ìjábọ̀_iye['checks'].append('VNC incorrect password rejected')
            Darapọ̀,ipò_iye=화면인증(Àwọn_ààtò['vnc_password']);assert ipò_iye==0
            with Darapọ̀:
                Darapọ̀.sendall(b'\x01');초기=정확히(Darapọ̀,24);너비,높이=struct.unpack('!HH',초기[:4]);Orúkọ=정확히(Darapọ̀,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Orúkọ
                def 화면(증분=0):
                    Darapọ̀.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Darapọ̀,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    íyàwòrán_iye=bytearray(너비*높이*4)
                    for _ in range(수):
                        ibi_ìtọ́kasí_x,세로좌표,영역너비,영역높이,ìlànà_móòdù=struct.unpack('!HHHHi',정확히(Darapọ̀,12));assert ìlànà_móòdù==0 and ibi_ìtọ́kasí_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        píkísẹ̀=정확히(Darapọ̀,영역너비*영역높이*4);합계+=len(píkísẹ̀)
                        for ìlà in range(영역높이):íyàwòrán_iye[((세로좌표+ìlà)*너비+ibi_ìtọ́kasí_x)*4:((세로좌표+ìlà)*너비+ibi_ìtọ́kasí_x+영역너비)*4]=píkísẹ̀[ìlà*영역너비*4:(ìlà+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(íyàwòrán_iye),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ìjábọ̀_iye['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ìjábọ̀_iye['checks'].append('RFB incremental update')
                처음=len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                for ẹyọ_ọ̀rọ̀_iye in 'echo VNC_NATIVE_PASS\r':
                    àmì=0xff0d if ẹyọ_ọ̀rọ̀_iye=='\r' else ord(ẹyọ_ọ̀rọ̀_iye)
                    Darapọ̀.sendall(struct.pack('!BBHI',4,1,0,àmì));Darapọ̀.sendall(struct.pack('!BBHI',4,0,0,àmì))
                기다림(b'VNC_NATIVE_PASS',처음)
                ìjábọ̀_iye['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(àmì,누름=1):Darapọ̀.sendall(struct.pack('!BBHI',4,누름,0,àmì))
                처음=len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                for ẹyọ_ọ̀rọ̀_iye in 'echo ':글쇠(ord(ẹyọ_ọ̀rọ̀_iye))
                글쇠(0xffc6)
                for ẹyọ_ọ̀rọ̀_iye in 'gksrmf':글쇠(ord(ẹyọ_ọ̀rọ̀_iye))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ìjábọ̀_iye['checks'].append('Native VNC F9 two-set Hangul composition')
                Darapọ̀.sendall(struct.pack('!BBHH',5,0,120,100))
                ìjábọ̀_iye['checks'].append('VNC pointer input accepted')
            Ìlànà_iye.stdin.write(b'poweroff\n');Ìlànà_iye.stdin.flush();Ìlànà_iye.wait(timeout=15);assert Ìlànà_iye.returncode==0
            ìjábọ̀_iye['passed']=True
    finally:
        if Ìlànà_iye and Ìlànà_iye.poll() is None:
            Ìlànà_iye.terminate()
            try: Ìlànà_iye.wait(timeout=5)
            except subprocess.TimeoutExpired: Ìlànà_iye.kill();Ìlànà_iye.wait()
        (출력/'serial.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú)
        (출력/'report.json').write_text(json.dumps(ìjábọ̀_iye,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ìjábọ̀_iye,ensure_ascii=False,indent=2))


if __name__=='__main__': Rọ́ọ̀nù()
