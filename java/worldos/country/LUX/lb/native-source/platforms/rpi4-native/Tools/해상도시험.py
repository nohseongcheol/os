#!/usr/bin/env python3
"""aktuell_Daten QEMU/VNC에서 화면 d_Gréisst_veränneren·경계·Fënster verréckelen_VALUE·Swing·언어별 그리기를 검사한다."""
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
from Desktop_Vue import EXACT_VALUE
from ausféieren_Befeel import projezéieren_Racinn


def 해상도시험(너비, 높이, Mooss_Wee):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    d_Gréisst_veränneren_SMS = '{}x{}'.format(너비, 높이)
    Prozess_VALUE = subprocess.Popen(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', d_Gréisst_veränneren_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selekteur_a916db4e = selectors.DefaultSelector(); Selekteur_a916db4e.register(Prozess_VALUE.stdout, selectors.EVENT_READ)
    LOG_Rei = bytearray(); extern_VALUE = None; Transfer_VALUE = None

    def 기다리기(Show_VALUE, Laf=0):
        마감 = time.monotonic() + 60
        while Show_VALUE not in LOG_Rei[Laf:]:
            if time.monotonic() > 마감 or Prozess_VALUE.poll() is not None or b'HALTED' in LOG_Rei or b'PANIC:' in LOG_Rei:
                raise AssertionError(LOG_Rei[Laf:].decode('utf-8', 'replace'))
            for Evenement, _ in Selekteur_a916db4e.select(.1):
                Daten = Evenement.fileobj.read(65536)
                if Daten: LOG_Rei.extend(Daten)
        return LOG_Rei[Laf:].decode('utf-8', 'replace')

    def klicken_Tast(Symbol, 눌림=True): extern_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, Symbol))

    def SMS_schécken(SMS):
        Laf = len(LOG_Rei)
        for Zeechen_VALUE in SMS:
            Symbol = 0xff0d if Zeechen_VALUE == '\n' else ord(Zeechen_VALUE) if ord(Zeechen_VALUE) < 256 else 0x1000000 | ord(Zeechen_VALUE)
            klicken_Tast(Symbol); klicken_Tast(Symbol, False)
        return Laf

    def Shell(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_schécken(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Vertikal_positionéieren, 눌림): extern_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_positionéieren))

    def klicken_VALUE(가로, Vertikal_positionéieren): 가리키기(가로, Vertikal_positionéieren, 1); 가리키기(가로, Vertikal_positionéieren, 0)

    def Bitmap_Bild():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 aktuell_Daten 너비를 쓴다.
        extern_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        Zeechnung_VALUE = Image.new('RGB', (너비, 높이)); Beräich_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(extern_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                Längt_VALUE = struct.unpack('>I', EXACT_VALUE(extern_VALUE, 7)[3:])[0]; EXACT_VALUE(extern_VALUE, Längt_VALUE); continue
            assert 종류 == 0, 종류
            Element_COUNT = struct.unpack('>H', EXACT_VALUE(extern_VALUE, 3)[1:])[0]
            for _ in range(Element_COUNT):
                가로, Vertikal_positionéieren, 폭, Längt_VALUE, Codéierung_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(extern_VALUE, 12))
                assert Codéierung_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_positionéieren+Längt_VALUE <= 높이
                Zeechnung_VALUE.paste(Image.frombytes('RGB', (폭, Längt_VALUE), EXACT_VALUE(extern_VALUE, 폭*Längt_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_positionéieren))
                Beräich_VALUE_9285603e += 폭*Längt_VALUE
            if Beräich_VALUE_9285603e:
                assert Beräich_VALUE_9285603e == 너비*높이, Beräich_VALUE_9285603e
                return Zeechnung_VALUE

    def Scheck_Pel(Coordonnée_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            Zeechnung_VALUE = Bitmap_Bild()
            if Zeechnung_VALUE.getpixel(Coordonnée_VALUE) == 색: return Zeechnung_VALUE
            if time.monotonic() > 마감: raise AssertionError((Coordonnée_VALUE, Zeechnung_VALUE.getpixel(Coordonnée_VALUE), 색))

    def eroplueden_Fichieren(Numm, Daten): Transfer_VALUE.storbinary('STOR '+Numm, io.BytesIO(Daten))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+d_Gréisst_veränneren_SMS+' RGB32').encode() in LOG_Rei
        print('BOOT:', d_Gréisst_veränneren_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_Rei).group(1))
        extern_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(extern_VALUE, 12) == b'RFB 003.008\n'; extern_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(extern_VALUE, EXACT_VALUE(extern_VALUE, 1)[0]); extern_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(extern_VALUE, 4) == b'\0'*4; extern_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(extern_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(extern_VALUE, struct.unpack('>I', 초기[20:])[0])
        extern_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        extern_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        Scheck_Pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        Scheck_Pel((너비-568, 높이-360), (32, 80, 144))
        Laf = len(LOG_Rei); klicken_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Laf)
        Scheck_Pel((너비-568, 높이-360), (24, 32, 48))
        Laf = len(LOG_Rei); klicken_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Laf)
        Shell('ftpd start')
        Transfer_VALUE = ftplib.FTP(); Transfer_VALUE.encoding = 'utf-8'; Transfer_VALUE.connect('127.0.0.1', 접속번호, timeout=20); Transfer_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·Clip 밖·빈 사각형을 포함한다.
        Quell = '''#include <화면규약.h>
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
    schreiwen_Fichier_Daten(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        eroplueden_Fichieren('화면시험.c', Quell.encode())
        assert 'exit 0' in Shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_schécken('run /화면시험\n'))
        Scheck_Pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_schécken('q'))
        Quell = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, System_Feeler
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except System_Feeler as Feeler:
    assert Feeler.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        eroplueden_Fichieren('화면시험.py', Quell.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_schécken('python /화면시험.py\n'))
        Scheck_Pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_schécken('q'))
        Quell = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("d_Gréisst_veränneren");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("Clip"); }
        catch (잘못된인수예외 Feeler) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 Host javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = Mooss_Wee/'해상도경계시험.java'
        경계원문.write_text(Quell.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projezéieren_Racinn/'dist/jkoros-native-korean.jar'), '-d', str(Mooss_Wee), str(경계원문)])
        eroplueden_Fichieren('해상도경계시험.class', (Mooss_Wee/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_schécken('java 해상도경계시험\n'))
        Scheck_Pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_schécken('q'))
        # 게스트 javac의 Support_VALUE 문법으로 d_Gréisst_veränneren Requête_VALUE·지우기·다섯 인수 그리기를 컴파일한다.
        Quell = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.schreiwen_Zeil("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        eroplueden_Fichieren('해상도시험.java', Quell.encode())
        Mooss = Shell('javac 해상도시험.java'); assert 'exit 0' in Mooss, Mooss
        기다리기(b'JAVA RESOLUTION PASS', SMS_schécken('java 해상도시험\n'))
        Scheck_Pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_schécken('q'))
        eroplueden_Fichieren('스윙시험.class', (Mooss_Wee/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_schécken('java 스윙시험\n'))
        가로, Vertikal_positionéieren = (너비-400)//2, (높이-280)//2
        Zeechnung_VALUE = Scheck_Pel((가로, Vertikal_positionéieren), (32, 80, 144))
        Zeechnung_VALUE.save(str(Mooss_Wee/(d_Gréisst_veränneren_SMS+'.png')))
        Laf = len(LOG_Rei); klicken_VALUE(가로+80, Vertikal_positionéieren+155)
        기다리기('SWING CLICK Numm'.encode(), Laf)
        Laf = len(LOG_Rei); klicken_VALUE(가로+385, Vertikal_positionéieren+15); 기다리기(b'jkoros-native> ', Laf)
        assert 'AFTER_RESOLUTION' in Shell('echo AFTER_RESOLUTION')
        print('PASS:', d_Gréisst_veränneren_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Transfer_VALUE: Transfer_VALUE.close()
        if extern_VALUE: extern_VALUE.close()
        if Prozess_VALUE.poll() is None:
            Prozess_VALUE.terminate()
            try: Prozess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Prozess_VALUE.kill(); Prozess_VALUE.wait()
        Selekteur_a916db4e.close(); Prozess_VALUE.stdout.close()
        (Mooss_Wee/(d_Gréisst_veränneren_SMS+'.log')).write_bytes(LOG_Rei)


def Laf():
    Mooss_Wee = projezéieren_Racinn/'build/verification/resolution'; Mooss_Wee.mkdir(parents=True, exist_ok=True)
    LOG_Rei = {'passed': False, 'kernel_sha256': hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ongëlteg_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            Mooss = subprocess.run(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'), '--resolution', ongëlteg_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert Mooss.returncode == 2 and b'--resolution' in Mooss.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Mooss_Wee), str(projezéieren_Racinn/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, Mooss_Wee); LOG_Rei['resolutions'].append([너비, 높이])
        LOG_Rei.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (Mooss_Wee/'report.json').write_text(json.dumps(LOG_Rei, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Laf()
