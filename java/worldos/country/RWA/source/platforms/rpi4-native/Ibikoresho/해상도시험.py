#!/usr/bin/env python3
"""nyakuri_amakurushingiro QEMU/VNC에서 화면 Ingano·경계·idirishya kwimura_agaciro·Swing·언어별 그리기를 검사한다."""
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
from biro_igaragaza import 정확한값
from gukora_ibwiriza import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ingano_SMS = '{}x{}'.format(너비, 높이)
    Inzira_agaciro = subprocess.Popen(['python3', str(기준/'Ibikoresho/gukora_ibwiriza.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ingano_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    muhitamo_a916db4e = selectors.DefaultSelector(); muhitamo_a916db4e.register(Inzira_agaciro.stdout, selectors.EVENT_READ)
    kubika_umurongo = bytearray(); kure_agaciro = None; iyimura_agaciro = None

    def 기다리기(kugaragaza_agaciro, ihuriro=0):
        마감 = time.monotonic() + 60
        while kugaragaza_agaciro not in kubika_umurongo[ihuriro:]:
            if time.monotonic() > 마감 or Inzira_agaciro.poll() is not None or b'HALTED' in kubika_umurongo or b'PANIC:' in kubika_umurongo:
                raise AssertionError(kubika_umurongo[ihuriro:].decode('utf-8', 'replace'))
            for icyabaye, _ in muhitamo_a916db4e.select(.1):
                amakurushingiro = icyabaye.fileobj.read(65536)
                if amakurushingiro: kubika_umurongo.extend(amakurushingiro)
        return kubika_umurongo[ihuriro:].decode('utf-8', 'replace')

    def gukanda_buto(ikimenyetso, 눌림=True): kure_agaciro.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ikimenyetso))

    def ohereza_SMS(Umwandiko):
        ihuriro = len(kubika_umurongo)
        for inyuguti_agaciro in Umwandiko:
            ikimenyetso = 0xff0d if inyuguti_agaciro == '\n' else ord(inyuguti_agaciro) if ord(inyuguti_agaciro) < 256 else 0x1000000 | ord(inyuguti_agaciro)
            gukanda_buto(ikimenyetso); gukanda_buto(ikimenyetso, False)
        return ihuriro

    def insomamabwiriza(Umwandiko): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ohereza_SMS(Umwandiko+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kure_agaciro.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def gukanda_agaciro(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitimapu_ishusho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 nyakuri_amakurushingiro 너비를 쓴다.
        kure_agaciro.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        igishushanyo_agaciro = Image.new('RGB', (너비, 높이)); akanya_agaciro = 0
        while True:
            종류 = 정확한값(kure_agaciro, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uburebure_agaciro = struct.unpack('>I', 정확한값(kure_agaciro, 7)[3:])[0]; 정확한값(kure_agaciro, uburebure_agaciro); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kure_agaciro, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, uburebure_agaciro, gusobeka_agaciro = struct.unpack('>HHHHi', 정확한값(kure_agaciro, 12))
                assert gusobeka_agaciro == 0 and 가로+폭 <= 너비 and 세로+uburebure_agaciro <= 높이
                igishushanyo_agaciro.paste(Image.frombytes('RGB', (폭, uburebure_agaciro), 정확한값(kure_agaciro, 폭*uburebure_agaciro*4), 'raw', 'BGRX'), (가로, 세로))
                akanya_agaciro += 폭*uburebure_agaciro
            if akanya_agaciro:
                assert akanya_agaciro == 너비*높이, akanya_agaciro
                return igishushanyo_agaciro

    def sheki_pel(guhuza_agaciro, 색):
        마감 = time.monotonic()+10
        while True:
            igishushanyo_agaciro = bitimapu_ishusho()
            if igishushanyo_agaciro.getpixel(guhuza_agaciro) == 색: return igishushanyo_agaciro
            if time.monotonic() > 마감: raise AssertionError((guhuza_agaciro, igishushanyo_agaciro.getpixel(guhuza_agaciro), 색))

    def gukurura_Dosiye(Izina, amakurushingiro): iyimura_agaciro.storbinary('STOR '+Izina, io.BytesIO(amakurushingiro))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ingano_SMS+' RGB32').encode() in kubika_umurongo
        print('BOOT:', ingano_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', kubika_umurongo).group(1))
        kure_agaciro = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kure_agaciro, 12) == b'RFB 003.008\n'; kure_agaciro.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kure_agaciro, 정확한값(kure_agaciro, 1)[0]); kure_agaciro.sendall(b'\x01')
        assert 정확한값(kure_agaciro, 4) == b'\0'*4; kure_agaciro.sendall(b'\x01')
        초기 = 정확한값(kure_agaciro, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kure_agaciro, struct.unpack('>I', 초기[20:])[0])
        kure_agaciro.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kure_agaciro.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        sheki_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        sheki_pel((너비-568, 높이-360), (32, 80, 144))
        ihuriro = len(kubika_umurongo); gukanda_agaciro(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ihuriro)
        sheki_pel((너비-568, 높이-360), (24, 32, 48))
        ihuriro = len(kubika_umurongo); gukanda_agaciro(80, 16); 기다리기(b'TERMINAL FOCUS 1', ihuriro)
        insomamabwiriza('ftpd start')
        iyimura_agaciro = ftplib.FTP(); iyimura_agaciro.encoding = 'utf-8'; iyimura_agaciro.connect('127.0.0.1', 접속번호, timeout=20); iyimura_agaciro.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·kiripu 밖·빈 사각형을 포함한다.
        Inkomoko = '''#include <화면규약.h>
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
    kwandika_dosiye_amakurushingiro(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        gukurura_Dosiye('화면시험.c', Inkomoko.encode())
        assert 'exit 0' in insomamabwiriza('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ohereza_SMS('run /화면시험\n'))
        sheki_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ohereza_SMS('q'))
        Inkomoko = '''from Ikinyarwanda import 화면크기, 네모그리기, 그림기다리기, 출력, sisitemu_ikosa
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sisitemu_ikosa as IKOSA:
    assert IKOSA.umugerekashakiro == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        gukurura_Dosiye('화면시험.py', Inkomoko.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ohereza_SMS('python /화면시험.py\n'))
        sheki_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ohereza_SMS('q'))
        Inkomoko = '''import Ikinyarwanda.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ingano");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("kiripu"); }
        catch (잘못된인수예외 IKOSA) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 gucumbikira javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(Inkomoko.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        gukurura_Dosiye('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ohereza_SMS('java 해상도경계시험\n'))
        sheki_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ohereza_SMS('q'))
        # 게스트 javac의 Ubufasha_agaciro 문법으로 Ingano isaba_agaciro·지우기·다섯 인수 그리기를 컴파일한다.
        Inkomoko = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Ikinyarwanda.자체.화면.너비();
        int 높이=Ikinyarwanda.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Ikinyarwanda.자체.화면.지우기(3153944);
        Ikinyarwanda.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Ikinyarwanda.자체.출력.kwandika_umurongo("JAVA RESOLUTION PASS");
        Ikinyarwanda.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        gukurura_Dosiye('해상도시험.java', Inkomoko.encode())
        결과 = insomamabwiriza('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', ohereza_SMS('java 해상도시험\n'))
        sheki_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ohereza_SMS('q'))
        gukurura_Dosiye('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ohereza_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        igishushanyo_agaciro = sheki_pel((가로, 세로), (32, 80, 144))
        igishushanyo_agaciro.save(str(결과경로/(ingano_SMS+'.png')))
        ihuriro = len(kubika_umurongo); gukanda_agaciro(가로+80, 세로+155)
        기다리기('SWING CLICK Izina'.encode(), ihuriro)
        ihuriro = len(kubika_umurongo); gukanda_agaciro(가로+385, 세로+15); 기다리기(b'jkoros-native> ', ihuriro)
        assert 'AFTER_RESOLUTION' in insomamabwiriza('echo AFTER_RESOLUTION')
        print('PASS:', ingano_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if iyimura_agaciro: iyimura_agaciro.close()
        if kure_agaciro: kure_agaciro.close()
        if Inzira_agaciro.poll() is None:
            Inzira_agaciro.terminate()
            try: Inzira_agaciro.wait(timeout=8)
            except subprocess.TimeoutExpired: Inzira_agaciro.kill(); Inzira_agaciro.wait()
        muhitamo_a916db4e.close(); Inzira_agaciro.stdout.close()
        (결과경로/(ingano_SMS+'.log')).write_bytes(kubika_umurongo)


def ihuriro():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    kubika_umurongo = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for kitemewe_agaciro in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Ibikoresho/gukora_ibwiriza.py'), '--resolution', kitemewe_agaciro], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); kubika_umurongo['resolutions'].append([너비, 높이])
        kubika_umurongo.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(kubika_umurongo, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ihuriro()
