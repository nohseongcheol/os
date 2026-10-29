#!/usr/bin/env python3
"""aktual_data QEMU/VNC에서 terminal 모서리 seret_VALUE·pointer·동적 karakter_VALUE slot_entri·Edit_VALUE Isi_VALUE 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from desktop_Tampilan import EXACT_VALUE
from Jalankan_perintah import Tugas_akar


def 창크기시험(너비, 높이, KR_jalur):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); nomor_port = 임시.getsockname()[1]
    ukuran_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Tugas_akar/'alat/Jalankan_perintah.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(nomor_port), '--resolution', ukuran_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pemilih_a916db4e = selectors.DefaultSelector(); pemilih_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_baris = bytearray(); jarak_jauh_VALUE = None; Transfer_VALUE = None; pointer_Tersembunyi=[False]

    def 기다리기(show_VALUE, jalankan=0):
        tenggat_waktu_VALUE = time.monotonic() + 60
        while show_VALUE not in LOG_baris[jalankan:]:
            if time.monotonic() > tenggat_waktu_VALUE or Proses_VALUE.poll() is not None or b'HALTED' in LOG_baris or b'PANIC:' in LOG_baris:
                raise AssertionError(LOG_baris[jalankan:].decode('utf-8', 'replace'))
            for Even, _ in pemilih_a916db4e.select(.1):
                data = Even.fileobj.read(65536)
                if data: LOG_baris.extend(data)
        return LOG_baris[jalankan:].decode('utf-8', 'replace')

    def klik_tombol(simbol, 눌림=True): jarak_jauh_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def kirim_SMS(teks):
        jalankan = len(LOG_baris)
        for karakter_VALUE in teks:
            simbol = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            klik_tombol(simbol); klik_tombol(simbol, False)
        return jalankan

    def shell(teks): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', kirim_SMS(teks+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikal_posisi, 눌림): jarak_jauh_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_posisi))

    def klik_VALUE(가로, Vertikal_posisi): 가리키기(가로, Vertikal_posisi, 1); 가리키기(가로, Vertikal_posisi, 0)

    def bitmap_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 aktual_data 너비를 쓴다.
        jarak_jauh_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        gambar_VALUE = Image.new('RGB', (너비, 높이)); area_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(jarak_jauh_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                panjang_VALUE = struct.unpack('>I', EXACT_VALUE(jarak_jauh_VALUE, 7)[3:])[0]; EXACT_VALUE(jarak_jauh_VALUE, panjang_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(jarak_jauh_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, Vertikal_posisi, 폭, panjang_VALUE, pengodean_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(jarak_jauh_VALUE, 12))
                if pengodean_VALUE == -239:
                    assert 폭==0 and panjang_VALUE==0, 'remote cursor must be hidden'
                    pointer_Tersembunyi[0]=True
                    continue
                assert pengodean_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_posisi+panjang_VALUE <= 높이
                gambar_VALUE.paste(Image.frombytes('RGB', (폭, panjang_VALUE), EXACT_VALUE(jarak_jauh_VALUE, 폭*panjang_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_posisi))
                area_VALUE_9285603e += 폭*panjang_VALUE
            if area_VALUE_9285603e:
                assert area_VALUE_9285603e == 너비*높이, area_VALUE_9285603e
                return gambar_VALUE

    def cek_elgam(koordinat_VALUE, 색):
        tenggat_waktu_VALUE = time.monotonic()+10
        while True:
            gambar_VALUE = bitmap_foto()
            if gambar_VALUE.getpixel(koordinat_VALUE) == 색: return gambar_VALUE
            if time.monotonic() > tenggat_waktu_VALUE: raise AssertionError((koordinat_VALUE, gambar_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_File(Nama_2, data): Transfer_VALUE.storbinary('STOR '+Nama_2, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ukuran_SMS+' RGB32').encode() in LOG_baris
        print('BOOT:', ukuran_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_baris).group(1))
        jarak_jauh_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(jarak_jauh_VALUE, 12) == b'RFB 003.008\n'; jarak_jauh_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(jarak_jauh_VALUE, EXACT_VALUE(jarak_jauh_VALUE, 1)[0]); jarak_jauh_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(jarak_jauh_VALUE, 4) == b'\0'*4; jarak_jauh_VALUE.sendall(b'\x01')
        keadaan_awal = EXACT_VALUE(jarak_jauh_VALUE, 24); assert struct.unpack('>HH', keadaan_awal[:4]) == (너비, 높이)
        EXACT_VALUE(jarak_jauh_VALUE, struct.unpack('>I', keadaan_awal[20:])[0])
        jarak_jauh_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        jarak_jauh_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cek_elgam((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Even,_ in pemilih_a916db4e.select(.02):
                    data=Even.fileobj.read(65536)
                    if data:LOG_baris.extend(data)
        Jendela=[12,48,568,360]
        def periksa_ukuran():
            kolom_VALUE,ROW_VALUE=(Jendela[2]-24)//8,(Jendela[3]-56)//16
            teks=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(kolom_VALUE,ROW_VALUE) in teks,teks
            # aktual_data Jendela 테두리: 단지 Ukuran kueri_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cek_elgam((Jendela[0],Jendela[1]),(32,80,144))
            gambar_VALUE=cek_elgam((Jendela[0]+Jendela[2]-1,Jendela[1]+Jendela[3]-1),(39,49,64))
            return gambar_VALUE
        def 모서리(방향):
            return (Jendela[0]+(3 if 방향 in (1,3) else Jendela[2]-4),Jendela[1]+(3 if 방향<=2 else Jendela[3]-4))
        def ubah_ukuran_seret(방향,차이,tombol=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cek_elgam(흰점,(255,255,255))
            가리키기(가,세,tombol)
            끝가=max(0,min(너비-1,가+차이[0]));mengakhiri_Vertikal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,mengakhiri_Vertikal,tombol);가리키기(끝가,mengakhiri_Vertikal,0);숨고르기()
            if tombol==1:
                LEFT_VALUE,위,폭,panjang_VALUE=Jendela;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+panjang_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+mengakhiri_Vertikal-세))
                else:아래=max(위+216,min(높이,아래+mengakhiri_Vertikal-세))
                Jendela[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        periksa_ukuran();assert pointer_Tersembunyi[0]
        ubah_ukuran_seret(4,(-100,-60),4);periksa_ukuran() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ubah_ukuran_seret(방향,차이);periksa_ukuran()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        kirim_SMS("echo '"+긴글+"'");숨고르기()
        ubah_ukuran_seret(4,(-1000,-1000));assert Jendela[2:]==[360,216]
        ubah_ukuran_seret(4,(너비,높이))
        jalankan=kirim_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),jalankan);periksa_ukuran()
        # vi가 Edit_VALUE 중에 화면 크기를 coba_lagi_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        Transfer_VALUE=ftplib.FTP();Transfer_VALUE.encoding='utf-8';Transfer_VALUE.connect('127.0.0.1',nomor_port,timeout=20);Transfer_VALUE.login()
        기다리기(b'NORMAL',kirim_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',kirim_SMS('i미저장 한글 data\n'));숨고르기()
        ubah_ukuran_seret(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Jendela[3]-56)//16)).encode() in LOG_baris[-4096:]
        kirim_SMS('작은 창에서도 이어 Tulis\n');숨고르기()
        ubah_ukuran_seret(4,(너비,높이))
        kirim_SMS('큰 창에서도 이어 Tulis\n');숨고르기()
        klik_tombol(0xff1b);klik_tombol(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',kirim_SMS(':wq\n'))
        Isi_VALUE=bytearray();Transfer_VALUE.retrbinary('RETR 크기자료.txt',Isi_VALUE.extend)
        assert Isi_VALUE=='미저장 한글 data\n작은 창에서도 이어 Tulis\n큰 창에서도 이어 Tulis\n'.encode(),Isi_VALUE
        periksa_ukuran().save(str(KR_jalur/(ukuran_SMS+'-large.png')))
        # 두 번째 창은 nilai_default Ukuran, coba_lagi_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        jalankan=len(LOG_baris);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',jalankan)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        jalankan=len(LOG_baris);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',jalankan);periksa_ukuran()
        ubah_ukuran_seret(4,(-너비,-높이));periksa_ukuran().save(str(KR_jalur/(ukuran_SMS+'-small.png')))
        # Ukuran ubah_VALUE BACK_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        jalankan=len(LOG_baris);klik_VALUE(Jendela[0]+Jendela[2]-20,Jendela[1]+15);기다리기(b'TERMINAL FOCUS 2',jalankan)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',ukuran_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Transfer_VALUE:Transfer_VALUE.close()
        if jarak_jauh_VALUE:jarak_jauh_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
        pemilih_a916db4e.close();Proses_VALUE.stdout.close();(KR_jalur/(ukuran_SMS+'.log')).write_bytes(LOG_baris)


def jalankan():
    KR_jalur=Tugas_akar/'build/verification/resize';KR_jalur.mkdir(parents=True,exist_ok=True)
    LOG_baris={'passed':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_jalur);LOG_baris['resolutions'].append([너비,높이])
        LOG_baris.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_jalur/'report.json').write_text(json.dumps(LOG_baris,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':jalankan()
