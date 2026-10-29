#!/usr/bin/env python3
"""அசல்_தரவு OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை
from பிணையம்_பிரிட்ஜ் import பிணையம்_பிரிட்ஜ்


def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--kernel', type=Path, default=திட்டப்பணி_மூலம் / 'build/kernel8.img')
    பார்சர்_48ee4b1b.add_argument('--access', type=Path, default=திட்டப்பணி_மூலம் / 'build/remote/access.json')
    பார்சர்_48ee4b1b.add_argument('--output', type=Path, default=திட்டப்பணி_மூலம் / 'build/verification/native-remote')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    வெளியீட்டு_இடம் = செயலுருபுகள்.output
    வெளியீட்டு_இடம்.mkdir(parents=True, exist_ok=True)
    அமைப்புகள் = json.loads(செயலுருபுகள்.access.read_text())
    அறிக்கை_மதிப்பு = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(செயலுருபுகள்.kernel.read_bytes()).hexdigest(), 'checks': []}
    def வெறுமை_முணையம்():
        with socket.socket() as இணைக்க:
            இணைக்க.bind(('127.0.0.5', 0))
            return இணைக்க.getsockname()[1]
    கூடு_முணையம், 화면포트, கோப்பு_முணையம் = வெறுமை_முணையம்(), வெறுமை_முணையம்(), வெறுமை_முணையம்()
    பதிவு_பதிவு = bytearray()
    செயலகம்_மதிப்பு = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, பிணையம்_பிரிட்ஜ்(கோப்பு_முணையம்,
                ['tcp:{}:22'.format(கூடு_முணையம்), 'tcp:{}:5900'.format(화면포트)], ஓம்பு_முகவரி='127.0.0.5') as பிரிட்ஜ்_மதிப்பு:
            실행인수 = கட்டளை()
            실행인수[실행인수.index('-kernel') + 1] = str(செயலுருபுகள்.kernel.resolve())
            செயலகம்_மதிப்பு = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + பிரிட்ஜ்_மதிப்பு.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    தரவு = செயலகம்_மதிப்பு.stdout.read(4096)
                    if not தரவு: break
                    பதிவு_பதிவு.extend(தரவு)
            தொடரிழை_மதிப்பு = threading.Thread(target=수집, daemon=True)
            தொடரிழை_மதிப்பு.start()
            def காத்திரு_நிலை(சொல்_உரை, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while சொல்_உரை not in பதிவு_பதிவு[처음:]:
                    if time.monotonic()>끝 or செயலகம்_மதிப்பு.poll() is not None:
                        raise AssertionError('Missing '+repr(சொல்_உரை)+'\n'+பதிவு_பதிவு[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            காத்திரு_நிலை(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def பாதுகாப்பானது_கூடு(கடவுச்சொல்_மதிப்பு, ஆணை_மதிப்பு, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=கடவுச்சொல்_மதிப்பு
                செயலுருபுகள்=['ssh','-v']+list(추가)+['-p',str(கூடு_முணையம்),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ஆணை_மதிப்பு]
                அளவிடக்கூடியது=subprocess.run(செயலுருபுகள்,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return அளவிடக்கூடியது
            அளவிடக்கூடியது=பாதுகாப்பானது_கூடு('!' + அமைப்புகள்['ssh_password'], 'echo SHOULD_NOT_RUN')
            (வெளியீட்டு_இடம்/'ssh-rejected.log').write_bytes(அளவிடக்கூடியது.stderr)
            assert அளவிடக்கூடியது.returncode!=0 and b'Permission denied' in அளவிடக்கூடியது.stderr and b'SHOULD_NOT_RUN' not in பதிவு_பதிவு, அளவிடக்கூடியது.stderr
            அறிக்கை_மதிப்பு['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            அளவிடக்கூடியது=பாதுகாப்பானது_கூடு(அமைப்புகள்['ssh_password'], 'echo SSH_NATIVE_PASS')
            (வெளியீட்டு_இடம்/'ssh.log').write_bytes(அளவிடக்கூடியது.stderr)
            (வெளியீட்டு_இடம்/'ssh-output.txt').write_bytes(அளவிடக்கூடியது.stdout)
            assert அளவிடக்கூடியது.returncode==0 and b'SSH_NATIVE_PASS' in அளவிடக்கூடியது.stdout, (அளவிடக்கூடியது.returncode,அளவிடக்கூடியது.stdout,அளவிடக்கூடியது.stderr)
            அறிக்கை_மதிப்பு['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in அளவிடக்கூடியது.stderr, அளவிடக்கூடியது.stderr
            அறிக்கை_மதிப்பு['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            அளவிடக்கூடியது=பாதுகாப்பானது_கூடு(அமைப்புகள்['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert அளவிடக்கூடியது.returncode==0 and 'JAVA வெளியீட்டு_இடம்: 안녕하세요 😀'.encode() in அளவிடக்கூடியது.stdout,அளவிடக்கூடியது.stdout
            அறிக்கை_மதிப்பு['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            அளவிடக்கூடியது=பாதுகாப்பானது_கூடு(அமைப்புகள்['ssh_password'], 'missing_remote_command')
            assert அளவிடக்கூடியது.returncode==127,அளவிடக்கூடியது.returncode
            அறிக்கை_மதிப்பு['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            அளவிடக்கூடியது=பாதுகாப்பானது_கூடு(அமைப்புகள்['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (வெளியீட்டு_இடம்/'ssh-rekey.log').write_bytes(அளவிடக்கூடியது.stderr)
            assert அளவிடக்கூடியது.returncode==0 and 'class 창예제'.encode() in அளவிடக்கூடியது.stdout, (அளவிடக்கூடியது.returncode,அளவிடக்கூடியது.stdout,அளவிடக்கூடியது.stderr)
            assert அளவிடக்கூடியது.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, அளவிடக்கூடியது.stderr
            அறிக்கை_மதிப்பு['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(கூடு_முணையம்),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ஊடாடு_அமர்வு=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();தேர்வு_மதிப்பு=selectors.DefaultSelector();தேர்வு_மதிப்பு.register(ஊடாடு_அமர்வு.stdout,selectors.EVENT_READ)
            def 대화읽기(காட்சி_மதிப்பு_487749b8):
                마감=time.monotonic()+30
                while காட்சி_மதிப்பு_487749b8 not in 대화기록:
                    if time.monotonic()>마감 or ஊடாடு_அமர்வு.poll() is not None:raise AssertionError('SSH interactive missing '+repr(காட்சி_மதிப்பு_487749b8)+' '+repr(bytes(대화기록)))
                    for உள்ளீடு_மதிப்பு,_ in தேர்வு_மதிப்பு.select(.1):
                        조각=உள்ளீடு_மதிப்பு.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ஊடாடு_அமர்வு.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ஊடாடு_அமர்வு.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ஊடாடு_அமர்வு.stdin.write(b'\x04');ஊடாடு_அமர்வு.stdin.flush();나머지,பிழை=ஊடாடு_அமர்வு.communicate(timeout=15)
                assert ஊடாடு_அமர்வு.returncode==0 and b'PTY allocation request failed' not in பிழை,(ஊடாடு_அமர்வு.returncode,பிழை)
                (வெளியீட்டு_இடம்/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                தேர்வு_மதிப்பு.close()
                if ஊடாடு_அமர்வு.poll() is None:ஊடாடு_அமர்வு.kill();ஊடாடு_அமர்வு.wait()
            அறிக்கை_மதிப்பு['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(இணைக்க, 수):
                தரவு=bytearray()
                while len(தரவு)<수:
                    덩이=இணைக்க.recv(수-len(தரவு))
                    if not 덩이: raise AssertionError('RFB EOF')
                    தரவு.extend(덩이)
                return bytes(தரவு)
            def 화면인증(கடவுச்சொல்_மதிப்பு):
                இணைக்க=socket.create_connection(('127.0.0.5',화면포트),10);இணைக்க.settimeout(30)
                assert 정확히(இணைக்க,12)==b'RFB 003.008\n'
                இணைக்க.sendall(b'RFB 003.008\n');assert 정확히(இணைக்க,2)==b'\x01\x02'
                இணைக்க.sendall(b'\x02');சவால்_மதிப்பு=정확히(இணைக்க,16)
                입력암호=கடவுச்சொல்_மதிப்பு.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                இணைக்க.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(சவால்_மதிப்பு))
                நிலை_மதிப்பு_e10195a1=struct.unpack('!I',정확히(இணைக்க,4))[0]
                return இணைக்க,நிலை_மதிப்பு_e10195a1
            செல்லுபடியாகாத_கடவுச்சொல்='!' if not அமைப்புகள்['vnc_password'].startswith('!') else '?'
            இணைக்க,நிலை_மதிப்பு_e10195a1=화면인증(செல்லுபடியாகாத_கடவுச்சொல்);assert நிலை_மதிப்பு_e10195a1==1;இணைக்க.close();time.sleep(.6)
            அறிக்கை_மதிப்பு['checks'].append('VNC incorrect password rejected')
            இணைக்க,நிலை_மதிப்பு_e10195a1=화면인증(அமைப்புகள்['vnc_password']);assert நிலை_மதிப்பு_e10195a1==0
            with இணைக்க:
                இணைக்க.sendall(b'\x01');초기=정확히(இணைக்க,24);너비,높이=struct.unpack('!HH',초기[:4]);பெயர்=정확히(இணைக்க,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==பெயர்
                def 화면(증분=0):
                    இணைக்க.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(இணைக்க,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    வரைதல்_மதிப்பு=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு,영역너비,영역높이,முறை_பயன்முறை=struct.unpack('!HHHHi',정확히(இணைக்க,12));assert முறை_பயன்முறை==0 and x_ஒத்ததரமுள்ளது+영역너비<=너비 and Y_பொத்தான்_அச்சுத்_தொகுப்பு+영역높이<=높이
                        படக்_கூறு=정확히(இணைக்க,영역너비*영역높이*4);합계+=len(படக்_கூறு)
                        for உள்ளீட்டு_வரி in range(영역높이):வரைதல்_மதிப்பு[((Y_பொத்தான்_அச்சுத்_தொகுப்பு+உள்ளீட்டு_வரி)*너비+x_ஒத்ததரமுள்ளது)*4:((Y_பொத்தான்_அச்சுத்_தொகுப்பு+உள்ளீட்டு_வரி)*너비+x_ஒத்ததரமுள்ளது+영역너비)*4]=படக்_கூறு[உள்ளீட்டு_வரி*영역너비*4:(உள்ளீட்டு_வரி+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(வரைதல்_மதிப்பு),'raw','BGRX').save(str(வெளியீட்டு_இடம்/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                அறிக்கை_மதிப்பு['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                அறிக்கை_மதிப்பு['checks'].append('RFB incremental update')
                처음=len(பதிவு_பதிவு)
                for எழுத்துக்குறி_மதிப்பு in 'echo VNC_NATIVE_PASS\r':
                    சின்னம்=0xff0d if எழுத்துக்குறி_மதிப்பு=='\r' else ord(எழுத்துக்குறி_மதிப்பு)
                    இணைக்க.sendall(struct.pack('!BBHI',4,1,0,சின்னம்));இணைக்க.sendall(struct.pack('!BBHI',4,0,0,சின்னம்))
                காத்திரு_நிலை(b'VNC_NATIVE_PASS',처음)
                அறிக்கை_மதிப்பு['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(சின்னம்,누름=1):இணைக்க.sendall(struct.pack('!BBHI',4,누름,0,சின்னம்))
                처음=len(பதிவு_பதிவு)
                for எழுத்துக்குறி_மதிப்பு in 'echo ':글쇠(ord(எழுத்துக்குறி_மதிப்பு))
                글쇠(0xffc6)
                for எழுத்துக்குறி_மதிப்பு in 'gksrmf':글쇠(ord(எழுத்துக்குறி_மதிப்பு))
                글쇠(0xffc6);글쇠(0xff0d)
                காத்திரு_நிலை('\r\n한글\r\n'.encode(),처음)
                அறிக்கை_மதிப்பு['checks'].append('Native VNC F9 two-set Hangul composition')
                இணைக்க.sendall(struct.pack('!BBHH',5,0,120,100))
                அறிக்கை_மதிப்பு['checks'].append('VNC pointer input accepted')
            செயலகம்_மதிப்பு.stdin.write(b'poweroff\n');செயலகம்_மதிப்பு.stdin.flush();செயலகம்_மதிப்பு.wait(timeout=15);assert செயலகம்_மதிப்பு.returncode==0
            அறிக்கை_மதிப்பு['passed']=True
    finally:
        if செயலகம்_மதிப்பு and செயலகம்_மதிப்பு.poll() is None:
            செயலகம்_மதிப்பு.terminate()
            try: செயலகம்_மதிப்பு.wait(timeout=5)
            except subprocess.TimeoutExpired: செயலகம்_மதிப்பு.kill();செயலகம்_மதிப்பு.wait()
        (வெளியீட்டு_இடம்/'serial.log').write_bytes(பதிவு_பதிவு)
        (வெளியீட்டு_இடம்/'report.json').write_text(json.dumps(அறிக்கை_மதிப்பு,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(அறிக்கை_மதிப்பு,ensure_ascii=False,indent=2))


if __name__=='__main__': செயல்படுத்துக()
