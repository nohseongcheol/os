#!/usr/bin/env python3
"""raun_gögn QEMU/VNC에서 화면 Stærð·경계·Gluggi færa_VALUE·Swing·언어별 그리기를 검사한다."""
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
from skjáborð_Sýn import EXACT_VALUE
from keyra_skipun import verk_rót


def 해상도시험(너비, 높이, mæld_stærð_slóð):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); tengisnúmer = 임시.getsockname()[1]
    breyta_stærð_SMS = '{}x{}'.format(너비, 높이)
    Ferli_VALUE = subprocess.Popen(['python3', str(verk_rót/'Verkfæri/keyra_skipun.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(tengisnúmer), '--resolution', breyta_stærð_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    val_a916db4e = selectors.DefaultSelector(); val_a916db4e.register(Ferli_VALUE.stdout, selectors.EVENT_READ)
    LOG_lína = bytearray(); fjartengdur_VALUE = None; flytja_VALUE = None

    def 기다리기(sýna_VALUE, Keyra_2=0):
        마감 = time.monotonic() + 60
        while sýna_VALUE not in LOG_lína[Keyra_2:]:
            if time.monotonic() > 마감 or Ferli_VALUE.poll() is not None or b'HALTED' in LOG_lína or b'PANIC:' in LOG_lína:
                raise AssertionError(LOG_lína[Keyra_2:].decode('utf-8', 'replace'))
            for atvik, _ in val_a916db4e.select(.1):
                gögn = atvik.fileobj.read(65536)
                if gögn: LOG_lína.extend(gögn)
        return LOG_lína[Keyra_2:].decode('utf-8', 'replace')

    def smella_hnappur(tákn, 눌림=True): fjartengdur_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, tákn))

    def senda_SMS(Texti):
        Keyra_2 = len(LOG_lína)
        for stafur_VALUE in Texti:
            tákn = 0xff0d if stafur_VALUE == '\n' else ord(stafur_VALUE) if ord(stafur_VALUE) < 256 else 0x1000000 | ord(stafur_VALUE)
            smella_hnappur(tákn); smella_hnappur(tákn, False)
        return Keyra_2

    def skel(Texti): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', senda_SMS(Texti+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Lóðrétt_staða, 눌림): fjartengdur_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Lóðrétt_staða))

    def smella_VALUE(가로, Lóðrétt_staða): 가리키기(가로, Lóðrétt_staða, 1); 가리키기(가로, Lóðrétt_staða, 0)

    def punktamynd_mynd():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 raun_gögn 너비를 쓴다.
        fjartengdur_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        teikning_VALUE = Image.new('RGB', (너비, 높이)); svæði_VALUE = 0
        while True:
            종류 = EXACT_VALUE(fjartengdur_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengd_VALUE = struct.unpack('>I', EXACT_VALUE(fjartengdur_VALUE, 7)[3:])[0]; EXACT_VALUE(fjartengdur_VALUE, lengd_VALUE); continue
            assert 종류 == 0, 종류
            vara_COUNT = struct.unpack('>H', EXACT_VALUE(fjartengdur_VALUE, 3)[1:])[0]
            for _ in range(vara_COUNT):
                가로, Lóðrétt_staða, 폭, lengd_VALUE, kóðun_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(fjartengdur_VALUE, 12))
                assert kóðun_VALUE == 0 and 가로+폭 <= 너비 and Lóðrétt_staða+lengd_VALUE <= 높이
                teikning_VALUE.paste(Image.frombytes('RGB', (폭, lengd_VALUE), EXACT_VALUE(fjartengdur_VALUE, 폭*lengd_VALUE*4), 'raw', 'BGRX'), (가로, Lóðrétt_staða))
                svæði_VALUE += 폭*lengd_VALUE
            if svæði_VALUE:
                assert svæði_VALUE == 너비*높이, svæði_VALUE
                return teikning_VALUE

    def athuga_díll(hnit_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            teikning_VALUE = punktamynd_mynd()
            if teikning_VALUE.getpixel(hnit_VALUE) == 색: return teikning_VALUE
            if time.monotonic() > 마감: raise AssertionError((hnit_VALUE, teikning_VALUE.getpixel(hnit_VALUE), 색))

    def hlaða_upp_Skrár(Heiti, gögn): flytja_VALUE.storbinary('STOR '+Heiti, io.BytesIO(gögn))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+breyta_stærð_SMS+' RGB32').encode() in LOG_lína
        print('BOOT:', breyta_stærð_SMS, flush=True)
        fjartengdur_númer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_lína).group(1))
        fjartengdur_VALUE = socket.create_connection(('127.0.0.1', fjartengdur_númer), timeout=20)
        assert EXACT_VALUE(fjartengdur_VALUE, 12) == b'RFB 003.008\n'; fjartengdur_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(fjartengdur_VALUE, EXACT_VALUE(fjartengdur_VALUE, 1)[0]); fjartengdur_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(fjartengdur_VALUE, 4) == b'\0'*4; fjartengdur_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(fjartengdur_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(fjartengdur_VALUE, struct.unpack('>I', 초기[20:])[0])
        fjartengdur_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjartengdur_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        athuga_díll((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        athuga_díll((너비-568, 높이-360), (32, 80, 144))
        Keyra_2 = len(LOG_lína); smella_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Keyra_2)
        athuga_díll((너비-568, 높이-360), (24, 32, 48))
        Keyra_2 = len(LOG_lína); smella_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Keyra_2)
        skel('ftpd start')
        flytja_VALUE = ftplib.FTP(); flytja_VALUE.encoding = 'utf-8'; flytja_VALUE.connect('127.0.0.1', tengisnúmer, timeout=20); flytja_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·miðlaskrá 밖·빈 사각형을 포함한다.
        Uppruni = '''#include <화면규약.h>
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
    skrifa_skrá_gögn(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        hlaða_upp_Skrár('화면시험.c', Uppruni.encode())
        assert 'exit 0' in skel('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', senda_SMS('run /화면시험\n'))
        athuga_díll((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', senda_SMS('q'))
        Uppruni = '''from Íslenska import 화면크기, 네모그리기, 그림기다리기, úttak, kerfi_villa
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except kerfi_villa as Villa:
    assert Villa.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
úttak("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        hlaða_upp_Skrár('화면시험.py', Uppruni.encode())
        기다리기(b'PYTHON RESOLUTION PASS', senda_SMS('python /화면시험.py\n'))
        athuga_díll((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', senda_SMS('q'))
        Uppruni = '''import Íslenska.eigin.*;
public class 해상도시험 {
    public static void main(String[] Viðföng) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new staða_undantekning("Stærð");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new staða_undantekning("miðlaskrá"); }
        catch (ógilt_frumbreyta_undantekning Villa) { }
        화면.eyða_færsla(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # undantekning 처리는 hýsa javac 결과를 eigin JVM에 올려 검사한다.
        경계원문 = mæld_stærð_slóð/'해상도경계시험.java'
        경계원문.write_text(Uppruni.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(verk_rót/'dist/jkoros-native-korean.jar'), '-d', str(mæld_stærð_slóð), str(경계원문)])
        hlaða_upp_Skrár('해상도경계시험.class', (mæld_stærð_slóð/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', senda_SMS('java 해상도경계시험\n'))
        athuga_díll((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', senda_SMS('q'))
        # 게스트 javac의 Aðstoð_VALUE 문법으로 Stærð fyrirspurn_VALUE·eyða_færsla·다섯 Viðföng 그리기를 컴파일한다.
        Uppruni = '''public class 해상도시험 {
    public static void main(String[] Viðföng) {
        int 너비=Íslenska.eigin.화면.너비();
        int 높이=Íslenska.eigin.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Íslenska.eigin.화면.eyða_færsla(3153944);
        Íslenska.eigin.화면.사각형(너비-1,높이-1,1,1,10061943);
        Íslenska.eigin.úttak.skrifa_lína("JAVA RESOLUTION PASS");
        Íslenska.eigin.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        hlaða_upp_Skrár('해상도시험.java', Uppruni.encode())
        NIÐURSTAÐA = skel('javac 해상도시험.java'); assert 'exit 0' in NIÐURSTAÐA, NIÐURSTAÐA
        기다리기(b'JAVA RESOLUTION PASS', senda_SMS('java 해상도시험\n'))
        athuga_díll((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', senda_SMS('q'))
        hlaða_upp_Skrár('스윙시험.class', (mæld_stærð_slóð/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', senda_SMS('java 스윙시험\n'))
        가로, Lóðrétt_staða = (너비-400)//2, (높이-280)//2
        teikning_VALUE = athuga_díll((가로, Lóðrétt_staða), (32, 80, 144))
        teikning_VALUE.save(str(mæld_stærð_slóð/(breyta_stærð_SMS+'.png')))
        Keyra_2 = len(LOG_lína); smella_VALUE(가로+80, Lóðrétt_staða+155)
        기다리기('SWING CLICK Heiti'.encode(), Keyra_2)
        Keyra_2 = len(LOG_lína); smella_VALUE(가로+385, Lóðrétt_staða+15); 기다리기(b'jkoros-native> ', Keyra_2)
        assert 'AFTER_RESOLUTION' in skel('echo AFTER_RESOLUTION')
        print('PASS:', breyta_stærð_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if flytja_VALUE: flytja_VALUE.close()
        if fjartengdur_VALUE: fjartengdur_VALUE.close()
        if Ferli_VALUE.poll() is None:
            Ferli_VALUE.terminate()
            try: Ferli_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Ferli_VALUE.kill(); Ferli_VALUE.wait()
        val_a916db4e.close(); Ferli_VALUE.stdout.close()
        (mæld_stærð_slóð/(breyta_stærð_SMS+'.log')).write_bytes(LOG_lína)


def Keyra_2():
    mæld_stærð_slóð = verk_rót/'build/verification/resolution'; mæld_stærð_slóð.mkdir(parents=True, exist_ok=True)
    LOG_lína = {'passed': False, 'kernel_sha256': hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ógilt_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            NIÐURSTAÐA = subprocess.run(['python3', str(verk_rót/'Verkfæri/keyra_skipun.py'), '--resolution', ógilt_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert NIÐURSTAÐA.returncode == 2 and b'--resolution' in NIÐURSTAÐA.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mæld_stærð_slóð), str(verk_rót/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mæld_stærð_slóð); LOG_lína['resolutions'].append([너비, 높이])
        LOG_lína.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mæld_stærð_slóð/'report.json').write_text(json.dumps(LOG_lína, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Keyra_2()
