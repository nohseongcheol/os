#!/usr/bin/env python3
"""वास्तविक_डेटा OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश
from संचारजाळे_ब्रिज import संचारजाळे_ब्रिज


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--kernel', type=Path, default=प्रोजेक्ट_मूळ / 'build/kernel8.img')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--access', type=Path, default=प्रोजेक्ट_मूळ / 'build/remote/access.json')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--output', type=Path, default=प्रोजेक्ट_मूळ / 'build/verification/native-remote')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    आउटपुट = बाबी.output
    आउटपुट.mkdir(parents=True, exist_ok=True)
    संयोजना = json.loads(बाबी.access.read_text())
    अहवाल_मूल्य = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(बाबी.kernel.read_bytes()).hexdigest(), 'checks': []}
    def रिक्त_पॉर्ट():
        with socket.socket() as जोडा:
            जोडा.bind(('127.0.0.5', 0))
            return जोडा.getsockname()[1]
    शेल_पॉर्ट, पडदा_पॉर्ट, संचिका_पॉर्ट = रिक्त_पॉर्ट(), रिक्त_पॉर्ट(), रिक्त_पॉर्ट()
    लॉग_नोंद = bytearray()
    प्रक्रिया_मूल्य = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as तात्पुरते_मूल्य, संचारजाळे_ब्रिज(संचिका_पॉर्ट,
                ['tcp:{}:22'.format(शेल_पॉर्ट), 'tcp:{}:5900'.format(पडदा_पॉर्ट)], होस्ट_पत्ता='127.0.0.5') as ब्रिज_मूल्य:
            वितर्क = आदेश()
            वितर्क[वितर्क.index('-kernel') + 1] = str(बाबी.kernel.resolve())
            प्रक्रिया_मूल्य = subprocess.Popen(वितर्क + ['-display','none','-monitor','none','-serial','stdio'] + ब्रिज_मूल्य.अग्रेषित_वितर्क(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def गोळाकरा_मूल्ये():
                while True:
                    डेटा = प्रक्रिया_मूल्य.stdout.read(4096)
                    if not डेटा: break
                    लॉग_नोंद.extend(डेटा)
            कार्यसूत्र_मूल्य_5b72a632 = threading.Thread(target=गोळाकरा_मूल्ये, daemon=True)
            कार्यसूत्र_मूल्य_5b72a632.start()
            def प्रतीक्षा_करा_राज्य(शब्द_मजकूर, प्रारंभिक_आयटम=0, मर्यादा_मूल्य=60):
                शेवट = time.monotonic() + मर्यादा_मूल्य
                while शब्द_मजकूर not in लॉग_नोंद[प्रारंभिक_आयटम:]:
                    if time.monotonic()>शेवट or प्रक्रिया_मूल्य.poll() is not None:
                        raise AssertionError('Missing '+repr(शब्द_मजकूर)+'\n'+लॉग_नोंद[प्रारंभिक_आयटम:].decode('utf-8','replace'))
                    time.sleep(.02)
            प्रतीक्षा_करा_राज्य(b'jkoros-native> ')
            सहायक_मूल्य_44c0808f = Path(तात्पुरते_मूल्य)/'askpass'
            सहायक_मूल्य_44c0808f.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            सहायक_मूल्य_44c0808f.chmod(0o700)
            पर्यावरण = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(सहायक_मूल्य_44c0808f), SSH_ASKPASS_REQUIRE='force')
            def सुरक्षित_शेल(पासवर्ड_मूल्य, निर्देश_मूल्य, शेवटीजोडा_प्रविष्टी=()):
                पर्यावरण['JKOROS_TEST_PASSWORD']=पासवर्ड_मूल्य
                बाबी=['ssh','-v']+list(शेवटीजोडा_प्रविष्टी)+['-p',str(शेल_पॉर्ट),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(तात्पुरते_मूल्य)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',निर्देश_मूल्य]
                मोजमाप=subprocess.run(बाबी,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=पर्यावरण,start_new_session=True,timeout=50)
                return मोजमाप
            मोजमाप=सुरक्षित_शेल('!' + संयोजना['ssh_password'], 'echo SHOULD_NOT_RUN')
            (आउटपुट/'ssh-rejected.log').write_bytes(मोजमाप.stderr)
            assert मोजमाप.returncode!=0 and b'Permission denied' in मोजमाप.stderr and b'SHOULD_NOT_RUN' not in लॉग_नोंद, मोजमाप.stderr
            अहवाल_मूल्य['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            मोजमाप=सुरक्षित_शेल(संयोजना['ssh_password'], 'echo SSH_NATIVE_PASS')
            (आउटपुट/'ssh.log').write_bytes(मोजमाप.stderr)
            (आउटपुट/'ssh-output.txt').write_bytes(मोजमाप.stdout)
            assert मोजमाप.returncode==0 and b'SSH_NATIVE_PASS' in मोजमाप.stdout, (मोजमाप.returncode,मोजमाप.stdout,मोजमाप.stderr)
            अहवाल_मूल्य['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in मोजमाप.stderr, मोजमाप.stderr
            अहवाल_मूल्य['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            मोजमाप=सुरक्षित_शेल(संयोजना['ssh_password'], 'cd /example/java; java प्रदान_उदाहरण; cd /')
            assert मोजमाप.returncode==0 and 'JAVA आउटपुट: 안녕하세요 😀'.encode() in मोजमाप.stdout,मोजमाप.stdout
            अहवाल_मूल्य['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            मोजमाप=सुरक्षित_शेल(संयोजना['ssh_password'], 'missing_remote_command')
            assert मोजमाप.returncode==127,मोजमाप.returncode
            अहवाल_मूल्य['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            मोजमाप=सुरक्षित_शेल(संयोजना['ssh_password'], 'cat /example/java/खिडकीउदाहरण.java', ('-o', 'RekeyLimit=1K'))
            (आउटपुट/'ssh-rekey.log').write_bytes(मोजमाप.stderr)
            assert मोजमाप.returncode==0 and 'class खिडकीउदाहरण'.encode() in मोजमाप.stdout, (मोजमाप.returncode,मोजमाप.stdout,मोजमाप.stderr)
            assert मोजमाप.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, मोजमाप.stderr
            अहवाल_मूल्य['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            परस्परसंवादी_वितर्क=['ssh','-tt','-p',str(शेल_पॉर्ट),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(तात्पुरते_मूल्य)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            परस्परसंवादी_सत्र=subprocess.Popen(परस्परसंवादी_वितर्क,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=पर्यावरण,start_new_session=True,bufsize=0)
            सत्रलेख=bytearray();निवड_मूल्य=selectors.DefaultSelector();निवड_मूल्य.register(परस्परसंवादी_सत्र.stdout,selectors.EVENT_READ)
            def परस्परसंवादी_वाचा(मूल्य_शो):
                अंतिमवेळ_मूल्य=time.monotonic()+30
                while मूल्य_शो not in सत्रलेख:
                    if time.monotonic()>अंतिमवेळ_मूल्य or परस्परसंवादी_सत्र.poll() is not None:raise AssertionError('SSH interactive missing '+repr(मूल्य_शो)+' '+repr(bytes(सत्रलेख)))
                    for प्रविष्टी_मूल्य,_ in निवड_मूल्य.select(.1):
                        तुकडा_मूल्य=प्रविष्टी_मूल्य.fileobj.read(4096)
                        if तुकडा_मूल्य:सत्रलेख.extend(तुकडा_मूल्य)
            try:
                परस्परसंवादी_वाचा(b'shared native console')
                परस्परसंवादी_सत्र.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');परस्परसंवादी_सत्र.stdin.flush();परस्परसंवादी_वाचा(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                परस्परसंवादी_सत्र.stdin.write(b'\x04');परस्परसंवादी_सत्र.stdin.flush();बाकी_मूल्य,त्रुटी=परस्परसंवादी_सत्र.communicate(timeout=15)
                assert परस्परसंवादी_सत्र.returncode==0 and b'PTY allocation request failed' not in त्रुटी,(परस्परसंवादी_सत्र.returncode,त्रुटी)
                (आउटपुट/'ssh-interactive.txt').write_bytes(सत्रलेख+बाकी_मूल्य)
            finally:
                निवड_मूल्य.close()
                if परस्परसंवादी_सत्र.poll() is None:परस्परसंवादी_सत्र.kill();परस्परसंवादी_सत्र.wait()
            अहवाल_मूल्य['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def नेमके_मूल्य(जोडा, संख्या):
                डेटा=bytearray()
                while len(डेटा)<संख्या:
                    खंड_मूल्य=जोडा.recv(संख्या-len(डेटा))
                    if not खंड_मूल्य: raise AssertionError('RFB EOF')
                    डेटा.extend(खंड_मूल्य)
                return bytes(डेटा)
            def पडदा_प्रमाणीकरण(पासवर्ड_मूल्य):
                जोडा=socket.create_connection(('127.0.0.5',पडदा_पॉर्ट),10);जोडा.settimeout(30)
                assert नेमके_मूल्य(जोडा,12)==b'RFB 003.008\n'
                जोडा.sendall(b'RFB 003.008\n');assert नेमके_मूल्य(जोडा,2)==b'\x01\x02'
                जोडा.sendall(b'\x02');आव्हान_मूल्य=नेमके_मूल्य(जोडा,16)
                आदान_पासवर्ड=पासवर्ड_मूल्य.encode('ascii')[:8].ljust(8, b'\0')
                कळ_सामग्री=bytes(int('{:08b}'.format(संख्या)[::-1],2) for संख्या in आदान_पासवर्ड)
                जोडा.sendall(DES.new(कळ_सामग्री,DES.MODE_ECB).encrypt(आव्हान_मूल्य))
                राज्य_मूल्य=struct.unpack('!I',नेमके_मूल्य(जोडा,4))[0]
                return जोडा,राज्य_मूल्य
            अवैध_पासवर्ड='!' if not संयोजना['vnc_password'].startswith('!') else '?'
            जोडा,राज्य_मूल्य=पडदा_प्रमाणीकरण(अवैध_पासवर्ड);assert राज्य_मूल्य==1;जोडा.close();time.sleep(.6)
            अहवाल_मूल्य['checks'].append('VNC incorrect password rejected')
            जोडा,राज्य_मूल्य=पडदा_प्रमाणीकरण(संयोजना['vnc_password']);assert राज्य_मूल्य==0
            with जोडा:
                जोडा.sendall(b'\x01');प्रारंभिक_राज्य=नेमके_मूल्य(जोडा,24);रुंदी_मूल्य,उंची_मूल्य=struct.unpack('!HH',प्रारंभिक_राज्य[:4]);नाव=नेमके_मूल्य(जोडा,struct.unpack('!I',प्रारंभिक_राज्य[20:24])[0])
                assert (रुंदी_मूल्य,उंची_मूल्य)==(640,480) and b'jkoros native'==नाव
                def पडदा(वाढ_पायरी=0):
                    जोडा.sendall(struct.pack('!BBHHHH',3,वाढ_पायरी,0,0,रुंदी_मूल्य,उंची_मूल्य));शीर्ष_मूल्य=नेमके_मूल्य(जोडा,4);संख्या=struct.unpack('!H',शीर्ष_मूल्य[2:])[0];एकूण_मूल्य=0
                    रेखांकन_मूल्य=bytearray(रुंदी_मूल्य*उंची_मूल्य*4)
                    for _ in range(संख्या):
                        आडवे_समन्वयीत,उभे_समन्वयीत,प्रदेश_रुंदी,प्रदेश_उंची,पद्धत_मोड=struct.unpack('!HHHHi',नेमके_मूल्य(जोडा,12));assert पद्धत_मोड==0 and आडवे_समन्वयीत+प्रदेश_रुंदी<=रुंदी_मूल्य and उभे_समन्वयीत+प्रदेश_उंची<=उंची_मूल्य
                        पिक्सेल=नेमके_मूल्य(जोडा,प्रदेश_रुंदी*प्रदेश_उंची*4);एकूण_मूल्य+=len(पिक्सेल)
                        for ओळ in range(प्रदेश_उंची):रेखांकन_मूल्य[((उभे_समन्वयीत+ओळ)*रुंदी_मूल्य+आडवे_समन्वयीत)*4:((उभे_समन्वयीत+ओळ)*रुंदी_मूल्य+आडवे_समन्वयीत+प्रदेश_रुंदी)*4]=पिक्सेल[ओळ*प्रदेश_रुंदी*4:(ओळ+1)*प्रदेश_रुंदी*4]
                    if not वाढ_पायरी:
                        from PIL import Image
                        Image.frombytes('RGB',(रुंदी_मूल्य,उंची_मूल्य),bytes(रेखांकन_मूल्य),'raw','BGRX').save(str(आउटपुट/'native-vnc.png'))
                    return संख्या,एकूण_मूल्य
                संख्या,एकूण_मूल्य=पडदा();assert संख्या>0 and एकूण_मूल्य==रुंदी_मूल्य*उंची_मूल्य*4
                अहवाल_मूल्य['checks'].append('Native framebuffer RFB full update {} bytes'.format(एकूण_मूल्य))
                संख्या,एकूण_मूल्य=पडदा(1);assert एकूण_मूल्य<रुंदी_मूल्य*उंची_मूल्य*4
                अहवाल_मूल्य['checks'].append('RFB incremental update')
                प्रारंभिक_आयटम=len(लॉग_नोंद)
                for वर्ण_मूल्य in 'echo VNC_NATIVE_PASS\r':
                    चिन्ह=0xff0d if वर्ण_मूल्य=='\r' else ord(वर्ण_मूल्य)
                    जोडा.sendall(struct.pack('!BBHI',4,1,0,चिन्ह));जोडा.sendall(struct.pack('!BBHI',4,0,0,चिन्ह))
                प्रतीक्षा_करा_राज्य(b'VNC_NATIVE_PASS',प्रारंभिक_आयटम)
                अहवाल_मूल्य['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def कळ_रेघ(चिन्ह,दाबा_मूल्य=1):जोडा.sendall(struct.pack('!BBHI',4,दाबा_मूल्य,0,चिन्ह))
                प्रारंभिक_आयटम=len(लॉग_नोंद)
                for वर्ण_मूल्य in 'echo ':कळ_रेघ(ord(वर्ण_मूल्य))
                कळ_रेघ(0xffc6)
                for वर्ण_मूल्य in 'gksrmf':कळ_रेघ(ord(वर्ण_मूल्य))
                कळ_रेघ(0xffc6);कळ_रेघ(0xff0d)
                प्रतीक्षा_करा_राज्य('\r\n한글\r\n'.encode(),प्रारंभिक_आयटम)
                अहवाल_मूल्य['checks'].append('Native VNC F9 two-set Hangul composition')
                जोडा.sendall(struct.pack('!BBHH',5,0,120,100))
                अहवाल_मूल्य['checks'].append('VNC pointer input accepted')
            प्रक्रिया_मूल्य.stdin.write(b'poweroff\n');प्रक्रिया_मूल्य.stdin.flush();प्रक्रिया_मूल्य.wait(timeout=15);assert प्रक्रिया_मूल्य.returncode==0
            अहवाल_मूल्य['passed']=True
    finally:
        if प्रक्रिया_मूल्य and प्रक्रिया_मूल्य.poll() is None:
            प्रक्रिया_मूल्य.terminate()
            try: प्रक्रिया_मूल्य.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया_मूल्य.kill();प्रक्रिया_मूल्य.wait()
        (आउटपुट/'serial.log').write_bytes(लॉग_नोंद)
        (आउटपुट/'report.json').write_text(json.dumps(अहवाल_मूल्य,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(अहवाल_मूल्य,ensure_ascii=False,indent=2))


if __name__=='__main__': सुरू_करा()
