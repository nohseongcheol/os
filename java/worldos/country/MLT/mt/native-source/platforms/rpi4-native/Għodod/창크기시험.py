#!/usr/bin/env python3
"""attwali_data QEMU/VNC에서 Terminal 모서리 dreggja_VALUE·pointer·동적 karattru_VALUE slott_entrata·editja_VALUE Kontenut_VALUE 보존를 검사한다."""
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
from desktop_wera import EXACT_VALUE
from eżegwixxa_kmand import pprojetta_għerq


def 창크기시험(너비, 높이, miżura_mogħdija):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    daqqas_SMS = '{}x{}'.format(너비, 높이)
    Proċess_VALUE = subprocess.Popen(['python3', str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', daqqas_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettur_a916db4e = selectors.DefaultSelector(); selettur_a916db4e.register(Proċess_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); mill_bogħod_VALUE = None; trasferiment_VALUE = None; pointer_moħbi=[False]

    def 기다리기(wera_VALUE_487749b8, serje=0):
        마감 = time.monotonic() + 60
        while wera_VALUE_487749b8 not in LOG_RECORD[serje:]:
            if time.monotonic() > 마감 or Proċess_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[serje:].decode('utf-8', 'replace'))
            for avveniment, _ in selettur_a916db4e.select(.1):
                data = avveniment.fileobj.read(65536)
                if data: LOG_RECORD.extend(data)
        return LOG_RECORD[serje:].decode('utf-8', 'replace')

    def klikkja_buttuna(simbolu, 눌림=True): mill_bogħod_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolu))

    def ibgħat_SMS(SMS):
        serje = len(LOG_RECORD)
        for karattru_VALUE in SMS:
            simbolu = 0xff0d if karattru_VALUE == '\n' else ord(karattru_VALUE) if ord(karattru_VALUE) < 256 else 0x1000000 | ord(karattru_VALUE)
            klikkja_buttuna(simbolu); klikkja_buttuna(simbolu, False)
        return serje

    def shell(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ibgħat_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikali_pożizzjoni, 눌림): mill_bogħod_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikali_pożizzjoni))

    def klikkja_VALUE(가로, Vertikali_pożizzjoni): 가리키기(가로, Vertikali_pożizzjoni, 1); 가리키기(가로, Vertikali_pożizzjoni, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 attwali_data 너비를 쓴다.
        mill_bogħod_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tpinġija_VALUE = Image.new('RGB', (너비, 높이)); żona_VALUE = 0
        while True:
            종류 = EXACT_VALUE(mill_bogħod_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                tul_VALUE = struct.unpack('>I', EXACT_VALUE(mill_bogħod_VALUE, 7)[3:])[0]; EXACT_VALUE(mill_bogħod_VALUE, tul_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(mill_bogħod_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Vertikali_pożizzjoni, 폭, tul_VALUE, kodifikar_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(mill_bogħod_VALUE, 12))
                if kodifikar_VALUE == -239:
                    assert 폭==0 and tul_VALUE==0, 'remote cursor must be hidden'
                    pointer_moħbi[0]=True
                    continue
                assert kodifikar_VALUE == 0 and 가로+폭 <= 너비 and Vertikali_pożizzjoni+tul_VALUE <= 높이
                tpinġija_VALUE.paste(Image.frombytes('RGB', (폭, tul_VALUE), EXACT_VALUE(mill_bogħod_VALUE, 폭*tul_VALUE*4), 'raw', 'BGRX'), (가로, Vertikali_pożizzjoni))
                żona_VALUE += 폭*tul_VALUE
            if żona_VALUE:
                assert żona_VALUE == 너비*높이, żona_VALUE
                return tpinġija_VALUE

    def ċekk_pel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            tpinġija_VALUE = bitmap_IMAGE()
            if tpinġija_VALUE.getpixel(koordinat_VALUE) == 색: return tpinġija_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, tpinġija_VALUE.getpixel(koordinat_VALUE), 색))

    def tella_Fajls(isem, data): trasferiment_VALUE.storbinary('STOR '+isem, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+daqqas_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', daqqas_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        mill_bogħod_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(mill_bogħod_VALUE, 12) == b'RFB 003.008\n'; mill_bogħod_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(mill_bogħod_VALUE, EXACT_VALUE(mill_bogħod_VALUE, 1)[0]); mill_bogħod_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(mill_bogħod_VALUE, 4) == b'\0'*4; mill_bogħod_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(mill_bogħod_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(mill_bogħod_VALUE, struct.unpack('>I', 초기[20:])[0])
        mill_bogħod_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        mill_bogħod_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ċekk_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for avveniment,_ in selettur_a916db4e.select(.02):
                    data=avveniment.fileobj.read(65536)
                    if data:LOG_RECORD.extend(data)
        tieqa=[12,48,568,360]
        def vverifika_daqqas():
            COLUMN_VALUE,ROW_VALUE=(tieqa[2]-24)//8,(tieqa[3]-56)//16
            SMS=shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in SMS,SMS
            # attwali_data tieqa 테두리: 단지 daqqas query_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ċekk_pel((tieqa[0],tieqa[1]),(32,80,144))
            tpinġija_VALUE=ċekk_pel((tieqa[0]+tieqa[2]-1,tieqa[1]+tieqa[3]-1),(39,49,64))
            return tpinġija_VALUE
        def 모서리(방향):
            return (tieqa[0]+(3 if 방향 in (1,3) else tieqa[2]-4),tieqa[1]+(3 if 방향<=2 else tieqa[3]-4))
        def rridimensjona_dreggja(방향,차이,buttuna=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ċekk_pel(흰점,(255,255,255))
            가리키기(가,세,buttuna)
            끝가=max(0,min(너비-1,가+차이[0]));ttermina_Vertikali=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ttermina_Vertikali,buttuna);가리키기(끝가,ttermina_Vertikali,0);숨고르기()
            if buttuna==1:
                LEFT_VALUE,위,폭,tul_VALUE=tieqa;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+tul_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ttermina_Vertikali-세))
                else:아래=max(위+216,min(높이,아래+ttermina_Vertikali-세))
                tieqa[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        vverifika_daqqas();assert pointer_moħbi[0]
        rridimensjona_dreggja(4,(-100,-60),4);vverifika_daqqas() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            rridimensjona_dreggja(방향,차이);vverifika_daqqas()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ibgħat_SMS("echo '"+긴글+"'");숨고르기()
        rridimensjona_dreggja(4,(-1000,-1000));assert tieqa[2:]==[360,216]
        rridimensjona_dreggja(4,(너비,높이))
        serje=ibgħat_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),serje);vverifika_daqqas()
        # vi가 editja_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        shell('ftpd start')
        trasferiment_VALUE=ftplib.FTP();trasferiment_VALUE.encoding='utf-8';trasferiment_VALUE.connect('127.0.0.1',접속번호,timeout=20);trasferiment_VALUE.login()
        기다리기(b'NORMAL',ibgħat_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ibgħat_SMS('i미저장 한글 data\n'));숨고르기()
        rridimensjona_dreggja(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((tieqa[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        ibgħat_SMS('작은 창에서도 이어 kiteb\n');숨고르기()
        rridimensjona_dreggja(4,(너비,높이))
        ibgħat_SMS('큰 창에서도 이어 kiteb\n');숨고르기()
        klikkja_buttuna(0xff1b);klikkja_buttuna(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ibgħat_SMS(':wq\n'))
        Kontenut_VALUE=bytearray();trasferiment_VALUE.retrbinary('RETR 크기자료.txt',Kontenut_VALUE.extend)
        assert Kontenut_VALUE=='미저장 한글 data\n작은 창에서도 이어 kiteb\n큰 창에서도 이어 kiteb\n'.encode(),Kontenut_VALUE
        vverifika_daqqas().save(str(miżura_mogħdija/(daqqas_SMS+'-large.png')))
        # 두 번째 창은 valur_default daqqas, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        serje=len(LOG_RECORD);klikkja_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',serje)
        assert 'TERMINAL SIZE 68x19' in shell('terminal size')
        serje=len(LOG_RECORD);klikkja_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',serje);vverifika_daqqas()
        rridimensjona_dreggja(4,(-너비,-높이));vverifika_daqqas().save(str(miżura_mogħdija/(daqqas_SMS+'-small.png')))
        # daqqas bidel_VALUE Lura_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        serje=len(LOG_RECORD);klikkja_VALUE(tieqa[0]+tieqa[2]-20,tieqa[1]+15);기다리기(b'TERMINAL FOCUS 2',serje)
        assert 'RESIZE CLOSED' in shell('echo RESIZE CLOSED')
        print('PASS:',daqqas_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if trasferiment_VALUE:trasferiment_VALUE.close()
        if mill_bogħod_VALUE:mill_bogħod_VALUE.close()
        if Proċess_VALUE.poll() is None:
            Proċess_VALUE.terminate()
            try:Proċess_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proċess_VALUE.kill();Proċess_VALUE.wait()
        selettur_a916db4e.close();Proċess_VALUE.stdout.close();(miżura_mogħdija/(daqqas_SMS+'.log')).write_bytes(LOG_RECORD)


def serje():
    miżura_mogħdija=pprojetta_għerq/'build/verification/resize';miżura_mogħdija.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,miżura_mogħdija);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(miżura_mogħdija/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':serje()
