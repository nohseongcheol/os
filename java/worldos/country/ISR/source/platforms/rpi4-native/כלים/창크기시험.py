#!/usr/bin/env python3
"""בפועל_נתונים QEMU/VNC에서 מסוף 모서리 גרור_ערך·מצביע·동적 תו_ערך חריץ_ערך·ערוך_ערך תוכן_ערך 보존를 검사한다."""
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


def 창크기시험(너비, גובה_ערך, תוצאה_נתיב):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); מספר_יציאה = 임시.getsockname()[1]
    גודל_טקסט_cdfada26 = '{}x{}'.format(너비, גובה_ערך)
    תהליך_ערך = subprocess.Popen(['python3', str(לשקף_בסיס/'כלים/לבצע_פקודה.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(מספר_יציאה), '--resolution', גודל_טקסט_cdfada26], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    בורר_a916db4e = selectors.DefaultSelector(); בורר_a916db4e.register(תהליך_ערך.stdout, selectors.EVENT_READ)
    לרשום_שיא = bytearray(); מרוחק_ערך = None; העבר_ערך = None; מצביע_מוסתר=[False]

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

    def מעטפת(טקסט): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', שלח_SMS(טקסט+'; echo __RESIZE_DONE__\n'))

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
                if קידוד_ערך == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    מצביע_מוסתר[0]=True
                    continue
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
        מרוחק_ערך.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        שיק_פיקסל((너비-1, גובה_ערך-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for אירוע,_ in בורר_a916db4e.select(.02):
                    נתונים=אירוע.fileobj.read(65536)
                    if נתונים:לרשום_שיא.extend(נתונים)
        חלון=[12,48,568,360]
        def ודא_אמת_גודל():
            עמודה_ערך,שורה_ערך=(חלון[2]-24)//8,(חלון[3]-56)//16
            טקסט=מעטפת('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(עמודה_ערך,שורה_ערך) in טקסט,טקסט
            # בפועל_נתונים חלון 테두리: 단지 גודל שאילתה_ערך 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            שיק_פיקסל((חלון[0],חלון[1]),(32,80,144))
            ציור_ערך=שיק_פיקסל((חלון[0]+חלון[2]-1,חלון[1]+חלון[3]-1),(39,49,64))
            return ציור_ערך
        def 모서리(방향):
            return (חלון[0]+(3 if 방향 in (1,3) else חלון[2]-4),חלון[1]+(3 if 방향<=2 else חלון[3]-4))
        def שנה_גודל_גרור(방향,차이,לחצן=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            שיק_פיקסל(흰점,(255,255,255))
            가리키기(가,세,לחצן)
            끝가=max(0,min(너비-1,가+차이[0]));סיים_שיחה_אנכי=max(0,min(גובה_ערך-1,세+차이[1]))
            가리키기(끝가,סיים_שיחה_אנכי,לחצן);가리키기(끝가,סיים_שיחה_אנכי,0);숨고르기()
            if לחצן==1:
                왼,위,폭,길이=חלון;זכות_ערך,아래=왼+폭,위+길이
                if 방향 in (1,3):왼=max(0,min(זכות_ערך-360,왼+끝가-가))
                else:זכות_ערך=max(왼+360,min(너비,זכות_ערך+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+סיים_שיחה_אנכי-세))
                else:아래=max(위+216,min(גובה_ערך,아래+סיים_שיחה_אנכי-세))
                חלון[:]=[왼,위,זכות_ערך-왼,아래-위]
        ודא_אמת_גודל();assert מצביע_מוסתר[0]
        שנה_גודל_גרור(4,(-100,-60),4);ודא_אמת_גודל() # זכות 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            שנה_גודל_גרור(방향,차이);ודא_אמת_גודל()
        # קלט_ערך 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        שלח_SMS("echo '"+긴글+"'");숨고르기()
        שנה_גודל_גרור(4,(-1000,-1000));assert חלון[2:]==[360,216]
        שנה_גודל_גרור(4,(너비,גובה_ערך))
        הפעלה=שלח_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),הפעלה);ודא_אמת_גודל()
        # vi가 ערוך_ערך 중에 화면 크기를 נסה_שנית_ערך 읽고, 저장하지 않은 한글도 유지한다.
        מעטפת('ftpd start')
        העבר_ערך=ftplib.FTP();העבר_ערך.encoding='utf-8';העבר_ערך.connect('127.0.0.1',מספר_יציאה,timeout=20);העבר_ערך.login()
        기다리기(b'NORMAL',שלח_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',שלח_SMS('i미저장 한글 נתונים\n'));숨고르기()
        שנה_גודל_גרור(4,(-너비,-גובה_ערך))
        # ANSI שורה_ערך 이동에 새 שורה_ערך 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((חלון[3]-56)//16)).encode() in לרשום_שיא[-4096:]
        שלח_SMS('작은 창에서도 이어 כתוב\n');숨고르기()
        שנה_גודל_גרור(4,(너비,גובה_ערך))
        שלח_SMS('큰 창에서도 이어 כתוב\n');숨고르기()
        לחץ_מקש(0xff1b);לחץ_מקש(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',שלח_SMS(':wq\n'))
        תוכן_ערך=bytearray();העבר_ערך.retrbinary('RETR 크기자료.txt',תוכן_ערך.extend)
        assert תוכן_ערך=='미저장 한글 נתונים\n작은 창에서도 이어 כתוב\n큰 창에서도 이어 כתוב\n'.encode(),תוכן_ערך
        ודא_אמת_גודל().save(str(תוצאה_נתיב/(גודל_טקסט_cdfada26+'-large.png')))
        # 두 번째 창은 ערך_ברירת_מחדל גודל, נסה_שנית_ערך 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        הפעלה=len(לרשום_שיא);לחץ_ערך(70,16);기다리기(b'TERMINAL FOCUS 2',הפעלה)
        assert 'TERMINAL SIZE 68x19' in מעטפת('terminal size')
        הפעלה=len(לרשום_שיא);לחץ_ערך(180,16);기다리기(b'TERMINAL FOCUS 1',הפעלה);ודא_אמת_גודל()
        שנה_גודל_גרור(4,(-너비,-גובה_ערך));ודא_אמת_גודל().save(str(תוצאה_נתיב/(גודל_טקסט_cdfada26+'-small.png')))
        # גודל שנה_ערך הקודם_ערך X 닫기도 새로운 זכות 가장자리를 사용한다.
        הפעלה=len(לרשום_שיא);לחץ_ערך(חלון[0]+חלון[2]-20,חלון[1]+15);기다리기(b'TERMINAL FOCUS 2',הפעלה)
        assert 'RESIZE CLOSED' in מעטפת('echo RESIZE CLOSED')
        print('PASS:',גודל_טקסט_cdfada26,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if העבר_ערך:העבר_ערך.close()
        if מרוחק_ערך:מרוחק_ערך.close()
        if תהליך_ערך.poll() is None:
            תהליך_ערך.terminate()
            try:תהליך_ערך.wait(timeout=8)
            except subprocess.TimeoutExpired:תהליך_ערך.kill();תהליך_ערך.wait()
        בורר_a916db4e.close();תהליך_ערך.stdout.close();(תוצאה_נתיב/(גודל_טקסט_cdfada26+'.log')).write_bytes(לרשום_שיא)


def הפעלה():
    תוצאה_נתיב=לשקף_בסיס/'build/verification/resize';תוצאה_נתיב.mkdir(parents=True,exist_ok=True)
    לרשום_שיא={'passed':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,גובה_ערך in ((640,480),(1920,1080)):
            창크기시험(너비,גובה_ערך,תוצאה_נתיב);לרשום_שיא['resolutions'].append([너비,גובה_ערך])
        לרשום_שיא.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(תוצאה_נתיב/'report.json').write_text(json.dumps(לרשום_שיא,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':הפעלה()
