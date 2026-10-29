#!/usr/bin/env python3
"""sebenar_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from laksanakan_perintah import projek_akar, Perintah
from rangkaian_penghubung import rangkaian_penghubung


def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--kernel', type=Path, default=projek_akar / 'build/kernel8.img')
    penghurai_48ee4b1b.add_argument('--access', type=Path, default=projek_akar / 'build/remote/access.json')
    penghurai_48ee4b1b.add_argument('--output', type=Path, default=projek_akar / 'build/verification/native-remote')
    인수 = penghurai_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    Tetapan = json.loads(인수.access.read_text())
    lapor_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Sambung:
            Sambung.bind(('127.0.0.5', 0))
            return Sambung.getsockname()[1]
    cangkerang_port, 화면포트, fail_port = 빈포트(), 빈포트(), 빈포트()
    LOG_baris = bytearray()
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, rangkaian_penghubung(fail_port,
                ['tcp:{}:22'.format(cangkerang_port), 'tcp:{}:5900'.format(화면포트)], hos_e_mel='127.0.0.5') as penghubung_VALUE:
            실행인수 = Perintah()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            Proses_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + penghubung_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proses_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_baris.extend(data)
            urutan_VALUE = threading.Thread(target=수집, daemon=True)
            urutan_VALUE.start()
            def keadaan_tunggu(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_baris[처음:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_baris[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            keadaan_tunggu(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            persekitaran = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def selamat_cangkerang(kata_laluan_VALUE, suruhan_VALUE, Tambah_pemasukan=()):
                persekitaran['JKOROS_TEST_PASSWORD']=kata_laluan_VALUE
                인수=['ssh','-v']+list(Tambah_pemasukan)+['-p',str(cangkerang_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',suruhan_VALUE]
                ukuran=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=persekitaran,start_new_session=True,timeout=50)
                return ukuran
            ukuran=selamat_cangkerang('!' + Tetapan['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(ukuran.stderr)
            assert ukuran.returncode!=0 and b'Permission denied' in ukuran.stderr and b'SHOULD_NOT_RUN' not in LOG_baris, ukuran.stderr
            lapor_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ukuran=selamat_cangkerang(Tetapan['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(ukuran.stderr)
            (출력/'ssh-output.txt').write_bytes(ukuran.stdout)
            assert ukuran.returncode==0 and b'SSH_NATIVE_PASS' in ukuran.stdout, (ukuran.returncode,ukuran.stdout,ukuran.stderr)
            lapor_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ukuran.stderr, ukuran.stderr
            lapor_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ukuran=selamat_cangkerang(Tetapan['ssh_password'], 'cd /example/java; java ContohKeluaran; cd /')
            assert ukuran.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in ukuran.stdout,ukuran.stdout
            lapor_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ukuran=selamat_cangkerang(Tetapan['ssh_password'], 'missing_remote_command')
            assert ukuran.returncode==127,ukuran.returncode
            lapor_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ukuran=selamat_cangkerang(Tetapan['ssh_password'], 'cat /example/java/ContohTetingkap.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(ukuran.stderr)
            assert ukuran.returncode==0 and 'class ContohTetingkap'.encode() in ukuran.stdout, (ukuran.returncode,ukuran.stdout,ukuran.stderr)
            assert ukuran.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ukuran.stderr
            lapor_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(cangkerang_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktif_sesi=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=persekitaran,start_new_session=True,bufsize=0)
            대화기록=bytearray();pilihan_VALUE=selectors.DefaultSelector();pilihan_VALUE.register(interaktif_sesi.stdout,selectors.EVENT_READ)
            def 대화읽기(tayang_VALUE):
                마감=time.monotonic()+30
                while tayang_VALUE not in 대화기록:
                    if time.monotonic()>마감 or interaktif_sesi.poll() is not None:raise AssertionError('SSH interactive missing '+repr(tayang_VALUE)+' '+repr(bytes(대화기록)))
                    for pemasukan_VALUE,_ in pilihan_VALUE.select(.1):
                        조각=pemasukan_VALUE.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktif_sesi.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktif_sesi.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktif_sesi.stdin.write(b'\x04');interaktif_sesi.stdin.flush();나머지,RALAT=interaktif_sesi.communicate(timeout=15)
                assert interaktif_sesi.returncode==0 and b'PTY allocation request failed' not in RALAT,(interaktif_sesi.returncode,RALAT)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                pilihan_VALUE.close()
                if interaktif_sesi.poll() is None:interaktif_sesi.kill();interaktif_sesi.wait()
            lapor_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Sambung, 수):
                data=bytearray()
                while len(data)<수:
                    cebis_VALUE=Sambung.recv(수-len(data))
                    if not cebis_VALUE: raise AssertionError('RFB EOF')
                    data.extend(cebis_VALUE)
                return bytes(data)
            def 화면인증(kata_laluan_VALUE):
                Sambung=socket.create_connection(('127.0.0.5',화면포트),10);Sambung.settimeout(30)
                assert 정확히(Sambung,12)==b'RFB 003.008\n'
                Sambung.sendall(b'RFB 003.008\n');assert 정확히(Sambung,2)==b'\x01\x02'
                Sambung.sendall(b'\x02');cabaran_VALUE=정확히(Sambung,16)
                입력암호=kata_laluan_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Sambung.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(cabaran_VALUE))
                status_VALUE=struct.unpack('!I',정확히(Sambung,4))[0]
                return Sambung,status_VALUE
            tak_sah_kata_laluan='!' if not Tetapan['vnc_password'].startswith('!') else '?'
            Sambung,status_VALUE=화면인증(tak_sah_kata_laluan);assert status_VALUE==1;Sambung.close();time.sleep(.6)
            lapor_VALUE['checks'].append('VNC incorrect password rejected')
            Sambung,status_VALUE=화면인증(Tetapan['vnc_password']);assert status_VALUE==0
            with Sambung:
                Sambung.sendall(b'\x01');초기=정확히(Sambung,24);너비,높이=struct.unpack('!HH',초기[:4]);Nama=정확히(Sambung,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nama
                def 화면(tokokan_langkah=0):
                    Sambung.sendall(struct.pack('!BBHHHH',3,tokokan_langkah,0,0,너비,높이));머리=정확히(Sambung,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    lukisan_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        koordinat_x,Y_koordinat,영역너비,영역높이,kaedah_mod=struct.unpack('!HHHHi',정확히(Sambung,12));assert kaedah_mod==0 and koordinat_x+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        pel=정확히(Sambung,영역너비*영역높이*4);합계+=len(pel)
                        for baris in range(영역높이):lukisan_VALUE[((Y_koordinat+baris)*너비+koordinat_x)*4:((Y_koordinat+baris)*너비+koordinat_x+영역너비)*4]=pel[baris*영역너비*4:(baris+1)*영역너비*4]
                    if not tokokan_langkah:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(lukisan_VALUE),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                lapor_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                lapor_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_baris)
                for aksara_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if aksara_VALUE=='\r' else ord(aksara_VALUE)
                    Sambung.sendall(struct.pack('!BBHI',4,1,0,simbol));Sambung.sendall(struct.pack('!BBHI',4,0,0,simbol))
                keadaan_tunggu(b'VNC_NATIVE_PASS',처음)
                lapor_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbol,tekan_VALUE=1):Sambung.sendall(struct.pack('!BBHI',4,tekan_VALUE,0,simbol))
                처음=len(LOG_baris)
                for aksara_VALUE in 'echo ':글쇠(ord(aksara_VALUE))
                글쇠(0xffc6)
                for aksara_VALUE in 'gksrmf':글쇠(ord(aksara_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                keadaan_tunggu('\r\n한글\r\n'.encode(),처음)
                lapor_VALUE['checks'].append('Native VNC F9 two-set Hangul composition')
                Sambung.sendall(struct.pack('!BBHH',5,0,120,100))
                lapor_VALUE['checks'].append('VNC pointer input accepted')
            Proses_VALUE.stdin.write(b'poweroff\n');Proses_VALUE.stdin.flush();Proses_VALUE.wait(timeout=15);assert Proses_VALUE.returncode==0
            lapor_VALUE['passed']=True
    finally:
        if Proses_VALUE and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses_VALUE.kill();Proses_VALUE.wait()
        (출력/'serial.log').write_bytes(LOG_baris)
        (출력/'report.json').write_text(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': Jalan()
