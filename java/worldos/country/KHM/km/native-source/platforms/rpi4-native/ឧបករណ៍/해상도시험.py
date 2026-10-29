#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ QEMU/VNC에서 화면 ដាក់ទំហំ·경계·វីនដូ ផ្លាស់ទី_តំលៃ·Swing·언어별 그리기를 검사한다."""
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
from ដែសថប_ការមើល import 정확한값
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def 해상도시험(너비, 높이, ការវាស់វែង_ផ្លូវ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); លេខរន្ធ = 임시.getsockname()[1]
    ដាក់ទំហំ_អត្ថបទ = '{}x{}'.format(너비, 높이)
    ដំណើរការ_តំលៃ = subprocess.Popen(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(លេខរន្ធ), '--resolution', ដាក់ទំហំ_អត្ថបទ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    អ្នកជ្រើសរើស_a916db4e = selectors.DefaultSelector(); អ្នកជ្រើសរើស_a916db4e.register(ដំណើរការ_តំលៃ.stdout, selectors.EVENT_READ)
    កំណត់_ហេតុ_ថត = bytearray(); ពីចម្ងាយ_តំលៃ = None; ផ្ទេរ_តំលៃ = None

    def 기다리기(បង្ហាញ_តំលៃ, រត់=0):
        마감 = time.monotonic() + 60
        while បង្ហាញ_តំលៃ not in កំណត់_ហេតុ_ថត[រត់:]:
            if time.monotonic() > 마감 or ដំណើរការ_តំលៃ.poll() is not None or b'HALTED' in កំណត់_ហេតុ_ថត or b'PANIC:' in កំណត់_ហេតុ_ថត:
                raise AssertionError(កំណត់_ហេតុ_ថត[រត់:].decode('utf-8', 'replace'))
            for ព្រឹត្តិការណ៍, _ in អ្នកជ្រើសរើស_a916db4e.select(.1):
                ទិន្នន័យ = ព្រឹត្តិការណ៍.fileobj.read(65536)
                if ទិន្នន័យ: កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
        return កំណត់_ហេតុ_ថត[រត់:].decode('utf-8', 'replace')

    def ចុច_ប៊ូតុង(និមិត្ត_សញ្ញា, 눌림=True): ពីចម្ងាយ_តំលៃ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, និមិត្ត_សញ្ញា))

    def ផ្ញើអត្ថបទ(អត្ថបទ):
        រត់ = len(កំណត់_ហេតុ_ថត)
        for តួអក្សរ_តំលៃ in អត្ថបទ:
            និមិត្ត_សញ្ញា = 0xff0d if តួអក្សរ_តំលៃ == '\n' else ord(តួអក្សរ_តំលៃ) if ord(តួអក្សរ_តំលៃ) < 256 else 0x1000000 | ord(តួអក្សរ_តំលៃ)
            ចុច_ប៊ូតុង(និមិត្ត_សញ្ញា); ចុច_ប៊ូតុង(និមិត្ត_សញ្ញា, False)
        return រត់

    def 셸(អត្ថបទ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ផ្ញើអត្ថបទ(អត្ថបទ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, បញ្ឈរ_កំណត់ទីតាំង, 눌림): ពីចម្ងាយ_តំលៃ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, បញ្ឈរ_កំណត់ទីតាំង))

    def ចុច_តំលៃ(가로, បញ្ឈរ_កំណត់ទីតាំង): 가리키기(가로, បញ្ឈរ_កំណត់ទីតាំង, 1); 가리키기(가로, បញ្ឈរ_កំណត់ទីតាំង, 0)

    def រូបភាព_bitmap_រូបថត():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ដែលពិត_ទិន្នន័យ 너비를 쓴다.
        ពីចម្ងាយ_តំលៃ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ការគូរ_តំលៃ = Image.new('RGB', (너비, 높이)); ប្រភេទ_តំលៃ_9285603e = 0
        while True:
            종류 = 정확한값(ពីចម្ងាយ_តំលៃ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ប្រវែង_តំលៃ = struct.unpack('>I', 정확한값(ពីចម្ងាយ_តំលៃ, 7)[3:])[0]; 정확한값(ពីចម្ងាយ_តំលៃ, ប្រវែង_តំលៃ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ពីចម្ងាយ_តំលៃ, 3)[1:])[0]
            for _ in range(개수):
                가로, បញ្ឈរ_កំណត់ទីតាំង, 폭, ប្រវែង_តំលៃ, ការបំលែងកូដ_តំលៃ = struct.unpack('>HHHHi', 정확한값(ពីចម្ងាយ_តំលៃ, 12))
                assert ការបំលែងកូដ_តំលៃ == 0 and 가로+폭 <= 너비 and បញ្ឈរ_កំណត់ទីតាំង+ប្រវែង_តំលៃ <= 높이
                ការគូរ_តំលៃ.paste(Image.frombytes('RGB', (폭, ប្រវែង_តំលៃ), 정확한값(ពីចម្ងាយ_តំលៃ, 폭*ប្រវែង_តំលៃ*4), 'raw', 'BGRX'), (가로, បញ្ឈរ_កំណត់ទីតាំង))
                ប្រភេទ_តំលៃ_9285603e += 폭*ប្រវែង_តំលៃ
            if ប្រភេទ_តំលៃ_9285603e:
                assert ប្រភេទ_តំលៃ_9285603e == 너비*높이, ប្រភេទ_តំលៃ_9285603e
                return ការគូរ_តំលៃ

    def ត្រួតពិនិត្យ_ចំនុចតូចៗ(កូអរដោនេ_តំលៃ, 색):
        마감 = time.monotonic()+10
        while True:
            ការគូរ_តំលៃ = រូបភាព_bitmap_រូបថត()
            if ការគូរ_តំលៃ.getpixel(កូអរដោនេ_តំលៃ) == 색: return ការគូរ_តំលៃ
            if time.monotonic() > 마감: raise AssertionError((កូអរដោនេ_តំលៃ, ការគូរ_តំលៃ.getpixel(កូអរដោនេ_តំលៃ), 색))

    def បង្ហោះ_ឯកសារ(ឈ្មោះ, ទិន្នន័យ): ផ្ទេរ_តំលៃ.storbinary('STOR '+ឈ្មោះ, io.BytesIO(ទិន្នន័យ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ដាក់ទំហំ_អត្ថបទ+' RGB32').encode() in កំណត់_ហេតុ_ថត
        print('BOOT:', ដាក់ទំហំ_អត្ថបទ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', កំណត់_ហេតុ_ថត).group(1))
        ពីចម្ងាយ_តំលៃ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ពីចម្ងាយ_តំលៃ, 12) == b'RFB 003.008\n'; ពីចម្ងាយ_តំលៃ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ពីចម្ងាយ_តំលៃ, 정확한값(ពីចម្ងាយ_តំលៃ, 1)[0]); ពីចម្ងាយ_តំលៃ.sendall(b'\x01')
        assert 정확한값(ពីចម្ងាយ_តំលៃ, 4) == b'\0'*4; ពីចម្ងាយ_តំលៃ.sendall(b'\x01')
        초기 = 정확한값(ពីចម្ងាយ_តំលៃ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ពីចម្ងាយ_តំលៃ, struct.unpack('>I', 초기[20:])[0])
        ពីចម្ងាយ_តំលៃ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ពីចម្ងាយ_តំលៃ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-568, 높이-360), (32, 80, 144))
        រត់ = len(កំណត់_ហេតុ_ថត); ចុច_តំលៃ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', រត់)
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-568, 높이-360), (24, 32, 48))
        រត់ = len(កំណត់_ហេតុ_ថត); ចុច_តំលៃ(80, 16); 기다리기(b'TERMINAL FOCUS 1', រត់)
        셸('ftpd start')
        ផ្ទេរ_តំលៃ = ftplib.FTP(); ផ្ទេរ_តំលៃ.encoding = 'utf-8'; ផ្ទេរ_តំលៃ.connect('127.0.0.1', លេខរន្ធ, timeout=20); ផ្ទេរ_តំលៃ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·មេឌៀខ្លីៗ 밖·빈 사각형을 포함한다.
        ប្រភព = '''#include <화면규약.h>
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
    សរសេរ_ឯកសារ_ទិន្នន័យ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        បង្ហោះ_ឯកសារ('화면시험.c', ប្រភព.encode())
        assert 'exit 0' in 셸('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ផ្ញើអត្ថបទ('run /화면시험\n'))
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ផ្ញើអត្ថបទ('q'))
        ប្រភព = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, លទ្ធផល, ប្រព័ន្ធ_កំហុស
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ប្រព័ន្ធ_កំហុស as កំហុស:
    assert កំហុស.សន្ទស្សន៏ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
លទ្ធផល("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        បង្ហោះ_ឯកសារ('화면시험.py', ប្រភព.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ផ្ញើអត្ថបទ('python /화면시험.py\n'))
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ផ្ញើអត្ថបទ('q'))
        ប្រភព = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] អាគុយម៉ង់) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new ភាព_ការលើកលែង("ដាក់ទំហំ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new ភាព_ការលើកលែង("មេឌៀខ្លីៗ"); }
        catch (មិនត្រឹមត្រូវ_អាគុយម៉ង់_ការលើកលែង កំហុស) { }
        화면.លុប_ការបញ្ចូល(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ការលើកលែង 처리는 ហូស javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ការវាស់វែង_ផ្លូវ/'해상도경계시험.java'
        경계원문.write_text(ប្រភព.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(បញ្ចាំង_ឬស/'dist/jkoros-native-korean.jar'), '-d', str(ការវាស់វែង_ផ្លូវ), str(경계원문)])
        បង្ហោះ_ឯកសារ('해상도경계시험.class', (ការវាស់វែង_ផ្លូវ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ផ្ញើអត្ថបទ('java 해상도경계시험\n'))
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ផ្ញើអត្ថបទ('q'))
        # 게스트 javac의 ទម្រ_តំលៃ 문법으로 ដាក់ទំហំ សំណើ_តំលៃ·លុប_ការបញ្ចូល·다섯 អាគុយម៉ង់ 그리기를 컴파일한다.
        ប្រភព = '''public class 해상도시험 {
    public static void main(String[] អាគុយម៉ង់) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.លុប_ការបញ្ចូល(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.លទ្ធផល.សរសេរ_បណ្ដាញ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        បង្ហោះ_ឯកសារ('해상도시험.java', ប្រភព.encode())
        ការវាស់វែង = 셸('javac 해상도시험.java'); assert 'exit 0' in ការវាស់វែង, ការវាស់វែង
        기다리기(b'JAVA RESOLUTION PASS', ផ្ញើអត្ថបទ('java 해상도시험\n'))
        ត្រួតពិនិត្យ_ចំនុចតូចៗ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ផ្ញើអត្ថបទ('q'))
        បង្ហោះ_ឯកសារ('스윙시험.class', (ការវាស់វែង_ផ្លូវ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ផ្ញើអត្ថបទ('java 스윙시험\n'))
        가로, បញ្ឈរ_កំណត់ទីតាំង = (너비-400)//2, (높이-280)//2
        ការគូរ_តំលៃ = ត្រួតពិនិត្យ_ចំនុចតូចៗ((가로, បញ្ឈរ_កំណត់ទីតាំង), (32, 80, 144))
        ការគូរ_តំលៃ.save(str(ការវាស់វែង_ផ្លូវ/(ដាក់ទំហំ_អត្ថបទ+'.png')))
        រត់ = len(កំណត់_ហេតុ_ថត); ចុច_តំលៃ(가로+80, បញ្ឈរ_កំណត់ទីតាំង+155)
        기다리기('SWING CLICK ឈ្មោះ'.encode(), រត់)
        រត់ = len(កំណត់_ហេតុ_ថត); ចុច_តំលៃ(가로+385, បញ្ឈរ_កំណត់ទីតាំង+15); 기다리기(b'jkoros-native> ', រត់)
        assert 'AFTER_RESOLUTION' in 셸('echo AFTER_RESOLUTION')
        print('PASS:', ដាក់ទំហំ_អត្ថបទ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ផ្ទេរ_តំលៃ: ផ្ទេរ_តំលៃ.close()
        if ពីចម្ងាយ_តំលៃ: ពីចម្ងាយ_តំលៃ.close()
        if ដំណើរការ_តំលៃ.poll() is None:
            ដំណើរការ_តំលៃ.terminate()
            try: ដំណើរការ_តំលៃ.wait(timeout=8)
            except subprocess.TimeoutExpired: ដំណើរការ_តំលៃ.kill(); ដំណើរការ_តំលៃ.wait()
        អ្នកជ្រើសរើស_a916db4e.close(); ដំណើរការ_តំលៃ.stdout.close()
        (ការវាស់វែង_ផ្លូវ/(ដាក់ទំហំ_អត្ថបទ+'.log')).write_bytes(កំណត់_ហេតុ_ថត)


def រត់():
    ការវាស់វែង_ផ្លូវ = បញ្ចាំង_ឬស/'build/verification/resolution'; ការវាស់វែង_ផ្លូវ.mkdir(parents=True, exist_ok=True)
    កំណត់_ហេតុ_ថត = {'passed': False, 'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for មិនត្រឹមត្រូវ_តំលៃ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ការវាស់វែង = subprocess.run(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py'), '--resolution', មិនត្រឹមត្រូវ_តំលៃ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ការវាស់វែង.returncode == 2 and b'--resolution' in ការវាស់វែង.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ការវាស់វែង_ផ្លូវ), str(បញ្ចាំង_ឬស/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ការវាស់វែង_ផ្លូវ); កំណត់_ហេតុ_ថត['resolutions'].append([너비, 높이])
        កំណត់_ហេតុ_ថត.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ការវាស់វែង_ផ្លូវ/'report.json').write_text(json.dumps(កំណត់_ហេតុ_ថត, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': រត់()
