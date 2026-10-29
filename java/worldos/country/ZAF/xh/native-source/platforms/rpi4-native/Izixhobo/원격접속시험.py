#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ukwenza_umyalelo import 기준, Umyalelo
from Inethiwekhi_ibhulorho import Inethiwekhi_ibhulorho


def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=기준 / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=기준 / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=기준 / 'build/verification/native-remote')
    인수 = 해석기.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Imimiselo = json.loads(인수.access.read_text())
    ingxelo_ixabiso_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def engenanto_iphothi():
        with socket.socket() as Nxulumanisa:
            Nxulumanisa.bind(('127.0.0.5', 0))
            return Nxulumanisa.getsockname()[1]
    isiniki_myalelo_iphothi, 화면포트, ifayile_iphothi = engenanto_iphothi(), engenanto_iphothi(), engenanto_iphothi()
    ilog_umqolo = bytearray()
    Inkqubo_ixabiso = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, Inethiwekhi_ibhulorho(ifayile_iphothi,
                ['tcp:{}:22'.format(isiniki_myalelo_iphothi), 'tcp:{}:5900'.format(화면포트)], umsingathi_idilesi='127.0.0.5') as ibhulorho_ixabiso:
            실행인수 = Umyalelo()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Inkqubo_ixabiso = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ibhulorho_ixabiso.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    iingcombolo = Inkqubo_ixabiso.stdout.read(4096)
                    if not iingcombolo: break
                    ilog_umqolo.extend(iingcombolo)
            ithredi_ixabiso = threading.Thread(target=수집, daemon=True)
            ithredi_ixabiso.start()
            def 기다림(Igama_I_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Igama_I_SMS not in ilog_umqolo[처음:]:
                    if time.monotonic()>끝 or Inkqubo_ixabiso.poll() is not None:
                        raise AssertionError('Missing '+repr(Igama_I_SMS)+'\n'+ilog_umqolo[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            기다림(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ikhuselekile_isiniki_myalelo(iphaswedi_ixabiso, umyalelo_ixabiso, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=iphaswedi_ixabiso
                인수=['ssh','-v']+list(추가)+['-p',str(isiniki_myalelo_iphothi),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',umyalelo_ixabiso]
                결과=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return 결과
            결과=ikhuselekile_isiniki_myalelo('!' + Imimiselo['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(결과.stderr)
            assert 결과.returncode!=0 and b'Permission denied' in 결과.stderr and b'SHOULD_NOT_RUN' not in ilog_umqolo, 결과.stderr
            ingxelo_ixabiso_ddf2aaf3['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            결과=ikhuselekile_isiniki_myalelo(Imimiselo['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(결과.stderr)
            (출력/'ssh-output.txt').write_bytes(결과.stdout)
            assert 결과.returncode==0 and b'SSH_NATIVE_PASS' in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            ingxelo_ixabiso_ddf2aaf3['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in 결과.stderr, 결과.stderr
            ingxelo_ixabiso_ddf2aaf3['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            결과=ikhuselekile_isiniki_myalelo(Imimiselo['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert 결과.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in 결과.stdout,결과.stdout
            ingxelo_ixabiso_ddf2aaf3['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            결과=ikhuselekile_isiniki_myalelo(Imimiselo['ssh_password'], 'missing_remote_command')
            assert 결과.returncode==127,결과.returncode
            ingxelo_ixabiso_ddf2aaf3['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            결과=ikhuselekile_isiniki_myalelo(Imimiselo['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(결과.stderr)
            assert 결과.returncode==0 and 'class 창예제'.encode() in 결과.stdout, (결과.returncode,결과.stdout,결과.stderr)
            assert 결과.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, 결과.stderr
            ingxelo_ixabiso_ddf2aaf3['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(isiniki_myalelo_iphothi),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            esebenzisana_nomsebenzi_iseshoni=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ukukhetha_ixabiso=selectors.DefaultSelector();ukukhetha_ixabiso.register(esebenzisana_nomsebenzi_iseshoni.stdout,selectors.EVENT_READ)
            def 대화읽기(bonisa_ixabiso):
                마감=time.monotonic()+30
                while bonisa_ixabiso not in 대화기록:
                    if time.monotonic()>마감 or esebenzisana_nomsebenzi_iseshoni.poll() is not None:raise AssertionError('SSH interactive missing '+repr(bonisa_ixabiso)+' '+repr(bytes(대화기록)))
                    for ufako_nkcukacha_ixabiso,_ in ukukhetha_ixabiso.select(.1):
                        조각=ufako_nkcukacha_ixabiso.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                esebenzisana_nomsebenzi_iseshoni.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');esebenzisana_nomsebenzi_iseshoni.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                esebenzisana_nomsebenzi_iseshoni.stdin.write(b'\x04');esebenzisana_nomsebenzi_iseshoni.stdin.flush();나머지,Impazamo=esebenzisana_nomsebenzi_iseshoni.communicate(timeout=15)
                assert esebenzisana_nomsebenzi_iseshoni.returncode==0 and b'PTY allocation request failed' not in Impazamo,(esebenzisana_nomsebenzi_iseshoni.returncode,Impazamo)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ukukhetha_ixabiso.close()
                if esebenzisana_nomsebenzi_iseshoni.poll() is None:esebenzisana_nomsebenzi_iseshoni.kill();esebenzisana_nomsebenzi_iseshoni.wait()
            ingxelo_ixabiso_ddf2aaf3['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Nxulumanisa, 수):
                iingcombolo=bytearray()
                while len(iingcombolo)<수:
                    덩이=Nxulumanisa.recv(수-len(iingcombolo))
                    if not 덩이: raise AssertionError('RFB EOF')
                    iingcombolo.extend(덩이)
                return bytes(iingcombolo)
            def 화면인증(iphaswedi_ixabiso):
                Nxulumanisa=socket.create_connection(('127.0.0.5',화면포트),10);Nxulumanisa.settimeout(30)
                assert 정확히(Nxulumanisa,12)==b'RFB 003.008\n'
                Nxulumanisa.sendall(b'RFB 003.008\n');assert 정확히(Nxulumanisa,2)==b'\x01\x02'
                Nxulumanisa.sendall(b'\x02');umngeni_ixabiso=정확히(Nxulumanisa,16)
                입력암호=iphaswedi_ixabiso.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Nxulumanisa.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(umngeni_ixabiso))
                imo_ixabiso=struct.unpack('!I',정확히(Nxulumanisa,4))[0]
                return Nxulumanisa,imo_ixabiso
            ayisebenzi_iphaswedi='!' if not Imimiselo['vnc_password'].startswith('!') else '?'
            Nxulumanisa,imo_ixabiso=화면인증(ayisebenzi_iphaswedi);assert imo_ixabiso==1;Nxulumanisa.close();time.sleep(.6)
            ingxelo_ixabiso_ddf2aaf3['checks'].append('VNC incorrect password rejected')
            Nxulumanisa,imo_ixabiso=화면인증(Imimiselo['vnc_password']);assert imo_ixabiso==0
            with Nxulumanisa:
                Nxulumanisa.sendall(b'\x01');초기=정확히(Nxulumanisa,24);너비,높이=struct.unpack('!HH',초기[:4]);Igama=정확히(Nxulumanisa,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Igama
                def 화면(증분=0):
                    Nxulumanisa.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(Nxulumanisa,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    umzobo_ixabiso=bytearray(너비*높이*4)
                    for _ in range(수):
                        isilungelelanisi_x,세로좌표,영역너비,영역높이,imethodi_imo=struct.unpack('!HHHHi',정확히(Nxulumanisa,12));assert imethodi_imo==0 and isilungelelanisi_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        i_pel=정확히(Nxulumanisa,영역너비*영역높이*4);합계+=len(i_pel)
                        for umgca in range(영역높이):umzobo_ixabiso[((세로좌표+umgca)*너비+isilungelelanisi_x)*4:((세로좌표+umgca)*너비+isilungelelanisi_x+영역너비)*4]=i_pel[umgca*영역너비*4:(umgca+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(umzobo_ixabiso),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ingxelo_ixabiso_ddf2aaf3['checks'].append('RFB incremental update')
                처음=len(ilog_umqolo)
                for ikharakhtha_ixabiso in 'echo VNC_NATIVE_PASS\r':
                    isimboli=0xff0d if ikharakhtha_ixabiso=='\r' else ord(ikharakhtha_ixabiso)
                    Nxulumanisa.sendall(struct.pack('!BBHI',4,1,0,isimboli));Nxulumanisa.sendall(struct.pack('!BBHI',4,0,0,isimboli))
                기다림(b'VNC_NATIVE_PASS',처음)
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(isimboli,누름=1):Nxulumanisa.sendall(struct.pack('!BBHI',4,누름,0,isimboli))
                처음=len(ilog_umqolo)
                for ikharakhtha_ixabiso in 'echo ':글쇠(ord(ikharakhtha_ixabiso))
                글쇠(0xffc6)
                for ikharakhtha_ixabiso in 'gksrmf':글쇠(ord(ikharakhtha_ixabiso))
                글쇠(0xffc6);글쇠(0xff0d)
                기다림('\r\n한글\r\n'.encode(),처음)
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Native VNC F9 two-set Hangul composition')
                Nxulumanisa.sendall(struct.pack('!BBHH',5,0,120,100))
                ingxelo_ixabiso_ddf2aaf3['checks'].append('VNC pointer input accepted')
            Inkqubo_ixabiso.stdin.write(b'poweroff\n');Inkqubo_ixabiso.stdin.flush();Inkqubo_ixabiso.wait(timeout=15);assert Inkqubo_ixabiso.returncode==0
            ingxelo_ixabiso_ddf2aaf3['passed']=True
    finally:
        if Inkqubo_ixabiso and Inkqubo_ixabiso.poll() is None:
            Inkqubo_ixabiso.terminate()
            try: Inkqubo_ixabiso.wait(timeout=5)
            except subprocess.TimeoutExpired: Inkqubo_ixabiso.kill();Inkqubo_ixabiso.wait()
        (출력/'serial.log').write_bytes(ilog_umqolo)
        (출력/'report.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ingxelo_ixabiso_ddf2aaf3,ensure_ascii=False,indent=2))


if __name__=='__main__': Phumeza()
