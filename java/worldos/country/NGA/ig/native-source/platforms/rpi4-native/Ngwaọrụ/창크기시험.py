#!/usr/bin/env python3
"""ǹdịnezie_datà QEMU/VNC에서 터미널 모서리 dọkpụrụ_valuu·nrụaka·동적 mkpụrụedemede_valuu oghere_ndebà·dezìmà_valuu ndịnà_valuu 보존를 검사한다."""
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
from desktọpụ_lèe import 정확한값
from mee_nnyemiwu import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ụha_SMS = '{}x{}'.format(너비, 높이)
    ùsòrò_valuu_6712bde7 = subprocess.Popen(['python3', str(기준/'Ngwaọrụ/mee_nnyemiwu.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ụha_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ihe_nhọpụta_a916db4e = selectors.DefaultSelector(); ihe_nhọpụta_a916db4e.register(ùsòrò_valuu_6712bde7.stdout, selectors.EVENT_READ)
    ndekọ_NDEKỌ = bytearray(); ebe_dị̀anyā_valuu = None; dògharịa_valuu = None; nrụaka_nzòròèzo=[False]

    def 기다리기(gòsi_valuu, Bido=0):
        마감 = time.monotonic() + 60
        while gòsi_valuu not in ndekọ_NDEKỌ[Bido:]:
            if time.monotonic() > 마감 or ùsòrò_valuu_6712bde7.poll() is not None or b'HALTED' in ndekọ_NDEKỌ or b'PANIC:' in ndekọ_NDEKỌ:
                raise AssertionError(ndekọ_NDEKỌ[Bido:].decode('utf-8', 'replace'))
            for mmèrème, _ in ihe_nhọpụta_a916db4e.select(.1):
                datà = mmèrème.fileobj.read(65536)
                if datà: ndekọ_NDEKỌ.extend(datà)
        return ndekọ_NDEKỌ[Bido:].decode('utf-8', 'replace')

    def pịkịnye_ọdụmbi(adimara, 눌림=True): ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHI', 4, int(눌림), 0, adimara))

    def zipu_SMS(SMS):
        Bido = len(ndekọ_NDEKỌ)
        for mkpụrụedemede_valuu in SMS:
            adimara = 0xff0d if mkpụrụedemede_valuu == '\n' else ord(mkpụrụedemede_valuu) if ord(mkpụrụedemede_valuu) < 256 else 0x1000000 | ord(mkpụrụedemede_valuu)
            pịkịnye_ọdụmbi(adimara); pịkịnye_ọdụmbi(adimara, False)
        return Bido

    def nkọwannyemiwu(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', zipu_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def pịkịnye_valuu(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ǹdịnezie_datà 너비를 쓴다.
        ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        osise_valuu = Image.new('RGB', (너비, 높이)); kàtigori_valuu = 0
        while True:
            종류 = 정확한값(ebe_dị̀anyā_valuu, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ogologo_valuu = struct.unpack('>I', 정확한값(ebe_dị̀anyā_valuu, 7)[3:])[0]; 정확한값(ebe_dị̀anyā_valuu, ogologo_valuu); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ebe_dị̀anyā_valuu, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ogologo_valuu, ntinye_koòdù_valuu = struct.unpack('>HHHHi', 정확한값(ebe_dị̀anyā_valuu, 12))
                if ntinye_koòdù_valuu == -239:
                    assert 폭==0 and ogologo_valuu==0, 'remote cursor must be hidden'
                    nrụaka_nzòròèzo[0]=True
                    continue
                assert ntinye_koòdù_valuu == 0 and 가로+폭 <= 너비 and 세로+ogologo_valuu <= 높이
                osise_valuu.paste(Image.frombytes('RGB', (폭, ogologo_valuu), 정확한값(ebe_dị̀anyā_valuu, 폭*ogologo_valuu*4), 'raw', 'BGRX'), (가로, 세로))
                kàtigori_valuu += 폭*ogologo_valuu
            if kàtigori_valuu:
                assert kàtigori_valuu == 너비*높이, kàtigori_valuu
                return osise_valuu

    def cheèk_pel(nsòezikọebē_valuu, 색):
        마감 = time.monotonic()+10
        while True:
            osise_valuu = bitmap_foto()
            if osise_valuu.getpixel(nsòezikọebē_valuu) == 색: return osise_valuu
            if time.monotonic() > 마감: raise AssertionError((nsòezikọebē_valuu, osise_valuu.getpixel(nsòezikọebē_valuu), 색))

    def bùlie_Ndi_ọbọakwụkwọ(Aha, datà): dògharịa_valuu.storbinary('STOR '+Aha, io.BytesIO(datà))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ụha_SMS+' RGB32').encode() in ndekọ_NDEKỌ
        print('BOOT:', ụha_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ndekọ_NDEKỌ).group(1))
        ebe_dị̀anyā_valuu = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ebe_dị̀anyā_valuu, 12) == b'RFB 003.008\n'; ebe_dị̀anyā_valuu.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ebe_dị̀anyā_valuu, 정확한값(ebe_dị̀anyā_valuu, 1)[0]); ebe_dị̀anyā_valuu.sendall(b'\x01')
        assert 정확한값(ebe_dị̀anyā_valuu, 4) == b'\0'*4; ebe_dị̀anyā_valuu.sendall(b'\x01')
        초기 = 정확한값(ebe_dị̀anyā_valuu, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ebe_dị̀anyā_valuu, struct.unpack('>I', 초기[20:])[0])
        ebe_dị̀anyā_valuu.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ebe_dị̀anyā_valuu.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cheèk_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for mmèrème,_ in ihe_nhọpụta_a916db4e.select(.02):
                    datà=mmèrème.fileobj.read(65536)
                    if datà:ndekọ_NDEKỌ.extend(datà)
        windò=[12,48,568,360]
        def nkwàdo_eziokwū_ụha():
            ọgbàràogō_valuu,ihendekọta_valuu=(windò[2]-24)//8,(windò[3]-56)//16
            SMS=nkọwannyemiwu('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ọgbàràogō_valuu,ihendekọta_valuu) in SMS,SMS
            # ǹdịnezie_datà windò 테두리: 단지 Ụhara mgbaajụjụ_valuu 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cheèk_pel((windò[0],windò[1]),(32,80,144))
            osise_valuu=cheèk_pel((windò[0]+windò[2]-1,windò[1]+windò[3]-1),(39,49,64))
            return osise_valuu
        def 모서리(방향):
            return (windò[0]+(3 if 방향 in (1,3) else windò[2]-4),windò[1]+(3 if 방향<=2 else windò[3]-4))
        def mmegharị_nhà_dọkpụrụ(방향,차이,ọdụmbi=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cheèk_pel(흰점,(255,255,255))
            가리키기(가,세,ọdụmbi)
            끝가=max(0,min(너비-1,가+차이[0]));mèdebe_Ndepụta_Nkwụọtọ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,mèdebe_Ndepụta_Nkwụọtọ,ọdụmbi);가리키기(끝가,mèdebe_Ndepụta_Nkwụọtọ,0);숨고르기()
            if ọdụmbi==1:
                왼,위,폭,ogologo_valuu=windò;오른,아래=왼+폭,위+ogologo_valuu
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+mèdebe_Ndepụta_Nkwụọtọ-세))
                else:아래=max(위+216,min(높이,아래+mèdebe_Ndepụta_Nkwụọtọ-세))
                windò[:]=[왼,위,오른-왼,아래-위]
        nkwàdo_eziokwū_ụha();assert nrụaka_nzòròèzo[0]
        mmegharị_nhà_dọkpụrụ(4,(-100,-60),4);nkwàdo_eziokwū_ụha() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            mmegharị_nhà_dọkpụrụ(방향,차이);nkwàdo_eziokwū_ụha()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        zipu_SMS("echo '"+긴글+"'");숨고르기()
        mmegharị_nhà_dọkpụrụ(4,(-1000,-1000));assert windò[2:]==[360,216]
        mmegharị_nhà_dọkpụrụ(4,(너비,높이))
        Bido=zipu_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Bido);nkwàdo_eziokwū_ụha()
        # vi가 dezìmà_valuu 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        nkọwannyemiwu('ftpd start')
        dògharịa_valuu=ftplib.FTP();dògharịa_valuu.encoding='utf-8';dògharịa_valuu.connect('127.0.0.1',접속번호,timeout=20);dògharịa_valuu.login()
        기다리기(b'NORMAL',zipu_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',zipu_SMS('i미저장 한글 datà\n'));숨고르기()
        mmegharị_nhà_dọkpụrụ(4,(-너비,-높이))
        # ANSI ihendekọta_valuu 이동에 새 ihendekọta_valuu 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((windò[3]-56)//16)).encode() in ndekọ_NDEKỌ[-4096:]
        zipu_SMS('작은 창에서도 이어 Chekwaa_ozi\n');숨고르기()
        mmegharị_nhà_dọkpụrụ(4,(너비,높이))
        zipu_SMS('큰 창에서도 이어 Chekwaa_ozi\n');숨고르기()
        pịkịnye_ọdụmbi(0xff1b);pịkịnye_ọdụmbi(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',zipu_SMS(':wq\n'))
        ndịnà_valuu=bytearray();dògharịa_valuu.retrbinary('RETR 크기자료.txt',ndịnà_valuu.extend)
        assert ndịnà_valuu=='미저장 한글 datà\n작은 창에서도 이어 Chekwaa_ozi\n큰 창에서도 이어 Chekwaa_ozi\n'.encode(),ndịnà_valuu
        nkwàdo_eziokwū_ụha().save(str(결과경로/(ụha_SMS+'-large.png')))
        # 두 번째 창은 Ngwa_ihe_dịadị Ụhara, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Bido=len(ndekọ_NDEKỌ);pịkịnye_valuu(70,16);기다리기(b'TERMINAL FOCUS 2',Bido)
        assert 'TERMINAL SIZE 68x19' in nkọwannyemiwu('terminal size')
        Bido=len(ndekọ_NDEKỌ);pịkịnye_valuu(180,16);기다리기(b'TERMINAL FOCUS 1',Bido);nkwàdo_eziokwū_ụha()
        mmegharị_nhà_dọkpụrụ(4,(-너비,-높이));nkwàdo_eziokwū_ụha().save(str(결과경로/(ụha_SMS+'-small.png')))
        # Ụhara gbanwèe_valuu Àzụ_valuu X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Bido=len(ndekọ_NDEKỌ);pịkịnye_valuu(windò[0]+windò[2]-20,windò[1]+15);기다리기(b'TERMINAL FOCUS 2',Bido)
        assert 'RESIZE CLOSED' in nkọwannyemiwu('echo RESIZE CLOSED')
        print('PASS:',ụha_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if dògharịa_valuu:dògharịa_valuu.close()
        if ebe_dị̀anyā_valuu:ebe_dị̀anyā_valuu.close()
        if ùsòrò_valuu_6712bde7.poll() is None:
            ùsòrò_valuu_6712bde7.terminate()
            try:ùsòrò_valuu_6712bde7.wait(timeout=8)
            except subprocess.TimeoutExpired:ùsòrò_valuu_6712bde7.kill();ùsòrò_valuu_6712bde7.wait()
        ihe_nhọpụta_a916db4e.close();ùsòrò_valuu_6712bde7.stdout.close();(결과경로/(ụha_SMS+'.log')).write_bytes(ndekọ_NDEKỌ)


def Bido():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    ndekọ_NDEKỌ={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);ndekọ_NDEKỌ['resolutions'].append([너비,높이])
        ndekọ_NDEKỌ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(ndekọ_NDEKỌ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Bido()
