#!/usr/bin/env python3
"""go_iawn_data QEMU/VNC에서 화면 Maint·경계·ffenestr symud_VALUE·Swing·언어별 그리기를 검사한다."""
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
from bwrdd_gwaith_Gwedd import EXACT_VALUE
from Gweithredu_gorchymyn import prosiect_gwraidd


def 해상도시험(너비, 높이, mesur_llwybr):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); rhif_porth = 임시.getsockname()[1]
    newid_maint_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_gorchymyn.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(rhif_porth), '--resolution', newid_maint_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    dewisydd_a916db4e = selectors.DefaultSelector(); dewisydd_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_rhes = bytearray(); pell_VALUE = None; trosglwyddo_VALUE = None

    def 기다리기(sioe_VALUE, Gweithredu_2=0):
        마감 = time.monotonic() + 60
        while sioe_VALUE not in LOG_rhes[Gweithredu_2:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_rhes or b'PANIC:' in LOG_rhes:
                raise AssertionError(LOG_rhes[Gweithredu_2:].decode('utf-8', 'replace'))
            for digwyddiad, _ in dewisydd_a916db4e.select(.1):
                data = digwyddiad.fileobj.read(65536)
                if data: LOG_rhes.extend(data)
        return LOG_rhes[Gweithredu_2:].decode('utf-8', 'replace')

    def clicio_botwm(symbol, 눌림=True): pell_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def anfon_SMS(Testun):
        Gweithredu_2 = len(LOG_rhes)
        for nod_VALUE in Testun:
            symbol = 0xff0d if nod_VALUE == '\n' else ord(nod_VALUE) if ord(nod_VALUE) < 256 else 0x1000000 | ord(nod_VALUE)
            clicio_botwm(symbol); clicio_botwm(symbol, False)
        return Gweithredu_2

    def cragen(Testun): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', anfon_SMS(Testun+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Ar_i_fyny_safle, 눌림): pell_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ar_i_fyny_safle))

    def clicio_VALUE(가로, Ar_i_fyny_safle): 가리키기(가로, Ar_i_fyny_safle, 1); 가리키기(가로, Ar_i_fyny_safle, 0)

    def map_didau_llun():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 go_iawn_data 너비를 쓴다.
        pell_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        lluniad_VALUE = Image.new('RGB', (너비, 높이)); ardal_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(pell_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                hyd_VALUE = struct.unpack('>I', EXACT_VALUE(pell_VALUE, 7)[3:])[0]; EXACT_VALUE(pell_VALUE, hyd_VALUE); continue
            assert 종류 == 0, 종류
            eitem_COUNT = struct.unpack('>H', EXACT_VALUE(pell_VALUE, 3)[1:])[0]
            for _ in range(eitem_COUNT):
                가로, Ar_i_fyny_safle, 폭, hyd_VALUE, amgodio_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(pell_VALUE, 12))
                assert amgodio_VALUE == 0 and 가로+폭 <= 너비 and Ar_i_fyny_safle+hyd_VALUE <= 높이
                lluniad_VALUE.paste(Image.frombytes('RGB', (폭, hyd_VALUE), EXACT_VALUE(pell_VALUE, 폭*hyd_VALUE*4), 'raw', 'BGRX'), (가로, Ar_i_fyny_safle))
                ardal_VALUE_9285603e += 폭*hyd_VALUE
            if ardal_VALUE_9285603e:
                assert ardal_VALUE_9285603e == 너비*높이, ardal_VALUE_9285603e
                return lluniad_VALUE

    def gwirio_pel(cyfesuryn_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            lluniad_VALUE = map_didau_llun()
            if lluniad_VALUE.getpixel(cyfesuryn_VALUE) == 색: return lluniad_VALUE
            if time.monotonic() > 마감: raise AssertionError((cyfesuryn_VALUE, lluniad_VALUE.getpixel(cyfesuryn_VALUE), 색))

    def Upload_Ffeil(Enw, data): trosglwyddo_VALUE.storbinary('STOR '+Enw, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+newid_maint_SMS+' RGB32').encode() in LOG_rhes
        print('BOOT:', newid_maint_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_rhes).group(1))
        pell_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(pell_VALUE, 12) == b'RFB 003.008\n'; pell_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(pell_VALUE, EXACT_VALUE(pell_VALUE, 1)[0]); pell_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(pell_VALUE, 4) == b'\0'*4; pell_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(pell_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(pell_VALUE, struct.unpack('>I', 초기[20:])[0])
        pell_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        pell_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        gwirio_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        gwirio_pel((너비-568, 높이-360), (32, 80, 144))
        Gweithredu_2 = len(LOG_rhes); clicio_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Gweithredu_2)
        gwirio_pel((너비-568, 높이-360), (24, 32, 48))
        Gweithredu_2 = len(LOG_rhes); clicio_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Gweithredu_2)
        cragen('ftpd start')
        trosglwyddo_VALUE = ftplib.FTP(); trosglwyddo_VALUE.encoding = 'utf-8'; trosglwyddo_VALUE.connect('127.0.0.1', rhif_porth, timeout=20); trosglwyddo_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·clip 밖·빈 사각형을 포함한다.
        FFYNHONNELL = '''#include <화면규약.h>
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
    ysgrifennu_ffeil_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Ffeil('화면시험.c', FFYNHONNELL.encode())
        assert 'exit 0' in cragen('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', anfon_SMS('run /화면시험\n'))
        gwirio_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', anfon_SMS('q'))
        FFYNHONNELL = '''from Cymraeg import 화면크기, 네모그리기, 그림기다리기, Allbwn, system_gwall
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except system_gwall as Gwall:
    assert Gwall.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Allbwn("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Ffeil('화면시험.py', FFYNHONNELL.encode())
        기다리기(b'PYTHON RESOLUTION PASS', anfon_SMS('python /화면시험.py\n'))
        gwirio_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', anfon_SMS('q'))
        FFYNHONNELL = '''import Cymraeg.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new cyflwr_eithriad("Maint");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new cyflwr_eithriad("clip"); }
        catch (annilys_arg_eithriad Gwall) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # eithriad 처리는 lletya javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = mesur_llwybr/'해상도경계시험.java'
        경계원문.write_text(FFYNHONNELL.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(prosiect_gwraidd/'dist/jkoros-native-korean.jar'), '-d', str(mesur_llwybr), str(경계원문)])
        Upload_Ffeil('해상도경계시험.class', (mesur_llwybr/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', anfon_SMS('java 해상도경계시험\n'))
        gwirio_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', anfon_SMS('q'))
        # 게스트 javac의 Cymorth_VALUE 문법으로 Maint ymholiad_VALUE·지우기·다섯 인수 그리기를 컴파일한다.
        FFYNHONNELL = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Cymraeg.자체.화면.너비();
        int 높이=Cymraeg.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Cymraeg.자체.화면.지우기(3153944);
        Cymraeg.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Cymraeg.자체.Allbwn.ysgrifennu_llinell("JAVA RESOLUTION PASS");
        Cymraeg.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Ffeil('해상도시험.java', FFYNHONNELL.encode())
        mesur = cragen('javac 해상도시험.java'); assert 'exit 0' in mesur, mesur
        기다리기(b'JAVA RESOLUTION PASS', anfon_SMS('java 해상도시험\n'))
        gwirio_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', anfon_SMS('q'))
        Upload_Ffeil('스윙시험.class', (mesur_llwybr/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', anfon_SMS('java 스윙시험\n'))
        가로, Ar_i_fyny_safle = (너비-400)//2, (높이-280)//2
        lluniad_VALUE = gwirio_pel((가로, Ar_i_fyny_safle), (32, 80, 144))
        lluniad_VALUE.save(str(mesur_llwybr/(newid_maint_SMS+'.png')))
        Gweithredu_2 = len(LOG_rhes); clicio_VALUE(가로+80, Ar_i_fyny_safle+155)
        기다리기('SWING CLICK Enw'.encode(), Gweithredu_2)
        Gweithredu_2 = len(LOG_rhes); clicio_VALUE(가로+385, Ar_i_fyny_safle+15); 기다리기(b'jkoros-native> ', Gweithredu_2)
        assert 'AFTER_RESOLUTION' in cragen('echo AFTER_RESOLUTION')
        print('PASS:', newid_maint_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if trosglwyddo_VALUE: trosglwyddo_VALUE.close()
        if pell_VALUE: pell_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try: Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_VALUE.kill(); Proses_VALUE.wait()
        dewisydd_a916db4e.close(); Proses_VALUE.stdout.close()
        (mesur_llwybr/(newid_maint_SMS+'.log')).write_bytes(LOG_rhes)


def Gweithredu_2():
    mesur_llwybr = prosiect_gwraidd/'build/verification/resolution'; mesur_llwybr.mkdir(parents=True, exist_ok=True)
    LOG_rhes = {'passed': False, 'kernel_sha256': hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for annilys_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            mesur = subprocess.run(['python3', str(prosiect_gwraidd/'Offer/Gweithredu_gorchymyn.py'), '--resolution', annilys_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert mesur.returncode == 2 and b'--resolution' in mesur.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mesur_llwybr), str(prosiect_gwraidd/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mesur_llwybr); LOG_rhes['resolutions'].append([너비, 높이])
        LOG_rhes.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mesur_llwybr/'report.json').write_text(json.dumps(LOG_rhes, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Gweithredu_2()
