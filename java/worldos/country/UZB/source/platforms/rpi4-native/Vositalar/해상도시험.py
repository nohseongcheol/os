#!/usr/bin/env python3
"""real_ma_lumotlar QEMU/VNC에서 화면 Hajmi·경계·oyna ko_chirmoq_VALUE·Swing·언어별 그리기를 검사한다."""
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
from ishchi_stol_ko_rinish import EXACT_VALUE
from bajarmoq_buyruq import Project_ildiz


def 해상도시험(너비, 높이, o_lchov_yo_l):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    o_lcham_SMS = '{}x{}'.format(너비, 높이)
    Jarayon_VALUE = subprocess.Popen(['python3', str(Project_ildiz/'Vositalar/bajarmoq_buyruq.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', o_lcham_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tanlagich_a916db4e = selectors.DefaultSelector(); tanlagich_a916db4e.register(Jarayon_VALUE.stdout, selectors.EVENT_READ)
    LOG_satr = bytearray(); masofaviy_VALUE = None; uzatish_VALUE = None

    def 기다리기(ko_rsatmoq_VALUE, Bajarish=0):
        마감 = time.monotonic() + 60
        while ko_rsatmoq_VALUE not in LOG_satr[Bajarish:]:
            if time.monotonic() > 마감 or Jarayon_VALUE.poll() is not None or b'HALTED' in LOG_satr or b'PANIC:' in LOG_satr:
                raise AssertionError(LOG_satr[Bajarish:].decode('utf-8', 'replace'))
            for hodisa, _ in tanlagich_a916db4e.select(.1):
                ma_lumotlar = hodisa.fileobj.read(65536)
                if ma_lumotlar: LOG_satr.extend(ma_lumotlar)
        return LOG_satr[Bajarish:].decode('utf-8', 'replace')

    def chertmoq_tugma(ramz, 눌림=True): masofaviy_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ramz))

    def SMS_yuborish(Matn):
        Bajarish = len(LOG_satr)
        for belgi_VALUE in Matn:
            ramz = 0xff0d if belgi_VALUE == '\n' else ord(belgi_VALUE) if ord(belgi_VALUE) < 256 else 0x1000000 | ord(belgi_VALUE)
            chertmoq_tugma(ramz); chertmoq_tugma(ramz, False)
        return Bajarish

    def qobiq(Matn): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_yuborish(Matn+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Vertikal_holat, 눌림): masofaviy_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_holat))

    def chertmoq_VALUE(가로, Vertikal_holat): 가리키기(가로, Vertikal_holat, 1); 가리키기(가로, Vertikal_holat, 0)

    def nuqtali_rasm_rasm():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_ma_lumotlar 너비를 쓴다.
        masofaviy_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        chizish_VALUE = Image.new('RGB', (너비, 높이)); soha_VALUE = 0
        while True:
            종류 = EXACT_VALUE(masofaviy_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uzunlik_VALUE = struct.unpack('>I', EXACT_VALUE(masofaviy_VALUE, 7)[3:])[0]; EXACT_VALUE(masofaviy_VALUE, uzunlik_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(masofaviy_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Vertikal_holat, 폭, uzunlik_VALUE, kodlash_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(masofaviy_VALUE, 12))
                assert kodlash_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_holat+uzunlik_VALUE <= 높이
                chizish_VALUE.paste(Image.frombytes('RGB', (폭, uzunlik_VALUE), EXACT_VALUE(masofaviy_VALUE, 폭*uzunlik_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_holat))
                soha_VALUE += 폭*uzunlik_VALUE
            if soha_VALUE:
                assert soha_VALUE == 너비*높이, soha_VALUE
                return chizish_VALUE

    def chek_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            chizish_VALUE = nuqtali_rasm_rasm()
            if chizish_VALUE.getpixel(koordinat_VALUE) == 색: return chizish_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, chizish_VALUE.getpixel(koordinat_VALUE), 색))

    def uzatmoq_Fayllar(Nomi, ma_lumotlar): uzatish_VALUE.storbinary('STOR '+Nomi, io.BytesIO(ma_lumotlar))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+o_lcham_SMS+' RGB32').encode() in LOG_satr
        print('BOOT:', o_lcham_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_satr).group(1))
        masofaviy_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(masofaviy_VALUE, 12) == b'RFB 003.008\n'; masofaviy_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(masofaviy_VALUE, EXACT_VALUE(masofaviy_VALUE, 1)[0]); masofaviy_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(masofaviy_VALUE, 4) == b'\0'*4; masofaviy_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(masofaviy_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(masofaviy_VALUE, struct.unpack('>I', 초기[20:])[0])
        masofaviy_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        masofaviy_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        chek_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        chek_piksel((너비-568, 높이-360), (32, 80, 144))
        Bajarish = len(LOG_satr); chertmoq_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Bajarish)
        chek_piksel((너비-568, 높이-360), (24, 32, 48))
        Bajarish = len(LOG_satr); chertmoq_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Bajarish)
        qobiq('ftpd start')
        uzatish_VALUE = ftplib.FTP(); uzatish_VALUE.encoding = 'utf-8'; uzatish_VALUE.connect('127.0.0.1', 접속번호, timeout=20); uzatish_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klip 밖·빈 사각형을 포함한다.
        manba = '''#include <화면규약.h>
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
    yozmoq_fayl_ma_lumotlar(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uzatmoq_Fayllar('화면시험.c', manba.encode())
        assert 'exit 0' in qobiq('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_yuborish('run /화면시험\n'))
        chek_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_yuborish('q'))
        manba = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, tizim_xato
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except tizim_xato as Xato:
    assert Xato.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uzatmoq_Fayllar('화면시험.py', manba.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_yuborish('python /화면시험.py\n'))
        chek_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_yuborish('q'))
        manba = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new holat_istisno("Hajmi");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new holat_istisno("klip"); }
        catch (xato_dalil_istisno Xato) { }
        화면.tozalash_kiritish(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # istisno 처리는 tashkilotchi javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = o_lchov_yo_l/'해상도경계시험.java'
        경계원문.write_text(manba.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_ildiz/'dist/jkoros-native-korean.jar'), '-d', str(o_lchov_yo_l), str(경계원문)])
        uzatmoq_Fayllar('해상도경계시험.class', (o_lchov_yo_l/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_yuborish('java 해상도경계시험\n'))
        chek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_yuborish('q'))
        # 게스트 javac의 madad_VALUE 문법으로 Hajmi so_rov_VALUE·tozalash_kiritish·다섯 인수 그리기를 컴파일한다.
        manba = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.tozalash_kiritish(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.yozmoq_satr("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uzatmoq_Fayllar('해상도시험.java', manba.encode())
        o_lchov = qobiq('javac 해상도시험.java'); assert 'exit 0' in o_lchov, o_lchov
        기다리기(b'JAVA RESOLUTION PASS', SMS_yuborish('java 해상도시험\n'))
        chek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_yuborish('q'))
        uzatmoq_Fayllar('스윙시험.class', (o_lchov_yo_l/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_yuborish('java 스윙시험\n'))
        가로, Vertikal_holat = (너비-400)//2, (높이-280)//2
        chizish_VALUE = chek_piksel((가로, Vertikal_holat), (32, 80, 144))
        chizish_VALUE.save(str(o_lchov_yo_l/(o_lcham_SMS+'.png')))
        Bajarish = len(LOG_satr); chertmoq_VALUE(가로+80, Vertikal_holat+155)
        기다리기('SWING CLICK Nomi'.encode(), Bajarish)
        Bajarish = len(LOG_satr); chertmoq_VALUE(가로+385, Vertikal_holat+15); 기다리기(b'jkoros-native> ', Bajarish)
        assert 'AFTER_RESOLUTION' in qobiq('echo AFTER_RESOLUTION')
        print('PASS:', o_lcham_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if uzatish_VALUE: uzatish_VALUE.close()
        if masofaviy_VALUE: masofaviy_VALUE.close()
        if Jarayon_VALUE.poll() is None:
            Jarayon_VALUE.terminate()
            try: Jarayon_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Jarayon_VALUE.kill(); Jarayon_VALUE.wait()
        tanlagich_a916db4e.close(); Jarayon_VALUE.stdout.close()
        (o_lchov_yo_l/(o_lcham_SMS+'.log')).write_bytes(LOG_satr)


def Bajarish():
    o_lchov_yo_l = Project_ildiz/'build/verification/resolution'; o_lchov_yo_l.mkdir(parents=True, exist_ok=True)
    LOG_satr = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for xato_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            o_lchov = subprocess.run(['python3', str(Project_ildiz/'Vositalar/bajarmoq_buyruq.py'), '--resolution', xato_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert o_lchov.returncode == 2 and b'--resolution' in o_lchov.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(o_lchov_yo_l), str(Project_ildiz/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, o_lchov_yo_l); LOG_satr['resolutions'].append([너비, 높이])
        LOG_satr.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (o_lchov_yo_l/'report.json').write_text(json.dumps(LOG_satr, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Bajarish()
