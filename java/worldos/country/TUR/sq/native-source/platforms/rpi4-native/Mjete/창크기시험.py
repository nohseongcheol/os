#!/usr/bin/env python3
"""aktual_të_dhëna QEMU/VNC에서 Terminali 모서리 zvarrit_VALUE·tregues·동적 karakter_VALUE hapësirë_për_tekst_futje·redaktim_VALUE Përmbajtje_VALUE 보존를 검사한다."""
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
from desktop_Pamja import EXACT_VALUE
from zbatoj_komandë import Project_rrënjë


def 창크기시험(너비, 높이, llogaritje_shteg):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numri_i_portës = 임시.getsockname()[1]
    ndryshoj_përmasat_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(Project_rrënjë/'Mjete/zbatoj_komandë.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numri_i_portës), '--resolution', ndryshoj_përmasat_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    përzgjedhësi_a916db4e = selectors.DefaultSelector(); përzgjedhësi_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); në_largësi_VALUE = None; transferim_VALUE = None; tregues_i_fshehur=[False]

    def 기다리기(shfaq_VALUE, Ekzekuto=0):
        마감 = time.monotonic() + 60
        while shfaq_VALUE not in LOG_RECORD[Ekzekuto:]:
            if time.monotonic() > 마감 or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Ekzekuto:].decode('utf-8', 'replace'))
            for Ngjarje, _ in përzgjedhësi_a916db4e.select(.1):
                të_dhëna = Ngjarje.fileobj.read(65536)
                if të_dhëna: LOG_RECORD.extend(të_dhëna)
        return LOG_RECORD[Ekzekuto:].decode('utf-8', 'replace')

    def klik_buton(simbol, 눌림=True): në_largësi_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def dërgoj_SMS(Teksti):
        Ekzekuto = len(LOG_RECORD)
        for karakter_VALUE in Teksti:
            simbol = 0xff0d if karakter_VALUE == '\n' else ord(karakter_VALUE) if ord(karakter_VALUE) < 256 else 0x1000000 | ord(karakter_VALUE)
            klik_buton(simbol); klik_buton(simbol, False)
        return Ekzekuto

    def pasues(Teksti): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', dërgoj_SMS(Teksti+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikal_pozicioni, 눌림): në_largësi_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_pozicioni))

    def klik_VALUE(가로, Vertikal_pozicioni): 가리키기(가로, Vertikal_pozicioni, 1); 가리키기(가로, Vertikal_pozicioni, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 aktual_të_dhëna 너비를 쓴다.
        në_largësi_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        vizatim_VALUE = Image.new('RGB', (너비, 높이)); zonë_VALUE = 0
        while True:
            종류 = EXACT_VALUE(në_largësi_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                gjatësi_VALUE = struct.unpack('>I', EXACT_VALUE(në_largësi_VALUE, 7)[3:])[0]; EXACT_VALUE(në_largësi_VALUE, gjatësi_VALUE); continue
            assert 종류 == 0, 종류
            njësi_COUNT = struct.unpack('>H', EXACT_VALUE(në_largësi_VALUE, 3)[1:])[0]
            for _ in range(njësi_COUNT):
                가로, Vertikal_pozicioni, 폭, gjatësi_VALUE, enkodim_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(në_largësi_VALUE, 12))
                if enkodim_VALUE == -239:
                    assert 폭==0 and gjatësi_VALUE==0, 'remote cursor must be hidden'
                    tregues_i_fshehur[0]=True
                    continue
                assert enkodim_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_pozicioni+gjatësi_VALUE <= 높이
                vizatim_VALUE.paste(Image.frombytes('RGB', (폭, gjatësi_VALUE), EXACT_VALUE(në_largësi_VALUE, 폭*gjatësi_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_pozicioni))
                zonë_VALUE += 폭*gjatësi_VALUE
            if zonë_VALUE:
                assert zonë_VALUE == 너비*높이, zonë_VALUE
                return vizatim_VALUE

    def çek_pikëz(koordinatë_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            vizatim_VALUE = bitmap_IMAGE()
            if vizatim_VALUE.getpixel(koordinatë_VALUE) == 색: return vizatim_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinatë_VALUE, vizatim_VALUE.getpixel(koordinatë_VALUE), 색))

    def Ngarkim_Skedarët(Emër, të_dhëna): transferim_VALUE.storbinary('STOR '+Emër, io.BytesIO(të_dhëna))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ndryshoj_përmasat_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', ndryshoj_përmasat_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        në_largësi_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(në_largësi_VALUE, 12) == b'RFB 003.008\n'; në_largësi_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(në_largësi_VALUE, EXACT_VALUE(në_largësi_VALUE, 1)[0]); në_largësi_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(në_largësi_VALUE, 4) == b'\0'*4; në_largësi_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(në_largësi_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(në_largësi_VALUE, struct.unpack('>I', 초기[20:])[0])
        në_largësi_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        në_largësi_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        çek_pikëz((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Ngjarje,_ in përzgjedhësi_a916db4e.select(.02):
                    të_dhëna=Ngjarje.fileobj.read(65536)
                    if të_dhëna:LOG_RECORD.extend(të_dhëna)
        Dritare=[12,48,568,360]
        def verifikoj_ndryshoj_përmasat():
            COLUMN_VALUE,ROW_VALUE=(Dritare[2]-24)//8,(Dritare[3]-56)//16
            Teksti=pasues('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Teksti,Teksti
            # aktual_të_dhëna Dritare 테두리: 단지 Madhësi pyetja_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            çek_pikëz((Dritare[0],Dritare[1]),(32,80,144))
            vizatim_VALUE=çek_pikëz((Dritare[0]+Dritare[2]-1,Dritare[1]+Dritare[3]-1),(39,49,64))
            return vizatim_VALUE
        def 모서리(방향):
            return (Dritare[0]+(3 if 방향 in (1,3) else Dritare[2]-4),Dritare[1]+(3 if 방향<=2 else Dritare[3]-4))
        def ndrysho_madhësinë_zvarrit(방향,차이,Buton=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            çek_pikëz(흰점,(255,255,255))
            가리키기(가,세,Buton)
            끝가=max(0,min(너비-1,가+차이[0]));mbaroj_Vertikal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,mbaroj_Vertikal,Buton);가리키기(끝가,mbaroj_Vertikal,0);숨고르기()
            if Buton==1:
                LEFT_VALUE,위,폭,gjatësi_VALUE=Dritare;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+gjatësi_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+mbaroj_Vertikal-세))
                else:아래=max(위+216,min(높이,아래+mbaroj_Vertikal-세))
                Dritare[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verifikoj_ndryshoj_përmasat();assert tregues_i_fshehur[0]
        ndrysho_madhësinë_zvarrit(4,(-100,-60),4);verifikoj_ndryshoj_përmasat() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ndrysho_madhësinë_zvarrit(방향,차이);verifikoj_ndryshoj_përmasat()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        dërgoj_SMS("echo '"+긴글+"'");숨고르기()
        ndrysho_madhësinë_zvarrit(4,(-1000,-1000));assert Dritare[2:]==[360,216]
        ndrysho_madhësinë_zvarrit(4,(너비,높이))
        Ekzekuto=dërgoj_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Ekzekuto);verifikoj_ndryshoj_përmasat()
        # vi가 redaktim_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        pasues('ftpd start')
        transferim_VALUE=ftplib.FTP();transferim_VALUE.encoding='utf-8';transferim_VALUE.connect('127.0.0.1',numri_i_portës,timeout=20);transferim_VALUE.login()
        기다리기(b'NORMAL',dërgoj_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',dërgoj_SMS('i미저장 한글 të_dhëna\n'));숨고르기()
        ndrysho_madhësinë_zvarrit(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Dritare[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        dërgoj_SMS('작은 창에서도 이어 Shkrimi\n');숨고르기()
        ndrysho_madhësinë_zvarrit(4,(너비,높이))
        dërgoj_SMS('큰 창에서도 이어 Shkrimi\n');숨고르기()
        klik_buton(0xff1b);klik_buton(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',dërgoj_SMS(':wq\n'))
        Përmbajtje_VALUE=bytearray();transferim_VALUE.retrbinary('RETR 크기자료.txt',Përmbajtje_VALUE.extend)
        assert Përmbajtje_VALUE=='미저장 한글 të_dhëna\n작은 창에서도 이어 Shkrimi\n큰 창에서도 이어 Shkrimi\n'.encode(),Përmbajtje_VALUE
        verifikoj_ndryshoj_përmasat().save(str(llogaritje_shteg/(ndryshoj_përmasat_SMS+'-large.png')))
        # 두 번째 창은 vlerë_e_parazgjedhur Madhësi, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Ekzekuto=len(LOG_RECORD);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Ekzekuto)
        assert 'TERMINAL SIZE 68x19' in pasues('terminal size')
        Ekzekuto=len(LOG_RECORD);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Ekzekuto);verifikoj_ndryshoj_përmasat()
        ndrysho_madhësinë_zvarrit(4,(-너비,-높이));verifikoj_ndryshoj_përmasat().save(str(llogaritje_shteg/(ndryshoj_përmasat_SMS+'-small.png')))
        # Madhësi ndryshoj_VALUE PAS_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Ekzekuto=len(LOG_RECORD);klik_VALUE(Dritare[0]+Dritare[2]-20,Dritare[1]+15);기다리기(b'TERMINAL FOCUS 2',Ekzekuto)
        assert 'RESIZE CLOSED' in pasues('echo RESIZE CLOSED')
        print('PASS:',ndryshoj_përmasat_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transferim_VALUE:transferim_VALUE.close()
        if në_largësi_VALUE:në_largësi_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        përzgjedhësi_a916db4e.close();Proces_VALUE.stdout.close();(llogaritje_shteg/(ndryshoj_përmasat_SMS+'.log')).write_bytes(LOG_RECORD)


def Ekzekuto():
    llogaritje_shteg=Project_rrënjë/'build/verification/resize';llogaritje_shteg.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,llogaritje_shteg);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(llogaritje_shteg/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Ekzekuto()
