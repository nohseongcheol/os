#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from gudanar_Umarni import 기준, Umarni
from 통신다리 import 통신다리


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    tatsar_manhaja_48ee4b1b.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    tatsar_manhaja_48ee4b1b.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Saituna = json.loads(인수.access.read_text())
    Rahoto_Daraja = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def holoko_fot():
        with socket.socket() as Haɗi:
            Haɗi.bind(('127.0.0.5', 0))
            return Haɗi.getsockname()[1]
    Mai_fayyace_umani_fot, 화면포트, Fayil_fot = holoko_fot(), holoko_fot(), holoko_fot()
    logu_naɗa = bytearray()
    haryar_aikin_na_ura_Daraja = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, 통신다리(Fayil_fot,
                ['tcp:{}:22'.format(Mai_fayyace_umani_fot), 'tcp:{}:5900'.format(화면포트)], sauka_imel='127.0.0.5') as 다리:
            실행인수 = Umarni()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            haryar_aikin_na_ura_Daraja = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + 다리.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    Tarin_bayani = haryar_aikin_na_ura_Daraja.stdout.read(4096)
                    if not Tarin_bayani: break
                    logu_naɗa.extend(Tarin_bayani)
            hira_Daraja = threading.Thread(target=수집, daemon=True)
            hira_Daraja.start()
            def jira_Matsayi(Microsoft_Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Microsoft_Word_SMS not in logu_naɗa[처음:]:
                    if time.monotonic()>끝 or haryar_aikin_na_ura_Daraja.poll() is not None:
                        raise AssertionError('Missing '+repr(Microsoft_Word_SMS)+'\n'+logu_naɗa[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            jira_Matsayi(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def kararre_Mai_fayyace_umani(kalmar_sirri_Daraja, Sharadi_Daraja, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=kalmar_sirri_Daraja
                인수=['ssh','-v']+list(추가)+['-p',str(Mai_fayyace_umani_fot),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',Sharadi_Daraja]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=kararre_Mai_fayyace_umani('!' + Saituna['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in logu_naɗa, 결과.stderr
            Rahoto_Daraja['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=kararre_Mai_fayyace_umani(Saituna['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            Rahoto_Daraja['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            Rahoto_Daraja['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=kararre_Mai_fayyace_umani(Saituna['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            Rahoto_Daraja['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=kararre_Mai_fayyace_umani(Saituna['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            Rahoto_Daraja['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=kararre_Mai_fayyace_umani(Saituna['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            Rahoto_Daraja['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(Mai_fayyace_umani_fot),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();bangaren_zaɓi_Daraja=selectors.DefaultSelector();bangaren_zaɓi_Daraja.register(Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.stdout,selectors.EVENT_READ)
            def 대화읽기(Nuna_Daraja):
                마감=time.monotonic()+30
                while Nuna_Daraja not in 대화기록:
                    if time.monotonic()>마감 or Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.poll() is not None:raise AssertionError('SSH interactive missing '+repr(Nuna_Daraja)+' '+repr(bytes(대화기록)))
                    for Mashigar_bayanai_Daraja,_ in bangaren_zaɓi_Daraja.select(.1):
                        조각=Mashigar_bayanai_Daraja.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.stdin.write(b'\x04');Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.stdin.flush();나머지,Kuskure=Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.communicate(timeout=15)
                assert Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.returncode==0 and b'PTY allocation request failed' not in Kuskure,(Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.returncode,Kuskure)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                bangaren_zaɓi_Daraja.close()
                if Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.poll() is None:Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.kill();Shigar_da_umarni_na_kwamfuta_Mahadin_canjin_bayanai.wait()
            Rahoto_Daraja['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Haɗi, 수):
                Tarin_bayani=bytearray()
                while len(Tarin_bayani)<수:
                    덩이=Haɗi.recv(수-len(Tarin_bayani))
                    if not 덩이: raise AssertionError('RFB EOF')
                    Tarin_bayani.extend(덩이)
                return bytes(Tarin_bayani)
            def 화면인증(kalmar_sirri_Daraja):
                Haɗi=socket.create_connection(('127.0.0.5',화면포트),10);Haɗi.settimeout(30)
                assert 정확히(Haɗi,12)==b'RFB 003.008\n'
                Haɗi.sendall(b'RFB 003.008\n');assert 정확히(Haɗi,2)==b'\x01\x02'
                Haɗi.sendall(b'\x02');ƙalubale_Daraja=정확히(Haɗi,16)
                입력암호=kalmar_sirri_Daraja.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Haɗi.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ƙalubale_Daraja))
                Matsayi_Daraja=struct.unpack('!I',정확히(Haɗi,4))[0]
                return Haɗi,Matsayi_Daraja
            mara_ƙarfi_kalmar_sirri='!' if not Saituna['vnc_password'].startswith('!') else '?'
            Haɗi,Matsayi_Daraja=화면인증(mara_ƙarfi_kalmar_sirri);assert Matsayi_Daraja==1;Haɗi.close();time.sleep(.6)
            Rahoto_Daraja['checks'].append('VNC incorrect password rejected')
            Haɗi,Matsayi_Daraja=화면인증(Saituna['vnc_password']);assert Matsayi_Daraja==0
            with Haɗi:
                Haɗi.sendall(b'\x01');초기=정확히(Haɗi,24);너비,높이=struct.unpack('!HH',초기[:4]);Suna=정확히(Haɗi,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Suna
                def 화면(증분=0):
                    Haɗi.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Haɗi,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    zane_Daraja=bytearray(너비*높이*4)
                    for _ in range(수):
                        gamayyar_x,Maɓallin_Y_Mai_tsarawa,영역너비,영역높이,tsari_yanayin_aiki=struct.unpack('!HHHHi',정확히(Haɗi,12));assert tsari_yanayin_aiki==0 and gamayyar_x+영역너비<=너비 and Maɓallin_Y_Mai_tsarawa+영역높이<=높이
                        pel=정확히(Haɗi,영역너비*영역높이*4);합계+=len(pel)
                        for Layi in range(영역높이):zane_Daraja[((Maɓallin_Y_Mai_tsarawa+Layi)*너비+gamayyar_x)*4:((Maɓallin_Y_Mai_tsarawa+Layi)*너비+gamayyar_x+영역너비)*4]=pel[Layi*영역너비*4:(Layi+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(zane_Daraja),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                Rahoto_Daraja['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                Rahoto_Daraja['checks'].append('RFB incremental update')
                처음=len(logu_naɗa)
                for Harafi_Daraja in 'echo VNC_NATIVE_PASS\r':
                    alama_ad6f1a96=0xff0d if Harafi_Daraja=='\r' else ord(Harafi_Daraja)
                    Haɗi.sendall(struct.pack('!BBHI',4,1,0,alama_ad6f1a96));Haɗi.sendall(struct.pack('!BBHI',4,0,0,alama_ad6f1a96))
                jira_Matsayi(b'VNC_NATIVE_PASS',처음)
                Rahoto_Daraja['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(alama_ad6f1a96,누름=1):Haɗi.sendall(struct.pack('!BBHI',4,누름,0,alama_ad6f1a96))
                처음=len(logu_naɗa)
                for Harafi_Daraja in 'echo ':글쇠(ord(Harafi_Daraja))
                글쇠(0xffc6)
                for Harafi_Daraja in 'gksrmf':글쇠(ord(Harafi_Daraja))
                글쇠(0xffc6);글쇠(0xff0d)
                jira_Matsayi('\r\n한글\r\n'.encode(),처음)
                Rahoto_Daraja['checks'].append('Native VNC F9 two-set Hangul composition')
                Haɗi.sendall(struct.pack('!BBHH',5,0,120,100))
                Rahoto_Daraja['checks'].append('VNC pointer input accepted')
            haryar_aikin_na_ura_Daraja.stdin.write(b'poweroff\n');haryar_aikin_na_ura_Daraja.stdin.flush();haryar_aikin_na_ura_Daraja.wait(timeout=15);assert haryar_aikin_na_ura_Daraja.returncode==0
            Rahoto_Daraja['passed']=True
    finally:
        if haryar_aikin_na_ura_Daraja and haryar_aikin_na_ura_Daraja.poll() is None:
            haryar_aikin_na_ura_Daraja.terminate()
            try: haryar_aikin_na_ura_Daraja.wait(timeout=5)
            except subprocess.TimeoutExpired: haryar_aikin_na_ura_Daraja.kill();haryar_aikin_na_ura_Daraja.wait()
        (출력/'serial.log').write_bytes(logu_naɗa)
        (출력/'report.json').write_text(json.dumps(Rahoto_Daraja,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Rahoto_Daraja,ensure_ascii=False,indent=2))


if __name__=='__main__': Tafiyar_da()
