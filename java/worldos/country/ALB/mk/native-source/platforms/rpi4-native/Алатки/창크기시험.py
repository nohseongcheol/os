#!/usr/bin/env python3
"""реален_податоци QEMU/VNC에서 Терминал 모서리 влечи_VALUE·покажувач·동적 знак_VALUE отвор_внес·уреди_VALUE Содржина_VALUE 보존를 검사한다."""
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
from десктоп_Приказ import EXACT_VALUE
from Изврши_наредба import Project_корен


def 창크기시험(너비, 높이, мерка_патека):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); број_на_порта = 임시.getsockname()[1]
    големина_СМС = '{}x{}'.format(너비, 높이)
    Процес_VALUE = subprocess.Popen(['python3', str(Project_корен/'Алатки/Изврши_наредба.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(број_на_порта), '--resolution', големина_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    избирач_a916db4e = selectors.DefaultSelector(); избирач_a916db4e.register(Процес_VALUE.stdout, selectors.EVENT_READ)
    LOG_ред = bytearray(); далечинскo_VALUE = None; пренос_VALUE = None; покажувач_скриен=[False]

    def 기다리기(прикажи_VALUE, Изврши_2=0):
        마감 = time.monotonic() + 60
        while прикажи_VALUE not in LOG_ред[Изврши_2:]:
            if time.monotonic() > 마감 or Процес_VALUE.poll() is not None or b'HALTED' in LOG_ред or b'PANIC:' in LOG_ред:
                raise AssertionError(LOG_ред[Изврши_2:].decode('utf-8', 'replace'))
            for настан, _ in избирач_a916db4e.select(.1):
                податоци = настан.fileobj.read(65536)
                if податоци: LOG_ред.extend(податоци)
        return LOG_ред[Изврши_2:].decode('utf-8', 'replace')

    def кликни_копче(симбол, 눌림=True): далечинскo_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, симбол))

    def испрати_СМС(Текст):
        Изврши_2 = len(LOG_ред)
        for знак_VALUE in Текст:
            симбол = 0xff0d if знак_VALUE == '\n' else ord(знак_VALUE) if ord(знак_VALUE) < 256 else 0x1000000 | ord(знак_VALUE)
            кликни_копче(симбол); кликни_копче(симбол, False)
        return Изврши_2

    def обвивка(Текст): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', испрати_СМС(Текст+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, вертикала_позиционирање, 눌림): далечинскo_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, вертикала_позиционирање))

    def кликни_VALUE(가로, вертикала_позиционирање): 가리키기(가로, вертикала_позиционирање, 1); 가리키기(가로, вертикала_позиционирање, 0)

    def бит_мапа_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 реален_податоци 너비를 쓴다.
        далечинскo_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        цртеж_VALUE = Image.new('RGB', (너비, 높이)); област_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(далечинскo_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                должина_VALUE = struct.unpack('>I', EXACT_VALUE(далечинскo_VALUE, 7)[3:])[0]; EXACT_VALUE(далечинскo_VALUE, должина_VALUE); continue
            assert 종류 == 0, 종류
            ставка_COUNT = struct.unpack('>H', EXACT_VALUE(далечинскo_VALUE, 3)[1:])[0]
            for _ in range(ставка_COUNT):
                가로, вертикала_позиционирање, 폭, должина_VALUE, кодирање_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(далечинскo_VALUE, 12))
                if кодирање_VALUE == -239:
                    assert 폭==0 and должина_VALUE==0, 'remote cursor must be hidden'
                    покажувач_скриен[0]=True
                    continue
                assert кодирање_VALUE == 0 and 가로+폭 <= 너비 and вертикала_позиционирање+должина_VALUE <= 높이
                цртеж_VALUE.paste(Image.frombytes('RGB', (폭, должина_VALUE), EXACT_VALUE(далечинскo_VALUE, 폭*должина_VALUE*4), 'raw', 'BGRX'), (가로, вертикала_позиционирање))
                област_VALUE_9285603e += 폭*должина_VALUE
            if област_VALUE_9285603e:
                assert област_VALUE_9285603e == 너비*높이, област_VALUE_9285603e
                return цртеж_VALUE

    def провери_пиксел(координата_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            цртеж_VALUE = бит_мапа_IMAGE()
            if цртеж_VALUE.getpixel(координата_VALUE) == 색: return цртеж_VALUE
            if time.monotonic() > 마감: raise AssertionError((координата_VALUE, цртеж_VALUE.getpixel(координата_VALUE), 색))

    def постави_Датотеки(Име, податоци): пренос_VALUE.storbinary('STOR '+Име, io.BytesIO(податоци))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+големина_СМС+' RGB32').encode() in LOG_ред
        print('BOOT:', големина_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ред).group(1))
        далечинскo_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(далечинскo_VALUE, 12) == b'RFB 003.008\n'; далечинскo_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(далечинскo_VALUE, EXACT_VALUE(далечинскo_VALUE, 1)[0]); далечинскo_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(далечинскo_VALUE, 4) == b'\0'*4; далечинскo_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(далечинскo_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(далечинскo_VALUE, struct.unpack('>I', 초기[20:])[0])
        далечинскo_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        далечинскo_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        провери_пиксел((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for настан,_ in избирач_a916db4e.select(.02):
                    податоци=настан.fileobj.read(65536)
                    if податоци:LOG_ред.extend(податоци)
        прозорец=[12,48,568,360]
        def провери_големина_c52b692c():
            COLUMN_VALUE,ROW_VALUE=(прозорец[2]-24)//8,(прозорец[3]-56)//16
            Текст=обвивка('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Текст,Текст
            # реален_податоци прозорец 테두리: 단지 Големина прашалник_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            провери_пиксел((прозорец[0],прозорец[1]),(32,80,144))
            цртеж_VALUE=провери_пиксел((прозорец[0]+прозорец[2]-1,прозорец[1]+прозорец[3]-1),(39,49,64))
            return цртеж_VALUE
        def 모서리(방향):
            return (прозорец[0]+(3 if 방향 in (1,3) else прозорец[2]-4),прозорец[1]+(3 if 방향<=2 else прозорец[3]-4))
        def промени_големина_влечи(방향,차이,копче=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            провери_пиксел(흰점,(255,255,255))
            가리키기(가,세,копче)
            끝가=max(0,min(너비-1,가+차이[0]));крај_вертикала=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,крај_вертикала,копче);가리키기(끝가,крај_вертикала,0);숨고르기()
            if копче==1:
                LEFT_VALUE,위,폭,должина_VALUE=прозорец;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+должина_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+крај_вертикала-세))
                else:아래=max(위+216,min(높이,아래+крај_вертикала-세))
                прозорец[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        провери_големина_c52b692c();assert покажувач_скриен[0]
        промени_големина_влечи(4,(-100,-60),4);провери_големина_c52b692c() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            промени_големина_влечи(방향,차이);провери_големина_c52b692c()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        испрати_СМС("echo '"+긴글+"'");숨고르기()
        промени_големина_влечи(4,(-1000,-1000));assert прозорец[2:]==[360,216]
        промени_големина_влечи(4,(너비,높이))
        Изврши_2=испрати_СМС('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Изврши_2);провери_големина_c52b692c()
        # vi가 уреди_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        обвивка('ftpd start')
        пренос_VALUE=ftplib.FTP();пренос_VALUE.encoding='utf-8';пренос_VALUE.connect('127.0.0.1',број_на_порта,timeout=20);пренос_VALUE.login()
        기다리기(b'NORMAL',испрати_СМС('vi /크기자료.txt\n'))
        기다리기(b'INSERT',испрати_СМС('i미저장 한글 податоци\n'));숨고르기()
        промени_големина_влечи(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((прозорец[3]-56)//16)).encode() in LOG_ред[-4096:]
        испрати_СМС('작은 창에서도 이어 Запиши\n');숨고르기()
        промени_големина_влечи(4,(너비,높이))
        испрати_СМС('큰 창에서도 이어 Запиши\n');숨고르기()
        кликни_копче(0xff1b);кликни_копче(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',испрати_СМС(':wq\n'))
        Содржина_VALUE=bytearray();пренос_VALUE.retrbinary('RETR 크기자료.txt',Содржина_VALUE.extend)
        assert Содржина_VALUE=='미저장 한글 податоци\n작은 창에서도 이어 Запиши\n큰 창에서도 이어 Запиши\n'.encode(),Содржина_VALUE
        провери_големина_c52b692c().save(str(мерка_патека/(големина_СМС+'-large.png')))
        # 두 번째 창은 стандардна_вредност Големина, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Изврши_2=len(LOG_ред);кликни_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Изврши_2)
        assert 'TERMINAL SIZE 68x19' in обвивка('terminal size')
        Изврши_2=len(LOG_ред);кликни_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Изврши_2);провери_големина_c52b692c()
        промени_големина_влечи(4,(-너비,-높이));провери_големина_c52b692c().save(str(мерка_патека/(големина_СМС+'-small.png')))
        # Големина измени_VALUE Назад_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Изврши_2=len(LOG_ред);кликни_VALUE(прозорец[0]+прозорец[2]-20,прозорец[1]+15);기다리기(b'TERMINAL FOCUS 2',Изврши_2)
        assert 'RESIZE CLOSED' in обвивка('echo RESIZE CLOSED')
        print('PASS:',големина_СМС,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if пренос_VALUE:пренос_VALUE.close()
        if далечинскo_VALUE:далечинскo_VALUE.close()
        if Процес_VALUE.poll() is None:
            Процес_VALUE.terminate()
            try:Процес_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Процес_VALUE.kill();Процес_VALUE.wait()
        избирач_a916db4e.close();Процес_VALUE.stdout.close();(мерка_патека/(големина_СМС+'.log')).write_bytes(LOG_ред)


def Изврши_2():
    мерка_патека=Project_корен/'build/verification/resize';мерка_патека.mkdir(parents=True,exist_ok=True)
    LOG_ред={'passed':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,мерка_патека);LOG_ред['resolutions'].append([너비,높이])
        LOG_ред.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(мерка_патека/'report.json').write_text(json.dumps(LOG_ред,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Изврши_2()
