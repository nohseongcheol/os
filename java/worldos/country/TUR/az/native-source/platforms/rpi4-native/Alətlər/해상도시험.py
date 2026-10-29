#!/usr/bin/env python3
"""faktiki_verilənlər QEMU/VNC에서 화면 Böyüklük·경계·pəncərə hərəkət_etdir_VALUE·Swing·언어별 그리기를 검사한다."""
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
from iş_masası_baxmaq import EXACT_VALUE
from icra_etmək_əmr import Project_kök


def 해상도시험(너비, 높이, ölçü_yol):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ölçünü_dəyişmək_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Project_kök/'Alətlər/icra_etmək_əmr.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ölçünü_dəyişmək_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector(); seçici_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_yaz = bytearray(); uzaq_VALUE = None; ötürmə_VALUE = None

    def 기다리기(göstərmək_VALUE, İcra_Et=0):
        마감 = time.monotonic() + 60
        while göstərmək_VALUE not in LOG_yaz[İcra_Et:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_yaz or b'PANIC:' in LOG_yaz:
                raise AssertionError(LOG_yaz[İcra_Et:].decode('utf-8', 'replace'))
            for hadisə, _ in seçici_a916db4e.select(.1):
                verilənlər = hadisə.fileobj.read(65536)
                if verilənlər: LOG_yaz.extend(verilənlər)
        return LOG_yaz[İcra_Et:].decode('utf-8', 'replace')

    def klikləmə_düymə(simvol, 눌림=True): uzaq_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simvol))

    def SMS_göndər(Mətn):
        İcra_Et = len(LOG_yaz)
        for simvol_VALUE_068c2631 in Mətn:
            simvol = 0xff0d if simvol_VALUE_068c2631 == '\n' else ord(simvol_VALUE_068c2631) if ord(simvol_VALUE_068c2631) < 256 else 0x1000000 | ord(simvol_VALUE_068c2631)
            klikləmə_düymə(simvol); klikləmə_düymə(simvol, False)
        return İcra_Et

    def örtük(Mətn): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_göndər(Mətn+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Şaquli_yerinə_qoymaq, 눌림): uzaq_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Şaquli_yerinə_qoymaq))

    def klikləmə_VALUE(가로, Şaquli_yerinə_qoymaq): 가리키기(가로, Şaquli_yerinə_qoymaq, 1); 가리키기(가로, Şaquli_yerinə_qoymaq, 0)

    def nöqtəli_təsvir_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktiki_verilənlər 너비를 쓴다.
        uzaq_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        rəsm_VALUE = Image.new('RGB', (너비, 높이)); sahə_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(uzaq_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uzunluq_VALUE = struct.unpack('>I', EXACT_VALUE(uzaq_VALUE, 7)[3:])[0]; EXACT_VALUE(uzaq_VALUE, uzunluq_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(uzaq_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Şaquli_yerinə_qoymaq, 폭, uzunluq_VALUE, kodlaşdırma_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(uzaq_VALUE, 12))
                assert kodlaşdırma_VALUE == 0 and 가로+폭 <= 너비 and Şaquli_yerinə_qoymaq+uzunluq_VALUE <= 높이
                rəsm_VALUE.paste(Image.frombytes('RGB', (폭, uzunluq_VALUE), EXACT_VALUE(uzaq_VALUE, 폭*uzunluq_VALUE*4), 'raw', 'BGRX'), (가로, Şaquli_yerinə_qoymaq))
                sahə_VALUE_9285603e += 폭*uzunluq_VALUE
            if sahə_VALUE_9285603e:
                assert sahə_VALUE_9285603e == 너비*높이, sahə_VALUE_9285603e
                return rəsm_VALUE

    def çek_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            rəsm_VALUE = nöqtəli_təsvir_IMAGE()
            if rəsm_VALUE.getpixel(koordinat_VALUE) == 색: return rəsm_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, rəsm_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Fayllar(Ad, verilənlər): ötürmə_VALUE.storbinary('STOR '+Ad, io.BytesIO(verilənlər))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ölçünü_dəyişmək_SMS+' RGB32').encode() in LOG_yaz
        print('BOOT:', ölçünü_dəyişmək_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_yaz).group(1))
        uzaq_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(uzaq_VALUE, 12) == b'RFB 003.008\n'; uzaq_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(uzaq_VALUE, EXACT_VALUE(uzaq_VALUE, 1)[0]); uzaq_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(uzaq_VALUE, 4) == b'\0'*4; uzaq_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(uzaq_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(uzaq_VALUE, struct.unpack('>I', 초기[20:])[0])
        uzaq_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzaq_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        çek_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        çek_piksel((너비-568, 높이-360), (32, 80, 144))
        İcra_Et = len(LOG_yaz); klikləmə_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', İcra_Et)
        çek_piksel((너비-568, 높이-360), (24, 32, 48))
        İcra_Et = len(LOG_yaz); klikləmə_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', İcra_Et)
        örtük('ftpd start')
        ötürmə_VALUE = ftplib.FTP(); ötürmə_VALUE.encoding = 'utf-8'; ötürmə_VALUE.connect('127.0.0.1', 접속번호, timeout=20); ötürmə_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klip 밖·빈 사각형을 포함한다.
        QAYNAQ = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(네모그리기(너비,높이,0,0,0)) return 2;
    if(네모그리기(너비,높이-1,1,1,0)!=-22) return 3;
    if(네모그리기(너비-1,높이,1,1,0)!=-22) return 4;
    if(네모그리기(-1,0,1,1,0)!=-22) return 5;
    if(네모그리기(0,0,-1,1,0)!=-22) return 6;
    if(네모그리기(너비-1,높이-1,1,1,0x332211)) return 7;
    yazmaq_fayl_verilənlər(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fayllar('화면시험.c', QAYNAQ.encode())
        assert 'exit 0' in örtük('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_göndər('run /화면시험\n'))
        çek_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_göndər('q'))
        QAYNAQ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, sistem_səhv
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_səhv as XƏTA:
    assert XƏTA.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fayllar('화면시험.py', QAYNAQ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_göndər('python /화면시험.py\n'))
        çek_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_göndər('q'))
        QAYNAQ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new vəziyyət_istisna("Böyüklük");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new vəziyyət_istisna("klip"); }
        catch (yanlış_arqument_istisna XƏTA) { }
        화면.silmək_daxiletmə_c8dbc399(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # istisna 처리는 host javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ölçü_yol/'해상도경계시험.java'
        경계원문.write_text(QAYNAQ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_kök/'dist/jkoros-native-korean.jar'), '-d', str(ölçü_yol), str(경계원문)])
        Upload_Fayllar('해상도경계시험.class', (ölçü_yol/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_göndər('java 해상도경계시험\n'))
        çek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_göndər('q'))
        # 게스트 javac의 Dəstək_VALUE 문법으로 Böyüklük sorğu_VALUE·silmək_daxiletmə_c8dbc399·다섯 인수 그리기를 컴파일한다.
        QAYNAQ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.silmək_daxiletmə_c8dbc399(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.yazmaq_xətt("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fayllar('해상도시험.java', QAYNAQ.encode())
        ölçü = örtük('javac 해상도시험.java'); assert 'exit 0' in ölçü, ölçü
        기다리기(b'JAVA RESOLUTION PASS', SMS_göndər('java 해상도시험\n'))
        çek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_göndər('q'))
        Upload_Fayllar('스윙시험.class', (ölçü_yol/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_göndər('java 스윙시험\n'))
        가로, Şaquli_yerinə_qoymaq = (너비-400)//2, (높이-280)//2
        rəsm_VALUE = çek_piksel((가로, Şaquli_yerinə_qoymaq), (32, 80, 144))
        rəsm_VALUE.save(str(ölçü_yol/(ölçünü_dəyişmək_SMS+'.png')))
        İcra_Et = len(LOG_yaz); klikləmə_VALUE(가로+80, Şaquli_yerinə_qoymaq+155)
        기다리기('SWING CLICK Ad'.encode(), İcra_Et)
        İcra_Et = len(LOG_yaz); klikləmə_VALUE(가로+385, Şaquli_yerinə_qoymaq+15); 기다리기(b'jkoros-native> ', İcra_Et)
        assert 'AFTER_RESOLUTION' in örtük('echo AFTER_RESOLUTION')
        print('PASS:', ölçünü_dəyişmək_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ötürmə_VALUE: ötürmə_VALUE.close()
        if uzaq_VALUE: uzaq_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_VALUE.kill(); Proses_VALUE.wait()
        seçici_a916db4e.close(); Proses_VALUE.stdout.close()
        (ölçü_yol/(ölçünü_dəyişmək_SMS+'.log')).write_bytes(LOG_yaz)


def İcra_Et():
    ölçü_yol = Project_kök/'build/verification/resolution'; ölçü_yol.mkdir(parents=True, exist_ok=True)
    LOG_yaz = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for yanlış_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ölçü = subprocess.run(['python3', str(Project_kök/'Alətlər/icra_etmək_əmr.py'), '--resolution', yanlış_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ölçü.returncode == 2 and b'--resolution' in ölçü.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ölçü_yol), str(Project_kök/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ölçü_yol); LOG_yaz['resolutions'].append([너비, 높이])
        LOG_yaz.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ölçü_yol/'report.json').write_text(json.dumps(LOG_yaz, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': İcra_Et()
