#!/usr/bin/env python3
"""werklik_data QEMU/VNC에서 화면 Grootte·경계·venster skuif_VALUE·Swing·언어별 그리기를 검사한다."""
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
from werkskerm_bekyk import EXACT_VALUE
from uitvoer_bevel import Project_wortel


def 해상도시험(너비, 높이, maatreël_pad):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    verstel_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', verstel_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selekteerder_a916db4e = selectors.DefaultSelector(); selekteerder_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_ry = bytearray(); afstands_VALUE = None; oordra_VALUE = None

    def 기다리기(wys_VALUE, Loop=0):
        마감 = time.monotonic() + 60
        while wys_VALUE not in LOG_ry[Loop:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_ry or b'PANIC:' in LOG_ry:
                raise AssertionError(LOG_ry[Loop:].decode('utf-8', 'replace'))
            for gebeurtenis, _ in selekteerder_a916db4e.select(.1):
                data = gebeurtenis.fileobj.read(65536)
                if data: LOG_ry.extend(data)
        return LOG_ry[Loop:].decode('utf-8', 'replace')

    def klik_knoppie(simbool, 눌림=True): afstands_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbool))

    def stuur_SMS(Teks):
        Loop = len(LOG_ry)
        for karakter_VALUE in Teks:
            simbool = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            klik_knoppie(simbool); klik_knoppie(simbool, False)
        return Loop

    def dop(Teks): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', stuur_SMS(Teks+'; echo __RESOLUTION_DONE__\n'))

    def p_at(가로, Vertikaal_plaas, 눌림): afstands_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikaal_plaas))

    def klik_VALUE(가로, Vertikaal_plaas): p_at(가로, Vertikaal_plaas, 1); p_at(가로, Vertikaal_plaas, 0)

    def bispatroon_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 werklik_data 너비를 쓴다.
        afstands_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tekening_VALUE = Image.new('RGB', (너비, 높이)); area_VALUE = 0
        while True:
            종류 = EXACT_VALUE(afstands_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengte_VALUE = struct.unpack('>I', EXACT_VALUE(afstands_VALUE, 7)[3:])[0]; EXACT_VALUE(afstands_VALUE, lengte_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(afstands_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, Vertikaal_plaas, 폭, lengte_VALUE, enkodering_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(afstands_VALUE, 12))
                assert enkodering_VALUE == 0 and 가로+폭 <= 너비 and Vertikaal_plaas+lengte_VALUE <= 높이
                tekening_VALUE.paste(Image.frombytes('RGB', (폭, lengte_VALUE), EXACT_VALUE(afstands_VALUE, 폭*lengte_VALUE*4), 'raw', 'BGRX'), (가로, Vertikaal_plaas))
                area_VALUE += 폭*lengte_VALUE
            if area_VALUE:
                assert area_VALUE == 너비*높이, area_VALUE
                return tekening_VALUE

    def tjek_pieksel(koördinaat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            tekening_VALUE = bispatroon_foto()
            if tekening_VALUE.getpixel(koördinaat_VALUE) == 색: return tekening_VALUE
            if time.monotonic() > 마감: raise AssertionError((koördinaat_VALUE, tekening_VALUE.getpixel(koördinaat_VALUE), 색))

    def oplaai_Lêers(Naam, data): oordra_VALUE.storbinary('STOR '+Naam, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+verstel_SMS+' RGB32').encode() in LOG_ry
        print('BOOT:', verstel_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ry).group(1))
        afstands_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(afstands_VALUE, 12) == b'RFB 003.008\n'; afstands_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(afstands_VALUE, EXACT_VALUE(afstands_VALUE, 1)[0]); afstands_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(afstands_VALUE, 4) == b'\0'*4; afstands_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(afstands_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(afstands_VALUE, struct.unpack('>I', 초기[20:])[0])
        afstands_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        afstands_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        tjek_pieksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        p_at(40, 60, 1); p_at(너비-568+28, 높이-360+12, 1); p_at(너비-568+28, 높이-360+12, 0)
        tjek_pieksel((너비-568, 높이-360), (32, 80, 144))
        Loop = len(LOG_ry); klik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Loop)
        tjek_pieksel((너비-568, 높이-360), (24, 32, 48))
        Loop = len(LOG_ry); klik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Loop)
        dop('ftpd start')
        oordra_VALUE = ftplib.FTP(); oordra_VALUE.encoding = 'utf-8'; oordra_VALUE.connect('127.0.0.1', 접속번호, timeout=20); oordra_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·snit 밖·빈 사각형을 포함한다.
        Bron = '''#include <화면규약.h>
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
    skryf_lêer_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        oplaai_Lêers('화면시험.c', Bron.encode())
        assert 'exit 0' in dop('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', stuur_SMS('run /화면시험\n'))
        tjek_pieksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', stuur_SMS('q'))
        Bron = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, Afvoer, stelsel_fout
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except stelsel_fout as Fout:
    assert Fout.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Afvoer("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        oplaai_Lêers('화면시험.py', Bron.encode())
        기다리기(b'PYTHON RESOLUTION PASS', stuur_SMS('python /화면시험.py\n'))
        tjek_pieksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', stuur_SMS('q'))
        Bron = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new stand_uitsondering("Grootte");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new stand_uitsondering("snit"); }
        catch (ongeldig_argument_uitsondering Fout) { }
        화면.vee_uit_inskrywing(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # uitsondering 처리는 hou javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = maatreël_pad/'해상도경계시험.java'
        경계원문.write_text(Bron.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_wortel/'dist/jkoros-native-korean.jar'), '-d', str(maatreël_pad), str(경계원문)])
        oplaai_Lêers('해상도경계시험.class', (maatreël_pad/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', stuur_SMS('java 해상도경계시험\n'))
        tjek_pieksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', stuur_SMS('q'))
        # 게스트 javac의 Bystand_VALUE 문법으로 Grootte navraag_VALUE·vee_uit_inskrywing·다섯 인수 그리기를 컴파일한다.
        Bron = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.vee_uit_inskrywing(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.Afvoer.skryf_lyn("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        oplaai_Lêers('해상도시험.java', Bron.encode())
        maatreël = dop('javac 해상도시험.java'); assert 'exit 0' in maatreël, maatreël
        기다리기(b'JAVA RESOLUTION PASS', stuur_SMS('java 해상도시험\n'))
        tjek_pieksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', stuur_SMS('q'))
        oplaai_Lêers('스윙시험.class', (maatreël_pad/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', stuur_SMS('java 스윙시험\n'))
        가로, Vertikaal_plaas = (너비-400)//2, (높이-280)//2
        tekening_VALUE = tjek_pieksel((가로, Vertikaal_plaas), (32, 80, 144))
        tekening_VALUE.save(str(maatreël_pad/(verstel_SMS+'.png')))
        Loop = len(LOG_ry); klik_VALUE(가로+80, Vertikaal_plaas+155)
        기다리기('SWING CLICK Naam'.encode(), Loop)
        Loop = len(LOG_ry); klik_VALUE(가로+385, Vertikaal_plaas+15); 기다리기(b'jkoros-native> ', Loop)
        assert 'AFTER_RESOLUTION' in dop('echo AFTER_RESOLUTION')
        print('PASS:', verstel_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if oordra_VALUE: oordra_VALUE.close()
        if afstands_VALUE: afstands_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_VALUE.kill(); Proses_VALUE.wait()
        selekteerder_a916db4e.close(); Proses_VALUE.stdout.close()
        (maatreël_pad/(verstel_SMS+'.log')).write_bytes(LOG_ry)


def Loop():
    maatreël_pad = Project_wortel/'build/verification/resolution'; maatreël_pad.mkdir(parents=True, exist_ok=True)
    LOG_ry = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ongeldig_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            maatreël = subprocess.run(['python3', str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'), '--resolution', ongeldig_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert maatreël.returncode == 2 and b'--resolution' in maatreël.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(maatreël_pad), str(Project_wortel/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, maatreël_pad); LOG_ry['resolutions'].append([너비, 높이])
        LOG_ry.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (maatreël_pad/'report.json').write_text(json.dumps(LOG_ry, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Loop()
