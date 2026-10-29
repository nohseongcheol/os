#!/usr/bin/env python3
"""dearbh_dàta QEMU/VNC에서 화면 atharraich_am_meud·경계·uinneag gluais_VALUE·Swing·언어별 그리기를 검사한다."""
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
from deasg_seall import EXACT_VALUE
from gnìomhaich_àithne import tilg_freumh


def 해상도시험(너비, 높이, tomhas_slighe):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    atharraich_am_meud_SMS = '{}x{}'.format(너비, 높이)
    Pròiseas_VALUE = subprocess.Popen(['python3', str(tilg_freumh/'innealan/gnìomhaich_àithne.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', atharraich_am_meud_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnaichear_a916db4e = selectors.DefaultSelector(); roghnaichear_a916db4e.register(Pròiseas_VALUE.stdout, selectors.EVENT_READ)
    LOG_ràgh = bytearray(); cian_VALUE = None; tar_chur_VALUE = None

    def 기다리기(show_VALUE, ruith=0):
        마감 = time.monotonic() + 60
        while show_VALUE not in LOG_ràgh[ruith:]:
            if time.monotonic() > 마감 or Pròiseas_VALUE.poll() is not None or b'HALTED' in LOG_ràgh or b'PANIC:' in LOG_ràgh:
                raise AssertionError(LOG_ràgh[ruith:].decode('utf-8', 'replace'))
            for tachartas, _ in roghnaichear_a916db4e.select(.1):
                dàta = tachartas.fileobj.read(65536)
                if dàta: LOG_ràgh.extend(dàta)
        return LOG_ràgh[ruith:].decode('utf-8', 'replace')

    def briog_putan(samhla, 눌림=True): cian_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, samhla))

    def cuir_SMS(SMS):
        ruith = len(LOG_ràgh)
        for caractar_VALUE in SMS:
            samhla = 0xff0d if caractar_VALUE == '\n' else ord(caractar_VALUE) if ord(caractar_VALUE) < 256 else 0x1000000 | ord(caractar_VALUE)
            briog_putan(samhla); briog_putan(samhla, False)
        return ruith

    def slige(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', cuir_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, inghearach_suidhich, 눌림): cian_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, inghearach_suidhich))

    def briog_VALUE(가로, inghearach_suidhich): 가리키기(가로, inghearach_suidhich, 1); 가리키기(가로, inghearach_suidhich, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dearbh_dàta 너비를 쓴다.
        cian_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tarraing_VALUE = Image.new('RGB', (너비, 높이)); raon_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(cian_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                faid_VALUE = struct.unpack('>I', EXACT_VALUE(cian_VALUE, 7)[3:])[0]; EXACT_VALUE(cian_VALUE, faid_VALUE); continue
            assert 종류 == 0, 종류
            nì_COUNT = struct.unpack('>H', EXACT_VALUE(cian_VALUE, 3)[1:])[0]
            for _ in range(nì_COUNT):
                가로, inghearach_suidhich, 폭, faid_VALUE, còdachadh_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(cian_VALUE, 12))
                assert còdachadh_VALUE == 0 and 가로+폭 <= 너비 and inghearach_suidhich+faid_VALUE <= 높이
                tarraing_VALUE.paste(Image.frombytes('RGB', (폭, faid_VALUE), EXACT_VALUE(cian_VALUE, 폭*faid_VALUE*4), 'raw', 'BGRX'), (가로, inghearach_suidhich))
                raon_VALUE_9285603e += 폭*faid_VALUE
            if raon_VALUE_9285603e:
                assert raon_VALUE_9285603e == 너비*높이, raon_VALUE_9285603e
                return tarraing_VALUE

    def seic_pel(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            tarraing_VALUE = bitmap_IMAGE()
            if tarraing_VALUE.getpixel(좌표) == 색: return tarraing_VALUE
            if time.monotonic() > 마감: raise AssertionError((좌표, tarraing_VALUE.getpixel(좌표), 색))

    def luchdaich_suas_faidhlichean(Ainm, dàta): tar_chur_VALUE.storbinary('STOR '+Ainm, io.BytesIO(dàta))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+atharraich_am_meud_SMS+' RGB32').encode() in LOG_ràgh
        print('BOOT:', atharraich_am_meud_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ràgh).group(1))
        cian_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(cian_VALUE, 12) == b'RFB 003.008\n'; cian_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cian_VALUE, EXACT_VALUE(cian_VALUE, 1)[0]); cian_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(cian_VALUE, 4) == b'\0'*4; cian_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(cian_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(cian_VALUE, struct.unpack('>I', 초기[20:])[0])
        cian_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        cian_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        seic_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        seic_pel((너비-568, 높이-360), (32, 80, 144))
        ruith = len(LOG_ràgh); briog_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ruith)
        seic_pel((너비-568, 높이-360), (24, 32, 48))
        ruith = len(LOG_ràgh); briog_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', ruith)
        slige('ftpd start')
        tar_chur_VALUE = ftplib.FTP(); tar_chur_VALUE.encoding = 'utf-8'; tar_chur_VALUE.connect('127.0.0.1', 접속번호, timeout=20); tar_chur_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·cliop 밖·빈 사각형을 포함한다.
        tùs = '''#include <화면규약.h>
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
    sgrìobh_faidhle_dàta(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        luchdaich_suas_faidhlichean('화면시험.c', tùs.encode())
        assert 'exit 0' in slige('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', cuir_SMS('run /화면시험\n'))
        seic_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', cuir_SMS('q'))
        tùs = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, siostam_mearachd
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except siostam_mearachd as Mearachd:
    assert Mearachd.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        luchdaich_suas_faidhlichean('화면시험.py', tùs.encode())
        기다리기(b'PYTHON RESOLUTION PASS', cuir_SMS('python /화면시험.py\n'))
        seic_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', cuir_SMS('q'))
        tùs = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("atharraich_am_meud");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("cliop"); }
        catch (잘못된인수예외 Mearachd) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 òstair javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = tomhas_slighe/'해상도경계시험.java'
        경계원문.write_text(tùs.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(tilg_freumh/'dist/jkoros-native-korean.jar'), '-d', str(tomhas_slighe), str(경계원문)])
        luchdaich_suas_faidhlichean('해상도경계시험.class', (tomhas_slighe/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', cuir_SMS('java 해상도경계시험\n'))
        seic_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', cuir_SMS('q'))
        # 게스트 javac의 taic_VALUE 문법으로 atharraich_am_meud ceist_VALUE·지우기·다섯 인수 그리기를 컴파일한다.
        tùs = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.sgrìobh_loidhne("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        luchdaich_suas_faidhlichean('해상도시험.java', tùs.encode())
        tomhas = slige('javac 해상도시험.java'); assert 'exit 0' in tomhas, tomhas
        기다리기(b'JAVA RESOLUTION PASS', cuir_SMS('java 해상도시험\n'))
        seic_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', cuir_SMS('q'))
        luchdaich_suas_faidhlichean('스윙시험.class', (tomhas_slighe/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', cuir_SMS('java 스윙시험\n'))
        가로, inghearach_suidhich = (너비-400)//2, (높이-280)//2
        tarraing_VALUE = seic_pel((가로, inghearach_suidhich), (32, 80, 144))
        tarraing_VALUE.save(str(tomhas_slighe/(atharraich_am_meud_SMS+'.png')))
        ruith = len(LOG_ràgh); briog_VALUE(가로+80, inghearach_suidhich+155)
        기다리기('SWING CLICK Ainm'.encode(), ruith)
        ruith = len(LOG_ràgh); briog_VALUE(가로+385, inghearach_suidhich+15); 기다리기(b'jkoros-native> ', ruith)
        assert 'AFTER_RESOLUTION' in slige('echo AFTER_RESOLUTION')
        print('PASS:', atharraich_am_meud_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if tar_chur_VALUE: tar_chur_VALUE.close()
        if cian_VALUE: cian_VALUE.close()
        if Pròiseas_VALUE.poll() is None:
            Pròiseas_VALUE.terminate()
            try: Pròiseas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Pròiseas_VALUE.kill(); Pròiseas_VALUE.wait()
        roghnaichear_a916db4e.close(); Pròiseas_VALUE.stdout.close()
        (tomhas_slighe/(atharraich_am_meud_SMS+'.log')).write_bytes(LOG_ràgh)


def ruith():
    tomhas_slighe = tilg_freumh/'build/verification/resolution'; tomhas_slighe.mkdir(parents=True, exist_ok=True)
    LOG_ràgh = {'passed': False, 'kernel_sha256': hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for mì_dhligheach_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            tomhas = subprocess.run(['python3', str(tilg_freumh/'innealan/gnìomhaich_àithne.py'), '--resolution', mì_dhligheach_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert tomhas.returncode == 2 and b'--resolution' in tomhas.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tomhas_slighe), str(tilg_freumh/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, tomhas_slighe); LOG_ràgh['resolutions'].append([너비, 높이])
        LOG_ràgh.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (tomhas_slighe/'report.json').write_text(json.dumps(LOG_ràgh, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ruith()
