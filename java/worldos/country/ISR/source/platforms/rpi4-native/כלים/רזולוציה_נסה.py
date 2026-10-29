#!/usr/bin/env python3
"""בפועל_נתונים QEMU/VNC에서 화면 גודל·경계·חלון להעביר_ערך·Swing·언어별 그리기를 검사한다."""
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
from מחשב_שולחני_הצג import 정확한값
from לבצע_פקודה import לשקף_בסיס


def רזולוציה_נסה(너비, גובה_ערך, תוצאה_נתיב):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); מספר_יציאה = 임시.getsockname()[1]
    גודל_טקסט_cdfada26 = '{}x{}'.format(너비, גובה_ערך)
    תהליך_ערך = subprocess.Popen(['python3', str(לשקף_בסיס/'כלים/לבצע_פקודה.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(מספר_יציאה), '--resolution', גודל_טקסט_cdfada26], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    בורר_a916db4e = selectors.DefaultSelector(); בורר_a916db4e.register(תהליך_ערך.stdout, selectors.EVENT_READ)
    לרשום_שיא = bytearray(); מרוחק_ערך = None; העבר_ערך = None

    def 기다리기(הופעה_ערך, הפעלה=0):
        תאריך_יעד_ערך = time.monotonic() + 60
        while הופעה_ערך not in לרשום_שיא[הפעלה:]:
            if time.monotonic() > תאריך_יעד_ערך or תהליך_ערך.poll() is not None or b'HALTED' in לרשום_שיא or b'PANIC:' in לרשום_שיא:
                raise AssertionError(לרשום_שיא[הפעלה:].decode('utf-8', 'replace'))
            for אירוע, _ in בורר_a916db4e.select(.1):
                נתונים = אירוע.fileobj.read(65536)
                if נתונים: לרשום_שיא.extend(נתונים)
        return לרשום_שיא[הפעלה:].decode('utf-8', 'replace')

    def לחץ_מקש(סימן, 눌림=True): מרוחק_ערך.sendall(struct.pack('>BBHI', 4, int(눌림), 0, סימן))

    def שלח_SMS(טקסט):
        הפעלה = len(לרשום_שיא)
        for תו_ערך in טקסט:
            סימן = 0xff0d if תו_ערך == '\n' else ord(תו_ערך) if ord(תו_ערך) < 256 else 0x1000000 | ord(תו_ערך)
            לחץ_מקש(סימן); לחץ_מקש(סימן, False)
        return הפעלה

    def מעטפת(טקסט): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', שלח_SMS(טקסט+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, אנכי_עמדה, 눌림): מרוחק_ערך.sendall(struct.pack('>BBHH', 5, 눌림, 가로, אנכי_עמדה))

    def לחץ_ערך(가로, אנכי_עמדה): 가리키기(가로, אנכי_עמדה, 1); 가리키기(가로, אנכי_עמדה, 0)

    def מפת_סיביות_תמונה():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 בפועל_נתונים 너비를 쓴다.
        מרוחק_ערך.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, גובה_ערך))
        ציור_ערך = Image.new('RGB', (너비, גובה_ערך)); אזור_ערך_9285603e = 0
        while True:
            종류 = 정확한값(מרוחק_ערך, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(מרוחק_ערך, 7)[3:])[0]; 정확한값(מרוחק_ערך, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(מרוחק_ערך, 3)[1:])[0]
            for _ in range(개수):
                가로, אנכי_עמדה, 폭, 길이, קידוד_ערך = struct.unpack('>HHHHi', 정확한값(מרוחק_ערך, 12))
                assert קידוד_ערך == 0 and 가로+폭 <= 너비 and אנכי_עמדה+길이 <= גובה_ערך
                ציור_ערך.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(מרוחק_ערך, 폭*길이*4), 'raw', 'BGRX'), (가로, אנכי_עמדה))
                אזור_ערך_9285603e += 폭*길이
            if אזור_ערך_9285603e:
                assert אזור_ערך_9285603e == 너비*גובה_ערך, אזור_ערך_9285603e
                return ציור_ערך

    def שיק_פיקסל(קואורדינטה_ערך, 색):
        תאריך_יעד_ערך = time.monotonic()+10
        while True:
            ציור_ערך = מפת_סיביות_תמונה()
            if ציור_ערך.getpixel(קואורדינטה_ערך) == 색: return ציור_ערך
            if time.monotonic() > תאריך_יעד_ערך: raise AssertionError((קואורדינטה_ערך, ציור_ערך.getpixel(קואורדינטה_ערך), 색))

    def העלה_קבצים(שם, נתונים): העבר_ערך.storbinary('STOR '+שם, io.BytesIO(נתונים))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+גודל_טקסט_cdfada26+' RGB32').encode() in לרשום_שיא
        print('BOOT:', גודל_טקסט_cdfada26, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', לרשום_שיא).group(1))
        מרוחק_ערך = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(מרוחק_ערך, 12) == b'RFB 003.008\n'; מרוחק_ערך.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(מרוחק_ערך, 정확한값(מרוחק_ערך, 1)[0]); מרוחק_ערך.sendall(b'\x01')
        assert 정확한값(מרוחק_ערך, 4) == b'\0'*4; מרוחק_ערך.sendall(b'\x01')
        מצב_התחלתי = 정확한값(מרוחק_ערך, 24); assert struct.unpack('>HH', מצב_התחלתי[:4]) == (너비, גובה_ערך)
        정확한값(מרוחק_ערך, struct.unpack('>I', מצב_התחלתי[20:])[0])
        מרוחק_ערך.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        מרוחק_ערך.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        שיק_פיקסל((너비-1, גובה_ערך-1), (24, 32, 48))
        # 화면 זכות 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, גובה_ערך-360+12, 1); 가리키기(너비-568+28, גובה_ערך-360+12, 0)
        שיק_פיקסל((너비-568, גובה_ערך-360), (32, 80, 144))
        הפעלה = len(לרשום_שיא); לחץ_ערך(너비-20, גובה_ערך-345); 기다리기(b'TERMINAL FOCUS 1', הפעלה)
        שיק_פיקסל((너비-568, גובה_ערך-360), (24, 32, 48))
        הפעלה = len(לרשום_שיא); לחץ_ערך(80, 16); 기다리기(b'TERMINAL FOCUS 1', הפעלה)
        מעטפת('ftpd start')
        העבר_ערך = ftplib.FTP(); העבר_ערך.encoding = 'utf-8'; העבר_ערך.connect('127.0.0.1', מספר_יציאה, timeout=20); העבר_ערך.login()
        # C 경계 검사는 32비트 unsigned 음수 המר_ערך·לגזור 밖·빈 사각형을 포함한다.
        קודמקור = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), גובה_ערך=화면높이();
    if(너비!=WIDTH || גובה_ערך!=HEIGHT) return 1;
    if(ציור_מלבן(너비,גובה_ערך,0,0,0)) return 2;
    if(ציור_מלבן(너비,גובה_ערך-1,1,1,0)!=-22) return 3;
    if(ציור_מלבן(너비-1,גובה_ערך,1,1,0)!=-22) return 4;
    if(ציור_מלבן(-1,0,1,1,0)!=-22) return 5;
    if(ציור_מלבן(0,0,-1,1,0)!=-22) return 6;
    if(ציור_מלבן(너비-1,גובה_ערך-1,1,1,0x332211)) return 7;
    כתיבה_קובץ_נתונים(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(גובה_ערך))
        העלה_קבצים('화면시험.c', קודמקור.encode())
        assert 'exit 0' in מעטפת('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', שלח_SMS('run /화면시험\n'))
        שיק_פיקסל((너비-1, גובה_ערך-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', שלח_SMS('q'))
        קודמקור = '''from עברית import 화면크기, ציור_מלבן, 그림기다리기, פלטטקסט, שגיאת_מערכת
너비, גובה_ערך = 화면크기()
assert (너비, גובה_ערך) == (WIDTH, HEIGHT)
try:
    ציור_מלבן(너비, גובה_ערך-1, 1, 1, 0)
    raise AssertionError("boundary")
except שגיאת_מערכת as שגיאה:
    assert שגיאה.מדד == 22
ציור_מלבן(너비-1, גובה_ערך-1, 1, 1, 0x665544)
פלטטקסט("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(גובה_ערך))
        העלה_קבצים('화면시험.py', קודמקור.encode())
        기다리기(b'PYTHON RESOLUTION PASS', שלח_SMS('python /화면시험.py\n'))
        שיק_פיקסל((너비-1, גובה_ערך-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', שלח_SMS('q'))
        קודמקור = '''import עברית.עצמי.*;
public class רזולוציה_נסה {
    public static void main(String[] ארגומנטים) {
        int 너비=화면.너비(), גובה_ערך=화면.גובה_ערך();
        if (너비!=WIDTH || גובה_ערך!=HEIGHT) throw new מצב_חריגה("גודל");
        try { 화면.מלבן(너비,גובה_ערך-1,1,1,0); throw new מצב_חריגה("לגזור"); }
        catch (לא_חוקי_ארגומנט_חריגה שגיאה) { }
        화면.מחק_ערך(0x302018);
        화면.מלבן(너비-1,גובה_ערך-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(גובה_ערך))
        # חריגה 처리는 ארח javac 결과를 עצמי JVM에 올려 검사한다.
        경계원문 = תוצאה_נתיב/'해상도경계시험.java'
        경계원문.write_text(קודמקור.replace('class רזולוציה_נסה', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(לשקף_בסיס/'dist/jkoros-native-korean.jar'), '-d', str(תוצאה_נתיב), str(경계원문)])
        העלה_קבצים('해상도경계시험.class', (תוצאה_נתיב/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', שלח_SMS('java 해상도경계시험\n'))
        שיק_פיקסל((너비-1, גובה_ערך-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', שלח_SMS('q'))
        # 게스트 javac의 תמך_ערך 문법으로 גודל שאילתה_ערך·מחק_ערך·다섯 ארגומנטים 그리기를 컴파일한다.
        קודמקור = '''public class רזולוציה_נסה {
    public static void main(String[] ארגומנטים) {
        int 너비=עברית.עצמי.화면.너비();
        int גובה_ערך=עברית.עצמי.화면.גובה_ערך();
        if (너비!=WIDTH || גובה_ערך!=HEIGHT) return;
        עברית.עצמי.화면.מחק_ערך(3153944);
        עברית.עצמי.화면.מלבן(너비-1,גובה_ערך-1,1,1,10061943);
        עברית.עצמי.פלטטקסט.כתיבה_קו("JAVA RESOLUTION PASS");
        עברית.עצמי.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(גובה_ערך))
        העלה_קבצים('רזולוציה_נסה.java', קודמקור.encode())
        תוצאה = מעטפת('javac רזולוציה_נסה.java'); assert 'exit 0' in תוצאה, תוצאה
        기다리기(b'JAVA RESOLUTION PASS', שלח_SMS('java רזולוציה_נסה\n'))
        שיק_פיקסל((너비-1, גובה_ערך-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', שלח_SMS('q'))
        העלה_קבצים('מוסיקת_סווינג_נסה.class', (תוצאה_נתיב/'מוסיקת_סווינג_נסה.class').read_bytes())
        기다리기(b'SWING READY', שלח_SMS('java מוסיקת_סווינג_נסה\n'))
        가로, אנכי_עמדה = (너비-400)//2, (גובה_ערך-280)//2
        ציור_ערך = שיק_פיקסל((가로, אנכי_עמדה), (32, 80, 144))
        ציור_ערך.save(str(תוצאה_נתיב/(גודל_טקסט_cdfada26+'.png')))
        הפעלה = len(לרשום_שיא); לחץ_ערך(가로+80, אנכי_עמדה+155)
        기다리기('SWING CLICK שם'.encode(), הפעלה)
        הפעלה = len(לרשום_שיא); לחץ_ערך(가로+385, אנכי_עמדה+15); 기다리기(b'jkoros-native> ', הפעלה)
        assert 'AFTER_RESOLUTION' in מעטפת('echo AFTER_RESOLUTION')
        print('PASS:', גודל_טקסט_cdfada26, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if העבר_ערך: העבר_ערך.close()
        if מרוחק_ערך: מרוחק_ערך.close()
        if תהליך_ערך.poll() is None:
            תהליך_ערך.terminate()
            try: תהליך_ערך.wait(timeout=8)
            except subprocess.TimeoutExpired: תהליך_ערך.kill(); תהליך_ערך.wait()
        בורר_a916db4e.close(); תהליך_ערך.stdout.close()
        (תוצאה_נתיב/(גודל_טקסט_cdfada26+'.log')).write_bytes(לרשום_שיא)


def הפעלה():
    תוצאה_נתיב = לשקף_בסיס/'build/verification/resolution'; תוצאה_נתיב.mkdir(parents=True, exist_ok=True)
    לרשום_שיא = {'passed': False, 'kernel_sha256': hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for לא_חוקי_ערך in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            תוצאה = subprocess.run(['python3', str(לשקף_בסיס/'כלים/לבצע_פקודה.py'), '--resolution', לא_חוקי_ערך], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert תוצאה.returncode == 2 and b'--resolution' in תוצאה.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(תוצאה_נתיב), str(לשקף_בסיס/'시험/자바/מוסיקת_סווינג_נסה.java')])
        for 너비, גובה_ערך in ((1920,1080), (1280,720), (640,480)):
            רזולוציה_נסה(너비, גובה_ערך, תוצאה_נתיב); לרשום_שיא['resolutions'].append([너비, גובה_ערך])
        לרשום_שיא.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (תוצאה_נתיב/'report.json').write_text(json.dumps(לרשום_שיא, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': הפעלה()
