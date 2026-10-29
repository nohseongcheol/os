#!/usr/bin/env python3
"""hakyky_maglumat QEMU/VNC에서 화면 Ululyk·경계·penjire ýerini_üýtget_baha·Swing·언어별 그리기를 검사한다."""
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
from iş_stoly_görkez import 정확한값
from ýerine_ýetir_buýruk import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ölçegi_üýtget_SMS = '{}x{}'.format(너비, 높이)
    Proses_baha = subprocess.Popen(['python3', str(기준/'Gurallar/ýerine_ýetir_buýruk.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ölçegi_üýtget_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    saýlaýjy_a916db4e = selectors.DefaultSelector(); saýlaýjy_a916db4e.register(Proses_baha.stdout, selectors.EVENT_READ)
    hasaba_alyş_setir = bytearray(); uzakdan_baha = None; geçir_baha = None

    def 기다리기(görkez_baha_487749b8, Bitir=0):
        마감 = time.monotonic() + 60
        while görkez_baha_487749b8 not in hasaba_alyş_setir[Bitir:]:
            if time.monotonic() > 마감 or Proses_baha.poll() is not None or b'HALTED' in hasaba_alyş_setir or b'PANIC:' in hasaba_alyş_setir:
                raise AssertionError(hasaba_alyş_setir[Bitir:].decode('utf-8', 'replace'))
            for waka, _ in saýlaýjy_a916db4e.select(.1):
                maglumat = waka.fileobj.read(65536)
                if maglumat: hasaba_alyş_setir.extend(maglumat)
        return hasaba_alyş_setir[Bitir:].decode('utf-8', 'replace')

    def bas_düwme(nyşan, 눌림=True): uzakdan_baha.sendall(struct.pack('>BBHI', 4, int(눌림), 0, nyşan))

    def SMS_iber(Metin):
        Bitir = len(hasaba_alyş_setir)
        for nyşan_baha_068c2631 in Metin:
            nyşan = 0xff0d if nyşan_baha_068c2631 == '\n' else ord(nyşan_baha_068c2631) if ord(nyşan_baha_068c2631) < 256 else 0x1000000 | ord(nyşan_baha_068c2631)
            bas_düwme(nyşan); bas_düwme(nyşan, False)
        return Bitir

    def gabyjak(Metin): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_iber(Metin+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): uzakdan_baha.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bas_baha(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def nokatlardan_ýygnalan_şekil_surat():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 hakyky_maglumat 너비를 쓴다.
        uzakdan_baha.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        çyzgy_baha = Image.new('RGB', (너비, 높이)); ýaýla_baha = 0
        while True:
            종류 = 정확한값(uzakdan_baha, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dowamlylyk_baha = struct.unpack('>I', 정확한값(uzakdan_baha, 7)[3:])[0]; 정확한값(uzakdan_baha, dowamlylyk_baha); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(uzakdan_baha, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, dowamlylyk_baha, kodlaşdyrma_baha = struct.unpack('>HHHHi', 정확한값(uzakdan_baha, 12))
                assert kodlaşdyrma_baha == 0 and 가로+폭 <= 너비 and 세로+dowamlylyk_baha <= 높이
                çyzgy_baha.paste(Image.frombytes('RGB', (폭, dowamlylyk_baha), 정확한값(uzakdan_baha, 폭*dowamlylyk_baha*4), 'raw', 'BGRX'), (가로, 세로))
                ýaýla_baha += 폭*dowamlylyk_baha
            if ýaýla_baha:
                assert ýaýla_baha == 너비*높이, ýaýla_baha
                return çyzgy_baha

    def derňe_pel(koordinata_baha, 색):
        마감 = time.monotonic()+10
        while True:
            çyzgy_baha = nokatlardan_ýygnalan_şekil_surat()
            if çyzgy_baha.getpixel(koordinata_baha) == 색: return çyzgy_baha
            if time.monotonic() > 마감: raise AssertionError((koordinata_baha, çyzgy_baha.getpixel(koordinata_baha), 색))

    def ýükle_Faýllar(Ad, maglumat): geçir_baha.storbinary('STOR '+Ad, io.BytesIO(maglumat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ölçegi_üýtget_SMS+' RGB32').encode() in hasaba_alyş_setir
        print('BOOT:', ölçegi_üýtget_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', hasaba_alyş_setir).group(1))
        uzakdan_baha = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(uzakdan_baha, 12) == b'RFB 003.008\n'; uzakdan_baha.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(uzakdan_baha, 정확한값(uzakdan_baha, 1)[0]); uzakdan_baha.sendall(b'\x01')
        assert 정확한값(uzakdan_baha, 4) == b'\0'*4; uzakdan_baha.sendall(b'\x01')
        초기 = 정확한값(uzakdan_baha, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(uzakdan_baha, struct.unpack('>I', 초기[20:])[0])
        uzakdan_baha.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzakdan_baha.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        derňe_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        derňe_pel((너비-568, 높이-360), (32, 80, 144))
        Bitir = len(hasaba_alyş_setir); bas_baha(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Bitir)
        derňe_pel((너비-568, 높이-360), (24, 32, 48))
        Bitir = len(hasaba_alyş_setir); bas_baha(80, 16); 기다리기(b'TERMINAL FOCUS 1', Bitir)
        gabyjak('ftpd start')
        geçir_baha = ftplib.FTP(); geçir_baha.encoding = 'utf-8'; geçir_baha.connect('127.0.0.1', 접속번호, timeout=20); geçir_baha.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·klip 밖·빈 사각형을 포함한다.
        Çeşme = '''#include <화면규약.h>
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
    ýaz_faýl_maglumat(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ýükle_Faýllar('화면시험.c', Çeşme.encode())
        assert 'exit 0' in gabyjak('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_iber('run /화면시험\n'))
        derňe_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_iber('q'))
        Çeşme = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, ulgam_säwlik
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ulgam_säwlik as Hata:
    assert Hata.indeks == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ýükle_Faýllar('화면시험.py', Çeşme.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_iber('python /화면시험.py\n'))
        derňe_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_iber('q'))
        Çeşme = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ululyk");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("klip"); }
        catch (잘못된인수예외 Hata) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 esasy javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(Çeşme.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        ýükle_Faýllar('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_iber('java 해상도경계시험\n'))
        derňe_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_iber('q'))
        # 게스트 javac의 Goldaw_baha 문법으로 Ululyk talap_baha·지우기·다섯 인수 그리기를 컴파일한다.
        Çeşme = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ýaz_setir("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ýükle_Faýllar('해상도시험.java', Çeşme.encode())
        결과 = gabyjak('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', SMS_iber('java 해상도시험\n'))
        derňe_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_iber('q'))
        ýükle_Faýllar('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_iber('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        çyzgy_baha = derňe_pel((가로, 세로), (32, 80, 144))
        çyzgy_baha.save(str(결과경로/(ölçegi_üýtget_SMS+'.png')))
        Bitir = len(hasaba_alyş_setir); bas_baha(가로+80, 세로+155)
        기다리기('SWING CLICK Ad'.encode(), Bitir)
        Bitir = len(hasaba_alyş_setir); bas_baha(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Bitir)
        assert 'AFTER_RESOLUTION' in gabyjak('echo AFTER_RESOLUTION')
        print('PASS:', ölçegi_üýtget_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if geçir_baha: geçir_baha.close()
        if uzakdan_baha: uzakdan_baha.close()
        if Proses_baha.poll() is None:
            Proses_baha.terminate()
            try: Proses_baha.wait(timeout=8)
            except subprocess.TimeoutExpired: Proses_baha.kill(); Proses_baha.wait()
        saýlaýjy_a916db4e.close(); Proses_baha.stdout.close()
        (결과경로/(ölçegi_üýtget_SMS+'.log')).write_bytes(hasaba_alyş_setir)


def Bitir():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    hasaba_alyş_setir = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nädogry_baha in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Gurallar/ýerine_ýetir_buýruk.py'), '--resolution', nädogry_baha], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); hasaba_alyş_setir['resolutions'].append([너비, 높이])
        hasaba_alyş_setir.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(hasaba_alyş_setir, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Bitir()
