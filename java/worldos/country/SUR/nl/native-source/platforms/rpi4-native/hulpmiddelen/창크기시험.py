#!/usr/bin/env python3
"""werkelijk_gegevens QEMU/VNC에서 terminal 모서리 slepen_WAARDE·wijzer·동적 teken_WAARDE sleuf_invoer·Bewerk_WAARDE Inhoud_WAARDE 보존를 검사한다."""
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
from pc_Weergave import GELIJK_WAARDE
from Uitvoeren_opdracht import Taken_wortel


def 창크기시험(너비, hoogte_WAARDE, HR_pad):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); poortnummer = 임시.getsockname()[1]
    formaat_wijzigen_sms = '{}x{}'.format(너비, hoogte_WAARDE)
    Proces_WAARDE = subprocess.Popen(['python3', str(Taken_wortel/'hulpmiddelen/Uitvoeren_opdracht.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(poortnummer), '--resolution', formaat_wijzigen_sms], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector_a916db4e = selectors.DefaultSelector(); selector_a916db4e.register(Proces_WAARDE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); extern_WAARDE_28edcfa1 = None; transfer_WAARDE = None; wijzer_Verborgen=[False]

    def 기다리기(weergeven_WAARDE, starten=0):
        deadline_WAARDE = time.monotonic() + 60
        while weergeven_WAARDE not in LOG_RECORD[starten:]:
            if time.monotonic() > deadline_WAARDE or Proces_WAARDE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[starten:].decode('utf-8', 'replace'))
            for Gebeurtenis, _ in selector_a916db4e.select(.1):
                gegevens = Gebeurtenis.fileobj.read(65536)
                if gegevens: LOG_RECORD.extend(gegevens)
        return LOG_RECORD[starten:].decode('utf-8', 'replace')

    def click_knop(symbool, 눌림=True): extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbool))

    def sms_en(tekst):
        starten = len(LOG_RECORD)
        for teken_WAARDE in tekst:
            symbool = 0xff0d if teken_WAARDE == '\n' else ord(teken_WAARDE) if ord(teken_WAARDE) < 256 else 0x1000000 | ord(teken_WAARDE)
            click_knop(symbool); click_knop(symbool, False)
        return starten

    def Shell(tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', sms_en(tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Verticaal_functie, 눌림): extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Verticaal_functie))

    def click_WAARDE(가로, Verticaal_functie): 가리키기(가로, Verticaal_functie, 1); 가리키기(가로, Verticaal_functie, 0)

    def bitmap_kopie():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 werkelijk_gegevens 너비를 쓴다.
        extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, hoogte_WAARDE))
        tekening_WAARDE = Image.new('RGB', (너비, hoogte_WAARDE)); gebied_WAARDE_9285603e = 0
        while True:
            soort_WAARDE = GELIJK_WAARDE(extern_WAARDE_28edcfa1, 1)[0]
            if soort_WAARDE == 2: continue
            if soort_WAARDE == 3:
                tijdsduur_WAARDE = struct.unpack('>I', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 7)[3:])[0]; GELIJK_WAARDE(extern_WAARDE_28edcfa1, tijdsduur_WAARDE); continue
            assert soort_WAARDE == 0, soort_WAARDE
            item_AANTAL = struct.unpack('>H', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 3)[1:])[0]
            for _ in range(item_AANTAL):
                가로, Verticaal_functie, 폭, tijdsduur_WAARDE, Encoding_WAARDE = struct.unpack('>HHHHi', GELIJK_WAARDE(extern_WAARDE_28edcfa1, 12))
                if Encoding_WAARDE == -239:
                    assert 폭==0 and tijdsduur_WAARDE==0, 'remote cursor must be hidden'
                    wijzer_Verborgen[0]=True
                    continue
                assert Encoding_WAARDE == 0 and 가로+폭 <= 너비 and Verticaal_functie+tijdsduur_WAARDE <= hoogte_WAARDE
                tekening_WAARDE.paste(Image.frombytes('RGB', (폭, tijdsduur_WAARDE), GELIJK_WAARDE(extern_WAARDE_28edcfa1, 폭*tijdsduur_WAARDE*4), 'raw', 'BGRX'), (가로, Verticaal_functie))
                gebied_WAARDE_9285603e += 폭*tijdsduur_WAARDE
            if gebied_WAARDE_9285603e:
                assert gebied_WAARDE_9285603e == 너비*hoogte_WAARDE, gebied_WAARDE_9285603e
                return tekening_WAARDE

    def cheque_pixel(coördinaat_WAARDE, 색):
        deadline_WAARDE = time.monotonic()+10
        while True:
            tekening_WAARDE = bitmap_kopie()
            if tekening_WAARDE.getpixel(coördinaat_WAARDE) == 색: return tekening_WAARDE
            if time.monotonic() > deadline_WAARDE: raise AssertionError((coördinaat_WAARDE, tekening_WAARDE.getpixel(coördinaat_WAARDE), 색))

    def Upload_Files(Naam, gegevens): transfer_WAARDE.storbinary('STOR '+Naam, io.BytesIO(gegevens))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+formaat_wijzigen_sms+' RGB32').encode() in LOG_RECORD
        print('BOOT:', formaat_wijzigen_sms, flush=True)
        extern_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        extern_WAARDE_28edcfa1 = socket.create_connection(('127.0.0.1', extern_nummer), timeout=20)
        assert GELIJK_WAARDE(extern_WAARDE_28edcfa1, 12) == b'RFB 003.008\n'; extern_WAARDE_28edcfa1.sendall(b'RFB 003.008\n')
        assert 1 in GELIJK_WAARDE(extern_WAARDE_28edcfa1, GELIJK_WAARDE(extern_WAARDE_28edcfa1, 1)[0]); extern_WAARDE_28edcfa1.sendall(b'\x01')
        assert GELIJK_WAARDE(extern_WAARDE_28edcfa1, 4) == b'\0'*4; extern_WAARDE_28edcfa1.sendall(b'\x01')
        begintoestand = GELIJK_WAARDE(extern_WAARDE_28edcfa1, 24); assert struct.unpack('>HH', begintoestand[:4]) == (너비, hoogte_WAARDE)
        GELIJK_WAARDE(extern_WAARDE_28edcfa1, struct.unpack('>I', begintoestand[20:])[0])
        extern_WAARDE_28edcfa1.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        extern_WAARDE_28edcfa1.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cheque_pixel((너비-1, hoogte_WAARDE-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Gebeurtenis,_ in selector_a916db4e.select(.02):
                    gegevens=Gebeurtenis.fileobj.read(65536)
                    if gegevens:LOG_RECORD.extend(gegevens)
        Venster=[12,48,568,360]
        def bevestigen_formaat_wijzigen():
            KOLOM_WAARDE,RIJ_WAARDE=(Venster[2]-24)//8,(Venster[3]-56)//16
            tekst=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(KOLOM_WAARDE,RIJ_WAARDE) in tekst,tekst
            # werkelijk_gegevens Venster 테두리: 단지 Grootte query_WAARDE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cheque_pixel((Venster[0],Venster[1]),(32,80,144))
            tekening_WAARDE=cheque_pixel((Venster[0]+Venster[2]-1,Venster[1]+Venster[3]-1),(39,49,64))
            return tekening_WAARDE
        def 모서리(방향):
            return (Venster[0]+(3 if 방향 in (1,3) else Venster[2]-4),Venster[1]+(3 if 방향<=2 else Venster[3]-4))
        def formaat_wijzigen_slepen(방향,차이,knop=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cheque_pixel(흰점,(255,255,255))
            가리키기(가,세,knop)
            끝가=max(0,min(너비-1,가+차이[0]));beëindigen_Verticaal=max(0,min(hoogte_WAARDE-1,세+차이[1]))
            가리키기(끝가,beëindigen_Verticaal,knop);가리키기(끝가,beëindigen_Verticaal,0);숨고르기()
            if knop==1:
                LINKS_WAARDE,위,폭,tijdsduur_WAARDE=Venster;recht_WAARDE,아래=LINKS_WAARDE+폭,위+tijdsduur_WAARDE
                if 방향 in (1,3):LINKS_WAARDE=max(0,min(recht_WAARDE-360,LINKS_WAARDE+끝가-가))
                else:recht_WAARDE=max(LINKS_WAARDE+360,min(너비,recht_WAARDE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+beëindigen_Verticaal-세))
                else:아래=max(위+216,min(hoogte_WAARDE,아래+beëindigen_Verticaal-세))
                Venster[:]=[LINKS_WAARDE,위,recht_WAARDE-LINKS_WAARDE,아래-위]
        bevestigen_formaat_wijzigen();assert wijzer_Verborgen[0]
        formaat_wijzigen_slepen(4,(-100,-60),4);bevestigen_formaat_wijzigen() # recht 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            formaat_wijzigen_slepen(방향,차이);bevestigen_formaat_wijzigen()
        # invoer_WAARDE 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        sms_en("echo '"+긴글+"'");숨고르기()
        formaat_wijzigen_slepen(4,(-1000,-1000));assert Venster[2:]==[360,216]
        formaat_wijzigen_slepen(4,(너비,hoogte_WAARDE))
        starten=sms_en('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),starten);bevestigen_formaat_wijzigen()
        # vi가 Bewerk_WAARDE 중에 scherm 크기를 opnieuw_proberen_WAARDE 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        transfer_WAARDE=ftplib.FTP();transfer_WAARDE.encoding='utf-8';transfer_WAARDE.connect('127.0.0.1',poortnummer,timeout=20);transfer_WAARDE.login()
        기다리기(b'NORMAL',sms_en('vi /크기자료.txt\n'))
        기다리기(b'INSERT',sms_en('i미저장 한글 gegevens\n'));숨고르기()
        formaat_wijzigen_slepen(4,(-너비,-hoogte_WAARDE))
        # ANSI RIJ_WAARDE 이동에 새 RIJ_WAARDE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Venster[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        sms_en('작은 창에서도 이어 Schrijven\n');숨고르기()
        formaat_wijzigen_slepen(4,(너비,hoogte_WAARDE))
        sms_en('큰 창에서도 이어 Schrijven\n');숨고르기()
        click_knop(0xff1b);click_knop(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',sms_en(':wq\n'))
        Inhoud_WAARDE=bytearray();transfer_WAARDE.retrbinary('RETR 크기자료.txt',Inhoud_WAARDE.extend)
        assert Inhoud_WAARDE=='미저장 한글 gegevens\n작은 창에서도 이어 Schrijven\n큰 창에서도 이어 Schrijven\n'.encode(),Inhoud_WAARDE
        bevestigen_formaat_wijzigen().save(str(HR_pad/(formaat_wijzigen_sms+'-large.png')))
        # 두 번째 창은 standaardwaarde Grootte, opnieuw_proberen_WAARDE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        starten=len(LOG_RECORD);click_WAARDE(70,16);기다리기(b'TERMINAL FOCUS 2',starten)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        starten=len(LOG_RECORD);click_WAARDE(180,16);기다리기(b'TERMINAL FOCUS 1',starten);bevestigen_formaat_wijzigen()
        formaat_wijzigen_slepen(4,(-너비,-hoogte_WAARDE));bevestigen_formaat_wijzigen().save(str(HR_pad/(formaat_wijzigen_sms+'-small.png')))
        # Grootte wijzigen_WAARDE BACK_WAARDE X 닫기도 새로운 recht 가장자리를 사용한다.
        starten=len(LOG_RECORD);click_WAARDE(Venster[0]+Venster[2]-20,Venster[1]+15);기다리기(b'TERMINAL FOCUS 2',starten)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',formaat_wijzigen_sms,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transfer_WAARDE:transfer_WAARDE.close()
        if extern_WAARDE_28edcfa1:extern_WAARDE_28edcfa1.close()
        if Proces_WAARDE.poll() is None:
            Proces_WAARDE.terminate()
            try:Proces_WAARDE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_WAARDE.kill();Proces_WAARDE.wait()
        selector_a916db4e.close();Proces_WAARDE.stdout.close();(HR_pad/(formaat_wijzigen_sms+'.log')).write_bytes(LOG_RECORD)


def starten():
    HR_pad=Taken_wortel/'build/verification/resize';HR_pad.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,hoogte_WAARDE in ((640,480),(1920,1080)):
            창크기시험(너비,hoogte_WAARDE,HR_pad);LOG_RECORD['resolutions'].append([너비,hoogte_WAARDE])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(HR_pad/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':starten()
