#!/usr/bin/env python3
"""tényleges_adat QEMU/VNC에서 Terminál 모서리 húz_ÉRTÉK·mutató·동적 karakter_ÉRTÉK tárolóhely_bejegyzés·szerkeszt_ÉRTÉK Tartalom_ÉRTÉK 보존를 검사한다."""
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
from Asztal_Nézet import AZONOS_ÉRTÉK
from végrehajt_parancs import teendő_gyök


def 창크기시험(너비, 높이, KR_útvonal):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portszám = 임시.getsockname()[1]
    méretez_SMS = '{}x{}'.format(너비, 높이)
    folyamat_ÉRTÉK = subprocess.Popen(['python3', str(teendő_gyök/'Eszközök/végrehajt_parancs.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portszám), '--resolution', méretez_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    szelektor_a916db4e = selectors.DefaultSelector(); szelektor_a916db4e.register(folyamat_ÉRTÉK.stdout, selectors.EVENT_READ)
    LOG_REKORD = bytearray(); távoli_ÉRTÉK = None; átvisz_ÉRTÉK = None; mutató_Rejtett=[False]

    def 기다리기(bemutató_ÉRTÉK, Futtatás=0):
        határidő_ÉRTÉK = time.monotonic() + 60
        while bemutató_ÉRTÉK not in LOG_REKORD[Futtatás:]:
            if time.monotonic() > határidő_ÉRTÉK or folyamat_ÉRTÉK.poll() is not None or b'HALTED' in LOG_REKORD or b'PANIC:' in LOG_REKORD:
                raise AssertionError(LOG_REKORD[Futtatás:].decode('utf-8', 'replace'))
            for Esemény, _ in szelektor_a916db4e.select(.1):
                adat = Esemény.fileobj.read(65536)
                if adat: LOG_REKORD.extend(adat)
        return LOG_REKORD[Futtatás:].decode('utf-8', 'replace')

    def kattint_gomb(szimbólum, 눌림=True): távoli_ÉRTÉK.sendall(struct.pack('>BBHI', 4, int(눌림), 0, szimbólum))

    def SMS_küldése(Szöveg):
        Futtatás = len(LOG_REKORD)
        for karakter_ÉRTÉK in Szöveg:
            szimbólum = 0xff0d if karakter_ÉRTÉK == '\n' else ord(karakter_ÉRTÉK) if ord(karakter_ÉRTÉK) < 256 else 0x1000000 | ord(karakter_ÉRTÉK)
            kattint_gomb(szimbólum); kattint_gomb(szimbólum, False)
        return Futtatás

    def felület(Szöveg): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_küldése(Szöveg+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, szektor_pozíció, 눌림): távoli_ÉRTÉK.sendall(struct.pack('>BBHH', 5, 눌림, 가로, szektor_pozíció))

    def kattint_ÉRTÉK(가로, szektor_pozíció): 가리키기(가로, szektor_pozíció, 1); 가리키기(가로, szektor_pozíció, 0)

    def bitkép_KÉP():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tényleges_adat 너비를 쓴다.
        távoli_ÉRTÉK.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        rajz_ÉRTÉK = Image.new('RGB', (너비, 높이)); terület_ÉRTÉK_9285603e = 0
        while True:
            Altípus_ÉRTÉK = AZONOS_ÉRTÉK(távoli_ÉRTÉK, 1)[0]
            if Altípus_ÉRTÉK == 2: continue
            if Altípus_ÉRTÉK == 3:
                hossz_ÉRTÉK = struct.unpack('>I', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 7)[3:])[0]; AZONOS_ÉRTÉK(távoli_ÉRTÉK, hossz_ÉRTÉK); continue
            assert Altípus_ÉRTÉK == 0, Altípus_ÉRTÉK
            cikk_DARAB = struct.unpack('>H', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 3)[1:])[0]
            for _ in range(cikk_DARAB):
                가로, szektor_pozíció, 폭, hossz_ÉRTÉK, kódolás_ÉRTÉK = struct.unpack('>HHHHi', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 12))
                if kódolás_ÉRTÉK == -239:
                    assert 폭==0 and hossz_ÉRTÉK==0, 'remote cursor must be hidden'
                    mutató_Rejtett[0]=True
                    continue
                assert kódolás_ÉRTÉK == 0 and 가로+폭 <= 너비 and szektor_pozíció+hossz_ÉRTÉK <= 높이
                rajz_ÉRTÉK.paste(Image.frombytes('RGB', (폭, hossz_ÉRTÉK), AZONOS_ÉRTÉK(távoli_ÉRTÉK, 폭*hossz_ÉRTÉK*4), 'raw', 'BGRX'), (가로, szektor_pozíció))
                terület_ÉRTÉK_9285603e += 폭*hossz_ÉRTÉK
            if terület_ÉRTÉK_9285603e:
                assert terület_ÉRTÉK_9285603e == 너비*높이, terület_ÉRTÉK_9285603e
                return rajz_ÉRTÉK

    def csekk_képpont(koordináta_ÉRTÉK, 색):
        határidő_ÉRTÉK = time.monotonic()+10
        while True:
            rajz_ÉRTÉK = bitkép_KÉP()
            if rajz_ÉRTÉK.getpixel(koordináta_ÉRTÉK) == 색: return rajz_ÉRTÉK
            if time.monotonic() > határidő_ÉRTÉK: raise AssertionError((koordináta_ÉRTÉK, rajz_ÉRTÉK.getpixel(koordináta_ÉRTÉK), 색))

    def feltölt_Files(Név, adat): átvisz_ÉRTÉK.storbinary('STOR '+Név, io.BytesIO(adat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+méretez_SMS+' RGB32').encode() in LOG_REKORD
        print('BOOT:', méretez_SMS, flush=True)
        távoli_szám = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_REKORD).group(1))
        távoli_ÉRTÉK = socket.create_connection(('127.0.0.1', távoli_szám), timeout=20)
        assert AZONOS_ÉRTÉK(távoli_ÉRTÉK, 12) == b'RFB 003.008\n'; távoli_ÉRTÉK.sendall(b'RFB 003.008\n')
        assert 1 in AZONOS_ÉRTÉK(távoli_ÉRTÉK, AZONOS_ÉRTÉK(távoli_ÉRTÉK, 1)[0]); távoli_ÉRTÉK.sendall(b'\x01')
        assert AZONOS_ÉRTÉK(távoli_ÉRTÉK, 4) == b'\0'*4; távoli_ÉRTÉK.sendall(b'\x01')
        kiinduló_állapot = AZONOS_ÉRTÉK(távoli_ÉRTÉK, 24); assert struct.unpack('>HH', kiinduló_állapot[:4]) == (너비, 높이)
        AZONOS_ÉRTÉK(távoli_ÉRTÉK, struct.unpack('>I', kiinduló_állapot[20:])[0])
        távoli_ÉRTÉK.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        távoli_ÉRTÉK.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        csekk_képpont((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Esemény,_ in szelektor_a916db4e.select(.02):
                    adat=Esemény.fileobj.read(65536)
                    if adat:LOG_REKORD.extend(adat)
        Ablak=[12,48,568,360]
        def igazol_méretez():
            OSZLOP_ÉRTÉK,SOR_ÉRTÉK=(Ablak[2]-24)//8,(Ablak[3]-56)//16
            Szöveg=felület('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(OSZLOP_ÉRTÉK,SOR_ÉRTÉK) in Szöveg,Szöveg
            # tényleges_adat Ablak 테두리: 단지 Méret lekérdez_ÉRTÉK 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            csekk_képpont((Ablak[0],Ablak[1]),(32,80,144))
            rajz_ÉRTÉK=csekk_képpont((Ablak[0]+Ablak[2]-1,Ablak[1]+Ablak[3]-1),(39,49,64))
            return rajz_ÉRTÉK
        def 모서리(방향):
            return (Ablak[0]+(3 if 방향 in (1,3) else Ablak[2]-4),Ablak[1]+(3 if 방향<=2 else Ablak[3]-4))
        def méretez_húz(방향,차이,gomb=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            csekk_képpont(흰점,(255,255,255))
            가리키기(가,세,gomb)
            끝가=max(0,min(너비-1,가+차이[0]));megszüntet_szektor=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,megszüntet_szektor,gomb);가리키기(끝가,megszüntet_szektor,0);숨고르기()
            if gomb==1:
                BAL_ÉRTÉK,위,폭,hossz_ÉRTÉK=Ablak;jog_ÉRTÉK,아래=BAL_ÉRTÉK+폭,위+hossz_ÉRTÉK
                if 방향 in (1,3):BAL_ÉRTÉK=max(0,min(jog_ÉRTÉK-360,BAL_ÉRTÉK+끝가-가))
                else:jog_ÉRTÉK=max(BAL_ÉRTÉK+360,min(너비,jog_ÉRTÉK+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+megszüntet_szektor-세))
                else:아래=max(위+216,min(높이,아래+megszüntet_szektor-세))
                Ablak[:]=[BAL_ÉRTÉK,위,jog_ÉRTÉK-BAL_ÉRTÉK,아래-위]
        igazol_méretez();assert mutató_Rejtett[0]
        méretez_húz(4,(-100,-60),4);igazol_méretez() # jog 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            méretez_húz(방향,차이);igazol_méretez()
        # bevitel_ÉRTÉK 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_küldése("echo '"+긴글+"'");숨고르기()
        méretez_húz(4,(-1000,-1000));assert Ablak[2:]==[360,216]
        méretez_húz(4,(너비,높이))
        Futtatás=SMS_küldése('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Futtatás);igazol_méretez()
        # vi가 szerkeszt_ÉRTÉK 중에 화면 크기를 újrapróbál_ÉRTÉK 읽고, 저장하지 않은 한글도 유지한다.
        felület('ftpd start')
        átvisz_ÉRTÉK=ftplib.FTP();átvisz_ÉRTÉK.encoding='utf-8';átvisz_ÉRTÉK.connect('127.0.0.1',portszám,timeout=20);átvisz_ÉRTÉK.login()
        기다리기(b'NORMAL',SMS_küldése('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_küldése('i미저장 한글 adat\n'));숨고르기()
        méretez_húz(4,(-너비,-높이))
        # ANSI SOR_ÉRTÉK 이동에 새 SOR_ÉRTÉK 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Ablak[3]-56)//16)).encode() in LOG_REKORD[-4096:]
        SMS_küldése('작은 창에서도 이어 Írás\n');숨고르기()
        méretez_húz(4,(너비,높이))
        SMS_küldése('큰 창에서도 이어 Írás\n');숨고르기()
        kattint_gomb(0xff1b);kattint_gomb(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_küldése(':wq\n'))
        Tartalom_ÉRTÉK=bytearray();átvisz_ÉRTÉK.retrbinary('RETR 크기자료.txt',Tartalom_ÉRTÉK.extend)
        assert Tartalom_ÉRTÉK=='미저장 한글 adat\n작은 창에서도 이어 Írás\n큰 창에서도 이어 Írás\n'.encode(),Tartalom_ÉRTÉK
        igazol_méretez().save(str(KR_útvonal/(méretez_SMS+'-large.png')))
        # 두 번째 창은 alapértelmezett_érték Méret, újrapróbál_ÉRTÉK 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Futtatás=len(LOG_REKORD);kattint_ÉRTÉK(70,16);기다리기(b'TERMINAL FOCUS 2',Futtatás)
        assert 'TERMINAL SIZE 68x19' in felület('terminal size')
        Futtatás=len(LOG_REKORD);kattint_ÉRTÉK(180,16);기다리기(b'TERMINAL FOCUS 1',Futtatás);igazol_méretez()
        méretez_húz(4,(-너비,-높이));igazol_méretez().save(str(KR_útvonal/(méretez_SMS+'-small.png')))
        # Méret módosítás_ÉRTÉK BACK_ÉRTÉK X 닫기도 새로운 jog 가장자리를 사용한다.
        Futtatás=len(LOG_REKORD);kattint_ÉRTÉK(Ablak[0]+Ablak[2]-20,Ablak[1]+15);기다리기(b'TERMINAL FOCUS 2',Futtatás)
        assert 'RESIZE CLOSED' in felület('echo RESIZE CLOSED')
        print('PASS:',méretez_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if átvisz_ÉRTÉK:átvisz_ÉRTÉK.close()
        if távoli_ÉRTÉK:távoli_ÉRTÉK.close()
        if folyamat_ÉRTÉK.poll() is None:
            folyamat_ÉRTÉK.terminate()
            try:folyamat_ÉRTÉK.wait(timeout=8)
            except subprocess.TimeoutExpired:folyamat_ÉRTÉK.kill();folyamat_ÉRTÉK.wait()
        szelektor_a916db4e.close();folyamat_ÉRTÉK.stdout.close();(KR_útvonal/(méretez_SMS+'.log')).write_bytes(LOG_REKORD)


def Futtatás():
    KR_útvonal=teendő_gyök/'build/verification/resize';KR_útvonal.mkdir(parents=True,exist_ok=True)
    LOG_REKORD={'passed':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_útvonal);LOG_REKORD['resolutions'].append([너비,높이])
        LOG_REKORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_útvonal/'report.json').write_text(json.dumps(LOG_REKORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Futtatás()
