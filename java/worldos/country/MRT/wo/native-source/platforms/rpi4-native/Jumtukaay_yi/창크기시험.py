#!/usr/bin/env python3
"""liteew_mbir QEMU/VNC에서 터미널 모서리 randal_xëyma·joxañukaay·동적 Araf_xëyma xar_xar_dugal_xabaar·soppi_xëyma Këmb_xëyma 보존를 검사한다."""
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
from Biro_wonin import 정확한값
from def_ndigel import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    tolluwaay_SMS = '{}x{}'.format(너비, 높이)
    yokkute_xëyma = subprocess.Popen(['python3', str(기준/'Jumtukaay_yi/def_ndigel.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', tolluwaay_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tànnkat_a916db4e = selectors.DefaultSelector(); tànnkat_a916db4e.register(yokkute_xëyma.stdout, selectors.EVENT_READ)
    làq_Dënk = bytearray(); lu_soree_xëyma = None; toxal_xëyma_630ba093 = None; joxañukaay_nëmbu=[False]

    def 기다리기(féeñal_xëyma, daw=0):
        마감 = time.monotonic() + 60
        while féeñal_xëyma not in làq_Dënk[daw:]:
            if time.monotonic() > 마감 or yokkute_xëyma.poll() is not None or b'HALTED' in làq_Dënk or b'PANIC:' in làq_Dënk:
                raise AssertionError(làq_Dënk[daw:].decode('utf-8', 'replace'))
            for xewxew, _ in tànnkat_a916db4e.select(.1):
                mbir = xewxew.fileobj.read(65536)
                if mbir: làq_Dënk.extend(mbir)
        return làq_Dënk[daw:].decode('utf-8', 'replace')

    def bës_butoñ(sembóol, 눌림=True): lu_soree_xëyma.sendall(struct.pack('>BBHI', 4, int(눌림), 0, sembóol))

    def yónnee_SMS(Tekst):
        daw = len(làq_Dënk)
        for Araf_xëyma in Tekst:
            sembóol = 0xff0d if Araf_xëyma == '\n' else ord(Araf_xëyma) if ord(Araf_xëyma) < 256 else 0x1000000 | ord(Araf_xëyma)
            bës_butoñ(sembóol); bës_butoñ(sembóol, False)
        return daw

    def Wëreef(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', yónnee_SMS(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): lu_soree_xëyma.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bës_xëyma(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Nataal_bu_sosoo_ci_ay_tomb_nataal():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 liteew_mbir 너비를 쓴다.
        lu_soree_xëyma.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        deseñ_xëyma = Image.new('RGB', (너비, 높이)); ngiir_xëyma_9285603e = 0
        while True:
            종류 = 정확한값(lu_soree_xëyma, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                diir_xëyma = struct.unpack('>I', 정확한값(lu_soree_xëyma, 7)[3:])[0]; 정확한값(lu_soree_xëyma, diir_xëyma); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(lu_soree_xëyma, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, diir_xëyma, nëbbin_ci_lim_xëyma = struct.unpack('>HHHHi', 정확한값(lu_soree_xëyma, 12))
                if nëbbin_ci_lim_xëyma == -239:
                    assert 폭==0 and diir_xëyma==0, 'remote cursor must be hidden'
                    joxañukaay_nëmbu[0]=True
                    continue
                assert nëbbin_ci_lim_xëyma == 0 and 가로+폭 <= 너비 and 세로+diir_xëyma <= 높이
                deseñ_xëyma.paste(Image.frombytes('RGB', (폭, diir_xëyma), 정확한값(lu_soree_xëyma, 폭*diir_xëyma*4), 'raw', 'BGRX'), (가로, 세로))
                ngiir_xëyma_9285603e += 폭*diir_xëyma
            if ngiir_xëyma_9285603e:
                assert ngiir_xëyma_9285603e == 너비*높이, ngiir_xëyma_9285603e
                return deseñ_xëyma

    def sek_piksel(tolluwaay_xëyma, 색):
        마감 = time.monotonic()+10
        while True:
            deseñ_xëyma = Nataal_bu_sosoo_ci_ay_tomb_nataal()
            if deseñ_xëyma.getpixel(tolluwaay_xëyma) == 색: return deseñ_xëyma
            if time.monotonic() > 마감: raise AssertionError((tolluwaay_xëyma, deseñ_xëyma.getpixel(tolluwaay_xëyma), 색))

    def toxalsi_Fisiye_yi(tur_253d1510, mbir): toxal_xëyma_630ba093.storbinary('STOR '+tur_253d1510, io.BytesIO(mbir))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+tolluwaay_SMS+' RGB32').encode() in làq_Dënk
        print('BOOT:', tolluwaay_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', làq_Dënk).group(1))
        lu_soree_xëyma = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(lu_soree_xëyma, 12) == b'RFB 003.008\n'; lu_soree_xëyma.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(lu_soree_xëyma, 정확한값(lu_soree_xëyma, 1)[0]); lu_soree_xëyma.sendall(b'\x01')
        assert 정확한값(lu_soree_xëyma, 4) == b'\0'*4; lu_soree_xëyma.sendall(b'\x01')
        초기 = 정확한값(lu_soree_xëyma, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(lu_soree_xëyma, struct.unpack('>I', 초기[20:])[0])
        lu_soree_xëyma.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        lu_soree_xëyma.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sek_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for xewxew,_ in tànnkat_a916db4e.select(.02):
                    mbir=xewxew.fileobj.read(65536)
                    if mbir:làq_Dënk.extend(mbir)
        palanteer=[12,48,568,360]
        def luñutu_tolluwaay():
            Jen_xëyma,Dënk_xëyma=(palanteer[2]-24)//8,(palanteer[3]-56)//16
            Tekst=Wëreef('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(Jen_xëyma,Dënk_xëyma) in Tekst,Tekst
            # liteew_mbir palanteer 테두리: 단지 tolluwaay laaj_xëyma 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sek_piksel((palanteer[0],palanteer[1]),(32,80,144))
            deseñ_xëyma=sek_piksel((palanteer[0]+palanteer[2]-1,palanteer[1]+palanteer[3]-1),(39,49,64))
            return deseñ_xëyma
        def 모서리(방향):
            return (palanteer[0]+(3 if 방향 in (1,3) else palanteer[2]-4),palanteer[1]+(3 if 방향<=2 else palanteer[3]-4))
        def nattaat_randal(방향,차이,butoñ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sek_piksel(흰점,(255,255,255))
            가리키기(가,세,butoñ)
            끝가=max(0,min(너비-1,가+차이[0]));jeexal_Taxaw=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,jeexal_Taxaw,butoñ);가리키기(끝가,jeexal_Taxaw,0);숨고르기()
            if butoñ==1:
                왼,위,폭,diir_xëyma=palanteer;오른,아래=왼+폭,위+diir_xëyma
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+jeexal_Taxaw-세))
                else:아래=max(위+216,min(높이,아래+jeexal_Taxaw-세))
                palanteer[:]=[왼,위,오른-왼,아래-위]
        luñutu_tolluwaay();assert joxañukaay_nëmbu[0]
        nattaat_randal(4,(-100,-60),4);luñutu_tolluwaay() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            nattaat_randal(방향,차이);luñutu_tolluwaay()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        yónnee_SMS("echo '"+긴글+"'");숨고르기()
        nattaat_randal(4,(-1000,-1000));assert palanteer[2:]==[360,216]
        nattaat_randal(4,(너비,높이))
        daw=yónnee_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),daw);luñutu_tolluwaay()
        # vi가 soppi_xëyma 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        Wëreef('ftpd start')
        toxal_xëyma_630ba093=ftplib.FTP();toxal_xëyma_630ba093.encoding='utf-8';toxal_xëyma_630ba093.connect('127.0.0.1',접속번호,timeout=20);toxal_xëyma_630ba093.login()
        기다리기(b'NORMAL',yónnee_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',yónnee_SMS('i미저장 한글 mbir\n'));숨고르기()
        nattaat_randal(4,(-너비,-높이))
        # ANSI Dënk_xëyma 이동에 새 Dënk_xëyma 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((palanteer[3]-56)//16)).encode() in làq_Dënk[-4096:]
        yónnee_SMS('작은 창에서도 이어 biir\n');숨고르기()
        nattaat_randal(4,(너비,높이))
        yónnee_SMS('큰 창에서도 이어 biir\n');숨고르기()
        bës_butoñ(0xff1b);bës_butoñ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',yónnee_SMS(':wq\n'))
        Këmb_xëyma=bytearray();toxal_xëyma_630ba093.retrbinary('RETR 크기자료.txt',Këmb_xëyma.extend)
        assert Këmb_xëyma=='미저장 한글 mbir\n작은 창에서도 이어 biir\n큰 창에서도 이어 biir\n'.encode(),Këmb_xëyma
        luñutu_tolluwaay().save(str(결과경로/(tolluwaay_SMS+'-large.png')))
        # 두 번째 창은 xayma_bi_teew tolluwaay, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        daw=len(làq_Dënk);bës_xëyma(70,16);기다리기(b'TERMINAL FOCUS 2',daw)
        assert 'TERMINAL SIZE 68x19' in Wëreef('terminal size')
        daw=len(làq_Dënk);bës_xëyma(180,16);기다리기(b'TERMINAL FOCUS 1',daw);luñutu_tolluwaay()
        nattaat_randal(4,(-너비,-높이));luñutu_tolluwaay().save(str(결과경로/(tolluwaay_SMS+'-small.png')))
        # tolluwaay soppi_xëyma_16f64fe4 woñeeku_xëyma X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        daw=len(làq_Dënk);bës_xëyma(palanteer[0]+palanteer[2]-20,palanteer[1]+15);기다리기(b'TERMINAL FOCUS 2',daw)
        assert 'RESIZE CLOSED' in Wëreef('echo RESIZE CLOSED')
        print('PASS:',tolluwaay_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if toxal_xëyma_630ba093:toxal_xëyma_630ba093.close()
        if lu_soree_xëyma:lu_soree_xëyma.close()
        if yokkute_xëyma.poll() is None:
            yokkute_xëyma.terminate()
            try:yokkute_xëyma.wait(timeout=8)
            except subprocess.TimeoutExpired:yokkute_xëyma.kill();yokkute_xëyma.wait()
        tànnkat_a916db4e.close();yokkute_xëyma.stdout.close();(결과경로/(tolluwaay_SMS+'.log')).write_bytes(làq_Dënk)


def daw():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    làq_Dënk={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);làq_Dënk['resolutions'].append([너비,높이])
        làq_Dënk.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(làq_Dënk,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':daw()
