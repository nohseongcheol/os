#!/usr/bin/env python3
"""benetako_datuak QEMU/VNC에서 화면 Tamaina·경계·Leihoa eraman_balio·Swing·언어별 그리기를 검사한다."""
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
from mahaigain_ikusi import BERDIN_balio
from exekutatu_komando import Project_erro


def 해상도시험(너비, 높이, neurria_bide_izen):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ataka_zenbaki = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    prozesu_balio = subprocess.Popen(['python3', str(Project_erro/'Tresnak/exekutatu_komando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ataka_zenbaki), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(prozesu_balio.stdout, selectors.EVENT_READ)
    LOG_marka = bytearray(); urruneko_balio = None; transferitu_balio = None

    def 기다리기(erakutsi_balio, Exekutatu_2=0):
        마감 = time.monotonic() + 60
        while erakutsi_balio not in LOG_marka[Exekutatu_2:]:
            if time.monotonic() > 마감 or prozesu_balio.poll() is not None or b'HALTED' in LOG_marka or b'PANIC:' in LOG_marka:
                raise AssertionError(LOG_marka[Exekutatu_2:].decode('utf-8', 'replace'))
            for Gertaera, _ in 선택기.select(.1):
                datuak = Gertaera.fileobj.read(65536)
                if datuak: LOG_marka.extend(datuak)
        return LOG_marka[Exekutatu_2:].decode('utf-8', 'replace')

    def klik_botoi(ikur, 눌림=True): urruneko_balio.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ikur))

    def bidali_SMSa(Testua):
        Exekutatu_2 = len(LOG_marka)
        for karaktere_balio in Testua:
            ikur = 0xff0d if karaktere_balio == '\n' else ord(karaktere_balio) if ord(karaktere_balio) < 256 else 0x1000000 | ord(karaktere_balio)
            klik_botoi(ikur); klik_botoi(ikur, False)
        return Exekutatu_2

    def shell(Testua): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', bidali_SMSa(Testua+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Bertikala_kargu, 눌림): urruneko_balio.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Bertikala_kargu))

    def klik_balio(가로, Bertikala_kargu): 가리키기(가로, Bertikala_kargu, 1); 가리키기(가로, Bertikala_kargu, 0)

    def bit_mapa_irudi():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 benetako_datuak 너비를 쓴다.
        urruneko_balio.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); area_balio = 0
        while True:
            종류 = BERDIN_balio(urruneko_balio, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                luzera_balio = struct.unpack('>I', BERDIN_balio(urruneko_balio, 7)[3:])[0]; BERDIN_balio(urruneko_balio, luzera_balio); continue
            assert 종류 == 0, 종류
            elementu_ZENBATU = struct.unpack('>H', BERDIN_balio(urruneko_balio, 3)[1:])[0]
            for _ in range(elementu_ZENBATU):
                가로, Bertikala_kargu, 폭, luzera_balio, kodeketa_balio = struct.unpack('>HHHHi', BERDIN_balio(urruneko_balio, 12))
                assert kodeketa_balio == 0 and 가로+폭 <= 너비 and Bertikala_kargu+luzera_balio <= 높이
                그림.paste(Image.frombytes('RGB', (폭, luzera_balio), BERDIN_balio(urruneko_balio, 폭*luzera_balio*4), 'raw', 'BGRX'), (가로, Bertikala_kargu))
                area_balio += 폭*luzera_balio
            if area_balio:
                assert area_balio == 너비*높이, area_balio
                return 그림

    def txeke_pixel(koordenatu_balio, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = bit_mapa_irudi()
            if 그림.getpixel(koordenatu_balio) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((koordenatu_balio, 그림.getpixel(koordenatu_balio), 색))

    def Upload_Fitxategiak(Izena, datuak): transferitu_balio.storbinary('STOR '+Izena, io.BytesIO(datuak))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in LOG_marka
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_marka).group(1))
        urruneko_balio = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert BERDIN_balio(urruneko_balio, 12) == b'RFB 003.008\n'; urruneko_balio.sendall(b'RFB 003.008\n')
        assert 1 in BERDIN_balio(urruneko_balio, BERDIN_balio(urruneko_balio, 1)[0]); urruneko_balio.sendall(b'\x01')
        assert BERDIN_balio(urruneko_balio, 4) == b'\0'*4; urruneko_balio.sendall(b'\x01')
        초기 = BERDIN_balio(urruneko_balio, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        BERDIN_balio(urruneko_balio, struct.unpack('>I', 초기[20:])[0])
        urruneko_balio.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        urruneko_balio.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        txeke_pixel((너비-1, 높이-1), (24, 32, 48))
        # 화면 ESKUIN 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        txeke_pixel((너비-568, 높이-360), (32, 80, 144))
        Exekutatu_2 = len(LOG_marka); klik_balio(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Exekutatu_2)
        txeke_pixel((너비-568, 높이-360), (24, 32, 48))
        Exekutatu_2 = len(LOG_marka); klik_balio(80, 16); 기다리기(b'TERMINAL FOCUS 1', Exekutatu_2)
        shell('ftpd start')
        transferitu_balio = ftplib.FTP(); transferitu_balio.encoding = 'utf-8'; transferitu_balio.connect('127.0.0.1', ataka_zenbaki, timeout=20); transferitu_balio.login()
        # C 경계 검사는 32비트 unsigned 음수 BIHURTU_balio·klip 밖·빈 사각형을 포함한다.
        ITURBURUA = '''#include <화면규약.h>
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
    idatzi_fitxategi_datuak(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fitxategiak('화면시험.c', ITURBURUA.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', bidali_SMSa('run /화면시험\n'))
        txeke_pixel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', bidali_SMSa('q'))
        ITURBURUA = '''from Euskara import 화면크기, 네모그리기, 그림기다리기, Irteera, sistema_errore
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistema_errore as errorea:
    assert errorea.INDIZE == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Irteera("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fitxategiak('화면시험.py', ITURBURUA.encode())
        기다리기(b'PYTHON RESOLUTION PASS', bidali_SMSa('python /화면시험.py\n'))
        txeke_pixel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', bidali_SMSa('q'))
        ITURBURUA = '''import Euskara.자체.*;
public class 해상도시험 {
    public static void main(String[] Argumentuak) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Egoera_salbuespen("Tamaina");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new Egoera_salbuespen("klip"); }
        catch (baliogabe_arg_salbuespen errorea) { }
        화면.ezabatu_sarrera(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # salbuespen 처리는 Ostalari javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = neurria_bide_izen/'해상도경계시험.java'
        경계원문.write_text(ITURBURUA.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_erro/'dist/jkoros-native-korean.jar'), '-d', str(neurria_bide_izen), str(경계원문)])
        Upload_Fitxategiak('해상도경계시험.class', (neurria_bide_izen/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', bidali_SMSa('java 해상도경계시험\n'))
        txeke_pixel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', bidali_SMSa('q'))
        # 게스트 javac의 Laguntza_balio 문법으로 Tamaina kontsulta_balio·ezabatu_sarrera·다섯 Argumentuak 그리기를 컴파일한다.
        ITURBURUA = '''public class 해상도시험 {
    public static void main(String[] Argumentuak) {
        int 너비=Euskara.자체.화면.너비();
        int 높이=Euskara.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Euskara.자체.화면.ezabatu_sarrera(3153944);
        Euskara.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Euskara.자체.Irteera.idatzi_lerro("JAVA RESOLUTION PASS");
        Euskara.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fitxategiak('해상도시험.java', ITURBURUA.encode())
        EMAITZA = shell('javac 해상도시험.java'); assert 'exit 0' in EMAITZA, EMAITZA
        기다리기(b'JAVA RESOLUTION PASS', bidali_SMSa('java 해상도시험\n'))
        txeke_pixel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', bidali_SMSa('q'))
        Upload_Fitxategiak('스윙시험.class', (neurria_bide_izen/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', bidali_SMSa('java 스윙시험\n'))
        가로, Bertikala_kargu = (너비-400)//2, (높이-280)//2
        그림 = txeke_pixel((가로, Bertikala_kargu), (32, 80, 144))
        그림.save(str(neurria_bide_izen/(크기글+'.png')))
        Exekutatu_2 = len(LOG_marka); klik_balio(가로+80, Bertikala_kargu+155)
        기다리기('SWING CLICK Izena'.encode(), Exekutatu_2)
        Exekutatu_2 = len(LOG_marka); klik_balio(가로+385, Bertikala_kargu+15); 기다리기(b'jkoros-native> ', Exekutatu_2)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', 크기글, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if transferitu_balio: transferitu_balio.close()
        if urruneko_balio: urruneko_balio.close()
        if prozesu_balio.poll() is None:
            prozesu_balio.terminate()
            try: prozesu_balio.wait(timeout=8)
            except subprocess.TimeoutExpired: prozesu_balio.kill(); prozesu_balio.wait()
        선택기.close(); prozesu_balio.stdout.close()
        (neurria_bide_izen/(크기글+'.log')).write_bytes(LOG_marka)


def Exekutatu_2():
    neurria_bide_izen = Project_erro/'build/verification/resolution'; neurria_bide_izen.mkdir(parents=True, exist_ok=True)
    LOG_marka = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for baliogabe_balio in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            EMAITZA = subprocess.run(['python3', str(Project_erro/'Tresnak/exekutatu_komando.py'), '--resolution', baliogabe_balio], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert EMAITZA.returncode == 2 and b'--resolution' in EMAITZA.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(neurria_bide_izen), str(Project_erro/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, neurria_bide_izen); LOG_marka['resolutions'].append([너비, 높이])
        LOG_marka.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (neurria_bide_izen/'report.json').write_text(json.dumps(LOG_marka, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Exekutatu_2()
