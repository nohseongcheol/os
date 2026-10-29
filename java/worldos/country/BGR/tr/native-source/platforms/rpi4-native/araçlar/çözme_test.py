#!/usr/bin/env python3
"""fiili_veri QEMU/VNC에서 화면 Boyut·sınır_değer·Pencere taşımak_değer_83b651b8·Swing·언어별 그리기를 검사한다."""
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
from Masaüstü_Görünüm import ÖZDEŞ_değer
from yürütmek_komut import işlem_kök


def çözme_test(너비, 높이, KR_yol):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); bağlantı_noktası_numarası = 임시.getsockname()[1]
    boyutlandırmak_SMS = '{}x{}'.format(너비, 높이)
    işlem_değer = subprocess.Popen(['python3', str(işlem_kök/'araçlar/yürütmek_komut.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(bağlantı_noktası_numarası), '--resolution', boyutlandırmak_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector(); seçici_a916db4e.register(işlem_değer.stdout, selectors.EVENT_READ)
    LOG_KAYIT = bytearray(); uzak_değer = None; devir_değer = None

    def 기다리기(şov_değer, çalıştır=0):
        son_tarih_değer = time.monotonic() + 60
        while şov_değer not in LOG_KAYIT[çalıştır:]:
            if time.monotonic() > son_tarih_değer or işlem_değer.poll() is not None or b'HALTED' in LOG_KAYIT or b'PANIC:' in LOG_KAYIT:
                raise AssertionError(LOG_KAYIT[çalıştır:].decode('utf-8', 'replace'))
            for Olay, _ in seçici_a916db4e.select(.1):
                veri = Olay.fileobj.read(65536)
                if veri: LOG_KAYIT.extend(veri)
        return LOG_KAYIT[çalıştır:].decode('utf-8', 'replace')

    def tık_düğme(simge, 눌림=True): uzak_değer.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simge))

    def SMS_gönderme(metin):
        çalıştır = len(LOG_KAYIT)
        for karakter_değer in metin:
            simge = 0xff0d if karakter_değer == '\n' else ord(karakter_değer) if ord(karakter_değer) < 256 else 0x1000000 | ord(karakter_değer)
            tık_düğme(simge); tık_düğme(simge, False)
        return çalıştır

    def kabuk(metin): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_gönderme(metin+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Dikey_konum, 눌림): uzak_değer.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Dikey_konum))

    def tık_değer(가로, Dikey_konum): 가리키기(가로, Dikey_konum, 1); 가리키기(가로, Dikey_konum, 0)

    def bit_eşlem_RESİM():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 fiili_veri 너비를 쓴다.
        uzak_değer.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        çizim_değer = Image.new('RGB', (너비, 높이)); alan_değer_9285603e = 0
        while True:
            Tip_değer = ÖZDEŞ_değer(uzak_değer, 1)[0]
            if Tip_değer == 2: continue
            if Tip_değer == 3:
                süre_değer = struct.unpack('>I', ÖZDEŞ_değer(uzak_değer, 7)[3:])[0]; ÖZDEŞ_değer(uzak_değer, süre_değer); continue
            assert Tip_değer == 0, Tip_değer
            öğe_BAĞ_DEĞ_SAY = struct.unpack('>H', ÖZDEŞ_değer(uzak_değer, 3)[1:])[0]
            for _ in range(öğe_BAĞ_DEĞ_SAY):
                가로, Dikey_konum, 폭, süre_değer, kodlama_değer = struct.unpack('>HHHHi', ÖZDEŞ_değer(uzak_değer, 12))
                assert kodlama_değer == 0 and 가로+폭 <= 너비 and Dikey_konum+süre_değer <= 높이
                çizim_değer.paste(Image.frombytes('RGB', (폭, süre_değer), ÖZDEŞ_değer(uzak_değer, 폭*süre_değer*4), 'raw', 'BGRX'), (가로, Dikey_konum))
                alan_değer_9285603e += 폭*süre_değer
            if alan_değer_9285603e:
                assert alan_değer_9285603e == 너비*높이, alan_değer_9285603e
                return çizim_değer

    def çek_piksel(koordinat_değer, 색):
        son_tarih_değer = time.monotonic()+10
        while True:
            çizim_değer = bit_eşlem_RESİM()
            if çizim_değer.getpixel(koordinat_değer) == 색: return çizim_değer
            if time.monotonic() > son_tarih_değer: raise AssertionError((koordinat_değer, çizim_değer.getpixel(koordinat_değer), 색))

    def yükle_Dosyalar(İsim, veri): devir_değer.storbinary('STOR '+İsim, io.BytesIO(veri))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+boyutlandırmak_SMS+' RGB32').encode() in LOG_KAYIT
        print('BOOT:', boyutlandırmak_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_KAYIT).group(1))
        uzak_değer = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert ÖZDEŞ_değer(uzak_değer, 12) == b'RFB 003.008\n'; uzak_değer.sendall(b'RFB 003.008\n')
        assert 1 in ÖZDEŞ_değer(uzak_değer, ÖZDEŞ_değer(uzak_değer, 1)[0]); uzak_değer.sendall(b'\x01')
        assert ÖZDEŞ_değer(uzak_değer, 4) == b'\0'*4; uzak_değer.sendall(b'\x01')
        başlangıç_durumu = ÖZDEŞ_değer(uzak_değer, 24); assert struct.unpack('>HH', başlangıç_durumu[:4]) == (너비, 높이)
        ÖZDEŞ_değer(uzak_değer, struct.unpack('>I', başlangıç_durumu[20:])[0])
        uzak_değer.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzak_değer.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        çek_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 hak 아래까지 이동한다. Önceki_öğe 640×480 sınır_değer 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        çek_piksel((너비-568, 높이-360), (32, 80, 144))
        çalıştır = len(LOG_KAYIT); tık_değer(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', çalıştır)
        çek_piksel((너비-568, 높이-360), (24, 32, 48))
        çalıştır = len(LOG_KAYIT); tık_değer(80, 16); 기다리기(b'TERMINAL FOCUS 1', çalıştır)
        kabuk('ftpd start')
        devir_değer = ftplib.FTP(); devir_değer.encoding = 'utf-8'; devir_değer.connect('127.0.0.1', bağlantı_noktası_numarası, timeout=20); devir_değer.login()
        # C sınır_değer 검사는 32비트 unsigned Negatif_değer ÇEVİR_değer·klip 밖·빈 사각형을 포함한다.
        kaynakKod = '''#include <화면규약.h>
#include <Dosya_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Çizim_dikdörtgen(너비,높이,0,0,0)) return 2;
    if(Çizim_dikdörtgen(너비,높이-1,1,1,0)!=-22) return 3;
    if(Çizim_dikdörtgen(너비-1,높이,1,1,0)!=-22) return 4;
    if(Çizim_dikdörtgen(-1,0,1,1,0)!=-22) return 5;
    if(Çizim_dikdörtgen(0,0,-1,1,0)!=-22) return 6;
    if(Çizim_dikdörtgen(너비-1,높이-1,1,1,0x332211)) return 7;
    yazma_Dosya_veri(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        yükle_Dosyalar('화면시험.c', kaynakKod.encode())
        assert 'exit 0' in kabuk('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_gönderme('run /화면시험\n'))
        çek_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_gönderme('q'))
        kaynakKod = '''from Türkçe import 화면크기, Çizim_dikdörtgen, 그림기다리기, metinÇıktısı, sistem_hatası
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Çizim_dikdörtgen(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_hatası as hata:
    assert hata.Dizin == 22
Çizim_dikdörtgen(너비-1, 높이-1, 1, 1, 0x665544)
metinÇıktısı("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        yükle_Dosyalar('화면시험.py', kaynakKod.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_gönderme('python /화면시험.py\n'))
        çek_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_gönderme('q'))
        kaynakKod = '''import Türkçe.Öz.*;
public class çözme_test {
    public static void main(String[] bağımsız_değişkenler) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Durum_özel_durum("Boyut");
        try { 화면.dikdörtgen(너비,높이-1,1,1,0); throw new Durum_özel_durum("klip"); }
        catch (geçersiz_bağımsız_değişken_özel_durum hata) { }
        화면.silmek_girdi(0x302018);
        화면.dikdörtgen(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # özel_durum 처리는 konak javac 결과를 Öz JVM에 올려 검사한다.
        sınır_kaynak = KR_yol/'해상도경계시험.java'
        sınır_kaynak.write_text(kaynakKod.replace('class çözme_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(işlem_kök/'dist/jkoros-native-korean.jar'), '-d', str(KR_yol), str(sınır_kaynak)])
        yükle_Dosyalar('해상도경계시험.class', (KR_yol/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_gönderme('java 해상도경계시험\n'))
        çek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_gönderme('q'))
        # 게스트 javac의 Destek_değer 문법으로 Boyut sorgu_değer·silmek_girdi·다섯 bağımsız_değişkenler 그리기를 컴파일한다.
        kaynakKod = '''public class çözme_test {
    public static void main(String[] bağımsız_değişkenler) {
        int 너비=Türkçe.Öz.화면.너비();
        int 높이=Türkçe.Öz.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Türkçe.Öz.화면.silmek_girdi(3153944);
        Türkçe.Öz.화면.dikdörtgen(너비-1,높이-1,1,1,10061943);
        Türkçe.Öz.metinÇıktısı.yazma_hat("JAVA RESOLUTION PASS");
        Türkçe.Öz.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        yükle_Dosyalar('çözme_test.java', kaynakKod.encode())
        sonuç = kabuk('javac çözme_test.java'); assert 'exit 0' in sonuç, sonuç
        기다리기(b'JAVA RESOLUTION PASS', SMS_gönderme('java çözme_test\n'))
        çek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_gönderme('q'))
        yükle_Dosyalar('Swing_test.class', (KR_yol/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', SMS_gönderme('java Swing_test\n'))
        가로, Dikey_konum = (너비-400)//2, (높이-280)//2
        çizim_değer = çek_piksel((가로, Dikey_konum), (32, 80, 144))
        çizim_değer.save(str(KR_yol/(boyutlandırmak_SMS+'.png')))
        çalıştır = len(LOG_KAYIT); tık_değer(가로+80, Dikey_konum+155)
        기다리기('SWING CLICK İsim'.encode(), çalıştır)
        çalıştır = len(LOG_KAYIT); tık_değer(가로+385, Dikey_konum+15); 기다리기(b'jkoros-native> ', çalıştır)
        assert 'AFTER_RESOLUTION' in kabuk('echo AFTER_RESOLUTION')
        print('PASS:', boyutlandırmak_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if devir_değer: devir_değer.close()
        if uzak_değer: uzak_değer.close()
        if işlem_değer.poll() is None:
            işlem_değer.terminate()
            try: işlem_değer.wait(timeout=8)
            except subprocess.TimeoutExpired: işlem_değer.kill(); işlem_değer.wait()
        seçici_a916db4e.close(); işlem_değer.stdout.close()
        (KR_yol/(boyutlandırmak_SMS+'.log')).write_bytes(LOG_KAYIT)


def çalıştır():
    KR_yol = işlem_kök/'build/verification/resolution'; KR_yol.mkdir(parents=True, exist_ok=True)
    LOG_KAYIT = {'passed': False, 'kernel_sha256': hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for geçersiz_değer in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            sonuç = subprocess.run(['python3', str(işlem_kök/'araçlar/yürütmek_komut.py'), '--resolution', geçersiz_değer], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert sonuç.returncode == 2 and b'--resolution' in sonuç.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_yol), str(işlem_kök/'sınamalar/자바/Swing_test.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            çözme_test(너비, 높이, KR_yol); LOG_KAYIT['resolutions'].append([너비, 높이])
        LOG_KAYIT.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_yol/'report.json').write_text(json.dumps(LOG_KAYIT, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': çalıştır()
