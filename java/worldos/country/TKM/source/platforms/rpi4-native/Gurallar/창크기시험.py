#!/usr/bin/env python3
"""hakyky_maglumat QEMU/VNC에서 터미널 모서리 süýşür_baha·görkeziji·동적 nyşan_baha_068c2631 ýer_girizmeklik·redaktirle_baha Mazmun_baha 보존를 검사한다."""
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
from iş_stoly_görkez import 정확한값
from ýerine_ýetir_buýruk import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ölçegi_üýtget_SMS = '{}x{}'.format(너비, 높이)
    Proses_baha = subprocess.Popen(['python3', str(기준/'Gurallar/ýerine_ýetir_buýruk.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ölçegi_üýtget_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    saýlaýjy_a916db4e = selectors.DefaultSelector(); saýlaýjy_a916db4e.register(Proses_baha.stdout, selectors.EVENT_READ)
    hasaba_alyş_setir = bytearray(); uzakdan_baha = None; geçir_baha = None; görkeziji_gizlin=[False]

    def 기다리기(görkez_baha_487749b8, Bitir=0):
        마감 = time.monotonic() + 60
        while görkez_baha_487749b8 not in hasaba_alyş_setir[Bitir:]:
            if time.monotonic() > 마감 or Proses_baha.poll() is not None or b'HALTED' in hasaba_alyş_setir or b'PANIC:' in hasaba_alyş_setir:
                raise AssertionError(hasaba_alyş_setir[Bitir:].decode('utf-8', 'replace'))
            for waka, _ in saýlaýjy_a916db4e.select(.1):
                maglumat = waka.fileobj.read(65536)
                if maglumat: hasaba_alyş_setir.extend(maglumat)
        return hasaba_alyş_setir[Bitir:].decode('utf-8', 'replace')

    def bas_düwme(nyşan, 눌림=True): uzakdan_baha.sendall(struct.pack('>BBHI', 4, int(눌림), 0, nyşan))

    def SMS_iber(Metin):
        Bitir = len(hasaba_alyş_setir)
        for nyşan_baha_068c2631 in Metin:
            nyşan = 0xff0d if nyşan_baha_068c2631 == '\n' else ord(nyşan_baha_068c2631) if ord(nyşan_baha_068c2631) < 256 else 0x1000000 | ord(nyşan_baha_068c2631)
            bas_düwme(nyşan); bas_düwme(nyşan, False)
        return Bitir

    def gabyjak(Metin): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_iber(Metin+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): uzakdan_baha.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bas_baha(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def nokatlardan_ýygnalan_şekil_surat():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 hakyky_maglumat 너비를 쓴다.
        uzakdan_baha.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        çyzgy_baha = Image.new('RGB', (너비, 높이)); ýaýla_baha = 0
        while True:
            종류 = 정확한값(uzakdan_baha, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                dowamlylyk_baha = struct.unpack('>I', 정확한값(uzakdan_baha, 7)[3:])[0]; 정확한값(uzakdan_baha, dowamlylyk_baha); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(uzakdan_baha, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, dowamlylyk_baha, kodlaşdyrma_baha = struct.unpack('>HHHHi', 정확한값(uzakdan_baha, 12))
                if kodlaşdyrma_baha == -239:
                    assert 폭==0 and dowamlylyk_baha==0, 'remote cursor must be hidden'
                    görkeziji_gizlin[0]=True
                    continue
                assert kodlaşdyrma_baha == 0 and 가로+폭 <= 너비 and 세로+dowamlylyk_baha <= 높이
                çyzgy_baha.paste(Image.frombytes('RGB', (폭, dowamlylyk_baha), 정확한값(uzakdan_baha, 폭*dowamlylyk_baha*4), 'raw', 'BGRX'), (가로, 세로))
                ýaýla_baha += 폭*dowamlylyk_baha
            if ýaýla_baha:
                assert ýaýla_baha == 너비*높이, ýaýla_baha
                return çyzgy_baha

    def derňe_pel(koordinata_baha, 색):
        마감 = time.monotonic()+10
        while True:
            çyzgy_baha = nokatlardan_ýygnalan_şekil_surat()
            if çyzgy_baha.getpixel(koordinata_baha) == 색: return çyzgy_baha
            if time.monotonic() > 마감: raise AssertionError((koordinata_baha, çyzgy_baha.getpixel(koordinata_baha), 색))

    def ýükle_Faýllar(Ad, maglumat): geçir_baha.storbinary('STOR '+Ad, io.BytesIO(maglumat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ölçegi_üýtget_SMS+' RGB32').encode() in hasaba_alyş_setir
        print('BOOT:', ölçegi_üýtget_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', hasaba_alyş_setir).group(1))
        uzakdan_baha = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(uzakdan_baha, 12) == b'RFB 003.008\n'; uzakdan_baha.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(uzakdan_baha, 정확한값(uzakdan_baha, 1)[0]); uzakdan_baha.sendall(b'\x01')
        assert 정확한값(uzakdan_baha, 4) == b'\0'*4; uzakdan_baha.sendall(b'\x01')
        초기 = 정확한값(uzakdan_baha, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(uzakdan_baha, struct.unpack('>I', 초기[20:])[0])
        uzakdan_baha.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzakdan_baha.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        derňe_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for waka,_ in saýlaýjy_a916db4e.select(.02):
                    maglumat=waka.fileobj.read(65536)
                    if maglumat:hasaba_alyş_setir.extend(maglumat)
        penjire=[12,48,568,360]
        def barla_ölçegi_üýtget():
            sütün_baha,setir_baha=(penjire[2]-24)//8,(penjire[3]-56)//16
            Metin=gabyjak('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(sütün_baha,setir_baha) in Metin,Metin
            # hakyky_maglumat penjire 테두리: 단지 Ululyk talap_baha 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            derňe_pel((penjire[0],penjire[1]),(32,80,144))
            çyzgy_baha=derňe_pel((penjire[0]+penjire[2]-1,penjire[1]+penjire[3]-1),(39,49,64))
            return çyzgy_baha
        def 모서리(방향):
            return (penjire[0]+(3 if 방향 in (1,3) else penjire[2]-4),penjire[1]+(3 if 방향<=2 else penjire[3]-4))
        def ölçegi_üýtget_süýşür(방향,차이,düwme=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            derňe_pel(흰점,(255,255,255))
            가리키기(가,세,düwme)
            끝가=max(0,min(너비-1,가+차이[0]));tamamla_Dik=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,tamamla_Dik,düwme);가리키기(끝가,tamamla_Dik,0);숨고르기()
            if düwme==1:
                왼,위,폭,dowamlylyk_baha=penjire;오른,아래=왼+폭,위+dowamlylyk_baha
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+tamamla_Dik-세))
                else:아래=max(위+216,min(높이,아래+tamamla_Dik-세))
                penjire[:]=[왼,위,오른-왼,아래-위]
        barla_ölçegi_üýtget();assert görkeziji_gizlin[0]
        ölçegi_üýtget_süýşür(4,(-100,-60),4);barla_ölçegi_üýtget() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ölçegi_üýtget_süýşür(방향,차이);barla_ölçegi_üýtget()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_iber("echo '"+긴글+"'");숨고르기()
        ölçegi_üýtget_süýşür(4,(-1000,-1000));assert penjire[2:]==[360,216]
        ölçegi_üýtget_süýşür(4,(너비,높이))
        Bitir=SMS_iber('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Bitir);barla_ölçegi_üýtget()
        # vi가 redaktirle_baha 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        gabyjak('ftpd start')
        geçir_baha=ftplib.FTP();geçir_baha.encoding='utf-8';geçir_baha.connect('127.0.0.1',접속번호,timeout=20);geçir_baha.login()
        기다리기(b'NORMAL',SMS_iber('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_iber('i미저장 한글 maglumat\n'));숨고르기()
        ölçegi_üýtget_süýşür(4,(-너비,-높이))
        # ANSI setir_baha 이동에 새 setir_baha 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((penjire[3]-56)//16)).encode() in hasaba_alyş_setir[-4096:]
        SMS_iber('작은 창에서도 이어 Ýaz\n');숨고르기()
        ölçegi_üýtget_süýşür(4,(너비,높이))
        SMS_iber('큰 창에서도 이어 Ýaz\n');숨고르기()
        bas_düwme(0xff1b);bas_düwme(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_iber(':wq\n'))
        Mazmun_baha=bytearray();geçir_baha.retrbinary('RETR 크기자료.txt',Mazmun_baha.extend)
        assert Mazmun_baha=='미저장 한글 maglumat\n작은 창에서도 이어 Ýaz\n큰 창에서도 이어 Ýaz\n'.encode(),Mazmun_baha
        barla_ölçegi_üýtget().save(str(결과경로/(ölçegi_üýtget_SMS+'-large.png')))
        # 두 번째 창은 öňünden_kabul_edilen_baha Ululyk, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Bitir=len(hasaba_alyş_setir);bas_baha(70,16);기다리기(b'TERMINAL FOCUS 2',Bitir)
        assert 'TERMINAL SIZE 68x19' in gabyjak('terminal size')
        Bitir=len(hasaba_alyş_setir);bas_baha(180,16);기다리기(b'TERMINAL FOCUS 1',Bitir);barla_ölçegi_üýtget()
        ölçegi_üýtget_süýşür(4,(-너비,-높이));barla_ölçegi_üýtget().save(str(결과경로/(ölçegi_üýtget_SMS+'-small.png')))
        # Ululyk üýtget_baha Yza_baha X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Bitir=len(hasaba_alyş_setir);bas_baha(penjire[0]+penjire[2]-20,penjire[1]+15);기다리기(b'TERMINAL FOCUS 2',Bitir)
        assert 'RESIZE CLOSED' in gabyjak('echo RESIZE CLOSED')
        print('PASS:',ölçegi_üýtget_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if geçir_baha:geçir_baha.close()
        if uzakdan_baha:uzakdan_baha.close()
        if Proses_baha.poll() is None:
            Proses_baha.terminate()
            try:Proses_baha.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_baha.kill();Proses_baha.wait()
        saýlaýjy_a916db4e.close();Proses_baha.stdout.close();(결과경로/(ölçegi_üýtget_SMS+'.log')).write_bytes(hasaba_alyş_setir)


def Bitir():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    hasaba_alyş_setir={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);hasaba_alyş_setir['resolutions'].append([너비,높이])
        hasaba_alyş_setir.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(hasaba_alyş_setir,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Bitir()
