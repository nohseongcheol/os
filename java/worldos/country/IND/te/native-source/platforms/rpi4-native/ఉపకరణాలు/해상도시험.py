#!/usr/bin/env python3
"""వాస్తవ_డేటా QEMU/VNC에서 화면 పరిమాణం·경계·విండో తరలించు_మూల్యం·Swing·언어별 그리기를 검사한다."""
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
from డెస్క్_టాప్_వీక్షణ import 정확한값
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def 해상도시험(너비, 높이, ప్రమాణం_పథం):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); పోర్ట్_సంఖ్య = 임시.getsockname()[1]
    పరిమాణం_మార్చు_పాఠం = '{}x{}'.format(너비, 높이)
    విధానం_మూల్యం = subprocess.Popen(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(పోర్ట్_సంఖ్య), '--resolution', పరిమాణం_మార్చు_పాఠం], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్_a916db4e = selectors.DefaultSelector(); సెలక్టర్_a916db4e.register(విధానం_మూల్యం.stdout, selectors.EVENT_READ)
    లాగ్_వరుస = bytearray(); రిమోట్_మూల్యం = None; బదిలీ_మూల్యం = None

    def 기다리기(చూపించు_మూల్యం, నడుపుము=0):
        마감 = time.monotonic() + 60
        while చూపించు_మూల్యం not in లాగ్_వరుస[నడుపుము:]:
            if time.monotonic() > 마감 or విధానం_మూల్యం.poll() is not None or b'HALTED' in లాగ్_వరుస or b'PANIC:' in లాగ్_వరుస:
                raise AssertionError(లాగ్_వరుస[నడుపుము:].decode('utf-8', 'replace'))
            for ఈవెంట్, _ in సెలక్టర్_a916db4e.select(.1):
                డేటా = ఈవెంట్.fileobj.read(65536)
                if డేటా: లాగ్_వరుస.extend(డేటా)
        return లాగ్_వరుస[నడుపుము:].decode('utf-8', 'replace')

    def క్లిక్_చెయండి_బటన్(చిహ్నం, 눌림=True): రిమోట్_మూల్యం.sendall(struct.pack('>BBHI', 4, int(눌림), 0, చిహ్నం))

    def SMS_పంపు(పాఠ్యము):
        నడుపుము = len(లాగ్_వరుస)
        for అక్షరం_మూల్యం in పాఠ్యము:
            చిహ్నం = 0xff0d if అక్షరం_మూల్యం == '\n' else ord(అక్షరం_మూల్యం) if ord(అక్షరం_మూల్యం) < 256 else 0x1000000 | ord(అక్షరం_మూల్యం)
            క్లిక్_చెయండి_బటన్(చిహ్నం); క్లిక్_చెయండి_బటన్(చిహ్నం, False)
        return నడుపుము

    def షెల్(పాఠ్యము): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_పంపు(పాఠ్యము+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, నిలువు_స్థాయి, 눌림): రిమోట్_మూల్యం.sendall(struct.pack('>BBHH', 5, 눌림, 가로, నిలువు_స్థాయి))

    def క్లిక్_చెయండి_మూల్యం(가로, నిలువు_స్థాయి): 가리키기(가로, నిలువు_స్థాయి, 1); 가리키기(가로, నిలువు_స్థాయి, 0)

    def బిట్_మ్యాప్_చిత్రం():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 వాస్తవ_డేటా 너비를 쓴다.
        రిమోట్_మూల్యం.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        రేఖాచిత్రణ_మూల్యం = Image.new('RGB', (너비, 높이)); ప్రదేశం_మూల్యం = 0
        while True:
            종류 = 정확한값(రిమోట్_మూల్యం, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                పొడవు_మూల్యం = struct.unpack('>I', 정확한값(రిమోట్_మూల్యం, 7)[3:])[0]; 정확한값(రిమోట్_మూల్యం, పొడవు_మూల్యం); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(రిమోట్_మూల్యం, 3)[1:])[0]
            for _ in range(개수):
                가로, నిలువు_స్థాయి, 폭, పొడవు_మూల్యం, సంకేతీకరణం_మూల్యం = struct.unpack('>HHHHi', 정확한값(రిమోట్_మూల్యం, 12))
                assert సంకేతీకరణం_మూల్యం == 0 and 가로+폭 <= 너비 and నిలువు_స్థాయి+పొడవు_మూల్యం <= 높이
                రేఖాచిత్రణ_మూల్యం.paste(Image.frombytes('RGB', (폭, పొడవు_మూల్యం), 정확한값(రిమోట్_మూల్యం, 폭*పొడవు_మూల్యం*4), 'raw', 'BGRX'), (가로, నిలువు_స్థాయి))
                ప్రదేశం_మూల్యం += 폭*పొడవు_మూల్యం
            if ప్రదేశం_మూల్యం:
                assert ప్రదేశం_మూల్యం == 너비*높이, ప్రదేశం_మూల్యం
                return రేఖాచిత్రణ_మూల్యం

    def తనిఖీ_పెల్(సమన్వయపరుచు_మూల్యం, 색):
        마감 = time.monotonic()+10
        while True:
            రేఖాచిత్రణ_మూల్యం = బిట్_మ్యాప్_చిత్రం()
            if రేఖాచిత్రణ_మూల్యం.getpixel(సమన్వయపరుచు_మూల్యం) == 색: return రేఖాచిత్రణ_మూల్యం
            if time.monotonic() > 마감: raise AssertionError((సమన్వయపరుచు_మూల్యం, రేఖాచిత్రణ_మూల్యం.getpixel(సమన్వయపరుచు_మూల్యం), 색))

    def అప్_లోడ్_ఫైల్_లు(పేరు, డేటా): బదిలీ_మూల్యం.storbinary('STOR '+పేరు, io.BytesIO(డేటా))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+పరిమాణం_మార్చు_పాఠం+' RGB32').encode() in లాగ్_వరుస
        print('BOOT:', పరిమాణం_మార్చు_పాఠం, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', లాగ్_వరుస).group(1))
        రిమోట్_మూల్యం = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(రిమోట్_మూల్యం, 12) == b'RFB 003.008\n'; రిమోట్_మూల్యం.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(రిమోట్_మూల్యం, 정확한값(రిమోట్_మూల్యం, 1)[0]); రిమోట్_మూల్యం.sendall(b'\x01')
        assert 정확한값(రిమోట్_మూల్యం, 4) == b'\0'*4; రిమోట్_మూల్యం.sendall(b'\x01')
        초기 = 정확한값(రిమోట్_మూల్యం, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(రిమోట్_మూల్యం, struct.unpack('>I', 초기[20:])[0])
        రిమోట్_మూల్యం.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        రిమోట్_మూల్యం.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        తనిఖీ_పెల్((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        తనిఖీ_పెల్((너비-568, 높이-360), (32, 80, 144))
        నడుపుము = len(లాగ్_వరుస); క్లిక్_చెయండి_మూల్యం(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', నడుపుము)
        తనిఖీ_పెల్((너비-568, 높이-360), (24, 32, 48))
        నడుపుము = len(లాగ్_వరుస); క్లిక్_చెయండి_మూల్యం(80, 16); 기다리기(b'TERMINAL FOCUS 1', నడుపుము)
        షెల్('ftpd start')
        బదిలీ_మూల్యం = ftplib.FTP(); బదిలీ_మూల్యం.encoding = 'utf-8'; బదిలీ_మూల్యం.connect('127.0.0.1', పోర్ట్_సంఖ్య, timeout=20); బదిలీ_మూల్యం.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·క్లిప్ 밖·빈 사각형을 포함한다.
        వనరు = '''#include <화면규약.h>
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
    వ్రాయి_ఫైలు_డేటా(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        అప్_లోడ్_ఫైల్_లు('화면시험.c', వనరు.encode())
        assert 'exit 0' in షెల్('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_పంపు('run /화면시험\n'))
        తనిఖీ_పెల్((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_పంపు('q'))
        వనరు = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, అవుట్పుట్, సిస్టం_దోషం
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except సిస్టం_దోషం as దోషం:
    assert దోషం.సూచీ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
అవుట్పుట్("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        అప్_లోడ్_ఫైల్_లు('화면시험.py', వనరు.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_పంపు('python /화면시험.py\n'))
        తనిఖీ_పెల్((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_పంపు('q'))
        వనరు = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new స్థితి_మినహాయింపు("పరిమాణం");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new స్థితి_మినహాయింపు("క్లిప్"); }
        catch (చెల్లని_కారకం_మినహాయింపు దోషం) { }
        화면.తుడిచివేయి_ప్రవేశం(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # మినహాయింపు 처리는 హోస్ట్ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ప్రమాణం_పథం/'해상도경계시험.java'
        경계원문.write_text(వనరు.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-korean.jar'), '-d', str(ప్రమాణం_పథం), str(경계원문)])
        అప్_లోడ్_ఫైల్_లు('해상도경계시험.class', (ప్రమాణం_పథం/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_పంపు('java 해상도경계시험\n'))
        తనిఖీ_పెల్((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_పంపు('q'))
        # 게스트 javac의 మద్దతు_మూల్యం 문법으로 పరిమాణం ప్రశ్న_మూల్యం·తుడిచివేయి_ప్రవేశం·다섯 인수 그리기를 컴파일한다.
        వనరు = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.తుడిచివేయి_ప్రవేశం(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.అవుట్పుట్.వ్రాయి_పంక్తి("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        అప్_లోడ్_ఫైల్_లు('해상도시험.java', వనరు.encode())
        ప్రమాణం = షెల్('javac 해상도시험.java'); assert 'exit 0' in ప్రమాణం, ప్రమాణం
        기다리기(b'JAVA RESOLUTION PASS', SMS_పంపు('java 해상도시험\n'))
        తనిఖీ_పెల్((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_పంపు('q'))
        అప్_లోడ్_ఫైల్_లు('스윙시험.class', (ప్రమాణం_పథం/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_పంపు('java 스윙시험\n'))
        가로, నిలువు_స్థాయి = (너비-400)//2, (높이-280)//2
        రేఖాచిత్రణ_మూల్యం = తనిఖీ_పెల్((가로, నిలువు_స్థాయి), (32, 80, 144))
        రేఖాచిత్రణ_మూల్యం.save(str(ప్రమాణం_పథం/(పరిమాణం_మార్చు_పాఠం+'.png')))
        నడుపుము = len(లాగ్_వరుస); క్లిక్_చెయండి_మూల్యం(가로+80, నిలువు_స్థాయి+155)
        기다리기('SWING CLICK పేరు'.encode(), నడుపుము)
        నడుపుము = len(లాగ్_వరుస); క్లిక్_చెయండి_మూల్యం(가로+385, నిలువు_స్థాయి+15); 기다리기(b'jkoros-native> ', నడుపుము)
        assert 'AFTER_RESOLUTION' in షెల్('echo AFTER_RESOLUTION')
        print('PASS:', పరిమాణం_మార్చు_పాఠం, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if బదిలీ_మూల్యం: బదిలీ_మూల్యం.close()
        if రిమోట్_మూల్యం: రిమోట్_మూల్యం.close()
        if విధానం_మూల్యం.poll() is None:
            విధానం_మూల్యం.terminate()
            try: విధానం_మూల్యం.wait(timeout=8)
            except subprocess.TimeoutExpired: విధానం_మూల్యం.kill(); విధానం_మూల్యం.wait()
        సెలక్టర్_a916db4e.close(); విధానం_మూల్యం.stdout.close()
        (ప్రమాణం_పథం/(పరిమాణం_మార్చు_పాఠం+'.log')).write_bytes(లాగ్_వరుస)


def నడుపుము():
    ప్రమాణం_పథం = ప్రొజెక్ట్_మూలం/'build/verification/resolution'; ప్రమాణం_పథం.mkdir(parents=True, exist_ok=True)
    లాగ్_వరుస = {'passed': False, 'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for చెల్లని_మూల్యం in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ప్రమాణం = subprocess.run(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'), '--resolution', చెల్లని_మూల్యం], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ప్రమాణం.returncode == 2 and b'--resolution' in ప్రమాణం.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ప్రమాణం_పథం), str(ప్రొజెక్ట్_మూలం/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ప్రమాణం_పథం); లాగ్_వరుస['resolutions'].append([너비, 높이])
        లాగ్_వరుస.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ప్రమాణం_పథం/'report.json').write_text(json.dumps(లాగ్_వరుస, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': నడుపుము()
