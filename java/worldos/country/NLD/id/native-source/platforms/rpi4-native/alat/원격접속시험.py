#!/usr/bin/env python3
"""aktual_data OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from Jalankan_perintah import Tugas_akar, perintah
from jaringan_bridge import jaringan_bridge


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--kernel', type=Path, default=Tugas_akar / 'build/kernel8.img')
    parser_48ee4b1b.add_argument('--access', type=Path, default=Tugas_akar / 'build/remote/access.json')
    parser_48ee4b1b.add_argument('--output', type=Path, default=Tugas_akar / 'build/verification/native-remote')
    argumen = parser_48ee4b1b.parse_args()
    keluaranTeks = argumen.output
    keluaranTeks.mkdir(parents=True, exist_ok=True)
    Konfigurasi = json.loads(argumen.access.read_text())
    lapor_VALUE = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(argumen.kernel.read_bytes()).hexdigest(), 'checks': []}
    def kosong_port():
        with socket.socket() as Sambung:
            Sambung.bind(('127.0.0.5', 0))
            return Sambung.getsockname()[1]
    shell_port, 화면포트, file_port = kosong_port(), kosong_port(), kosong_port()
    LOG_baris = bytearray()
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, jaringan_bridge(file_port,
                ['tcp:{}:22'.format(shell_port), 'tcp:{}:5900'.format(화면포트)], host_surel='127.0.0.5') as bridge_VALUE:
            실행인수 = perintah()
            실행인수[실행인수.index('-kernel') + 1] = str(argumen.kernel.resolve())
            Proses_VALUE = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + bridge_VALUE.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    data = Proses_VALUE.stdout.read(4096)
                    if not data: break
                    LOG_baris.extend(data)
            alur_VALUE = threading.Thread(target=수집, daemon=True)
            alur_VALUE.start()
            def tunggu_Status(Kata_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Kata_SMS not in LOG_baris[처음:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing '+repr(Kata_SMS)+'\n'+LOG_baris[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            tunggu_Status(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            lingkungan = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def aman_shell(sandi_VALUE, instruksi_VALUE, tambah_entri=()):
                lingkungan['JKOROS_TEST_PASSWORD']=sandi_VALUE
                argumen=['ssh','-v']+list(tambah_entri)+['-p',str(shell_port),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',instruksi_VALUE]
                hasil=subprocess.run(argumen,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=lingkungan,start_new_session=True,timeout=50)
                return hasil
            hasil=aman_shell('!' + Konfigurasi['ssh_password'], 'echo SHOULD_NOT_RUN')
            (keluaranTeks/'ssh-rejected.log').write_bytes(hasil.stderr)
            assert hasil.returncode!=0 and b'Permission denied' in hasil.stderr and b'SHOULD_NOT_RUN' not in LOG_baris, hasil.stderr
            lapor_VALUE['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            hasil=aman_shell(Konfigurasi['ssh_password'], 'echo SSH_NATIVE_PASS')
            (keluaranTeks/'ssh.log').write_bytes(hasil.stderr)
            (keluaranTeks/'ssh-output.txt').write_bytes(hasil.stdout)
            assert hasil.returncode==0 and b'SSH_NATIVE_PASS' in hasil.stdout, (hasil.returncode,hasil.stdout,hasil.stderr)
            lapor_VALUE['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in hasil.stderr, hasil.stderr
            lapor_VALUE['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            hasil=aman_shell(Konfigurasi['ssh_password'], 'cd /example/java; java ContohKeluaran; cd /')
            assert hasil.returncode==0 and 'JAVA keluaranTeks: 안녕하세요 😀'.encode() in hasil.stdout,hasil.stdout
            lapor_VALUE['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            hasil=aman_shell(Konfigurasi['ssh_password'], 'missing_remote_command')
            assert hasil.returncode==127,hasil.returncode
            lapor_VALUE['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            hasil=aman_shell(Konfigurasi['ssh_password'], 'cat /example/java/ContohJendela.java', ('-o', 'RekeyLimit=1K'))
            (keluaranTeks/'ssh-rekey.log').write_bytes(hasil.stderr)
            assert hasil.returncode==0 and 'class ContohJendela'.encode() in hasil.stdout, (hasil.returncode,hasil.stdout,hasil.stderr)
            assert hasil.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, hasil.stderr
            lapor_VALUE['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(shell_port),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            interaktif_sesi=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=lingkungan,start_new_session=True,bufsize=0)
            transkrip=bytearray();pilihan_VALUE=selectors.DefaultSelector();pilihan_VALUE.register(interaktif_sesi.stdout,selectors.EVENT_READ)
            def 대화읽기(show_VALUE):
                tenggat_waktu_VALUE=time.monotonic()+30
                while show_VALUE not in transkrip:
                    if time.monotonic()>tenggat_waktu_VALUE or interaktif_sesi.poll() is not None:raise AssertionError('SSH interactive missing '+repr(show_VALUE)+' '+repr(bytes(transkrip)))
                    for entri_VALUE,_ in pilihan_VALUE.select(.1):
                        조각=entri_VALUE.fileobj.read(4096)
                        if 조각:transkrip.extend(조각)
            try:
                대화읽기(b'shared native console')
                interaktif_sesi.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');interaktif_sesi.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                interaktif_sesi.stdin.write(b'\x04');interaktif_sesi.stdin.flush();나머지,galat=interaktif_sesi.communicate(timeout=15)
                assert interaktif_sesi.returncode==0 and b'PTY allocation request failed' not in galat,(interaktif_sesi.returncode,galat)
                (keluaranTeks/'ssh-interactive.txt').write_bytes(transkrip+나머지)
            finally:
                pilihan_VALUE.close()
                if interaktif_sesi.poll() is None:interaktif_sesi.kill();interaktif_sesi.wait()
            lapor_VALUE['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Sambung, 수):
                data=bytearray()
                while len(data)<수:
                    gugus_VALUE=Sambung.recv(수-len(data))
                    if not gugus_VALUE: raise AssertionError('RFB EOF')
                    data.extend(gugus_VALUE)
                return bytes(data)
            def 화면인증(sandi_VALUE):
                Sambung=socket.create_connection(('127.0.0.5',화면포트),10);Sambung.settimeout(30)
                assert 정확히(Sambung,12)==b'RFB 003.008\n'
                Sambung.sendall(b'RFB 003.008\n');assert 정확히(Sambung,2)==b'\x01\x02'
                Sambung.sendall(b'\x02');tantangan_VALUE=정확히(Sambung,16)
                입력암호=sandi_VALUE.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                Sambung.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(tantangan_VALUE))
                Status_VALUE=struct.unpack('!I',정확히(Sambung,4))[0]
                return Sambung,Status_VALUE
            tidak_sahih_sandi='!' if not Konfigurasi['vnc_password'].startswith('!') else '?'
            Sambung,Status_VALUE=화면인증(tidak_sahih_sandi);assert Status_VALUE==1;Sambung.close();time.sleep(.6)
            lapor_VALUE['checks'].append('VNC incorrect password rejected')
            Sambung,Status_VALUE=화면인증(Konfigurasi['vnc_password']);assert Status_VALUE==0
            with Sambung:
                Sambung.sendall(b'\x01');keadaan_awal=정확히(Sambung,24);너비,높이=struct.unpack('!HH',keadaan_awal[:4]);Nama_2=정확히(Sambung,struct.unpack('!I',keadaan_awal[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==Nama_2
                def 화면(tahapan_langkah=0):
                    Sambung.sendall(struct.pack('!BBHHHH',3,tahapan_langkah,0,0,너비,높이));kepala_VALUE=정확히(Sambung,4);수=struct.unpack('!H',kepala_VALUE[2:])[0];total_VALUE=0
                    gambar_VALUE=bytearray(너비*높이*4)
                    for _ in range(수):
                        koordinat_x,Y_koordinat,영역너비,영역높이,metode_MODE=struct.unpack('!HHHHi',정확히(Sambung,12));assert metode_MODE==0 and koordinat_x+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        elgam=정확히(Sambung,영역너비*영역높이*4);total_VALUE+=len(elgam)
                        for baris_masukan in range(영역높이):gambar_VALUE[((Y_koordinat+baris_masukan)*너비+koordinat_x)*4:((Y_koordinat+baris_masukan)*너비+koordinat_x+영역너비)*4]=elgam[baris_masukan*영역너비*4:(baris_masukan+1)*영역너비*4]
                    if not tahapan_langkah:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(gambar_VALUE),'raw','BGRX').save(str(keluaranTeks/'native-vnc.png'))
                    return 수,total_VALUE
                수,total_VALUE=화면();assert 수>0 and total_VALUE==너비*높이*4
                lapor_VALUE['checks'].append('Native framebuffer RFB full update {} bytes'.format(total_VALUE))
                수,total_VALUE=화면(1);assert total_VALUE<너비*높이*4
                lapor_VALUE['checks'].append('RFB incremental update')
                처음=len(LOG_baris)
                for karakter_VALUE in 'echo VNC_NATIVE_PASS\r':
                    simbol=0xff0d if karakter_VALUE=='\r' else ord(karakter_VALUE)
                    Sambung.sendall(struct.pack('!BBHI',4,1,0,simbol));Sambung.sendall(struct.pack('!BBHI',4,0,0,simbol))
                tunggu_Status(b'VNC_NATIVE_PASS',처음)
                lapor_VALUE['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(simbol,tekan_VALUE=1):Sambung.sendall(struct.pack('!BBHI',4,tekan_VALUE,0,simbol))
                처음=len(LOG_baris)
                for karakter_VALUE in 'echo ':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6)
                for karakter_VALUE in 'gksrmf':글쇠(ord(karakter_VALUE))
                글쇠(0xffc6);글쇠(0xff0d)
                tunggu_Status('\r\n한글\r\n'.encode(),처음)
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
        (keluaranTeks/'serial.log').write_bytes(LOG_baris)
        (keluaranTeks/'report.json').write_text(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2))


if __name__=='__main__': jalankan()
