#!/usr/bin/env python3
"""اصلي_ڪوائف QEMU/VNC에서 터미널 모서리 گهليو_قدر·پوائنٽر·동적 ڪريڪٽر_قدر سوراخ_داخلا·تدوين_قدر مواد_قدر 보존를 검사한다."""
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
from ڊيسڪٽاپ_منظر import 정확한값
from تعميل_ڪرڻ_حڪم import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    سائيز_متن = '{}x{}'.format(너비, 높이)
    عمل_قدر = subprocess.Popen(['python3', str(기준/'اوزار/تعميل_ڪرڻ_حڪم.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', سائيز_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    چونڊيندڙ_a916db4e = selectors.DefaultSelector(); چونڊيندڙ_a916db4e.register(عمل_قدر.stdout, selectors.EVENT_READ)
    لاگ_صف = bytearray(); بعيد_قدر = None; منتقلي_قدر = None; پوائنٽر_ڳجهو=[False]

    def 기다리기(نمائش_ڪريو_قدر, هلائڻ=0):
        마감 = time.monotonic() + 60
        while نمائش_ڪريو_قدر not in لاگ_صف[هلائڻ:]:
            if time.monotonic() > 마감 or عمل_قدر.poll() is not None or b'HALTED' in لاگ_صف or b'PANIC:' in لاگ_صف:
                raise AssertionError(لاگ_صف[هلائڻ:].decode('utf-8', 'replace'))
            for واقعو, _ in چونڊيندڙ_a916db4e.select(.1):
                ڪوائف = واقعو.fileobj.read(65536)
                if ڪوائف: لاگ_صف.extend(ڪوائف)
        return لاگ_صف[هلائڻ:].decode('utf-8', 'replace')

    def ڪلڪ_ڪريو_بٽن(نشاني, 눌림=True): بعيد_قدر.sendall(struct.pack('>BBHI', 4, int(눌림), 0, نشاني))

    def SMS_موڪليو(متن):
        هلائڻ = len(لاگ_صف)
        for ڪريڪٽر_قدر in متن:
            نشاني = 0xff0d if ڪريڪٽر_قدر == '\n' else ord(ڪريڪٽر_قدر) if ord(ڪريڪٽر_قدر) < 256 else 0x1000000 | ord(ڪريڪٽر_قدر)
            ڪلڪ_ڪريو_بٽن(نشاني); ڪلڪ_ڪريو_بٽن(نشاني, False)
        return هلائڻ

    def شيل(متن): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_موڪليو(متن+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): بعيد_قدر.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ڪلڪ_ڪريو_قدر(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def بٽ_نقشو_نقش():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 اصلي_ڪوائف 너비를 쓴다.
        بعيد_قدر.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ڊرائنگ_قدر = Image.new('RGB', (너비, 높이)); قسم_قدر_9285603e = 0
        while True:
            종류 = 정확한값(بعيد_قدر, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                لمبائي_قدر = struct.unpack('>I', 정확한값(بعيد_قدر, 7)[3:])[0]; 정확한값(بعيد_قدر, لمبائي_قدر); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعيد_قدر, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, لمبائي_قدر, ضابطه_ربائي_قدر = struct.unpack('>HHHHi', 정확한값(بعيد_قدر, 12))
                if ضابطه_ربائي_قدر == -239:
                    assert 폭==0 and لمبائي_قدر==0, 'remote cursor must be hidden'
                    پوائنٽر_ڳجهو[0]=True
                    continue
                assert ضابطه_ربائي_قدر == 0 and 가로+폭 <= 너비 and 세로+لمبائي_قدر <= 높이
                ڊرائنگ_قدر.paste(Image.frombytes('RGB', (폭, لمبائي_قدر), 정확한값(بعيد_قدر, 폭*لمبائي_قدر*4), 'raw', 'BGRX'), (가로, 세로))
                قسم_قدر_9285603e += 폭*لمبائي_قدر
            if قسم_قدر_9285603e:
                assert قسم_قدر_9285603e == 너비*높이, قسم_قدر_9285603e
                return ڊرائنگ_قدر

    def پڙتال_ڪريو_پيل(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ڊرائنگ_قدر = بٽ_نقشو_نقش()
            if ڊرائنگ_قدر.getpixel(좌표) == 색: return ڊرائنگ_قدر
            if time.monotonic() > 마감: raise AssertionError((좌표, ڊرائنگ_قدر.getpixel(좌표), 색))

    def اپ_لوڊ_ڪريو_فائلون(نالو, ڪوائف): منتقلي_قدر.storbinary('STOR '+نالو, io.BytesIO(ڪوائف))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+سائيز_متن+' RGB32').encode() in لاگ_صف
        print('BOOT:', سائيز_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', لاگ_صف).group(1))
        بعيد_قدر = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(بعيد_قدر, 12) == b'RFB 003.008\n'; بعيد_قدر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعيد_قدر, 정확한값(بعيد_قدر, 1)[0]); بعيد_قدر.sendall(b'\x01')
        assert 정확한값(بعيد_قدر, 4) == b'\0'*4; بعيد_قدر.sendall(b'\x01')
        초기 = 정확한값(بعيد_قدر, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(بعيد_قدر, struct.unpack('>I', 초기[20:])[0])
        بعيد_قدر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعيد_قدر.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        پڙتال_ڪريو_پيل((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for واقعو,_ in چونڊيندڙ_a916db4e.select(.02):
                    ڪوائف=واقعو.fileobj.read(65536)
                    if ڪوائف:لاگ_صف.extend(ڪوائف)
        دري=[12,48,568,360]
        def تصديق_ڪريو_سائيز():
            ڪالم_قدر,صف_قدر=(دري[2]-24)//8,(دري[3]-56)//16
            متن=شيل('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ڪالم_قدر,صف_قدر) in متن,متن
            # اصلي_ڪوائف دري 테두리: 단지 سائيز سوال_قدر 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            پڙتال_ڪريو_پيل((دري[0],دري[1]),(32,80,144))
            ڊرائنگ_قدر=پڙتال_ڪريو_پيل((دري[0]+دري[2]-1,دري[1]+دري[3]-1),(39,49,64))
            return ڊرائنگ_قدر
        def 모서리(방향):
            return (دري[0]+(3 if 방향 in (1,3) else دري[2]-4),دري[1]+(3 if 방향<=2 else دري[3]-4))
        def ٻيهر_سائيز_ڪريو_گهليو(방향,차이,بٽن=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            پڙتال_ڪريو_پيل(흰점,(255,255,255))
            가리키기(가,세,بٽن)
            끝가=max(0,min(너비-1,가+차이[0]));ختم_ڪريو_عمودي=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ختم_ڪريو_عمودي,بٽن);가리키기(끝가,ختم_ڪريو_عمودي,0);숨고르기()
            if بٽن==1:
                왼,위,폭,لمبائي_قدر=دري;오른,아래=왼+폭,위+لمبائي_قدر
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ختم_ڪريو_عمودي-세))
                else:아래=max(위+216,min(높이,아래+ختم_ڪريو_عمودي-세))
                دري[:]=[왼,위,오른-왼,아래-위]
        تصديق_ڪريو_سائيز();assert پوائنٽر_ڳجهو[0]
        ٻيهر_سائيز_ڪريو_گهليو(4,(-100,-60),4);تصديق_ڪريو_سائيز() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ٻيهر_سائيز_ڪريو_گهليو(방향,차이);تصديق_ڪريو_سائيز()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_موڪليو("echo '"+긴글+"'");숨고르기()
        ٻيهر_سائيز_ڪريو_گهليو(4,(-1000,-1000));assert دري[2:]==[360,216]
        ٻيهر_سائيز_ڪريو_گهليو(4,(너비,높이))
        هلائڻ=SMS_موڪليو('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),هلائڻ);تصديق_ڪريو_سائيز()
        # vi가 تدوين_قدر 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        شيل('ftpd start')
        منتقلي_قدر=ftplib.FTP();منتقلي_قدر.encoding='utf-8';منتقلي_قدر.connect('127.0.0.1',접속번호,timeout=20);منتقلي_قدر.login()
        기다리기(b'NORMAL',SMS_موڪليو('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_موڪليو('i미저장 한글 ڪوائف\n'));숨고르기()
        ٻيهر_سائيز_ڪريو_گهليو(4,(-너비,-높이))
        # ANSI صف_قدر 이동에 새 صف_قدر 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((دري[3]-56)//16)).encode() in لاگ_صف[-4096:]
        SMS_موڪليو('작은 창에서도 이어 لکو\n');숨고르기()
        ٻيهر_سائيز_ڪريو_گهليو(4,(너비,높이))
        SMS_موڪليو('큰 창에서도 이어 لکو\n');숨고르기()
        ڪلڪ_ڪريو_بٽن(0xff1b);ڪلڪ_ڪريو_بٽن(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_موڪليو(':wq\n'))
        مواد_قدر=bytearray();منتقلي_قدر.retrbinary('RETR 크기자료.txt',مواد_قدر.extend)
        assert مواد_قدر=='미저장 한글 ڪوائف\n작은 창에서도 이어 لکو\n큰 창에서도 이어 لکو\n'.encode(),مواد_قدر
        تصديق_ڪريو_سائيز().save(str(결과경로/(سائيز_متن+'-large.png')))
        # 두 번째 창은 طئي_ٿيل_ملهه سائيز, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        هلائڻ=len(لاگ_صف);ڪلڪ_ڪريو_قدر(70,16);기다리기(b'TERMINAL FOCUS 2',هلائڻ)
        assert 'TERMINAL SIZE 68x19' in شيل('terminal size')
        هلائڻ=len(لاگ_صف);ڪلڪ_ڪريو_قدر(180,16);기다리기(b'TERMINAL FOCUS 1',هلائڻ);تصديق_ڪريو_سائيز()
        ٻيهر_سائيز_ڪريو_گهليو(4,(-너비,-높이));تصديق_ڪريو_سائيز().save(str(결과경로/(سائيز_متن+'-small.png')))
        # سائيز تبديل_ڪريو_قدر واپس_قدر X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        هلائڻ=len(لاگ_صف);ڪلڪ_ڪريو_قدر(دري[0]+دري[2]-20,دري[1]+15);기다리기(b'TERMINAL FOCUS 2',هلائڻ)
        assert 'RESIZE CLOSED' in شيل('echo RESIZE CLOSED')
        print('PASS:',سائيز_متن,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if منتقلي_قدر:منتقلي_قدر.close()
        if بعيد_قدر:بعيد_قدر.close()
        if عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try:عمل_قدر.wait(timeout=8)
            except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
        چونڊيندڙ_a916db4e.close();عمل_قدر.stdout.close();(결과경로/(سائيز_متن+'.log')).write_bytes(لاگ_صف)


def هلائڻ():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    لاگ_صف={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);لاگ_صف['resolutions'].append([너비,높이])
        لاگ_صف.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':هلائڻ()
