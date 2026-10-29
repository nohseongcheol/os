#!/usr/bin/env python3
"""tegelik_andmed QEMU/VNC에서 terminal 모서리 lohistama_VALUE·kursor·동적 märk_VALUE 칸·muudatus_VALUE Sisu_VALUE 보존를 검사한다."""
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
from töölaud_Kuva import EXACT_VALUE
from Täida_käsk import Project_juur


def 창크기시험(너비, 높이, näitaja_tee):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); pordinumber = 임시.getsockname()[1]
    suurust_muutma_SMS = '{}x{}'.format(너비, 높이)
    Joonis_VALUE = subprocess.Popen(['python3', str(Project_juur/'Tööriistad/Täida_käsk.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(pordinumber), '--resolution', suurust_muutma_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valija_a916db4e = selectors.DefaultSelector(); valija_a916db4e.register(Joonis_VALUE.stdout, selectors.EVENT_READ)
    LOG_kirje = bytearray(); kauge_VALUE = None; Edasta_VALUE = None; kursor_Peidetud=[False]

    def 기다리기(saade_VALUE, Käivita_2=0):
        tähtaeg_VALUE = time.monotonic() + 60
        while saade_VALUE not in LOG_kirje[Käivita_2:]:
            if time.monotonic() > tähtaeg_VALUE or Joonis_VALUE.poll() is not None or b'HALTED' in LOG_kirje or b'PANIC:' in LOG_kirje:
                raise AssertionError(LOG_kirje[Käivita_2:].decode('utf-8', 'replace'))
            for Sündmus, _ in valija_a916db4e.select(.1):
                andmed = Sündmus.fileobj.read(65536)
                if andmed: LOG_kirje.extend(andmed)
        return LOG_kirje[Käivita_2:].decode('utf-8', 'replace')

    def klõps_nupp(sümbol, 눌림=True): kauge_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, sümbol))

    def SMSi_saatmine(Tekst):
        Käivita_2 = len(LOG_kirje)
        for märk_VALUE in Tekst:
            sümbol = 0xff0d if märk_VALUE == '\n' else ord(märk_VALUE) if ord(märk_VALUE) < 256 else 0x1000000 | ord(märk_VALUE)
            klõps_nupp(sümbol); klõps_nupp(sümbol, False)
        return Käivita_2

    def kest(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMSi_saatmine(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikaal_ametikoht, 눌림): kauge_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikaal_ametikoht))

    def klõps_VALUE(가로, vertikaal_ametikoht): 가리키기(가로, vertikaal_ametikoht, 1); 가리키기(가로, vertikaal_ametikoht, 0)

    def bittraster_pilt():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tegelik_andmed 너비를 쓴다.
        kauge_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        joonis_VALUE = Image.new('RGB', (너비, 높이)); ala_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(kauge_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(kauge_VALUE, 7)[3:])[0]; EXACT_VALUE(kauge_VALUE, 길이); continue
            assert 종류 == 0, 종류
            kaup_COUNT = struct.unpack('>H', EXACT_VALUE(kauge_VALUE, 3)[1:])[0]
            for _ in range(kaup_COUNT):
                가로, vertikaal_ametikoht, 폭, 길이, kodeerimine_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(kauge_VALUE, 12))
                if kodeerimine_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    kursor_Peidetud[0]=True
                    continue
                assert kodeerimine_VALUE == 0 and 가로+폭 <= 너비 and vertikaal_ametikoht+길이 <= 높이
                joonis_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(kauge_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikaal_ametikoht))
                ala_VALUE_9285603e += 폭*길이
            if ala_VALUE_9285603e:
                assert ala_VALUE_9285603e == 너비*높이, ala_VALUE_9285603e
                return joonis_VALUE

    def tšekk_piksel(좌표, 색):
        tähtaeg_VALUE = time.monotonic()+10
        while True:
            joonis_VALUE = bittraster_pilt()
            if joonis_VALUE.getpixel(좌표) == 색: return joonis_VALUE
            if time.monotonic() > tähtaeg_VALUE: raise AssertionError((좌표, joonis_VALUE.getpixel(좌표), 색))

    def Upload_Failid(Nimi_2, andmed): Edasta_VALUE.storbinary('STOR '+Nimi_2, io.BytesIO(andmed))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+suurust_muutma_SMS+' RGB32').encode() in LOG_kirje
        print('BOOT:', suurust_muutma_SMS, flush=True)
        kauge_number = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_kirje).group(1))
        kauge_VALUE = socket.create_connection(('127.0.0.1', kauge_number), timeout=20)
        assert EXACT_VALUE(kauge_VALUE, 12) == b'RFB 003.008\n'; kauge_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(kauge_VALUE, EXACT_VALUE(kauge_VALUE, 1)[0]); kauge_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(kauge_VALUE, 4) == b'\0'*4; kauge_VALUE.sendall(b'\x01')
        lähteolek = EXACT_VALUE(kauge_VALUE, 24); assert struct.unpack('>HH', lähteolek[:4]) == (너비, 높이)
        EXACT_VALUE(kauge_VALUE, struct.unpack('>I', lähteolek[20:])[0])
        kauge_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kauge_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        tšekk_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Sündmus,_ in valija_a916db4e.select(.02):
                    andmed=Sündmus.fileobj.read(65536)
                    if andmed:LOG_kirje.extend(andmed)
        aken=[12,48,568,360]
        def kinnitama_suurust_muutma():
            veerg_VALUE,ROW_VALUE=(aken[2]-24)//8,(aken[3]-56)//16
            Tekst=kest('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(veerg_VALUE,ROW_VALUE) in Tekst,Tekst
            # tegelik_andmed aken 테두리: 단지 Suurus päring_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            tšekk_piksel((aken[0],aken[1]),(32,80,144))
            joonis_VALUE=tšekk_piksel((aken[0]+aken[2]-1,aken[1]+aken[3]-1),(39,49,64))
            return joonis_VALUE
        def 모서리(방향):
            return (aken[0]+(3 if 방향 in (1,3) else aken[2]-4),aken[1]+(3 if 방향<=2 else aken[3]-4))
        def suurust_muutma_lohistama(방향,차이,nupp=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            tšekk_piksel(흰점,(255,255,255))
            가리키기(가,세,nupp)
            끝가=max(0,min(너비-1,가+차이[0]));lõpeta_kõne_vertikaal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,lõpeta_kõne_vertikaal,nupp);가리키기(끝가,lõpeta_kõne_vertikaal,0);숨고르기()
            if nupp==1:
                LEFT_VALUE,위,폭,길이=aken;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+lõpeta_kõne_vertikaal-세))
                else:아래=max(위+216,min(높이,아래+lõpeta_kõne_vertikaal-세))
                aken[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        kinnitama_suurust_muutma();assert kursor_Peidetud[0]
        suurust_muutma_lohistama(4,(-100,-60),4);kinnitama_suurust_muutma() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            suurust_muutma_lohistama(방향,차이);kinnitama_suurust_muutma()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMSi_saatmine("echo '"+긴글+"'");숨고르기()
        suurust_muutma_lohistama(4,(-1000,-1000));assert aken[2:]==[360,216]
        suurust_muutma_lohistama(4,(너비,높이))
        Käivita_2=SMSi_saatmine('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Käivita_2);kinnitama_suurust_muutma()
        # vi가 muudatus_VALUE 중에 화면 크기를 uuesti_proovima_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        kest('ftpd start')
        Edasta_VALUE=ftplib.FTP();Edasta_VALUE.encoding='utf-8';Edasta_VALUE.connect('127.0.0.1',pordinumber,timeout=20);Edasta_VALUE.login()
        기다리기(b'NORMAL',SMSi_saatmine('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMSi_saatmine('i미저장 한글 andmed\n'));숨고르기()
        suurust_muutma_lohistama(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((aken[3]-56)//16)).encode() in LOG_kirje[-4096:]
        SMSi_saatmine('작은 창에서도 이어 Kirjutamine\n');숨고르기()
        suurust_muutma_lohistama(4,(너비,높이))
        SMSi_saatmine('큰 창에서도 이어 Kirjutamine\n');숨고르기()
        klõps_nupp(0xff1b);klõps_nupp(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMSi_saatmine(':wq\n'))
        Sisu_VALUE=bytearray();Edasta_VALUE.retrbinary('RETR 크기자료.txt',Sisu_VALUE.extend)
        assert Sisu_VALUE=='미저장 한글 andmed\n작은 창에서도 이어 Kirjutamine\n큰 창에서도 이어 Kirjutamine\n'.encode(),Sisu_VALUE
        kinnitama_suurust_muutma().save(str(näitaja_tee/(suurust_muutma_SMS+'-large.png')))
        # 두 번째 창은 vaikeväärtus Suurus, uuesti_proovima_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Käivita_2=len(LOG_kirje);klõps_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Käivita_2)
        assert 'TERMINAL SIZE 68x19' in kest('terminal size')
        Käivita_2=len(LOG_kirje);klõps_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Käivita_2);kinnitama_suurust_muutma()
        suurust_muutma_lohistama(4,(-너비,-높이));kinnitama_suurust_muutma().save(str(näitaja_tee/(suurust_muutma_SMS+'-small.png')))
        # Suurus muutma_VALUE Tagasi_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Käivita_2=len(LOG_kirje);klõps_VALUE(aken[0]+aken[2]-20,aken[1]+15);기다리기(b'TERMINAL FOCUS 2',Käivita_2)
        assert 'RESIZE CLOSED' in kest('echo RESIZE CLOSED')
        print('PASS:',suurust_muutma_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Edasta_VALUE:Edasta_VALUE.close()
        if kauge_VALUE:kauge_VALUE.close()
        if Joonis_VALUE.poll() is None:
            Joonis_VALUE.terminate()
            try:Joonis_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Joonis_VALUE.kill();Joonis_VALUE.wait()
        valija_a916db4e.close();Joonis_VALUE.stdout.close();(näitaja_tee/(suurust_muutma_SMS+'.log')).write_bytes(LOG_kirje)


def Käivita_2():
    näitaja_tee=Project_juur/'build/verification/resize';näitaja_tee.mkdir(parents=True,exist_ok=True)
    LOG_kirje={'passed':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,näitaja_tee);LOG_kirje['resolutions'].append([너비,높이])
        LOG_kirje.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(näitaja_tee/'report.json').write_text(json.dumps(LOG_kirje,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Käivita_2()
