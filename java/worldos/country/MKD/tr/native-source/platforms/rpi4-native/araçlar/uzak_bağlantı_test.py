#!/usr/bin/env python3
"""fiili_veri OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from yürütmek_komut import işlem_kök, komut
from köprü_3de4fe3a import köprü_3de4fe3a


def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--kernel', type=Path, default=işlem_kök / 'build/kernel8.img')
    ayrıştırıcı_48ee4b1b.add_argument('--access', type=Path, default=işlem_kök / 'build/remote/access.json')
    ayrıştırıcı_48ee4b1b.add_argument('--output', type=Path, default=işlem_kök / 'build/verification/native-remote')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    metinÇıktısı = bağımsız_değişkenler.output
    metinÇıktısı.mkdir(parents=True, exist_ok=True)
    Ayarlar = json.loads(bağımsız_değişkenler.access.read_text())
    Rapor_değer = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(bağımsız_değişkenler.kernel.read_bytes()).hexdigest(), 'checks': []}
    def boş_taşımak():
        with socket.socket() as Bağlan:
            Bağlan.bind(('127.0.0.5', 0))
            return Bağlan.getsockname()[1]
    kabuk_taşımak, 화면포트, Dosya_taşımak = boş_taşımak(), boş_taşımak(), boş_taşımak()
    LOG_KAYIT = bytearray()
    işlem_değer = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, köprü_3de4fe3a(Dosya_taşımak,
                ['tcp:{}:22'.format(kabuk_taşımak), 'tcp:{}:5900'.format(화면포트)], konak_ADRES='127.0.0.5') as köprü_değer_982037b1:
            실행인수 = komut()
            실행인수[실행인수.index('-kernel') + 1] = str(bağımsız_değişkenler.kernel.resolve())
            işlem_değer = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + köprü_değer_982037b1.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    veri = işlem_değer.stdout.read(4096)
                    if not veri: break
                    LOG_KAYIT.extend(veri)
            yazışma_değer = threading.Thread(target=수집, daemon=True)
            yazışma_değer.start()
            def bekleme_durumu(Word_SMS, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Word_SMS not in LOG_KAYIT[처음:]:
                    if time.monotonic()>끝 or işlem_değer.poll() is not None:
                        raise AssertionError('Missing '+repr(Word_SMS)+'\n'+LOG_KAYIT[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            bekleme_durumu(b'jkoros-native> ')
            yardımcı_değer = Path(임시)/'askpass'
            yardımcı_değer.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            yardımcı_değer.chmod(0o700)
            ortam = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(yardımcı_değer), SSH_ASKPASS_REQUIRE='force')
            def SSH(parola_değer, 명령어, Ekleme_girdi=()):
                ortam['JKOROS_TEST_PASSWORD']=parola_değer
                bağımsız_değişkenler=['ssh','-v']+list(Ekleme_girdi)+['-p',str(kabuk_taşımak),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                sonuç=subprocess.run(bağımsız_değişkenler,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=ortam,start_new_session=True,timeout=50)
                return sonuç
            sonuç=SSH('!' + Ayarlar['ssh_password'], 'echo SHOULD_NOT_RUN')
            (metinÇıktısı/'ssh-rejected.log').write_bytes(sonuç.stderr)
            assert sonuç.returncode!=0 and b'Permission denied' in sonuç.stderr and b'SHOULD_NOT_RUN' not in LOG_KAYIT, sonuç.stderr
            Rapor_değer['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            sonuç=SSH(Ayarlar['ssh_password'], 'echo SSH_NATIVE_PASS')
            (metinÇıktısı/'ssh.log').write_bytes(sonuç.stderr)
            (metinÇıktısı/'ssh-output.txt').write_bytes(sonuç.stdout)
            assert sonuç.returncode==0 and b'SSH_NATIVE_PASS' in sonuç.stdout, (sonuç.returncode,sonuç.stdout,sonuç.stderr)
            Rapor_değer['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in sonuç.stderr, sonuç.stderr
            Rapor_değer['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            sonuç=SSH(Ayarlar['ssh_password'], 'cd /example/java; java ÇıktıÖrneği; cd /')
            assert sonuç.returncode==0 and 'JAVA metinÇıktısı: 안녕하세요 😀'.encode() in sonuç.stdout,sonuç.stdout
            Rapor_değer['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            sonuç=SSH(Ayarlar['ssh_password'], 'missing_remote_command')
            assert sonuç.returncode==127,sonuç.returncode
            Rapor_değer['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            sonuç=SSH(Ayarlar['ssh_password'], 'cat /example/java/PencereÖrneği.java', ('-o', 'RekeyLimit=1K'))
            (metinÇıktısı/'ssh-rekey.log').write_bytes(sonuç.stderr)
            assert sonuç.returncode==0 and 'class PencereÖrneği'.encode() in sonuç.stdout, (sonuç.returncode,sonuç.stdout,sonuç.stderr)
            assert sonuç.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, sonuç.stderr
            Rapor_değer['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(kabuk_taşımak),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            devralmak_oturum=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ortam,start_new_session=True,bufsize=0)
            döküm=bytearray();seçim_değer=selectors.DefaultSelector();seçim_değer.register(devralmak_oturum.stdout,selectors.EVENT_READ)
            def 대화읽기(şov_değer):
                son_tarih_değer=time.monotonic()+30
                while şov_değer not in döküm:
                    if time.monotonic()>son_tarih_değer or devralmak_oturum.poll() is not None:raise AssertionError('SSH interactive missing '+repr(şov_değer)+' '+repr(bytes(döküm)))
                    for girdi_değer,_ in seçim_değer.select(.1):
                        parça_değer=girdi_değer.fileobj.read(4096)
                        if parça_değer:döküm.extend(parça_değer)
            try:
                대화읽기(b'shared native console')
                devralmak_oturum.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');devralmak_oturum.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                devralmak_oturum.stdin.write(b'\x04');devralmak_oturum.stdin.flush();나머지,hata=devralmak_oturum.communicate(timeout=15)
                assert devralmak_oturum.returncode==0 and b'PTY allocation request failed' not in hata,(devralmak_oturum.returncode,hata)
                (metinÇıktısı/'ssh-interactive.txt').write_bytes(döküm+나머지)
            finally:
                seçim_değer.close()
                if devralmak_oturum.poll() is None:devralmak_oturum.kill();devralmak_oturum.wait()
            Rapor_değer['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Bağlan, 수):
                veri=bytearray()
                while len(veri)<수:
                    öbek_değer=Bağlan.recv(수-len(veri))
                    if not öbek_değer: raise AssertionError('RFB EOF')
                    veri.extend(öbek_değer)
                return bytes(veri)
            def 화면인증(parola_değer):
                Bağlan=socket.create_connection(('127.0.0.5',화면포트),10);Bağlan.settimeout(30)
                assert 정확히(Bağlan,12)==b'RFB 003.008\n'
                Bağlan.sendall(b'RFB 003.008\n');assert 정확히(Bağlan,2)==b'\x01\x02'
                Bağlan.sendall(b'\x02');görev_değer=정확히(Bağlan,16)
                artış_parola=parola_değer.encode('ascii')[:8].ljust(8, b'\0')
                tuş_malzeme=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in artış_parola)
                Bağlan.sendall(DES.new(tuş_malzeme,DES.MODE_ECB).encrypt(görev_değer))
                Durum_değer=struct.unpack('!I',정확히(Bağlan,4))[0]
                return Bağlan,Durum_değer
            geçersiz_parola='!' if not Ayarlar['vnc_password'].startswith('!') else '?'
            Bağlan,Durum_değer=화면인증(geçersiz_parola);assert Durum_değer==1;Bağlan.close();time.sleep(.6)
            Rapor_değer['checks'].append('VNC incorrect password rejected')
            Bağlan,Durum_değer=화면인증(Ayarlar['vnc_password']);assert Durum_değer==0
            with Bağlan:
                Bağlan.sendall(b'\x01');başlangıç_durumu=정확히(Bağlan,24);너비,높이=struct.unpack('!HH',başlangıç_durumu[:4]);İsim=정확히(Bağlan,struct.unpack('!I',başlangıç_durumu[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==İsim
                def 화면(artış_adım=0):
                    Bağlan.sendall(struct.pack('!BBHHHH',3,artış_adım,0,0,너비,높이));머리=정확히(Bağlan,4);수=struct.unpack('!H',머리[2:])[0];toplam_değer=0
                    çizim_değer=bytearray(너비*높이*4)
                    for _ in range(수):
                        x_koordinatı,Y_koordinat,영역너비,영역높이,metot_mod=struct.unpack('!HHHHi',정확히(Bağlan,12));assert metot_mod==0 and x_koordinatı+영역너비<=너비 and Y_koordinat+영역높이<=높이
                        piksel=정확히(Bağlan,영역너비*영역높이*4);toplam_değer+=len(piksel)
                        for girdi_satırı in range(영역높이):çizim_değer[((Y_koordinat+girdi_satırı)*너비+x_koordinatı)*4:((Y_koordinat+girdi_satırı)*너비+x_koordinatı+영역너비)*4]=piksel[girdi_satırı*영역너비*4:(girdi_satırı+1)*영역너비*4]
                    if not artış_adım:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(çizim_değer),'raw','BGRX').save(str(metinÇıktısı/'native-vnc.png'))
                    return 수,toplam_değer
                수,toplam_değer=화면();assert 수>0 and toplam_değer==너비*높이*4
                Rapor_değer['checks'].append('Native framebuffer RFB full update {} bytes'.format(toplam_değer))
                수,toplam_değer=화면(1);assert toplam_değer<너비*높이*4
                Rapor_değer['checks'].append('RFB incremental update')
                처음=len(LOG_KAYIT)
                for karakter_değer in 'echo VNC_NATIVE_PASS\r':
                    simge=0xff0d if karakter_değer=='\r' else ord(karakter_değer)
                    Bağlan.sendall(struct.pack('!BBHI',4,1,0,simge));Bağlan.sendall(struct.pack('!BBHI',4,0,0,simge))
                bekleme_durumu(b'VNC_NATIVE_PASS',처음)
                Rapor_değer['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def tuş_vuruş(simge,bas_değer=1):Bağlan.sendall(struct.pack('!BBHI',4,bas_değer,0,simge))
                처음=len(LOG_KAYIT)
                for karakter_değer in 'echo ':tuş_vuruş(ord(karakter_değer))
                tuş_vuruş(0xffc6)
                for karakter_değer in 'gksrmf':tuş_vuruş(ord(karakter_değer))
                tuş_vuruş(0xffc6);tuş_vuruş(0xff0d)
                bekleme_durumu('\r\n한글\r\n'.encode(),처음)
                Rapor_değer['checks'].append('Native VNC F9 two-set Hangul composition')
                Bağlan.sendall(struct.pack('!BBHH',5,0,120,100))
                Rapor_değer['checks'].append('VNC pointer input accepted')
            işlem_değer.stdin.write(b'poweroff\n');işlem_değer.stdin.flush();işlem_değer.wait(timeout=15);assert işlem_değer.returncode==0
            Rapor_değer['passed']=True
    finally:
        if işlem_değer and işlem_değer.poll() is None:
            işlem_değer.terminate()
            try: işlem_değer.wait(timeout=5)
            except subprocess.TimeoutExpired: işlem_değer.kill();işlem_değer.wait()
        (metinÇıktısı/'serial.log').write_bytes(LOG_KAYIT)
        (metinÇıktısı/'report.json').write_text(json.dumps(Rapor_değer,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(Rapor_değer,ensure_ascii=False,indent=2))


if __name__=='__main__': çalıştır()
