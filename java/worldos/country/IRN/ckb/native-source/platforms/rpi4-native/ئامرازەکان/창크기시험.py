#!/usr/bin/env python3
"""ڕاستەکی_دەیتا QEMU/VNC에서 터미널 모서리 ڕاکێشان_نرخ·نیشاندەر·동적 نووسە_نرخ کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین·بژار_نرخ ناوەرۆک_نرخ 보존를 검사한다."""
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
from دێسکتۆپ_دیمەن import 정확한값
from جێبەجێکردن_فەرمان import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    گۆڕینی_ئەندازە_دەق = '{}x{}'.format(너비, 높이)
    پرۆسە_نرخ = subprocess.Popen(['python3', str(기준/'ئامرازەکان/جێبەجێکردن_فەرمان.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', گۆڕینی_ئەندازە_دەق], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    هەڵبژێرەر_a916db4e = selectors.DefaultSelector(); هەڵبژێرەر_a916db4e.register(پرۆسە_نرخ.stdout, selectors.EVENT_READ)
    تۆمار_ڕزن = bytearray(); دوورەدەس_نرخ = None; گواستنەوە_نرخ_630ba093 = None; نیشاندەر_شاراوە=[False]

    def 기다리기(نیشاندان_نرخ, ڕادان=0):
        마감 = time.monotonic() + 60
        while نیشاندان_نرخ not in تۆمار_ڕزن[ڕادان:]:
            if time.monotonic() > 마감 or پرۆسە_نرخ.poll() is not None or b'HALTED' in تۆمار_ڕزن or b'PANIC:' in تۆمار_ڕزن:
                raise AssertionError(تۆمار_ڕزن[ڕادان:].decode('utf-8', 'replace'))
            for پێشهات, _ in هەڵبژێرەر_a916db4e.select(.1):
                دەیتا = پێشهات.fileobj.read(65536)
                if دەیتا: تۆمار_ڕزن.extend(دەیتا)
        return تۆمار_ڕزن[ڕادان:].decode('utf-8', 'replace')

    def کرته_کردن_دوگمه(سیمبۆل, 눌림=True): دوورەدەس_نرخ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, سیمبۆل))

    def تێکست_بنێرە(دەق):
        ڕادان = len(تۆمار_ڕزن)
        for نووسە_نرخ in دەق:
            سیمبۆل = 0xff0d if نووسە_نرخ == '\n' else ord(نووسە_نرخ) if ord(نووسە_نرخ) < 256 else 0x1000000 | ord(نووسە_نرخ)
            کرته_کردن_دوگمه(سیمبۆل); کرته_کردن_دوگمه(سیمبۆل, False)
        return ڕادان

    def توێکڵ(دەق): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', تێکست_بنێرە(دەق+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): دوورەدەس_نرخ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def کرته_کردن_نرخ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def بیتمەپ_وێنە():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ڕاستەکی_دەیتا 너비를 쓴다.
        دوورەدەس_نرخ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        نگار_نرخ = Image.new('RGB', (너비, 높이)); شوێن_نرخ = 0
        while True:
            종류 = 정확한값(دوورەدەس_نرخ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                درێژی_نرخ = struct.unpack('>I', 정확한값(دوورەدەس_نرخ, 7)[3:])[0]; 정확한값(دوورەدەس_نرخ, درێژی_نرخ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(دوورەدەس_نرخ, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, درێژی_نرخ, نهێنبەندی_نرخ = struct.unpack('>HHHHi', 정확한값(دوورەدەس_نرخ, 12))
                if نهێنبەندی_نرخ == -239:
                    assert 폭==0 and درێژی_نرخ==0, 'remote cursor must be hidden'
                    نیشاندەر_شاراوە[0]=True
                    continue
                assert نهێنبەندی_نرخ == 0 and 가로+폭 <= 너비 and 세로+درێژی_نرخ <= 높이
                نگار_نرخ.paste(Image.frombytes('RGB', (폭, درێژی_نرخ), 정확한값(دوورەدەس_نرخ, 폭*درێژی_نرخ*4), 'raw', 'BGRX'), (가로, 세로))
                شوێن_نرخ += 폭*درێژی_نرخ
            if شوێن_نرخ:
                assert شوێن_نرخ == 너비*높이, شوێن_نرخ
                return نگار_نرخ

    def پشکنین_پێڵ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            نگار_نرخ = بیتمەپ_وێنە()
            if نگار_نرخ.getpixel(좌표) == 색: return نگار_نرخ
            if time.monotonic() > 마감: raise AssertionError((좌표, نگار_نرخ.getpixel(좌표), 색))

    def بار_کردن_فایله_کان(ناو, دەیتا): گواستنەوە_نرخ_630ba093.storbinary('STOR '+ناو, io.BytesIO(دەیتا))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+گۆڕینی_ئەندازە_دەق+' RGB32').encode() in تۆمار_ڕزن
        print('BOOT:', گۆڕینی_ئەندازە_دەق, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', تۆمار_ڕزن).group(1))
        دوورەدەس_نرخ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(دوورەدەس_نرخ, 12) == b'RFB 003.008\n'; دوورەدەس_نرخ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(دوورەدەس_نرخ, 정확한값(دوورەدەس_نرخ, 1)[0]); دوورەدەس_نرخ.sendall(b'\x01')
        assert 정확한값(دوورەدەس_نرخ, 4) == b'\0'*4; دوورەدەس_نرخ.sendall(b'\x01')
        초기 = 정확한값(دوورەدەس_نرخ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(دوورەدەس_نرخ, struct.unpack('>I', 초기[20:])[0])
        دوورەدەس_نرخ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        دوورەدەس_نرخ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        پشکنین_پێڵ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for پێشهات,_ in هەڵبژێرەر_a916db4e.select(.02):
                    دەیتا=پێشهات.fileobj.read(65536)
                    if دەیتا:تۆمار_ڕزن.extend(دەیتا)
        پەنجەرە=[12,48,568,360]
        def سەلماندن_گۆڕینی_ئەندازە():
            ستوون_نرخ,ڕزن_نرخ=(پەنجەرە[2]-24)//8,(پەنجەرە[3]-56)//16
            دەق=توێکڵ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ستوون_نرخ,ڕزن_نرخ) in دەق,دەق
            # ڕاستەکی_دەیتا پەنجەرە 테두리: 단지 گۆڕینی_ئەندازە پرس_نرخ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            پشکنین_پێڵ((پەنجەرە[0],پەنجەرە[1]),(32,80,144))
            نگار_نرخ=پشکنین_پێڵ((پەنجەرە[0]+پەنجەرە[2]-1,پەنجەرە[1]+پەنجەرە[3]-1),(39,49,64))
            return نگار_نرخ
        def 모서리(방향):
            return (پەنجەرە[0]+(3 if 방향 in (1,3) else پەنجەرە[2]-4),پەنجەرە[1]+(3 if 방향<=2 else پەنجەرە[3]-4))
        def گۆڕینی_ئەندازە_ڕاکێشان(방향,차이,دوگمه=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            پشکنین_پێڵ(흰점,(255,255,255))
            가리키기(가,세,دوگمه)
            끝가=max(0,min(너비-1,가+차이[0]));دوایی_کردن_ئاسۆیی=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,دوایی_کردن_ئاسۆیی,دوگمه);가리키기(끝가,دوایی_کردن_ئاسۆیی,0);숨고르기()
            if دوگمه==1:
                왼,위,폭,درێژی_نرخ=پەنجەرە;오른,아래=왼+폭,위+درێژی_نرخ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+دوایی_کردن_ئاسۆیی-세))
                else:아래=max(위+216,min(높이,아래+دوایی_کردن_ئاسۆیی-세))
                پەنجەرە[:]=[왼,위,오른-왼,아래-위]
        سەلماندن_گۆڕینی_ئەندازە();assert نیشاندەر_شاراوە[0]
        گۆڕینی_ئەندازە_ڕاکێشان(4,(-100,-60),4);سەلماندن_گۆڕینی_ئەندازە() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            گۆڕینی_ئەندازە_ڕاکێشان(방향,차이);سەلماندن_گۆڕینی_ئەندازە()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        تێکست_بنێرە("echo '"+긴글+"'");숨고르기()
        گۆڕینی_ئەندازە_ڕاکێشان(4,(-1000,-1000));assert پەنجەرە[2:]==[360,216]
        گۆڕینی_ئەندازە_ڕاکێشان(4,(너비,높이))
        ڕادان=تێکست_بنێرە('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ڕادان);سەلماندن_گۆڕینی_ئەندازە()
        # vi가 بژار_نرخ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        توێکڵ('ftpd start')
        گواستنەوە_نرخ_630ba093=ftplib.FTP();گواستنەوە_نرخ_630ba093.encoding='utf-8';گواستنەوە_نرخ_630ba093.connect('127.0.0.1',접속번호,timeout=20);گواستنەوە_نرخ_630ba093.login()
        기다리기(b'NORMAL',تێکست_بنێرە('vi /크기자료.txt\n'))
        기다리기(b'INSERT',تێکست_بنێرە('i미저장 한글 دەیتا\n'));숨고르기()
        گۆڕینی_ئەندازە_ڕاکێشان(4,(-너비,-높이))
        # ANSI ڕزن_نرخ 이동에 새 ڕزن_نرخ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((پەنجەرە[3]-56)//16)).encode() in تۆمار_ڕزن[-4096:]
        تێکست_بنێرە('작은 창에서도 이어 ڕایت_کردن\n');숨고르기()
        گۆڕینی_ئەندازە_ڕاکێشان(4,(너비,높이))
        تێکست_بنێرە('큰 창에서도 이어 ڕایت_کردن\n');숨고르기()
        کرته_کردن_دوگمه(0xff1b);کرته_کردن_دوگمه(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',تێکست_بنێرە(':wq\n'))
        ناوەرۆک_نرخ=bytearray();گواستنەوە_نرخ_630ba093.retrbinary('RETR 크기자료.txt',ناوەرۆک_نرخ.extend)
        assert ناوەرۆک_نرخ=='미저장 한글 دەیتا\n작은 창에서도 이어 ڕایت_کردن\n큰 창에서도 이어 ڕایت_کردن\n'.encode(),ناوەرۆک_نرخ
        سەلماندن_گۆڕینی_ئەندازە().save(str(결과경로/(گۆڕینی_ئەندازە_دەق+'-large.png')))
        # 두 번째 창은 بەهای_گریمانە گۆڕینی_ئەندازە, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ڕادان=len(تۆمار_ڕزن);کرته_کردن_نرخ(70,16);기다리기(b'TERMINAL FOCUS 2',ڕادان)
        assert 'TERMINAL SIZE 68x19' in توێکڵ('terminal size')
        ڕادان=len(تۆمار_ڕزن);کرته_کردن_نرخ(180,16);기다리기(b'TERMINAL FOCUS 1',ڕادان);سەلماندن_گۆڕینی_ئەندازە()
        گۆڕینی_ئەندازە_ڕاکێشان(4,(-너비,-높이));سەلماندن_گۆڕینی_ئەندازە().save(str(결과경로/(گۆڕینی_ئەندازە_دەق+'-small.png')))
        # گۆڕینی_ئەندازە گۆڕین_نرخ دواوە_نرخ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ڕادان=len(تۆمار_ڕزن);کرته_کردن_نرخ(پەنجەرە[0]+پەنجەرە[2]-20,پەنجەرە[1]+15);기다리기(b'TERMINAL FOCUS 2',ڕادان)
        assert 'RESIZE CLOSED' in توێکڵ('echo RESIZE CLOSED')
        print('PASS:',گۆڕینی_ئەندازە_دەق,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if گواستنەوە_نرخ_630ba093:گواستنەوە_نرخ_630ba093.close()
        if دوورەدەس_نرخ:دوورەدەس_نرخ.close()
        if پرۆسە_نرخ.poll() is None:
            پرۆسە_نرخ.terminate()
            try:پرۆسە_نرخ.wait(timeout=8)
            except subprocess.TimeoutExpired:پرۆسە_نرخ.kill();پرۆسە_نرخ.wait()
        هەڵبژێرەر_a916db4e.close();پرۆسە_نرخ.stdout.close();(결과경로/(گۆڕینی_ئەندازە_دەق+'.log')).write_bytes(تۆمار_ڕزن)


def ڕادان():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    تۆمار_ڕزن={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);تۆمار_ڕزن['resolutions'].append([너비,높이])
        تۆمار_ڕزن.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(تۆمار_ڕزن,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ڕادان()
