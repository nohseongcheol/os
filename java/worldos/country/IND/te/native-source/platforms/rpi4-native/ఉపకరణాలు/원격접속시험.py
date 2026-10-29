#!/usr/bin/env python3
"""వాస్తవ_డేటా OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం, ఆదేశము
from నెట్_వర్క్_బ్రిడ్జ్ import నెట్_వర్క్_బ్రిడ్జ్


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--kernel', type=Path, default=ప్రొజెక్ట్_మూలం / 'build/kernel8.img')
    పార్సర్_48ee4b1b.add_argument('--access', type=Path, default=ప్రొజెక్ట్_మూలం / 'build/remote/access.json')
    పార్సర్_48ee4b1b.add_argument('--output', type=Path, default=ప్రొజెక్ట్_మూలం / 'build/verification/native-remote')
    인수 = పార్సర్_48ee4b1b.parse_args()
    అవుట్పుట్ = 인수.output
    అవుట్పుట్.mkdir(parents=True, exist_ok=True)
    అమరికలు = json.loads(인수.access.read_text())
    నివేదిక_మూల్యం = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ఖాళీ_పోర్టు():
        with socket.socket() as కనెక్టుచేయి:
            కనెక్టుచేయి.bind(('127.0.0.5', 0))
            return కనెక్టుచేయి.getsockname()[1]
    షెల్_పోర్టు, 화면포트, ఫైలు_పోర్టు = ఖాళీ_పోర్టు(), ఖాళీ_పోర్టు(), ఖాళీ_పోర్టు()
    లాగ్_వరుస = bytearray()
    విధానం_మూల్యం = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, నెట్_వర్క్_బ్రిడ్జ్(ఫైలు_పోర్టు,
                ['tcp:{}:22'.format(షెల్_పోర్టు), 'tcp:{}:5900'.format(화면포트)], హోస్ట్_ఇమెయిల్='127.0.0.5') as బ్రిడ్జ్_మూల్యం:
            실행인수 = ఆదేశము()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            విధానం_మూల్యం = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + బ్రిడ్జ్_మూల్యం.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    డేటా = విధానం_మూల్యం.stdout.read(4096)
                    if not డేటా: break
                    లాగ్_వరుస.extend(డేటా)
            థ్రెడ్_మూల్యం = threading.Thread(target=수집, daemon=True)
            థ్రెడ్_మూల్యం.start()
            def వేచియుండు_స్థితి(పదం_పాఠం, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while పదం_పాఠం not in లాగ్_వరుస[처음:]:
                    if time.monotonic()>끝 or విధానం_మూల్యం.poll() is not None:
                        raise AssertionError('Missing '+repr(పదం_పాఠం)+'\n'+లాగ్_వరుస[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            వేచియుండు_స్థితి(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def సురక్షితం_షెల్(అనుమతిపదం_మూల్యం, సూచన_మూల్యం, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=అనుమతిపదం_మూల్యం
                인수=['ssh','-v']+list(추가)+['-p',str(షెల్_పోర్టు),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',సూచన_మూల్యం]
                ప్రమాణం=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ప్రమాణం
            ప్రమాణం=సురక్షితం_షెల్('!' + అమరికలు['ssh_password'], 'echo SHOULD_NOT_RUN')
            (అవుట్పుట్/'ssh-rejected.log').write_bytes(ప్రమాణం.stderr)
            assert ప్రమాణం.returncode!=0 and b'Permission denied' in ప్రమాణం.stderr and b'SHOULD_NOT_RUN' not in లాగ్_వరుస, ప్రమాణం.stderr
            నివేదిక_మూల్యం['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ప్రమాణం=సురక్షితం_షెల్(అమరికలు['ssh_password'], 'echo SSH_NATIVE_PASS')
            (అవుట్పుట్/'ssh.log').write_bytes(ప్రమాణం.stderr)
            (అవుట్పుట్/'ssh-output.txt').write_bytes(ప్రమాణం.stdout)
            assert ప్రమాణం.returncode==0 and b'SSH_NATIVE_PASS' in ప్రమాణం.stdout, (ప్రమాణం.returncode,ప్రమాణం.stdout,ప్రమాణం.stderr)
            నివేదిక_మూల్యం['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ప్రమాణం.stderr, ప్రమాణం.stderr
            నివేదిక_మూల్యం['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ప్రమాణం=సురక్షితం_షెల్(అమరికలు['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ప్రమాణం.returncode==0 and 'JAVA అవుట్పుట్: 안녕하세요 😀'.encode() in ప్రమాణం.stdout,ప్రమాణం.stdout
            నివేదిక_మూల్యం['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ప్రమాణం=సురక్షితం_షెల్(అమరికలు['ssh_password'], 'missing_remote_command')
            assert ప్రమాణం.returncode==127,ప్రమాణం.returncode
            నివేదిక_మూల్యం['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ప్రమాణం=సురక్షితం_షెల్(అమరికలు['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (అవుట్పుట్/'ssh-rekey.log').write_bytes(ప్రమాణం.stderr)
            assert ప్రమాణం.returncode==0 and 'class 창예제'.encode() in ప్రమాణం.stdout, (ప్రమాణం.returncode,ప్రమాణం.stdout,ప్రమాణం.stderr)
            assert ప్రమాణం.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ప్రమాణం.stderr
            నివేదిక_మూల్యం['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(షెల్_పోర్టు),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            పరస్పర_సెషన్=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ఎంపిక_మూల్యం=selectors.DefaultSelector();ఎంపిక_మూల్యం.register(పరస్పర_సెషన్.stdout,selectors.EVENT_READ)
            def 대화읽기(చూపించు_మూల్యం):
                마감=time.monotonic()+30
                while చూపించు_మూల్యం not in 대화기록:
                    if time.monotonic()>마감 or పరస్పర_సెషన్.poll() is not None:raise AssertionError('SSH interactive missing '+repr(చూపించు_మూల్యం)+' '+repr(bytes(대화기록)))
                    for ప్రవేశం_మూల్యం,_ in ఎంపిక_మూల్యం.select(.1):
                        조각=ప్రవేశం_మూల్యం.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                పరస్పర_సెషన్.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');పరస్పర_సెషన్.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                పరస్పర_సెషన్.stdin.write(b'\x04');పరస్పర_సెషన్.stdin.flush();나머지,దోషం=పరస్పర_సెషన్.communicate(timeout=15)
                assert పరస్పర_సెషన్.returncode==0 and b'PTY allocation request failed' not in దోషం,(పరస్పర_సెషన్.returncode,దోషం)
                (అవుట్పుట్/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ఎంపిక_మూల్యం.close()
                if పరస్పర_సెషన్.poll() is None:పరస్పర_సెషన్.kill();పరస్పర_సెషన్.wait()
            నివేదిక_మూల్యం['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(కనెక్టుచేయి, 수):
                డేటా=bytearray()
                while len(డేటా)<수:
                    덩이=కనెక్టుచేయి.recv(수-len(డేటా))
                    if not 덩이: raise AssertionError('RFB EOF')
                    డేటా.extend(덩이)
                return bytes(డేటా)
            def 화면인증(అనుమతిపదం_మూల్యం):
                కనెక్టుచేయి=socket.create_connection(('127.0.0.5',화면포트),10);కనెక్టుచేయి.settimeout(30)
                assert 정확히(కనెక్టుచేయి,12)==b'RFB 003.008\n'
                కనెక్టుచేయి.sendall(b'RFB 003.008\n');assert 정확히(కనెక్టుచేయి,2)==b'\x01\x02'
                కనెక్టుచేయి.sendall(b'\x02');సవాలు_మూల్యం=정확히(కనెక్టుచేయి,16)
                입력암호=అనుమతిపదం_మూల్యం.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                కనెక్టుచేయి.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(సవాలు_మూల్యం))
                స్థితి_మూల్యం=struct.unpack('!I',정확히(కనెక్టుచేయి,4))[0]
                return కనెక్టుచేయి,స్థితి_మూల్యం
            చెల్లని_అనుమతిపదం='!' if not అమరికలు['vnc_password'].startswith('!') else '?'
            కనెక్టుచేయి,స్థితి_మూల్యం=화면인증(చెల్లని_అనుమతిపదం);assert స్థితి_మూల్యం==1;కనెక్టుచేయి.close();time.sleep(.6)
            నివేదిక_మూల్యం['checks'].append('VNC incorrect password rejected')
            కనెక్టుచేయి,స్థితి_మూల్యం=화면인증(అమరికలు['vnc_password']);assert స్థితి_మూల్యం==0
            with కనెక్టుచేయి:
                కనెక్టుచేయి.sendall(b'\x01');초기=정확히(కనెక్టుచేయి,24);너비,높이=struct.unpack('!HH',초기[:4]);పేరు=정확히(కనెక్టుచేయి,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==పేరు
                def 화면(증분=0):
                    కనెక్టుచేయి.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(కనెక్టుచేయి,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    రేఖాచిత్రణ_మూల్యం=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు,영역너비,영역높이,విధానం_మోడ్_3f5e5497=struct.unpack('!HHHHi',정확히(కనెక్టుచేయి,12));assert విధానం_మోడ్_3f5e5497==0 and x_నిర్దేశాంకం+영역너비<=너비 and Y_బటన్_సమన్వయపరుచు+영역높이<=높이
                        పెల్=정확히(కనెక్టుచేయి,영역너비*영역높이*4);합계+=len(పెల్)
                        for పంక్తి in range(영역높이):రేఖాచిత్రణ_మూల్యం[((Y_బటన్_సమన్వయపరుచు+పంక్తి)*너비+x_నిర్దేశాంకం)*4:((Y_బటన్_సమన్వయపరుచు+పంక్తి)*너비+x_నిర్దేశాంకం+영역너비)*4]=పెల్[పంక్తి*영역너비*4:(పంక్తి+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(రేఖాచిత్రణ_మూల్యం),'raw','BGRX').save(str(అవుట్పుట్/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                నివేదిక_మూల్యం['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                నివేదిక_మూల్యం['checks'].append('RFB incremental update')
                처음=len(లాగ్_వరుస)
                for అక్షరం_మూల్యం in 'echo VNC_NATIVE_PASS\r':
                    చిహ్నం=0xff0d if అక్షరం_మూల్యం=='\r' else ord(అక్షరం_మూల్యం)
                    కనెక్టుచేయి.sendall(struct.pack('!BBHI',4,1,0,చిహ్నం));కనెక్టుచేయి.sendall(struct.pack('!BBHI',4,0,0,చిహ్నం))
                వేచియుండు_స్థితి(b'VNC_NATIVE_PASS',처음)
                నివేదిక_మూల్యం['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(చిహ్నం,누름=1):కనెక్టుచేయి.sendall(struct.pack('!BBHI',4,누름,0,చిహ్నం))
                처음=len(లాగ్_వరుస)
                for అక్షరం_మూల్యం in 'echo ':글쇠(ord(అక్షరం_మూల్యం))
                글쇠(0xffc6)
                for అక్షరం_మూల్యం in 'gksrmf':글쇠(ord(అక్షరం_మూల్యం))
                글쇠(0xffc6);글쇠(0xff0d)
                వేచియుండు_స్థితి('\r\n한글\r\n'.encode(),처음)
                నివేదిక_మూల్యం['checks'].append('Native VNC F9 two-set Hangul composition')
                కనెక్టుచేయి.sendall(struct.pack('!BBHH',5,0,120,100))
                నివేదిక_మూల్యం['checks'].append('VNC pointer input accepted')
            విధానం_మూల్యం.stdin.write(b'poweroff\n');విధానం_మూల్యం.stdin.flush();విధానం_మూల్యం.wait(timeout=15);assert విధానం_మూల్యం.returncode==0
            నివేదిక_మూల్యం['passed']=True
    finally:
        if విధానం_మూల్యం and విధానం_మూల్యం.poll() is None:
            విధానం_మూల్యం.terminate()
            try: విధానం_మూల్యం.wait(timeout=5)
            except subprocess.TimeoutExpired: విధానం_మూల్యం.kill();విధానం_మూల్యం.wait()
        (అవుట్పుట్/'serial.log').write_bytes(లాగ్_వరుస)
        (అవుట్పుట్/'report.json').write_text(json.dumps(నివేదిక_మూల్యం,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(నివేదిక_మూల్యం,ensure_ascii=False,indent=2))


if __name__=='__main__': నడుపుము()
