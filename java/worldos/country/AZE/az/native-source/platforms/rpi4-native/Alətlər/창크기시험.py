#!/usr/bin/env python3
"""faktiki_verilənlər QEMU/VNC에서 Terminal 모서리 sürükləmək_VALUE·göstərici·동적 simvol_VALUE_068c2631 slot_daxiletmə·redaktə_VALUE Məzmun_VALUE 보존를 검사한다."""
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
from iş_masası_baxmaq import EXACT_VALUE
from icra_etmək_əmr import Project_kök


def 창크기시험(너비, 높이, ölçü_yol):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ölçünü_dəyişmək_SMS = '{}x{}'.format(너비, 높이)
    Proses_VALUE = subprocess.Popen(['python3', str(Project_kök/'Alətlər/icra_etmək_əmr.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ölçünü_dəyişmək_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector(); seçici_a916db4e.register(Proses_VALUE.stdout, selectors.EVENT_READ)
    LOG_yaz = bytearray(); uzaq_VALUE = None; ötürmə_VALUE = None; göstərici_gizli=[False]

    def 기다리기(göstərmək_VALUE, İcra_Et=0):
        마감 = time.monotonic() + 60
        while göstərmək_VALUE not in LOG_yaz[İcra_Et:]:
            if time.monotonic() > 마감 or Proses_VALUE.poll() is not None or b'HALTED' in LOG_yaz or b'PANIC:' in LOG_yaz:
                raise AssertionError(LOG_yaz[İcra_Et:].decode('utf-8', 'replace'))
            for hadisə, _ in seçici_a916db4e.select(.1):
                verilənlər = hadisə.fileobj.read(65536)
                if verilənlər: LOG_yaz.extend(verilənlər)
        return LOG_yaz[İcra_Et:].decode('utf-8', 'replace')

    def klikləmə_düymə(simvol, 눌림=True): uzaq_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simvol))

    def SMS_göndər(Mətn):
        İcra_Et = len(LOG_yaz)
        for simvol_VALUE_068c2631 in Mətn:
            simvol = 0xff0d if simvol_VALUE_068c2631 == '\n' else ord(simvol_VALUE_068c2631) if ord(simvol_VALUE_068c2631) < 256 else 0x1000000 | ord(simvol_VALUE_068c2631)
            klikləmə_düymə(simvol); klikləmə_düymə(simvol, False)
        return İcra_Et

    def örtük(Mətn): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_göndər(Mətn+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Şaquli_yerinə_qoymaq, 눌림): uzaq_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Şaquli_yerinə_qoymaq))

    def klikləmə_VALUE(가로, Şaquli_yerinə_qoymaq): 가리키기(가로, Şaquli_yerinə_qoymaq, 1); 가리키기(가로, Şaquli_yerinə_qoymaq, 0)

    def nöqtəli_təsvir_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktiki_verilənlər 너비를 쓴다.
        uzaq_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        rəsm_VALUE = Image.new('RGB', (너비, 높이)); sahə_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(uzaq_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uzunluq_VALUE = struct.unpack('>I', EXACT_VALUE(uzaq_VALUE, 7)[3:])[0]; EXACT_VALUE(uzaq_VALUE, uzunluq_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(uzaq_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Şaquli_yerinə_qoymaq, 폭, uzunluq_VALUE, kodlaşdırma_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(uzaq_VALUE, 12))
                if kodlaşdırma_VALUE == -239:
                    assert 폭==0 and uzunluq_VALUE==0, 'remote cursor must be hidden'
                    göstərici_gizli[0]=True
                    continue
                assert kodlaşdırma_VALUE == 0 and 가로+폭 <= 너비 and Şaquli_yerinə_qoymaq+uzunluq_VALUE <= 높이
                rəsm_VALUE.paste(Image.frombytes('RGB', (폭, uzunluq_VALUE), EXACT_VALUE(uzaq_VALUE, 폭*uzunluq_VALUE*4), 'raw', 'BGRX'), (가로, Şaquli_yerinə_qoymaq))
                sahə_VALUE_9285603e += 폭*uzunluq_VALUE
            if sahə_VALUE_9285603e:
                assert sahə_VALUE_9285603e == 너비*높이, sahə_VALUE_9285603e
                return rəsm_VALUE

    def çek_piksel(koordinat_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            rəsm_VALUE = nöqtəli_təsvir_IMAGE()
            if rəsm_VALUE.getpixel(koordinat_VALUE) == 색: return rəsm_VALUE
            if time.monotonic() > 마감: raise AssertionError((koordinat_VALUE, rəsm_VALUE.getpixel(koordinat_VALUE), 색))

    def Upload_Fayllar(Ad, verilənlər): ötürmə_VALUE.storbinary('STOR '+Ad, io.BytesIO(verilənlər))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ölçünü_dəyişmək_SMS+' RGB32').encode() in LOG_yaz
        print('BOOT:', ölçünü_dəyişmək_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_yaz).group(1))
        uzaq_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(uzaq_VALUE, 12) == b'RFB 003.008\n'; uzaq_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(uzaq_VALUE, EXACT_VALUE(uzaq_VALUE, 1)[0]); uzaq_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(uzaq_VALUE, 4) == b'\0'*4; uzaq_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(uzaq_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(uzaq_VALUE, struct.unpack('>I', 초기[20:])[0])
        uzaq_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzaq_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        çek_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for hadisə,_ in seçici_a916db4e.select(.02):
                    verilənlər=hadisə.fileobj.read(65536)
                    if verilənlər:LOG_yaz.extend(verilənlər)
        pəncərə=[12,48,568,360]
        def yoxlamaq_ölçünü_dəyişmək():
            sütun_VALUE,ROW_VALUE=(pəncərə[2]-24)//8,(pəncərə[3]-56)//16
            Mətn=örtük('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(sütun_VALUE,ROW_VALUE) in Mətn,Mətn
            # faktiki_verilənlər pəncərə 테두리: 단지 Böyüklük sorğu_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            çek_piksel((pəncərə[0],pəncərə[1]),(32,80,144))
            rəsm_VALUE=çek_piksel((pəncərə[0]+pəncərə[2]-1,pəncərə[1]+pəncərə[3]-1),(39,49,64))
            return rəsm_VALUE
        def 모서리(방향):
            return (pəncərə[0]+(3 if 방향 in (1,3) else pəncərə[2]-4),pəncərə[1]+(3 if 방향<=2 else pəncərə[3]-4))
        def ölçüsünü_dəyişmək_sürükləmək(방향,차이,düymə=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            çek_piksel(흰점,(255,255,255))
            가리키기(가,세,düymə)
            끝가=max(0,min(너비-1,가+차이[0]));bitirmək_Şaquli=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,bitirmək_Şaquli,düymə);가리키기(끝가,bitirmək_Şaquli,0);숨고르기()
            if düymə==1:
                LEFT_VALUE,위,폭,uzunluq_VALUE=pəncərə;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+uzunluq_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+bitirmək_Şaquli-세))
                else:아래=max(위+216,min(높이,아래+bitirmək_Şaquli-세))
                pəncərə[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        yoxlamaq_ölçünü_dəyişmək();assert göstərici_gizli[0]
        ölçüsünü_dəyişmək_sürükləmək(4,(-100,-60),4);yoxlamaq_ölçünü_dəyişmək() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ölçüsünü_dəyişmək_sürükləmək(방향,차이);yoxlamaq_ölçünü_dəyişmək()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_göndər("echo '"+긴글+"'");숨고르기()
        ölçüsünü_dəyişmək_sürükləmək(4,(-1000,-1000));assert pəncərə[2:]==[360,216]
        ölçüsünü_dəyişmək_sürükləmək(4,(너비,높이))
        İcra_Et=SMS_göndər('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),İcra_Et);yoxlamaq_ölçünü_dəyişmək()
        # vi가 redaktə_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        örtük('ftpd start')
        ötürmə_VALUE=ftplib.FTP();ötürmə_VALUE.encoding='utf-8';ötürmə_VALUE.connect('127.0.0.1',접속번호,timeout=20);ötürmə_VALUE.login()
        기다리기(b'NORMAL',SMS_göndər('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_göndər('i미저장 한글 verilənlər\n'));숨고르기()
        ölçüsünü_dəyişmək_sürükləmək(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((pəncərə[3]-56)//16)).encode() in LOG_yaz[-4096:]
        SMS_göndər('작은 창에서도 이어 Yazma\n');숨고르기()
        ölçüsünü_dəyişmək_sürükləmək(4,(너비,높이))
        SMS_göndər('큰 창에서도 이어 Yazma\n');숨고르기()
        klikləmə_düymə(0xff1b);klikləmə_düymə(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_göndər(':wq\n'))
        Məzmun_VALUE=bytearray();ötürmə_VALUE.retrbinary('RETR 크기자료.txt',Məzmun_VALUE.extend)
        assert Məzmun_VALUE=='미저장 한글 verilənlər\n작은 창에서도 이어 Yazma\n큰 창에서도 이어 Yazma\n'.encode(),Məzmun_VALUE
        yoxlamaq_ölçünü_dəyişmək().save(str(ölçü_yol/(ölçünü_dəyişmək_SMS+'-large.png')))
        # 두 번째 창은 standart_qiymət Böyüklük, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        İcra_Et=len(LOG_yaz);klikləmə_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',İcra_Et)
        assert 'TERMINAL SIZE 68x19' in örtük('terminal size')
        İcra_Et=len(LOG_yaz);klikləmə_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',İcra_Et);yoxlamaq_ölçünü_dəyişmək()
        ölçüsünü_dəyişmək_sürükləmək(4,(-너비,-높이));yoxlamaq_ölçünü_dəyişmək().save(str(ölçü_yol/(ölçünü_dəyişmək_SMS+'-small.png')))
        # Böyüklük dəyişdirmək_VALUE GERİ_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        İcra_Et=len(LOG_yaz);klikləmə_VALUE(pəncərə[0]+pəncərə[2]-20,pəncərə[1]+15);기다리기(b'TERMINAL FOCUS 2',İcra_Et)
        assert 'RESIZE CLOSED' in örtük('echo RESIZE CLOSED')
        print('PASS:',ölçünü_dəyişmək_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ötürmə_VALUE:ötürmə_VALUE.close()
        if uzaq_VALUE:uzaq_VALUE.close()
        if Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:Proses_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
        seçici_a916db4e.close();Proses_VALUE.stdout.close();(ölçü_yol/(ölçünü_dəyişmək_SMS+'.log')).write_bytes(LOG_yaz)


def İcra_Et():
    ölçü_yol=Project_kök/'build/verification/resize';ölçü_yol.mkdir(parents=True,exist_ok=True)
    LOG_yaz={'passed':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ölçü_yol);LOG_yaz['resolutions'].append([너비,높이])
        LOG_yaz.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ölçü_yol/'report.json').write_text(json.dumps(LOG_yaz,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':İcra_Et()
