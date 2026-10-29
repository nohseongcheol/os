#!/usr/bin/env python3
"""اصل_کوائف QEMU/VNC에서 حکم_کی_تشریح_کرنے_والا 모서리 گھسیٹیں_قدر·پوائنٹر·동적 کریکٹر_قدر سلاٹ_اندراج·تدوین_قدر مشمول_قدر 보존를 검사한다."""
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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def 창크기시험(너비, 높이, پیمائش_راہ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); دہانہ_نمبر = 임시.getsockname()[1]
    سائز_دیں_متن = '{}x{}'.format(너비, 높이)
    عمل_قدر = subprocess.Popen(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(دہانہ_نمبر), '--resolution', سائز_دیں_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کنندہ_a916db4e = selectors.DefaultSelector(); منتخب_کنندہ_a916db4e.register(عمل_قدر.stdout, selectors.EVENT_READ)
    لاگ_صف = bytearray(); بعید_قدر = None; منتقلی_قدر = None; پوائنٹر_خفیہ=[False]

    def 기다리기(دکھانا_قدر, چلائیں=0):
        마감 = time.monotonic() + 60
        while دکھانا_قدر not in لاگ_صف[چلائیں:]:
            if time.monotonic() > 마감 or عمل_قدر.poll() is not None or b'HALTED' in لاگ_صف or b'PANIC:' in لاگ_صف:
                raise AssertionError(لاگ_صف[چلائیں:].decode('utf-8', 'replace'))
            for واقعہ, _ in منتخب_کنندہ_a916db4e.select(.1):
                کوائف = واقعہ.fileobj.read(65536)
                if کوائف: لاگ_صف.extend(کوائف)
        return لاگ_صف[چلائیں:].decode('utf-8', 'replace')

    def کلک_بٹن(علامت, 눌림=True): بعید_قدر.sendall(struct.pack('>BBHI', 4, int(눌림), 0, علامت))

    def SMS_بھیجیں(متن):
        چلائیں = len(لاگ_صف)
        for کریکٹر_قدر in متن:
            علامت = 0xff0d if کریکٹر_قدر == '\n' else ord(کریکٹر_قدر) if ord(کریکٹر_قدر) < 256 else 0x1000000 | ord(کریکٹر_قدر)
            کلک_بٹن(علامت); کلک_بٹن(علامت, False)
        return چلائیں

    def شیل(متن): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_بھیجیں(متن+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 눌림): بعید_قدر.sendall(struct.pack('>BBHH', 5, 눌림, 가로, عمودی_پوزیشن_ٹھیک_کریں))

    def کلک_قدر(가로, عمودی_پوزیشن_ٹھیک_کریں): 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 1); 가리키기(가로, عمودی_پوزیشن_ٹھیک_کریں, 0)

    def بِٹ_میپ_نقش():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 اصل_کوائف 너비를 쓴다.
        بعید_قدر.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ڈرائنگ_قدر = Image.new('RGB', (너비, 높이)); زمرہ_قدر_9285603e = 0
        while True:
            종류 = 정확한값(بعید_قدر, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                لمبا_ئی_قدر = struct.unpack('>I', 정확한값(بعید_قدر, 7)[3:])[0]; 정확한값(بعید_قدر, لمبا_ئی_قدر); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(بعید_قدر, 3)[1:])[0]
            for _ in range(개수):
                가로, عمودی_پوزیشن_ٹھیک_کریں, 폭, لمبا_ئی_قدر, ضابطہ_بندی_قدر = struct.unpack('>HHHHi', 정확한값(بعید_قدر, 12))
                if ضابطہ_بندی_قدر == -239:
                    assert 폭==0 and لمبا_ئی_قدر==0, 'remote cursor must be hidden'
                    پوائنٹر_خفیہ[0]=True
                    continue
                assert ضابطہ_بندی_قدر == 0 and 가로+폭 <= 너비 and عمودی_پوزیشن_ٹھیک_کریں+لمبا_ئی_قدر <= 높이
                ڈرائنگ_قدر.paste(Image.frombytes('RGB', (폭, لمبا_ئی_قدر), 정확한값(بعید_قدر, 폭*لمبا_ئی_قدر*4), 'raw', 'BGRX'), (가로, عمودی_پوزیشن_ٹھیک_کریں))
                زمرہ_قدر_9285603e += 폭*لمبا_ئی_قدر
            if زمرہ_قدر_9285603e:
                assert زمرہ_قدر_9285603e == 너비*높이, زمرہ_قدر_9285603e
                return ڈرائنگ_قدر

    def پڑتال_کریں_پکسل(محدد_قدر, 색):
        마감 = time.monotonic()+10
        while True:
            ڈرائنگ_قدر = بِٹ_میپ_نقش()
            if ڈرائنگ_قدر.getpixel(محدد_قدر) == 색: return ڈرائنگ_قدر
            if time.monotonic() > 마감: raise AssertionError((محدد_قدر, ڈرائنگ_قدر.getpixel(محدد_قدر), 색))

    def اپ_لوڈ_کريں_فائلیں(نام, کوائف): منتقلی_قدر.storbinary('STOR '+نام, io.BytesIO(کوائف))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+سائز_دیں_متن+' RGB32').encode() in لاگ_صف
        print('BOOT:', سائز_دیں_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', لاگ_صف).group(1))
        بعید_قدر = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(بعید_قدر, 12) == b'RFB 003.008\n'; بعید_قدر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(بعید_قدر, 정확한값(بعید_قدر, 1)[0]); بعید_قدر.sendall(b'\x01')
        assert 정확한값(بعید_قدر, 4) == b'\0'*4; بعید_قدر.sendall(b'\x01')
        초기 = 정확한값(بعید_قدر, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(بعید_قدر, struct.unpack('>I', 초기[20:])[0])
        بعید_قدر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        بعید_قدر.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        پڑتال_کریں_پکسل((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for واقعہ,_ in منتخب_کنندہ_a916db4e.select(.02):
                    کوائف=واقعہ.fileobj.read(65536)
                    if کوائف:لاگ_صف.extend(کوائف)
        ونڈو=[12,48,568,360]
        def تصدیق_کریں_سائز_دیں():
            کالم_قدر,صف_قدر=(ونڈو[2]-24)//8,(ونڈو[3]-56)//16
            متن=شیل('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(کالم_قدر,صف_قدر) in متن,متن
            # اصل_کوائف ونڈو 테두리: 단지 حجم طلب_قدر 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            پڑتال_کریں_پکسل((ونڈو[0],ونڈو[1]),(32,80,144))
            ڈرائنگ_قدر=پڑتال_کریں_پکسل((ونڈو[0]+ونڈو[2]-1,ونڈو[1]+ونڈو[3]-1),(39,49,64))
            return ڈرائنگ_قدر
        def 모서리(방향):
            return (ونڈو[0]+(3 if 방향 in (1,3) else ونڈو[2]-4),ونڈو[1]+(3 if 방향<=2 else ونڈو[3]-4))
        def سائز_تبدیل_کریں_گھسیٹیں(방향,차이,بٹن=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            پڑتال_کریں_پکسل(흰점,(255,255,255))
            가리키기(가,세,بٹن)
            끝가=max(0,min(너비-1,가+차이[0]));اختتام_عمودی=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,اختتام_عمودی,بٹن);가리키기(끝가,اختتام_عمودی,0);숨고르기()
            if بٹن==1:
                왼,위,폭,لمبا_ئی_قدر=ونڈو;오른,아래=왼+폭,위+لمبا_ئی_قدر
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+اختتام_عمودی-세))
                else:아래=max(위+216,min(높이,아래+اختتام_عمودی-세))
                ونڈو[:]=[왼,위,오른-왼,아래-위]
        تصدیق_کریں_سائز_دیں();assert پوائنٹر_خفیہ[0]
        سائز_تبدیل_کریں_گھسیٹیں(4,(-100,-60),4);تصدیق_کریں_سائز_دیں() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            سائز_تبدیل_کریں_گھسیٹیں(방향,차이);تصدیق_کریں_سائز_دیں()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_بھیجیں("echo '"+긴글+"'");숨고르기()
        سائز_تبدیل_کریں_گھسیٹیں(4,(-1000,-1000));assert ونڈو[2:]==[360,216]
        سائز_تبدیل_کریں_گھسیٹیں(4,(너비,높이))
        چلائیں=SMS_بھیجیں('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),چلائیں);تصدیق_کریں_سائز_دیں()
        # vi가 تدوین_قدر 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        شیل('ftpd start')
        منتقلی_قدر=ftplib.FTP();منتقلی_قدر.encoding='utf-8';منتقلی_قدر.connect('127.0.0.1',دہانہ_نمبر,timeout=20);منتقلی_قدر.login()
        기다리기(b'NORMAL',SMS_بھیجیں('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_بھیجیں('i미저장 한글 کوائف\n'));숨고르기()
        سائز_تبدیل_کریں_گھسیٹیں(4,(-너비,-높이))
        # ANSI صف_قدر 이동에 새 صف_قدر 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ونڈو[3]-56)//16)).encode() in لاگ_صف[-4096:]
        SMS_بھیجیں('작은 창에서도 이어 لکھیں\n');숨고르기()
        سائز_تبدیل_کریں_گھسیٹیں(4,(너비,높이))
        SMS_بھیجیں('큰 창에서도 이어 لکھیں\n');숨고르기()
        کلک_بٹن(0xff1b);کلک_بٹن(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_بھیجیں(':wq\n'))
        مشمول_قدر=bytearray();منتقلی_قدر.retrbinary('RETR 크기자료.txt',مشمول_قدر.extend)
        assert مشمول_قدر=='미저장 한글 کوائف\n작은 창에서도 이어 لکھیں\n큰 창에서도 이어 لکھیں\n'.encode(),مشمول_قدر
        تصدیق_کریں_سائز_دیں().save(str(پیمائش_راہ/(سائز_دیں_متن+'-large.png')))
        # 두 번째 창은 طے_شدہ_قدر حجم, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        چلائیں=len(لاگ_صف);کلک_قدر(70,16);기다리기(b'TERMINAL FOCUS 2',چلائیں)
        assert 'TERMINAL SIZE 68x19' in شیل('terminal size')
        چلائیں=len(لاگ_صف);کلک_قدر(180,16);기다리기(b'TERMINAL FOCUS 1',چلائیں);تصدیق_کریں_سائز_دیں()
        سائز_تبدیل_کریں_گھسیٹیں(4,(-너비,-높이));تصدیق_کریں_سائز_دیں().save(str(پیمائش_راہ/(سائز_دیں_متن+'-small.png')))
        # حجم تبدیل_کریں_قدر واپس_قدر X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        چلائیں=len(لاگ_صف);کلک_قدر(ونڈو[0]+ونڈو[2]-20,ونڈو[1]+15);기다리기(b'TERMINAL FOCUS 2',چلائیں)
        assert 'RESIZE CLOSED' in شیل('echo RESIZE CLOSED')
        print('PASS:',سائز_دیں_متن,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if منتقلی_قدر:منتقلی_قدر.close()
        if بعید_قدر:بعید_قدر.close()
        if عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try:عمل_قدر.wait(timeout=8)
            except subprocess.TimeoutExpired:عمل_قدر.kill();عمل_قدر.wait()
        منتخب_کنندہ_a916db4e.close();عمل_قدر.stdout.close();(پیمائش_راہ/(سائز_دیں_متن+'.log')).write_bytes(لاگ_صف)


def چلائیں():
    پیمائش_راہ=عکس_ڈالنا_روٹ/'build/verification/resize';پیمائش_راہ.mkdir(parents=True,exist_ok=True)
    لاگ_صف={'passed':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,پیمائش_راہ);لاگ_صف['resolutions'].append([너비,높이])
        لاگ_صف.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(پیمائش_راہ/'report.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':چلائیں()
