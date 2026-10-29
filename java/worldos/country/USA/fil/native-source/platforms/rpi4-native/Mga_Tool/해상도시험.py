#!/usr/bin/env python3
"""totoo_data QEMU/VNC에서 화면 sukat_82232621·경계·window ilipat_VALUE·Swing·언어별 그리기를 검사한다."""
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
from desktop_View import EXACT_VALUE
from Mag_execute_utos import Project_root


def 해상도시험(너비, 높이, sukat_path):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numero_ng_port = 임시.getsockname()[1]
    sukat_SMS = '{}x{}'.format(너비, 높이)
    Proseso_VALUE = subprocess.Popen(['python3', str(Project_root/'Mga_Tool/Mag_execute_utos.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numero_ng_port), '--resolution', sukat_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tagapili_a916db4e = selectors.DefaultSelector(); tagapili_a916db4e.register(Proseso_VALUE.stdout, selectors.EVENT_READ)
    LOG_hanay = bytearray(); malayuan_VALUE = None; lipat_VALUE = None

    def 기다리기(ipakita_VALUE, run=0):
        마감 = time.monotonic() + 60
        while ipakita_VALUE not in LOG_hanay[run:]:
            if time.monotonic() > 마감 or Proseso_VALUE.poll() is not None or b'HALTED' in LOG_hanay or b'PANIC:' in LOG_hanay:
                raise AssertionError(LOG_hanay[run:].decode('utf-8', 'replace'))
            for kaganapan, _ in tagapili_a916db4e.select(.1):
                data = kaganapan.fileobj.read(65536)
                if data: LOG_hanay.extend(data)
        return LOG_hanay[run:].decode('utf-8', 'replace')

    def magklik_button(simbolo, 눌림=True): malayuan_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolo))

    def magpadala_ng_SMS(SMS):
        run = len(LOG_hanay)
        for karakter_VALUE in SMS:
            simbolo = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            magklik_button(simbolo); magklik_button(simbolo, False)
        return run

    def shell(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', magpadala_ng_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, archive_posisyon, 눌림): malayuan_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, archive_posisyon))

    def magklik_VALUE(가로, archive_posisyon): 가리키기(가로, archive_posisyon, 1); 가리키기(가로, archive_posisyon, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 totoo_data 너비를 쓴다.
        malayuan_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        iginuhit_VALUE = Image.new('RGB', (너비, 높이)); lugar_VALUE = 0
        while True:
            종류 = EXACT_VALUE(malayuan_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                haba_VALUE = struct.unpack('>I', EXACT_VALUE(malayuan_VALUE, 7)[3:])[0]; EXACT_VALUE(malayuan_VALUE, haba_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(malayuan_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, archive_posisyon, 폭, haba_VALUE, pag_encode_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(malayuan_VALUE, 12))
                assert pag_encode_VALUE == 0 and 가로+폭 <= 너비 and archive_posisyon+haba_VALUE <= 높이
                iginuhit_VALUE.paste(Image.frombytes('RGB', (폭, haba_VALUE), EXACT_VALUE(malayuan_VALUE, 폭*haba_VALUE*4), 'raw', 'BGRX'), (가로, archive_posisyon))
                lugar_VALUE += 폭*haba_VALUE
            if lugar_VALUE:
                assert lugar_VALUE == 너비*높이, lugar_VALUE
                return iginuhit_VALUE

    def tseke_pel(coordinate_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            iginuhit_VALUE = bitmap_IMAGE()
            if iginuhit_VALUE.getpixel(coordinate_VALUE) == 색: return iginuhit_VALUE
            if time.monotonic() > 마감: raise AssertionError((coordinate_VALUE, iginuhit_VALUE.getpixel(coordinate_VALUE), 색))

    def upload_Mga_File(pangalan, data): lipat_VALUE.storbinary('STOR '+pangalan, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+sukat_SMS+' RGB32').encode() in LOG_hanay
        print('BOOT:', sukat_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_hanay).group(1))
        malayuan_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(malayuan_VALUE, 12) == b'RFB 003.008\n'; malayuan_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(malayuan_VALUE, EXACT_VALUE(malayuan_VALUE, 1)[0]); malayuan_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(malayuan_VALUE, 4) == b'\0'*4; malayuan_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(malayuan_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(malayuan_VALUE, struct.unpack('>I', 초기[20:])[0])
        malayuan_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        malayuan_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        tseke_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        tseke_pel((너비-568, 높이-360), (32, 80, 144))
        run = len(LOG_hanay); magklik_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', run)
        tseke_pel((너비-568, 높이-360), (24, 32, 48))
        run = len(LOG_hanay); magklik_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', run)
        shell('ftpd start')
        lipat_VALUE = ftplib.FTP(); lipat_VALUE.encoding = 'utf-8'; lipat_VALUE.connect('127.0.0.1', numero_ng_port, timeout=20); lipat_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·clip 밖·빈 사각형을 포함한다.
        pinagmulan = '''#include <화면규약.h>
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
    sumulat_file_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        upload_Mga_File('화면시험.c', pinagmulan.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', magpadala_ng_SMS('run /화면시험\n'))
        tseke_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', magpadala_ng_SMS('q'))
        pinagmulan = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, system_error
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except system_error as error:
    assert error.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        upload_Mga_File('화면시험.py', pinagmulan.encode())
        기다리기(b'PYTHON RESOLUTION PASS', magpadala_ng_SMS('python /화면시험.py\n'))
        tseke_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', magpadala_ng_SMS('q'))
        pinagmulan = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new katayuan_pagbubukod("sukat_82232621");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new katayuan_pagbubukod("clip"); }
        catch (hindi_tama_argumento_pagbubukod error) { }
        화면.burahin_pagpasok(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # pagbubukod 처리는 host javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = sukat_path/'해상도경계시험.java'
        경계원문.write_text(pinagmulan.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_root/'dist/jkoros-native-korean.jar'), '-d', str(sukat_path), str(경계원문)])
        upload_Mga_File('해상도경계시험.class', (sukat_path/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', magpadala_ng_SMS('java 해상도경계시험\n'))
        tseke_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', magpadala_ng_SMS('q'))
        # 게스트 javac의 Suporta_VALUE 문법으로 sukat_82232621 query_VALUE·burahin_pagpasok·다섯 인수 그리기를 컴파일한다.
        pinagmulan = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.burahin_pagpasok(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.sumulat_linya("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        upload_Mga_File('해상도시험.java', pinagmulan.encode())
        sukat = shell('javac 해상도시험.java'); assert 'exit 0' in sukat, sukat
        기다리기(b'JAVA RESOLUTION PASS', magpadala_ng_SMS('java 해상도시험\n'))
        tseke_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', magpadala_ng_SMS('q'))
        upload_Mga_File('스윙시험.class', (sukat_path/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', magpadala_ng_SMS('java 스윙시험\n'))
        가로, archive_posisyon = (너비-400)//2, (높이-280)//2
        iginuhit_VALUE = tseke_pel((가로, archive_posisyon), (32, 80, 144))
        iginuhit_VALUE.save(str(sukat_path/(sukat_SMS+'.png')))
        run = len(LOG_hanay); magklik_VALUE(가로+80, archive_posisyon+155)
        기다리기('SWING CLICK pangalan'.encode(), run)
        run = len(LOG_hanay); magklik_VALUE(가로+385, archive_posisyon+15); 기다리기(b'jkoros-native> ', run)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', sukat_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if lipat_VALUE: lipat_VALUE.close()
        if malayuan_VALUE: malayuan_VALUE.close()
        if Proseso_VALUE.poll() is None:
            Proseso_VALUE.terminate()
            try: Proseso_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proseso_VALUE.kill(); Proseso_VALUE.wait()
        tagapili_a916db4e.close(); Proseso_VALUE.stdout.close()
        (sukat_path/(sukat_SMS+'.log')).write_bytes(LOG_hanay)


def run():
    sukat_path = Project_root/'build/verification/resolution'; sukat_path.mkdir(parents=True, exist_ok=True)
    LOG_hanay = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for hindi_tama_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            sukat = subprocess.run(['python3', str(Project_root/'Mga_Tool/Mag_execute_utos.py'), '--resolution', hindi_tama_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert sukat.returncode == 2 and b'--resolution' in sukat.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(sukat_path), str(Project_root/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, sukat_path); LOG_hanay['resolutions'].append([너비, 높이])
        LOG_hanay.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (sukat_path/'report.json').write_text(json.dumps(LOG_hanay, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': run()
