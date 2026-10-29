#!/usr/bin/env python3
"""tūturu_raraunga OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from kawe_tono import whakaatu_pūtake, tono
from whatunga_arawhata import whatunga_arawhata


def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=whakaatu_pūtake / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=whakaatu_pūtake / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=whakaatu_pūtake / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Ngā_Tautuhinga = json.loads(인수.access.read_text())
    pūrongo_uara = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def putua_kawe():
        with socket.socket() as TŪHONO:
            TŪHONO.bind(('127.0.0.5', 0))
            return TŪHONO.getsockname()[1]
    anga_kawe, 화면포트, kōnae_kawe = putua_kawe(), putua_kawe(), putua_kawe()
    LOG_RECORD = bytearray()
    Hātepe_uara = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, whatunga_arawhata(kōnae_kawe,
                ['tcp:{}:22'.format(anga_kawe), 'tcp:{}:5900'.format(화면포트)], taurima_ADDRESS='127.0.0.5') as arawhata_uara:
            실행인수 = tono()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Hātepe_uara = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + arawhata_uara.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    raraunga = Hātepe_uara.stdout.read(4096)
                    if not raraunga: break
                    LOG_RECORD.extend(raraunga)
            miro_uara = threading.Thread(target=수집, daemon=True)
            miro_uara.start()
            def 기다림(Word_TEXT, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_TEXT not in LOG_RECORD[처음:]:
                    if time.monotonic()>끝 or Hātepe_uara.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_TEXT)+'\n'+LOG_RECORD[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def haumaru_anga(kupuhipa_uara, tohutohu_uara, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=kupuhipa_uara
                인수=['ssh','-v']+list(추가)+['-p',str(anga_kawe),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',tohutohu_uara]
                mēhua=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return mēhua
            mēhua=haumaru_anga('!' + Ngā_Tautuhinga['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(mēhua.stderr)
            assert mēhua.returncode!=0 and b'Permission denied' in mēhua.stderr and b'SHOULD_NOT_RUN' not in LOG_RECORD, mēhua.stderr
            pūrongo_uara['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            mēhua=haumaru_anga(Ngā_Tautuhinga['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(mēhua.stderr)
            (출력/'ssh-output.txt').write_bytes(mēhua.stdout)
            assert mēhua.returncode==0 and b'SSH_NATIVE_PASS' in mēhua.stdout, (mēhua.returncode,mēhua.stdout,mēhua.stderr)
            pūrongo_uara['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in mēhua.stderr, mēhua.stderr
            pūrongo_uara['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            mēhua=haumaru_anga(Ngā_Tautuhinga['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert mēhua.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in mēhua.stdout,mēhua.stdout
            pūrongo_uara['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            mēhua=haumaru_anga(Ngā_Tautuhinga['ssh_password'], 'missing_remote_command')
            assert mēhua.returncode==127,mēhua.returncode
            pūrongo_uara['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            mēhua=haumaru_anga(Ngā_Tautuhinga['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(mēhua.stderr)
            assert mēhua.returncode==0 and 'class 창예제'.encode() in mēhua.stdout, (mēhua.returncode,mēhua.stdout,mēhua.stderr)
            assert mēhua.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, mēhua.stderr
            pūrongo_uara['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(anga_kawe),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            pāhekoheko_wātū=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();tīpakonga_uara=selectors.DefaultSelector();tīpakonga_uara.register(pāhekoheko_wātū.stdout,selectors.EVENT_READ)
            def 대화읽기(whakaatu_uara):
                마감=time.monotonic()+30
                while whakaatu_uara not in 대화기록:
                    if time.monotonic()>마감 or pāhekoheko_wātū.poll() is not None:raise AssertionError('SSH interactive missing '+repr(whakaatu_uara)+' '+repr(bytes(대화기록)))
                    for tāurunga_uara,_ in tīpakonga_uara.select(.1):
                        조각=tāurunga_uara.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                pāhekoheko_wātū.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');pāhekoheko_wātū.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                pāhekoheko_wātū.stdin.write(b'\x04');pāhekoheko_wātū.stdin.flush();나머지,Pōhēhē=pāhekoheko_wātū.communicate(timeout=15)
                assert pāhekoheko_wātū.returncode==0 and b'PTY allocation request failed' not in Pōhēhē,(pāhekoheko_wātū.returncode,Pōhēhē)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                tīpakonga_uara.close()
                if pāhekoheko_wātū.poll() is None:pāhekoheko_wātū.kill();pāhekoheko_wātū.wait()
            pūrongo_uara['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(TŪHONO, 수):
                raraunga=bytearray()
                while len(raraunga)<수:
                    덩이=TŪHONO.recv(수-len(raraunga))
                    if not 덩이: raise AssertionError('RFB EOF')
                    raraunga.extend(덩이)
                return bytes(raraunga)
            def 화면인증(kupuhipa_uara):
                TŪHONO=socket.create_connection(('127.0.0.5',화면포트),10);TŪHONO.settimeout(30)
                assert 정확히(TŪHONO,12)==b'RFB 003.008\n'
                TŪHONO.sendall(b'RFB 003.008\n');assert 정확히(TŪHONO,2)==b'\x01\x02'
                TŪHONO.sendall(b'\x02');wero_uara=정확히(TŪHONO,16)
                입력암호=kupuhipa_uara.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                TŪHONO.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(wero_uara))
                tūnga_uara=struct.unpack('!I',정확히(TŪHONO,4))[0]
                return TŪHONO,tūnga_uara
            muhu_kupuhipa='!' if not Ngā_Tautuhinga['vnc_password'].startswith('!') else '?'
            TŪHONO,tūnga_uara=화면인증(muhu_kupuhipa);assert tūnga_uara==1;TŪHONO.close();time.sleep(.6)
            pūrongo_uara['checks'].append('VNC incorrect password rejected')
            TŪHONO,tūnga_uara=화면인증(Ngā_Tautuhinga['vnc_password']);assert tūnga_uara==0
            with TŪHONO:
                TŪHONO.sendall(b'\x01');초기=정확히(TŪHONO,24);너비,높이=struct.unpack('!HH',초기[:4]);Ingoa=정확히(TŪHONO,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Ingoa
                def 화면(증분=0):
                    TŪHONO.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(TŪHONO,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    tātuhi_uara=bytearray(너비*높이*4)
                    for _ in range(수):
                        taunga_x,세로좌표,영역너비,영역높이,aratuka_MODE=struct.unpack('!HHHHi',정확히(TŪHONO,12));assert aratuka_MODE==0 and taunga_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pika=정확히(TŪHONO,영역너비*영역높이*4);합계+=len(pika)
                        for hononga in range(영역높이):tātuhi_uara[((세로좌표+hononga)*너비+taunga_x)*4:((세로좌표+hononga)*너비+taunga_x+영역너비)*4]=pika[hononga*영역너비*4:(hononga+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(tātuhi_uara),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                pūrongo_uara['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                pūrongo_uara['checks'].append('RFB incremental update')
                처음=len(LOG_RECORD)
                for pūāhua_uara in 'echo VNC_NATIVE_PASS\r':
                    tohu=0xff0d if pūāhua_uara=='\r' else ord(pūāhua_uara)
                    TŪHONO.sendall(struct.pack('!BBHI',4,1,0,tohu));TŪHONO.sendall(struct.pack('!BBHI',4,0,0,tohu))
                기다림(b'VNC_NATIVE_PASS',처음)
                pūrongo_uara['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(tohu,누름=1):TŪHONO.sendall(struct.pack('!BBHI',4,누름,0,tohu))
                처음=len(LOG_RECORD)
                for pūāhua_uara in 'echo ':글쇠(ord(pūāhua_uara))
                글쇠(0xffc6)
                for pūāhua_uara in 'gksrmf':글쇠(ord(pūāhua_uara))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                pūrongo_uara['checks'].append('Native VNC F9 two-set Hangul composition')
                TŪHONO.sendall(struct.pack('!BBHH',5,0,120,100))
                pūrongo_uara['checks'].append('VNC pointer input accepted')
            Hātepe_uara.stdin.write(b'poweroff\n');Hātepe_uara.stdin.flush();Hātepe_uara.wait(timeout=15);assert Hātepe_uara.returncode==0
            pūrongo_uara['passed']=True
    finally:
        if Hātepe_uara and Hātepe_uara.poll() is None:
            Hātepe_uara.terminate()
            try: Hātepe_uara.wait(timeout=5)
            except subprocess.TimeoutExpired: Hātepe_uara.kill();Hātepe_uara.wait()
        (출력/'serial.log').write_bytes(LOG_RECORD)
        (출력/'report.json').write_text(json.dumps(pūrongo_uara,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pūrongo_uara,ensure_ascii=False,indent=2))


if __name__=='__main__': whakahaere()
