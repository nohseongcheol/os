#!/usr/bin/env python3
"""faktisk_data QEMU/VNC에서 Terminal 모서리 dra_VERDI·peker·동적 tegn_VERDI åpning_oppføring·Rediger_VERDI Innhold_VERDI 보존를 검사한다."""
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
from stasjonær_vise import EKSAKT_VERDI
from Utfør_kommando import speile_rot


def 창크기시험(너비, 높이, KR_bane):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    skalere_SMS = '{}x{}'.format(너비, 높이)
    Prosess_VERDI = subprocess.Popen(['python3', str(speile_rot/'Verktøy/Utfør_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', skalere_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    velger_a916db4e = selectors.DefaultSelector(); velger_a916db4e.register(Prosess_VERDI.stdout, selectors.EVENT_READ)
    LOG_POST = bytearray(); ekstern_VERDI_28edcfa1 = None; overføre_VERDI = None; peker_Skjult=[False]

    def 기다리기(vise_VERDI_487749b8, Kjør_2=0):
        tidsfrist_VERDI = time.monotonic() + 60
        while vise_VERDI_487749b8 not in LOG_POST[Kjør_2:]:
            if time.monotonic() > tidsfrist_VERDI or Prosess_VERDI.poll() is not None or b'HALTED' in LOG_POST or b'PANIC:' in LOG_POST:
                raise AssertionError(LOG_POST[Kjør_2:].decode('utf-8', 'replace'))
            for Hendelse, _ in velger_a916db4e.select(.1):
                data = Hendelse.fileobj.read(65536)
                if data: LOG_POST.extend(data)
        return LOG_POST[Kjør_2:].decode('utf-8', 'replace')

    def klikk_knapp(symbol, 눌림=True): ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def send_SMS(Tekst):
        Kjør_2 = len(LOG_POST)
        for tegn_VERDI in Tekst:
            symbol = 0xff0d if tegn_VERDI == '\n' else ord(tegn_VERDI) if ord(tegn_VERDI) < 256 else 0x1000000 | ord(tegn_VERDI)
            klikk_knapp(symbol); klikk_knapp(symbol, False)
        return Kjør_2

    def Shell(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', send_SMS(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikal_plassere, 눌림): ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikal_plassere))

    def klikk_VERDI(가로, vertikal_plassere): 가리키기(가로, vertikal_plassere, 1); 가리키기(가로, vertikal_plassere, 0)

    def punktgrafikk_BILDE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisk_data 너비를 쓴다.
        ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tegning_VERDI = Image.new('RGB', (너비, 높이)); område_VERDI_9285603e = 0
        while True:
            종류 = EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengde_VERDI = struct.unpack('>I', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 7)[3:])[0]; EKSAKT_VERDI(ekstern_VERDI_28edcfa1, lengde_VERDI); continue
            assert 종류 == 0, 종류
            vare_ANTALL = struct.unpack('>H', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 3)[1:])[0]
            for _ in range(vare_ANTALL):
                가로, vertikal_plassere, 폭, lengde_VERDI, koding_VERDI = struct.unpack('>HHHHi', EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 12))
                if koding_VERDI == -239:
                    assert 폭==0 and lengde_VERDI==0, 'remote cursor must be hidden'
                    peker_Skjult[0]=True
                    continue
                assert koding_VERDI == 0 and 가로+폭 <= 너비 and vertikal_plassere+lengde_VERDI <= 높이
                tegning_VERDI.paste(Image.frombytes('RGB', (폭, lengde_VERDI), EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 폭*lengde_VERDI*4), 'raw', 'BGRX'), (가로, vertikal_plassere))
                område_VERDI_9285603e += 폭*lengde_VERDI
            if område_VERDI_9285603e:
                assert område_VERDI_9285603e == 너비*높이, område_VERDI_9285603e
                return tegning_VERDI

    def sjekk_piksel(koordinat_VERDI, 색):
        tidsfrist_VERDI = time.monotonic()+10
        while True:
            tegning_VERDI = punktgrafikk_BILDE()
            if tegning_VERDI.getpixel(koordinat_VERDI) == 색: return tegning_VERDI
            if time.monotonic() > tidsfrist_VERDI: raise AssertionError((koordinat_VERDI, tegning_VERDI.getpixel(koordinat_VERDI), 색))

    def Upload_Filer(Navn, data): overføre_VERDI.storbinary('STOR '+Navn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+skalere_SMS+' RGB32').encode() in LOG_POST
        print('BOOT:', skalere_SMS, flush=True)
        ekstern_nummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_POST).group(1))
        ekstern_VERDI_28edcfa1 = socket.create_connection(('127.0.0.1', ekstern_nummer), timeout=20)
        assert EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 12) == b'RFB 003.008\n'; ekstern_VERDI_28edcfa1.sendall(b'RFB 003.008\n')
        assert 1 in EKSAKT_VERDI(ekstern_VERDI_28edcfa1, EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 1)[0]); ekstern_VERDI_28edcfa1.sendall(b'\x01')
        assert EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 4) == b'\0'*4; ekstern_VERDI_28edcfa1.sendall(b'\x01')
        opprinnelig_tilstand = EKSAKT_VERDI(ekstern_VERDI_28edcfa1, 24); assert struct.unpack('>HH', opprinnelig_tilstand[:4]) == (너비, 높이)
        EKSAKT_VERDI(ekstern_VERDI_28edcfa1, struct.unpack('>I', opprinnelig_tilstand[20:])[0])
        ekstern_VERDI_28edcfa1.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ekstern_VERDI_28edcfa1.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sjekk_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Hendelse,_ in velger_a916db4e.select(.02):
                    data=Hendelse.fileobj.read(65536)
                    if data:LOG_POST.extend(data)
        Vindu=[12,48,568,360]
        def bekrefte_skalere():
            spalte_VERDI,RAD_VERDI=(Vindu[2]-24)//8,(Vindu[3]-56)//16
            Tekst=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(spalte_VERDI,RAD_VERDI) in Tekst,Tekst
            # faktisk_data Vindu 테두리: 단지 Størrelse spørre_VERDI 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sjekk_piksel((Vindu[0],Vindu[1]),(32,80,144))
            tegning_VERDI=sjekk_piksel((Vindu[0]+Vindu[2]-1,Vindu[1]+Vindu[3]-1),(39,49,64))
            return tegning_VERDI
        def 모서리(방향):
            return (Vindu[0]+(3 if 방향 in (1,3) else Vindu[2]-4),Vindu[1]+(3 if 방향<=2 else Vindu[3]-4))
        def endre_størrelse_på_dra(방향,차이,Knapp=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sjekk_piksel(흰점,(255,255,255))
            가리키기(가,세,Knapp)
            끝가=max(0,min(너비-1,가+차이[0]));avslutte_en_samtale_vertikal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,avslutte_en_samtale_vertikal,Knapp);가리키기(끝가,avslutte_en_samtale_vertikal,0);숨고르기()
            if Knapp==1:
                VENSTRE_VERDI,위,폭,lengde_VERDI=Vindu;HØYRE_VERDI,아래=VENSTRE_VERDI+폭,위+lengde_VERDI
                if 방향 in (1,3):VENSTRE_VERDI=max(0,min(HØYRE_VERDI-360,VENSTRE_VERDI+끝가-가))
                else:HØYRE_VERDI=max(VENSTRE_VERDI+360,min(너비,HØYRE_VERDI+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+avslutte_en_samtale_vertikal-세))
                else:아래=max(위+216,min(높이,아래+avslutte_en_samtale_vertikal-세))
                Vindu[:]=[VENSTRE_VERDI,위,HØYRE_VERDI-VENSTRE_VERDI,아래-위]
        bekrefte_skalere();assert peker_Skjult[0]
        endre_størrelse_på_dra(4,(-100,-60),4);bekrefte_skalere() # HØYRE 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            endre_størrelse_på_dra(방향,차이);bekrefte_skalere()
        # inndata_VERDI 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        send_SMS("echo '"+긴글+"'");숨고르기()
        endre_størrelse_på_dra(4,(-1000,-1000));assert Vindu[2:]==[360,216]
        endre_størrelse_på_dra(4,(너비,높이))
        Kjør_2=send_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Kjør_2);bekrefte_skalere()
        # vi가 Rediger_VERDI 중에 skjermbilde 크기를 prøve_på_nytt_VERDI 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        overføre_VERDI=ftplib.FTP();overføre_VERDI.encoding='utf-8';overføre_VERDI.connect('127.0.0.1',portnummer,timeout=20);overføre_VERDI.login()
        기다리기(b'NORMAL',send_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',send_SMS('i미저장 한글 data\n'));숨고르기()
        endre_størrelse_på_dra(4,(-너비,-높이))
        # ANSI RAD_VERDI 이동에 새 RAD_VERDI 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Vindu[3]-56)//16)).encode() in LOG_POST[-4096:]
        send_SMS('작은 창에서도 이어 Skriv\n');숨고르기()
        endre_størrelse_på_dra(4,(너비,높이))
        send_SMS('큰 창에서도 이어 Skriv\n');숨고르기()
        klikk_knapp(0xff1b);klikk_knapp(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',send_SMS(':wq\n'))
        Innhold_VERDI=bytearray();overføre_VERDI.retrbinary('RETR 크기자료.txt',Innhold_VERDI.extend)
        assert Innhold_VERDI=='미저장 한글 data\n작은 창에서도 이어 Skriv\n큰 창에서도 이어 Skriv\n'.encode(),Innhold_VERDI
        bekrefte_skalere().save(str(KR_bane/(skalere_SMS+'-large.png')))
        # 두 번째 창은 standardverdi Størrelse, prøve_på_nytt_VERDI 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Kjør_2=len(LOG_POST);klikk_VERDI(70,16);기다리기(b'TERMINAL FOCUS 2',Kjør_2)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        Kjør_2=len(LOG_POST);klikk_VERDI(180,16);기다리기(b'TERMINAL FOCUS 1',Kjør_2);bekrefte_skalere()
        endre_størrelse_på_dra(4,(-너비,-높이));bekrefte_skalere().save(str(KR_bane/(skalere_SMS+'-small.png')))
        # Størrelse endre_VERDI TILBAKE_VERDI X 닫기도 새로운 HØYRE 가장자리를 사용한다.
        Kjør_2=len(LOG_POST);klikk_VERDI(Vindu[0]+Vindu[2]-20,Vindu[1]+15);기다리기(b'TERMINAL FOCUS 2',Kjør_2)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',skalere_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if overføre_VERDI:overføre_VERDI.close()
        if ekstern_VERDI_28edcfa1:ekstern_VERDI_28edcfa1.close()
        if Prosess_VERDI.poll() is None:
            Prosess_VERDI.terminate()
            try:Prosess_VERDI.wait(timeout=8)
            except subprocess.TimeoutExpired:Prosess_VERDI.kill();Prosess_VERDI.wait()
        velger_a916db4e.close();Prosess_VERDI.stdout.close();(KR_bane/(skalere_SMS+'.log')).write_bytes(LOG_POST)


def Kjør_2():
    KR_bane=speile_rot/'build/verification/resize';KR_bane.mkdir(parents=True,exist_ok=True)
    LOG_POST={'passed':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_bane);LOG_POST['resolutions'].append([너비,높이])
        LOG_POST.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_bane/'report.json').write_text(json.dumps(LOG_POST,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Kjør_2()
