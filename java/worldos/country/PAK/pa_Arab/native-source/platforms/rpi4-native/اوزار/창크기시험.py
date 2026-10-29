#!/usr/bin/env python3
"""اصلی_کوائف QEMU/VNC에서 터미널 모서리 گھسیٹو_قدر·پوائنٹر·동적 کریکٹر_قدر سلاٹ_داخلہ·تدوین_قدر اجزاء_قدر 보존를 검사한다."""
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
from ڈیسک_ٹاپ_منظر import 정확한값
from نفاذ_کرو_حکم import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    سائز_متن = '{}x{}'.format(너비, 높이)
    عمل_قدر = subprocess.Popen(['python3', str(기준/'اوزار/نفاذ_کرو_حکم.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', سائز_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کرنڑ_آلا_a916db4e = selectors.DefaultSelector(); منتخب_کرنڑ_آلا_a916db4e.register(عمل_قدر.stdout, selectors.EVENT_READ)
    لاگ_صف = bytearray(); بعيد_قدر = None; منتقلی_قدر = None; پوائنٹر_خفیہ=[False]

    def 기다리기(نمایش_کرو_قدر, چلاؤ=0):
        마감 = time.monotonic() + 60
        while نمایش_کرو_قدر not in لاگ_صف[چلاؤ:]:
            if time.monotonic() > 마감 or عمل_قدر.poll() is not None or b'HALTED' in لاگ_صف or b'PANIC:' in لاگ_صف:
                raise AssertionError(لاگ_صف[چلاؤ:].decode('utf-8', 'replace'))
            for واقعہ, _ in منتخب_کرنڑ_آلا_a916db4e.select(.1):
                کوائف = واقعہ.fileobj.read(65536)
                if کوائف: لاگ_صف.extend(کوائف)
        return لاگ_صف[چلاؤ:].decode('utf-8', 'replace')

    def کلک_کرو_بٹن(علامت, 눌림=True): بعيد_قدر.sendall(struct.pack('>BBHI', 4, int(눌림), 0, علامت))

    def متن_پیجو(متن):
        چلاؤ = len(لاگ_صف)
        for کریکٹر_قدر in متن:
            علامت = 0xff0d if کریکٹر_قدر == '\n' else ord(کریکٹر_قدر) if ord(کریکٹر_قدر) < 256 else 0x1000000 | ord(کریکٹر_قدر)
            کلک_کرو_بٹن(علامت); کلک_کرو_بٹن(علامت, False)
        return چلاؤ

    def شیل(متن): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', متن_پیجو(متن+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): بعيد_قدر.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def کلک_کرو_قدر(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def بِٹ_میپ_نقش():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 اصلی_کوائف 너비를 쓴다.
        بعيد_قدر.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ڈرائنگ_قدر = Image.new('RGB', (너비, 높이)); قِسم_قدر = 0
        while True:
            종류 = 정확한값(بعيد_قدر, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                لمبائی_قدر = struct.unpack('>I', 정확한값(بعيد_قدر, 7)[3:])[0]; 정확한값(بعيد_قدر, لمبائی_قدر); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعيد_قدر, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, لمبائی_قدر, ضابطہ_ربائی_قدر = struct.unpack('>HHHHi', 정확한값(بعيد_قدر, 12))
                if ضابطہ_ربائی_قدر == -239:
                    assert 폭==0 and لمبائی_قدر==0, 'remote cursor must be hidden'
                    پوائنٹر_خفیہ[0]=True
                    continue
                assert ضابطہ_ربائی_قدر == 0 and 가로+폭 <= 너비 and 세로+لمبائی_قدر <= 높이
                ڈرائنگ_قدر.paste(Image.frombytes('RGB', (폭, لمبائی_قدر), 정확한값(بعيد_قدر, 폭*لمبائی_قدر*4), 'raw', 'BGRX'), (가로, 세로))
                قِسم_قدر += 폭*لمبائی_قدر
            if قِسم_قدر:
                assert قِسم_قدر == 너비*높이, قِسم_قدر
                return ڈرائنگ_قدر

    def پڑتال_دانہ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ڈرائنگ_قدر = بِٹ_میپ_نقش()
            if ڈرائنگ_قدر.getpixel(좌표) == 색: return ڈرائنگ_قدر
            if time.monotonic() > 마감: raise AssertionError((좌표, ڈرائنگ_قدر.getpixel(좌표), 색))

    def اپ_لوڈ_کرو_فائلاں(ناں, کوائف): منتقلی_قدر.storbinary('STOR '+ناں, io.BytesIO(کوائف))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+سائز_متن+' RGB32').encode() in لاگ_صف
        print('BOOT:', سائز_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', لاگ_صف).group(1))
        بعيد_قدر = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(بعيد_قدر, 12) == b'RFB 003.008\n'; بعيد_قدر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعيد_قدر, 정확한값(بعيد_قدر, 1)[0]); بعيد_قدر.sendall(b'\x01')
        assert 정확한값(بعيد_قدر, 4) == b'\0'*4; بعيد_قدر.sendall(b'\x01')
        초기 = 정확한값(بعيد_قدر, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(بعيد_قدر, struct.unpack('>I', 초기[20:])[0])
        بعيد_قدر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعيد_قدر.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        پڑتال_دانہ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for واقعہ,_ in منتخب_کرنڑ_آلا_a916db4e.select(.02):
                    کوائف=واقعہ.fileobj.read(65536)
                    if کوائف:لاگ_صف.extend(کوائف)
        کھڑکی=[12,48,568,360]
        def تصدیق_کرو_سائز():
            کالم_قدر,صف_قدر=(کھڑکی[2]-24)//8,(کھڑکی[3]-56)//16
            متن=شیل('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(کالم_قدر,صف_قدر) in متن,متن
            # اصلی_کوائف کھڑکی 테두리: 단지 سائز طلب_قدر 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            پڑتال_دانہ((کھڑکی[0],کھڑکی[1]),(32,80,144))
            ڈرائنگ_قدر=پڑتال_دانہ((کھڑکی[0]+کھڑکی[2]-1,کھڑکی[1]+کھڑکی[3]-1),(39,49,64))
            return ڈرائنگ_قدر
        def 모서리(방향):
            return (کھڑکی[0]+(3 if 방향 in (1,3) else کھڑکی[2]-4),کھڑکی[1]+(3 if 방향<=2 else کھڑکی[3]-4))
        def پھر_سائز_کرو_گھسیٹو(방향,차이,بٹن=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            پڑتال_دانہ(흰점,(255,255,255))
            가리키기(가,세,بٹن)
            끝가=max(0,min(너비-1,가+차이[0]));ختم_کرو_عمودی=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ختم_کرو_عمودی,بٹن);가리키기(끝가,ختم_کرو_عمودی,0);숨고르기()
            if بٹن==1:
                왼,위,폭,لمبائی_قدر=کھڑکی;오른,아래=왼+폭,위+لمبائی_قدر
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ختم_کرو_عمودی-세))
                else:아래=max(위+216,min(높이,아래+ختم_کرو_عمودی-세))
                کھڑکی[:]=[왼,위,오른-왼,아래-위]
        تصدیق_کرو_سائز();assert پوائنٹر_خفیہ[0]
        پھر_سائز_کرو_گھسیٹو(4,(-100,-60),4);تصدیق_کرو_سائز() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            پھر_سائز_کرو_گھسیٹو(방향,차이);تصدیق_کرو_سائز()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        متن_پیجو("echo '"+긴글+"'");숨고르기()
        پھر_سائز_کرو_گھسیٹو(4,(-1000,-1000));assert کھڑکی[2:]==[360,216]
        پھر_سائز_کرو_گھسیٹو(4,(너비,높이))
        چلاؤ=متن_پیجو('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),چلاؤ);تصدیق_کرو_سائز()
        # vi가 تدوین_قدر 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        شیل('ftpd start')
        منتقلی_قدر=ftplib.FTP();منتقلی_قدر.encoding='utf-8';منتقلی_قدر.connect('127.0.0.1',접속번호,timeout=20);منتقلی_قدر.login()
        기다리기(b'NORMAL',متن_پیجو('vi /크기자료.txt\n'))
        기다리기(b'INSERT',متن_پیجو('i미저장 한글 کوائف\n'));숨고르기()
        پھر_سائز_کرو_گھسیٹو(4,(-너비,-높이))
        # ANSI صف_قدر 이동에 새 صف_قدر 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((کھڑکی[3]-56)//16)).encode() in لاگ_صف[-4096:]
        متن_پیجو('작은 창에서도 이어 لکھو\n');숨고르기()
        پھر_سائز_کرو_گھسیٹو(4,(너비,높이))
        متن_پیجو('큰 창에서도 이어 لکھو\n');숨고르기()
        کلک_کرو_بٹن(0xff1b);کلک_کرو_بٹن(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',متن_پیجو(':wq\n'))
        اجزاء_قدر=bytearray();منتقلی_قدر.retrbinary('RETR 크기자료.txt',اجزاء_قدر.extend)
        assert اجزاء_قدر=='미저장 한글 کوائف\n작은 창에서도 이어 لکھو\n큰 창에서도 이어 لکھو\n'.encode(),اجزاء_قدر
        تصدیق_کرو_سائز().save(str(결과경로/(سائز_متن+'-large.png')))
        # 두 번째 창은 طےشدہ_قدر سائز, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        چلاؤ=len(لاگ_صف);کلک_کرو_قدر(70,16);기다리기(b'TERMINAL FOCUS 2',چلاؤ)
        assert 'TERMINAL SIZE 68x19' in شیل('terminal size')
        چلاؤ=len(لاگ_صف);کلک_کرو_قدر(180,16);기다리기(b'TERMINAL FOCUS 1',چلاؤ);تصدیق_کرو_سائز()
        پھر_سائز_کرو_گھسیٹو(4,(-너비,-높이));تصدیق_کرو_سائز().save(str(결과경로/(سائز_متن+'-small.png')))
        # سائز تبدیل_کرو_قدر پیچھے_قدر X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        چلاؤ=len(لاگ_صف);کلک_کرو_قدر(کھڑکی[0]+کھڑکی[2]-20,کھڑکی[1]+15);기다리기(b'TERMINAL FOCUS 2',چلاؤ)
        assert 'RESIZE CLOSED' in شیل('echo RESIZE CLOSED')
        print('PASS:',سائز_متن,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if منتقلی_قدر:منتقلی_قدر.close()
        if بعيد_قدر:بعيد_قدر.close()
        if عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try:عمل_قدر.wait(timeout=8)
            except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
        منتخب_کرنڑ_آلا_a916db4e.close();عمل_قدر.stdout.close();(결과경로/(سائز_متن+'.log')).write_bytes(لاگ_صف)


def چلاؤ():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    لاگ_صف={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);لاگ_صف['resolutions'].append([너비,높이])
        لاگ_صف.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':چلاؤ()
