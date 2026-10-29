#!/usr/bin/env python3
"""aktual_data QEMU/VNC에서 화면 Ukuran·경계·Jendela gerak_VALUE·Swing·언어별 그리기를 검사한다."""
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


def 해상도시험(너비, 높이, KR_jalur):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); nomor_port = 임시.getsockname()[1]
    ukuran_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Tugas_akar/'alat/Jalankan_perintah.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(nomor_port), '--resolution', ukuran_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pemilih_a916db4e = selectors.DefaultSelector(); pemilih_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_baris = bytearray(); jarak_jauh_VALUE = None; Transfer_VALUE = None

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

    def shell(teks): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', kirim_SMS(teks+'; echo __RESOLUTION_DONE__\n'))

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
        jarak_jauh_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cek_elgam((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        cek_elgam((너비-568, 높이-360), (32, 80, 144))
        jalankan = len(LOG_baris); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', jalankan)
        cek_elgam((너비-568, 높이-360), (24, 32, 48))
        jalankan = len(LOG_baris); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', jalankan)
        shell('ftpd start')
        Transfer_VALUE = ftplib.FTP(); Transfer_VALUE.encoding = 'utf-8'; Transfer_VALUE.connect('127.0.0.1', nomor_port, timeout=20); Transfer_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klip 밖·빈 사각형을 포함한다.
        kodeSumber = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Gambar_persegi(너비,높이,0,0,0)) return 2;
    if(Gambar_persegi(너비,높이-1,1,1,0)!=-22) return 3;
    if(Gambar_persegi(너비-1,높이,1,1,0)!=-22) return 4;
    if(Gambar_persegi(-1,0,1,1,0)!=-22) return 5;
    if(Gambar_persegi(0,0,-1,1,0)!=-22) return 6;
    if(Gambar_persegi(너비-1,높이-1,1,1,0x332211)) return 7;
    tulis_file_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_File('화면시험.c', kodeSumber.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', kirim_SMS('run /화면시험\n'))
        cek_elgam((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', kirim_SMS('q'))
        kodeSumber = '''from Indonesia import 화면크기, Gambar_persegi, 그림기다리기, keluaranTeks, sistem_kesalahan
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Gambar_persegi(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_kesalahan as galat:
    assert galat.INDEX == 22
Gambar_persegi(너비-1, 높이-1, 1, 1, 0x665544)
keluaranTeks("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_File('화면시험.py', kodeSumber.encode())
        기다리기(b'PYTHON RESOLUTION PASS', kirim_SMS('python /화면시험.py\n'))
        cek_elgam((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', kirim_SMS('q'))
        kodeSumber = '''import Indonesia.Asli.*;
public class 해상도시험 {
    public static void main(String[] argumen) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Status_pengecualian("Ukuran");
        try { 화면.persegi(너비,높이-1,1,1,0); throw new Status_pengecualian("klip"); }
        catch (tidak_sahih_argumen_pengecualian galat) { }
        화면.hapus_entri_c8dbc399(0x302018);
        화면.persegi(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # pengecualian 처리는 host javac 결과를 Asli JVM에 올려 검사한다.
        경계원문 = KR_jalur/'해상도경계시험.java'
        경계원문.write_text(kodeSumber.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Tugas_akar/'dist/jkoros-native-korean.jar'), '-d', str(KR_jalur), str(경계원문)])
        Upload_File('해상도경계시험.class', (KR_jalur/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', kirim_SMS('java 해상도경계시험\n'))
        cek_elgam((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', kirim_SMS('q'))
        # 게스트 javac의 dukung_VALUE 문법으로 Ukuran kueri_VALUE·hapus_entri_c8dbc399·다섯 argumen 그리기를 컴파일한다.
        kodeSumber = '''public class 해상도시험 {
    public static void main(String[] argumen) {
        int 너비=Indonesia.Asli.화면.너비();
        int 높이=Indonesia.Asli.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Indonesia.Asli.화면.hapus_entri_c8dbc399(3153944);
        Indonesia.Asli.화면.persegi(너비-1,높이-1,1,1,10061943);
        Indonesia.Asli.keluaranTeks.tulis_baris("JAVA RESOLUTION PASS");
        Indonesia.Asli.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_File('해상도시험.java', kodeSumber.encode())
        hasil = shell('javac 해상도시험.java'); assert 'exit 0' in hasil, hasil
        기다리기(b'JAVA RESOLUTION PASS', kirim_SMS('java 해상도시험\n'))
        cek_elgam((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', kirim_SMS('q'))
        Upload_File('스윙시험.class', (KR_jalur/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', kirim_SMS('java 스윙시험\n'))
        가로, Vertikal_posisi = (너비-400)//2, (높이-280)//2
        gambar_VALUE = cek_elgam((가로, Vertikal_posisi), (32, 80, 144))
        gambar_VALUE.save(str(KR_jalur/(ukuran_SMS+'.png')))
        jalankan = len(LOG_baris); klik_VALUE(가로+80, Vertikal_posisi+155)
        기다리기('SWING CLICK Nama_2'.encode(), jalankan)
        jalankan = len(LOG_baris); klik_VALUE(가로+385, Vertikal_posisi+15); 기다리기(b'jkoros-native> ', jalankan)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', ukuran_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Transfer_VALUE: Transfer_VALUE.close()
        if jarak_jauh_VALUE: jarak_jauh_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_VALUE.kill(); Proses_VALUE.wait()
        pemilih_a916db4e.close(); Proses_VALUE.stdout.close()
        (KR_jalur/(ukuran_SMS+'.log')).write_bytes(LOG_baris)


def jalankan():
    KR_jalur = Tugas_akar/'build/verification/resolution'; KR_jalur.mkdir(parents=True, exist_ok=True)
    LOG_baris = {'passed': False, 'kernel_sha256': hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for tidak_sahih_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            hasil = subprocess.run(['python3', str(Tugas_akar/'alat/Jalankan_perintah.py'), '--resolution', tidak_sahih_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert hasil.returncode == 2 and b'--resolution' in hasil.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_jalur), str(Tugas_akar/'pengujian/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, KR_jalur); LOG_baris['resolutions'].append([너비, 높이])
        LOG_baris.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_jalur/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': jalankan()
