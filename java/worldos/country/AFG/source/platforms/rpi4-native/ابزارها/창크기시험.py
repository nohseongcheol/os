#!/usr/bin/env python3
"""واقعی_داده_ها QEMU/VNC에서 پایانه 모서리 کشیدن_مقدار·اشاره_گر·동적 نویسه_مقدار شکاف_ورودی·ویرایش_مقدار محتوا_مقدار 보존를 검사한다."""
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
from رایانه_نما import 정확한값
from اجرا_فرمان import نمایش_دادن_جذر


def 창크기시험(너비, 높이, سنجش_مسیر):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); شماره_درگاه = 임시.getsockname()[1]
    اندازه_کردن_متن = '{}x{}'.format(너비, 높이)
    فرآیند_مقدار = subprocess.Popen(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(شماره_درگاه), '--resolution', اندازه_کردن_متن], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    انتخاب_کننده_a916db4e = selectors.DefaultSelector(); انتخاب_کننده_a916db4e.register(فرآیند_مقدار.stdout, selectors.EVENT_READ)
    واقعه_نگار_ردیف = bytearray(); راه_دور_مقدار = None; انتقال_مقدار_630ba093 = None; اشاره_گر_پنهان=[False]

    def 기다리기(نمایش_مقدار, اجرا_2=0):
        마감 = time.monotonic() + 60
        while نمایش_مقدار not in واقعه_نگار_ردیف[اجرا_2:]:
            if time.monotonic() > 마감 or فرآیند_مقدار.poll() is not None or b'HALTED' in واقعه_نگار_ردیف or b'PANIC:' in واقعه_نگار_ردیف:
                raise AssertionError(واقعه_نگار_ردیف[اجرا_2:].decode('utf-8', 'replace'))
            for رویداد, _ in انتخاب_کننده_a916db4e.select(.1):
                داده_ها = رویداد.fileobj.read(65536)
                if داده_ها: واقعه_نگار_ردیف.extend(داده_ها)
        return واقعه_نگار_ردیف[اجرا_2:].decode('utf-8', 'replace')

    def کلیک_دکمه(نماد, 눌림=True): راه_دور_مقدار.sendall(struct.pack('>BBHI', 4, int(눌림), 0, نماد))

    def ارسال_متن(متن):
        اجرا_2 = len(واقعه_نگار_ردیف)
        for نویسه_مقدار in متن:
            نماد = 0xff0d if نویسه_مقدار == '\n' else ord(نویسه_مقدار) if ord(نویسه_مقدار) < 256 else 0x1000000 | ord(نویسه_مقدار)
            کلیک_دکمه(نماد); کلیک_دکمه(نماد, False)
        return اجرا_2

    def واسط(متن): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ارسال_متن(متن+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, عمودی_مرتب_کردن, 눌림): راه_دور_مقدار.sendall(struct.pack('>BBHH', 5, 눌림, 가로, عمودی_مرتب_کردن))

    def کلیک_مقدار(가로, عمودی_مرتب_کردن): 가리키기(가로, عمودی_مرتب_کردن, 1); 가리키기(가로, عمودی_مرتب_کردن, 0)

    def نقش_نقطه_ای_عکس():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 واقعی_داده_ها 너비를 쓴다.
        راه_دور_مقدار.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        نقاشی_مقدار = Image.new('RGB', (너비, 높이)); مقوله_مقدار = 0
        while True:
            종류 = 정확한값(راه_دور_مقدار, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                طول_مقدار = struct.unpack('>I', 정확한값(راه_دور_مقدار, 7)[3:])[0]; 정확한값(راه_دور_مقدار, طول_مقدار); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(راه_دور_مقدار, 3)[1:])[0]
            for _ in range(개수):
                가로, عمودی_مرتب_کردن, 폭, طول_مقدار, رمزگذاری_مقدار = struct.unpack('>HHHHi', 정확한값(راه_دور_مقدار, 12))
                if رمزگذاری_مقدار == -239:
                    assert 폭==0 and طول_مقدار==0, 'remote cursor must be hidden'
                    اشاره_گر_پنهان[0]=True
                    continue
                assert رمزگذاری_مقدار == 0 and 가로+폭 <= 너비 and عمودی_مرتب_کردن+طول_مقدار <= 높이
                نقاشی_مقدار.paste(Image.frombytes('RGB', (폭, طول_مقدار), 정확한값(راه_دور_مقدار, 폭*طول_مقدار*4), 'raw', 'BGRX'), (가로, عمودی_مرتب_کردن))
                مقوله_مقدار += 폭*طول_مقدار
            if مقوله_مقدار:
                assert مقوله_مقدار == 너비*높이, مقوله_مقدار
                return نقاشی_مقدار

    def بررسی_پیکسل(مختصات_مقدار, 색):
        마감 = time.monotonic()+10
        while True:
            نقاشی_مقدار = نقش_نقطه_ای_عکس()
            if نقاشی_مقدار.getpixel(مختصات_مقدار) == 색: return نقاشی_مقدار
            if time.monotonic() > 마감: raise AssertionError((مختصات_مقدار, نقاشی_مقدار.getpixel(مختصات_مقدار), 색))

    def آپلود_فایل(نام, داده_ها): انتقال_مقدار_630ba093.storbinary('STOR '+نام, io.BytesIO(داده_ها))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+اندازه_کردن_متن+' RGB32').encode() in واقعه_نگار_ردیف
        print('BOOT:', اندازه_کردن_متن, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', واقعه_نگار_ردیف).group(1))
        راه_دور_مقدار = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(راه_دور_مقدار, 12) == b'RFB 003.008\n'; راه_دور_مقدار.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(راه_دور_مقدار, 정확한값(راه_دور_مقدار, 1)[0]); راه_دور_مقدار.sendall(b'\x01')
        assert 정확한값(راه_دور_مقدار, 4) == b'\0'*4; راه_دور_مقدار.sendall(b'\x01')
        초기 = 정확한값(راه_دور_مقدار, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(راه_دور_مقدار, struct.unpack('>I', 초기[20:])[0])
        راه_دور_مقدار.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        راه_دور_مقدار.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        بررسی_پیکسل((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for رویداد,_ in انتخاب_کننده_a916db4e.select(.02):
                    داده_ها=رویداد.fileobj.read(65536)
                    if داده_ها:واقعه_نگار_ردیف.extend(داده_ها)
        پنجره=[12,48,568,360]
        def تأیید_صحت_اندازه_کردن():
            ستون_مقدار,ردیف_مقدار=(پنجره[2]-24)//8,(پنجره[3]-56)//16
            متن=واسط('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ستون_مقدار,ردیف_مقدار) in متن,متن
            # واقعی_داده_ها پنجره 테두리: 단지 اندازه جستار_مقدار 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            بررسی_پیکسل((پنجره[0],پنجره[1]),(32,80,144))
            نقاشی_مقدار=بررسی_پیکسل((پنجره[0]+پنجره[2]-1,پنجره[1]+پنجره[3]-1),(39,49,64))
            return نقاشی_مقدار
        def 모서리(방향):
            return (پنجره[0]+(3 if 방향 in (1,3) else پنجره[2]-4),پنجره[1]+(3 if 방향<=2 else پنجره[3]-4))
        def تغییر_اندازه_کشیدن(방향,차이,دکمه=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            بررسی_پیکسل(흰점,(255,255,255))
            가리키기(가,세,دکمه)
            끝가=max(0,min(너비-1,가+차이[0]));پایان_دادن_عمودی=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,پایان_دادن_عمودی,دکمه);가리키기(끝가,پایان_دادن_عمودی,0);숨고르기()
            if دکمه==1:
                왼,위,폭,طول_مقدار=پنجره;오른,아래=왼+폭,위+طول_مقدار
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+پایان_دادن_عمودی-세))
                else:아래=max(위+216,min(높이,아래+پایان_دادن_عمودی-세))
                پنجره[:]=[왼,위,오른-왼,아래-위]
        تأیید_صحت_اندازه_کردن();assert اشاره_گر_پنهان[0]
        تغییر_اندازه_کشیدن(4,(-100,-60),4);تأیید_صحت_اندازه_کردن() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            تغییر_اندازه_کشیدن(방향,차이);تأیید_صحت_اندازه_کردن()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ارسال_متن("echo '"+긴글+"'");숨고르기()
        تغییر_اندازه_کشیدن(4,(-1000,-1000));assert پنجره[2:]==[360,216]
        تغییر_اندازه_کشیدن(4,(너비,높이))
        اجرا_2=ارسال_متن('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),اجرا_2);تأیید_صحت_اندازه_کردن()
        # vi가 ویرایش_مقدار 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        واسط('ftpd start')
        انتقال_مقدار_630ba093=ftplib.FTP();انتقال_مقدار_630ba093.encoding='utf-8';انتقال_مقدار_630ba093.connect('127.0.0.1',شماره_درگاه,timeout=20);انتقال_مقدار_630ba093.login()
        기다리기(b'NORMAL',ارسال_متن('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ارسال_متن('i미저장 한글 داده_ها\n'));숨고르기()
        تغییر_اندازه_کشیدن(4,(-너비,-높이))
        # ANSI ردیف_مقدار 이동에 새 ردیف_مقدار 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((پنجره[3]-56)//16)).encode() in واقعه_نگار_ردیف[-4096:]
        ارسال_متن('작은 창에서도 이어 نوشتن\n');숨고르기()
        تغییر_اندازه_کشیدن(4,(너비,높이))
        ارسال_متن('큰 창에서도 이어 نوشتن\n');숨고르기()
        کلیک_دکمه(0xff1b);کلیک_دکمه(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ارسال_متن(':wq\n'))
        محتوا_مقدار=bytearray();انتقال_مقدار_630ba093.retrbinary('RETR 크기자료.txt',محتوا_مقدار.extend)
        assert محتوا_مقدار=='미저장 한글 داده_ها\n작은 창에서도 이어 نوشتن\n큰 창에서도 이어 نوشتن\n'.encode(),محتوا_مقدار
        تأیید_صحت_اندازه_کردن().save(str(سنجش_مسیر/(اندازه_کردن_متن+'-large.png')))
        # 두 번째 창은 مقدار_پیش_فرض اندازه, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        اجرا_2=len(واقعه_نگار_ردیف);کلیک_مقدار(70,16);기다리기(b'TERMINAL FOCUS 2',اجرا_2)
        assert 'TERMINAL SIZE 68x19' in واسط('terminal size')
        اجرا_2=len(واقعه_نگار_ردیف);کلیک_مقدار(180,16);기다리기(b'TERMINAL FOCUS 1',اجرا_2);تأیید_صحت_اندازه_کردن()
        تغییر_اندازه_کشیدن(4,(-너비,-높이));تأیید_صحت_اندازه_کردن().save(str(سنجش_مسیر/(اندازه_کردن_متن+'-small.png')))
        # اندازه تغییر_مقدار برگشت_مقدار X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        اجرا_2=len(واقعه_نگار_ردیف);کلیک_مقدار(پنجره[0]+پنجره[2]-20,پنجره[1]+15);기다리기(b'TERMINAL FOCUS 2',اجرا_2)
        assert 'RESIZE CLOSED' in واسط('echo RESIZE CLOSED')
        print('PASS:',اندازه_کردن_متن,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if انتقال_مقدار_630ba093:انتقال_مقدار_630ba093.close()
        if راه_دور_مقدار:راه_دور_مقدار.close()
        if فرآیند_مقدار.poll() is None:
            فرآیند_مقدار.terminate()
            try:فرآیند_مقدار.wait(timeout=8)
            except subprocess.TimeoutExpired:فرآیند_مقدار.kill();فرآیند_مقدار.wait()
        انتخاب_کننده_a916db4e.close();فرآیند_مقدار.stdout.close();(سنجش_مسیر/(اندازه_کردن_متن+'.log')).write_bytes(واقعه_نگار_ردیف)


def اجرا_2():
    سنجش_مسیر=نمایش_دادن_جذر/'build/verification/resize';سنجش_مسیر.mkdir(parents=True,exist_ok=True)
    واقعه_نگار_ردیف={'passed':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,سنجش_مسیر);واقعه_نگار_ردیف['resolutions'].append([너비,높이])
        واقعه_نگار_ردیف.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(سنجش_مسیر/'report.json').write_text(json.dumps(واقعه_نگار_ردیف,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':اجرا_2()
