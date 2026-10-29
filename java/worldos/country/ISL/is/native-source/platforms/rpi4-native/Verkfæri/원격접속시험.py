#!/usr/bin/env python3
"""raun_gögn OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from keyra_skipun import verk_rót, Skipun
from Net_brú import Net_brú


def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--kernel', type=Path, default=verk_rót / 'build/kernel8.img')
    þáttari_48ee4b1b.add_argument('--access', type=Path, default=verk_rót / 'build/remote/access.json')
    þáttari_48ee4b1b.add_argument('--output', type=Path, default=verk_rót / 'build/verification/native-remote')
    Viðföng = þáttari_48ee4b1b.parse_args()
    úttak = Viðföng.output
    úttak.mkdir(parents=True, exist_ok=True)
    Stillingar = json.loads(Viðföng.access.read_text())
    skrá_VALUE_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Viðföng.kernel.read_bytes()).hexdigest(), 'checks': []}
    def autt_gátt():
        with socket.socket() as Tengjast:
            Tengjast.bind(('127.0.0.5', 0))
            return Tengjast.getsockname()[1]
    skel_gátt, 화면포트, skrá_gátt = autt_gátt(), autt_gátt(), autt_gátt()
    LOG_lína = bytearray()
    Ferli_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Net_brú(skrá_gátt,
                ['tcp:{}:22'.format(skel_gátt), 'tcp:{}:5900'.format(화면포트)], hýsa_slóð='127.0.0.5') as brú_VALUE:
            실행인수 = Skipun()
            실행인수[실행인수.index('-kernel') + 1] = str(Viðföng.kernel.resolve())
            Ferli_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + brú_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    gögn = Ferli_VALUE.stdout.read(4096)
                    if not gögn: break
                    LOG_lína.extend(gögn)
            þráður_VALUE = threading.Thread(target=수집, daemon=True)
            þráður_VALUE.start()
            def Bíddu_staða(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_lína[처음:]:
                    if time.monotonic()>끝 or Ferli_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_lína[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            Bíddu_staða(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def öruggt_skel(aðgangsorð_VALUE, skipun_VALUE, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=aðgangsorð_VALUE
                Viðföng=['ssh','-v']+list(추가)+['-p',str(skel_gátt),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',skipun_VALUE]
                NIÐURSTAÐA=subprocess.run(Viðföng,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return NIÐURSTAÐA
            NIÐURSTAÐA=öruggt_skel('!' + Stillingar['ssh_password'], 'echo SHOULD_NOT_RUN')
            (úttak/'ssh-rejected.log').write_bytes(NIÐURSTAÐA.stderr)
            assert NIÐURSTAÐA.returncode!=0 and b'Permission denied' in NIÐURSTAÐA.stderr and b'SHOULD_NOT_RUN' not in LOG_lína, NIÐURSTAÐA.stderr
            skrá_VALUE_ddf2aaf3['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            NIÐURSTAÐA=öruggt_skel(Stillingar['ssh_password'], 'echo SSH_NATIVE_PASS')
            (úttak/'ssh.log').write_bytes(NIÐURSTAÐA.stderr)
            (úttak/'ssh-output.txt').write_bytes(NIÐURSTAÐA.stdout)
            assert NIÐURSTAÐA.returncode==0 and b'SSH_NATIVE_PASS' in NIÐURSTAÐA.stdout, (NIÐURSTAÐA.returncode,NIÐURSTAÐA.stdout,NIÐURSTAÐA.stderr)
            skrá_VALUE_ddf2aaf3['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in NIÐURSTAÐA.stderr, NIÐURSTAÐA.stderr
            skrá_VALUE_ddf2aaf3['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            NIÐURSTAÐA=öruggt_skel(Stillingar['ssh_password'], 'cd /example/java; java Úttaksdæmi; cd /')
            assert NIÐURSTAÐA.returncode==0 and 'JAVA úttak: 안녕하세요 😀'.encode() in NIÐURSTAÐA.stdout,NIÐURSTAÐA.stdout
            skrá_VALUE_ddf2aaf3['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            NIÐURSTAÐA=öruggt_skel(Stillingar['ssh_password'], 'missing_remote_command')
            assert NIÐURSTAÐA.returncode==127,NIÐURSTAÐA.returncode
            skrá_VALUE_ddf2aaf3['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            NIÐURSTAÐA=öruggt_skel(Stillingar['ssh_password'], 'cat /example/java/Gluggadæmi.java', ('-o', 'RekeyLimit=1K'))
            (úttak/'ssh-rekey.log').write_bytes(NIÐURSTAÐA.stderr)
            assert NIÐURSTAÐA.returncode==0 and 'class Gluggadæmi'.encode() in NIÐURSTAÐA.stdout, (NIÐURSTAÐA.returncode,NIÐURSTAÐA.stdout,NIÐURSTAÐA.stderr)
            assert NIÐURSTAÐA.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, NIÐURSTAÐA.stderr
            skrá_VALUE_ddf2aaf3['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(skel_gátt),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            gagnvirkur_lota=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();val_VALUE=selectors.DefaultSelector();val_VALUE.register(gagnvirkur_lota.stdout,selectors.EVENT_READ)
            def 대화읽기(sýna_VALUE):
                마감=time.monotonic()+30
                while sýna_VALUE not in 대화기록:
                    if time.monotonic()>마감 or gagnvirkur_lota.poll() is not None:raise AssertionError('SSH interactive missing '+repr(sýna_VALUE)+' '+repr(bytes(대화기록)))
                    for færsla_VALUE,_ in val_VALUE.select(.1):
                        조각=færsla_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                gagnvirkur_lota.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');gagnvirkur_lota.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                gagnvirkur_lota.stdin.write(b'\x04');gagnvirkur_lota.stdin.flush();나머지,Villa=gagnvirkur_lota.communicate(timeout=15)
                assert gagnvirkur_lota.returncode==0 and b'PTY allocation request failed' not in Villa,(gagnvirkur_lota.returncode,Villa)
                (úttak/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                val_VALUE.close()
                if gagnvirkur_lota.poll() is None:gagnvirkur_lota.kill();gagnvirkur_lota.wait()
            skrá_VALUE_ddf2aaf3['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Tengjast, númer):
                gögn=bytearray()
                while len(gögn)<númer:
                    덩이=Tengjast.recv(númer-len(gögn))
                    if not 덩이: raise AssertionError('RFB EOF')
                    gögn.extend(덩이)
                return bytes(gögn)
            def 화면인증(aðgangsorð_VALUE):
                Tengjast=socket.create_connection(('127.0.0.5',화면포트),10);Tengjast.settimeout(30)
                assert 정확히(Tengjast,12)==b'RFB 003.008\n'
                Tengjast.sendall(b'RFB 003.008\n');assert 정확히(Tengjast,2)==b'\x01\x02'
                Tengjast.sendall(b'\x02');áskorun_VALUE=정확히(Tengjast,16)
                입력암호=aðgangsorð_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(númer)[::-1],2) for númer in 입력암호)
                Tengjast.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(áskorun_VALUE))
                staða_VALUE_e10195a1=struct.unpack('!I',정확히(Tengjast,4))[0]
                return Tengjast,staða_VALUE_e10195a1
            ógilt_aðgangsorð='!' if not Stillingar['vnc_password'].startswith('!') else '?'
            Tengjast,staða_VALUE_e10195a1=화면인증(ógilt_aðgangsorð);assert staða_VALUE_e10195a1==1;Tengjast.close();time.sleep(.6)
            skrá_VALUE_ddf2aaf3['checks'].append('VNC incorrect password rejected')
            Tengjast,staða_VALUE_e10195a1=화면인증(Stillingar['vnc_password']);assert staða_VALUE_e10195a1==0
            with Tengjast:
                Tengjast.sendall(b'\x01');초기=정확히(Tengjast,24);너비,높이=struct.unpack('!HH',초기[:4]);Heiti=정확히(Tengjast,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Heiti
                def 화면(증분=0):
                    Tengjast.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Tengjast,4);númer=struct.unpack('!H',머리[2:])[0];samtala_VALUE=0
                    teikning_VALUE=bytearray(너비*높이*4)
                    for _ in range(númer):
                        x_hnit,Y_hnit,영역너비,영역높이,aðferð_MODE=struct.unpack('!HHHHi',정확히(Tengjast,12));assert aðferð_MODE==0 and x_hnit+영역너비<=너비 and Y_hnit+영역높이<=높이
                        díll=정확히(Tengjast,영역너비*영역높이*4);samtala_VALUE+=len(díll)
                        for Lína in range(영역높이):teikning_VALUE[((Y_hnit+Lína)*너비+x_hnit)*4:((Y_hnit+Lína)*너비+x_hnit+영역너비)*4]=díll[Lína*영역너비*4:(Lína+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(teikning_VALUE),'raw','BGRX').save(str(úttak/'native-vnc.png'))
                    return númer,samtala_VALUE
                númer,samtala_VALUE=화면();assert númer>0 and samtala_VALUE==너비*높이*4
                skrá_VALUE_ddf2aaf3['checks'].append('Native framebuffer RFB full update {} bytes'.format(samtala_VALUE))
                númer,samtala_VALUE=화면(1);assert samtala_VALUE<너비*높이*4
                skrá_VALUE_ddf2aaf3['checks'].append('RFB incremental update')
                처음=len(LOG_lína)
                for stafur_VALUE in 'echo VNC_NATIVE_PASS\r':
                    tákn=0xff0d if stafur_VALUE=='\r' else ord(stafur_VALUE)
                    Tengjast.sendall(struct.pack('!BBHI',4,1,0,tákn));Tengjast.sendall(struct.pack('!BBHI',4,0,0,tákn))
                Bíddu_staða(b'VNC_NATIVE_PASS',처음)
                skrá_VALUE_ddf2aaf3['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(tákn,ýta_VALUE=1):Tengjast.sendall(struct.pack('!BBHI',4,ýta_VALUE,0,tákn))
                처음=len(LOG_lína)
                for stafur_VALUE in 'echo ':글쇠(ord(stafur_VALUE))
                글쇠(0xffc6)
                for stafur_VALUE in 'gksrmf':글쇠(ord(stafur_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                Bíddu_staða('\r\n한글\r\n'.encode(),처음)
                skrá_VALUE_ddf2aaf3['checks'].append('Native VNC F9 two-set Hangul composition')
                Tengjast.sendall(struct.pack('!BBHH',5,0,120,100))
                skrá_VALUE_ddf2aaf3['checks'].append('VNC pointer input accepted')
            Ferli_VALUE.stdin.write(b'poweroff\n');Ferli_VALUE.stdin.flush();Ferli_VALUE.wait(timeout=15);assert Ferli_VALUE.returncode==0
            skrá_VALUE_ddf2aaf3['passed']=True
    finally:
        if Ferli_VALUE and Ferli_VALUE.poll() is None:
            Ferli_VALUE.terminate()
            try: Ferli_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Ferli_VALUE.kill();Ferli_VALUE.wait()
        (úttak/'serial.log').write_bytes(LOG_lína)
        (úttak/'report.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(skrá_VALUE_ddf2aaf3,ensure_ascii=False,indent=2))


if __name__=='__main__': Keyra_2()
