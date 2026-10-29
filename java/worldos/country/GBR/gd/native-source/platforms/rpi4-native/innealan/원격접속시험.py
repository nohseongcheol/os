#!/usr/bin/env python3
"""dearbh_dàta OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from gnìomhaich_àithne import tilg_freumh, àithne
from lìonra_drochaid import lìonra_drochaid


def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=tilg_freumh / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=tilg_freumh / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=tilg_freumh / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    roghainnean = json.loads(인수.access.read_text())
    aithisg_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def falamh_port():
        with socket.socket() as CONNECT:
            CONNECT.bind(('127.0.0.5', 0))
            return CONNECT.getsockname()[1]
    slige_port, 화면포트, faidhle_port = falamh_port(), falamh_port(), falamh_port()
    LOG_ràgh = bytearray()
    Pròiseas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, lìonra_drochaid(faidhle_port,
                ['tcp:{}:22'.format(slige_port), 'tcp:{}:5900'.format(화면포트)], òstair_ADDRESS='127.0.0.5') as drochaid_VALUE:
            실행인수 = àithne()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Pròiseas_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + drochaid_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    dàta = Pròiseas_VALUE.stdout.read(4096)
                    if not dàta: break
                    LOG_ràgh.extend(dàta)
            snàithlean_VALUE = threading.Thread(target=수집, daemon=True)
            snàithlean_VALUE.start()
            def fuirich_cor(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_ràgh[처음:]:
                    if time.monotonic()>끝 or Pròiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_ràgh[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            fuirich_cor(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def tèarainte_slige(facal_faire_VALUE, treòrachadh_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=facal_faire_VALUE
                인수=['ssh','-v']+list(추가)+['-p',str(slige_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',treòrachadh_VALUE]
                tomhas=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return tomhas
            tomhas=tèarainte_slige('!' + roghainnean['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(tomhas.stderr)
            assert tomhas.returncode!=0 and b'Permission denied' in tomhas.stderr and b'SHOULD_NOT_RUN' not in LOG_ràgh, tomhas.stderr
            aithisg_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            tomhas=tèarainte_slige(roghainnean['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(tomhas.stderr)
            (출력/'ssh-output.txt').write_bytes(tomhas.stdout)
            assert tomhas.returncode==0 and b'SSH_NATIVE_PASS' in tomhas.stdout, (tomhas.returncode,tomhas.stdout,tomhas.stderr)
            aithisg_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in tomhas.stderr, tomhas.stderr
            aithisg_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            tomhas=tèarainte_slige(roghainnean['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert tomhas.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in tomhas.stdout,tomhas.stdout
            aithisg_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            tomhas=tèarainte_slige(roghainnean['ssh_password'], 'missing_remote_command')
            assert tomhas.returncode==127,tomhas.returncode
            aithisg_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            tomhas=tèarainte_slige(roghainnean['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(tomhas.stderr)
            assert tomhas.returncode==0 and 'class 창예제'.encode() in tomhas.stdout, (tomhas.returncode,tomhas.stdout,tomhas.stderr)
            assert tomhas.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, tomhas.stderr
            aithisg_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(slige_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            eadar_ghnìomhach_seisean=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();taghadh_VALUE=selectors.DefaultSelector();taghadh_VALUE.register(eadar_ghnìomhach_seisean.stdout,selectors.EVENT_READ)
            def 대화읽기(show_VALUE):
                마감=time.monotonic()+30
                while show_VALUE not in 대화기록:
                    if time.monotonic()>마감 or eadar_ghnìomhach_seisean.poll() is not None:raise AssertionError('SSH interactive missing '+repr(show_VALUE)+' '+repr(bytes(대화기록)))
                    for cur_a_steach_VALUE,_ in taghadh_VALUE.select(.1):
                        조각=cur_a_steach_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                eadar_ghnìomhach_seisean.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');eadar_ghnìomhach_seisean.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                eadar_ghnìomhach_seisean.stdin.write(b'\x04');eadar_ghnìomhach_seisean.stdin.flush();나머지,Mearachd=eadar_ghnìomhach_seisean.communicate(timeout=15)
                assert eadar_ghnìomhach_seisean.returncode==0 and b'PTY allocation request failed' not in Mearachd,(eadar_ghnìomhach_seisean.returncode,Mearachd)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                taghadh_VALUE.close()
                if eadar_ghnìomhach_seisean.poll() is None:eadar_ghnìomhach_seisean.kill();eadar_ghnìomhach_seisean.wait()
            aithisg_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(CONNECT, 수):
                dàta=bytearray()
                while len(dàta)<수:
                    덩이=CONNECT.recv(수-len(dàta))
                    if not 덩이: raise AssertionError('RFB EOF')
                    dàta.extend(덩이)
                return bytes(dàta)
            def 화면인증(facal_faire_VALUE):
                CONNECT=socket.create_connection(('127.0.0.5',화면포트),10);CONNECT.settimeout(30)
                assert 정확히(CONNECT,12)==b'RFB 003.008\n'
                CONNECT.sendall(b'RFB 003.008\n');assert 정확히(CONNECT,2)==b'\x01\x02'
                CONNECT.sendall(b'\x02');dùbhlan_VALUE=정확히(CONNECT,16)
                입력암호=facal_faire_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                CONNECT.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(dùbhlan_VALUE))
                cor_VALUE=struct.unpack('!I',정확히(CONNECT,4))[0]
                return CONNECT,cor_VALUE
            mì_dhligheach_facal_faire='!' if not roghainnean['vnc_password'].startswith('!') else '?'
            CONNECT,cor_VALUE=화면인증(mì_dhligheach_facal_faire);assert cor_VALUE==1;CONNECT.close();time.sleep(.6)
            aithisg_VALUE['checks'].append('VNC incorrect password rejected')
            CONNECT,cor_VALUE=화면인증(roghainnean['vnc_password']);assert cor_VALUE==0
            with CONNECT:
                CONNECT.sendall(b'\x01');초기=정확히(CONNECT,24);너비,높이=struct.unpack('!HH',초기[:4]);Ainm=정확히(CONNECT,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ainm
                def 화면(증분=0):
                    CONNECT.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(CONNECT,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    tarraing_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        co_chomharra_x,세로좌표,영역너비,영역높이,dòigh_MODE=struct.unpack('!HHHHi',정확히(CONNECT,12));assert dòigh_MODE==0 and co_chomharra_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pel=정확히(CONNECT,영역너비*영역높이*4);합계+=len(pel)
                        for loidhne in range(영역높이):tarraing_VALUE[((세로좌표+loidhne)*너비+co_chomharra_x)*4:((세로좌표+loidhne)*너비+co_chomharra_x+영역너비)*4]=pel[loidhne*영역너비*4:(loidhne+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(tarraing_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                aithisg_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                aithisg_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_ràgh)
                for caractar_VALUE in 'echo VNC_NATIVE_PASS\r':
                    samhla=0xff0d if caractar_VALUE=='\r' else ord(caractar_VALUE)
                    CONNECT.sendall(struct.pack('!BBHI',4,1,0,samhla));CONNECT.sendall(struct.pack('!BBHI',4,0,0,samhla))
                fuirich_cor(b'VNC_NATIVE_PASS',처음)
                aithisg_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(samhla,누름=1):CONNECT.sendall(struct.pack('!BBHI',4,누름,0,samhla))
                처음=len(LOG_ràgh)
                for caractar_VALUE in 'echo ':글쇠(ord(caractar_VALUE))
                글쇠(0xffc6)
                for caractar_VALUE in 'gksrmf':글쇠(ord(caractar_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                fuirich_cor('\r\n한글\r\n'.encode(),처음)
                aithisg_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                CONNECT.sendall(struct.pack('!BBHH',5,0,120,100))
                aithisg_VALUE['checks'].append('VNC pointer input accepted')
            Pròiseas_VALUE.stdin.write(b'poweroff\n');Pròiseas_VALUE.stdin.flush();Pròiseas_VALUE.wait(timeout=15);assert Pròiseas_VALUE.returncode==0
            aithisg_VALUE['passed']=True
    finally:
        if Pròiseas_VALUE and Pròiseas_VALUE.poll() is None:
            Pròiseas_VALUE.terminate()
            try: Pròiseas_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Pròiseas_VALUE.kill();Pròiseas_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_ràgh)
        (출력/'report.json').write_text(json.dumps(aithisg_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(aithisg_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': ruith()
