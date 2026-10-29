#!/usr/bin/env python3
"""tota_tshedimosetso QEMU/VNC에서 터미널 모서리 Goga_Boleng·sesupi·동적 Letshwao_Boleng sebaka_tsenyo·Tseleganya_Boleng Diteng_Boleng 보존를 검사한다."""
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
from desekethopo_Tebego import 정확한값
from diragatsa_Taelo import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    lekanya_SMS = '{}x{}'.format(너비, 높이)
    Thulaganyo_Boleng = subprocess.Popen(['python3', str(기준/'Thuluse/diragatsa_Taelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', lekanya_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    setlhophi_a916db4e = selectors.DefaultSelector(); setlhophi_a916db4e.register(Thulaganyo_Boleng.stdout, selectors.EVENT_READ)
    rekota_mola = bytearray(); kgakala_Boleng = None; fudusa_Boleng = None; sesupi_fitlhegileng=[False]

    def 기다리기(bontsha_Boleng, dirisa=0):
        마감 = time.monotonic() + 60
        while bontsha_Boleng not in rekota_mola[dirisa:]:
            if time.monotonic() > 마감 or Thulaganyo_Boleng.poll() is not None or b'HALTED' in rekota_mola or b'PANIC:' in rekota_mola:
                raise AssertionError(rekota_mola[dirisa:].decode('utf-8', 'replace'))
            for tiragalo, _ in setlhophi_a916db4e.select(.1):
                tshedimosetso = tiragalo.fileobj.read(65536)
                if tshedimosetso: rekota_mola.extend(tshedimosetso)
        return rekota_mola[dirisa:].decode('utf-8', 'replace')

    def tobetsa_konopo(letshwao, 눌림=True): kgakala_Boleng.sendall(struct.pack('>BBHI', 4, int(눌림), 0, letshwao))

    def romela_SMS(SMS):
        dirisa = len(rekota_mola)
        for Letshwao_Boleng in SMS:
            letshwao = 0xff0d if Letshwao_Boleng == '\n' else ord(Letshwao_Boleng) if ord(Letshwao_Boleng) < 256 else 0x1000000 | ord(Letshwao_Boleng)
            tobetsa_konopo(letshwao); tobetsa_konopo(letshwao, False)
        return dirisa

    def setlhalosataelo(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', romela_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kgakala_Boleng.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def tobetsa_Boleng(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Setshwantsho_sa_maronthorontho_Setshwantsho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tota_tshedimosetso 너비를 쓴다.
        kgakala_Boleng.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        sethalo_Boleng = Image.new('RGB', (너비, 높이)); lefelo_Boleng_9285603e = 0
        while True:
            종류 = 정확한값(kgakala_Boleng, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                boleele_Boleng = struct.unpack('>I', 정확한값(kgakala_Boleng, 7)[3:])[0]; 정확한값(kgakala_Boleng, boleele_Boleng); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kgakala_Boleng, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, boleele_Boleng, khoutufatso_Boleng = struct.unpack('>HHHHi', 정확한값(kgakala_Boleng, 12))
                if khoutufatso_Boleng == -239:
                    assert 폭==0 and boleele_Boleng==0, 'remote cursor must be hidden'
                    sesupi_fitlhegileng[0]=True
                    continue
                assert khoutufatso_Boleng == 0 and 가로+폭 <= 너비 and 세로+boleele_Boleng <= 높이
                sethalo_Boleng.paste(Image.frombytes('RGB', (폭, boleele_Boleng), 정확한값(kgakala_Boleng, 폭*boleele_Boleng*4), 'raw', 'BGRX'), (가로, 세로))
                lefelo_Boleng_9285603e += 폭*boleele_Boleng
            if lefelo_Boleng_9285603e:
                assert lefelo_Boleng_9285603e == 너비*높이, lefelo_Boleng_9285603e
                return sethalo_Boleng

    def tlhola_phele(khoodineite_Boleng, 색):
        마감 = time.monotonic()+10
        while True:
            sethalo_Boleng = Setshwantsho_sa_maronthorontho_Setshwantsho()
            if sethalo_Boleng.getpixel(khoodineite_Boleng) == 색: return sethalo_Boleng
            if time.monotonic() > 마감: raise AssertionError((khoodineite_Boleng, sethalo_Boleng.getpixel(khoodineite_Boleng), 색))

    def laisa_Difaele(leina, tshedimosetso): fudusa_Boleng.storbinary('STOR '+leina, io.BytesIO(tshedimosetso))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+lekanya_SMS+' RGB32').encode() in rekota_mola
        print('BOOT:', lekanya_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', rekota_mola).group(1))
        kgakala_Boleng = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kgakala_Boleng, 12) == b'RFB 003.008\n'; kgakala_Boleng.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kgakala_Boleng, 정확한값(kgakala_Boleng, 1)[0]); kgakala_Boleng.sendall(b'\x01')
        assert 정확한값(kgakala_Boleng, 4) == b'\0'*4; kgakala_Boleng.sendall(b'\x01')
        초기 = 정확한값(kgakala_Boleng, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kgakala_Boleng, struct.unpack('>I', 초기[20:])[0])
        kgakala_Boleng.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kgakala_Boleng.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        tlhola_phele((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for tiragalo,_ in setlhophi_a916db4e.select(.02):
                    tshedimosetso=tiragalo.fileobj.read(65536)
                    if tshedimosetso:rekota_mola.extend(tshedimosetso)
        fensetere=[12,48,568,360]
        def netefatsa_lekanya():
            Kholomo_Boleng,mola_Boleng=(fensetere[2]-24)//8,(fensetere[3]-56)//16
            SMS=setlhalosataelo('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(Kholomo_Boleng,mola_Boleng) in SMS,SMS
            # tota_tshedimosetso fensetere 테두리: 단지 lekanya fenenkolola_Boleng 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            tlhola_phele((fensetere[0],fensetere[1]),(32,80,144))
            sethalo_Boleng=tlhola_phele((fensetere[0]+fensetere[2]-1,fensetere[1]+fensetere[3]-1),(39,49,64))
            return sethalo_Boleng
        def 모서리(방향):
            return (fensetere[0]+(3 if 방향 in (1,3) else fensetere[2]-4),fensetere[1]+(3 if 방향<=2 else fensetere[3]-4))
        def lekanyasešwa_Goga(방향,차이,konopo=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            tlhola_phele(흰점,(255,255,255))
            가리키기(가,세,konopo)
            끝가=max(0,min(너비-1,가+차이[0]));kgaola_Tsepamo=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,kgaola_Tsepamo,konopo);가리키기(끝가,kgaola_Tsepamo,0);숨고르기()
            if konopo==1:
                왼,위,폭,boleele_Boleng=fensetere;오른,아래=왼+폭,위+boleele_Boleng
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+kgaola_Tsepamo-세))
                else:아래=max(위+216,min(높이,아래+kgaola_Tsepamo-세))
                fensetere[:]=[왼,위,오른-왼,아래-위]
        netefatsa_lekanya();assert sesupi_fitlhegileng[0]
        lekanyasešwa_Goga(4,(-100,-60),4);netefatsa_lekanya() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            lekanyasešwa_Goga(방향,차이);netefatsa_lekanya()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        romela_SMS("echo '"+긴글+"'");숨고르기()
        lekanyasešwa_Goga(4,(-1000,-1000));assert fensetere[2:]==[360,216]
        lekanyasešwa_Goga(4,(너비,높이))
        dirisa=romela_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),dirisa);netefatsa_lekanya()
        # vi가 Tseleganya_Boleng 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        setlhalosataelo('ftpd start')
        fudusa_Boleng=ftplib.FTP();fudusa_Boleng.encoding='utf-8';fudusa_Boleng.connect('127.0.0.1',접속번호,timeout=20);fudusa_Boleng.login()
        기다리기(b'NORMAL',romela_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',romela_SMS('i미저장 한글 tshedimosetso\n'));숨고르기()
        lekanyasešwa_Goga(4,(-너비,-높이))
        # ANSI mola_Boleng 이동에 새 mola_Boleng 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((fensetere[3]-56)//16)).encode() in rekota_mola[-4096:]
        romela_SMS('작은 창에서도 이어 kwala\n');숨고르기()
        lekanyasešwa_Goga(4,(너비,높이))
        romela_SMS('큰 창에서도 이어 kwala\n');숨고르기()
        tobetsa_konopo(0xff1b);tobetsa_konopo(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',romela_SMS(':wq\n'))
        Diteng_Boleng=bytearray();fudusa_Boleng.retrbinary('RETR 크기자료.txt',Diteng_Boleng.extend)
        assert Diteng_Boleng=='미저장 한글 tshedimosetso\n작은 창에서도 이어 kwala\n큰 창에서도 이어 kwala\n'.encode(),Diteng_Boleng
        netefatsa_lekanya().save(str(결과경로/(lekanya_SMS+'-large.png')))
        # 두 번째 창은 boleng_jo_bo_rulaganyeditsweng_ruri lekanya, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        dirisa=len(rekota_mola);tobetsa_Boleng(70,16);기다리기(b'TERMINAL FOCUS 2',dirisa)
        assert 'TERMINAL SIZE 68x19' in setlhalosataelo('terminal size')
        dirisa=len(rekota_mola);tobetsa_Boleng(180,16);기다리기(b'TERMINAL FOCUS 1',dirisa);netefatsa_lekanya()
        lekanyasešwa_Goga(4,(-너비,-높이));netefatsa_lekanya().save(str(결과경로/(lekanya_SMS+'-small.png')))
        # lekanya fetola_Boleng Morago_Boleng X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        dirisa=len(rekota_mola);tobetsa_Boleng(fensetere[0]+fensetere[2]-20,fensetere[1]+15);기다리기(b'TERMINAL FOCUS 2',dirisa)
        assert 'RESIZE CLOSED' in setlhalosataelo('echo RESIZE CLOSED')
        print('PASS:',lekanya_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if fudusa_Boleng:fudusa_Boleng.close()
        if kgakala_Boleng:kgakala_Boleng.close()
        if Thulaganyo_Boleng.poll() is None:
            Thulaganyo_Boleng.terminate()
            try:Thulaganyo_Boleng.wait(timeout=8)
            except subprocess.TimeoutExpired:Thulaganyo_Boleng.kill();Thulaganyo_Boleng.wait()
        setlhophi_a916db4e.close();Thulaganyo_Boleng.stdout.close();(결과경로/(lekanya_SMS+'.log')).write_bytes(rekota_mola)


def dirisa():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    rekota_mola={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);rekota_mola['resolutions'].append([너비,높이])
        rekota_mola.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(rekota_mola,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':dirisa()
