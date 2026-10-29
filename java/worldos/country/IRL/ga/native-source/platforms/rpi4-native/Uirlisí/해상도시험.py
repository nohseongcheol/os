#!/usr/bin/env python3
"""iarbhír_sonraí QEMU/VNC에서 화면 Méid·경계·fuinneog bog_VALUE·Swing·언어별 그리기를 검사한다."""
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
from deasc_Amharc import EXACT_VALUE
from Rith_ordú import teilgean_fréamh


def 해상도시험(너비, 높이, tomhas_cosán):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); uimhir_phoirt = 임시.getsockname()[1]
    socraigh_méid_SMS = '{}x{}'.format(너비, 높이)
    Próiseas_VALUE = subprocess.Popen(['python3', str(teilgean_fréamh/'Uirlisí/Rith_ordú.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(uimhir_phoirt), '--resolution', socraigh_méid_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnóir_a916db4e = selectors.DefaultSelector(); roghnóir_a916db4e.register(Próiseas_VALUE.stdout, selectors.EVENT_READ)
    LOG_ró = bytearray(); cianda_VALUE = None; traschur_VALUE = None

    def 기다리기(seó_VALUE, Rith_2=0):
        마감 = time.monotonic() + 60
        while seó_VALUE not in LOG_ró[Rith_2:]:
            if time.monotonic() > 마감 or Próiseas_VALUE.poll() is not None or b'HALTED' in LOG_ró or b'PANIC:' in LOG_ró:
                raise AssertionError(LOG_ró[Rith_2:].decode('utf-8', 'replace'))
            for ócáid, _ in roghnóir_a916db4e.select(.1):
                sonraí = ócáid.fileobj.read(65536)
                if sonraí: LOG_ró.extend(sonraí)
        return LOG_ró[Rith_2:].decode('utf-8', 'replace')

    def cliceáil_cnaipe(siombail, 눌림=True): cianda_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, siombail))

    def SMS_a_sheoladh(Téacs):
        Rith_2 = len(LOG_ró)
        for carachtar_VALUE in Téacs:
            siombail = 0xff0d if carachtar_VALUE == '\n' else ord(carachtar_VALUE) if ord(carachtar_VALUE) < 256 else 0x1000000 | ord(carachtar_VALUE)
            cliceáil_cnaipe(siombail); cliceáil_cnaipe(siombail, False)
        return Rith_2

    def blaosc(Téacs): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_a_sheoladh(Téacs+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Ingearach_suíomh, 눌림): cianda_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ingearach_suíomh))

    def cliceáil_VALUE(가로, Ingearach_suíomh): 가리키기(가로, Ingearach_suíomh, 1); 가리키기(가로, Ingearach_suíomh, 0)

    def mapa_giotán_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 iarbhír_sonraí 너비를 쓴다.
        cianda_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        líníocht_VALUE = Image.new('RGB', (너비, 높이)); catagóir_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(cianda_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                fad_VALUE = struct.unpack('>I', EXACT_VALUE(cianda_VALUE, 7)[3:])[0]; EXACT_VALUE(cianda_VALUE, fad_VALUE); continue
            assert 종류 == 0, 종류
            mír_COUNT = struct.unpack('>H', EXACT_VALUE(cianda_VALUE, 3)[1:])[0]
            for _ in range(mír_COUNT):
                가로, Ingearach_suíomh, 폭, fad_VALUE, ionchódú_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(cianda_VALUE, 12))
                assert ionchódú_VALUE == 0 and 가로+폭 <= 너비 and Ingearach_suíomh+fad_VALUE <= 높이
                líníocht_VALUE.paste(Image.frombytes('RGB', (폭, fad_VALUE), EXACT_VALUE(cianda_VALUE, 폭*fad_VALUE*4), 'raw', 'BGRX'), (가로, Ingearach_suíomh))
                catagóir_VALUE_9285603e += 폭*fad_VALUE
            if catagóir_VALUE_9285603e:
                assert catagóir_VALUE_9285603e == 너비*높이, catagóir_VALUE_9285603e
                return líníocht_VALUE

    def seic_picteilín(comhordanáid_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            líníocht_VALUE = mapa_giotán_IMAGE()
            if líníocht_VALUE.getpixel(comhordanáid_VALUE) == 색: return líníocht_VALUE
            if time.monotonic() > 마감: raise AssertionError((comhordanáid_VALUE, líníocht_VALUE.getpixel(comhordanáid_VALUE), 색))

    def uaslódáil_Comhaid(Ainm, sonraí): traschur_VALUE.storbinary('STOR '+Ainm, io.BytesIO(sonraí))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+socraigh_méid_SMS+' RGB32').encode() in LOG_ró
        print('BOOT:', socraigh_méid_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ró).group(1))
        cianda_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(cianda_VALUE, 12) == b'RFB 003.008\n'; cianda_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cianda_VALUE, EXACT_VALUE(cianda_VALUE, 1)[0]); cianda_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(cianda_VALUE, 4) == b'\0'*4; cianda_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(cianda_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(cianda_VALUE, struct.unpack('>I', 초기[20:])[0])
        cianda_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        cianda_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        seic_picteilín((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        seic_picteilín((너비-568, 높이-360), (32, 80, 144))
        Rith_2 = len(LOG_ró); cliceáil_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Rith_2)
        seic_picteilín((너비-568, 높이-360), (24, 32, 48))
        Rith_2 = len(LOG_ró); cliceáil_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Rith_2)
        blaosc('ftpd start')
        traschur_VALUE = ftplib.FTP(); traschur_VALUE.encoding = 'utf-8'; traschur_VALUE.connect('127.0.0.1', uimhir_phoirt, timeout=20); traschur_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·gearrthóg 밖·빈 사각형을 포함한다.
        FOINSE = '''#include <화면규약.h>
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
    scríobh_comhad_sonraí(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uaslódáil_Comhaid('화면시험.c', FOINSE.encode())
        assert 'exit 0' in blaosc('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_a_sheoladh('run /화면시험\n'))
        seic_picteilín((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_a_sheoladh('q'))
        FOINSE = '''from Gaeilge import 화면크기, 네모그리기, 그림기다리기, Aschur, córas_earráid
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except córas_earráid as ERREÁID:
    assert ERREÁID.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
Aschur("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uaslódáil_Comhaid('화면시험.py', FOINSE.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_a_sheoladh('python /화면시험.py\n'))
        seic_picteilín((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_a_sheoladh('q'))
        FOINSE = '''import Gaeilge.자체.*;
public class 해상도시험 {
    public static void main(String[] Argóintí) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new staid_eisceacht("Méid");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new staid_eisceacht("gearrthóg"); }
        catch (neamhbhailí_argóint_eisceacht ERREÁID) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # eisceacht 처리는 óstach javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = tomhas_cosán/'해상도경계시험.java'
        경계원문.write_text(FOINSE.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(teilgean_fréamh/'dist/jkoros-native-korean.jar'), '-d', str(tomhas_cosán), str(경계원문)])
        uaslódáil_Comhaid('해상도경계시험.class', (tomhas_cosán/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_a_sheoladh('java 해상도경계시험\n'))
        seic_picteilín((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_a_sheoladh('q'))
        # 게스트 javac의 Tacaíocht_VALUE 문법으로 Méid iarratas_VALUE·지우기·다섯 Argóintí 그리기를 컴파일한다.
        FOINSE = '''public class 해상도시험 {
    public static void main(String[] Argóintí) {
        int 너비=Gaeilge.자체.화면.너비();
        int 높이=Gaeilge.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Gaeilge.자체.화면.지우기(3153944);
        Gaeilge.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Gaeilge.자체.Aschur.scríobh_líne("JAVA RESOLUTION PASS");
        Gaeilge.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        uaslódáil_Comhaid('해상도시험.java', FOINSE.encode())
        tomhas = blaosc('javac 해상도시험.java'); assert 'exit 0' in tomhas, tomhas
        기다리기(b'JAVA RESOLUTION PASS', SMS_a_sheoladh('java 해상도시험\n'))
        seic_picteilín((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_a_sheoladh('q'))
        uaslódáil_Comhaid('스윙시험.class', (tomhas_cosán/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_a_sheoladh('java 스윙시험\n'))
        가로, Ingearach_suíomh = (너비-400)//2, (높이-280)//2
        líníocht_VALUE = seic_picteilín((가로, Ingearach_suíomh), (32, 80, 144))
        líníocht_VALUE.save(str(tomhas_cosán/(socraigh_méid_SMS+'.png')))
        Rith_2 = len(LOG_ró); cliceáil_VALUE(가로+80, Ingearach_suíomh+155)
        기다리기('SWING CLICK Ainm'.encode(), Rith_2)
        Rith_2 = len(LOG_ró); cliceáil_VALUE(가로+385, Ingearach_suíomh+15); 기다리기(b'jkoros-native> ', Rith_2)
        assert 'AFTER_RESOLUTION' in blaosc('echo AFTER_RESOLUTION')
        print('PASS:', socraigh_méid_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if traschur_VALUE: traschur_VALUE.close()
        if cianda_VALUE: cianda_VALUE.close()
        if Próiseas_VALUE.poll() is None:
            Próiseas_VALUE.terminate()
            try: Próiseas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Próiseas_VALUE.kill(); Próiseas_VALUE.wait()
        roghnóir_a916db4e.close(); Próiseas_VALUE.stdout.close()
        (tomhas_cosán/(socraigh_méid_SMS+'.log')).write_bytes(LOG_ró)


def Rith_2():
    tomhas_cosán = teilgean_fréamh/'build/verification/resolution'; tomhas_cosán.mkdir(parents=True, exist_ok=True)
    LOG_ró = {'passed': False, 'kernel_sha256': hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for neamhbhailí_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            tomhas = subprocess.run(['python3', str(teilgean_fréamh/'Uirlisí/Rith_ordú.py'), '--resolution', neamhbhailí_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert tomhas.returncode == 2 and b'--resolution' in tomhas.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tomhas_cosán), str(teilgean_fréamh/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, tomhas_cosán); LOG_ró['resolutions'].append([너비, 높이])
        LOG_ró.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (tomhas_cosán/'report.json').write_text(json.dumps(LOG_ró, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Rith_2()
