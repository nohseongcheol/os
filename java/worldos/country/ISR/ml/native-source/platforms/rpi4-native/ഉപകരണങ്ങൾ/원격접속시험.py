#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ
from നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ് import നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--kernel', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img')
    പാഴ്_സർ_48ee4b1b.add_argument('--access', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/remote/access.json')
    പാഴ്_സർ_48ee4b1b.add_argument('--output', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/native-remote')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    ഫലം = 인수.output
    ഫലം.mkdir(parents=True, exist_ok=True)
    സജ്ജീകരണം = json.loads(인수.access.read_text())
    నివేదిక_മൂല്യം = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ശൂന്യം_പോര്_ട്ട്():
        with socket.socket() as കണക്ടു്_ചെയ്യുക:
            കണക്ടു്_ചെയ്യുക.bind(('127.0.0.5', 0))
            return കണക്ടു്_ചെയ്യുക.getsockname()[1]
    ഷെല്_പോര്_ട്ട്, 화면포트, ഫയല്_പോര്_ട്ട് = ശൂന്യം_പോര്_ട്ട്(), ശൂന്യം_പോര്_ട്ട്(), ശൂന്യം_പോര്_ട്ട്()
    ലോഗ്_രേഖ = bytearray()
    പ്രോസസ്_മൂല്യം = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്(ഫയല്_പോര്_ട്ട്,
                ['tcp:{}:22'.format(ഷെല്_പോര്_ട്ട്), 'tcp:{}:5900'.format(화면포트)], ഹോസ്റ്റ്_ഇമെയിൽ='127.0.0.5') as ബ്രിഡ്_ജ്_മൂല്യം:
            실행인수 = ആജ്ഞ()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            പ്രോസസ്_മൂല്യം = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ബ്രിഡ്_ജ്_മൂല്യം.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ഡാറ്റാ = പ്രോസസ്_മൂല്യം.stdout.read(4096)
                    if not ഡാറ്റാ: break
                    ലോഗ്_രേഖ.extend(ഡാറ്റാ)
            ത്രെഡ്_മൂല്യം = threading.Thread(target=수집, daemon=True)
            ത്രെഡ്_മൂല്യം.start()
            def കാക്കുക_അവസ്ഥ(വാക്ക്_ലിഖിതം, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while വാക്ക്_ലിഖിതം not in ലോഗ്_രേഖ[처음:]:
                    if time.monotonic()>끝 or പ്രോസസ്_മൂല്യം.poll() is not None:
                        raise AssertionError('Missing '+repr(വാക്ക്_ലിഖിതം)+'\n'+ലോഗ്_രേഖ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            കാക്കുക_അവസ്ഥ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def സുരക്ഷിതം_ഷെല്(പാസ്_വേഡ്_മൂല്യം, നിര്_ദേശം_മൂല്യം, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=പാസ്_വേഡ്_മൂല്യം
                인수=['ssh','-v']+list(추가)+['-p',str(ഷെല്_പോര്_ട്ട്),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',നിര്_ദേശം_മൂല്യം]
                അളവ്=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return അളവ്
            അളവ്=സുരക്ഷിതം_ഷെല്('!' + സജ്ജീകരണം['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ഫലം/'ssh-rejected.log').write_bytes(അളവ്.stderr)
            assert അളവ്.returncode!=0 and b'Permission denied' in അളവ്.stderr and b'SHOULD_NOT_RUN' not in ലോഗ്_രേഖ, അളവ്.stderr
            నివేదిక_മൂല്യം['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            അളവ്=സുരക്ഷിതം_ഷെല്(സജ്ജീകരണം['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ഫലം/'ssh.log').write_bytes(അളവ്.stderr)
            (ഫലം/'ssh-output.txt').write_bytes(അളവ്.stdout)
            assert അളവ്.returncode==0 and b'SSH_NATIVE_PASS' in അളവ്.stdout, (അളവ്.returncode,അളവ്.stdout,അളവ്.stderr)
            నివేదిక_മൂല്യം['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in അളവ്.stderr, അളവ്.stderr
            నివేదిక_മൂല്യം['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            അളവ്=സുരക്ഷിതം_ഷെല്(സജ്ജീകരണം['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert അളവ്.returncode==0 and 'JAVA ഫലം: 안녕하세요 😀'.encode() in അളവ്.stdout,അളവ്.stdout
            నివేదిక_മൂല്യം['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            അളവ്=സുരക്ഷിതം_ഷെല്(സജ്ജീകരണം['ssh_password'], 'missing_remote_command')
            assert അളവ്.returncode==127,അളവ്.returncode
            నివేదిక_മൂല്യം['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            അളവ്=സുരക്ഷിതം_ഷെല്(സജ്ജീകരണം['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ഫലം/'ssh-rekey.log').write_bytes(അളവ്.stderr)
            assert അളവ്.returncode==0 and 'class 창예제'.encode() in അളവ്.stdout, (അളവ്.returncode,അളവ്.stdout,അളവ്.stderr)
            assert അളവ്.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, അളവ്.stderr
            నివేదిక_മൂല്യം['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ഷെല്_പോര്_ട്ട്),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ഇടപെടാനുതകുന്ന_സെഷൻ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();തിരഞ്ഞെടുക്കല്_മൂല്യം=selectors.DefaultSelector();തിരഞ്ഞെടുക്കല്_മൂല്യം.register(ഇടപെടാനുതകുന്ന_സെഷൻ.stdout,selectors.EVENT_READ)
            def 대화읽기(പ്രദർശനം_മൂല്യം):
                마감=time.monotonic()+30
                while പ്രദർശനം_മൂല്യം not in 대화기록:
                    if time.monotonic()>마감 or ഇടപെടാനുതകുന്ന_സെഷൻ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(പ്രദർശനം_മൂല്യം)+' '+repr(bytes(대화기록)))
                    for എന്_ട്രി_മൂല്യം,_ in തിരഞ്ഞെടുക്കല്_മൂല്യം.select(.1):
                        조각=എന്_ട്രി_മൂല്യം.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ഇടപെടാനുതകുന്ന_സെഷൻ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ഇടപെടാനുതകുന്ന_സെഷൻ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ഇടപെടാനുതകുന്ന_സെഷൻ.stdin.write(b'\x04');ഇടപെടാനുതകുന്ന_സെഷൻ.stdin.flush();나머지,പിശക്=ഇടപെടാനുതകുന്ന_സെഷൻ.communicate(timeout=15)
                assert ഇടപെടാനുതകുന്ന_സെഷൻ.returncode==0 and b'PTY allocation request failed' not in പിശക്,(ഇടപെടാനുതകുന്ന_സെഷൻ.returncode,പിശക്)
                (ഫലം/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                തിരഞ്ഞെടുക്കല്_മൂല്യം.close()
                if ഇടപെടാനുതകുന്ന_സെഷൻ.poll() is None:ഇടപെടാനുതകുന്ന_സെഷൻ.kill();ഇടപെടാനുതകുന്ന_സെഷൻ.wait()
            నివేదిక_മൂല്യം['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(കണക്ടു്_ചെയ്യുക, 수):
                ഡാറ്റാ=bytearray()
                while len(ഡാറ്റാ)<수:
                    덩이=കണക്ടു്_ചെയ്യുക.recv(수-len(ഡാറ്റാ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ഡാറ്റാ.extend(덩이)
                return bytes(ഡാറ്റാ)
            def 화면인증(പാസ്_വേഡ്_മൂല്യം):
                കണക്ടു്_ചെയ്യുക=socket.create_connection(('127.0.0.5',화면포트),10);കണക്ടു്_ചെയ്യുക.settimeout(30)
                assert 정확히(കണക്ടു്_ചെയ്യുക,12)==b'RFB 003.008\n'
                കണക്ടു്_ചെയ്യുക.sendall(b'RFB 003.008\n');assert 정확히(കണക്ടു്_ചെയ്യുക,2)==b'\x01\x02'
                കണക്ടു്_ചെയ്യുക.sendall(b'\x02');കടമ്പ_മൂല്യം=정확히(കണക്ടു്_ചെയ്യുക,16)
                입력암호=പാസ്_വേഡ്_മൂല്യം.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                കണക്ടു്_ചെയ്യുക.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(കടമ്പ_മൂല്യം))
                അവസ്ഥ_മൂല്യം=struct.unpack('!I',정확히(കണക്ടു്_ചെയ്യുക,4))[0]
                return കണക്ടു്_ചെയ്യുക,അവസ്ഥ_മൂല്യം
            അസാധുവായ_പാസ്_വേഡ്='!' if not സജ്ജീകരണം['vnc_password'].startswith('!') else '?'
            കണക്ടു്_ചെയ്യുക,അവസ്ഥ_മൂല്യം=화면인증(അസാധുവായ_പാസ്_വേഡ്);assert അവസ്ഥ_മൂല്യം==1;കണക്ടു്_ചെയ്യുക.close();time.sleep(.6)
            నివేదిక_മൂല്യം['checks'].append('VNC incorrect password rejected')
            കണക്ടു്_ചെയ്യുക,അവസ്ഥ_മൂല്യം=화면인증(സജ്ജീകരണം['vnc_password']);assert അവസ്ഥ_മൂല്യം==0
            with കണക്ടു്_ചെയ്യുക:
                കണക്ടു്_ചെയ്യുക.sendall(b'\x01');초기=정확히(കണക്ടു്_ചെയ്യുക,24);너비,높이=struct.unpack('!HH',초기[:4]);പേരു്=정확히(കണക്ടു്_ചെയ്യുക,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==പേരു്
                def 화면(증분=0):
                    കണക്ടു്_ചെയ്യുക.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(കണക്ടു്_ചെയ്യുക,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ഡ്രോയിംഗ്_മൂല്യം=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം,영역너비,영역높이,విధానం_മോഡ്=struct.unpack('!HHHHi',정확히(കണക്ടു്_ചെയ്യുക,12));assert విధానం_മോഡ്==0 and x_ഏകോപനം+영역너비<=너비 and Y_ബട്ടൺ_ഏകോപനം+영역높이<=높이
                        പെല്=정확히(കണക്ടു്_ചെയ്യുക,영역너비*영역높이*4);합계+=len(പെല്)
                        for ലൈൻ in range(영역높이):ഡ്രോയിംഗ്_മൂല്യം[((Y_ബട്ടൺ_ഏകോപനം+ലൈൻ)*너비+x_ഏകോപനം)*4:((Y_ബട്ടൺ_ഏകോപനം+ലൈൻ)*너비+x_ഏകോപനം+영역너비)*4]=പെല്[ലൈൻ*영역너비*4:(ലൈൻ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ഡ്രോയിംഗ്_മൂല്യം),'raw','BGRX').save(str(ഫലം/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                నివేదిక_മൂല്യം['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                నివేదిక_മൂല്യം['checks'].append('RFB incremental update')
                처음=len(ലോഗ്_രേഖ)
                for പ്രതീകം_മൂല്യം in 'echo VNC_NATIVE_PASS\r':
                    nbsp_ചിഹ്നം=0xff0d if പ്രതീകം_മൂല്യം=='\r' else ord(പ്രതീകം_മൂല്യം)
                    കണക്ടു്_ചെയ്യുക.sendall(struct.pack('!BBHI',4,1,0,nbsp_ചിഹ്നം));കണക്ടു്_ചെയ്യുക.sendall(struct.pack('!BBHI',4,0,0,nbsp_ചിഹ്നം))
                കാക്കുക_അവസ്ഥ(b'VNC_NATIVE_PASS',처음)
                నివేదిక_മൂല്യം['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(nbsp_ചിഹ്നം,누름=1):കണക്ടു്_ചെയ്യുക.sendall(struct.pack('!BBHI',4,누름,0,nbsp_ചിഹ്നം))
                처음=len(ലോഗ്_രേഖ)
                for പ്രതീകം_മൂല്യം in 'echo ':글쇠(ord(പ്രതീകം_മൂല്യം))
                글쇠(0xffc6)
                for പ്രതീകം_മൂല്യം in 'gksrmf':글쇠(ord(പ്രതീകം_മൂല്യം))
                글쇠(0xffc6);글쇠(0xff0d)
                കാക്കുക_അവസ്ഥ('\r\n한글\r\n'.encode(),처음)
                నివేదిక_മൂല്യം['checks'].append('Native VNC F9 two-set Hangul composition')
                കണക്ടു്_ചെയ്യുക.sendall(struct.pack('!BBHH',5,0,120,100))
                నివేదిక_മൂല്യം['checks'].append('VNC pointer input accepted')
            പ്രോസസ്_മൂല്യം.stdin.write(b'poweroff\n');പ്രോസസ്_മൂല്യം.stdin.flush();പ്രോസസ്_മൂല്യം.wait(timeout=15);assert പ്രോസസ്_മൂല്യം.returncode==0
            నివేదిక_മൂല്യം['passed']=True
    finally:
        if പ്രോസസ്_മൂല്യം and പ്രോസസ്_മൂല്യം.poll() is None:
            പ്രോസസ്_മൂല്യം.terminate()
            try: പ്രോസസ്_മൂല്യം.wait(timeout=5)
            except subprocess.TimeoutExpired: പ്രോസസ്_മൂല്യം.kill();പ്രോസസ്_മൂല്യം.wait()
        (ഫലം/'serial.log').write_bytes(ലോഗ്_രേഖ)
        (ഫലം/'report.json').write_text(json.dumps(నివేదిక_മൂല്യം,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(నివేదిక_മൂല്യം,ensure_ascii=False,indent=2))


if __name__=='__main__': നടപ്പിലാക്കുക()
