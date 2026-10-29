#!/usr/bin/env python3
"""liteew_mbir QEMU/VNC에서 화면 tolluwaay·경계·palanteer toxal_xëyma·Swing·언어별 그리기를 검사한다."""
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
from Biro_wonin import 정확한값
from def_ndigel import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    tolluwaay_SMS = '{}x{}'.format(너비, 높이)
    yokkute_xëyma = subprocess.Popen(['python3', str(기준/'Jumtukaay_yi/def_ndigel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', tolluwaay_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tànnkat_a916db4e = selectors.DefaultSelector(); tànnkat_a916db4e.register(yokkute_xëyma.stdout, selectors.EVENT_READ)
    làq_Dënk = bytearray(); lu_soree_xëyma = None; toxal_xëyma_630ba093 = None

    def 기다리기(féeñal_xëyma, daw=0):
        마감 = time.monotonic() + 60
        while féeñal_xëyma not in làq_Dënk[daw:]:
            if time.monotonic() > 마감 or yokkute_xëyma.poll() is not None or b'HALTED' in làq_Dënk or b'PANIC:' in làq_Dënk:
                raise AssertionError(làq_Dënk[daw:].decode('utf-8', 'replace'))
            for xewxew, _ in tànnkat_a916db4e.select(.1):
                mbir = xewxew.fileobj.read(65536)
                if mbir: làq_Dënk.extend(mbir)
        return làq_Dënk[daw:].decode('utf-8', 'replace')

    def bës_butoñ(sembóol, 눌림=True): lu_soree_xëyma.sendall(struct.pack('>BBHI', 4, int(눌림), 0, sembóol))

    def yónnee_SMS(Tekst):
        daw = len(làq_Dënk)
        for Araf_xëyma in Tekst:
            sembóol = 0xff0d if Araf_xëyma == '\n' else ord(Araf_xëyma) if ord(Araf_xëyma) < 256 else 0x1000000 | ord(Araf_xëyma)
            bës_butoñ(sembóol); bës_butoñ(sembóol, False)
        return daw

    def Wëreef(Tekst): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', yónnee_SMS(Tekst+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): lu_soree_xëyma.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bës_xëyma(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Nataal_bu_sosoo_ci_ay_tomb_nataal():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 liteew_mbir 너비를 쓴다.
        lu_soree_xëyma.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        deseñ_xëyma = Image.new('RGB', (너비, 높이)); ngiir_xëyma_9285603e = 0
        while True:
            종류 = 정확한값(lu_soree_xëyma, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                diir_xëyma = struct.unpack('>I', 정확한값(lu_soree_xëyma, 7)[3:])[0]; 정확한값(lu_soree_xëyma, diir_xëyma); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(lu_soree_xëyma, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, diir_xëyma, nëbbin_ci_lim_xëyma = struct.unpack('>HHHHi', 정확한값(lu_soree_xëyma, 12))
                assert nëbbin_ci_lim_xëyma == 0 and 가로+폭 <= 너비 and 세로+diir_xëyma <= 높이
                deseñ_xëyma.paste(Image.frombytes('RGB', (폭, diir_xëyma), 정확한값(lu_soree_xëyma, 폭*diir_xëyma*4), 'raw', 'BGRX'), (가로, 세로))
                ngiir_xëyma_9285603e += 폭*diir_xëyma
            if ngiir_xëyma_9285603e:
                assert ngiir_xëyma_9285603e == 너비*높이, ngiir_xëyma_9285603e
                return deseñ_xëyma

    def sek_piksel(tolluwaay_xëyma, 색):
        마감 = time.monotonic()+10
        while True:
            deseñ_xëyma = Nataal_bu_sosoo_ci_ay_tomb_nataal()
            if deseñ_xëyma.getpixel(tolluwaay_xëyma) == 색: return deseñ_xëyma
            if time.monotonic() > 마감: raise AssertionError((tolluwaay_xëyma, deseñ_xëyma.getpixel(tolluwaay_xëyma), 색))

    def toxalsi_Fisiye_yi(tur_253d1510, mbir): toxal_xëyma_630ba093.storbinary('STOR '+tur_253d1510, io.BytesIO(mbir))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+tolluwaay_SMS+' RGB32').encode() in làq_Dënk
        print('BOOT:', tolluwaay_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', làq_Dënk).group(1))
        lu_soree_xëyma = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(lu_soree_xëyma, 12) == b'RFB 003.008\n'; lu_soree_xëyma.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(lu_soree_xëyma, 정확한값(lu_soree_xëyma, 1)[0]); lu_soree_xëyma.sendall(b'\x01')
        assert 정확한값(lu_soree_xëyma, 4) == b'\0'*4; lu_soree_xëyma.sendall(b'\x01')
        초기 = 정확한값(lu_soree_xëyma, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(lu_soree_xëyma, struct.unpack('>I', 초기[20:])[0])
        lu_soree_xëyma.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        lu_soree_xëyma.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        sek_piksel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        sek_piksel((너비-568, 높이-360), (32, 80, 144))
        daw = len(làq_Dënk); bës_xëyma(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', daw)
        sek_piksel((너비-568, 높이-360), (24, 32, 48))
        daw = len(làq_Dënk); bës_xëyma(80, 16); 기다리기(b'TERMINAL FOCUS 1', daw)
        Wëreef('ftpd start')
        toxal_xëyma_630ba093 = ftplib.FTP(); toxal_xëyma_630ba093.encoding = 'utf-8'; toxal_xëyma_630ba093.connect('127.0.0.1', 접속번호, timeout=20); toxal_xëyma_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·kilip 밖·빈 사각형을 포함한다.
        Cosaan = '''#include <화면규약.h>
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
    biir_bara_denc_mbir(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        toxalsi_Fisiye_yi('화면시험.c', Cosaan.encode())
        assert 'exit 0' in Wëreef('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', yónnee_SMS('run /화면시험\n'))
        sek_piksel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', yónnee_SMS('q'))
        Cosaan = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, kureel_njumte
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except kureel_njumte as njumte:
    assert njumte.àlluwa_tur == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        toxalsi_Fisiye_yi('화면시험.py', Cosaan.encode())
        기다리기(b'PYTHON RESOLUTION PASS', yónnee_SMS('python /화면시험.py\n'))
        sek_piksel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', yónnee_SMS('q'))
        Cosaan = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("tolluwaay");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("kilip"); }
        catch (잘못된인수예외 njumte) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 dalal javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(Cosaan.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        toxalsi_Fisiye_yi('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', yónnee_SMS('java 해상도경계시험\n'))
        sek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', yónnee_SMS('q'))
        # 게스트 javac의 Ndimbal_xëyma 문법으로 tolluwaay laaj_xëyma·지우기·다섯 인수 그리기를 컴파일한다.
        Cosaan = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.biir_buum("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        toxalsi_Fisiye_yi('해상도시험.java', Cosaan.encode())
        결과 = Wëreef('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', yónnee_SMS('java 해상도시험\n'))
        sek_piksel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', yónnee_SMS('q'))
        toxalsi_Fisiye_yi('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', yónnee_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        deseñ_xëyma = sek_piksel((가로, 세로), (32, 80, 144))
        deseñ_xëyma.save(str(결과경로/(tolluwaay_SMS+'.png')))
        daw = len(làq_Dënk); bës_xëyma(가로+80, 세로+155)
        기다리기('SWING CLICK tur_253d1510'.encode(), daw)
        daw = len(làq_Dënk); bës_xëyma(가로+385, 세로+15); 기다리기(b'jkoros-native> ', daw)
        assert 'AFTER_RESOLUTION' in Wëreef('echo AFTER_RESOLUTION')
        print('PASS:', tolluwaay_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if toxal_xëyma_630ba093: toxal_xëyma_630ba093.close()
        if lu_soree_xëyma: lu_soree_xëyma.close()
        if yokkute_xëyma.poll() is None:
            yokkute_xëyma.terminate()
            try: yokkute_xëyma.wait(timeout=8)
            except subprocess.TimeoutExpired: yokkute_xëyma.kill(); yokkute_xëyma.wait()
        tànnkat_a916db4e.close(); yokkute_xëyma.stdout.close()
        (결과경로/(tolluwaay_SMS+'.log')).write_bytes(làq_Dënk)


def daw():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    làq_Dënk = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for baaxul_xëyma in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Jumtukaay_yi/def_ndigel.py'), '--resolution', baaxul_xëyma], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); làq_Dënk['resolutions'].append([너비, 높이])
        làq_Dënk.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(làq_Dënk, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': daw()
