#!/usr/bin/env python3
"""real_ma_lumotlar QEMU/VNC에서 Terminal 모서리 tortib_o_tkazmoq_VALUE·kursor·동적 belgi_VALUE in_kiritish·tahrirlamoq_VALUE tarkib_VALUE 보존를 검사한다."""
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
from ishchi_stol_ko_rinish import EXACT_VALUE
from bajarmoq_buyruq import Project_ildiz


def 창크기시험(너비, 높이, o_lchov_yo_l):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    o_lcham_SMS = '{}x{}'.format(너비, 높이)
    Jarayon_VALUE = subprocess.Popen(['python3', str(Project_ildiz/'Vositalar/bajarmoq_buyruq.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', o_lcham_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tanlagich_a916db4e = selectors.DefaultSelector(); tanlagich_a916db4e.register(Jarayon_VALUE.stdout, selectors.EVENT_READ)
    LOG_satr = bytearray(); masofaviy_VALUE = None; uzatish_VALUE = None; kursor_yashirin=[False]

    def 기다리기(ko_rsatmoq_VALUE, Bajarish=0):
        마감 = time.monotonic() + 60
        while ko_rsatmoq_VALUE not in LOG_satr[Bajarish:]:
            if time.monotonic() > 마감 or Jarayon_VALUE.poll() is not None or b'HALTED' in LOG_satr or b'PANIC:' in LOG_satr:
                raise AssertionError(LOG_satr[Bajarish:].decode('utf-8', 'replace'))
            for hodisa, _ in tanlagich_a916db4e.select(.1):
                ma_lumotlar = hodisa.fileobj.read(65536)
                if ma_lumotlar: LOG_satr.extend(ma_lumotlar)
        return LOG_satr[Bajarish:].decode('utf-8', 'replace')

    def chertmoq_tugma(ramz, 눌림=True): masofaviy_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ramz))

    def SMS_yuborish(Matn):
        Bajarish = len(LOG_satr)
        for belgi_VALUE in Matn:
            ramz = 0xff0d if belgi_VALUE == '\n' else ord(belgi_VALUE) if ord(belgi_VALUE) < 256 else 0x1000000 | ord(belgi_VALUE)
            chertmoq_tugma(ramz); chertmoq_tugma(ramz, False)
        return Bajarish

    def qobiq(Matn): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_yuborish(Matn+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Vertikal_holat, 눌림): masofaviy_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Vertikal_holat))

    def chertmoq_VALUE(가로, Vertikal_holat): 가리키기(가로, Vertikal_holat, 1); 가리키기(가로, Vertikal_holat, 0)

    def nuqtali_rasm_rasm():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_ma_lumotlar 너비를 쓴다.
        masofaviy_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        chizish_VALUE = Image.new('RGB', (너비, 높이)); soha_VALUE = 0
        while True:
            종류 = EXACT_VALUE(masofaviy_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uzunlik_VALUE = struct.unpack('>I', EXACT_VALUE(masofaviy_VALUE, 7)[3:])[0]; EXACT_VALUE(masofaviy_VALUE, uzunlik_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(masofaviy_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Vertikal_holat, 폭, uzunlik_VALUE, kodlash_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(masofaviy_VALUE, 12))
                if kodlash_VALUE == -239:
                    assert 폭==0 and uzunlik_VALUE==0, 'remote cursor must be hidden'
                    kursor_yashirin[0]=True
                    continue
                assert kodlash_VALUE == 0 and 가로+폭 <= 너비 and Vertikal_holat+uzunlik_VALUE <= 높이
                chizish_VALUE.paste(Image.frombytes('RGB', (폭, uzunlik_VALUE), EXACT_VALUE(masofaviy_VALUE, 폭*uzunlik_VALUE*4), 'raw', 'BGRX'), (가로, Vertikal_holat))
                soha_VALUE += 폭*uzunlik_VALUE
            if soha_VALUE:
                assert soha_VALUE == 너비*높이, soha_VALUE
                return chizish_VALUE

    def chek_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            chizish_VALUE = nuqtali_rasm_rasm()
            if chizish_VALUE.getpixel(koordinat_VALUE) == 색: return chizish_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, chizish_VALUE.getpixel(koordinat_VALUE), 색))

    def uzatmoq_Fayllar(Nomi, ma_lumotlar): uzatish_VALUE.storbinary('STOR '+Nomi, io.BytesIO(ma_lumotlar))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+o_lcham_SMS+' RGB32').encode() in LOG_satr
        print('BOOT:', o_lcham_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_satr).group(1))
        masofaviy_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(masofaviy_VALUE, 12) == b'RFB 003.008\n'; masofaviy_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(masofaviy_VALUE, EXACT_VALUE(masofaviy_VALUE, 1)[0]); masofaviy_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(masofaviy_VALUE, 4) == b'\0'*4; masofaviy_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(masofaviy_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(masofaviy_VALUE, struct.unpack('>I', 초기[20:])[0])
        masofaviy_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        masofaviy_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        chek_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for hodisa,_ in tanlagich_a916db4e.select(.02):
                    ma_lumotlar=hodisa.fileobj.read(65536)
                    if ma_lumotlar:LOG_satr.extend(ma_lumotlar)
        oyna=[12,48,568,360]
        def tasdiqlamoq_o_lcham():
            ustun_VALUE,ROW_VALUE=(oyna[2]-24)//8,(oyna[3]-56)//16
            Matn=qobiq('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ustun_VALUE,ROW_VALUE) in Matn,Matn
            # real_ma_lumotlar oyna 테두리: 단지 Hajmi so_rov_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            chek_piksel((oyna[0],oyna[1]),(32,80,144))
            chizish_VALUE=chek_piksel((oyna[0]+oyna[2]-1,oyna[1]+oyna[3]-1),(39,49,64))
            return chizish_VALUE
        def 모서리(방향):
            return (oyna[0]+(3 if 방향 in (1,3) else oyna[2]-4),oyna[1]+(3 if 방향<=2 else oyna[3]-4))
        def o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(방향,차이,tugma=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            chek_piksel(흰점,(255,255,255))
            가리키기(가,세,tugma)
            끝가=max(0,min(너비-1,가+차이[0]));to_xtatmoq_Vertikal=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,to_xtatmoq_Vertikal,tugma);가리키기(끝가,to_xtatmoq_Vertikal,0);숨고르기()
            if tugma==1:
                LEFT_VALUE,위,폭,uzunlik_VALUE=oyna;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+uzunlik_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+to_xtatmoq_Vertikal-세))
                else:아래=max(위+216,min(높이,아래+to_xtatmoq_Vertikal-세))
                oyna[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        tasdiqlamoq_o_lcham();assert kursor_yashirin[0]
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(-100,-60),4);tasdiqlamoq_o_lcham() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(방향,차이);tasdiqlamoq_o_lcham()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_yuborish("echo '"+긴글+"'");숨고르기()
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(-1000,-1000));assert oyna[2:]==[360,216]
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(너비,높이))
        Bajarish=SMS_yuborish('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Bajarish);tasdiqlamoq_o_lcham()
        # vi가 tahrirlamoq_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        qobiq('ftpd start')
        uzatish_VALUE=ftplib.FTP();uzatish_VALUE.encoding='utf-8';uzatish_VALUE.connect('127.0.0.1',접속번호,timeout=20);uzatish_VALUE.login()
        기다리기(b'NORMAL',SMS_yuborish('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_yuborish('i미저장 한글 ma_lumotlar\n'));숨고르기()
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((oyna[3]-56)//16)).encode() in LOG_satr[-4096:]
        SMS_yuborish('작은 창에서도 이어 Yozish\n');숨고르기()
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(너비,높이))
        SMS_yuborish('큰 창에서도 이어 Yozish\n');숨고르기()
        chertmoq_tugma(0xff1b);chertmoq_tugma(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_yuborish(':wq\n'))
        tarkib_VALUE=bytearray();uzatish_VALUE.retrbinary('RETR 크기자료.txt',tarkib_VALUE.extend)
        assert tarkib_VALUE=='미저장 한글 ma_lumotlar\n작은 창에서도 이어 Yozish\n큰 창에서도 이어 Yozish\n'.encode(),tarkib_VALUE
        tasdiqlamoq_o_lcham().save(str(o_lchov_yo_l/(o_lcham_SMS+'-large.png')))
        # 두 번째 창은 sukut_bo_yicha_qiymat Hajmi, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Bajarish=len(LOG_satr);chertmoq_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Bajarish)
        assert 'TERMINAL SIZE 68x19' in qobiq('terminal size')
        Bajarish=len(LOG_satr);chertmoq_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Bajarish);tasdiqlamoq_o_lcham()
        o_lchamni_o_zgartirmoq_tortib_o_tkazmoq(4,(-너비,-높이));tasdiqlamoq_o_lcham().save(str(o_lchov_yo_l/(o_lcham_SMS+'-small.png')))
        # Hajmi o_zgartirmoq_VALUE Orqaga_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Bajarish=len(LOG_satr);chertmoq_VALUE(oyna[0]+oyna[2]-20,oyna[1]+15);기다리기(b'TERMINAL FOCUS 2',Bajarish)
        assert 'RESIZE CLOSED' in qobiq('echo RESIZE CLOSED')
        print('PASS:',o_lcham_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if uzatish_VALUE:uzatish_VALUE.close()
        if masofaviy_VALUE:masofaviy_VALUE.close()
        if Jarayon_VALUE.poll() is None:
            Jarayon_VALUE.terminate()
            try:Jarayon_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Jarayon_VALUE.kill();Jarayon_VALUE.wait()
        tanlagich_a916db4e.close();Jarayon_VALUE.stdout.close();(o_lchov_yo_l/(o_lcham_SMS+'.log')).write_bytes(LOG_satr)


def Bajarish():
    o_lchov_yo_l=Project_ildiz/'build/verification/resize';o_lchov_yo_l.mkdir(parents=True,exist_ok=True)
    LOG_satr={'passed':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,o_lchov_yo_l);LOG_satr['resolutions'].append([너비,높이])
        LOG_satr.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(o_lchov_yo_l/'report.json').write_text(json.dumps(LOG_satr,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Bajarish()
