#!/usr/bin/env python3
"""aktuell_Daten QEMU/VNC에서 Terminal 모서리 eriwwerzéien_VALUE·Uweiser·동적 Zeechen_VALUE Slot_Agab·Editéieren_VALUE Inhalt_VALUE 보존를 검사한다."""
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
from Desktop_Vue import EXACT_VALUE
from ausféieren_Befeel import projezéieren_Racinn


def 창크기시험(너비, 높이, Mooss_Wee):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    d_Gréisst_veränneren_SMS = '{}x{}'.format(너비, 높이)
    Prozess_VALUE = subprocess.Popen(['python3', str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', d_Gréisst_veränneren_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selekteur_a916db4e = selectors.DefaultSelector(); Selekteur_a916db4e.register(Prozess_VALUE.stdout, selectors.EVENT_READ)
    LOG_Rei = bytearray(); extern_VALUE = None; Transfer_VALUE = None; Uweiser_verstoppt=[False]

    def 기다리기(Show_VALUE, Laf=0):
        마감 = time.monotonic() + 60
        while Show_VALUE not in LOG_Rei[Laf:]:
            if time.monotonic() > 마감 or Prozess_VALUE.poll() is not None or b'HALTED' in LOG_Rei or b'PANIC:' in LOG_Rei:
                raise AssertionError(LOG_Rei[Laf:].decode('utf-8', 'replace'))
            for Evenement, _ in Selekteur_a916db4e.select(.1):
                Daten = Evenement.fileobj.read(65536)
                if Daten: LOG_Rei.extend(Daten)
        return LOG_Rei[Laf:].decode('utf-8', 'replace')

    def klicken_Tast(Symbol, 눌림=True): extern_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, Symbol))

    def SMS_schécken(SMS):
        Laf = len(LOG_Rei)
        for Zeechen_VALUE in SMS:
            Symbol = 0xff0d if Zeechen_VALUE == '\n' else ord(Zeechen_VALUE) if ord(Zeechen_VALUE) < 256 else 0x1000000 | ord(Zeechen_VALUE)
            klicken_Tast(Symbol); klicken_Tast(Symbol, False)
        return Laf

    def Shell(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_schécken(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikal_positionéieren, 눌림): extern_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_positionéieren))

    def klicken_VALUE(가로, Vertikal_positionéieren): 가리키기(가로, Vertikal_positionéieren, 1); 가리키기(가로, Vertikal_positionéieren, 0)

    def Bitmap_Bild():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 aktuell_Daten 너비를 쓴다.
        extern_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        Zeechnung_VALUE = Image.new('RGB', (너비, 높이)); Beräich_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(extern_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                Längt_VALUE = struct.unpack('>I', EXACT_VALUE(extern_VALUE, 7)[3:])[0]; EXACT_VALUE(extern_VALUE, Längt_VALUE); continue
            assert 종류 == 0, 종류
            Element_COUNT = struct.unpack('>H', EXACT_VALUE(extern_VALUE, 3)[1:])[0]
            for _ in range(Element_COUNT):
                가로, Vertikal_positionéieren, 폭, Längt_VALUE, Codéierung_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(extern_VALUE, 12))
                if Codéierung_VALUE == -239:
                    assert 폭==0 and Längt_VALUE==0, 'remote cursor must be hidden'
                    Uweiser_verstoppt[0]=True
                    continue
                assert Codéierung_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_positionéieren+Längt_VALUE <= 높이
                Zeechnung_VALUE.paste(Image.frombytes('RGB', (폭, Längt_VALUE), EXACT_VALUE(extern_VALUE, 폭*Längt_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_positionéieren))
                Beräich_VALUE_9285603e += 폭*Längt_VALUE
            if Beräich_VALUE_9285603e:
                assert Beräich_VALUE_9285603e == 너비*높이, Beräich_VALUE_9285603e
                return Zeechnung_VALUE

    def Scheck_Pel(Coordonnée_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            Zeechnung_VALUE = Bitmap_Bild()
            if Zeechnung_VALUE.getpixel(Coordonnée_VALUE) == 색: return Zeechnung_VALUE
            if time.monotonic() > 마감: raise AssertionError((Coordonnée_VALUE, Zeechnung_VALUE.getpixel(Coordonnée_VALUE), 색))

    def eroplueden_Fichieren(Numm, Daten): Transfer_VALUE.storbinary('STOR '+Numm, io.BytesIO(Daten))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+d_Gréisst_veränneren_SMS+' RGB32').encode() in LOG_Rei
        print('BOOT:', d_Gréisst_veränneren_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_Rei).group(1))
        extern_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(extern_VALUE, 12) == b'RFB 003.008\n'; extern_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(extern_VALUE, EXACT_VALUE(extern_VALUE, 1)[0]); extern_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(extern_VALUE, 4) == b'\0'*4; extern_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(extern_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(extern_VALUE, struct.unpack('>I', 초기[20:])[0])
        extern_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        extern_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        Scheck_Pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Evenement,_ in Selekteur_a916db4e.select(.02):
                    Daten=Evenement.fileobj.read(65536)
                    if Daten:LOG_Rei.extend(Daten)
        Fënster=[12,48,568,360]
        def verifizéieren_d_Gréisst_veränneren():
            COLUMN_VALUE,ROW_VALUE=(Fënster[2]-24)//8,(Fënster[3]-56)//16
            SMS=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in SMS,SMS
            # aktuell_Daten Fënster 테두리: 단지 d_Gréisst_veränneren Requête_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            Scheck_Pel((Fënster[0],Fënster[1]),(32,80,144))
            Zeechnung_VALUE=Scheck_Pel((Fënster[0]+Fënster[2]-1,Fënster[1]+Fënster[3]-1),(39,49,64))
            return Zeechnung_VALUE
        def 모서리(방향):
            return (Fënster[0]+(3 if 방향 in (1,3) else Fënster[2]-4),Fënster[1]+(3 if 방향<=2 else Fënster[3]-4))
        def Gréisst_änneren_eriwwerzéien(방향,차이,Tast=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            Scheck_Pel(흰점,(255,255,255))
            가리키기(가,세,Tast)
            끝가=max(0,min(너비-1,가+차이[0]));bëennegen_Vertikal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,bëennegen_Vertikal,Tast);가리키기(끝가,bëennegen_Vertikal,0);숨고르기()
            if Tast==1:
                LEFT_VALUE,위,폭,Längt_VALUE=Fënster;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+Längt_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+bëennegen_Vertikal-세))
                else:아래=max(위+216,min(높이,아래+bëennegen_Vertikal-세))
                Fënster[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verifizéieren_d_Gréisst_veränneren();assert Uweiser_verstoppt[0]
        Gréisst_änneren_eriwwerzéien(4,(-100,-60),4);verifizéieren_d_Gréisst_veränneren() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            Gréisst_änneren_eriwwerzéien(방향,차이);verifizéieren_d_Gréisst_veränneren()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_schécken("echo '"+긴글+"'");숨고르기()
        Gréisst_änneren_eriwwerzéien(4,(-1000,-1000));assert Fënster[2:]==[360,216]
        Gréisst_änneren_eriwwerzéien(4,(너비,높이))
        Laf=SMS_schécken('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Laf);verifizéieren_d_Gréisst_veränneren()
        # vi가 Editéieren_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        Transfer_VALUE=ftplib.FTP();Transfer_VALUE.encoding='utf-8';Transfer_VALUE.connect('127.0.0.1',접속번호,timeout=20);Transfer_VALUE.login()
        기다리기(b'NORMAL',SMS_schécken('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_schécken('i미저장 한글 Daten\n'));숨고르기()
        Gréisst_änneren_eriwwerzéien(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Fënster[3]-56)//16)).encode() in LOG_Rei[-4096:]
        SMS_schécken('작은 창에서도 이어 schreiwen\n');숨고르기()
        Gréisst_änneren_eriwwerzéien(4,(너비,높이))
        SMS_schécken('큰 창에서도 이어 schreiwen\n');숨고르기()
        klicken_Tast(0xff1b);klicken_Tast(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_schécken(':wq\n'))
        Inhalt_VALUE=bytearray();Transfer_VALUE.retrbinary('RETR 크기자료.txt',Inhalt_VALUE.extend)
        assert Inhalt_VALUE=='미저장 한글 Daten\n작은 창에서도 이어 schreiwen\n큰 창에서도 이어 schreiwen\n'.encode(),Inhalt_VALUE
        verifizéieren_d_Gréisst_veränneren().save(str(Mooss_Wee/(d_Gréisst_veränneren_SMS+'-large.png')))
        # 두 번째 창은 Standardwäert d_Gréisst_veränneren, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Laf=len(LOG_Rei);klicken_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Laf)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        Laf=len(LOG_Rei);klicken_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Laf);verifizéieren_d_Gréisst_veränneren()
        Gréisst_änneren_eriwwerzéien(4,(-너비,-높이));verifizéieren_d_Gréisst_veränneren().save(str(Mooss_Wee/(d_Gréisst_veränneren_SMS+'-small.png')))
        # d_Gréisst_veränneren änneren_VALUE Zeréck_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Laf=len(LOG_Rei);klicken_VALUE(Fënster[0]+Fënster[2]-20,Fënster[1]+15);기다리기(b'TERMINAL FOCUS 2',Laf)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',d_Gréisst_veränneren_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Transfer_VALUE:Transfer_VALUE.close()
        if extern_VALUE:extern_VALUE.close()
        if Prozess_VALUE.poll() is None:
            Prozess_VALUE.terminate()
            try:Prozess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Prozess_VALUE.kill();Prozess_VALUE.wait()
        Selekteur_a916db4e.close();Prozess_VALUE.stdout.close();(Mooss_Wee/(d_Gréisst_veränneren_SMS+'.log')).write_bytes(LOG_Rei)


def Laf():
    Mooss_Wee=projezéieren_Racinn/'build/verification/resize';Mooss_Wee.mkdir(parents=True,exist_ok=True)
    LOG_Rei={'passed':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,Mooss_Wee);LOG_Rei['resolutions'].append([너비,높이])
        LOG_Rei.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(Mooss_Wee/'report.json').write_text(json.dumps(LOG_Rei,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Laf()
