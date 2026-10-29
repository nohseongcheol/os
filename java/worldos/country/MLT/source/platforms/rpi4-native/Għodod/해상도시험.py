#!/usr/bin/env python3
"""attwali_data QEMU/VNC에서 화면 daqqas·경계·tieqa mexxi_VALUE·Swing·언어별 그리기를 검사한다."""
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
from desktop_wera import EXACT_VALUE
from eżegwixxa_kmand import pprojetta_għerq


def 해상도시험(너비, 높이, miżura_mogħdija):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    daqqas_SMS = '{}x{}'.format(너비, 높이)
    Proċess_VALUE = subprocess.Popen(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', daqqas_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettur_a916db4e = selectors.DefaultSelector(); selettur_a916db4e.register(Proċess_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); mill_bogħod_VALUE = None; trasferiment_VALUE = None

    def 기다리기(wera_VALUE_487749b8, serje=0):
        마감 = time.monotonic() + 60
        while wera_VALUE_487749b8 not in LOG_RECORD[serje:]:
            if time.monotonic() > 마감 or Proċess_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[serje:].decode('utf-8', 'replace'))
            for avveniment, _ in selettur_a916db4e.select(.1):
                data = avveniment.fileobj.read(65536)
                if data: LOG_RECORD.extend(data)
        return LOG_RECORD[serje:].decode('utf-8', 'replace')

    def klikkja_buttuna(simbolu, 눌림=True): mill_bogħod_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolu))

    def ibgħat_SMS(SMS):
        serje = len(LOG_RECORD)
        for karattru_VALUE in SMS:
            simbolu = 0xff0d if karattru_VALUE == '\n' else ord(karattru_VALUE) if ord(karattru_VALUE) < 256 else 0x1000000 | ord(karattru_VALUE)
            klikkja_buttuna(simbolu); klikkja_buttuna(simbolu, False)
        return serje

    def shell(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ibgħat_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Vertikali_pożizzjoni, 눌림): mill_bogħod_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikali_pożizzjoni))

    def klikkja_VALUE(가로, Vertikali_pożizzjoni): 가리키기(가로, Vertikali_pożizzjoni, 1); 가리키기(가로, Vertikali_pożizzjoni, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 attwali_data 너비를 쓴다.
        mill_bogħod_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tpinġija_VALUE = Image.new('RGB', (너비, 높이)); żona_VALUE = 0
        while True:
            종류 = EXACT_VALUE(mill_bogħod_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                tul_VALUE = struct.unpack('>I', EXACT_VALUE(mill_bogħod_VALUE, 7)[3:])[0]; EXACT_VALUE(mill_bogħod_VALUE, tul_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(mill_bogħod_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Vertikali_pożizzjoni, 폭, tul_VALUE, kodifikar_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(mill_bogħod_VALUE, 12))
                assert kodifikar_VALUE == 0 and 가로+폭 <= 너비 and Vertikali_pożizzjoni+tul_VALUE <= 높이
                tpinġija_VALUE.paste(Image.frombytes('RGB', (폭, tul_VALUE), EXACT_VALUE(mill_bogħod_VALUE, 폭*tul_VALUE*4), 'raw', 'BGRX'), (가로, Vertikali_pożizzjoni))
                żona_VALUE += 폭*tul_VALUE
            if żona_VALUE:
                assert żona_VALUE == 너비*높이, żona_VALUE
                return tpinġija_VALUE

    def ċekk_pel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            tpinġija_VALUE = bitmap_IMAGE()
            if tpinġija_VALUE.getpixel(koordinat_VALUE) == 색: return tpinġija_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, tpinġija_VALUE.getpixel(koordinat_VALUE), 색))

    def tella_Fajls(isem, data): trasferiment_VALUE.storbinary('STOR '+isem, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+daqqas_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', daqqas_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        mill_bogħod_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(mill_bogħod_VALUE, 12) == b'RFB 003.008\n'; mill_bogħod_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(mill_bogħod_VALUE, EXACT_VALUE(mill_bogħod_VALUE, 1)[0]); mill_bogħod_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(mill_bogħod_VALUE, 4) == b'\0'*4; mill_bogħod_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(mill_bogħod_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(mill_bogħod_VALUE, struct.unpack('>I', 초기[20:])[0])
        mill_bogħod_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        mill_bogħod_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ċekk_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ċekk_pel((너비-568, 높이-360), (32, 80, 144))
        serje = len(LOG_RECORD); klikkja_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', serje)
        ċekk_pel((너비-568, 높이-360), (24, 32, 48))
        serje = len(LOG_RECORD); klikkja_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', serje)
        shell('ftpd start')
        trasferiment_VALUE = ftplib.FTP(); trasferiment_VALUE.encoding = 'utf-8'; trasferiment_VALUE.connect('127.0.0.1', 접속번호, timeout=20); trasferiment_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klipp 밖·빈 사각형을 포함한다.
        sors = '''#include <화면규약.h>
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
    kiteb_fajl_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tella_Fajls('화면시험.c', sors.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ibgħat_SMS('run /화면시험\n'))
        ċekk_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ibgħat_SMS('q'))
        sors = '''from Malti import 화면크기, 네모그리기, 그림기다리기, 출력, sistema_żball
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistema_żball as żball:
    assert żball.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tella_Fajls('화면시험.py', sors.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ibgħat_SMS('python /화면시험.py\n'))
        ċekk_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ibgħat_SMS('q'))
        sors = '''import Malti.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("daqqas");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("klipp"); }
        catch (잘못된인수예외 żball) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 host javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = miżura_mogħdija/'해상도경계시험.java'
        경계원문.write_text(sors.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(pprojetta_għerq/'dist/jkoros-native-korean.jar'), '-d', str(miżura_mogħdija), str(경계원문)])
        tella_Fajls('해상도경계시험.class', (miżura_mogħdija/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ibgħat_SMS('java 해상도경계시험\n'))
        ċekk_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ibgħat_SMS('q'))
        # 게스트 javac의 Appoġġ_VALUE 문법으로 daqqas query_VALUE·지우기·다섯 인수 그리기를 컴파일한다.
        sors = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Malti.자체.화면.너비();
        int 높이=Malti.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Malti.자체.화면.지우기(3153944);
        Malti.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Malti.자체.출력.kiteb_linja("JAVA RESOLUTION PASS");
        Malti.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tella_Fajls('해상도시험.java', sors.encode())
        miżura = shell('javac 해상도시험.java'); assert 'exit 0' in miżura, miżura
        기다리기(b'JAVA RESOLUTION PASS', ibgħat_SMS('java 해상도시험\n'))
        ċekk_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ibgħat_SMS('q'))
        tella_Fajls('스윙시험.class', (miżura_mogħdija/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ibgħat_SMS('java 스윙시험\n'))
        가로, Vertikali_pożizzjoni = (너비-400)//2, (높이-280)//2
        tpinġija_VALUE = ċekk_pel((가로, Vertikali_pożizzjoni), (32, 80, 144))
        tpinġija_VALUE.save(str(miżura_mogħdija/(daqqas_SMS+'.png')))
        serje = len(LOG_RECORD); klikkja_VALUE(가로+80, Vertikali_pożizzjoni+155)
        기다리기('SWING CLICK isem'.encode(), serje)
        serje = len(LOG_RECORD); klikkja_VALUE(가로+385, Vertikali_pożizzjoni+15); 기다리기(b'jkoros-native> ', serje)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', daqqas_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if trasferiment_VALUE: trasferiment_VALUE.close()
        if mill_bogħod_VALUE: mill_bogħod_VALUE.close()
        if Proċess_VALUE.poll() is None:
            Proċess_VALUE.terminate()
            try: Proċess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proċess_VALUE.kill(); Proċess_VALUE.wait()
        selettur_a916db4e.close(); Proċess_VALUE.stdout.close()
        (miżura_mogħdija/(daqqas_SMS+'.log')).write_bytes(LOG_RECORD)


def serje():
    miżura_mogħdija = pprojetta_għerq/'build/verification/resolution'; miżura_mogħdija.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for invalidu_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            miżura = subprocess.run(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'), '--resolution', invalidu_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert miżura.returncode == 2 and b'--resolution' in miżura.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(miżura_mogħdija), str(pprojetta_għerq/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, miżura_mogħdija); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (miżura_mogħdija/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': serje()
