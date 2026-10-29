#!/usr/bin/env python3
"""real_date QEMU/VNC에서 Terminal 모서리 glisa_VALUE·cursor·동적 caracter_VALUE 칸·edita_VALUE Conținut_VALUE 보존를 검사한다."""
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
from desktop_vizualiza import EXACT_VALUE
from executa_comandă import Project_rădăcină


def 창크기시험(너비, 높이, KR_cale):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); număr_port = 임시.getsockname()[1]
    dimensiona_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(Project_rădăcină/'Instrumente/executa_comandă.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(număr_port), '--resolution', dimensiona_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector_a916db4e = selectors.DefaultSelector(); selector_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); la_distanță_VALUE = None; Transfer_VALUE = None; cursor_Ascunsă=[False]

    def 기다리기(afișa_VALUE, Pornește=0):
        dată_limită_VALUE = time.monotonic() + 60
        while afișa_VALUE not in LOG_RECORD[Pornește:]:
            if time.monotonic() > dată_limită_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Pornește:].decode('utf-8', 'replace'))
            for Eveniment, _ in selector_a916db4e.select(.1):
                date = Eveniment.fileobj.read(65536)
                if date: LOG_RECORD.extend(date)
        return LOG_RECORD[Pornește:].decode('utf-8', 'replace')

    def clic_buton(simbol, 눌림=True): la_distanță_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def trimitere_SMS(SMS):
        Pornește = len(LOG_RECORD)
        for caracter_VALUE in SMS:
            simbol = 0xff0d if caracter_VALUE == '\n' else ord(caracter_VALUE) if ord(caracter_VALUE) < 256 else 0x1000000 | ord(caracter_VALUE)
            clic_buton(simbol); clic_buton(simbol, False)
        return Pornește

    def shell(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', trimitere_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Verticală_poziție, 눌림): la_distanță_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Verticală_poziție))

    def clic_VALUE(가로, Verticală_poziție): 가리키기(가로, Verticală_poziție, 1); 가리키기(가로, Verticală_poziție, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_date 너비를 쓴다.
        la_distanță_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        desen_VALUE = Image.new('RGB', (너비, 높이)); zonă_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(la_distanță_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lungime_VALUE = struct.unpack('>I', EXACT_VALUE(la_distanță_VALUE, 7)[3:])[0]; EXACT_VALUE(la_distanță_VALUE, lungime_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(la_distanță_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Verticală_poziție, 폭, lungime_VALUE, codificare_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(la_distanță_VALUE, 12))
                if codificare_VALUE == -239:
                    assert 폭==0 and lungime_VALUE==0, 'remote cursor must be hidden'
                    cursor_Ascunsă[0]=True
                    continue
                assert codificare_VALUE == 0 and 가로+폭 <= 너비 and Verticală_poziție+lungime_VALUE <= 높이
                desen_VALUE.paste(Image.frombytes('RGB', (폭, lungime_VALUE), EXACT_VALUE(la_distanță_VALUE, 폭*lungime_VALUE*4), 'raw', 'BGRX'), (가로, Verticală_poziție))
                zonă_VALUE_9285603e += 폭*lungime_VALUE
            if zonă_VALUE_9285603e:
                assert zonă_VALUE_9285603e == 너비*높이, zonă_VALUE_9285603e
                return desen_VALUE

    def verifica_element_imagine(좌표, 색):
        dată_limită_VALUE = time.monotonic()+10
        while True:
            desen_VALUE = bitmap_IMAGE()
            if desen_VALUE.getpixel(좌표) == 색: return desen_VALUE
            if time.monotonic() > dată_limită_VALUE: raise AssertionError((좌표, desen_VALUE.getpixel(좌표), 색))

    def Upload_Fișiere(Nume, date): Transfer_VALUE.storbinary('STOR '+Nume, io.BytesIO(date))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+dimensiona_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', dimensiona_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        la_distanță_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(la_distanță_VALUE, 12) == b'RFB 003.008\n'; la_distanță_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(la_distanță_VALUE, EXACT_VALUE(la_distanță_VALUE, 1)[0]); la_distanță_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(la_distanță_VALUE, 4) == b'\0'*4; la_distanță_VALUE.sendall(b'\x01')
        stare_inițială = EXACT_VALUE(la_distanță_VALUE, 24); assert struct.unpack('>HH', stare_inițială[:4]) == (너비, 높이)
        EXACT_VALUE(la_distanță_VALUE, struct.unpack('>I', stare_inițială[20:])[0])
        la_distanță_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        la_distanță_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        verifica_element_imagine((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Eveniment,_ in selector_a916db4e.select(.02):
                    date=Eveniment.fileobj.read(65536)
                    if date:LOG_RECORD.extend(date)
        Fereastră=[12,48,568,360]
        def verifica_dimensiona_c52b692c():
            COLUMN_VALUE,ROW_VALUE=(Fereastră[2]-24)//8,(Fereastră[3]-56)//16
            SMS=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in SMS,SMS
            # real_date Fereastră 테두리: 단지 Mărime interoga_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            verifica_element_imagine((Fereastră[0],Fereastră[1]),(32,80,144))
            desen_VALUE=verifica_element_imagine((Fereastră[0]+Fereastră[2]-1,Fereastră[1]+Fereastră[3]-1),(39,49,64))
            return desen_VALUE
        def 모서리(방향):
            return (Fereastră[0]+(3 if 방향 in (1,3) else Fereastră[2]-4),Fereastră[1]+(3 if 방향<=2 else Fereastră[3]-4))
        def redimensiona_glisa(방향,차이,buton=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            verifica_element_imagine(흰점,(255,255,255))
            가리키기(가,세,buton)
            끝가=max(0,min(너비-1,가+차이[0]));termina_un_apel_Verticală=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,termina_un_apel_Verticală,buton);가리키기(끝가,termina_un_apel_Verticală,0);숨고르기()
            if buton==1:
                LEFT_VALUE,위,폭,lungime_VALUE=Fereastră;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+lungime_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+termina_un_apel_Verticală-세))
                else:아래=max(위+216,min(높이,아래+termina_un_apel_Verticală-세))
                Fereastră[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verifica_dimensiona_c52b692c();assert cursor_Ascunsă[0]
        redimensiona_glisa(4,(-100,-60),4);verifica_dimensiona_c52b692c() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            redimensiona_glisa(방향,차이);verifica_dimensiona_c52b692c()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        trimitere_SMS("echo '"+긴글+"'");숨고르기()
        redimensiona_glisa(4,(-1000,-1000));assert Fereastră[2:]==[360,216]
        redimensiona_glisa(4,(너비,높이))
        Pornește=trimitere_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Pornește);verifica_dimensiona_c52b692c()
        # vi가 edita_VALUE 중에 화면 크기를 reîncerca_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        Transfer_VALUE=ftplib.FTP();Transfer_VALUE.encoding='utf-8';Transfer_VALUE.connect('127.0.0.1',număr_port,timeout=20);Transfer_VALUE.login()
        기다리기(b'NORMAL',trimitere_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',trimitere_SMS('i미저장 한글 date\n'));숨고르기()
        redimensiona_glisa(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Fereastră[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        trimitere_SMS('작은 창에서도 이어 Scriere\n');숨고르기()
        redimensiona_glisa(4,(너비,높이))
        trimitere_SMS('큰 창에서도 이어 Scriere\n');숨고르기()
        clic_buton(0xff1b);clic_buton(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',trimitere_SMS(':wq\n'))
        Conținut_VALUE=bytearray();Transfer_VALUE.retrbinary('RETR 크기자료.txt',Conținut_VALUE.extend)
        assert Conținut_VALUE=='미저장 한글 date\n작은 창에서도 이어 Scriere\n큰 창에서도 이어 Scriere\n'.encode(),Conținut_VALUE
        verifica_dimensiona_c52b692c().save(str(KR_cale/(dimensiona_SMS+'-large.png')))
        # 두 번째 창은 valoare_implicită Mărime, reîncerca_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Pornește=len(LOG_RECORD);clic_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Pornește)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        Pornește=len(LOG_RECORD);clic_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Pornește);verifica_dimensiona_c52b692c()
        redimensiona_glisa(4,(-너비,-높이));verifica_dimensiona_c52b692c().save(str(KR_cale/(dimensiona_SMS+'-small.png')))
        # Mărime schimba_VALUE ÎNAPOI_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Pornește=len(LOG_RECORD);clic_VALUE(Fereastră[0]+Fereastră[2]-20,Fereastră[1]+15);기다리기(b'TERMINAL FOCUS 2',Pornește)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',dimensiona_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Transfer_VALUE:Transfer_VALUE.close()
        if la_distanță_VALUE:la_distanță_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        selector_a916db4e.close();Proces_VALUE.stdout.close();(KR_cale/(dimensiona_SMS+'.log')).write_bytes(LOG_RECORD)


def Pornește():
    KR_cale=Project_rădăcină/'build/verification/resize';KR_cale.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_cale);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_cale/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Pornește()
