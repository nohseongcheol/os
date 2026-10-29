#!/usr/bin/env python3
"""ǹdịnezie_datà QEMU/VNC에서 화면 Ụhara·경계·windò gàa_valuu·Swing·언어별 그리기를 검사한다."""
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
from desktọpụ_lèe import 정확한값
from mee_nnyemiwu import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ụha_SMS = '{}x{}'.format(너비, 높이)
    ùsòrò_valuu_6712bde7 = subprocess.Popen(['python3', str(기준/'Ngwaọrụ/mee_nnyemiwu.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ụha_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ihe_nhọpụta_a916db4e = selectors.DefaultSelector(); ihe_nhọpụta_a916db4e.register(ùsòrò_valuu_6712bde7.stdout, selectors.EVENT_READ)
    ndekọ_NDEKỌ = bytearray(); ebe_dị̀anyā_valuu = None; dògharịa_valuu = None

    def 기다리기(gòsi_valuu, Bido=0):
        마감 = time.monotonic() + 60
        while gòsi_valuu not in ndekọ_NDEKỌ[Bido:]:
            if time.monotonic() > 마감 or ùsòrò_valuu_6712bde7.poll() is not None or b'HALTED' in ndekọ_NDEKỌ or b'PANIC:' in ndekọ_NDEKỌ:
                raise AssertionError(ndekọ_NDEKỌ[Bido:].decode('utf-8', 'replace'))
            for mmèrème, _ in ihe_nhọpụta_a916db4e.select(.1):
                datà = mmèrème.fileobj.read(65536)
                if datà: ndekọ_NDEKỌ.extend(datà)
        return ndekọ_NDEKỌ[Bido:].decode('utf-8', 'replace')

    def pịkịnye_ọdụmbi(adimara, 눌림=True): ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHI', 4, int(눌림), 0, adimara))

    def zipu_SMS(SMS):
        Bido = len(ndekọ_NDEKỌ)
        for mkpụrụedemede_valuu in SMS:
            adimara = 0xff0d if mkpụrụedemede_valuu == '\n' else ord(mkpụrụedemede_valuu) if ord(mkpụrụedemede_valuu) < 256 else 0x1000000 | ord(mkpụrụedemede_valuu)
            pịkịnye_ọdụmbi(adimara); pịkịnye_ọdụmbi(adimara, False)
        return Bido

    def nkọwannyemiwu(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', zipu_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def pịkịnye_valuu(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ǹdịnezie_datà 너비를 쓴다.
        ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        osise_valuu = Image.new('RGB', (너비, 높이)); kàtigori_valuu = 0
        while True:
            종류 = 정확한값(ebe_dị̀anyā_valuu, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ogologo_valuu = struct.unpack('>I', 정확한값(ebe_dị̀anyā_valuu, 7)[3:])[0]; 정확한값(ebe_dị̀anyā_valuu, ogologo_valuu); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ebe_dị̀anyā_valuu, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ogologo_valuu, ntinye_koòdù_valuu = struct.unpack('>HHHHi', 정확한값(ebe_dị̀anyā_valuu, 12))
                assert ntinye_koòdù_valuu == 0 and 가로+폭 <= 너비 and 세로+ogologo_valuu <= 높이
                osise_valuu.paste(Image.frombytes('RGB', (폭, ogologo_valuu), 정확한값(ebe_dị̀anyā_valuu, 폭*ogologo_valuu*4), 'raw', 'BGRX'), (가로, 세로))
                kàtigori_valuu += 폭*ogologo_valuu
            if kàtigori_valuu:
                assert kàtigori_valuu == 너비*높이, kàtigori_valuu
                return osise_valuu

    def cheèk_pel(nsòezikọebē_valuu, 색):
        마감 = time.monotonic()+10
        while True:
            osise_valuu = bitmap_foto()
            if osise_valuu.getpixel(nsòezikọebē_valuu) == 색: return osise_valuu
            if time.monotonic() > 마감: raise AssertionError((nsòezikọebē_valuu, osise_valuu.getpixel(nsòezikọebē_valuu), 색))

    def bùlie_Ndi_ọbọakwụkwọ(Aha, datà): dògharịa_valuu.storbinary('STOR '+Aha, io.BytesIO(datà))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ụha_SMS+' RGB32').encode() in ndekọ_NDEKỌ
        print('BOOT:', ụha_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ndekọ_NDEKỌ).group(1))
        ebe_dị̀anyā_valuu = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ebe_dị̀anyā_valuu, 12) == b'RFB 003.008\n'; ebe_dị̀anyā_valuu.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ebe_dị̀anyā_valuu, 정확한값(ebe_dị̀anyā_valuu, 1)[0]); ebe_dị̀anyā_valuu.sendall(b'\x01')
        assert 정확한값(ebe_dị̀anyā_valuu, 4) == b'\0'*4; ebe_dị̀anyā_valuu.sendall(b'\x01')
        초기 = 정확한값(ebe_dị̀anyā_valuu, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ebe_dị̀anyā_valuu, struct.unpack('>I', 초기[20:])[0])
        ebe_dị̀anyā_valuu.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        cheèk_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        cheèk_pel((너비-568, 높이-360), (32, 80, 144))
        Bido = len(ndekọ_NDEKỌ); pịkịnye_valuu(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Bido)
        cheèk_pel((너비-568, 높이-360), (24, 32, 48))
        Bido = len(ndekọ_NDEKỌ); pịkịnye_valuu(80, 16); 기다리기(b'TERMINAL FOCUS 1', Bido)
        nkọwannyemiwu('ftpd start')
        dògharịa_valuu = ftplib.FTP(); dògharịa_valuu.encoding = 'utf-8'; dògharịa_valuu.connect('127.0.0.1', 접속번호, timeout=20); dògharịa_valuu.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ntipanye 밖·빈 사각형을 포함한다.
        ebensìbịa = '''#include <화면규약.h>
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
    dee_ọbọakwụkwọ_datà(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        bùlie_Ndi_ọbọakwụkwọ('화면시험.c', ebensìbịa.encode())
        assert 'exit 0' in nkọwannyemiwu('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', zipu_SMS('run /화면시험\n'))
        cheèk_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', zipu_SMS('q'))
        ebensìbịa = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, sistèm_mmejọ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistèm_mmejọ as mmejọ:
    assert mmejọ.indèks == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        bùlie_Ndi_ọbọakwụkwọ('화면시험.py', ebensìbịa.encode())
        기다리기(b'PYTHON RESOLUTION PASS', zipu_SMS('python /화면시험.py\n'))
        cheèk_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', zipu_SMS('q'))
        ebensìbịa = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ụhara");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ntipanye"); }
        catch (잘못된인수예외 mmejọ) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 usu javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(ebensìbịa.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        bùlie_Ndi_ọbọakwụkwọ('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', zipu_SMS('java 해상도경계시험\n'))
        cheèk_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', zipu_SMS('q'))
        # 게스트 javac의 nkwado_valuu 문법으로 Ụhara mgbaajụjụ_valuu·지우기·다섯 인수 그리기를 컴파일한다.
        ebensìbịa = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.dee_ahịrī("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        bùlie_Ndi_ọbọakwụkwọ('해상도시험.java', ebensìbịa.encode())
        결과 = nkọwannyemiwu('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', zipu_SMS('java 해상도시험\n'))
        cheèk_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', zipu_SMS('q'))
        bùlie_Ndi_ọbọakwụkwọ('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', zipu_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        osise_valuu = cheèk_pel((가로, 세로), (32, 80, 144))
        osise_valuu.save(str(결과경로/(ụha_SMS+'.png')))
        Bido = len(ndekọ_NDEKỌ); pịkịnye_valuu(가로+80, 세로+155)
        기다리기('SWING CLICK Aha'.encode(), Bido)
        Bido = len(ndekọ_NDEKỌ); pịkịnye_valuu(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Bido)
        assert 'AFTER_RESOLUTION' in nkọwannyemiwu('echo AFTER_RESOLUTION')
        print('PASS:', ụha_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if dògharịa_valuu: dògharịa_valuu.close()
        if ebe_dị̀anyā_valuu: ebe_dị̀anyā_valuu.close()
        if ùsòrò_valuu_6712bde7.poll() is None:
            ùsòrò_valuu_6712bde7.terminate()
            try: ùsòrò_valuu_6712bde7.wait(timeout=8)
            except subprocess.TimeoutExpired: ùsòrò_valuu_6712bde7.kill(); ùsòrò_valuu_6712bde7.wait()
        ihe_nhọpụta_a916db4e.close(); ùsòrò_valuu_6712bde7.stdout.close()
        (결과경로/(ụha_SMS+'.log')).write_bytes(ndekọ_NDEKỌ)


def Bido():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    ndekọ_NDEKỌ = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for abànihe_valuu in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Ngwaọrụ/mee_nnyemiwu.py'), '--resolution', abànihe_valuu], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); ndekọ_NDEKỌ['resolutions'].append([너비, 높이])
        ndekọ_NDEKỌ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(ndekọ_NDEKỌ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Bido()
