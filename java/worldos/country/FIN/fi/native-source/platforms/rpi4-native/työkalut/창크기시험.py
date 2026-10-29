#!/usr/bin/env python3
"""todellinen_data QEMU/VNC에서 komentotulkki 모서리 vetää_ARVO·osoitin·동적 merkki_ARVO paikka_merkintä·muutos_ARVO Sisältö_ARVO 보존를 검사한다."""
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
from työpöytä_Näkymä import VERTAA_ARVO
from Suorita_komento import aloite_juuri


def 창크기시험(너비, 높이, KR_polku):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portin_numero = 임시.getsockname()[1]
    muuttaa_kokoa_SMS = '{}x{}'.format(너비, 높이)
    prosessi_ARVO = subprocess.Popen(['python3', str(aloite_juuri/'työkalut/Suorita_komento.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portin_numero), '--resolution', muuttaa_kokoa_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valitsin_a916db4e = selectors.DefaultSelector(); valitsin_a916db4e.register(prosessi_ARVO.stdout, selectors.EVENT_READ)
    LOG_TIETUE = bytearray(); etä_ARVO = None; Siirrä_ARVO = None; osoitin_Piilotettu=[False]

    def 기다리기(näyttää_ARVO, Suorita_2=0):
        määräaika_ARVO = time.monotonic() + 60
        while näyttää_ARVO not in LOG_TIETUE[Suorita_2:]:
            if time.monotonic() > määräaika_ARVO or prosessi_ARVO.poll() is not None or b'HALTED' in LOG_TIETUE or b'PANIC:' in LOG_TIETUE:
                raise AssertionError(LOG_TIETUE[Suorita_2:].decode('utf-8', 'replace'))
            for Tapahtuma, _ in valitsin_a916db4e.select(.1):
                data = Tapahtuma.fileobj.read(65536)
                if data: LOG_TIETUE.extend(data)
        return LOG_TIETUE[Suorita_2:].decode('utf-8', 'replace')

    def osoittaa_painike(symboli, 눌림=True): etä_ARVO.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symboli))

    def lähettää_tekstiviesti(teksti):
        Suorita_2 = len(LOG_TIETUE)
        for merkki_ARVO in teksti:
            symboli = 0xff0d if merkki_ARVO == '\n' else ord(merkki_ARVO) if ord(merkki_ARVO) < 256 else 0x1000000 | ord(merkki_ARVO)
            osoittaa_painike(symboli); osoittaa_painike(symboli, False)
        return Suorita_2

    def liittymä(teksti): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', lähettää_tekstiviesti(teksti+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, toimiala_toimi, 눌림): etä_ARVO.sendall(struct.pack('>BBHH', 5, 눌림, 가로, toimiala_toimi))

    def osoittaa_ARVO(가로, toimiala_toimi): 가리키기(가로, toimiala_toimi, 1); 가리키기(가로, toimiala_toimi, 0)

    def bittikartta_KUVA():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 todellinen_data 너비를 쓴다.
        etä_ARVO.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        piirustus_ARVO = Image.new('RGB', (너비, 높이)); alue_ARVO_9285603e = 0
        while True:
            종류 = VERTAA_ARVO(etä_ARVO, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                kesto_ARVO = struct.unpack('>I', VERTAA_ARVO(etä_ARVO, 7)[3:])[0]; VERTAA_ARVO(etä_ARVO, kesto_ARVO); continue
            assert 종류 == 0, 종류
            kohde_LASKE = struct.unpack('>H', VERTAA_ARVO(etä_ARVO, 3)[1:])[0]
            for _ in range(kohde_LASKE):
                가로, toimiala_toimi, 폭, kesto_ARVO, koodaus_ARVO = struct.unpack('>HHHHi', VERTAA_ARVO(etä_ARVO, 12))
                if koodaus_ARVO == -239:
                    assert 폭==0 and kesto_ARVO==0, 'remote cursor must be hidden'
                    osoitin_Piilotettu[0]=True
                    continue
                assert koodaus_ARVO == 0 and 가로+폭 <= 너비 and toimiala_toimi+kesto_ARVO <= 높이
                piirustus_ARVO.paste(Image.frombytes('RGB', (폭, kesto_ARVO), VERTAA_ARVO(etä_ARVO, 폭*kesto_ARVO*4), 'raw', 'BGRX'), (가로, toimiala_toimi))
                alue_ARVO_9285603e += 폭*kesto_ARVO
            if alue_ARVO_9285603e:
                assert alue_ARVO_9285603e == 너비*높이, alue_ARVO_9285603e
                return piirustus_ARVO

    def sekki_kuvapiste(koordinaatti_ARVO, 색):
        määräaika_ARVO = time.monotonic()+10
        while True:
            piirustus_ARVO = bittikartta_KUVA()
            if piirustus_ARVO.getpixel(koordinaatti_ARVO) == 색: return piirustus_ARVO
            if time.monotonic() > määräaika_ARVO: raise AssertionError((koordinaatti_ARVO, piirustus_ARVO.getpixel(koordinaatti_ARVO), 색))

    def Upload_Files(Nimi, data): Siirrä_ARVO.storbinary('STOR '+Nimi, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+muuttaa_kokoa_SMS+' RGB32').encode() in LOG_TIETUE
        print('BOOT:', muuttaa_kokoa_SMS, flush=True)
        etä_numero = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_TIETUE).group(1))
        etä_ARVO = socket.create_connection(('127.0.0.1', etä_numero), timeout=20)
        assert VERTAA_ARVO(etä_ARVO, 12) == b'RFB 003.008\n'; etä_ARVO.sendall(b'RFB 003.008\n')
        assert 1 in VERTAA_ARVO(etä_ARVO, VERTAA_ARVO(etä_ARVO, 1)[0]); etä_ARVO.sendall(b'\x01')
        assert VERTAA_ARVO(etä_ARVO, 4) == b'\0'*4; etä_ARVO.sendall(b'\x01')
        alkutila = VERTAA_ARVO(etä_ARVO, 24); assert struct.unpack('>HH', alkutila[:4]) == (너비, 높이)
        VERTAA_ARVO(etä_ARVO, struct.unpack('>I', alkutila[20:])[0])
        etä_ARVO.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        etä_ARVO.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sekki_kuvapiste((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Tapahtuma,_ in valitsin_a916db4e.select(.02):
                    data=Tapahtuma.fileobj.read(65536)
                    if data:LOG_TIETUE.extend(data)
        Ikkuna=[12,48,568,360]
        def tarkistaa_muuttaa_kokoa():
            SARAKE_ARVO,RIVI_ARVO=(Ikkuna[2]-24)//8,(Ikkuna[3]-56)//16
            teksti=liittymä('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(SARAKE_ARVO,RIVI_ARVO) in teksti,teksti
            # todellinen_data Ikkuna 테두리: 단지 Koko kysely_ARVO 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sekki_kuvapiste((Ikkuna[0],Ikkuna[1]),(32,80,144))
            piirustus_ARVO=sekki_kuvapiste((Ikkuna[0]+Ikkuna[2]-1,Ikkuna[1]+Ikkuna[3]-1),(39,49,64))
            return piirustus_ARVO
        def 모서리(방향):
            return (Ikkuna[0]+(3 if 방향 in (1,3) else Ikkuna[2]-4),Ikkuna[1]+(3 if 방향<=2 else Ikkuna[3]-4))
        def muuttaa_kokoa_vetää(방향,차이,painike=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sekki_kuvapiste(흰점,(255,255,255))
            가리키기(가,세,painike)
            끝가=max(0,min(너비-1,가+차이[0]));lopettaa_puhelu_toimiala=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,lopettaa_puhelu_toimiala,painike);가리키기(끝가,lopettaa_puhelu_toimiala,0);숨고르기()
            if painike==1:
                VASEN_ARVO,위,폭,kesto_ARVO=Ikkuna;OIKEA_ARVO,아래=VASEN_ARVO+폭,위+kesto_ARVO
                if 방향 in (1,3):VASEN_ARVO=max(0,min(OIKEA_ARVO-360,VASEN_ARVO+끝가-가))
                else:OIKEA_ARVO=max(VASEN_ARVO+360,min(너비,OIKEA_ARVO+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+lopettaa_puhelu_toimiala-세))
                else:아래=max(위+216,min(높이,아래+lopettaa_puhelu_toimiala-세))
                Ikkuna[:]=[VASEN_ARVO,위,OIKEA_ARVO-VASEN_ARVO,아래-위]
        tarkistaa_muuttaa_kokoa();assert osoitin_Piilotettu[0]
        muuttaa_kokoa_vetää(4,(-100,-60),4);tarkistaa_muuttaa_kokoa() # OIKEA 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            muuttaa_kokoa_vetää(방향,차이);tarkistaa_muuttaa_kokoa()
        # syöte_ARVO 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        lähettää_tekstiviesti("echo '"+긴글+"'");숨고르기()
        muuttaa_kokoa_vetää(4,(-1000,-1000));assert Ikkuna[2:]==[360,216]
        muuttaa_kokoa_vetää(4,(너비,높이))
        Suorita_2=lähettää_tekstiviesti('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Suorita_2);tarkistaa_muuttaa_kokoa()
        # vi가 muutos_ARVO 중에 화면 크기를 yrittää_uudelleen_ARVO 읽고, 저장하지 않은 한글도 유지한다.
        liittymä('ftpd start')
        Siirrä_ARVO=ftplib.FTP();Siirrä_ARVO.encoding='utf-8';Siirrä_ARVO.connect('127.0.0.1',portin_numero,timeout=20);Siirrä_ARVO.login()
        기다리기(b'NORMAL',lähettää_tekstiviesti('vi /크기자료.txt\n'))
        기다리기(b'INSERT',lähettää_tekstiviesti('i미저장 한글 data\n'));숨고르기()
        muuttaa_kokoa_vetää(4,(-너비,-높이))
        # ANSI RIVI_ARVO 이동에 새 RIVI_ARVO 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Ikkuna[3]-56)//16)).encode() in LOG_TIETUE[-4096:]
        lähettää_tekstiviesti('작은 창에서도 이어 Kirjoitus\n');숨고르기()
        muuttaa_kokoa_vetää(4,(너비,높이))
        lähettää_tekstiviesti('큰 창에서도 이어 Kirjoitus\n');숨고르기()
        osoittaa_painike(0xff1b);osoittaa_painike(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',lähettää_tekstiviesti(':wq\n'))
        Sisältö_ARVO=bytearray();Siirrä_ARVO.retrbinary('RETR 크기자료.txt',Sisältö_ARVO.extend)
        assert Sisältö_ARVO=='미저장 한글 data\n작은 창에서도 이어 Kirjoitus\n큰 창에서도 이어 Kirjoitus\n'.encode(),Sisältö_ARVO
        tarkistaa_muuttaa_kokoa().save(str(KR_polku/(muuttaa_kokoa_SMS+'-large.png')))
        # 두 번째 창은 oletusarvo Koko, yrittää_uudelleen_ARVO 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Suorita_2=len(LOG_TIETUE);osoittaa_ARVO(70,16);기다리기(b'TERMINAL FOCUS 2',Suorita_2)
        assert 'TERMINAL SIZE 68x19' in liittymä('terminal size')
        Suorita_2=len(LOG_TIETUE);osoittaa_ARVO(180,16);기다리기(b'TERMINAL FOCUS 1',Suorita_2);tarkistaa_muuttaa_kokoa()
        muuttaa_kokoa_vetää(4,(-너비,-높이));tarkistaa_muuttaa_kokoa().save(str(KR_polku/(muuttaa_kokoa_SMS+'-small.png')))
        # Koko muuttaa_ARVO BACK_ARVO X 닫기도 새로운 OIKEA 가장자리를 사용한다.
        Suorita_2=len(LOG_TIETUE);osoittaa_ARVO(Ikkuna[0]+Ikkuna[2]-20,Ikkuna[1]+15);기다리기(b'TERMINAL FOCUS 2',Suorita_2)
        assert 'RESIZE CLOSED' in liittymä('echo RESIZE CLOSED')
        print('PASS:',muuttaa_kokoa_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Siirrä_ARVO:Siirrä_ARVO.close()
        if etä_ARVO:etä_ARVO.close()
        if prosessi_ARVO.poll() is None:
            prosessi_ARVO.terminate()
            try:prosessi_ARVO.wait(timeout=8)
            except subprocess.TimeoutExpired:prosessi_ARVO.kill();prosessi_ARVO.wait()
        valitsin_a916db4e.close();prosessi_ARVO.stdout.close();(KR_polku/(muuttaa_kokoa_SMS+'.log')).write_bytes(LOG_TIETUE)


def Suorita_2():
    KR_polku=aloite_juuri/'build/verification/resize';KR_polku.mkdir(parents=True,exist_ok=True)
    LOG_TIETUE={'passed':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_polku);LOG_TIETUE['resolutions'].append([너비,높이])
        LOG_TIETUE.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_polku/'report.json').write_text(json.dumps(LOG_TIETUE,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Suorita_2()
