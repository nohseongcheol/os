#!/usr/bin/env python3
"""taannallarik_titiqqat QEMU/VNC에서 터미널 모서리 Nusuarli_atuutilik·포인터·동적 immikkuuqtuq_atuutilik 칸·aaqqigiarli_atuutilik Ilulingit_atuutilik 보존를 검사한다."""
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
from igalaujaq_takussarurli import 정확한값
from 실행 import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    anininga_titiqqaq = '{}x{}'.format(너비, 높이)
    Pivallianiq_atuutilik = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', anininga_titiqqaq], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Pivallianiq_atuutilik.stdout, selectors.EVENT_READ)
    papattivik_sanimukutaak = bytearray(); ungasittuq_atuutilik = None; aullaaqtilli_atuutilik = None; 포인터숨김=[False]

    def 기다리기(saqqilli_atuutilik, 시작=0):
        마감 = time.monotonic() + 60
        while saqqilli_atuutilik not in papattivik_sanimukutaak[시작:]:
            if time.monotonic() > 마감 or Pivallianiq_atuutilik.poll() is not None or b'HALTED' in papattivik_sanimukutaak or b'PANIC:' in papattivik_sanimukutaak:
                raise AssertionError(papattivik_sanimukutaak[시작:].decode('utf-8', 'replace'))
            for piniku, _ in 선택기.select(.1):
                titiqqat = piniku.fileobj.read(65536)
                if titiqqat: papattivik_sanimukutaak.extend(titiqqat)
        return papattivik_sanimukutaak[시작:].decode('utf-8', 'replace')

    def naqilli_tikkuagaq(기호, 눌림=True): ungasittuq_atuutilik.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def nassiutili_titiqqaq(titiqqaq):
        시작 = len(papattivik_sanimukutaak)
        for immikkuuqtuq_atuutilik in titiqqaq:
            기호 = 0xff0d if immikkuuqtuq_atuutilik == '\n' else ord(immikkuuqtuq_atuutilik) if ord(immikkuuqtuq_atuutilik) < 256 else 0x1000000 | ord(immikkuuqtuq_atuutilik)
            naqilli_tikkuagaq(기호); naqilli_tikkuagaq(기호, False)
        return 시작

    def piqujijjutiliriji(titiqqaq): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', nassiutili_titiqqaq(titiqqaq+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ungasittuq_atuutilik.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def naqilli_atuutilik(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Bitmap_ajjinnguaq():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 taannallarik_titiqqat 너비를 쓴다.
        ungasittuq_atuutilik.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        titiraujarniq_atuutilik = Image.new('RGB', (너비, 높이)); sukuttia_atuutilik_9285603e = 0
        while True:
            종류 = 정확한값(ungasittuq_atuutilik, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                takininga_atuutilik = struct.unpack('>I', 정확한값(ungasittuq_atuutilik, 7)[3:])[0]; 정확한값(ungasittuq_atuutilik, takininga_atuutilik); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ungasittuq_atuutilik, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, takininga_atuutilik, tukiniktiri_atuutilik = struct.unpack('>HHHHi', 정확한값(ungasittuq_atuutilik, 12))
                if tukiniktiri_atuutilik == -239:
                    assert 폭==0 and takininga_atuutilik==0, 'remote cursor must be hidden'
                    포인터숨김[0]=True
                    continue
                assert tukiniktiri_atuutilik == 0 and 가로+폭 <= 너비 and 세로+takininga_atuutilik <= 높이
                titiraujarniq_atuutilik.paste(Image.frombytes('RGB', (폭, takininga_atuutilik), 정확한값(ungasittuq_atuutilik, 폭*takininga_atuutilik*4), 'raw', 'BGRX'), (가로, 세로))
                sukuttia_atuutilik_9285603e += 폭*takininga_atuutilik
            if sukuttia_atuutilik_9285603e:
                assert sukuttia_atuutilik_9285603e == 너비*높이, sukuttia_atuutilik_9285603e
                return titiraujarniq_atuutilik

    def qaujigiarli_pel(pittariik_atuutilik, 색):
        마감 = time.monotonic()+10
        while True:
            titiraujarniq_atuutilik = Bitmap_ajjinnguaq()
            if titiraujarniq_atuutilik.getpixel(pittariik_atuutilik) == 색: return titiraujarniq_atuutilik
            if time.monotonic() > 마감: raise AssertionError((pittariik_atuutilik, titiraujarniq_atuutilik.getpixel(pittariik_atuutilik), 색))

    def 올리기(atiq, titiqqat): aullaaqtilli_atuutilik.storbinary('STOR '+atiq, io.BytesIO(titiqqat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+anininga_titiqqaq+' RGB32').encode() in papattivik_sanimukutaak
        print('BOOT:', anininga_titiqqaq, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', papattivik_sanimukutaak).group(1))
        ungasittuq_atuutilik = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ungasittuq_atuutilik, 12) == b'RFB 003.008\n'; ungasittuq_atuutilik.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ungasittuq_atuutilik, 정확한값(ungasittuq_atuutilik, 1)[0]); ungasittuq_atuutilik.sendall(b'\x01')
        assert 정확한값(ungasittuq_atuutilik, 4) == b'\0'*4; ungasittuq_atuutilik.sendall(b'\x01')
        초기 = 정확한값(ungasittuq_atuutilik, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ungasittuq_atuutilik, struct.unpack('>I', 초기[20:])[0])
        ungasittuq_atuutilik.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ungasittuq_atuutilik.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        qaujigiarli_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for piniku,_ in 선택기.select(.02):
                    titiqqat=piniku.fileobj.read(65536)
                    if titiqqat:papattivik_sanimukutaak.extend(titiqqat)
        igalaangujaq=[12,48,568,360]
        def nalunairli_anininga():
            ammukutaak_atuutilik,sanimukutaak_atuutilik=(igalaangujaq[2]-24)//8,(igalaangujaq[3]-56)//16
            titiqqaq=piqujijjutiliriji('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ammukutaak_atuutilik,sanimukutaak_atuutilik) in titiqqaq,titiqqaq
            # taannallarik_titiqqat igalaangujaq 테두리: 단지 anininga kiggusiqarialik_atuutilik 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            qaujigiarli_pel((igalaangujaq[0],igalaangujaq[1]),(32,80,144))
            titiraujarniq_atuutilik=qaujigiarli_pel((igalaangujaq[0]+igalaangujaq[2]-1,igalaangujaq[1]+igalaangujaq[3]-1),(39,49,64))
            return titiraujarniq_atuutilik
        def 모서리(방향):
            return (igalaangujaq[0]+(3 if 방향 in (1,3) else igalaangujaq[2]-4),igalaangujaq[1]+(3 if 방향<=2 else igalaangujaq[3]-4))
        def anginga_aaqqigiarli_Nusuarli(방향,차이,tikkuagaq=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            qaujigiarli_pel(흰점,(255,255,255))
            가리키기(가,세,tikkuagaq)
            끝가=max(0,min(너비-1,가+차이[0]));끝세=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,끝세,tikkuagaq);가리키기(끝가,끝세,0);숨고르기()
            if tikkuagaq==1:
                왼,위,폭,takininga_atuutilik=igalaangujaq;오른,아래=왼+폭,위+takininga_atuutilik
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+끝세-세))
                else:아래=max(위+216,min(높이,아래+끝세-세))
                igalaangujaq[:]=[왼,위,오른-왼,아래-위]
        nalunairli_anininga();assert 포인터숨김[0]
        anginga_aaqqigiarli_Nusuarli(4,(-100,-60),4);nalunairli_anininga() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            anginga_aaqqigiarli_Nusuarli(방향,차이);nalunairli_anininga()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        nassiutili_titiqqaq("echo '"+긴글+"'");숨고르기()
        anginga_aaqqigiarli_Nusuarli(4,(-1000,-1000));assert igalaangujaq[2:]==[360,216]
        anginga_aaqqigiarli_Nusuarli(4,(너비,높이))
        시작=nassiutili_titiqqaq('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),시작);nalunairli_anininga()
        # vi가 aaqqigiarli_atuutilik 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        piqujijjutiliriji('ftpd start')
        aullaaqtilli_atuutilik=ftplib.FTP();aullaaqtilli_atuutilik.encoding='utf-8';aullaaqtilli_atuutilik.connect('127.0.0.1',접속번호,timeout=20);aullaaqtilli_atuutilik.login()
        기다리기(b'NORMAL',nassiutili_titiqqaq('vi /크기자료.txt\n'))
        기다리기(b'INSERT',nassiutili_titiqqaq('i미저장 한글 titiqqat\n'));숨고르기()
        anginga_aaqqigiarli_Nusuarli(4,(-너비,-높이))
        # ANSI sanimukutaak_atuutilik 이동에 새 sanimukutaak_atuutilik 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((igalaangujaq[3]-56)//16)).encode() in papattivik_sanimukutaak[-4096:]
        nassiutili_titiqqaq('작은 창에서도 이어 titiraq\n');숨고르기()
        anginga_aaqqigiarli_Nusuarli(4,(너비,높이))
        nassiutili_titiqqaq('큰 창에서도 이어 titiraq\n');숨고르기()
        naqilli_tikkuagaq(0xff1b);naqilli_tikkuagaq(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',nassiutili_titiqqaq(':wq\n'))
        Ilulingit_atuutilik=bytearray();aullaaqtilli_atuutilik.retrbinary('RETR 크기자료.txt',Ilulingit_atuutilik.extend)
        assert Ilulingit_atuutilik=='미저장 한글 titiqqat\n작은 창에서도 이어 titiraq\n큰 창에서도 이어 titiraq\n'.encode(),Ilulingit_atuutilik
        nalunairli_anininga().save(str(결과경로/(anininga_titiqqaq+'-large.png')))
        # 두 번째 창은 Aturniliuvagiiqtut anininga, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        시작=len(papattivik_sanimukutaak);naqilli_atuutilik(70,16);기다리기(b'TERMINAL FOCUS 2',시작)
        assert 'TERMINAL SIZE 68x19' in piqujijjutiliriji('terminal size')
        시작=len(papattivik_sanimukutaak);naqilli_atuutilik(180,16);기다리기(b'TERMINAL FOCUS 1',시작);nalunairli_anininga()
        anginga_aaqqigiarli_Nusuarli(4,(-너비,-높이));nalunairli_anininga().save(str(결과경로/(anininga_titiqqaq+'-small.png')))
        # anininga asijjirli_atuutilik Utimut_atuutilik X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        시작=len(papattivik_sanimukutaak);naqilli_atuutilik(igalaangujaq[0]+igalaangujaq[2]-20,igalaangujaq[1]+15);기다리기(b'TERMINAL FOCUS 2',시작)
        assert 'RESIZE CLOSED' in piqujijjutiliriji('echo RESIZE CLOSED')
        print('PASS:',anininga_titiqqaq,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if aullaaqtilli_atuutilik:aullaaqtilli_atuutilik.close()
        if ungasittuq_atuutilik:ungasittuq_atuutilik.close()
        if Pivallianiq_atuutilik.poll() is None:
            Pivallianiq_atuutilik.terminate()
            try:Pivallianiq_atuutilik.wait(timeout=8)
            except subprocess.TimeoutExpired:Pivallianiq_atuutilik.kill();Pivallianiq_atuutilik.wait()
        선택기.close();Pivallianiq_atuutilik.stdout.close();(결과경로/(anininga_titiqqaq+'.log')).write_bytes(papattivik_sanimukutaak)


def 시작():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    papattivik_sanimukutaak={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);papattivik_sanimukutaak['resolutions'].append([너비,높이])
        papattivik_sanimukutaak.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(papattivik_sanimukutaak,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':시작()
