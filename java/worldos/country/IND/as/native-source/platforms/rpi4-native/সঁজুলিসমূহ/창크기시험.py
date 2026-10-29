#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা QEMU/VNC에서 টাৰ্মিনেল 모서리 টানক_মান·পইণ্টাৰ·동적 বৰ্ণ_মান শ্লট_প্রবিষ্ট·সম্পাদনা_মান সামগ্ৰী_মান 보존를 검사한다."""
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
from ডেস্কটপ_দর্শন import 정확한값
from নিষ্পাদন_আদেশ import 기준


def 창크기시험(너비, 높이, পৰিমাপ_পথ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    আকাৰ_কৰক_পাঠ = '{}x{}'.format(너비, 높이)
    প্ৰক্ৰিয়া_মান = subprocess.Popen(['python3', str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', আকাৰ_কৰক_পাঠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    চয়নকাৰী_a916db4e = selectors.DefaultSelector(); চয়নকাৰী_a916db4e.register(প্ৰক্ৰিয়া_মান.stdout, selectors.EVENT_READ)
    লগ_শাৰী = bytearray(); দূৰবৰ্তী_মান = None; স্থানান্তৰণ_মান = None; পইণ্টাৰ_লুকাই_থকা=[False]

    def 기다리기(শ্ব_মান, সঞ্চালন=0):
        마감 = time.monotonic() + 60
        while শ্ব_মান not in লগ_শাৰী[সঞ্চালন:]:
            if time.monotonic() > 마감 or প্ৰক্ৰিয়া_মান.poll() is not None or b'HALTED' in লগ_শাৰী or b'PANIC:' in লগ_শাৰী:
                raise AssertionError(লগ_শাৰী[সঞ্চালন:].decode('utf-8', 'replace'))
            for ইভেণ্ট, _ in চয়নকাৰী_a916db4e.select(.1):
                ডাটা = ইভেণ্ট.fileobj.read(65536)
                if ডাটা: লগ_শাৰী.extend(ডাটা)
        return লগ_শাৰী[সঞ্চালন:].decode('utf-8', 'replace')

    def ক্লিক_কৰক_বুটাম(প্ৰতীক, 눌림=True): দূৰবৰ্তী_মান.sendall(struct.pack('>BBHI', 4, int(눌림), 0, প্ৰতীক))

    def SMS_প্ৰেৰণ_কৰক(টেক্সট):
        সঞ্চালন = len(লগ_শাৰী)
        for বৰ্ণ_মান in টেক্সট:
            প্ৰতীক = 0xff0d if বৰ্ণ_মান == '\n' else ord(বৰ্ণ_মান) if ord(বৰ্ণ_মান) < 256 else 0x1000000 | ord(বৰ্ণ_মান)
            ক্লিক_কৰক_বুটাম(প্ৰতীক); ক্লিক_কৰক_বুটাম(প্ৰতীক, False)
        return সঞ্চালন

    def শ্বেল(টেক্সট): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_প্ৰেৰণ_কৰক(টেক্সট+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 눌림): দূৰবৰ্তী_মান.sendall(struct.pack('>BBHH', 5, 눌림, 가로, উলম্ব_স্থান_সলনি_কৰক))

    def ক্লিক_কৰক_মান(가로, উলম্ব_স্থান_সলনি_কৰক): 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 1); 가리키기(가로, উলম্ব_স্থান_সলনি_কৰক, 0)

    def বিটমেপ_ছবি():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 প্ৰকৃত_ডাটা 너비를 쓴다.
        দূৰবৰ্তী_মান.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        অংকন_মান = Image.new('RGB', (너비, 높이)); বৰ্গ_মান = 0
        while True:
            종류 = 정확한값(দূৰবৰ্তী_মান, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                দৈর্ঘ্য_মান = struct.unpack('>I', 정확한값(দূৰবৰ্তী_মান, 7)[3:])[0]; 정확한값(দূৰবৰ্তী_মান, দৈর্ঘ্য_মান); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(দূৰবৰ্তী_মান, 3)[1:])[0]
            for _ in range(개수):
                가로, উলম্ব_স্থান_সলনি_কৰক, 폭, দৈর্ঘ্য_মান, এনকোডিং_মান = struct.unpack('>HHHHi', 정확한값(দূৰবৰ্তী_মান, 12))
                if এনকোডিং_মান == -239:
                    assert 폭==0 and দৈর্ঘ্য_মান==0, 'remote cursor must be hidden'
                    পইণ্টাৰ_লুকাই_থকা[0]=True
                    continue
                assert এনকোডিং_মান == 0 and 가로+폭 <= 너비 and উলম্ব_স্থান_সলনি_কৰক+দৈর্ঘ্য_মান <= 높이
                অংকন_মান.paste(Image.frombytes('RGB', (폭, দৈর্ঘ্য_মান), 정확한값(দূৰবৰ্তী_মান, 폭*দৈর্ঘ্য_মান*4), 'raw', 'BGRX'), (가로, উলম্ব_স্থান_সলনি_কৰক))
                বৰ্গ_মান += 폭*দৈর্ঘ্য_মান
            if বৰ্গ_মান:
                assert বৰ্গ_মান == 너비*높이, বৰ্গ_মান
                return অংকন_মান

    def পৰীক্ষণ_পিক্সেল(সমন্বয়_মান, 색):
        마감 = time.monotonic()+10
        while True:
            অংকন_মান = বিটমেপ_ছবি()
            if অংকন_মান.getpixel(সমন্বয়_মান) == 색: return অংকন_মান
            if time.monotonic() > 마감: raise AssertionError((সমন্বয়_মান, অংকন_মান.getpixel(সমন্বয়_মান), 색))

    def আপল_ড_কৰক_ফাইলসমূহ(নাম, ডাটা): স্থানান্তৰণ_মান.storbinary('STOR '+নাম, io.BytesIO(ডাটা))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+আকাৰ_কৰক_পাঠ+' RGB32').encode() in লগ_শাৰী
        print('BOOT:', আকাৰ_কৰক_পাঠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', লগ_শাৰী).group(1))
        দূৰবৰ্তী_মান = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(দূৰবৰ্তী_মান, 12) == b'RFB 003.008\n'; দূৰবৰ্তী_মান.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(দূৰবৰ্তী_মান, 정확한값(দূৰবৰ্তী_মান, 1)[0]); দূৰবৰ্তী_মান.sendall(b'\x01')
        assert 정확한값(দূৰবৰ্তী_মান, 4) == b'\0'*4; দূৰবৰ্তী_মান.sendall(b'\x01')
        초기 = 정확한값(দূৰবৰ্তী_মান, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(দূৰবৰ্তী_মান, struct.unpack('>I', 초기[20:])[0])
        দূৰবৰ্তী_মান.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        দূৰবৰ্তী_মান.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        পৰীক্ষণ_পিক্সেল((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ইভেণ্ট,_ in চয়নকাৰী_a916db4e.select(.02):
                    ডাটা=ইভেণ্ট.fileobj.read(65536)
                    if ডাটা:লগ_শাৰী.extend(ডাটা)
        উইণ্ড=[12,48,568,360]
        def প্ৰমাণিত_কৰক_আকাৰ_কৰক():
            স্তম্ভ_মান,শাৰী_মান=(উইণ্ড[2]-24)//8,(উইণ্ড[3]-56)//16
            টেক্সট=শ্বেল('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(স্তম্ভ_মান,শাৰী_মান) in টেক্সট,টেক্সট
            # প্ৰকৃত_ডাটা উইণ্ড 테두리: 단지 মাপ কুৱেৰী_মান 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            পৰীক্ষণ_পিক্সেল((উইণ্ড[0],উইণ্ড[1]),(32,80,144))
            অংকন_মান=পৰীক্ষণ_পিক্সেল((উইণ্ড[0]+উইণ্ড[2]-1,উইণ্ড[1]+উইণ্ড[3]-1),(39,49,64))
            return অংকন_মান
        def 모서리(방향):
            return (উইণ্ড[0]+(3 if 방향 in (1,3) else উইণ্ড[2]-4),উইণ্ড[1]+(3 if 방향<=2 else উইণ্ড[3]-4))
        def পুণ_আকাৰ_কৰক_টানক(방향,차이,বুটাম=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            পৰীক্ষণ_পিক্সেল(흰점,(255,255,255))
            가리키기(가,세,বুটাম)
            끝가=max(0,min(너비-1,가+차이[0]));অন্ত_কৰক_উলম্ব=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,অন্ত_কৰক_উলম্ব,বুটাম);가리키기(끝가,অন্ত_কৰক_উলম্ব,0);숨고르기()
            if বুটাম==1:
                왼,위,폭,দৈর্ঘ্য_মান=উইণ্ড;오른,아래=왼+폭,위+দৈর্ঘ্য_মান
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+অন্ত_কৰক_উলম্ব-세))
                else:아래=max(위+216,min(높이,아래+অন্ত_কৰক_উলম্ব-세))
                উইণ্ড[:]=[왼,위,오른-왼,아래-위]
        প্ৰমাণিত_কৰক_আকাৰ_কৰক();assert পইণ্টাৰ_লুকাই_থকা[0]
        পুণ_আকাৰ_কৰক_টানক(4,(-100,-60),4);প্ৰমাণিত_কৰক_আকাৰ_কৰক() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            পুণ_আকাৰ_কৰক_টানক(방향,차이);প্ৰমাণিত_কৰক_আকাৰ_কৰক()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_প্ৰেৰণ_কৰক("echo '"+긴글+"'");숨고르기()
        পুণ_আকাৰ_কৰক_টানক(4,(-1000,-1000));assert উইণ্ড[2:]==[360,216]
        পুণ_আকাৰ_কৰক_টানক(4,(너비,높이))
        সঞ্চালন=SMS_প্ৰেৰণ_কৰক('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),সঞ্চালন);প্ৰমাণিত_কৰক_আকাৰ_কৰক()
        # vi가 সম্পাদনা_মান 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        শ্বেল('ftpd start')
        স্থানান্তৰণ_মান=ftplib.FTP();স্থানান্তৰণ_মান.encoding='utf-8';স্থানান্তৰণ_মান.connect('127.0.0.1',접속번호,timeout=20);স্থানান্তৰণ_মান.login()
        기다리기(b'NORMAL',SMS_প্ৰেৰণ_কৰক('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_প্ৰেৰণ_কৰক('i미저장 한글 ডাটা\n'));숨고르기()
        পুণ_আকাৰ_কৰক_টানক(4,(-너비,-높이))
        # ANSI শাৰী_মান 이동에 새 শাৰী_মান 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((উইণ্ড[3]-56)//16)).encode() in লগ_শাৰী[-4096:]
        SMS_প্ৰেৰণ_কৰক('작은 창에서도 이어 লিখা\n');숨고르기()
        পুণ_আকাৰ_কৰক_টানক(4,(너비,높이))
        SMS_প্ৰেৰণ_কৰক('큰 창에서도 이어 লিখা\n');숨고르기()
        ক্লিক_কৰক_বুটাম(0xff1b);ক্লিক_কৰক_বুটাম(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_প্ৰেৰণ_কৰক(':wq\n'))
        সামগ্ৰী_মান=bytearray();স্থানান্তৰণ_মান.retrbinary('RETR 크기자료.txt',সামগ্ৰী_মান.extend)
        assert সামগ্ৰী_মান=='미저장 한글 ডাটা\n작은 창에서도 이어 লিখা\n큰 창에서도 이어 লিখা\n'.encode(),সামগ্ৰী_মান
        প্ৰমাণিত_কৰক_আকাৰ_কৰক().save(str(পৰিমাপ_পথ/(আকাৰ_কৰক_পাঠ+'-large.png')))
        # 두 번째 창은 ডিফ_ল্ট_মান মাপ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        সঞ্চালন=len(লগ_শাৰী);ক্লিক_কৰক_মান(70,16);기다리기(b'TERMINAL FOCUS 2',সঞ্চালন)
        assert 'TERMINAL SIZE 68x19' in শ্বেল('terminal size')
        সঞ্চালন=len(লগ_শাৰী);ক্লিক_কৰক_মান(180,16);기다리기(b'TERMINAL FOCUS 1',সঞ্চালন);প্ৰমাণিত_কৰক_আকাৰ_কৰক()
        পুণ_আকাৰ_কৰক_টানক(4,(-너비,-높이));প্ৰমাণিত_কৰক_আকাৰ_কৰক().save(str(পৰিমাপ_পথ/(আকাৰ_কৰক_পাঠ+'-small.png')))
        # মাপ পৰিবৰ্তন_কৰক_মান পাছলৈ_মান X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        সঞ্চালন=len(লগ_শাৰী);ক্লিক_কৰক_মান(উইণ্ড[0]+উইণ্ড[2]-20,উইণ্ড[1]+15);기다리기(b'TERMINAL FOCUS 2',সঞ্চালন)
        assert 'RESIZE CLOSED' in শ্বেল('echo RESIZE CLOSED')
        print('PASS:',আকাৰ_কৰক_পাঠ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if স্থানান্তৰণ_মান:স্থানান্তৰণ_মান.close()
        if দূৰবৰ্তী_মান:দূৰবৰ্তী_মান.close()
        if প্ৰক্ৰিয়া_মান.poll() is None:
            প্ৰক্ৰিয়া_মান.terminate()
            try:প্ৰক্ৰিয়া_মান.wait(timeout=8)
            except subprocess.TimeoutExpired:প্ৰক্ৰিয়া_মান.kill();প্ৰক্ৰিয়া_মান.wait()
        চয়নকাৰী_a916db4e.close();প্ৰক্ৰিয়া_মান.stdout.close();(পৰিমাপ_পথ/(আকাৰ_কৰক_পাঠ+'.log')).write_bytes(লগ_শাৰী)


def সঞ্চালন():
    পৰিমাপ_পথ=기준/'build/verification/resize';পৰিমাপ_পথ.mkdir(parents=True,exist_ok=True)
    লগ_শাৰী={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,পৰিমাপ_পথ);লগ_শাৰী['resolutions'].append([너비,높이])
        লগ_শাৰী.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(পৰিমাপ_পথ/'report.json').write_text(json.dumps(লগ_শাৰী,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':সঞ্চালন()
