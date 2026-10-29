#!/usr/bin/env python3
"""raun_gögn QEMU/VNC에서 Skjáhermir 모서리 draga_VALUE·bendill·동적 stafur_VALUE rauf_færsla·breyta_VALUE Efni_VALUE 보존를 검사한다."""
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
from skjáborð_Sýn import EXACT_VALUE
from keyra_skipun import verk_rót


def 창크기시험(너비, 높이, mæld_stærð_slóð):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); tengisnúmer = 임시.getsockname()[1]
    breyta_stærð_SMS = '{}x{}'.format(너비, 높이)
    Ferli_VALUE = subprocess.Popen(['python3', str(verk_rót/'Verkfæri/keyra_skipun.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(tengisnúmer), '--resolution', breyta_stærð_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    val_a916db4e = selectors.DefaultSelector(); val_a916db4e.register(Ferli_VALUE.stdout, selectors.EVENT_READ)
    LOG_lína = bytearray(); fjartengdur_VALUE = None; flytja_VALUE = None; bendill_falið=[False]

    def 기다리기(sýna_VALUE, Keyra_2=0):
        마감 = time.monotonic() + 60
        while sýna_VALUE not in LOG_lína[Keyra_2:]:
            if time.monotonic() > 마감 or Ferli_VALUE.poll() is not None or b'HALTED' in LOG_lína or b'PANIC:' in LOG_lína:
                raise AssertionError(LOG_lína[Keyra_2:].decode('utf-8', 'replace'))
            for atvik, _ in val_a916db4e.select(.1):
                gögn = atvik.fileobj.read(65536)
                if gögn: LOG_lína.extend(gögn)
        return LOG_lína[Keyra_2:].decode('utf-8', 'replace')

    def smella_hnappur(tákn, 눌림=True): fjartengdur_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, tákn))

    def senda_SMS(Texti):
        Keyra_2 = len(LOG_lína)
        for stafur_VALUE in Texti:
            tákn = 0xff0d if stafur_VALUE == '\n' else ord(stafur_VALUE) if ord(stafur_VALUE) < 256 else 0x1000000 | ord(stafur_VALUE)
            smella_hnappur(tákn); smella_hnappur(tákn, False)
        return Keyra_2

    def skel(Texti): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', senda_SMS(Texti+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Lóðrétt_staða, 눌림): fjartengdur_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Lóðrétt_staða))

    def smella_VALUE(가로, Lóðrétt_staða): 가리키기(가로, Lóðrétt_staða, 1); 가리키기(가로, Lóðrétt_staða, 0)

    def punktamynd_mynd():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 raun_gögn 너비를 쓴다.
        fjartengdur_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        teikning_VALUE = Image.new('RGB', (너비, 높이)); svæði_VALUE = 0
        while True:
            종류 = EXACT_VALUE(fjartengdur_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lengd_VALUE = struct.unpack('>I', EXACT_VALUE(fjartengdur_VALUE, 7)[3:])[0]; EXACT_VALUE(fjartengdur_VALUE, lengd_VALUE); continue
            assert 종류 == 0, 종류
            vara_COUNT = struct.unpack('>H', EXACT_VALUE(fjartengdur_VALUE, 3)[1:])[0]
            for _ in range(vara_COUNT):
                가로, Lóðrétt_staða, 폭, lengd_VALUE, kóðun_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(fjartengdur_VALUE, 12))
                if kóðun_VALUE == -239:
                    assert 폭==0 and lengd_VALUE==0, 'remote cursor must be hidden'
                    bendill_falið[0]=True
                    continue
                assert kóðun_VALUE == 0 and 가로+폭 <= 너비 and Lóðrétt_staða+lengd_VALUE <= 높이
                teikning_VALUE.paste(Image.frombytes('RGB', (폭, lengd_VALUE), EXACT_VALUE(fjartengdur_VALUE, 폭*lengd_VALUE*4), 'raw', 'BGRX'), (가로, Lóðrétt_staða))
                svæði_VALUE += 폭*lengd_VALUE
            if svæði_VALUE:
                assert svæði_VALUE == 너비*높이, svæði_VALUE
                return teikning_VALUE

    def athuga_díll(hnit_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            teikning_VALUE = punktamynd_mynd()
            if teikning_VALUE.getpixel(hnit_VALUE) == 색: return teikning_VALUE
            if time.monotonic() > 마감: raise AssertionError((hnit_VALUE, teikning_VALUE.getpixel(hnit_VALUE), 색))

    def hlaða_upp_Skrár(Heiti, gögn): flytja_VALUE.storbinary('STOR '+Heiti, io.BytesIO(gögn))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+breyta_stærð_SMS+' RGB32').encode() in LOG_lína
        print('BOOT:', breyta_stærð_SMS, flush=True)
        fjartengdur_númer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_lína).group(1))
        fjartengdur_VALUE = socket.create_connection(('127.0.0.1', fjartengdur_númer), timeout=20)
        assert EXACT_VALUE(fjartengdur_VALUE, 12) == b'RFB 003.008\n'; fjartengdur_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(fjartengdur_VALUE, EXACT_VALUE(fjartengdur_VALUE, 1)[0]); fjartengdur_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(fjartengdur_VALUE, 4) == b'\0'*4; fjartengdur_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(fjartengdur_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(fjartengdur_VALUE, struct.unpack('>I', 초기[20:])[0])
        fjartengdur_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjartengdur_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        athuga_díll((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for atvik,_ in val_a916db4e.select(.02):
                    gögn=atvik.fileobj.read(65536)
                    if gögn:LOG_lína.extend(gögn)
        Gluggi=[12,48,568,360]
        def sannprófa_breyta_stærð():
            COLUMN_VALUE,ROW_VALUE=(Gluggi[2]-24)//8,(Gluggi[3]-56)//16
            Texti=skel('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Texti,Texti
            # raun_gögn Gluggi 테두리: 단지 Stærð fyrirspurn_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            athuga_díll((Gluggi[0],Gluggi[1]),(32,80,144))
            teikning_VALUE=athuga_díll((Gluggi[0]+Gluggi[2]-1,Gluggi[1]+Gluggi[3]-1),(39,49,64))
            return teikning_VALUE
        def 모서리(방향):
            return (Gluggi[0]+(3 if 방향 in (1,3) else Gluggi[2]-4),Gluggi[1]+(3 if 방향<=2 else Gluggi[3]-4))
        def breyta_stærð_draga(방향,차이,hnappur=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            athuga_díll(흰점,(255,255,255))
            가리키기(가,세,hnappur)
            끝가=max(0,min(너비-1,가+차이[0]));ljúka_Lóðrétt=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ljúka_Lóðrétt,hnappur);가리키기(끝가,ljúka_Lóðrétt,0);숨고르기()
            if hnappur==1:
                LEFT_VALUE,위,폭,lengd_VALUE=Gluggi;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+lengd_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ljúka_Lóðrétt-세))
                else:아래=max(위+216,min(높이,아래+ljúka_Lóðrétt-세))
                Gluggi[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        sannprófa_breyta_stærð();assert bendill_falið[0]
        breyta_stærð_draga(4,(-100,-60),4);sannprófa_breyta_stærð() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            breyta_stærð_draga(방향,차이);sannprófa_breyta_stærð()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        senda_SMS("echo '"+긴글+"'");숨고르기()
        breyta_stærð_draga(4,(-1000,-1000));assert Gluggi[2:]==[360,216]
        breyta_stærð_draga(4,(너비,높이))
        Keyra_2=senda_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Keyra_2);sannprófa_breyta_stærð()
        # vi가 breyta_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        skel('ftpd start')
        flytja_VALUE=ftplib.FTP();flytja_VALUE.encoding='utf-8';flytja_VALUE.connect('127.0.0.1',tengisnúmer,timeout=20);flytja_VALUE.login()
        기다리기(b'NORMAL',senda_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',senda_SMS('i미저장 한글 gögn\n'));숨고르기()
        breyta_stærð_draga(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Gluggi[3]-56)//16)).encode() in LOG_lína[-4096:]
        senda_SMS('작은 창에서도 이어 Skrift\n');숨고르기()
        breyta_stærð_draga(4,(너비,높이))
        senda_SMS('큰 창에서도 이어 Skrift\n');숨고르기()
        smella_hnappur(0xff1b);smella_hnappur(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',senda_SMS(':wq\n'))
        Efni_VALUE=bytearray();flytja_VALUE.retrbinary('RETR 크기자료.txt',Efni_VALUE.extend)
        assert Efni_VALUE=='미저장 한글 gögn\n작은 창에서도 이어 Skrift\n큰 창에서도 이어 Skrift\n'.encode(),Efni_VALUE
        sannprófa_breyta_stærð().save(str(mæld_stærð_slóð/(breyta_stærð_SMS+'-large.png')))
        # 두 번째 창은 sjálfgildi Stærð, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Keyra_2=len(LOG_lína);smella_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Keyra_2)
        assert 'TERMINAL SIZE 68x19' in skel('terminal size')
        Keyra_2=len(LOG_lína);smella_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Keyra_2);sannprófa_breyta_stærð()
        breyta_stærð_draga(4,(-너비,-높이));sannprófa_breyta_stærð().save(str(mæld_stærð_slóð/(breyta_stærð_SMS+'-small.png')))
        # Stærð breyta_VALUE_16f64fe4 TIL_BAKA_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Keyra_2=len(LOG_lína);smella_VALUE(Gluggi[0]+Gluggi[2]-20,Gluggi[1]+15);기다리기(b'TERMINAL FOCUS 2',Keyra_2)
        assert 'RESIZE CLOSED' in skel('echo RESIZE CLOSED')
        print('PASS:',breyta_stærð_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if flytja_VALUE:flytja_VALUE.close()
        if fjartengdur_VALUE:fjartengdur_VALUE.close()
        if Ferli_VALUE.poll() is None:
            Ferli_VALUE.terminate()
            try:Ferli_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Ferli_VALUE.kill();Ferli_VALUE.wait()
        val_a916db4e.close();Ferli_VALUE.stdout.close();(mæld_stærð_slóð/(breyta_stærð_SMS+'.log')).write_bytes(LOG_lína)


def Keyra_2():
    mæld_stærð_slóð=verk_rót/'build/verification/resize';mæld_stærð_slóð.mkdir(parents=True,exist_ok=True)
    LOG_lína={'passed':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mæld_stærð_slóð);LOG_lína['resolutions'].append([너비,높이])
        LOG_lína.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mæld_stærð_slóð/'report.json').write_text(json.dumps(LOG_lína,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Keyra_2()
