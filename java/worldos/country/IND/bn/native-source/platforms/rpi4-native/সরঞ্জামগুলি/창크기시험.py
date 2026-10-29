#!/usr/bin/env python3
"""প্রকৃত_ডাটা QEMU/VNC에서 আদেশ_ব্যাখ্যাকারী 모서리 টানুন_মান·নির্দেশক·동적 অক্ষর_মান স্লট_ভুক্তি·সম্পাদন_মান সামগ্রি_মান 보존를 검사한다."""
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
from ডেস্কটপ_ভিউ import 정확한값
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def 창크기시험(너비, 높이, পরিমাপ_পথ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); পোর্ট_নম্বর = 임시.getsockname()[1]
    আয়তন_পাঠ = '{}x{}'.format(너비, 높이)
    প্রসেসর_মান = subprocess.Popen(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(পোর্ট_নম্বর), '--resolution', আয়তন_পাঠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    নির্বাচক_a916db4e = selectors.DefaultSelector(); নির্বাচক_a916db4e.register(প্রসেসর_মান.stdout, selectors.EVENT_READ)
    লগ_সারি = bytearray(); দূরবর্তী_মান = None; স্থানান্তর_মান = None; নির্দেশক_লুকায়িত=[False]

    def 기다리기(শো_মান, চালনা=0):
        마감 = time.monotonic() + 60
        while শো_মান not in লগ_সারি[চালনা:]:
            if time.monotonic() > 마감 or প্রসেসর_মান.poll() is not None or b'HALTED' in লগ_সারি or b'PANIC:' in লগ_সারি:
                raise AssertionError(লগ_সারি[চালনা:].decode('utf-8', 'replace'))
            for ঘটনা, _ in নির্বাচক_a916db4e.select(.1):
                ডাটা = ঘটনা.fileobj.read(65536)
                if ডাটা: লগ_সারি.extend(ডাটা)
        return লগ_সারি[চালনা:].decode('utf-8', 'replace')

    def ক্লিক_করা_বোতাম(প্রতীক, 눌림=True): দূরবর্তী_মান.sendall(struct.pack('>BBHI', 4, int(눌림), 0, প্রতীক))

    def SMS_পাঠান(পাঠ):
        চালনা = len(লগ_সারি)
        for অক্ষর_মান in পাঠ:
            প্রতীক = 0xff0d if অক্ষর_মান == '\n' else ord(অক্ষর_মান) if ord(অক্ষর_মান) < 256 else 0x1000000 | ord(অক্ষর_মান)
            ক্লিক_করা_বোতাম(প্রতীক); ক্লিক_করা_বোতাম(প্রতীক, False)
        return চালনা

    def শেল(পাঠ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_পাঠান(পাঠ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, উল্লম্ব_পদ, 눌림): দূরবর্তী_মান.sendall(struct.pack('>BBHH', 5, 눌림, 가로, উল্লম্ব_পদ))

    def ক্লিক_করা_মান(가로, উল্লম্ব_পদ): 가리키기(가로, উল্লম্ব_পদ, 1); 가리키기(가로, উল্লম্ব_পদ, 0)

    def বিটম্যাপ_ছবি():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 প্রকৃত_ডাটা 너비를 쓴다.
        দূরবর্তী_মান.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        অঙ্কন_মান = Image.new('RGB', (너비, 높이)); এলাকা_মান = 0
        while True:
            종류 = 정확한값(দূরবর্তী_মান, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                দৈর্ঘ্য_মান = struct.unpack('>I', 정확한값(দূরবর্তী_মান, 7)[3:])[0]; 정확한값(দূরবর্তী_মান, দৈর্ঘ্য_মান); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(দূরবর্তী_মান, 3)[1:])[0]
            for _ in range(개수):
                가로, উল্লম্ব_পদ, 폭, দৈর্ঘ্য_মান, এনকোড_করা_মান = struct.unpack('>HHHHi', 정확한값(দূরবর্তী_মান, 12))
                if এনকোড_করা_মান == -239:
                    assert 폭==0 and দৈর্ঘ্য_মান==0, 'remote cursor must be hidden'
                    নির্দেশক_লুকায়িত[0]=True
                    continue
                assert এনকোড_করা_মান == 0 and 가로+폭 <= 너비 and উল্লম্ব_পদ+দৈর্ঘ্য_মান <= 높이
                অঙ্কন_মান.paste(Image.frombytes('RGB', (폭, দৈর্ঘ্য_মান), 정확한값(দূরবর্তী_মান, 폭*দৈর্ঘ্য_মান*4), 'raw', 'BGRX'), (가로, উল্লম্ব_পদ))
                এলাকা_মান += 폭*দৈর্ঘ্য_মান
            if এলাকা_মান:
                assert এলাকা_মান == 너비*높이, এলাকা_মান
                return অঙ্কন_মান

    def চেক_পেল্(অক্ষবিন্দু_মান, 색):
        마감 = time.monotonic()+10
        while True:
            অঙ্কন_মান = বিটম্যাপ_ছবি()
            if অঙ্কন_মান.getpixel(অক্ষবিন্দু_মান) == 색: return অঙ্কন_মান
            if time.monotonic() > 마감: raise AssertionError((অক্ষবিন্দু_মান, অঙ্কন_মান.getpixel(অক্ষবিন্দু_মান), 색))

    def আপলোড_ফাইলগুলি(নাম, ডাটা): স্থানান্তর_মান.storbinary('STOR '+নাম, io.BytesIO(ডাটা))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+আয়তন_পাঠ+' RGB32').encode() in লগ_সারি
        print('BOOT:', আয়তন_পাঠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', লগ_সারি).group(1))
        দূরবর্তী_মান = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(দূরবর্তী_মান, 12) == b'RFB 003.008\n'; দূরবর্তী_মান.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(দূরবর্তী_মান, 정확한값(দূরবর্তী_মান, 1)[0]); দূরবর্তী_মান.sendall(b'\x01')
        assert 정확한값(দূরবর্তী_মান, 4) == b'\0'*4; দূরবর্তী_মান.sendall(b'\x01')
        초기 = 정확한값(দূরবর্তী_মান, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(দূরবর্তী_মান, struct.unpack('>I', 초기[20:])[0])
        দূরবর্তী_মান.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        দূরবর্তী_মান.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        চেক_পেল্((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ঘটনা,_ in নির্বাচক_a916db4e.select(.02):
                    ডাটা=ঘটনা.fileobj.read(65536)
                    if ডাটা:লগ_সারি.extend(ডাটা)
        উইন্ডো=[12,48,568,360]
        def যাচাই_করা_আয়তন():
            কলাম_মান,সারি_মান=(উইন্ডো[2]-24)//8,(উইন্ডো[3]-56)//16
            পাঠ=শেল('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(কলাম_মান,সারি_মান) in পাঠ,পাঠ
            # প্রকৃত_ডাটা উইন্ডো 테두리: 단지 আকার জিজ্ঞাসা_মান 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            চেক_পেল্((উইন্ডো[0],উইন্ডো[1]),(32,80,144))
            অঙ্কন_মান=চেক_পেল্((উইন্ডো[0]+উইন্ডো[2]-1,উইন্ডো[1]+উইন্ডো[3]-1),(39,49,64))
            return অঙ্কন_মান
        def 모서리(방향):
            return (উইন্ডো[0]+(3 if 방향 in (1,3) else উইন্ডো[2]-4),উইন্ডো[1]+(3 if 방향<=2 else উইন্ডো[3]-4))
        def রিসাইজ_টানুন(방향,차이,বোতাম=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            চেক_পেল্(흰점,(255,255,255))
            가리키기(가,세,বোতাম)
            끝가=max(0,min(너비-1,가+차이[0]));শেষ_করা_উল্লম্ব=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,শেষ_করা_উল্লম্ব,বোতাম);가리키기(끝가,শেষ_করা_উল্লম্ব,0);숨고르기()
            if বোতাম==1:
                왼,위,폭,দৈর্ঘ্য_মান=উইন্ডো;오른,아래=왼+폭,위+দৈর্ঘ্য_মান
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+শেষ_করা_উল্লম্ব-세))
                else:아래=max(위+216,min(높이,아래+শেষ_করা_উল্লম্ব-세))
                উইন্ডো[:]=[왼,위,오른-왼,아래-위]
        যাচাই_করা_আয়তন();assert নির্দেশক_লুকায়িত[0]
        রিসাইজ_টানুন(4,(-100,-60),4);যাচাই_করা_আয়তন() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            রিসাইজ_টানুন(방향,차이);যাচাই_করা_আয়তন()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_পাঠান("echo '"+긴글+"'");숨고르기()
        রিসাইজ_টানুন(4,(-1000,-1000));assert উইন্ডো[2:]==[360,216]
        রিসাইজ_টানুন(4,(너비,높이))
        চালনা=SMS_পাঠান('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),চালনা);যাচাই_করা_আয়তন()
        # vi가 সম্পাদন_মান 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        শেল('ftpd start')
        স্থানান্তর_মান=ftplib.FTP();স্থানান্তর_মান.encoding='utf-8';স্থানান্তর_মান.connect('127.0.0.1',পোর্ট_নম্বর,timeout=20);স্থানান্তর_মান.login()
        기다리기(b'NORMAL',SMS_পাঠান('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_পাঠান('i미저장 한글 ডাটা\n'));숨고르기()
        রিসাইজ_টানুন(4,(-너비,-높이))
        # ANSI সারি_মান 이동에 새 সারি_মান 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((উইন্ডো[3]-56)//16)).encode() in লগ_সারি[-4096:]
        SMS_পাঠান('작은 창에서도 이어 লেখা\n');숨고르기()
        রিসাইজ_টানুন(4,(너비,높이))
        SMS_পাঠান('큰 창에서도 이어 লেখা\n');숨고르기()
        ক্লিক_করা_বোতাম(0xff1b);ক্লিক_করা_বোতাম(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_পাঠান(':wq\n'))
        সামগ্রি_মান=bytearray();স্থানান্তর_মান.retrbinary('RETR 크기자료.txt',সামগ্রি_মান.extend)
        assert সামগ্রি_মান=='미저장 한글 ডাটা\n작은 창에서도 이어 লেখা\n큰 창에서도 이어 লেখা\n'.encode(),সামগ্রি_মান
        যাচাই_করা_আয়তন().save(str(পরিমাপ_পথ/(আয়তন_পাঠ+'-large.png')))
        # 두 번째 창은 অমনোনীত_মান আকার, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        চালনা=len(লগ_সারি);ক্লিক_করা_মান(70,16);기다리기(b'TERMINAL FOCUS 2',চালনা)
        assert 'TERMINAL SIZE 68x19' in শেল('terminal size')
        চালনা=len(লগ_সারি);ক্লিক_করা_মান(180,16);기다리기(b'TERMINAL FOCUS 1',চালনা);যাচাই_করা_আয়তন()
        রিসাইজ_টানুন(4,(-너비,-높이));যাচাই_করা_আয়তন().save(str(পরিমাপ_পথ/(আয়তন_পাঠ+'-small.png')))
        # আকার পরিবর্তন_করা_মান ফিরে_যান_মান X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        চালনা=len(লগ_সারি);ক্লিক_করা_মান(উইন্ডো[0]+উইন্ডো[2]-20,উইন্ডো[1]+15);기다리기(b'TERMINAL FOCUS 2',চালনা)
        assert 'RESIZE CLOSED' in শেল('echo RESIZE CLOSED')
        print('PASS:',আয়তন_পাঠ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if স্থানান্তর_মান:স্থানান্তর_মান.close()
        if দূরবর্তী_মান:দূরবর্তী_মান.close()
        if প্রসেসর_মান.poll() is None:
            প্রসেসর_মান.terminate()
            try:প্রসেসর_মান.wait(timeout=8)
            except subprocess.TimeoutExpired:প্রসেসর_মান.kill();প্রসেসর_মান.wait()
        নির্বাচক_a916db4e.close();প্রসেসর_মান.stdout.close();(পরিমাপ_পথ/(আয়তন_পাঠ+'.log')).write_bytes(লগ_সারি)


def চালনা():
    পরিমাপ_পথ=প্রকল্প_মূল/'build/verification/resize';পরিমাপ_পথ.mkdir(parents=True,exist_ok=True)
    লগ_সারি={'passed':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,পরিমাপ_পথ);লগ_সারি['resolutions'].append([너비,높이])
        লগ_সারি.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(পরিমাপ_পথ/'report.json').write_text(json.dumps(লগ_সারি,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':চালনা()
