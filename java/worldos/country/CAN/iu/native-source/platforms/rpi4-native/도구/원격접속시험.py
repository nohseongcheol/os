#!/usr/bin/env python3
"""taannallarik_titiqqat OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from 실행 import 기준, piqujijjut
from 통신다리 import 통신다리


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    설정 = json.loads(인수.access.read_text())
    unikkaaq_atuutilik = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as kasurli:
            kasurli.bind(('127.0.0.5', 0))
            return kasurli.getsockname()[1]
    piqujijjutiliriji_kapputigaq, 화면포트, ini_kapputigaq = 빈포트(), 빈포트(), 빈포트()
    papattivik_sanimukutaak = bytearray()
    Pivallianiq_atuutilik = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(ini_kapputigaq,
                ['tcp:{}:22'.format(piqujijjutiliriji_kapputigaq), 'tcp:{}:5900'.format(화면포트)], tuttarvik_turaarut='127.0.0.5') as 다리:
            실행인수 = piqujijjut()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Pivallianiq_atuutilik = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    titiqqat = Pivallianiq_atuutilik.stdout.read(4096)
                    if not titiqqat: break
                    papattivik_sanimukutaak.extend(titiqqat)
            aqqusiqtarvik_atuutilik = threading.Thread(target=수집, daemon=True)
            aqqusiqtarvik_atuutilik.start()
            def 기다림(말, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 말 not in papattivik_sanimukutaak[처음:]:
                    if time.monotonic()>끝 or Pivallianiq_atuutilik.poll() is not None:
                        raise AssertionError('Missing '+repr(말)+'\n'+papattivik_sanimukutaak[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(isirut_atuutilik, maligialiit_atuutilik_4c26ea1b, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=isirut_atuutilik
                인수=['ssh','-v']+list(추가)+['-p',str(piqujijjutiliriji_kapputigaq),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',maligialiit_atuutilik_4c26ea1b]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=보안셸('!' + 설정['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in papattivik_sanimukutaak, 결과.stderr
            unikkaaq_atuutilik['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=보안셸(설정['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            unikkaaq_atuutilik['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            unikkaaq_atuutilik['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            unikkaaq_atuutilik['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            unikkaaq_atuutilik['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=보안셸(설정['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            unikkaaq_atuutilik['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(piqujijjutiliriji_kapputigaq),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ilaliujjarvilik_piliriaq=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();nirulussimaniq_atuutilik=selectors.DefaultSelector();nirulussimaniq_atuutilik.register(ilaliujjarvilik_piliriaq.stdout,selectors.EVENT_READ)
            def 대화읽기(saqqilli_atuutilik):
                마감=time.monotonic()+30
                while saqqilli_atuutilik not in 대화기록:
                    if time.monotonic()>마감 or ilaliujjarvilik_piliriaq.poll() is not None:raise AssertionError('SSH interactive missing '+repr(saqqilli_atuutilik)+' '+repr(bytes(대화기록)))
                    for Iliniku_atuutilik,_ in nirulussimaniq_atuutilik.select(.1):
                        조각=Iliniku_atuutilik.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ilaliujjarvilik_piliriaq.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ilaliujjarvilik_piliriaq.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ilaliujjarvilik_piliriaq.stdin.write(b'\x04');ilaliujjarvilik_piliriaq.stdin.flush();나머지,tammarniq=ilaliujjarvilik_piliriaq.communicate(timeout=15)
                assert ilaliujjarvilik_piliriaq.returncode==0 and b'PTY allocation request failed' not in tammarniq,(ilaliujjarvilik_piliriaq.returncode,tammarniq)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                nirulussimaniq_atuutilik.close()
                if ilaliujjarvilik_piliriaq.poll() is None:ilaliujjarvilik_piliriaq.kill();ilaliujjarvilik_piliriaq.wait()
            unikkaaq_atuutilik['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(kasurli, 수):
                titiqqat=bytearray()
                while len(titiqqat)<수:
                    덩이=kasurli.recv(수-len(titiqqat))
                    if not 덩이: raise AssertionError('RFB EOF')
                    titiqqat.extend(덩이)
                return bytes(titiqqat)
            def 화면인증(isirut_atuutilik):
                kasurli=socket.create_connection(('127.0.0.5',화면포트),10);kasurli.settimeout(30)
                assert 정확히(kasurli,12)==b'RFB 003.008\n'
                kasurli.sendall(b'RFB 003.008\n');assert 정확히(kasurli,2)==b'\x01\x02'
                kasurli.sendall(b'\x02');도전=정확히(kasurli,16)
                입력암호=isirut_atuutilik.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                kasurli.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(도전))
                qanuilinganiq_atuutilik=struct.unpack('!I',정확히(kasurli,4))[0]
                return kasurli,qanuilinganiq_atuutilik
            naammangittuq_isirut='!' if not 설정['vnc_password'].startswith('!') else '?'
            kasurli,qanuilinganiq_atuutilik=화면인증(naammangittuq_isirut);assert qanuilinganiq_atuutilik==1;kasurli.close();time.sleep(.6)
            unikkaaq_atuutilik['checks'].append('VNC incorrect password rejected')
            kasurli,qanuilinganiq_atuutilik=화면인증(설정['vnc_password']);assert qanuilinganiq_atuutilik==0
            with kasurli:
                kasurli.sendall(b'\x01');초기=정확히(kasurli,24);너비,높이=struct.unpack('!HH',초기[:4]);atiq=정확히(kasurli,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==atiq
                def 화면(증분=0):
                    kasurli.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(kasurli,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    titiraujarniq_atuutilik=bytearray(너비*높이*4)
                    for _ in range(수):
                        가로좌표,세로좌표,영역너비,영역높이,방식=struct.unpack('!HHHHi',정확히(kasurli,12));assert 방식==0 and 가로좌표+영역너비<=너비 and 세로좌표+영역높이<=높이
                        pel=정확히(kasurli,영역너비*영역높이*4);합계+=len(pel)
                        for titikutaak in range(영역높이):titiraujarniq_atuutilik[((세로좌표+titikutaak)*너비+가로좌표)*4:((세로좌표+titikutaak)*너비+가로좌표+영역너비)*4]=pel[titikutaak*영역너비*4:(titikutaak+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(titiraujarniq_atuutilik),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                unikkaaq_atuutilik['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                unikkaaq_atuutilik['checks'].append('RFB incremental update')
                처음=len(papattivik_sanimukutaak)
                for immikkuuqtuq_atuutilik in 'echo VNC_NATIVE_PASS\r':
                    기호=0xff0d if immikkuuqtuq_atuutilik=='\r' else ord(immikkuuqtuq_atuutilik)
                    kasurli.sendall(struct.pack('!BBHI',4,1,0,기호));kasurli.sendall(struct.pack('!BBHI',4,0,0,기호))
                기다림(b'VNC_NATIVE_PASS',처음)
                unikkaaq_atuutilik['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(기호,누름=1):kasurli.sendall(struct.pack('!BBHI',4,누름,0,기호))
                처음=len(papattivik_sanimukutaak)
                for immikkuuqtuq_atuutilik in 'echo ':글쇠(ord(immikkuuqtuq_atuutilik))
                글쇠(0xffc6)
                for immikkuuqtuq_atuutilik in 'gksrmf':글쇠(ord(immikkuuqtuq_atuutilik))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                unikkaaq_atuutilik['checks'].append('Native VNC F9 two-set Hangul composition')
                kasurli.sendall(struct.pack('!BBHH',5,0,120,100))
                unikkaaq_atuutilik['checks'].append('VNC pointer input accepted')
            Pivallianiq_atuutilik.stdin.write(b'poweroff\n');Pivallianiq_atuutilik.stdin.flush();Pivallianiq_atuutilik.wait(timeout=15);assert Pivallianiq_atuutilik.returncode==0
            unikkaaq_atuutilik['passed']=True
    finally:
        if Pivallianiq_atuutilik and Pivallianiq_atuutilik.poll() is None:
            Pivallianiq_atuutilik.terminate()
            try: Pivallianiq_atuutilik.wait(timeout=5)
            except subprocess.TimeoutExpired: Pivallianiq_atuutilik.kill();Pivallianiq_atuutilik.wait()
        (출력/'serial.log').write_bytes(papattivik_sanimukutaak)
        (출력/'report.json').write_text(json.dumps(unikkaaq_atuutilik,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(unikkaaq_atuutilik,ensure_ascii=False,indent=2))


if __name__=='__main__': 시작()
