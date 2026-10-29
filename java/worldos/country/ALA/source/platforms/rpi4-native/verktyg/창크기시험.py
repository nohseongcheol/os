#!/usr/bin/env python3
"""verklig_data QEMU/VNC에서 kommandotolk 모서리 dra_värde·markör·동적 tecken_värde fack_post·ändring_värde Innehåll_värde 보존를 검사한다."""
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
from Dator_vy import EXAKT_värde
from köra_kommando import åtgärd_rot


def 창크기시험(너비, 높이, KR_väg):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    storlek_SMS = '{}x{}'.format(너비, 높이)
    Process_värde = subprocess.Popen(['python3', str(åtgärd_rot/'verktyg/köra_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', storlek_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    väljare_a916db4e = selectors.DefaultSelector(); väljare_a916db4e.register(Process_värde.stdout, selectors.EVENT_READ)
    LOG_POST = bytearray(); fjärr_värde = None; Överför_värde = None; markör_Dold=[False]

    def 기다리기(visa_värde, Kör=0):
        måldatum_värde = time.monotonic() + 60
        while visa_värde not in LOG_POST[Kör:]:
            if time.monotonic() > måldatum_värde or Process_värde.poll() is not None or b'HALTED' in LOG_POST or b'PANIC:' in LOG_POST:
                raise AssertionError(LOG_POST[Kör:].decode('utf-8', 'replace'))
            for Händelse, _ in väljare_a916db4e.select(.1):
                data = Händelse.fileobj.read(65536)
                if data: LOG_POST.extend(data)
        return LOG_POST[Kör:].decode('utf-8', 'replace')

    def klick_knapp(symbol, 눌림=True): fjärr_värde.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def skicka_SMS(text):
        Kör = len(LOG_POST)
        for tecken_värde in text:
            symbol = 0xff0d if tecken_värde == '\n' else ord(tecken_värde) if ord(tecken_värde) < 256 else 0x1000000 | ord(tecken_värde)
            klick_knapp(symbol); klick_knapp(symbol, False)
        return Kör

    def Shell(text): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', skicka_SMS(text+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, bransch_placera, 눌림): fjärr_värde.sendall(struct.pack('>BBHH', 5, 눌림, 가로, bransch_placera))

    def klick_värde(가로, bransch_placera): 가리키기(가로, bransch_placera, 1); 가리키기(가로, bransch_placera, 0)

    def bitmapp_BILD():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 verklig_data 너비를 쓴다.
        fjärr_värde.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ritning_värde = Image.new('RGB', (너비, 높이)); yta_värde = 0
        while True:
            variant_värde = EXAKT_värde(fjärr_värde, 1)[0]
            if variant_värde == 2: continue
            if variant_värde == 3:
                längd_värde = struct.unpack('>I', EXAKT_värde(fjärr_värde, 7)[3:])[0]; EXAKT_värde(fjärr_värde, längd_värde); continue
            assert variant_värde == 0, variant_värde
            objekt_ANTAL = struct.unpack('>H', EXAKT_värde(fjärr_värde, 3)[1:])[0]
            for _ in range(objekt_ANTAL):
                가로, bransch_placera, 폭, längd_värde, kodning_värde = struct.unpack('>HHHHi', EXAKT_värde(fjärr_värde, 12))
                if kodning_värde == -239:
                    assert 폭==0 and längd_värde==0, 'remote cursor must be hidden'
                    markör_Dold[0]=True
                    continue
                assert kodning_värde == 0 and 가로+폭 <= 너비 and bransch_placera+längd_värde <= 높이
                ritning_värde.paste(Image.frombytes('RGB', (폭, längd_värde), EXAKT_värde(fjärr_värde, 폭*längd_värde*4), 'raw', 'BGRX'), (가로, bransch_placera))
                yta_värde += 폭*längd_värde
            if yta_värde:
                assert yta_värde == 너비*높이, yta_värde
                return ritning_värde

    def check_bildpunkt(koordinat_värde, 색):
        måldatum_värde = time.monotonic()+10
        while True:
            ritning_värde = bitmapp_BILD()
            if ritning_värde.getpixel(koordinat_värde) == 색: return ritning_värde
            if time.monotonic() > måldatum_värde: raise AssertionError((koordinat_värde, ritning_värde.getpixel(koordinat_värde), 색))

    def Upload_Filer(Namn, data): Överför_värde.storbinary('STOR '+Namn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+storlek_SMS+' RGB32').encode() in LOG_POST
        print('BOOT:', storlek_SMS, flush=True)
        fjärr_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_POST).group(1))
        fjärr_värde = socket.create_connection(('127.0.0.1', fjärr_nummer), timeout=20)
        assert EXAKT_värde(fjärr_värde, 12) == b'RFB 003.008\n'; fjärr_värde.sendall(b'RFB 003.008\n')
        assert 1 in EXAKT_värde(fjärr_värde, EXAKT_värde(fjärr_värde, 1)[0]); fjärr_värde.sendall(b'\x01')
        assert EXAKT_värde(fjärr_värde, 4) == b'\0'*4; fjärr_värde.sendall(b'\x01')
        starttillstånd = EXAKT_värde(fjärr_värde, 24); assert struct.unpack('>HH', starttillstånd[:4]) == (너비, 높이)
        EXAKT_värde(fjärr_värde, struct.unpack('>I', starttillstånd[20:])[0])
        fjärr_värde.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjärr_värde.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        check_bildpunkt((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Händelse,_ in väljare_a916db4e.select(.02):
                    data=Händelse.fileobj.read(65536)
                    if data:LOG_POST.extend(data)
        Fönster=[12,48,568,360]
        def verifiera_storlek():
            spalt_värde,RAD_värde=(Fönster[2]-24)//8,(Fönster[3]-56)//16
            text=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(spalt_värde,RAD_värde) in text,text
            # verklig_data Fönster 테두리: 단지 Storlek fråga_värde 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            check_bildpunkt((Fönster[0],Fönster[1]),(32,80,144))
            ritning_värde=check_bildpunkt((Fönster[0]+Fönster[2]-1,Fönster[1]+Fönster[3]-1),(39,49,64))
            return ritning_värde
        def 모서리(방향):
            return (Fönster[0]+(3 if 방향 in (1,3) else Fönster[2]-4),Fönster[1]+(3 if 방향<=2 else Fönster[3]-4))
        def ändra_storlek_dra(방향,차이,knapp=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            check_bildpunkt(흰점,(255,255,255))
            가리키기(가,세,knapp)
            끝가=max(0,min(너비-1,가+차이[0]));avsluta_bransch=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,avsluta_bransch,knapp);가리키기(끝가,avsluta_bransch,0);숨고르기()
            if knapp==1:
                VÄNSTER_värde,위,폭,längd_värde=Fönster;HÖGER_värde,아래=VÄNSTER_värde+폭,위+längd_värde
                if 방향 in (1,3):VÄNSTER_värde=max(0,min(HÖGER_värde-360,VÄNSTER_värde+끝가-가))
                else:HÖGER_värde=max(VÄNSTER_värde+360,min(너비,HÖGER_värde+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+avsluta_bransch-세))
                else:아래=max(위+216,min(높이,아래+avsluta_bransch-세))
                Fönster[:]=[VÄNSTER_värde,위,HÖGER_värde-VÄNSTER_värde,아래-위]
        verifiera_storlek();assert markör_Dold[0]
        ändra_storlek_dra(4,(-100,-60),4);verifiera_storlek() # HÖGER 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ändra_storlek_dra(방향,차이);verifiera_storlek()
        # indata_värde 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        skicka_SMS("echo '"+긴글+"'");숨고르기()
        ändra_storlek_dra(4,(-1000,-1000));assert Fönster[2:]==[360,216]
        ändra_storlek_dra(4,(너비,높이))
        Kör=skicka_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Kör);verifiera_storlek()
        # vi가 ändring_värde 중에 skärmbild 크기를 försöka_igen_värde 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        Överför_värde=ftplib.FTP();Överför_värde.encoding='utf-8';Överför_värde.connect('127.0.0.1',portnummer,timeout=20);Överför_värde.login()
        기다리기(b'NORMAL',skicka_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',skicka_SMS('i미저장 한글 data\n'));숨고르기()
        ändra_storlek_dra(4,(-너비,-높이))
        # ANSI RAD_värde 이동에 새 RAD_värde 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Fönster[3]-56)//16)).encode() in LOG_POST[-4096:]
        skicka_SMS('작은 창에서도 이어 Skriv\n');숨고르기()
        ändra_storlek_dra(4,(너비,높이))
        skicka_SMS('큰 창에서도 이어 Skriv\n');숨고르기()
        klick_knapp(0xff1b);klick_knapp(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',skicka_SMS(':wq\n'))
        Innehåll_värde=bytearray();Överför_värde.retrbinary('RETR 크기자료.txt',Innehåll_värde.extend)
        assert Innehåll_värde=='미저장 한글 data\n작은 창에서도 이어 Skriv\n큰 창에서도 이어 Skriv\n'.encode(),Innehåll_värde
        verifiera_storlek().save(str(KR_väg/(storlek_SMS+'-large.png')))
        # 두 번째 창은 standardvärde Storlek, försöka_igen_värde 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Kör=len(LOG_POST);klick_värde(70,16);기다리기(b'TERMINAL FOCUS 2',Kör)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        Kör=len(LOG_POST);klick_värde(180,16);기다리기(b'TERMINAL FOCUS 1',Kör);verifiera_storlek()
        ändra_storlek_dra(4,(-너비,-높이));verifiera_storlek().save(str(KR_väg/(storlek_SMS+'-small.png')))
        # Storlek ändra_värde BACK_värde X 닫기도 새로운 HÖGER 가장자리를 사용한다.
        Kör=len(LOG_POST);klick_värde(Fönster[0]+Fönster[2]-20,Fönster[1]+15);기다리기(b'TERMINAL FOCUS 2',Kör)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',storlek_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Överför_värde:Överför_värde.close()
        if fjärr_värde:fjärr_värde.close()
        if Process_värde.poll() is None:
            Process_värde.terminate()
            try:Process_värde.wait(timeout=8)
            except subprocess.TimeoutExpired:Process_värde.kill();Process_värde.wait()
        väljare_a916db4e.close();Process_värde.stdout.close();(KR_väg/(storlek_SMS+'.log')).write_bytes(LOG_POST)


def Kör():
    KR_väg=åtgärd_rot/'build/verification/resize';KR_väg.mkdir(parents=True,exist_ok=True)
    LOG_POST={'passed':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_väg);LOG_POST['resolutions'].append([너비,높이])
        LOG_POST.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_väg/'report.json').write_text(json.dumps(LOG_POST,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Kör()
