#!/usr/bin/env python3
"""tota_tshedimosetso QEMU/VNC에서 화면 lekanya·경계·fensetere sutisa_Boleng·Swing·언어별 그리기를 검사한다."""
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
from desekethopo_Tebego import 정확한값
from diragatsa_Taelo import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    lekanya_SMS = '{}x{}'.format(너비, 높이)
    Thulaganyo_Boleng = subprocess.Popen(['python3', str(기준/'Thuluse/diragatsa_Taelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', lekanya_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    setlhophi_a916db4e = selectors.DefaultSelector(); setlhophi_a916db4e.register(Thulaganyo_Boleng.stdout, selectors.EVENT_READ)
    rekota_mola = bytearray(); kgakala_Boleng = None; fudusa_Boleng = None

    def 기다리기(bontsha_Boleng, dirisa=0):
        마감 = time.monotonic() + 60
        while bontsha_Boleng not in rekota_mola[dirisa:]:
            if time.monotonic() > 마감 or Thulaganyo_Boleng.poll() is not None or b'HALTED' in rekota_mola or b'PANIC:' in rekota_mola:
                raise AssertionError(rekota_mola[dirisa:].decode('utf-8', 'replace'))
            for tiragalo, _ in setlhophi_a916db4e.select(.1):
                tshedimosetso = tiragalo.fileobj.read(65536)
                if tshedimosetso: rekota_mola.extend(tshedimosetso)
        return rekota_mola[dirisa:].decode('utf-8', 'replace')

    def tobetsa_konopo(letshwao, 눌림=True): kgakala_Boleng.sendall(struct.pack('>BBHI', 4, int(눌림), 0, letshwao))

    def romela_SMS(SMS):
        dirisa = len(rekota_mola)
        for Letshwao_Boleng in SMS:
            letshwao = 0xff0d if Letshwao_Boleng == '\n' else ord(Letshwao_Boleng) if ord(Letshwao_Boleng) < 256 else 0x1000000 | ord(Letshwao_Boleng)
            tobetsa_konopo(letshwao); tobetsa_konopo(letshwao, False)
        return dirisa

    def setlhalosataelo(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', romela_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kgakala_Boleng.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def tobetsa_Boleng(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Setshwantsho_sa_maronthorontho_Setshwantsho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tota_tshedimosetso 너비를 쓴다.
        kgakala_Boleng.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        sethalo_Boleng = Image.new('RGB', (너비, 높이)); lefelo_Boleng_9285603e = 0
        while True:
            종류 = 정확한값(kgakala_Boleng, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                boleele_Boleng = struct.unpack('>I', 정확한값(kgakala_Boleng, 7)[3:])[0]; 정확한값(kgakala_Boleng, boleele_Boleng); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kgakala_Boleng, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, boleele_Boleng, khoutufatso_Boleng = struct.unpack('>HHHHi', 정확한값(kgakala_Boleng, 12))
                assert khoutufatso_Boleng == 0 and 가로+폭 <= 너비 and 세로+boleele_Boleng <= 높이
                sethalo_Boleng.paste(Image.frombytes('RGB', (폭, boleele_Boleng), 정확한값(kgakala_Boleng, 폭*boleele_Boleng*4), 'raw', 'BGRX'), (가로, 세로))
                lefelo_Boleng_9285603e += 폭*boleele_Boleng
            if lefelo_Boleng_9285603e:
                assert lefelo_Boleng_9285603e == 너비*높이, lefelo_Boleng_9285603e
                return sethalo_Boleng

    def tlhola_phele(khoodineite_Boleng, 색):
        마감 = time.monotonic()+10
        while True:
            sethalo_Boleng = Setshwantsho_sa_maronthorontho_Setshwantsho()
            if sethalo_Boleng.getpixel(khoodineite_Boleng) == 색: return sethalo_Boleng
            if time.monotonic() > 마감: raise AssertionError((khoodineite_Boleng, sethalo_Boleng.getpixel(khoodineite_Boleng), 색))

    def laisa_Difaele(leina, tshedimosetso): fudusa_Boleng.storbinary('STOR '+leina, io.BytesIO(tshedimosetso))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+lekanya_SMS+' RGB32').encode() in rekota_mola
        print('BOOT:', lekanya_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', rekota_mola).group(1))
        kgakala_Boleng = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kgakala_Boleng, 12) == b'RFB 003.008\n'; kgakala_Boleng.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kgakala_Boleng, 정확한값(kgakala_Boleng, 1)[0]); kgakala_Boleng.sendall(b'\x01')
        assert 정확한값(kgakala_Boleng, 4) == b'\0'*4; kgakala_Boleng.sendall(b'\x01')
        초기 = 정확한값(kgakala_Boleng, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kgakala_Boleng, struct.unpack('>I', 초기[20:])[0])
        kgakala_Boleng.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kgakala_Boleng.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        tlhola_phele((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        tlhola_phele((너비-568, 높이-360), (32, 80, 144))
        dirisa = len(rekota_mola); tobetsa_Boleng(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', dirisa)
        tlhola_phele((너비-568, 높이-360), (24, 32, 48))
        dirisa = len(rekota_mola); tobetsa_Boleng(80, 16); 기다리기(b'TERMINAL FOCUS 1', dirisa)
        setlhalosataelo('ftpd start')
        fudusa_Boleng = ftplib.FTP(); fudusa_Boleng.encoding = 'utf-8'; fudusa_Boleng.connect('127.0.0.1', 접속번호, timeout=20); fudusa_Boleng.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·faelekhutshwe_ya_media 밖·빈 사각형을 포함한다.
        Motswedi = '''#include <화면규약.h>
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
    kwala_faele_tshedimosetso(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        laisa_Difaele('화면시험.c', Motswedi.encode())
        assert 'exit 0' in setlhalosataelo('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', romela_SMS('run /화면시험\n'))
        tlhola_phele((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        Motswedi = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, tsamaiso_phoso
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except tsamaiso_phoso as phoso:
    assert phoso.tshupane == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        laisa_Difaele('화면시험.py', Motswedi.encode())
        기다리기(b'PYTHON RESOLUTION PASS', romela_SMS('python /화면시험.py\n'))
        tlhola_phele((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        Motswedi = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("lekanya");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("faelekhutshwe_ya_media"); }
        catch (잘못된인수예외 phoso) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 pinagare javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(Motswedi.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        laisa_Difaele('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', romela_SMS('java 해상도경계시험\n'))
        tlhola_phele((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        # 게스트 javac의 Thuso_Boleng 문법으로 lekanya fenenkolola_Boleng·지우기·다섯 인수 그리기를 컴파일한다.
        Motswedi = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.kwala_Mola("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        laisa_Difaele('해상도시험.java', Motswedi.encode())
        결과 = setlhalosataelo('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', romela_SMS('java 해상도시험\n'))
        tlhola_phele((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        laisa_Difaele('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', romela_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        sethalo_Boleng = tlhola_phele((가로, 세로), (32, 80, 144))
        sethalo_Boleng.save(str(결과경로/(lekanya_SMS+'.png')))
        dirisa = len(rekota_mola); tobetsa_Boleng(가로+80, 세로+155)
        기다리기('SWING CLICK leina'.encode(), dirisa)
        dirisa = len(rekota_mola); tobetsa_Boleng(가로+385, 세로+15); 기다리기(b'jkoros-native> ', dirisa)
        assert 'AFTER_RESOLUTION' in setlhalosataelo('echo AFTER_RESOLUTION')
        print('PASS:', lekanya_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if fudusa_Boleng: fudusa_Boleng.close()
        if kgakala_Boleng: kgakala_Boleng.close()
        if Thulaganyo_Boleng.poll() is None:
            Thulaganyo_Boleng.terminate()
            try: Thulaganyo_Boleng.wait(timeout=8)
            except subprocess.TimeoutExpired: Thulaganyo_Boleng.kill(); Thulaganyo_Boleng.wait()
        setlhophi_a916db4e.close(); Thulaganyo_Boleng.stdout.close()
        (결과경로/(lekanya_SMS+'.log')).write_bytes(rekota_mola)


def dirisa():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    rekota_mola = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for Ga_e_a_siama_Boleng in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Thuluse/diragatsa_Taelo.py'), '--resolution', Ga_e_a_siama_Boleng], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); rekota_mola['resolutions'].append([너비, 높이])
        rekota_mola.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(rekota_mola, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': dirisa()
