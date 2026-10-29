#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from yenza_umyalo import 기준, Umlayelo
from iNethiwekhi_ibhuloho import iNethiwekhi_ibhuloho


def Sebenzisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Izinhlelo = json.loads(인수.access.read_text())
    umbiko_inani = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def okungasho_lutho_intuba():
        with socket.socket() as Xhumanisa:
            Xhumanisa.bind(('127.0.0.5', 0))
            return Xhumanisa.getsockname()[1]
    isihumushi_miyalelo_intuba, 화면포트, ifayela_intuba = okungasho_lutho_intuba(), okungasho_lutho_intuba(), okungasho_lutho_intuba()
    loga_umugqa = bytearray()
    Inqubo_inani = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, iNethiwekhi_ibhuloho(ifayela_intuba,
                ['tcp:{}:22'.format(isihumushi_miyalelo_intuba), 'tcp:{}:5900'.format(화면포트)], singatha_ikheli='127.0.0.5') as ibhuloho_inani:
            실행인수 = Umlayelo()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Inqubo_inani = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ibhuloho_inani.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    imininingwane = Inqubo_inani.stdout.read(4096)
                    if not imininingwane: break
                    loga_umugqa.extend(imininingwane)
            uhlu_lwemilayezo_inani = threading.Thread(target=수집, daemon=True)
            uhlu_lwemilayezo_inani.start()
            def 기다림(Amagama_I_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Amagama_I_SMS not in loga_umugqa[처음:]:
                    if time.monotonic()>끝 or Inqubo_inani.poll() is not None:
                        raise AssertionError('Missing '+repr(Amagama_I_SMS)+'\n'+loga_umugqa[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ivikelekile_isihumushi_miyalelo(iphasiwedi_inani, umyalelo_inani, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=iphasiwedi_inani
                인수=['ssh','-v']+list(추가)+['-p',str(isihumushi_miyalelo_intuba),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',umyalelo_inani]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=ivikelekile_isihumushi_miyalelo('!' + Izinhlelo['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in loga_umugqa, 결과.stderr
            umbiko_inani['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=ivikelekile_isihumushi_miyalelo(Izinhlelo['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            umbiko_inani['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            umbiko_inani['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=ivikelekile_isihumushi_miyalelo(Izinhlelo['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            umbiko_inani['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=ivikelekile_isihumushi_miyalelo(Izinhlelo['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            umbiko_inani['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=ivikelekile_isihumushi_miyalelo(Izinhlelo['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            umbiko_inani['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(isihumushi_miyalelo_intuba),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ingxoxo_nekhompiyutha_isikhathi_sokwenza=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();okukhethiwe_inani=selectors.DefaultSelector();okukhethiwe_inani.register(ingxoxo_nekhompiyutha_isikhathi_sokwenza.stdout,selectors.EVENT_READ)
            def 대화읽기(khombisa_inani):
                마감=time.monotonic()+30
                while khombisa_inani not in 대화기록:
                    if time.monotonic()>마감 or ingxoxo_nekhompiyutha_isikhathi_sokwenza.poll() is not None:raise AssertionError('SSH interactive missing '+repr(khombisa_inani)+' '+repr(bytes(대화기록)))
                    for okufakwayo_inani,_ in okukhethiwe_inani.select(.1):
                        조각=okufakwayo_inani.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ingxoxo_nekhompiyutha_isikhathi_sokwenza.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ingxoxo_nekhompiyutha_isikhathi_sokwenza.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ingxoxo_nekhompiyutha_isikhathi_sokwenza.stdin.write(b'\x04');ingxoxo_nekhompiyutha_isikhathi_sokwenza.stdin.flush();나머지,Iphutha=ingxoxo_nekhompiyutha_isikhathi_sokwenza.communicate(timeout=15)
                assert ingxoxo_nekhompiyutha_isikhathi_sokwenza.returncode==0 and b'PTY allocation request failed' not in Iphutha,(ingxoxo_nekhompiyutha_isikhathi_sokwenza.returncode,Iphutha)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                okukhethiwe_inani.close()
                if ingxoxo_nekhompiyutha_isikhathi_sokwenza.poll() is None:ingxoxo_nekhompiyutha_isikhathi_sokwenza.kill();ingxoxo_nekhompiyutha_isikhathi_sokwenza.wait()
            umbiko_inani['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Xhumanisa, 수):
                imininingwane=bytearray()
                while len(imininingwane)<수:
                    덩이=Xhumanisa.recv(수-len(imininingwane))
                    if not 덩이: raise AssertionError('RFB EOF')
                    imininingwane.extend(덩이)
                return bytes(imininingwane)
            def 화면인증(iphasiwedi_inani):
                Xhumanisa=socket.create_connection(('127.0.0.5',화면포트),10);Xhumanisa.settimeout(30)
                assert 정확히(Xhumanisa,12)==b'RFB 003.008\n'
                Xhumanisa.sendall(b'RFB 003.008\n');assert 정확히(Xhumanisa,2)==b'\x01\x02'
                Xhumanisa.sendall(b'\x02');inselele_inani=정확히(Xhumanisa,16)
                입력암호=iphasiwedi_inani.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Xhumanisa.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(inselele_inani))
                isimo_inani=struct.unpack('!I',정확히(Xhumanisa,4))[0]
                return Xhumanisa,isimo_inani
            akusikho_iphasiwedi='!' if not Izinhlelo['vnc_password'].startswith('!') else '?'
            Xhumanisa,isimo_inani=화면인증(akusikho_iphasiwedi);assert isimo_inani==1;Xhumanisa.close();time.sleep(.6)
            umbiko_inani['checks'].append('VNC incorrect password rejected')
            Xhumanisa,isimo_inani=화면인증(Izinhlelo['vnc_password']);assert isimo_inani==0
            with Xhumanisa:
                Xhumanisa.sendall(b'\x01');초기=정확히(Xhumanisa,24);너비,높이=struct.unpack('!HH',초기[:4]);Igama=정확히(Xhumanisa,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Igama
                def 화면(증분=0):
                    Xhumanisa.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Xhumanisa,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    umdwebo_inani=bytearray(너비*높이*4)
                    for _ in range(수):
                        okuxhumanisa_u_x,세로좌표,영역너비,영역높이,indlela_inqubo=struct.unpack('!HHHHi',정확히(Xhumanisa,12));assert indlela_inqubo==0 and okuxhumanisa_u_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        i_pel=정확히(Xhumanisa,영역너비*영역높이*4);합계+=len(i_pel)
                        for umugqa in range(영역높이):umdwebo_inani[((세로좌표+umugqa)*너비+okuxhumanisa_u_x)*4:((세로좌표+umugqa)*너비+okuxhumanisa_u_x+영역너비)*4]=i_pel[umugqa*영역너비*4:(umugqa+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(umdwebo_inani),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                umbiko_inani['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                umbiko_inani['checks'].append('RFB incremental update')
                처음=len(loga_umugqa)
                for uhlamvusimo_inani in 'echo VNC_NATIVE_PASS\r':
                    uphawu_ad6f1a96=0xff0d if uhlamvusimo_inani=='\r' else ord(uhlamvusimo_inani)
                    Xhumanisa.sendall(struct.pack('!BBHI',4,1,0,uphawu_ad6f1a96));Xhumanisa.sendall(struct.pack('!BBHI',4,0,0,uphawu_ad6f1a96))
                기다림(b'VNC_NATIVE_PASS',처음)
                umbiko_inani['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(uphawu_ad6f1a96,누름=1):Xhumanisa.sendall(struct.pack('!BBHI',4,누름,0,uphawu_ad6f1a96))
                처음=len(loga_umugqa)
                for uhlamvusimo_inani in 'echo ':글쇠(ord(uhlamvusimo_inani))
                글쇠(0xffc6)
                for uhlamvusimo_inani in 'gksrmf':글쇠(ord(uhlamvusimo_inani))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                umbiko_inani['checks'].append('Native VNC F9 two-set Hangul composition')
                Xhumanisa.sendall(struct.pack('!BBHH',5,0,120,100))
                umbiko_inani['checks'].append('VNC pointer input accepted')
            Inqubo_inani.stdin.write(b'poweroff\n');Inqubo_inani.stdin.flush();Inqubo_inani.wait(timeout=15);assert Inqubo_inani.returncode==0
            umbiko_inani['passed']=True
    finally:
        if Inqubo_inani and Inqubo_inani.poll() is None:
            Inqubo_inani.terminate()
            try: Inqubo_inani.wait(timeout=5)
            except subprocess.TimeoutExpired: Inqubo_inani.kill();Inqubo_inani.wait()
        (출력/'serial.log').write_bytes(loga_umugqa)
        (출력/'report.json').write_text(json.dumps(umbiko_inani,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(umbiko_inani,ensure_ascii=False,indent=2))


if __name__=='__main__': Sebenzisa()
