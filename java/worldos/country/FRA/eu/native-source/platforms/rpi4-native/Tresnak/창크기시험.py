#!/usr/bin/env python3
"""benetako_datuak QEMU/VNC에서 Terminala 모서리 arrastatu_balio·erakusle·동적 karaktere_balio 칸·edizio_balio eduki_balio 보존를 검사한다."""
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
from mahaigain_ikusi import BERDIN_balio
from exekutatu_komando import Project_erro


def 창크기시험(너비, 높이, neurria_bide_izen):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ataka_zenbaki = 임시.getsockname()[1]
    크기글 = '{}x{}'.format(너비, 높이)
    prozesu_balio = subprocess.Popen(['python3', str(Project_erro/'Tresnak/exekutatu_komando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ataka_zenbaki), '--resolution', 크기글], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(prozesu_balio.stdout, selectors.EVENT_READ)
    LOG_marka = bytearray(); urruneko_balio = None; transferitu_balio = None; erakusle_Ezkutua=[False]

    def 기다리기(erakutsi_balio, Exekutatu_2=0):
        마감 = time.monotonic() + 60
        while erakutsi_balio not in LOG_marka[Exekutatu_2:]:
            if time.monotonic() > 마감 or prozesu_balio.poll() is not None or b'HALTED' in LOG_marka or b'PANIC:' in LOG_marka:
                raise AssertionError(LOG_marka[Exekutatu_2:].decode('utf-8', 'replace'))
            for Gertaera, _ in 선택기.select(.1):
                datuak = Gertaera.fileobj.read(65536)
                if datuak: LOG_marka.extend(datuak)
        return LOG_marka[Exekutatu_2:].decode('utf-8', 'replace')

    def klik_botoi(ikur, 눌림=True): urruneko_balio.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ikur))

    def bidali_SMSa(Testua):
        Exekutatu_2 = len(LOG_marka)
        for karaktere_balio in Testua:
            ikur = 0xff0d if karaktere_balio == '\n' else ord(karaktere_balio) if ord(karaktere_balio) < 256 else 0x1000000 | ord(karaktere_balio)
            klik_botoi(ikur); klik_botoi(ikur, False)
        return Exekutatu_2

    def shell(Testua): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', bidali_SMSa(Testua+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Bertikala_kargu, 눌림): urruneko_balio.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Bertikala_kargu))

    def klik_balio(가로, Bertikala_kargu): 가리키기(가로, Bertikala_kargu, 1); 가리키기(가로, Bertikala_kargu, 0)

    def bit_mapa_irudi():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 benetako_datuak 너비를 쓴다.
        urruneko_balio.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        그림 = Image.new('RGB', (너비, 높이)); area_balio = 0
        while True:
            종류 = BERDIN_balio(urruneko_balio, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                luzera_balio = struct.unpack('>I', BERDIN_balio(urruneko_balio, 7)[3:])[0]; BERDIN_balio(urruneko_balio, luzera_balio); continue
            assert 종류 == 0, 종류
            elementu_ZENBATU = struct.unpack('>H', BERDIN_balio(urruneko_balio, 3)[1:])[0]
            for _ in range(elementu_ZENBATU):
                가로, Bertikala_kargu, 폭, luzera_balio, kodeketa_balio = struct.unpack('>HHHHi', BERDIN_balio(urruneko_balio, 12))
                if kodeketa_balio == -239:
                    assert 폭==0 and luzera_balio==0, 'remote cursor must be hidden'
                    erakusle_Ezkutua[0]=True
                    continue
                assert kodeketa_balio == 0 and 가로+폭 <= 너비 and Bertikala_kargu+luzera_balio <= 높이
                그림.paste(Image.frombytes('RGB', (폭, luzera_balio), BERDIN_balio(urruneko_balio, 폭*luzera_balio*4), 'raw', 'BGRX'), (가로, Bertikala_kargu))
                area_balio += 폭*luzera_balio
            if area_balio:
                assert area_balio == 너비*높이, area_balio
                return 그림

    def txeke_pixel(koordenatu_balio, 색):
        마감 = time.monotonic()+10
        while True:
            그림 = bit_mapa_irudi()
            if 그림.getpixel(koordenatu_balio) == 색: return 그림
            if time.monotonic() > 마감: raise AssertionError((koordenatu_balio, 그림.getpixel(koordenatu_balio), 색))

    def Upload_Fitxategiak(Izena, datuak): transferitu_balio.storbinary('STOR '+Izena, io.BytesIO(datuak))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+크기글+' RGB32').encode() in LOG_marka
        print('BOOT:', 크기글, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_marka).group(1))
        urruneko_balio = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert BERDIN_balio(urruneko_balio, 12) == b'RFB 003.008\n'; urruneko_balio.sendall(b'RFB 003.008\n')
        assert 1 in BERDIN_balio(urruneko_balio, BERDIN_balio(urruneko_balio, 1)[0]); urruneko_balio.sendall(b'\x01')
        assert BERDIN_balio(urruneko_balio, 4) == b'\0'*4; urruneko_balio.sendall(b'\x01')
        초기 = BERDIN_balio(urruneko_balio, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        BERDIN_balio(urruneko_balio, struct.unpack('>I', 초기[20:])[0])
        urruneko_balio.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        urruneko_balio.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        txeke_pixel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Gertaera,_ in 선택기.select(.02):
                    datuak=Gertaera.fileobj.read(65536)
                    if datuak:LOG_marka.extend(datuak)
        Leihoa=[12,48,568,360]
        def 크기확인():
            zutabe_balio,ERRENKADA_balio=(Leihoa[2]-24)//8,(Leihoa[3]-56)//16
            Testua=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(zutabe_balio,ERRENKADA_balio) in Testua,Testua
            # benetako_datuak Leihoa 테두리: 단지 Tamaina kontsulta_balio 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            txeke_pixel((Leihoa[0],Leihoa[1]),(32,80,144))
            그림=txeke_pixel((Leihoa[0]+Leihoa[2]-1,Leihoa[1]+Leihoa[3]-1),(39,49,64))
            return 그림
        def 모서리(방향):
            return (Leihoa[0]+(3 if 방향 in (1,3) else Leihoa[2]-4),Leihoa[1]+(3 if 방향<=2 else Leihoa[3]-4))
        def aldatu_tamaina_arrastatu(방향,차이,botoia=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            txeke_pixel(흰점,(255,255,255))
            가리키기(가,세,botoia)
            끝가=max(0,min(너비-1,가+차이[0]));amaitu_Bertikala=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,amaitu_Bertikala,botoia);가리키기(끝가,amaitu_Bertikala,0);숨고르기()
            if botoia==1:
                EZKER_balio,위,폭,luzera_balio=Leihoa;ESKUIN_balio,아래=EZKER_balio+폭,위+luzera_balio
                if 방향 in (1,3):EZKER_balio=max(0,min(ESKUIN_balio-360,EZKER_balio+끝가-가))
                else:ESKUIN_balio=max(EZKER_balio+360,min(너비,ESKUIN_balio+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+amaitu_Bertikala-세))
                else:아래=max(위+216,min(높이,아래+amaitu_Bertikala-세))
                Leihoa[:]=[EZKER_balio,위,ESKUIN_balio-EZKER_balio,아래-위]
        크기확인();assert erakusle_Ezkutua[0]
        aldatu_tamaina_arrastatu(4,(-100,-60),4);크기확인() # ESKUIN 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            aldatu_tamaina_arrastatu(방향,차이);크기확인()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        bidali_SMSa("echo '"+긴글+"'");숨고르기()
        aldatu_tamaina_arrastatu(4,(-1000,-1000));assert Leihoa[2:]==[360,216]
        aldatu_tamaina_arrastatu(4,(너비,높이))
        Exekutatu_2=bidali_SMSa('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Exekutatu_2);크기확인()
        # vi가 edizio_balio 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        transferitu_balio=ftplib.FTP();transferitu_balio.encoding='utf-8';transferitu_balio.connect('127.0.0.1',ataka_zenbaki,timeout=20);transferitu_balio.login()
        기다리기(b'NORMAL',bidali_SMSa('vi /크기자료.txt\n'))
        기다리기(b'INSERT',bidali_SMSa('i미저장 한글 datuak\n'));숨고르기()
        aldatu_tamaina_arrastatu(4,(-너비,-높이))
        # ANSI ERRENKADA_balio 이동에 새 ERRENKADA_balio 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Leihoa[3]-56)//16)).encode() in LOG_marka[-4096:]
        bidali_SMSa('작은 창에서도 이어 Idatzi\n');숨고르기()
        aldatu_tamaina_arrastatu(4,(너비,높이))
        bidali_SMSa('큰 창에서도 이어 Idatzi\n');숨고르기()
        klik_botoi(0xff1b);klik_botoi(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',bidali_SMSa(':wq\n'))
        eduki_balio=bytearray();transferitu_balio.retrbinary('RETR 크기자료.txt',eduki_balio.extend)
        assert eduki_balio=='미저장 한글 datuak\n작은 창에서도 이어 Idatzi\n큰 창에서도 이어 Idatzi\n'.encode(),eduki_balio
        크기확인().save(str(neurria_bide_izen/(크기글+'-large.png')))
        # 두 번째 창은 balio_lehenetsi Tamaina, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Exekutatu_2=len(LOG_marka);klik_balio(70,16);기다리기(b'TERMINAL FOCUS 2',Exekutatu_2)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        Exekutatu_2=len(LOG_marka);klik_balio(180,16);기다리기(b'TERMINAL FOCUS 1',Exekutatu_2);크기확인()
        aldatu_tamaina_arrastatu(4,(-너비,-높이));크기확인().save(str(neurria_bide_izen/(크기글+'-small.png')))
        # Tamaina aldatu_balio ATZERA_balio X 닫기도 새로운 ESKUIN 가장자리를 사용한다.
        Exekutatu_2=len(LOG_marka);klik_balio(Leihoa[0]+Leihoa[2]-20,Leihoa[1]+15);기다리기(b'TERMINAL FOCUS 2',Exekutatu_2)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',크기글,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if transferitu_balio:transferitu_balio.close()
        if urruneko_balio:urruneko_balio.close()
        if prozesu_balio.poll() is None:
            prozesu_balio.terminate()
            try:prozesu_balio.wait(timeout=8)
            except subprocess.TimeoutExpired:prozesu_balio.kill();prozesu_balio.wait()
        선택기.close();prozesu_balio.stdout.close();(neurria_bide_izen/(크기글+'.log')).write_bytes(LOG_marka)


def Exekutatu_2():
    neurria_bide_izen=Project_erro/'build/verification/resize';neurria_bide_izen.mkdir(parents=True,exist_ok=True)
    LOG_marka={'passed':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,neurria_bide_izen);LOG_marka['resolutions'].append([너비,높이])
        LOG_marka.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(neurria_bide_izen/'report.json').write_text(json.dumps(LOG_marka,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Exekutatu_2()
