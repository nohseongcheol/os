#!/usr/bin/env python3
"""իրական_տվյալ QEMU/VNC에서 Տերմինալ 모서리 քաշել_արժեք·նշորդ·동적 գրանշան_արժեք փորակ_մուտքագրում·խմբագրել_արժեք Բովանդակություն_արժեք 보존를 검사한다."""
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
from սեղան_տեսք import 정확한값
from կատարել_հրաման import արձակել_արմատ


def 창크기시험(너비, 높이, չափ_ուղի):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    չափափոխել_Գրվածք = '{}x{}'.format(너비, 높이)
    Ընթացք_արժեք = subprocess.Popen(['python3', str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', չափափոխել_Գրվածք], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ընտրիչ_a916db4e = selectors.DefaultSelector(); ընտրիչ_a916db4e.register(Ընթացք_արժեք.stdout, selectors.EVENT_READ)
    մատյան_տող = bytearray(); հեռակա_արժեք = None; փոխանցել_արժեք = None; նշորդ_թաքնված=[False]

    def 기다리기(ցուցադրել_արժեք, Գործարկել=0):
        마감 = time.monotonic() + 60
        while ցուցադրել_արժեք not in մատյան_տող[Գործարկել:]:
            if time.monotonic() > 마감 or Ընթացք_արժեք.poll() is not None or b'HALTED' in մատյան_տող or b'PANIC:' in մատյան_տող:
                raise AssertionError(մատյան_տող[Գործարկել:].decode('utf-8', 'replace'))
            for միջոցառում, _ in ընտրիչ_a916db4e.select(.1):
                տվյալ = միջոցառում.fileobj.read(65536)
                if տվյալ: մատյան_տող.extend(տվյալ)
        return մատյան_տող[Գործարկել:].decode('utf-8', 'replace')

    def կտտացնել_կոճակ(նշան, 눌림=True): հեռակա_արժեք.sendall(struct.pack('>BBHI', 4, int(눌림), 0, նշան))

    def ուղարկել_SMS(Տեքստ):
        Գործարկել = len(մատյան_տող)
        for գրանշան_արժեք in Տեքստ:
            նշան = 0xff0d if գրանշան_արժեք == '\n' else ord(գրանշան_արժեք) if ord(գրանշան_արժեք) < 256 else 0x1000000 | ord(գրանշան_արժեք)
            կտտացնել_կոճակ(նշան); կտտացնել_կոճակ(նշան, False)
        return Գործարկել

    def խեցի(Տեքստ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ուղարկել_SMS(Տեքստ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Ուղղահայաց_դիրք, 눌림): հեռակա_արժեք.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ուղղահայաց_դիրք))

    def կտտացնել_արժեք(가로, Ուղղահայաց_դիրք): 가리키기(가로, Ուղղահայաց_դիրք, 1); 가리키기(가로, Ուղղահայաց_դիրք, 0)

    def կետապատկեր_նկար():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 իրական_տվյալ 너비를 쓴다.
        հեռակա_արժեք.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        նկար_արժեք_c143fe9e = Image.new('RGB', (너비, 높이)); տարածք_արժեք = 0
        while True:
            종류 = 정확한값(հեռակա_արժեք, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                տեւողություն_արժեք = struct.unpack('>I', 정확한값(հեռակա_արժեք, 7)[3:])[0]; 정확한값(հեռակա_արժեք, տեւողություն_արժեք); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(հեռակա_արժեք, 3)[1:])[0]
            for _ in range(개수):
                가로, Ուղղահայաց_դիրք, 폭, տեւողություն_արժեք, կոդավորում_արժեք = struct.unpack('>HHHHi', 정확한값(հեռակա_արժեք, 12))
                if կոդավորում_արժեք == -239:
                    assert 폭==0 and տեւողություն_արժեք==0, 'remote cursor must be hidden'
                    նշորդ_թաքնված[0]=True
                    continue
                assert կոդավորում_արժեք == 0 and 가로+폭 <= 너비 and Ուղղահայաց_դիրք+տեւողություն_արժեք <= 높이
                նկար_արժեք_c143fe9e.paste(Image.frombytes('RGB', (폭, տեւողություն_արժեք), 정확한값(հեռակա_արժեք, 폭*տեւողություն_արժեք*4), 'raw', 'BGRX'), (가로, Ուղղահայաց_դիրք))
                տարածք_արժեք += 폭*տեւողություն_արժեք
            if տարածք_արժեք:
                assert տարածք_արժեք == 너비*높이, տարածք_արժեք
                return նկար_արժեք_c143fe9e

    def կտրոն_փիքսել(կոորդինատ_արժեք, 색):
        마감 = time.monotonic()+10
        while True:
            նկար_արժեք_c143fe9e = կետապատկեր_նկար()
            if նկար_արժեք_c143fe9e.getpixel(կոորդինատ_արժեք) == 색: return նկար_արժեք_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((կոորդինատ_արժեք, նկար_արժեք_c143fe9e.getpixel(կոորդինատ_արժեք), 색))

    def վերբեռնել_Նիշքեր(Անուն, տվյալ): փոխանցել_արժեք.storbinary('STOR '+Անուն, io.BytesIO(տվյալ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+չափափոխել_Գրվածք+' RGB32').encode() in մատյան_տող
        print('BOOT:', չափափոխել_Գրվածք, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', մատյան_տող).group(1))
        հեռակա_արժեք = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(հեռակա_արժեք, 12) == b'RFB 003.008\n'; հեռակա_արժեք.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(հեռակա_արժեք, 정확한값(հեռակա_արժեք, 1)[0]); հեռակա_արժեք.sendall(b'\x01')
        assert 정확한값(հեռակա_արժեք, 4) == b'\0'*4; հեռակա_արժեք.sendall(b'\x01')
        초기 = 정확한값(հեռակա_արժեք, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(հեռակա_արժեք, struct.unpack('>I', 초기[20:])[0])
        հեռակա_արժեք.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        հեռակա_արժեք.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        կտրոն_փիքսել((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for միջոցառում,_ in ընտրիչ_a916db4e.select(.02):
                    տվյալ=միջոցառում.fileobj.read(65536)
                    if տվյալ:մատյան_տող.extend(տվյալ)
        պատուհան=[12,48,568,360]
        def հաստատել_չափափոխել():
            սյունակ_արժեք,տող_արժեք=(պատուհան[2]-24)//8,(պատուհան[3]-56)//16
            Տեքստ=խեցի('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(սյունակ_արժեք,տող_արժեք) in Տեքստ,Տեքստ
            # իրական_տվյալ պատուհան 테두리: 단지 Չափս հարցում_արժեք 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            կտրոն_փիքսել((պատուհան[0],պատուհան[1]),(32,80,144))
            նկար_արժեք_c143fe9e=կտրոն_փիքսել((պատուհան[0]+պատուհան[2]-1,պատուհան[1]+պատուհան[3]-1),(39,49,64))
            return նկար_արժեք_c143fe9e
        def 모서리(방향):
            return (պատուհան[0]+(3 if 방향 in (1,3) else պատուհան[2]-4),պատուհան[1]+(3 if 방향<=2 else պատուհան[3]-4))
        def չափափոխել_քաշել(방향,차이,կոճակ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            կտրոն_փիքսել(흰점,(255,255,255))
            가리키기(가,세,կոճակ)
            끝가=max(0,min(너비-1,가+차이[0]));վերջացնել_Ուղղահայաց=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,վերջացնել_Ուղղահայաց,կոճակ);가리키기(끝가,վերջացնել_Ուղղահայաց,0);숨고르기()
            if կոճակ==1:
                왼,위,폭,տեւողություն_արժեք=պատուհան;오른,아래=왼+폭,위+տեւողություն_արժեք
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+վերջացնել_Ուղղահայաց-세))
                else:아래=max(위+216,min(높이,아래+վերջացնել_Ուղղահայաց-세))
                պատուհան[:]=[왼,위,오른-왼,아래-위]
        հաստատել_չափափոխել();assert նշորդ_թաքնված[0]
        չափափոխել_քաշել(4,(-100,-60),4);հաստատել_չափափոխել() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            չափափոխել_քաշել(방향,차이);հաստատել_չափափոխել()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ուղարկել_SMS("echo '"+긴글+"'");숨고르기()
        չափափոխել_քաշել(4,(-1000,-1000));assert պատուհան[2:]==[360,216]
        չափափոխել_քաշել(4,(너비,높이))
        Գործարկել=ուղարկել_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Գործարկել);հաստատել_չափափոխել()
        # vi가 խմբագրել_արժեք 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        խեցի('ftpd start')
        փոխանցել_արժեք=ftplib.FTP();փոխանցել_արժեք.encoding='utf-8';փոխանցել_արժեք.connect('127.0.0.1',접속번호,timeout=20);փոխանցել_արժեք.login()
        기다리기(b'NORMAL',ուղարկել_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ուղարկել_SMS('i미저장 한글 տվյալ\n'));숨고르기()
        չափափոխել_քաշել(4,(-너비,-높이))
        # ANSI տող_արժեք 이동에 새 տող_արժեք 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((պատուհան[3]-56)//16)).encode() in մատյան_տող[-4096:]
        ուղարկել_SMS('작은 창에서도 이어 Գրել\n');숨고르기()
        չափափոխել_քաշել(4,(너비,높이))
        ուղարկել_SMS('큰 창에서도 이어 Գրել\n');숨고르기()
        կտտացնել_կոճակ(0xff1b);կտտացնել_կոճակ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ուղարկել_SMS(':wq\n'))
        Բովանդակություն_արժեք=bytearray();փոխանցել_արժեք.retrbinary('RETR 크기자료.txt',Բովանդակություն_արժեք.extend)
        assert Բովանդակություն_արժեք=='미저장 한글 տվյալ\n작은 창에서도 이어 Գրել\n큰 창에서도 이어 Գրել\n'.encode(),Բովանդակություն_արժեք
        հաստատել_չափափոխել().save(str(չափ_ուղի/(չափափոխել_Գրվածք+'-large.png')))
        # 두 번째 창은 սկզբնադիր_արժեք Չափս, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Գործարկել=len(մատյան_տող);կտտացնել_արժեք(70,16);기다리기(b'TERMINAL FOCUS 2',Գործարկել)
        assert 'TERMINAL SIZE 68x19' in խեցի('terminal size')
        Գործարկել=len(մատյան_տող);կտտացնել_արժեք(180,16);기다리기(b'TERMINAL FOCUS 1',Գործարկել);հաստատել_չափափոխել()
        չափափոխել_քաշել(4,(-너비,-높이));հաստատել_չափափոխել().save(str(չափ_ուղի/(չափափոխել_Գրվածք+'-small.png')))
        # Չափս փոխել_արժեք Հետ_արժեք X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Գործարկել=len(մատյան_տող);կտտացնել_արժեք(պատուհան[0]+պատուհան[2]-20,պատուհան[1]+15);기다리기(b'TERMINAL FOCUS 2',Գործարկել)
        assert 'RESIZE CLOSED' in խեցի('echo RESIZE CLOSED')
        print('PASS:',չափափոխել_Գրվածք,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if փոխանցել_արժեք:փոխանցել_արժեք.close()
        if հեռակա_արժեք:հեռակա_արժեք.close()
        if Ընթացք_արժեք.poll() is None:
            Ընթացք_արժեք.terminate()
            try:Ընթացք_արժեք.wait(timeout=8)
            except subprocess.TimeoutExpired:Ընթացք_արժեք.kill();Ընթացք_արժեք.wait()
        ընտրիչ_a916db4e.close();Ընթացք_արժեք.stdout.close();(չափ_ուղի/(չափափոխել_Գրվածք+'.log')).write_bytes(մատյան_տող)


def Գործարկել():
    չափ_ուղի=արձակել_արմատ/'build/verification/resize';չափ_ուղի.mkdir(parents=True,exist_ok=True)
    մատյան_տող={'passed':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,չափ_ուղի);մատյան_տող['resolutions'].append([너비,높이])
        մատյան_տող.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(չափ_ուղի/'report.json').write_text(json.dumps(մատյան_տող,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Գործարկել()
