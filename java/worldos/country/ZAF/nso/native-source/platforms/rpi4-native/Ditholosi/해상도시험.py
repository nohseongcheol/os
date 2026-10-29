#!/usr/bin/env python3
"""kgonthe_data QEMU/VNC에서 화면 Bogolo·경계·lefastere šuthiša_boleng·Swing·언어별 그리기를 검사한다."""
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
from teskethopo_pogelo import 정확한값
from phethagatša_taelo import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    bogolo_SMS = '{}x{}'.format(너비, 높이)
    tiragalo_boleng = subprocess.Popen(['python3', str(기준/'Ditholosi/phethagatša_taelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', bogolo_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    sekgethi_a916db4e = selectors.DefaultSelector(); sekgethi_a916db4e.register(tiragalo_boleng.stdout, selectors.EVENT_READ)
    pego_rei = bytearray(); ya_kgole_boleng = None; fetišetša_boleng = None

    def 기다리기(bontšha_boleng, Diriša=0):
        마감 = time.monotonic() + 60
        while bontšha_boleng not in pego_rei[Diriša:]:
            if time.monotonic() > 마감 or tiragalo_boleng.poll() is not None or b'HALTED' in pego_rei or b'PANIC:' in pego_rei:
                raise AssertionError(pego_rei[Diriša:].decode('utf-8', 'replace'))
            for tiragalo, _ in sekgethi_a916db4e.select(.1):
                data = tiragalo.fileobj.read(65536)
                if data: pego_rei.extend(data)
        return pego_rei[Diriša:].decode('utf-8', 'replace')

    def klika_konope(leswao, 눌림=True): ya_kgole_boleng.sendall(struct.pack('>BBHI', 4, int(눌림), 0, leswao))

    def romela_SMS(Sengwalwa):
        Diriša = len(pego_rei)
        for tlhaka_boleng in Sengwalwa:
            leswao = 0xff0d if tlhaka_boleng == '\n' else ord(tlhaka_boleng) if ord(tlhaka_boleng) < 256 else 0x1000000 | ord(tlhaka_boleng)
            klika_konope(leswao); klika_konope(leswao, False)
        return Diriša

    def šele(Sengwalwa): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', romela_SMS(Sengwalwa+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ya_kgole_boleng.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def klika_boleng(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def seswantšho_sa_go_bopša_ka_dikhutlwana_seswantšho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 kgonthe_data 너비를 쓴다.
        ya_kgole_boleng.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        sethalwa_boleng = Image.new('RGB', (너비, 높이)); area_boleng = 0
        while True:
            종류 = 정확한값(ya_kgole_boleng, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                botelele_boleng = struct.unpack('>I', 정확한값(ya_kgole_boleng, 7)[3:])[0]; 정확한값(ya_kgole_boleng, botelele_boleng); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ya_kgole_boleng, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, botelele_boleng, go_enkhouta_boleng = struct.unpack('>HHHHi', 정확한값(ya_kgole_boleng, 12))
                assert go_enkhouta_boleng == 0 and 가로+폭 <= 너비 and 세로+botelele_boleng <= 높이
                sethalwa_boleng.paste(Image.frombytes('RGB', (폭, botelele_boleng), 정확한값(ya_kgole_boleng, 폭*botelele_boleng*4), 'raw', 'BGRX'), (가로, 세로))
                area_boleng += 폭*botelele_boleng
            if area_boleng:
                assert area_boleng == 너비*높이, area_boleng
                return sethalwa_boleng

    def lekola_phele(kgokaganyo_boleng, 색):
        마감 = time.monotonic()+10
        while True:
            sethalwa_boleng = seswantšho_sa_go_bopša_ka_dikhutlwana_seswantšho()
            if sethalwa_boleng.getpixel(kgokaganyo_boleng) == 색: return sethalwa_boleng
            if time.monotonic() > 마감: raise AssertionError((kgokaganyo_boleng, sethalwa_boleng.getpixel(kgokaganyo_boleng), 색))

    def apolouto_Difaele(Leina, data): fetišetša_boleng.storbinary('STOR '+Leina, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+bogolo_SMS+' RGB32').encode() in pego_rei
        print('BOOT:', bogolo_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', pego_rei).group(1))
        ya_kgole_boleng = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ya_kgole_boleng, 12) == b'RFB 003.008\n'; ya_kgole_boleng.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ya_kgole_boleng, 정확한값(ya_kgole_boleng, 1)[0]); ya_kgole_boleng.sendall(b'\x01')
        assert 정확한값(ya_kgole_boleng, 4) == b'\0'*4; ya_kgole_boleng.sendall(b'\x01')
        초기 = 정확한값(ya_kgole_boleng, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ya_kgole_boleng, struct.unpack('>I', 초기[20:])[0])
        ya_kgole_boleng.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ya_kgole_boleng.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        lekola_phele((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        lekola_phele((너비-568, 높이-360), (32, 80, 144))
        Diriša = len(pego_rei); klika_boleng(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Diriša)
        lekola_phele((너비-568, 높이-360), (24, 32, 48))
        Diriša = len(pego_rei); klika_boleng(80, 16); 기다리기(b'TERMINAL FOCUS 1', Diriša)
        šele('ftpd start')
        fetišetša_boleng = ftplib.FTP(); fetišetša_boleng.encoding = 'utf-8'; fetišetša_boleng.connect('127.0.0.1', 접속번호, timeout=20); fetišetša_boleng.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·setsopolwa 밖·빈 사각형을 포함한다.
        mohlodi = '''#include <화면규약.h>
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
    ngwala_faele_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        apolouto_Difaele('화면시험.c', mohlodi.encode())
        assert 'exit 0' in šele('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', romela_SMS('run /화면시험\n'))
        lekola_phele((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        mohlodi = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, lenaneo_phošo
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except lenaneo_phošo as Phošo:
    assert Phošo.lokela == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        apolouto_Difaele('화면시험.py', mohlodi.encode())
        기다리기(b'PYTHON RESOLUTION PASS', romela_SMS('python /화면시험.py\n'))
        lekola_phele((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        mohlodi = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Bogolo");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("setsopolwa"); }
        catch (잘못된인수예외 Phošo) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 go_nea_ditirelo javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(mohlodi.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        apolouto_Difaele('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', romela_SMS('java 해상도경계시험\n'))
        lekola_phele((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        # 게스트 javac의 Thekgo_boleng 문법으로 Bogolo kwiri_boleng·지우기·다섯 인수 그리기를 컴파일한다.
        mohlodi = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ngwala_mothaladi("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        apolouto_Difaele('해상도시험.java', mohlodi.encode())
        결과 = šele('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', romela_SMS('java 해상도시험\n'))
        lekola_phele((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', romela_SMS('q'))
        apolouto_Difaele('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', romela_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        sethalwa_boleng = lekola_phele((가로, 세로), (32, 80, 144))
        sethalwa_boleng.save(str(결과경로/(bogolo_SMS+'.png')))
        Diriša = len(pego_rei); klika_boleng(가로+80, 세로+155)
        기다리기('SWING CLICK Leina'.encode(), Diriša)
        Diriša = len(pego_rei); klika_boleng(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Diriša)
        assert 'AFTER_RESOLUTION' in šele('echo AFTER_RESOLUTION')
        print('PASS:', bogolo_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if fetišetša_boleng: fetišetša_boleng.close()
        if ya_kgole_boleng: ya_kgole_boleng.close()
        if tiragalo_boleng.poll() is None:
            tiragalo_boleng.terminate()
            try: tiragalo_boleng.wait(timeout=8)
            except subprocess.TimeoutExpired: tiragalo_boleng.kill(); tiragalo_boleng.wait()
        sekgethi_a916db4e.close(); tiragalo_boleng.stdout.close()
        (결과경로/(bogolo_SMS+'.log')).write_bytes(pego_rei)


def Diriša():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    pego_rei = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ye_e_phošagetšego_boleng in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Ditholosi/phethagatša_taelo.py'), '--resolution', ye_e_phošagetšego_boleng], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); pego_rei['resolutions'].append([너비, 높이])
        pego_rei.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(pego_rei, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Diriša()
