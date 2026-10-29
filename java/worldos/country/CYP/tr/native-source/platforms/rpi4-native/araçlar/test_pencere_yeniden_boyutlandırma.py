#!/usr/bin/env python3
"""fiili_veri QEMU/VNC에서 uçbirim 모서리 sürüklemek_değer·işaretçi·동적 karakter_değer yuva_girdi·Düzenle_değer içerik_değer 보존를 검사한다."""
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
from Masaüstü_Görünüm import ÖZDEŞ_değer
from yürütmek_komut import işlem_kök


def test_pencere_yeniden_boyutlandırma(너비, 높이, KR_yol):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); bağlantı_noktası_numarası = 임시.getsockname()[1]
    boyutlandırmak_SMS = '{}x{}'.format(너비, 높이)
    işlem_değer = subprocess.Popen(['python3', str(işlem_kök/'araçlar/yürütmek_komut.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(bağlantı_noktası_numarası), '--resolution', boyutlandırmak_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector(); seçici_a916db4e.register(işlem_değer.stdout, selectors.EVENT_READ)
    LOG_KAYIT = bytearray(); uzak_değer = None; devir_değer = None; işaretçi_Gizli=[False]

    def 기다리기(şov_değer, çalıştır=0):
        son_tarih_değer = time.monotonic() + 60
        while şov_değer not in LOG_KAYIT[çalıştır:]:
            if time.monotonic() > son_tarih_değer or işlem_değer.poll() is not None or b'HALTED' in LOG_KAYIT or b'PANIC:' in LOG_KAYIT:
                raise AssertionError(LOG_KAYIT[çalıştır:].decode('utf-8', 'replace'))
            for Olay, _ in seçici_a916db4e.select(.1):
                veri = Olay.fileobj.read(65536)
                if veri: LOG_KAYIT.extend(veri)
        return LOG_KAYIT[çalıştır:].decode('utf-8', 'replace')

    def tık_düğme(simge, 눌림=True): uzak_değer.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simge))

    def SMS_gönderme(metin):
        çalıştır = len(LOG_KAYIT)
        for karakter_değer in metin:
            simge = 0xff0d if karakter_değer == '\n' else ord(karakter_değer) if ord(karakter_değer) < 256 else 0x1000000 | ord(karakter_değer)
            tık_düğme(simge); tık_düğme(simge, False)
        return çalıştır

    def kabuk(metin): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_gönderme(metin+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Dikey_konum, 눌림): uzak_değer.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Dikey_konum))

    def tık_değer(가로, Dikey_konum): 가리키기(가로, Dikey_konum, 1); 가리키기(가로, Dikey_konum, 0)

    def bit_eşlem_RESİM():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 fiili_veri 너비를 쓴다.
        uzak_değer.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        çizim_değer = Image.new('RGB', (너비, 높이)); alan_değer_9285603e = 0
        while True:
            Tip_değer = ÖZDEŞ_değer(uzak_değer, 1)[0]
            if Tip_değer == 2: continue
            if Tip_değer == 3:
                süre_değer = struct.unpack('>I', ÖZDEŞ_değer(uzak_değer, 7)[3:])[0]; ÖZDEŞ_değer(uzak_değer, süre_değer); continue
            assert Tip_değer == 0, Tip_değer
            öğe_BAĞ_DEĞ_SAY = struct.unpack('>H', ÖZDEŞ_değer(uzak_değer, 3)[1:])[0]
            for _ in range(öğe_BAĞ_DEĞ_SAY):
                가로, Dikey_konum, 폭, süre_değer, kodlama_değer = struct.unpack('>HHHHi', ÖZDEŞ_değer(uzak_değer, 12))
                if kodlama_değer == -239:
                    assert 폭==0 and süre_değer==0, 'remote cursor must be hidden'
                    işaretçi_Gizli[0]=True
                    continue
                assert kodlama_değer == 0 and 가로+폭 <= 너비 and Dikey_konum+süre_değer <= 높이
                çizim_değer.paste(Image.frombytes('RGB', (폭, süre_değer), ÖZDEŞ_değer(uzak_değer, 폭*süre_değer*4), 'raw', 'BGRX'), (가로, Dikey_konum))
                alan_değer_9285603e += 폭*süre_değer
            if alan_değer_9285603e:
                assert alan_değer_9285603e == 너비*높이, alan_değer_9285603e
                return çizim_değer

    def çek_piksel(koordinat_değer, 색):
        son_tarih_değer = time.monotonic()+10
        while True:
            çizim_değer = bit_eşlem_RESİM()
            if çizim_değer.getpixel(koordinat_değer) == 색: return çizim_değer
            if time.monotonic() > son_tarih_değer: raise AssertionError((koordinat_değer, çizim_değer.getpixel(koordinat_değer), 색))

    def yükle_Dosyalar(İsim, veri): devir_değer.storbinary('STOR '+İsim, io.BytesIO(veri))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+boyutlandırmak_SMS+' RGB32').encode() in LOG_KAYIT
        print('BOOT:', boyutlandırmak_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_KAYIT).group(1))
        uzak_değer = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert ÖZDEŞ_değer(uzak_değer, 12) == b'RFB 003.008\n'; uzak_değer.sendall(b'RFB 003.008\n')
        assert 1 in ÖZDEŞ_değer(uzak_değer, ÖZDEŞ_değer(uzak_değer, 1)[0]); uzak_değer.sendall(b'\x01')
        assert ÖZDEŞ_değer(uzak_değer, 4) == b'\0'*4; uzak_değer.sendall(b'\x01')
        başlangıç_durumu = ÖZDEŞ_değer(uzak_değer, 24); assert struct.unpack('>HH', başlangıç_durumu[:4]) == (너비, 높이)
        ÖZDEŞ_değer(uzak_değer, struct.unpack('>I', başlangıç_durumu[20:])[0])
        uzak_değer.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        uzak_değer.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        çek_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Olay,_ in seçici_a916db4e.select(.02):
                    veri=Olay.fileobj.read(65536)
                    if veri:LOG_KAYIT.extend(veri)
        Pencere=[12,48,568,360]
        def doğrulamak_boyutlandırmak():
            SÜTUN_değer,SATIR_değer=(Pencere[2]-24)//8,(Pencere[3]-56)//16
            metin=kabuk('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(SÜTUN_değer,SATIR_değer) in metin,metin
            # fiili_veri Pencere 테두리: 단지 Boyut sorgu_değer 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            çek_piksel((Pencere[0],Pencere[1]),(32,80,144))
            çizim_değer=çek_piksel((Pencere[0]+Pencere[2]-1,Pencere[1]+Pencere[3]-1),(39,49,64))
            return çizim_değer
        def 모서리(방향):
            return (Pencere[0]+(3 if 방향 in (1,3) else Pencere[2]-4),Pencere[1]+(3 if 방향<=2 else Pencere[3]-4))
        def yeniden_boyutlandırmak_sürüklemek(방향,차이,düğme=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            çek_piksel(흰점,(255,255,255))
            가리키기(가,세,düğme)
            끝가=max(0,min(너비-1,가+차이[0]));Bitiş_Dikey=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,Bitiş_Dikey,düğme);가리키기(끝가,Bitiş_Dikey,0);숨고르기()
            if düğme==1:
                SOLDAN_değer,위,폭,süre_değer=Pencere;hak_değer,아래=SOLDAN_değer+폭,위+süre_değer
                if 방향 in (1,3):SOLDAN_değer=max(0,min(hak_değer-360,SOLDAN_değer+끝가-가))
                else:hak_değer=max(SOLDAN_değer+360,min(너비,hak_değer+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+Bitiş_Dikey-세))
                else:아래=max(위+216,min(높이,아래+Bitiş_Dikey-세))
                Pencere[:]=[SOLDAN_değer,위,hak_değer-SOLDAN_değer,아래-위]
        doğrulamak_boyutlandırmak();assert işaretçi_Gizli[0]
        yeniden_boyutlandırmak_sürüklemek(4,(-100,-60),4);doğrulamak_boyutlandırmak() # hak 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            yeniden_boyutlandırmak_sürüklemek(방향,차이);doğrulamak_boyutlandırmak()
        # artış_değer 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_gönderme("echo '"+긴글+"'");숨고르기()
        yeniden_boyutlandırmak_sürüklemek(4,(-1000,-1000));assert Pencere[2:]==[360,216]
        yeniden_boyutlandırmak_sürüklemek(4,(너비,높이))
        çalıştır=SMS_gönderme('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),çalıştır);doğrulamak_boyutlandırmak()
        # vi가 Düzenle_değer 중에 화면 크기를 yeniden_denemek_değer 읽고, 저장하지 않은 한글도 유지한다.
        kabuk('ftpd start')
        devir_değer=ftplib.FTP();devir_değer.encoding='utf-8';devir_değer.connect('127.0.0.1',bağlantı_noktası_numarası,timeout=20);devir_değer.login()
        기다리기(b'NORMAL',SMS_gönderme('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_gönderme('i미저장 한글 veri\n'));숨고르기()
        yeniden_boyutlandırmak_sürüklemek(4,(-너비,-높이))
        # ANSI SATIR_değer 이동에 새 SATIR_değer 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Pencere[3]-56)//16)).encode() in LOG_KAYIT[-4096:]
        SMS_gönderme('작은 창에서도 이어 Yazma\n');숨고르기()
        yeniden_boyutlandırmak_sürüklemek(4,(너비,높이))
        SMS_gönderme('큰 창에서도 이어 Yazma\n');숨고르기()
        tık_düğme(0xff1b);tık_düğme(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_gönderme(':wq\n'))
        içerik_değer=bytearray();devir_değer.retrbinary('RETR 크기자료.txt',içerik_değer.extend)
        assert içerik_değer=='미저장 한글 veri\n작은 창에서도 이어 Yazma\n큰 창에서도 이어 Yazma\n'.encode(),içerik_değer
        doğrulamak_boyutlandırmak().save(str(KR_yol/(boyutlandırmak_SMS+'-large.png')))
        # 두 번째 창은 varsayılan_değer Boyut, yeniden_denemek_değer 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        çalıştır=len(LOG_KAYIT);tık_değer(70,16);기다리기(b'TERMINAL FOCUS 2',çalıştır)
        assert 'TERMINAL SIZE 68x19' in kabuk('terminal size')
        çalıştır=len(LOG_KAYIT);tık_değer(180,16);기다리기(b'TERMINAL FOCUS 1',çalıştır);doğrulamak_boyutlandırmak()
        yeniden_boyutlandırmak_sürüklemek(4,(-너비,-높이));doğrulamak_boyutlandırmak().save(str(KR_yol/(boyutlandırmak_SMS+'-small.png')))
        # Boyut değiştirmek_değer BACK_değer X 닫기도 새로운 hak 가장자리를 사용한다.
        çalıştır=len(LOG_KAYIT);tık_değer(Pencere[0]+Pencere[2]-20,Pencere[1]+15);기다리기(b'TERMINAL FOCUS 2',çalıştır)
        assert 'RESIZE CLOSED' in kabuk('echo RESIZE CLOSED')
        print('PASS:',boyutlandırmak_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if devir_değer:devir_değer.close()
        if uzak_değer:uzak_değer.close()
        if işlem_değer.poll() is None:
            işlem_değer.terminate()
            try:işlem_değer.wait(timeout=8)
            except subprocess.TimeoutExpired:işlem_değer.kill();işlem_değer.wait()
        seçici_a916db4e.close();işlem_değer.stdout.close();(KR_yol/(boyutlandırmak_SMS+'.log')).write_bytes(LOG_KAYIT)


def çalıştır():
    KR_yol=işlem_kök/'build/verification/resize';KR_yol.mkdir(parents=True,exist_ok=True)
    LOG_KAYIT={'passed':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            test_pencere_yeniden_boyutlandırma(너비,높이,KR_yol);LOG_KAYIT['resolutions'].append([너비,높이])
        LOG_KAYIT.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_yol/'report.json').write_text(json.dumps(LOG_KAYIT,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':çalıştır()
