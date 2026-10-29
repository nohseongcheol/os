#!/usr/bin/env python3
"""dejanski_podatki QEMU/VNC에서 Terminal 모서리 povleči_VALUE·kazalec·동적 znak_VALUE 칸·Uredi_VALUE vsebina_VALUE 보존를 검사한다."""
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
from namizje_Pogled import EXACT_VALUE
from Izvedi_ukaz import pobuda_koren


def 창크기시험(너비, višina_VALUE, KR_pot):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); številka_vrat = 임시.getsockname()[1]
    spremeniti_velikost_SMS = '{}x{}'.format(너비, višina_VALUE)
    Proces_VALUE = subprocess.Popen(['python3', str(pobuda_koren/'Orodja/Izvedi_ukaz.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(številka_vrat), '--resolution', spremeniti_velikost_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    izbirnik_a916db4e = selectors.DefaultSelector(); izbirnik_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_zapis = bytearray(); oddaljen_VALUE = None; Prenos_VALUE = None; kazalec_Skrito=[False]

    def 기다리기(oddaja_VALUE_487749b8, Zaženi=0):
        rok_VALUE = time.monotonic() + 60
        while oddaja_VALUE_487749b8 not in LOG_zapis[Zaženi:]:
            if time.monotonic() > rok_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_zapis or b'PANIC:' in LOG_zapis:
                raise AssertionError(LOG_zapis[Zaženi:].decode('utf-8', 'replace'))
            for dogodek, _ in izbirnik_a916db4e.select(.1):
                podatki = dogodek.fileobj.read(65536)
                if podatki: LOG_zapis.extend(podatki)
        return LOG_zapis[Zaženi:].decode('utf-8', 'replace')

    def klik_gumb(simbol, 눌림=True): oddaljen_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def poslati_SMS(Besedilo):
        Zaženi = len(LOG_zapis)
        for znak_VALUE in Besedilo:
            simbol = 0xff0d if znak_VALUE == '\n' else ord(znak_VALUE) if ord(znak_VALUE) < 256 else 0x1000000 | ord(znak_VALUE)
            klik_gumb(simbol); klik_gumb(simbol, False)
        return Zaženi

    def lupina(Besedilo): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', poslati_SMS(Besedilo+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Navpično_položaj, 눌림): oddaljen_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Navpično_položaj))

    def klik_VALUE(가로, Navpično_položaj): 가리키기(가로, Navpično_položaj, 1); 가리키기(가로, Navpično_položaj, 0)

    def bitna_slika_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dejanski_podatki 너비를 쓴다.
        oddaljen_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, višina_VALUE))
        risba_VALUE = Image.new('RGB', (너비, višina_VALUE)); območje_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(oddaljen_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(oddaljen_VALUE, 7)[3:])[0]; EXACT_VALUE(oddaljen_VALUE, 길이); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(oddaljen_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Navpično_položaj, 폭, 길이, kodiranje_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(oddaljen_VALUE, 12))
                if kodiranje_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    kazalec_Skrito[0]=True
                    continue
                assert kodiranje_VALUE == 0 and 가로+폭 <= 너비 and Navpično_položaj+길이 <= višina_VALUE
                risba_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(oddaljen_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, Navpično_položaj))
                območje_VALUE_9285603e += 폭*길이
            if območje_VALUE_9285603e:
                assert območje_VALUE_9285603e == 너비*višina_VALUE, območje_VALUE_9285603e
                return risba_VALUE

    def preveriti_slikovna_pika(좌표, 색):
        rok_VALUE = time.monotonic()+10
        while True:
            risba_VALUE = bitna_slika_IMAGE()
            if risba_VALUE.getpixel(좌표) == 색: return risba_VALUE
            if time.monotonic() > rok_VALUE: raise AssertionError((좌표, risba_VALUE.getpixel(좌표), 색))

    def Upload_Datoteke(Ime, podatki): Prenos_VALUE.storbinary('STOR '+Ime, io.BytesIO(podatki))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+spremeniti_velikost_SMS+' RGB32').encode() in LOG_zapis
        print('BOOT:', spremeniti_velikost_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_zapis).group(1))
        oddaljen_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(oddaljen_VALUE, 12) == b'RFB 003.008\n'; oddaljen_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(oddaljen_VALUE, EXACT_VALUE(oddaljen_VALUE, 1)[0]); oddaljen_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(oddaljen_VALUE, 4) == b'\0'*4; oddaljen_VALUE.sendall(b'\x01')
        začetno_stanje = EXACT_VALUE(oddaljen_VALUE, 24); assert struct.unpack('>HH', začetno_stanje[:4]) == (너비, višina_VALUE)
        EXACT_VALUE(oddaljen_VALUE, struct.unpack('>I', začetno_stanje[20:])[0])
        oddaljen_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        oddaljen_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        preveriti_slikovna_pika((너비-1, višina_VALUE-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for dogodek,_ in izbirnik_a916db4e.select(.02):
                    podatki=dogodek.fileobj.read(65536)
                    if podatki:LOG_zapis.extend(podatki)
        okno=[12,48,568,360]
        def 크기확인():
            COLUMN_VALUE,ROW_VALUE=(okno[2]-24)//8,(okno[3]-56)//16
            Besedilo=lupina('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Besedilo,Besedilo
            # dejanski_podatki okno 테두리: 단지 Velikost poizvedba_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            preveriti_slikovna_pika((okno[0],okno[1]),(32,80,144))
            risba_VALUE=preveriti_slikovna_pika((okno[0]+okno[2]-1,okno[1]+okno[3]-1),(39,49,64))
            return risba_VALUE
        def 모서리(방향):
            return (okno[0]+(3 if 방향 in (1,3) else okno[2]-4),okno[1]+(3 if 방향<=2 else okno[3]-4))
        def spreminjati_velikost_povleči(방향,차이,Gumb=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            preveriti_slikovna_pika(흰점,(255,255,255))
            가리키기(가,세,Gumb)
            끝가=max(0,min(너비-1,가+차이[0]));končati_klic_Navpično=max(0,min(višina_VALUE-1,세+차이[1]))
            가리키기(끝가,končati_klic_Navpično,Gumb);가리키기(끝가,končati_klic_Navpično,0);숨고르기()
            if Gumb==1:
                LEFT_VALUE,위,폭,길이=okno;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+končati_klic_Navpično-세))
                else:아래=max(위+216,min(višina_VALUE,아래+končati_klic_Navpično-세))
                okno[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        크기확인();assert kazalec_Skrito[0]
        spreminjati_velikost_povleči(4,(-100,-60),4);크기확인() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            spreminjati_velikost_povleči(방향,차이);크기확인()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        poslati_SMS("echo '"+긴글+"'");숨고르기()
        spreminjati_velikost_povleči(4,(-1000,-1000));assert okno[2:]==[360,216]
        spreminjati_velikost_povleči(4,(너비,višina_VALUE))
        Zaženi=poslati_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Zaženi);크기확인()
        # vi가 Uredi_VALUE 중에 화면 크기를 znova_poskusiti_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        lupina('ftpd start')
        Prenos_VALUE=ftplib.FTP();Prenos_VALUE.encoding='utf-8';Prenos_VALUE.connect('127.0.0.1',številka_vrat,timeout=20);Prenos_VALUE.login()
        기다리기(b'NORMAL',poslati_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',poslati_SMS('i미저장 한글 podatki\n'));숨고르기()
        spreminjati_velikost_povleči(4,(-너비,-višina_VALUE))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((okno[3]-56)//16)).encode() in LOG_zapis[-4096:]
        poslati_SMS('작은 창에서도 이어 Pisanje\n');숨고르기()
        spreminjati_velikost_povleči(4,(너비,višina_VALUE))
        poslati_SMS('큰 창에서도 이어 Pisanje\n');숨고르기()
        klik_gumb(0xff1b);klik_gumb(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',poslati_SMS(':wq\n'))
        vsebina_VALUE=bytearray();Prenos_VALUE.retrbinary('RETR 크기자료.txt',vsebina_VALUE.extend)
        assert vsebina_VALUE=='미저장 한글 podatki\n작은 창에서도 이어 Pisanje\n큰 창에서도 이어 Pisanje\n'.encode(),vsebina_VALUE
        크기확인().save(str(KR_pot/(spremeniti_velikost_SMS+'-large.png')))
        # 두 번째 창은 privzeta_vrednost Velikost, znova_poskusiti_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Zaženi=len(LOG_zapis);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Zaženi)
        assert 'TERMINAL SIZE 68x19' in lupina('terminal size')
        Zaženi=len(LOG_zapis);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Zaženi);크기확인()
        spreminjati_velikost_povleči(4,(-너비,-višina_VALUE));크기확인().save(str(KR_pot/(spremeniti_velikost_SMS+'-small.png')))
        # Velikost spremeniti_VALUE ZAJ_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Zaženi=len(LOG_zapis);klik_VALUE(okno[0]+okno[2]-20,okno[1]+15);기다리기(b'TERMINAL FOCUS 2',Zaženi)
        assert 'RESIZE CLOSED' in lupina('echo RESIZE CLOSED')
        print('PASS:',spremeniti_velikost_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Prenos_VALUE:Prenos_VALUE.close()
        if oddaljen_VALUE:oddaljen_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VALUE.kill();Proces_VALUE.wait()
        izbirnik_a916db4e.close();Proces_VALUE.stdout.close();(KR_pot/(spremeniti_velikost_SMS+'.log')).write_bytes(LOG_zapis)


def Zaženi():
    KR_pot=pobuda_koren/'build/verification/resize';KR_pot.mkdir(parents=True,exist_ok=True)
    LOG_zapis={'passed':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,višina_VALUE in ((640,480),(1920,1080)):
            창크기시험(너비,višina_VALUE,KR_pot);LOG_zapis['resolutions'].append([너비,višina_VALUE])
        LOG_zapis.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_pot/'report.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Zaženi()
