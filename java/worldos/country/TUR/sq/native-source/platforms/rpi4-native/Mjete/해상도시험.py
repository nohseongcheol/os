#!/usr/bin/env python3
"""aktual_të_dhëna QEMU/VNC에서 화면 Madhësi·경계·Dritare lëviz_VALUE·Swing·언어별 그리기를 검사한다."""
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
from desktop_Pamja import EXACT_VALUE
from zbatoj_komandë import Project_rrënjë


def 해상도시험(너비, 높이, llogaritje_shteg):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numri_i_portës = 임시.getsockname()[1]
    ndryshoj_përmasat_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(Project_rrënjë/'Mjete/zbatoj_komandë.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numri_i_portës), '--resolution', ndryshoj_përmasat_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    përzgjedhësi_a916db4e = selectors.DefaultSelector(); përzgjedhësi_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); në_largësi_VALUE = None; transferim_VALUE = None

    def 기다리기(shfaq_VALUE, Ekzekuto=0):
        마감 = time.monotonic() + 60
        while shfaq_VALUE not in LOG_RECORD[Ekzekuto:]:
            if time.monotonic() > 마감 or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Ekzekuto:].decode('utf-8', 'replace'))
            for Ngjarje, _ in përzgjedhësi_a916db4e.select(.1):
                të_dhëna = Ngjarje.fileobj.read(65536)
                if të_dhëna: LOG_RECORD.extend(të_dhëna)
        return LOG_RECORD[Ekzekuto:].decode('utf-8', 'replace')

    def klik_buton(simbol, 눌림=True): në_largësi_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def dërgoj_SMS(Teksti):
        Ekzekuto = len(LOG_RECORD)
        for karakter_VALUE in Teksti:
            simbol = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            klik_buton(simbol); klik_buton(simbol, False)
        return Ekzekuto

    def pasues(Teksti): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', dërgoj_SMS(Teksti+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Vertikal_pozicioni, 눌림): në_largësi_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_pozicioni))

    def klik_VALUE(가로, Vertikal_pozicioni): 가리키기(가로, Vertikal_pozicioni, 1); 가리키기(가로, Vertikal_pozicioni, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 aktual_të_dhëna 너비를 쓴다.
        në_largësi_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        vizatim_VALUE = Image.new('RGB', (너비, 높이)); zonë_VALUE = 0
        while True:
            종류 = EXACT_VALUE(në_largësi_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                gjatësi_VALUE = struct.unpack('>I', EXACT_VALUE(në_largësi_VALUE, 7)[3:])[0]; EXACT_VALUE(në_largësi_VALUE, gjatësi_VALUE); continue
            assert 종류 == 0, 종류
            njësi_COUNT = struct.unpack('>H', EXACT_VALUE(në_largësi_VALUE, 3)[1:])[0]
            for _ in range(njësi_COUNT):
                가로, Vertikal_pozicioni, 폭, gjatësi_VALUE, enkodim_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(në_largësi_VALUE, 12))
                assert enkodim_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_pozicioni+gjatësi_VALUE <= 높이
                vizatim_VALUE.paste(Image.frombytes('RGB', (폭, gjatësi_VALUE), EXACT_VALUE(në_largësi_VALUE, 폭*gjatësi_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_pozicioni))
                zonë_VALUE += 폭*gjatësi_VALUE
            if zonë_VALUE:
                assert zonë_VALUE == 너비*높이, zonë_VALUE
                return vizatim_VALUE

    def çek_pikëz(koordinatë_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            vizatim_VALUE = bitmap_IMAGE()
            if vizatim_VALUE.getpixel(koordinatë_VALUE) == 색: return vizatim_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinatë_VALUE, vizatim_VALUE.getpixel(koordinatë_VALUE), 색))

    def Ngarkim_Skedarët(Emër, të_dhëna): transferim_VALUE.storbinary('STOR '+Emër, io.BytesIO(të_dhëna))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ndryshoj_përmasat_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', ndryshoj_përmasat_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        në_largësi_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(në_largësi_VALUE, 12) == b'RFB 003.008\n'; në_largësi_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(në_largësi_VALUE, EXACT_VALUE(në_largësi_VALUE, 1)[0]); në_largësi_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(në_largësi_VALUE, 4) == b'\0'*4; në_largësi_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(në_largësi_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(në_largësi_VALUE, struct.unpack('>I', 초기[20:])[0])
        në_largësi_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        në_largësi_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        çek_pikëz((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        çek_pikëz((너비-568, 높이-360), (32, 80, 144))
        Ekzekuto = len(LOG_RECORD); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Ekzekuto)
        çek_pikëz((너비-568, 높이-360), (24, 32, 48))
        Ekzekuto = len(LOG_RECORD); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Ekzekuto)
        pasues('ftpd start')
        transferim_VALUE = ftplib.FTP(); transferim_VALUE.encoding = 'utf-8'; transferim_VALUE.connect('127.0.0.1', numri_i_portës, timeout=20); transferim_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·fragment 밖·빈 사각형을 포함한다.
        BURIMI = '''#include <화면규약.h>
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
    shkruaj_skedar_të_dhëna(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Ngarkim_Skedarët('화면시험.c', BURIMI.encode())
        assert 'exit 0' in pasues('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', dërgoj_SMS('run /화면시험\n'))
        çek_pikëz((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', dërgoj_SMS('q'))
        BURIMI = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, sistem_gabim
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_gabim as GABIM:
    assert GABIM.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Ngarkim_Skedarët('화면시험.py', BURIMI.encode())
        기다리기(b'PYTHON RESOLUTION PASS', dërgoj_SMS('python /화면시험.py\n'))
        çek_pikëz((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', dërgoj_SMS('q'))
        BURIMI = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] Argumente) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new status_përjashtim("Madhësi");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new status_përjashtim("fragment"); }
        catch (i_pavlefshëm_argument_përjashtim GABIM) { }
        화면.spastroj_futje(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # përjashtim 처리는 pritës javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = llogaritje_shteg/'해상도경계시험.java'
        경계원문.write_text(BURIMI.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rrënjë/'dist/jkoros-native-korean.jar'), '-d', str(llogaritje_shteg), str(경계원문)])
        Ngarkim_Skedarët('해상도경계시험.class', (llogaritje_shteg/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', dërgoj_SMS('java 해상도경계시험\n'))
        çek_pikëz((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', dërgoj_SMS('q'))
        # 게스트 javac의 Mbështetje_VALUE 문법으로 Madhësi pyetja_VALUE·spastroj_futje·다섯 Argumente 그리기를 컴파일한다.
        BURIMI = '''public class 해상도시험 {
    public static void main(String[] Argumente) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.spastroj_futje(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.shkruaj_linjë("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Ngarkim_Skedarët('해상도시험.java', BURIMI.encode())
        llogaritje = pasues('javac 해상도시험.java'); assert 'exit 0' in llogaritje, llogaritje
        기다리기(b'JAVA RESOLUTION PASS', dërgoj_SMS('java 해상도시험\n'))
        çek_pikëz((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', dërgoj_SMS('q'))
        Ngarkim_Skedarët('스윙시험.class', (llogaritje_shteg/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', dërgoj_SMS('java 스윙시험\n'))
        가로, Vertikal_pozicioni = (너비-400)//2, (높이-280)//2
        vizatim_VALUE = çek_pikëz((가로, Vertikal_pozicioni), (32, 80, 144))
        vizatim_VALUE.save(str(llogaritje_shteg/(ndryshoj_përmasat_SMS+'.png')))
        Ekzekuto = len(LOG_RECORD); klik_VALUE(가로+80, Vertikal_pozicioni+155)
        기다리기('SWING CLICK Emër'.encode(), Ekzekuto)
        Ekzekuto = len(LOG_RECORD); klik_VALUE(가로+385, Vertikal_pozicioni+15); 기다리기(b'jkoros-native> ', Ekzekuto)
        assert 'AFTER_RESOLUTION' in pasues('echo AFTER_RESOLUTION')
        print('PASS:', ndryshoj_përmasat_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transferim_VALUE: transferim_VALUE.close()
        if në_largësi_VALUE: në_largësi_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        përzgjedhësi_a916db4e.close(); Proces_VALUE.stdout.close()
        (llogaritje_shteg/(ndryshoj_përmasat_SMS+'.log')).write_bytes(LOG_RECORD)


def Ekzekuto():
    llogaritje_shteg = Project_rrënjë/'build/verification/resolution'; llogaritje_shteg.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for i_pavlefshëm_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            llogaritje = subprocess.run(['python3', str(Project_rrënjë/'Mjete/zbatoj_komandë.py'), '--resolution', i_pavlefshëm_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert llogaritje.returncode == 2 and b'--resolution' in llogaritje.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(llogaritje_shteg), str(Project_rrënjë/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, llogaritje_shteg); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (llogaritje_shteg/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Ekzekuto()
