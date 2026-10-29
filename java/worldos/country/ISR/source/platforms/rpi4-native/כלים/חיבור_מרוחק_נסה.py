#!/usr/bin/env python3
"""בפועל_נתונים OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from לבצע_פקודה import לשקף_בסיס, פקודה
from גשר_3de4fe3a import גשר_3de4fe3a


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--kernel', type=Path, default=לשקף_בסיס / 'build/kernel8.img')
    מנתח_48ee4b1b.add_argument('--access', type=Path, default=לשקף_בסיס / 'build/remote/access.json')
    מנתח_48ee4b1b.add_argument('--output', type=Path, default=לשקף_בסיס / 'build/verification/native-remote')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    פלטטקסט = ארגומנטים.output
    פלטטקסט.mkdir(parents=True, exist_ok=True)
    הגדרות = json.loads(ארגומנטים.access.read_text())
    דוח_ערך_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(ארגומנטים.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ריק_הסב():
        with socket.socket() as חיבור:
            חיבור.bind(('127.0.0.5', 0))
            return חיבור.getsockname()[1]
    מעטפת_הסב, 화면포트, יציאת_קובץ = ריק_הסב(), ריק_הסב(), ריק_הסב()
    לרשום_שיא = bytearray()
    תהליך_ערך = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, גשר_3de4fe3a(יציאת_קובץ,
                ['tcp:{}:22'.format(מעטפת_הסב), 'tcp:{}:5900'.format(화면포트)], ארח_למען='127.0.0.5') as גשר_ערך:
            실행인수 = פקודה()
            실행인수[실행인수.index('-kernel') + 1] = str(ארגומנטים.kernel.resolve())
            תהליך_ערך = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + גשר_ערך.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    נתונים = תהליך_ערך.stdout.read(4096)
                    if not נתונים: break
                    לרשום_שיא.extend(נתונים)
            שרשור_ערך = threading.Thread(target=수집, daemon=True)
            שרשור_ערך.start()
            def מצב_המתנה(מילים_טקסט, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while מילים_טקסט not in לרשום_שיא[처음:]:
                    if time.monotonic()>끝 or תהליך_ערך.poll() is not None:
                        raise AssertionError('Missing '+repr(מילים_טקסט)+'\n'+לרשום_שיא[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            מצב_המתנה(b'jkoros-native> ')
            עוזר_ערך = Path(임시)/'askpass'
            עוזר_ערך.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            עוזר_ערך.chmod(0o700)
            סביבה = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(עוזר_ערך), SSH_ASKPASS_REQUIRE='force')
            def מאובטח_מעטפת(סיסמה_ערך, הוראה_ערך, צירוף_ערך_b73accca=()):
                סביבה['JKOROS_TEST_PASSWORD']=סיסמה_ערך
                ארגומנטים=['ssh','-v']+list(צירוף_ערך_b73accca)+['-p',str(מעטפת_הסב),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',הוראה_ערך]
                תוצאה=subprocess.run(ארגומנטים,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=סביבה,start_new_session=True,timeout=50)
                return תוצאה
            תוצאה=מאובטח_מעטפת('!' + הגדרות['ssh_password'], 'echo SHOULD_NOT_RUN')
            (פלטטקסט/'ssh-rejected.log').write_bytes(תוצאה.stderr)
            assert תוצאה.returncode!=0 and b'Permission denied' in תוצאה.stderr and b'SHOULD_NOT_RUN' not in לרשום_שיא, תוצאה.stderr
            דוח_ערך_ddf2aaf3['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            תוצאה=מאובטח_מעטפת(הגדרות['ssh_password'], 'echo SSH_NATIVE_PASS')
            (פלטטקסט/'ssh.log').write_bytes(תוצאה.stderr)
            (פלטטקסט/'ssh-output.txt').write_bytes(תוצאה.stdout)
            assert תוצאה.returncode==0 and b'SSH_NATIVE_PASS' in תוצאה.stdout, (תוצאה.returncode,תוצאה.stdout,תוצאה.stderr)
            דוח_ערך_ddf2aaf3['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in תוצאה.stderr, תוצאה.stderr
            דוח_ערך_ddf2aaf3['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            תוצאה=מאובטח_מעטפת(הגדרות['ssh_password'], 'cd /example/java; java דוגמתפלט; cd /')
            assert תוצאה.returncode==0 and 'JAVA פלטטקסט: 안녕하세요 😀'.encode() in תוצאה.stdout,תוצאה.stdout
            דוח_ערך_ddf2aaf3['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            תוצאה=מאובטח_מעטפת(הגדרות['ssh_password'], 'missing_remote_command')
            assert תוצאה.returncode==127,תוצאה.returncode
            דוח_ערך_ddf2aaf3['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            תוצאה=מאובטח_מעטפת(הגדרות['ssh_password'], 'cat /example/java/דוגמתחלון.java', ('-o', 'RekeyLimit=1K'))
            (פלטטקסט/'ssh-rekey.log').write_bytes(תוצאה.stderr)
            assert תוצאה.returncode==0 and 'class דוגמתחלון'.encode() in תוצאה.stdout, (תוצאה.returncode,תוצאה.stdout,תוצאה.stderr)
            assert תוצאה.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, תוצאה.stderr
            דוח_ערך_ddf2aaf3['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(מעטפת_הסב),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            אינטראקטיבי_הפעלה=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=סביבה,start_new_session=True,bufsize=0)
            תמליל=bytearray();קטע_נבחר_ערך=selectors.DefaultSelector();קטע_נבחר_ערך.register(אינטראקטיבי_הפעלה.stdout,selectors.EVENT_READ)
            def 대화읽기(הופעה_ערך):
                תאריך_יעד_ערך=time.monotonic()+30
                while הופעה_ערך not in תמליל:
                    if time.monotonic()>תאריך_יעד_ערך or אינטראקטיבי_הפעלה.poll() is not None:raise AssertionError('SSH interactive missing '+repr(הופעה_ערך)+' '+repr(bytes(תמליל)))
                    for ערך_ערך,_ in קטע_נבחר_ערך.select(.1):
                        조각=ערך_ערך.fileobj.read(4096)
                        if 조각:תמליל.extend(조각)
            try:
                대화읽기(b'shared native console')
                אינטראקטיבי_הפעלה.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');אינטראקטיבי_הפעלה.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                אינטראקטיבי_הפעלה.stdin.write(b'\x04');אינטראקטיבי_הפעלה.stdin.flush();나머지,שגיאה=אינטראקטיבי_הפעלה.communicate(timeout=15)
                assert אינטראקטיבי_הפעלה.returncode==0 and b'PTY allocation request failed' not in שגיאה,(אינטראקטיבי_הפעלה.returncode,שגיאה)
                (פלטטקסט/'ssh-interactive.txt').write_bytes(תמליל+나머지)
            finally:
                קטע_נבחר_ערך.close()
                if אינטראקטיבי_הפעלה.poll() is None:אינטראקטיבי_הפעלה.kill();אינטראקטיבי_הפעלה.wait()
            דוח_ערך_ddf2aaf3['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(חיבור, 수):
                נתונים=bytearray()
                while len(נתונים)<수:
                    덩이=חיבור.recv(수-len(נתונים))
                    if not 덩이: raise AssertionError('RFB EOF')
                    נתונים.extend(덩이)
                return bytes(נתונים)
            def 화면인증(סיסמה_ערך):
                חיבור=socket.create_connection(('127.0.0.5',화면포트),10);חיבור.settimeout(30)
                assert 정확히(חיבור,12)==b'RFB 003.008\n'
                חיבור.sendall(b'RFB 003.008\n');assert 정확히(חיבור,2)==b'\x01\x02'
                חיבור.sendall(b'\x02');אתגר_ערך=정확히(חיבור,16)
                קלט_סיסמה=סיסמה_ערך.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in קלט_סיסמה)
                חיבור.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(אתגר_ערך))
                מצב_ערך=struct.unpack('!I',정확히(חיבור,4))[0]
                return חיבור,מצב_ערך
            לא_חוקי_סיסמה='!' if not הגדרות['vnc_password'].startswith('!') else '?'
            חיבור,מצב_ערך=화면인증(לא_חוקי_סיסמה);assert מצב_ערך==1;חיבור.close();time.sleep(.6)
            דוח_ערך_ddf2aaf3['checks'].append('VNC incorrect password rejected')
            חיבור,מצב_ערך=화면인증(הגדרות['vnc_password']);assert מצב_ערך==0
            with חיבור:
                חיבור.sendall(b'\x01');מצב_התחלתי=정확히(חיבור,24);너비,גובה_ערך=struct.unpack('!HH',מצב_התחלתי[:4]);שם=정확히(חיבור,struct.unpack('!I',מצב_התחלתי[20:24])[0])
                assert (너비,גובה_ערך)==(640,480) and b'jkoros native'==שם
                def 화면(להגדיל_בהפרש_קבוע_צעד=0):
                    חיבור.sendall(struct.pack('!BBHHHH',3,להגדיל_בהפרש_קבוע_צעד,0,0,너비,גובה_ערך));ראש_ערך=정확히(חיבור,4);수=struct.unpack('!H',ראש_ערך[2:])[0];סך_הכל_ערך=0
                    ציור_ערך=bytearray(너비*גובה_ערך*4)
                    for _ in range(수):
                        קואורדינטת_x,세로좌표,영역너비,אזור_גובה,פעולת_שירות_מצב=struct.unpack('!HHHHi',정확히(חיבור,12));assert פעולת_שירות_מצב==0 and קואורדינטת_x+영역너비<=너비 and 세로좌표+אזור_גובה<=גובה_ערך
                        פיקסל=정확히(חיבור,영역너비*אזור_גובה*4);סך_הכל_ערך+=len(פיקסל)
                        for שורה in range(אזור_גובה):ציור_ערך[((세로좌표+שורה)*너비+קואורדינטת_x)*4:((세로좌표+שורה)*너비+קואורדינטת_x+영역너비)*4]=פיקסל[שורה*영역너비*4:(שורה+1)*영역너비*4]
                    if not להגדיל_בהפרש_קבוע_צעד:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,גובה_ערך),bytes(ציור_ערך),'raw','BGRX').save(str(פלטטקסט/'native-vnc.png'))
                    return 수,סך_הכל_ערך
                수,סך_הכל_ערך=화면();assert 수>0 and סך_הכל_ערך==너비*גובה_ערך*4
                דוח_ערך_ddf2aaf3['checks'].append('Native framebuffer RFB full update {} bytes'.format(סך_הכל_ערך))
                수,סך_הכל_ערך=화면(1);assert סך_הכל_ערך<너비*גובה_ערך*4
                דוח_ערך_ddf2aaf3['checks'].append('RFB incremental update')
                처음=len(לרשום_שיא)
                for תו_ערך in 'echo VNC_NATIVE_PASS\r':
                    סימן=0xff0d if תו_ערך=='\r' else ord(תו_ערך)
                    חיבור.sendall(struct.pack('!BBHI',4,1,0,סימן));חיבור.sendall(struct.pack('!BBHI',4,0,0,סימן))
                מצב_המתנה(b'VNC_NATIVE_PASS',처음)
                דוח_ערך_ddf2aaf3['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def מקש_משיכת_דיו(סימן,누름=1):חיבור.sendall(struct.pack('!BBHI',4,누름,0,סימן))
                처음=len(לרשום_שיא)
                for תו_ערך in 'echo ':מקש_משיכת_דיו(ord(תו_ערך))
                מקש_משיכת_דיו(0xffc6)
                for תו_ערך in 'gksrmf':מקש_משיכת_דיו(ord(תו_ערך))
                מקש_משיכת_דיו(0xffc6);מקש_משיכת_דיו(0xff0d)
                מצב_המתנה('\r\n한글\r\n'.encode(),처음)
                דוח_ערך_ddf2aaf3['checks'].append('Native VNC F9 two-set Hangul composition')
                חיבור.sendall(struct.pack('!BBHH',5,0,120,100))
                דוח_ערך_ddf2aaf3['checks'].append('VNC pointer input accepted')
            תהליך_ערך.stdin.write(b'poweroff\n');תהליך_ערך.stdin.flush();תהליך_ערך.wait(timeout=15);assert תהליך_ערך.returncode==0
            דוח_ערך_ddf2aaf3['passed']=True
    finally:
        if תהליך_ערך and תהליך_ערך.poll() is None:
            תהליך_ערך.terminate()
            try: תהליך_ערך.wait(timeout=5)
            except subprocess.TimeoutExpired: תהליך_ערך.kill();תהליך_ערך.wait()
        (פלטטקסט/'serial.log').write_bytes(לרשום_שיא)
        (פלטטקסט/'report.json').write_text(json.dumps(דוח_ערך_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(דוח_ערך_ddf2aaf3,ensure_ascii=False,indent=2))


if __name__=='__main__': הפעלה()
