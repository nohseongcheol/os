#!/usr/bin/env python3
"""taannallarik_titiqqat QEMU/VNC에서 화면 anininga·경계·igalaangujaq nuulli_atuutilik·Swing·언어별 그리기를 검사한다."""
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
from igalaujaq_takussarurli import 정확한값
from 실행 import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    anininga_titiqqaq = '{}x{}'.format(너비, 높이)
    Pivallianiq_atuutilik = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', anininga_titiqqaq], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Pivallianiq_atuutilik.stdout, selectors.EVENT_READ)
    papattivik_sanimukutaak = bytearray(); ungasittuq_atuutilik = None; aullaaqtilli_atuutilik = None

    def 기다리기(saqqilli_atuutilik, 시작=0):
        마감 = time.monotonic() + 60
        while saqqilli_atuutilik not in papattivik_sanimukutaak[시작:]:
            if time.monotonic() > 마감 or Pivallianiq_atuutilik.poll() is not None or b'HALTED' in papattivik_sanimukutaak or b'PANIC:' in papattivik_sanimukutaak:
                raise AssertionError(papattivik_sanimukutaak[시작:].decode('utf-8', 'replace'))
            for piniku, _ in 선택기.select(.1):
                titiqqat = piniku.fileobj.read(65536)
                if titiqqat: papattivik_sanimukutaak.extend(titiqqat)
        return papattivik_sanimukutaak[시작:].decode('utf-8', 'replace')

    def naqilli_tikkuagaq(기호, 눌림=True): ungasittuq_atuutilik.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def nassiutili_titiqqaq(titiqqaq):
        시작 = len(papattivik_sanimukutaak)
        for immikkuuqtuq_atuutilik in titiqqaq:
            기호 = 0xff0d if immikkuuqtuq_atuutilik == '\n' else ord(immikkuuqtuq_atuutilik) if ord(immikkuuqtuq_atuutilik) < 256 else 0x1000000 | ord(immikkuuqtuq_atuutilik)
            naqilli_tikkuagaq(기호); naqilli_tikkuagaq(기호, False)
        return 시작

    def piqujijjutiliriji(titiqqaq): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', nassiutili_titiqqaq(titiqqaq+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ungasittuq_atuutilik.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def naqilli_atuutilik(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Bitmap_ajjinnguaq():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 taannallarik_titiqqat 너비를 쓴다.
        ungasittuq_atuutilik.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        titiraujarniq_atuutilik = Image.new('RGB', (너비, 높이)); sukuttia_atuutilik_9285603e = 0
        while True:
            종류 = 정확한값(ungasittuq_atuutilik, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                takininga_atuutilik = struct.unpack('>I', 정확한값(ungasittuq_atuutilik, 7)[3:])[0]; 정확한값(ungasittuq_atuutilik, takininga_atuutilik); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ungasittuq_atuutilik, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, takininga_atuutilik, tukiniktiri_atuutilik = struct.unpack('>HHHHi', 정확한값(ungasittuq_atuutilik, 12))
                assert tukiniktiri_atuutilik == 0 and 가로+폭 <= 너비 and 세로+takininga_atuutilik <= 높이
                titiraujarniq_atuutilik.paste(Image.frombytes('RGB', (폭, takininga_atuutilik), 정확한값(ungasittuq_atuutilik, 폭*takininga_atuutilik*4), 'raw', 'BGRX'), (가로, 세로))
                sukuttia_atuutilik_9285603e += 폭*takininga_atuutilik
            if sukuttia_atuutilik_9285603e:
                assert sukuttia_atuutilik_9285603e == 너비*높이, sukuttia_atuutilik_9285603e
                return titiraujarniq_atuutilik

    def qaujigiarli_pel(pittariik_atuutilik, 색):
        마감 = time.monotonic()+10
        while True:
            titiraujarniq_atuutilik = Bitmap_ajjinnguaq()
            if titiraujarniq_atuutilik.getpixel(pittariik_atuutilik) == 색: return titiraujarniq_atuutilik
            if time.monotonic() > 마감: raise AssertionError((pittariik_atuutilik, titiraujarniq_atuutilik.getpixel(pittariik_atuutilik), 색))

    def 올리기(atiq, titiqqat): aullaaqtilli_atuutilik.storbinary('STOR '+atiq, io.BytesIO(titiqqat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+anininga_titiqqaq+' RGB32').encode() in papattivik_sanimukutaak
        print('BOOT:', anininga_titiqqaq, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', papattivik_sanimukutaak).group(1))
        ungasittuq_atuutilik = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ungasittuq_atuutilik, 12) == b'RFB 003.008\n'; ungasittuq_atuutilik.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ungasittuq_atuutilik, 정확한값(ungasittuq_atuutilik, 1)[0]); ungasittuq_atuutilik.sendall(b'\x01')
        assert 정확한값(ungasittuq_atuutilik, 4) == b'\0'*4; ungasittuq_atuutilik.sendall(b'\x01')
        초기 = 정확한값(ungasittuq_atuutilik, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ungasittuq_atuutilik, struct.unpack('>I', 초기[20:])[0])
        ungasittuq_atuutilik.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ungasittuq_atuutilik.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        qaujigiarli_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        qaujigiarli_pel((너비-568, 높이-360), (32, 80, 144))
        시작 = len(papattivik_sanimukutaak); naqilli_atuutilik(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', 시작)
        qaujigiarli_pel((너비-568, 높이-360), (24, 32, 48))
        시작 = len(papattivik_sanimukutaak); naqilli_atuutilik(80, 16); 기다리기(b'TERMINAL FOCUS 1', 시작)
        piqujijjutiliriji('ftpd start')
        aullaaqtilli_atuutilik = ftplib.FTP(); aullaaqtilli_atuutilik.encoding = 'utf-8'; aullaaqtilli_atuutilik.connect('127.0.0.1', 접속번호, timeout=20); aullaaqtilli_atuutilik.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·Nakatigat 밖·빈 사각형을 포함한다.
        pivviujuq = '''#include <화면규약.h>
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
    titiraq_ini_titiqqat(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.c', pivviujuq.encode())
        assert 'exit 0' in piqujijjutiliriji('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', nassiutili_titiqqaq('run /화면시험\n'))
        qaujigiarli_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', nassiutili_titiqqaq('q'))
        pivviujuq = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, qarasaujaq_tammarniq
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except qarasaujaq_tammarniq as tammarniq:
    assert tammarniq.nalunaiqsimavik == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.py', pivviujuq.encode())
        기다리기(b'PYTHON RESOLUTION PASS', nassiutili_titiqqaq('python /화면시험.py\n'))
        qaujigiarli_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', nassiutili_titiqqaq('q'))
        pivviujuq = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("anininga");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("Nakatigat"); }
        catch (잘못된인수예외 tammarniq) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 tuttarvik javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(pivviujuq.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        올리기('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', nassiutili_titiqqaq('java 해상도경계시험\n'))
        qaujigiarli_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', nassiutili_titiqqaq('q'))
        # 게스트 javac의 ikajuqsuiniq_atuutilik 문법으로 anininga kiggusiqarialik_atuutilik·지우기·다섯 인수 그리기를 컴파일한다.
        pivviujuq = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.titiraq_titikutaak("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('해상도시험.java', pivviujuq.encode())
        결과 = piqujijjutiliriji('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', nassiutili_titiqqaq('java 해상도시험\n'))
        qaujigiarli_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', nassiutili_titiqqaq('q'))
        올리기('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', nassiutili_titiqqaq('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        titiraujarniq_atuutilik = qaujigiarli_pel((가로, 세로), (32, 80, 144))
        titiraujarniq_atuutilik.save(str(결과경로/(anininga_titiqqaq+'.png')))
        시작 = len(papattivik_sanimukutaak); naqilli_atuutilik(가로+80, 세로+155)
        기다리기('SWING CLICK atiq'.encode(), 시작)
        시작 = len(papattivik_sanimukutaak); naqilli_atuutilik(가로+385, 세로+15); 기다리기(b'jkoros-native> ', 시작)
        assert 'AFTER_RESOLUTION' in piqujijjutiliriji('echo AFTER_RESOLUTION')
        print('PASS:', anininga_titiqqaq, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if aullaaqtilli_atuutilik: aullaaqtilli_atuutilik.close()
        if ungasittuq_atuutilik: ungasittuq_atuutilik.close()
        if Pivallianiq_atuutilik.poll() is None:
            Pivallianiq_atuutilik.terminate()
            try: Pivallianiq_atuutilik.wait(timeout=8)
            except subprocess.TimeoutExpired: Pivallianiq_atuutilik.kill(); Pivallianiq_atuutilik.wait()
        선택기.close(); Pivallianiq_atuutilik.stdout.close()
        (결과경로/(anininga_titiqqaq+'.log')).write_bytes(papattivik_sanimukutaak)


def 시작():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    papattivik_sanimukutaak = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for naammangittuq_atuutilik in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'도구/실행.py'), '--resolution', naammangittuq_atuutilik], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); papattivik_sanimukutaak['resolutions'].append([너비, 높이])
        papattivik_sanimukutaak.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(papattivik_sanimukutaak, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': 시작()
