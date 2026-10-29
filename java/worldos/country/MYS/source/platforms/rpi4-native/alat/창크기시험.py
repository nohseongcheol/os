#!/usr/bin/env python3
"""sebenar_data QEMU/VNC에서 Terminal 모서리 seret_VALUE·penuding·동적 aksara_VALUE 칸·edit_VALUE Kandungan_VALUE 보존를 검사한다."""
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
from meja_lihat import EXACT_VALUE
from laksanakan_perintah import projek_akar


def 창크기시험(너비, 높이, ukuran_laluan):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); nombor_port = 임시.getsockname()[1]
    saiz_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(projek_akar/'alat/laksanakan_perintah.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(nombor_port), '--resolution', saiz_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_baris = bytearray(); jauh_VALUE = None; pindah_VALUE = None; penuding_Tersembunyi=[False]

    def 기다리기(tayang_VALUE, Jalan=0):
        마감 = time.monotonic() + 60
        while tayang_VALUE not in LOG_baris[Jalan:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_baris or b'PANIC:' in LOG_baris:
                raise AssertionError(LOG_baris[Jalan:].decode('utf-8', 'replace'))
            for Peristiwa, _ in 선택기.select(.1):
                data = Peristiwa.fileobj.read(65536)
                if data: LOG_baris.extend(data)
        return LOG_baris[Jalan:].decode('utf-8', 'replace')

    def klik_butang(simbol, 눌림=True): jauh_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def hantar_SMS(Teks):
        Jalan = len(LOG_baris)
        for aksara_VALUE in Teks:
            simbol = 0xff0d if aksara_VALUE == '\n' else ord(aksara_VALUE) if ord(aksara_VALUE) < 256 else 0x1000000 | ord(aksara_VALUE)
            klik_butang(simbol); klik_butang(simbol, False)
        return Jalan

    def cangkerang(Teks): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', hantar_SMS(Teks+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Menegak_jawatan, 눌림): jauh_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Menegak_jawatan))

    def klik_VALUE(가로, Menegak_jawatan): 가리키기(가로, Menegak_jawatan, 1); 가리키기(가로, Menegak_jawatan, 0)

    def peta_bit_imej():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 sebenar_data 너비를 쓴다.
        jauh_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        lukisan_VALUE = Image.new('RGB', (너비, 높이)); bidang_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(jauh_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                kepanjangan_VALUE = struct.unpack('>I', EXACT_VALUE(jauh_VALUE, 7)[3:])[0]; EXACT_VALUE(jauh_VALUE, kepanjangan_VALUE); continue
            assert 종류 == 0, 종류
            item_COUNT = struct.unpack('>H', EXACT_VALUE(jauh_VALUE, 3)[1:])[0]
            for _ in range(item_COUNT):
                가로, Menegak_jawatan, 폭, kepanjangan_VALUE, pengekodan_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(jauh_VALUE, 12))
                if pengekodan_VALUE == -239:
                    assert 폭==0 and kepanjangan_VALUE==0, 'remote cursor must be hidden'
                    penuding_Tersembunyi[0]=True
                    continue
                assert pengekodan_VALUE == 0 and 가로+폭 <= 너비 and Menegak_jawatan+kepanjangan_VALUE <= 높이
                lukisan_VALUE.paste(Image.frombytes('RGB', (폭, kepanjangan_VALUE), EXACT_VALUE(jauh_VALUE, 폭*kepanjangan_VALUE*4), 'raw', 'BGRX'), (가로, Menegak_jawatan))
                bidang_VALUE_9285603e += 폭*kepanjangan_VALUE
            if bidang_VALUE_9285603e:
                assert bidang_VALUE_9285603e == 너비*높이, bidang_VALUE_9285603e
                return lukisan_VALUE

    def cek_pel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            lukisan_VALUE = peta_bit_imej()
            if lukisan_VALUE.getpixel(koordinat_VALUE) == 색: return lukisan_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, lukisan_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Fail(Nama, data): pindah_VALUE.storbinary('STOR '+Nama, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+saiz_SMS+' RGB32').encode() in LOG_baris
        print('BOOT:', saiz_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_baris).group(1))
        jauh_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(jauh_VALUE, 12) == b'RFB 003.008\n'; jauh_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(jauh_VALUE, EXACT_VALUE(jauh_VALUE, 1)[0]); jauh_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(jauh_VALUE, 4) == b'\0'*4; jauh_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(jauh_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(jauh_VALUE, struct.unpack('>I', 초기[20:])[0])
        jauh_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        jauh_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        cek_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Peristiwa,_ in 선택기.select(.02):
                    data=Peristiwa.fileobj.read(65536)
                    if data:LOG_baris.extend(data)
        Tetingkap=[12,48,568,360]
        def tentu_sahkan_saiz():
            lajur_VALUE,ROW_VALUE=(Tetingkap[2]-24)//8,(Tetingkap[3]-56)//16
            Teks=cangkerang('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(lajur_VALUE,ROW_VALUE) in Teks,Teks
            # sebenar_data Tetingkap 테두리: 단지 Saiz pertanyaan_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            cek_pel((Tetingkap[0],Tetingkap[1]),(32,80,144))
            lukisan_VALUE=cek_pel((Tetingkap[0]+Tetingkap[2]-1,Tetingkap[1]+Tetingkap[3]-1),(39,49,64))
            return lukisan_VALUE
        def 모서리(방향):
            return (Tetingkap[0]+(3 if 방향 in (1,3) else Tetingkap[2]-4),Tetingkap[1]+(3 if 방향<=2 else Tetingkap[3]-4))
        def saiz_semula_seret(방향,차이,Butang=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            cek_pel(흰점,(255,255,255))
            가리키기(가,세,Butang)
            끝가=max(0,min(너비-1,가+차이[0]));tamat_Menegak=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,tamat_Menegak,Butang);가리키기(끝가,tamat_Menegak,0);숨고르기()
            if Butang==1:
                LEFT_VALUE,위,폭,kepanjangan_VALUE=Tetingkap;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+kepanjangan_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+tamat_Menegak-세))
                else:아래=max(위+216,min(높이,아래+tamat_Menegak-세))
                Tetingkap[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        tentu_sahkan_saiz();assert penuding_Tersembunyi[0]
        saiz_semula_seret(4,(-100,-60),4);tentu_sahkan_saiz() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            saiz_semula_seret(방향,차이);tentu_sahkan_saiz()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        hantar_SMS("echo '"+긴글+"'");숨고르기()
        saiz_semula_seret(4,(-1000,-1000));assert Tetingkap[2:]==[360,216]
        saiz_semula_seret(4,(너비,높이))
        Jalan=hantar_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Jalan);tentu_sahkan_saiz()
        # vi가 edit_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        cangkerang('ftpd start')
        pindah_VALUE=ftplib.FTP();pindah_VALUE.encoding='utf-8';pindah_VALUE.connect('127.0.0.1',nombor_port,timeout=20);pindah_VALUE.login()
        기다리기(b'NORMAL',hantar_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',hantar_SMS('i미저장 한글 data\n'));숨고르기()
        saiz_semula_seret(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Tetingkap[3]-56)//16)).encode() in LOG_baris[-4096:]
        hantar_SMS('작은 창에서도 이어 Tulis\n');숨고르기()
        saiz_semula_seret(4,(너비,높이))
        hantar_SMS('큰 창에서도 이어 Tulis\n');숨고르기()
        klik_butang(0xff1b);klik_butang(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',hantar_SMS(':wq\n'))
        Kandungan_VALUE=bytearray();pindah_VALUE.retrbinary('RETR 크기자료.txt',Kandungan_VALUE.extend)
        assert Kandungan_VALUE=='미저장 한글 data\n작은 창에서도 이어 Tulis\n큰 창에서도 이어 Tulis\n'.encode(),Kandungan_VALUE
        tentu_sahkan_saiz().save(str(ukuran_laluan/(saiz_SMS+'-large.png')))
        # 두 번째 창은 nilai_lalai Saiz, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Jalan=len(LOG_baris);klik_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Jalan)
        assert 'TERMINAL SIZE 68x19' in cangkerang('terminal size')
        Jalan=len(LOG_baris);klik_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Jalan);tentu_sahkan_saiz()
        saiz_semula_seret(4,(-너비,-높이));tentu_sahkan_saiz().save(str(ukuran_laluan/(saiz_SMS+'-small.png')))
        # Saiz ubah_VALUE BACK_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Jalan=len(LOG_baris);klik_VALUE(Tetingkap[0]+Tetingkap[2]-20,Tetingkap[1]+15);기다리기(b'TERMINAL FOCUS 2',Jalan)
        assert 'RESIZE CLOSED' in cangkerang('echo RESIZE CLOSED')
        print('PASS:',saiz_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if pindah_VALUE:pindah_VALUE.close()
        if jauh_VALUE:jauh_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
        선택기.close();Proses_VALUE.stdout.close();(ukuran_laluan/(saiz_SMS+'.log')).write_bytes(LOG_baris)


def Jalan():
    ukuran_laluan=projek_akar/'build/verification/resize';ukuran_laluan.mkdir(parents=True,exist_ok=True)
    LOG_baris={'passed':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ukuran_laluan);LOG_baris['resolutions'].append([너비,높이])
        LOG_baris.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ukuran_laluan/'report.json').write_text(json.dumps(LOG_baris,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Jalan()
