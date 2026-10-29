#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane QEMU/VNC에서 화면 Ubungako·경계·ifasitela susa_inani·Swing·언어별 그리기를 검사한다."""
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
from ideskithophu_buka import 정확한값
from yenza_umyalo import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    linganisa_I_SMS = '{}x{}'.format(너비, 높이)
    Inqubo_inani = subprocess.Popen(['python3', str(기준/'Amathuluzi/yenza_umyalo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', linganisa_I_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    isiqoki_a916db4e = selectors.DefaultSelector(); isiqoki_a916db4e.register(Inqubo_inani.stdout, selectors.EVENT_READ)
    loga_umugqa = bytearray(); kude_inani = None; dlulisa_inani_630ba093 = None

    def 기다리기(khombisa_inani, Sebenzisa=0):
        마감 = time.monotonic() + 60
        while khombisa_inani not in loga_umugqa[Sebenzisa:]:
            if time.monotonic() > 마감 or Inqubo_inani.poll() is not None or b'HALTED' in loga_umugqa or b'PANIC:' in loga_umugqa:
                raise AssertionError(loga_umugqa[Sebenzisa:].decode('utf-8', 'replace'))
            for isigameko, _ in isiqoki_a916db4e.select(.1):
                imininingwane = isigameko.fileobj.read(65536)
                if imininingwane: loga_umugqa.extend(imininingwane)
        return loga_umugqa[Sebenzisa:].decode('utf-8', 'replace')

    def qhafaza_inkinobho(uphawu_ad6f1a96, 눌림=True): kude_inani.sendall(struct.pack('>BBHI', 4, int(눌림), 0, uphawu_ad6f1a96))

    def thumela_i_SMS(Itekisi):
        Sebenzisa = len(loga_umugqa)
        for uhlamvusimo_inani in Itekisi:
            uphawu_ad6f1a96 = 0xff0d if uhlamvusimo_inani == '\n' else ord(uhlamvusimo_inani) if ord(uhlamvusimo_inani) < 256 else 0x1000000 | ord(uhlamvusimo_inani)
            qhafaza_inkinobho(uphawu_ad6f1a96); qhafaza_inkinobho(uphawu_ad6f1a96, False)
        return Sebenzisa

    def isihumushi_miyalelo(Itekisi): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', thumela_i_SMS(Itekisi+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kude_inani.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def qhafaza_inani(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def isithombe_samabhithi_isithombe():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ulwazi_ngokwenzekile_imininingwane 너비를 쓴다.
        kude_inani.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        umdwebo_inani = Image.new('RGB', (너비, 높이)); indawo_inani = 0
        while True:
            종류 = 정확한값(kude_inani, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ubude_inani = struct.unpack('>I', 정확한값(kude_inani, 7)[3:])[0]; 정확한값(kude_inani, ubude_inani); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kude_inani, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ubude_inani, ukubhala_ngokufihla_inani = struct.unpack('>HHHHi', 정확한값(kude_inani, 12))
                assert ukubhala_ngokufihla_inani == 0 and 가로+폭 <= 너비 and 세로+ubude_inani <= 높이
                umdwebo_inani.paste(Image.frombytes('RGB', (폭, ubude_inani), 정확한값(kude_inani, 폭*ubude_inani*4), 'raw', 'BGRX'), (가로, 세로))
                indawo_inani += 폭*ubude_inani
            if indawo_inani:
                assert indawo_inani == 너비*높이, indawo_inani
                return umdwebo_inani

    def hlola_i_pel(iphuzumkhathi_inani, 색):
        마감 = time.monotonic()+10
        while True:
            umdwebo_inani = isithombe_samabhithi_isithombe()
            if umdwebo_inani.getpixel(iphuzumkhathi_inani) == 색: return umdwebo_inani
            if time.monotonic() > 마감: raise AssertionError((iphuzumkhathi_inani, umdwebo_inani.getpixel(iphuzumkhathi_inani), 색))

    def layisha_Amafayela(Igama, imininingwane): dlulisa_inani_630ba093.storbinary('STOR '+Igama, io.BytesIO(imininingwane))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+linganisa_I_SMS+' RGB32').encode() in loga_umugqa
        print('BOOT:', linganisa_I_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', loga_umugqa).group(1))
        kude_inani = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kude_inani, 12) == b'RFB 003.008\n'; kude_inani.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kude_inani, 정확한값(kude_inani, 1)[0]); kude_inani.sendall(b'\x01')
        assert 정확한값(kude_inani, 4) == b'\0'*4; kude_inani.sendall(b'\x01')
        초기 = 정확한값(kude_inani, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kude_inani, struct.unpack('>I', 초기[20:])[0])
        kude_inani.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kude_inani.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        hlola_i_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        hlola_i_pel((너비-568, 높이-360), (32, 80, 144))
        Sebenzisa = len(loga_umugqa); qhafaza_inani(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Sebenzisa)
        hlola_i_pel((너비-568, 높이-360), (24, 32, 48))
        Sebenzisa = len(loga_umugqa); qhafaza_inani(80, 16); 기다리기(b'TERMINAL FOCUS 1', Sebenzisa)
        isihumushi_miyalelo('ftpd start')
        dlulisa_inani_630ba093 = ftplib.FTP(); dlulisa_inani_630ba093.encoding = 'utf-8'; dlulisa_inani_630ba093.connect('127.0.0.1', 접속번호, timeout=20); dlulisa_inani_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·isiqeshana 밖·빈 사각형을 포함한다.
        umthombo = '''#include <화면규약.h>
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
    bhala_ifayela_imininingwane(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Amafayela('화면시험.c', umthombo.encode())
        assert 'exit 0' in isihumushi_miyalelo('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', thumela_i_SMS('run /화면시험\n'))
        hlola_i_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        umthombo = '''from Isi_Zulu import 화면크기, 네모그리기, 그림기다리기, 출력, isistimu_iphutha
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except isistimu_iphutha as Iphutha:
    assert Iphutha.thola_inkomba == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Amafayela('화면시험.py', umthombo.encode())
        기다리기(b'PYTHON RESOLUTION PASS', thumela_i_SMS('python /화면시험.py\n'))
        hlola_i_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        umthombo = '''import Isi_Zulu.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ubungako");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("isiqeshana"); }
        catch (잘못된인수예외 Iphutha) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 singatha javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(umthombo.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        layisha_Amafayela('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', thumela_i_SMS('java 해상도경계시험\n'))
        hlola_i_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        # 게스트 javac의 uxhaso_inani 문법으로 Ubungako umbuzo_inani·지우기·다섯 인수 그리기를 컴파일한다.
        umthombo = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Isi_Zulu.자체.화면.너비();
        int 높이=Isi_Zulu.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Isi_Zulu.자체.화면.지우기(3153944);
        Isi_Zulu.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Isi_Zulu.자체.출력.bhala_umugqa("JAVA RESOLUTION PASS");
        Isi_Zulu.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Amafayela('해상도시험.java', umthombo.encode())
        결과 = isihumushi_miyalelo('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', thumela_i_SMS('java 해상도시험\n'))
        hlola_i_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        layisha_Amafayela('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', thumela_i_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        umdwebo_inani = hlola_i_pel((가로, 세로), (32, 80, 144))
        umdwebo_inani.save(str(결과경로/(linganisa_I_SMS+'.png')))
        Sebenzisa = len(loga_umugqa); qhafaza_inani(가로+80, 세로+155)
        기다리기('SWING CLICK Igama'.encode(), Sebenzisa)
        Sebenzisa = len(loga_umugqa); qhafaza_inani(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Sebenzisa)
        assert 'AFTER_RESOLUTION' in isihumushi_miyalelo('echo AFTER_RESOLUTION')
        print('PASS:', linganisa_I_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if dlulisa_inani_630ba093: dlulisa_inani_630ba093.close()
        if kude_inani: kude_inani.close()
        if Inqubo_inani.poll() is None:
            Inqubo_inani.terminate()
            try: Inqubo_inani.wait(timeout=8)
            except subprocess.TimeoutExpired: Inqubo_inani.kill(); Inqubo_inani.wait()
        isiqoki_a916db4e.close(); Inqubo_inani.stdout.close()
        (결과경로/(linganisa_I_SMS+'.log')).write_bytes(loga_umugqa)


def Sebenzisa():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    loga_umugqa = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for akusikho_inani in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Amathuluzi/yenza_umyalo.py'), '--resolution', akusikho_inani], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); loga_umugqa['resolutions'].append([너비, 높이])
        loga_umugqa.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(loga_umugqa, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Sebenzisa()
