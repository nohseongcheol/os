#!/usr/bin/env python3
"""sebenar_data QEMU/VNC에서 화면 Saiz·경계·Tetingkap alih_VALUE·Swing·언어별 그리기를 검사한다."""
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
from meja_lihat import EXACT_VALUE
from laksanakan_perintah import projek_akar


def resolusi_ujian(너비, 높이, ukuran_laluan):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); nombor_port = 임시.getsockname()[1]
    saiz_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(projek_akar/'alat/laksanakan_perintah.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(nombor_port), '--resolution', saiz_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_baris = bytearray(); jauh_VALUE = None; pindah_VALUE = None

    def 기다리기(tayang_VALUE, Jalan=0):
        마감 = time.monotonic() + 60
        while tayang_VALUE not in LOG_baris[Jalan:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_baris or b'PANIC:' in LOG_baris:
                raise AssertionError(LOG_baris[Jalan:].decode('utf-8', 'replace'))
            for Peristiwa, _ in 선택기.select(.1):
                data = Peristiwa.fileobj.read(65536)
                if data: LOG_baris.extend(data)
        return LOG_baris[Jalan:].decode('utf-8', 'replace')

    def klik_butang(simbol, 눌림=True): jauh_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def hantar_SMS(Teks):
        Jalan = len(LOG_baris)
        for aksara_VALUE in Teks:
            simbol = 0xff0d if aksara_VALUE == '\n' else ord(aksara_VALUE) if ord(aksara_VALUE) < 256 else 0x1000000 | ord(aksara_VALUE)
            klik_butang(simbol); klik_butang(simbol, False)
        return Jalan

    def cangkerang(Teks): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', hantar_SMS(Teks+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Menegak_jawatan, 눌림): jauh_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Menegak_jawatan))

    def klik_VALUE(가로, Menegak_jawatan): 가리키기(가로, Menegak_jawatan, 1); 가리키기(가로, Menegak_jawatan, 0)

    def peta_bit_imej():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 sebenar_data 너비를 쓴다.
        jauh_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        lukisan_VALUE = Image.new('RGB', (너비, 높이)); bidang_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(jauh_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                kepanjangan_VALUE = struct.unpack('>I', EXACT_VALUE(jauh_VALUE, 7)[3:])[0]; EXACT_VALUE(jauh_VALUE, kepanjangan_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(jauh_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, Menegak_jawatan, 폭, kepanjangan_VALUE, pengekodan_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(jauh_VALUE, 12))
                assert pengekodan_VALUE == 0 and 가로+폭 <= 너비 and Menegak_jawatan+kepanjangan_VALUE <= 높이
                lukisan_VALUE.paste(Image.frombytes('RGB', (폭, kepanjangan_VALUE), EXACT_VALUE(jauh_VALUE, 폭*kepanjangan_VALUE*4), 'raw', 'BGRX'), (가로, Menegak_jawatan))
                bidang_VALUE_9285603e += 폭*kepanjangan_VALUE
            if bidang_VALUE_9285603e:
                assert bidang_VALUE_9285603e == 너비*높이, bidang_VALUE_9285603e
                return lukisan_VALUE

    def cek_pel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            lukisan_VALUE = peta_bit_imej()
            if lukisan_VALUE.getpixel(koordinat_VALUE) == 색: return lukisan_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, lukisan_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Fail(Nama, data): pindah_VALUE.storbinary('STOR '+Nama, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+saiz_SMS+' RGB32').encode() in LOG_baris
        print('BOOT:', saiz_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_baris).group(1))
        jauh_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(jauh_VALUE, 12) == b'RFB 003.008\n'; jauh_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(jauh_VALUE, EXACT_VALUE(jauh_VALUE, 1)[0]); jauh_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(jauh_VALUE, 4) == b'\0'*4; jauh_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(jauh_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(jauh_VALUE, struct.unpack('>I', 초기[20:])[0])
        jauh_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        jauh_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cek_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        cek_pel((너비-568, 높이-360), (32, 80, 144))
        Jalan = len(LOG_baris); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Jalan)
        cek_pel((너비-568, 높이-360), (24, 32, 48))
        Jalan = len(LOG_baris); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Jalan)
        cangkerang('ftpd start')
        pindah_VALUE = ftplib.FTP(); pindah_VALUE.encoding = 'utf-8'; pindah_VALUE.connect('127.0.0.1', nombor_port, timeout=20); pindah_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 tukar_VALUE·klip 밖·빈 사각형을 포함한다.
        SUMBER = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Lukis_segi_empat_tepat(너비,높이,0,0,0)) return 2;
    if(Lukis_segi_empat_tepat(너비,높이-1,1,1,0)!=-22) return 3;
    if(Lukis_segi_empat_tepat(너비-1,높이,1,1,0)!=-22) return 4;
    if(Lukis_segi_empat_tepat(-1,0,1,1,0)!=-22) return 5;
    if(Lukis_segi_empat_tepat(0,0,-1,1,0)!=-22) return 6;
    if(Lukis_segi_empat_tepat(너비-1,높이-1,1,1,0x332211)) return 7;
    tulis_fail_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fail('화면시험.c', SUMBER.encode())
        assert 'exit 0' in cangkerang('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', hantar_SMS('run /화면시험\n'))
        cek_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', hantar_SMS('q'))
        SUMBER = '''from Melayu import 화면크기, Lukis_segi_empat_tepat, 그림기다리기, 출력, sistem_ralat
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Lukis_segi_empat_tepat(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_ralat as RALAT:
    assert RALAT.INDEX == 22
Lukis_segi_empat_tepat(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fail('화면시험.py', SUMBER.encode())
        기다리기(b'PYTHON RESOLUTION PASS', hantar_SMS('python /화면시험.py\n'))
        cek_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', hantar_SMS('q'))
        SUMBER = '''import Melayu.Asli.*;
public class resolusi_ujian {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new status_pengecualian("Saiz");
        try { 화면.segi_empat_tepat(너비,높이-1,1,1,0); throw new status_pengecualian("klip"); }
        catch (tak_sah_argumen_pengecualian RALAT) { }
        화면.padam_pemasukan(0x302018);
        화면.segi_empat_tepat(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # pengecualian 처리는 hos javac 결과를 Asli JVM에 올려 검사한다.
        경계원문 = ukuran_laluan/'해상도경계시험.java'
        경계원문.write_text(SUMBER.replace('class resolusi_ujian', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projek_akar/'dist/jkoros-native-korean.jar'), '-d', str(ukuran_laluan), str(경계원문)])
        Upload_Fail('해상도경계시험.class', (ukuran_laluan/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', hantar_SMS('java 해상도경계시험\n'))
        cek_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', hantar_SMS('q'))
        # 게스트 javac의 Sokongan_VALUE 문법으로 Saiz pertanyaan_VALUE·padam_pemasukan·다섯 인수 그리기를 컴파일한다.
        SUMBER = '''public class resolusi_ujian {
    public static void main(String[] 인수) {
        int 너비=Melayu.Asli.화면.너비();
        int 높이=Melayu.Asli.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Melayu.Asli.화면.padam_pemasukan(3153944);
        Melayu.Asli.화면.segi_empat_tepat(너비-1,높이-1,1,1,10061943);
        Melayu.Asli.출력.tulis_baris("JAVA RESOLUTION PASS");
        Melayu.Asli.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fail('resolusi_ujian.java', SUMBER.encode())
        ukuran = cangkerang('javac resolusi_ujian.java'); assert 'exit 0' in ukuran, ukuran
        기다리기(b'JAVA RESOLUTION PASS', hantar_SMS('java resolusi_ujian\n'))
        cek_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', hantar_SMS('q'))
        Upload_Fail('스윙시험.class', (ukuran_laluan/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', hantar_SMS('java 스윙시험\n'))
        가로, Menegak_jawatan = (너비-400)//2, (높이-280)//2
        lukisan_VALUE = cek_pel((가로, Menegak_jawatan), (32, 80, 144))
        lukisan_VALUE.save(str(ukuran_laluan/(saiz_SMS+'.png')))
        Jalan = len(LOG_baris); klik_VALUE(가로+80, Menegak_jawatan+155)
        기다리기('SWING CLICK Nama'.encode(), Jalan)
        Jalan = len(LOG_baris); klik_VALUE(가로+385, Menegak_jawatan+15); 기다리기(b'jkoros-native> ', Jalan)
        assert 'AFTER_RESOLUTION' in cangkerang('echo AFTER_RESOLUTION')
        print('PASS:', saiz_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if pindah_VALUE: pindah_VALUE.close()
        if jauh_VALUE: jauh_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_VALUE.kill(); Proses_VALUE.wait()
        선택기.close(); Proses_VALUE.stdout.close()
        (ukuran_laluan/(saiz_SMS+'.log')).write_bytes(LOG_baris)


def Jalan():
    ukuran_laluan = projek_akar/'build/verification/resolution'; ukuran_laluan.mkdir(parents=True, exist_ok=True)
    LOG_baris = {'passed': False, 'kernel_sha256': hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for tak_sah_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ukuran = subprocess.run(['python3', str(projek_akar/'alat/laksanakan_perintah.py'), '--resolution', tak_sah_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ukuran.returncode == 2 and b'--resolution' in ukuran.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ukuran_laluan), str(projek_akar/'ujian/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            resolusi_ujian(너비, 높이, ukuran_laluan); LOG_baris['resolutions'].append([너비, 높이])
        LOG_baris.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ukuran_laluan/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Jalan()
