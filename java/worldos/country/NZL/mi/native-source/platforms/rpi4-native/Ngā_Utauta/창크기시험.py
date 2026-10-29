#!/usr/bin/env python3
"""tūturu_raraunga QEMU/VNC에서 Tauranga 모서리 tō_uara·atatohu·동적 pūāhua_uara kāniwha_tāurunga·whakatika_uara Ihirangi_uara 보존를 검사한다."""
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
from papamahi_tiro import EXACT_uara
from kawe_tono import whakaatu_pūtake


def 창크기시험(너비, 높이, mēhua_ara):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    rahi_TEXT = '{}x{}'.format(너비, 높이)
    Hātepe_uara = subprocess.Popen(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', rahi_TEXT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pūtīpako_a916db4e = selectors.DefaultSelector(); pūtīpako_a916db4e.register(Hātepe_uara.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); mamao_uara = None; whakawhiti_uara_630ba093 = None; atatohu_hunahuna=[False]

    def 기다리기(whakaatu_uara, whakahaere=0):
        마감 = time.monotonic() + 60
        while whakaatu_uara not in LOG_RECORD[whakahaere:]:
            if time.monotonic() > 마감 or Hātepe_uara.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[whakahaere:].decode('utf-8', 'replace'))
            for hui, _ in pūtīpako_a916db4e.select(.1):
                raraunga = hui.fileobj.read(65536)
                if raraunga: LOG_RECORD.extend(raraunga)
        return LOG_RECORD[whakahaere:].decode('utf-8', 'replace')

    def pāwhiri_pātene(tohu, 눌림=True): mamao_uara.sendall(struct.pack('>BBHI', 4, int(눌림), 0, tohu))

    def tuku_kuputuhi(Ngā_kupu):
        whakahaere = len(LOG_RECORD)
        for pūāhua_uara in Ngā_kupu:
            tohu = 0xff0d if pūāhua_uara == '\n' else ord(pūāhua_uara) if ord(pūāhua_uara) < 256 else 0x1000000 | ord(pūāhua_uara)
            pāwhiri_pātene(tohu); pāwhiri_pātene(tohu, False)
        return whakahaere

    def anga(Ngā_kupu): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', tuku_kuputuhi(Ngā_kupu+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Poutū_tūranga, 눌림): mamao_uara.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Poutū_tūranga))

    def pāwhiri_uara(가로, Poutū_tūranga): 가리키기(가로, Poutū_tūranga, 1); 가리키기(가로, Poutū_tūranga, 0)

    def maheremoka_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tūturu_raraunga 너비를 쓴다.
        mamao_uara.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tātuhi_uara = Image.new('RGB', (너비, 높이)); kāwai_uara_9285603e = 0
        while True:
            종류 = EXACT_uara(mamao_uara, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                roa_uara = struct.unpack('>I', EXACT_uara(mamao_uara, 7)[3:])[0]; EXACT_uara(mamao_uara, roa_uara); continue
            assert 종류 == 0, 종류
            tuemi_COUNT = struct.unpack('>H', EXACT_uara(mamao_uara, 3)[1:])[0]
            for _ in range(tuemi_COUNT):
                가로, Poutū_tūranga, 폭, roa_uara, whakawaehere_uara = struct.unpack('>HHHHi', EXACT_uara(mamao_uara, 12))
                if whakawaehere_uara == -239:
                    assert 폭==0 and roa_uara==0, 'remote cursor must be hidden'
                    atatohu_hunahuna[0]=True
                    continue
                assert whakawaehere_uara == 0 and 가로+폭 <= 너비 and Poutū_tūranga+roa_uara <= 높이
                tātuhi_uara.paste(Image.frombytes('RGB', (폭, roa_uara), EXACT_uara(mamao_uara, 폭*roa_uara*4), 'raw', 'BGRX'), (가로, Poutū_tūranga))
                kāwai_uara_9285603e += 폭*roa_uara
            if kāwai_uara_9285603e:
                assert kāwai_uara_9285603e == 너비*높이, kāwai_uara_9285603e
                return tātuhi_uara

    def taki_pika(ruruku_uara, 색):
        마감 = time.monotonic()+10
        while True:
            tātuhi_uara = maheremoka_IMAGE()
            if tātuhi_uara.getpixel(ruruku_uara) == 색: return tātuhi_uara
            if time.monotonic() > 마감: raise AssertionError((ruruku_uara, tātuhi_uara.getpixel(ruruku_uara), 색))

    def tukuatu_Ngā_Kōnae(Ingoa, raraunga): whakawhiti_uara_630ba093.storbinary('STOR '+Ingoa, io.BytesIO(raraunga))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+rahi_TEXT+' RGB32').encode() in LOG_RECORD
        print('BOOT:', rahi_TEXT, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        mamao_uara = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_uara(mamao_uara, 12) == b'RFB 003.008\n'; mamao_uara.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_uara(mamao_uara, EXACT_uara(mamao_uara, 1)[0]); mamao_uara.sendall(b'\x01')
        assert EXACT_uara(mamao_uara, 4) == b'\0'*4; mamao_uara.sendall(b'\x01')
        초기 = EXACT_uara(mamao_uara, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_uara(mamao_uara, struct.unpack('>I', 초기[20:])[0])
        mamao_uara.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        mamao_uara.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        taki_pika((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for hui,_ in pūtīpako_a916db4e.select(.02):
                    raraunga=hui.fileobj.read(65536)
                    if raraunga:LOG_RECORD.extend(raraunga)
        matapihi=[12,48,568,360]
        def manatoko_rahi():
            tīwae_uara,ROW_uara=(matapihi[2]-24)//8,(matapihi[3]-56)//16
            Ngā_kupu=anga('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(tīwae_uara,ROW_uara) in Ngā_kupu,Ngā_kupu
            # tūturu_raraunga matapihi 테두리: 단지 rahi uiui_uara 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            taki_pika((matapihi[0],matapihi[1]),(32,80,144))
            tātuhi_uara=taki_pika((matapihi[0]+matapihi[2]-1,matapihi[1]+matapihi[3]-1),(39,49,64))
            return tātuhi_uara
        def 모서리(방향):
            return (matapihi[0]+(3 if 방향 in (1,3) else matapihi[2]-4),matapihi[1]+(3 if 방향<=2 else matapihi[3]-4))
        def whakarahi_anō_tō(방향,차이,pātene=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            taki_pika(흰점,(255,255,255))
            가리키기(가,세,pātene)
            끝가=max(0,min(너비-1,가+차이[0]));mutu_Poutū=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,mutu_Poutū,pātene);가리키기(끝가,mutu_Poutū,0);숨고르기()
            if pātene==1:
                LEFT_uara,위,폭,roa_uara=matapihi;RIGHT_uara,아래=LEFT_uara+폭,위+roa_uara
                if 방향 in (1,3):LEFT_uara=max(0,min(RIGHT_uara-360,LEFT_uara+끝가-가))
                else:RIGHT_uara=max(LEFT_uara+360,min(너비,RIGHT_uara+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+mutu_Poutū-세))
                else:아래=max(위+216,min(높이,아래+mutu_Poutū-세))
                matapihi[:]=[LEFT_uara,위,RIGHT_uara-LEFT_uara,아래-위]
        manatoko_rahi();assert atatohu_hunahuna[0]
        whakarahi_anō_tō(4,(-100,-60),4);manatoko_rahi() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            whakarahi_anō_tō(방향,차이);manatoko_rahi()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        tuku_kuputuhi("echo '"+긴글+"'");숨고르기()
        whakarahi_anō_tō(4,(-1000,-1000));assert matapihi[2:]==[360,216]
        whakarahi_anō_tō(4,(너비,높이))
        whakahaere=tuku_kuputuhi('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),whakahaere);manatoko_rahi()
        # vi가 whakatika_uara 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        anga('ftpd start')
        whakawhiti_uara_630ba093=ftplib.FTP();whakawhiti_uara_630ba093.encoding='utf-8';whakawhiti_uara_630ba093.connect('127.0.0.1',접속번호,timeout=20);whakawhiti_uara_630ba093.login()
        기다리기(b'NORMAL',tuku_kuputuhi('vi /크기자료.txt\n'))
        기다리기(b'INSERT',tuku_kuputuhi('i미저장 한글 raraunga\n'));숨고르기()
        whakarahi_anō_tō(4,(-너비,-높이))
        # ANSI ROW_uara 이동에 새 ROW_uara 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((matapihi[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        tuku_kuputuhi('작은 창에서도 이어 Tuhia\n');숨고르기()
        whakarahi_anō_tō(4,(너비,높이))
        tuku_kuputuhi('큰 창에서도 이어 Tuhia\n');숨고르기()
        pāwhiri_pātene(0xff1b);pāwhiri_pātene(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',tuku_kuputuhi(':wq\n'))
        Ihirangi_uara=bytearray();whakawhiti_uara_630ba093.retrbinary('RETR 크기자료.txt',Ihirangi_uara.extend)
        assert Ihirangi_uara=='미저장 한글 raraunga\n작은 창에서도 이어 Tuhia\n큰 창에서도 이어 Tuhia\n'.encode(),Ihirangi_uara
        manatoko_rahi().save(str(mēhua_ara/(rahi_TEXT+'-large.png')))
        # 두 번째 창은 uara_taunoa rahi, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        whakahaere=len(LOG_RECORD);pāwhiri_uara(70,16);기다리기(b'TERMINAL FOCUS 2',whakahaere)
        assert 'TERMINAL SIZE 68x19' in anga('terminal size')
        whakahaere=len(LOG_RECORD);pāwhiri_uara(180,16);기다리기(b'TERMINAL FOCUS 1',whakahaere);manatoko_rahi()
        whakarahi_anō_tō(4,(-너비,-높이));manatoko_rahi().save(str(mēhua_ara/(rahi_TEXT+'-small.png')))
        # rahi huri_uara Hoki_uara X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        whakahaere=len(LOG_RECORD);pāwhiri_uara(matapihi[0]+matapihi[2]-20,matapihi[1]+15);기다리기(b'TERMINAL FOCUS 2',whakahaere)
        assert 'RESIZE CLOSED' in anga('echo RESIZE CLOSED')
        print('PASS:',rahi_TEXT,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if whakawhiti_uara_630ba093:whakawhiti_uara_630ba093.close()
        if mamao_uara:mamao_uara.close()
        if Hātepe_uara.poll() is None:
            Hātepe_uara.terminate()
            try:Hātepe_uara.wait(timeout=8)
            except subprocess.TimeoutExpired:Hātepe_uara.kill();Hātepe_uara.wait()
        pūtīpako_a916db4e.close();Hātepe_uara.stdout.close();(mēhua_ara/(rahi_TEXT+'.log')).write_bytes(LOG_RECORD)


def whakahaere():
    mēhua_ara=whakaatu_pūtake/'build/verification/resize';mēhua_ara.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mēhua_ara);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mēhua_ara/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':whakahaere()
