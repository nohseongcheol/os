#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani QEMU/VNC에서 화면 Girma·경계·taga Matsar_da_Daraja·Swing·언어별 그리기를 검사한다."""
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
from destof_s import 정확한값
from gudanar_Umarni import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); lambar_kafa = 임시.getsockname()[1]
    girma_SMS = '{}x{}'.format(너비, 높이)
    haryar_aikin_na_ura_Daraja = subprocess.Popen(['python3', str(기준/'Kaya/gudanar_Umarni.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(lambar_kafa), '--resolution', girma_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    mai_zabe_a916db4e = selectors.DefaultSelector(); mai_zabe_a916db4e.register(haryar_aikin_na_ura_Daraja.stdout, selectors.EVENT_READ)
    logu_naɗa = bytearray(); na_nesa_Daraja = None; Gusar_da_Daraja = None

    def 기다리기(Nuna_Daraja, Tafiyar_da=0):
        마감 = time.monotonic() + 60
        while Nuna_Daraja not in logu_naɗa[Tafiyar_da:]:
            if time.monotonic() > 마감 or haryar_aikin_na_ura_Daraja.poll() is not None or b'HALTED' in logu_naɗa or b'PANIC:' in logu_naɗa:
                raise AssertionError(logu_naɗa[Tafiyar_da:].decode('utf-8', 'replace'))
            for Faruwa, _ in mai_zabe_a916db4e.select(.1):
                Tarin_bayani = Faruwa.fileobj.read(65536)
                if Tarin_bayani: logu_naɗa.extend(Tarin_bayani)
        return logu_naɗa[Tafiyar_da:].decode('utf-8', 'replace')

    def Danna_maɓali(alama_ad6f1a96, 눌림=True): na_nesa_Daraja.sendall(struct.pack('>BBHI', 4, int(눌림), 0, alama_ad6f1a96))

    def aika_SMS(SMS):
        Tafiyar_da = len(logu_naɗa)
        for Harafi_Daraja in SMS:
            alama_ad6f1a96 = 0xff0d if Harafi_Daraja == '\n' else ord(Harafi_Daraja) if ord(Harafi_Daraja) < 256 else 0x1000000 | ord(Harafi_Daraja)
            Danna_maɓali(alama_ad6f1a96); Danna_maɓali(alama_ad6f1a96, False)
        return Tafiyar_da

    def Mai_fayyace_umani(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', aika_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): na_nesa_Daraja.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def Danna_Daraja(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Hoton_digo_digo_Hoto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 Na_hakika_Tarin_bayani 너비를 쓴다.
        na_nesa_Daraja.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        zane_Daraja = Image.new('RGB', (너비, 높이)); Wuri_Daraja = 0
        while True:
            종류 = 정확한값(na_nesa_Daraja, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                Tsawo_Daraja = struct.unpack('>I', 정확한값(na_nesa_Daraja, 7)[3:])[0]; 정확한값(na_nesa_Daraja, Tsawo_Daraja); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(na_nesa_Daraja, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, Tsawo_Daraja, Juyar_da_bayanai_zuwa_lamba_Daraja = struct.unpack('>HHHHi', 정확한값(na_nesa_Daraja, 12))
                assert Juyar_da_bayanai_zuwa_lamba_Daraja == 0 and 가로+폭 <= 너비 and 세로+Tsawo_Daraja <= 높이
                zane_Daraja.paste(Image.frombytes('RGB', (폭, Tsawo_Daraja), 정확한값(na_nesa_Daraja, 폭*Tsawo_Daraja*4), 'raw', 'BGRX'), (가로, 세로))
                Wuri_Daraja += 폭*Tsawo_Daraja
            if Wuri_Daraja:
                assert Wuri_Daraja == 너비*높이, Wuri_Daraja
                return zane_Daraja

    def Bincika_pel(Mai_tsarawa_Daraja, 색):
        마감 = time.monotonic()+10
        while True:
            zane_Daraja = Hoton_digo_digo_Hoto()
            if zane_Daraja.getpixel(Mai_tsarawa_Daraja) == 색: return zane_Daraja
            if time.monotonic() > 마감: raise AssertionError((Mai_tsarawa_Daraja, zane_Daraja.getpixel(Mai_tsarawa_Daraja), 색))

    def lodawa_Fayiloli(Suna, Tarin_bayani): Gusar_da_Daraja.storbinary('STOR '+Suna, io.BytesIO(Tarin_bayani))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+girma_SMS+' RGB32').encode() in logu_naɗa
        print('BOOT:', girma_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', logu_naɗa).group(1))
        na_nesa_Daraja = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(na_nesa_Daraja, 12) == b'RFB 003.008\n'; na_nesa_Daraja.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(na_nesa_Daraja, 정확한값(na_nesa_Daraja, 1)[0]); na_nesa_Daraja.sendall(b'\x01')
        assert 정확한값(na_nesa_Daraja, 4) == b'\0'*4; na_nesa_Daraja.sendall(b'\x01')
        초기 = 정확한값(na_nesa_Daraja, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(na_nesa_Daraja, struct.unpack('>I', 초기[20:])[0])
        na_nesa_Daraja.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        na_nesa_Daraja.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        Bincika_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        Bincika_pel((너비-568, 높이-360), (32, 80, 144))
        Tafiyar_da = len(logu_naɗa); Danna_Daraja(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Tafiyar_da)
        Bincika_pel((너비-568, 높이-360), (24, 32, 48))
        Tafiyar_da = len(logu_naɗa); Danna_Daraja(80, 16); 기다리기(b'TERMINAL FOCUS 1', Tafiyar_da)
        Mai_fayyace_umani('ftpd start')
        Gusar_da_Daraja = ftplib.FTP(); Gusar_da_Daraja.encoding = 'utf-8'; Gusar_da_Daraja.connect('127.0.0.1', lambar_kafa, timeout=20); Gusar_da_Daraja.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·darfi 밖·빈 사각형을 포함한다.
        tushe = '''#include <화면규약.h>
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
    Rubuta_Fayil_Tarin_bayani(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        lodawa_Fayiloli('화면시험.c', tushe.encode())
        assert 'exit 0' in Mai_fayyace_umani('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', aika_SMS('run /화면시험\n'))
        Bincika_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', aika_SMS('q'))
        tushe = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, na_ura_Kuskure
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except na_ura_Kuskure as Kuskure:
    assert Kuskure.Indes == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        lodawa_Fayiloli('화면시험.py', tushe.encode())
        기다리기(b'PYTHON RESOLUTION PASS', aika_SMS('python /화면시험.py\n'))
        Bincika_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', aika_SMS('q'))
        tushe = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Matsayi_banbanchi("Girma");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new Matsayi_banbanchi("darfi"); }
        catch (mara_ƙarfi_Tubalin_aiki_banbanchi Kuskure) { }
        화면.share_Mashigar_bayanai(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # banbanchi 처리는 sauka javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(tushe.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        lodawa_Fayiloli('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', aika_SMS('java 해상도경계시험\n'))
        Bincika_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', aika_SMS('q'))
        # 게스트 javac의 taimako_Daraja 문법으로 Girma Matantanci_Daraja·share_Mashigar_bayanai·다섯 인수 그리기를 컴파일한다.
        tushe = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.share_Mashigar_bayanai(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.Rubuta_Layi("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        lodawa_Fayiloli('해상도시험.java', tushe.encode())
        결과 = Mai_fayyace_umani('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', aika_SMS('java 해상도시험\n'))
        Bincika_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', aika_SMS('q'))
        lodawa_Fayiloli('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', aika_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        zane_Daraja = Bincika_pel((가로, 세로), (32, 80, 144))
        zane_Daraja.save(str(결과경로/(girma_SMS+'.png')))
        Tafiyar_da = len(logu_naɗa); Danna_Daraja(가로+80, 세로+155)
        기다리기('SWING CLICK Suna'.encode(), Tafiyar_da)
        Tafiyar_da = len(logu_naɗa); Danna_Daraja(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Tafiyar_da)
        assert 'AFTER_RESOLUTION' in Mai_fayyace_umani('echo AFTER_RESOLUTION')
        print('PASS:', girma_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Gusar_da_Daraja: Gusar_da_Daraja.close()
        if na_nesa_Daraja: na_nesa_Daraja.close()
        if haryar_aikin_na_ura_Daraja.poll() is None:
            haryar_aikin_na_ura_Daraja.terminate()
            try: haryar_aikin_na_ura_Daraja.wait(timeout=8)
            except subprocess.TimeoutExpired: haryar_aikin_na_ura_Daraja.kill(); haryar_aikin_na_ura_Daraja.wait()
        mai_zabe_a916db4e.close(); haryar_aikin_na_ura_Daraja.stdout.close()
        (결과경로/(girma_SMS+'.log')).write_bytes(logu_naɗa)


def Tafiyar_da():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    logu_naɗa = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for mara_ƙarfi_Daraja in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Kaya/gudanar_Umarni.py'), '--resolution', mara_ƙarfi_Daraja], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); logu_naɗa['resolutions'].append([너비, 높이])
        logu_naɗa.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(logu_naɗa, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Tafiyar_da()
